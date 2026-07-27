from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

STATUSES = {"incomplete", "abandoned", "delayed", "still-writing", "complete"}


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
        seen.add(item_id)
    return data


def build_report(data: dict[str, Any], statuses: set[str] | None = None) -> dict[str, Any]:
    if statuses and not statuses <= STATUSES:
        raise ValueError("unknown status filter")
    selected = [item for item in data["series"] if not statuses or item["status"] in statuses]
    selected.sort(key=lambda item: (item["status"], item["title"].casefold()))
    counts = Counter(item["status"] for item in selected)
    return {
        "version": 1,
        "total": len(selected),
        "counts": {status: counts.get(status, 0) for status in sorted(STATUSES)},
        "series": selected,
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
