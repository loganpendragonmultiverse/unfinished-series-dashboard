from __future__ import annotations

import json
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

STATUSES = {"incomplete", "abandoned", "delayed", "still-writing", "complete"}
DATE_BUCKETS = {"upcoming", "overdue", "unknown", "stale"}


def load_dashboard(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("version") != 1:
        raise ValueError("input must be a version 1 dashboard object")
    series = data.get("series")
    if not isinstance(series, list):
        raise TypeError("series must be a list")
    seen: set[str] = set()
    for index, item in enumerate(series, 1):
        if not isinstance(item, dict):
            raise TypeError(f"series item {index} must be an object")
        item_id = item.get("id")
        title = item.get("title")
        status = item.get("status")
        if not isinstance(item_id, str) or not item_id.strip() or item_id in seen:
            raise ValueError(f"series item {index} has a missing or duplicate id")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"series item {index} requires a title")
        if status not in STATUSES:
            raise ValueError(f"series item {index} has unsupported status {status!r}")
        for field in ("owned_volumes", "completed_volumes", "total_volumes", "priority"):
            value = item.get(field)
            if value is not None and (not isinstance(value, int) or value < 0):
                raise ValueError(f"series item {index} {field} must be a non-negative integer")
        if item.get("next_release"):
            try:
                date.fromisoformat(str(item["next_release"]))
            except ValueError as exc:
                raise ValueError(f"series item {index} next_release must be YYYY-MM-DD") from exc
        seen.add(item_id)
    return data


def build_report(
    data: dict[str, Any],
    statuses: set[str] | None = None,
    *,
    as_of: str | None = None,
    date_buckets: set[str] | None = None,
    formats: set[str] | None = None,
    publishers: set[str] | None = None,
    authors: set[str] | None = None,
    reader_statuses: set[str] | None = None,
) -> dict[str, Any]:
    if statuses and not statuses <= STATUSES:
        raise ValueError("unknown status filter")
    if date_buckets and not date_buckets <= DATE_BUCKETS:
        raise ValueError("unknown date bucket filter")
    today = date.fromisoformat(as_of) if as_of else datetime.now(timezone.utc).date()
    selected = []
    for original in data["series"]:
        item = dict(original)
        next_release = item.get("next_release")
        if not next_release:
            bucket = "unknown"
        elif date.fromisoformat(str(next_release)) < today:
            bucket = "stale" if item["status"] == "complete" else "overdue"
        else:
            bucket = "upcoming"
        owned = int(item.get("owned_volumes", 0))
        completed = int(item.get("completed_volumes", 0))
        total = item.get("total_volumes")
        item["date_bucket"] = bucket
        item["remaining_owned"] = max(owned - completed, 0)
        item["remaining_total"] = max(int(total) - completed, 0) if total is not None else None
        if statuses and item["status"] not in statuses:
            continue
        if date_buckets and bucket not in date_buckets:
            continue
        filters = (
            (formats, "format"),
            (publishers, "publisher"),
            (authors, "author"),
            (reader_statuses, "reader_status"),
        )
        if any(values and str(item.get(field, "")) not in values for values, field in filters):
            continue
        selected.append(item)
    selected.sort(key=lambda item: (-int(item.get("priority", 0)), item["title"].casefold()))
    counts = Counter(item["status"] for item in selected)
    return {
        "version": 2,
        "as_of": today.isoformat(),
        "total": len(selected),
        "counts": {status: counts.get(status, 0) for status in sorted(STATUSES)},
        "series": selected,
        "resume_queue": [
            {
                "id": item["id"],
                "title": item["title"],
                "priority": item.get("priority", 0),
                "next_action": item.get("next_action", "Resume the next unread volume."),
            }
            for item in selected
            if item["status"] != "complete" and item["remaining_owned"] > 0
        ],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Unfinished Series Dashboard", "", f"Tracked series: **{report['total']}**", ""]
    for status in sorted(STATUSES):
        items = [item for item in report["series"] if item["status"] == status]
        if not items:
            continue
        lines.extend([f"## {status.replace('-', ' ').title()} ({len(items)})", ""])
        for item in items:
            detail = item.get("reader_status", "status not recorded")
            next_release = item.get("next_release")
            suffix = f"; next: {next_release}" if next_release else ""
            lines.append(f"- **{item['title']}** — {detail}{suffix}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"
