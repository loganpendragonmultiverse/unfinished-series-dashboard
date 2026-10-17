"""Deterministic comparison of explicit, validated snapshots."""

from __future__ import annotations

import copy
import html
import json
from typing import Any

from .json_equality import json_equal


def compare_snapshots(before: list[dict[str, Any]], after: list[dict[str, Any]]) -> dict[str, Any]:
    old = {item["id"]: item for item in before}
    new = {item["id"]: item for item in after}
    changed = []
    unchanged = []
    for identity in sorted(old.keys() & new.keys()):
        fields = []
        for field in sorted((old[identity].keys() | new[identity].keys()) - {"id"}):
            a, b = old[identity], new[identity]
            if (field in a) != (field in b) or not json_equal(a.get(field), b.get(field)):
                fields.append(
                    {
                        "field": field,
                        "before_present": field in a,
                        "after_present": field in b,
                        "before": copy.deepcopy(a.get(field)),
                        "after": copy.deepcopy(b.get(field)),
                    }
                )
        if fields:
            changed.append({"id": identity, "fields": fields})
        else:
            unchanged.append(identity)
    return {
        "previous_count": len(old),
        "current_count": len(new),
        "added": [copy.deepcopy(new[k]) for k in sorted(new.keys() - old.keys())],
        "removed": [copy.deepcopy(old[k]) for k in sorted(old.keys() - new.keys())],
        "changed": changed,
        "unchanged_ids": unchanged,
    }


def comparison_markdown(value: dict[str, Any]) -> str:
    return (
        "\n## Snapshot comparison\n\n```json\n"
        + json.dumps(value, indent=2, ensure_ascii=False)
        + "\n```\n"
    )


def comparison_html(value: dict[str, Any]) -> str:
    return (
        '<section aria-label="Snapshot comparison"><h2>Snapshot comparison</h2><pre style="white-space:pre-wrap;overflow-wrap:anywhere">'
        + html.escape(json.dumps(value, indent=2, ensure_ascii=False))
        + "</pre></section>"
    )
