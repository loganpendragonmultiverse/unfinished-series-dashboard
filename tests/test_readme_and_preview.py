import json
from pathlib import Path

import pytest

from unfinished_series_dashboard.cli import main
from unfinished_series_dashboard.core import build_report, load_dashboard
from unfinished_series_dashboard.preview import render_html


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["--status", "delayed", "--format", "json"],
        ["--as-of", "2026-07-27", "--date-bucket", "overdue"],
        ["--format", "html"],
    ],
)
def test_exact_readme_commands(args) -> None:
    assert main([str(Path(__file__).parents[1] / "examples/series.json"), *args]) == 0


def test_unknown_dates_progress_and_escaped_notes(tmp_path) -> None:
    source = tmp_path / "input.json"
    source.write_text(
        json.dumps(
            {
                "version": 1,
                "series": [
                    {
                        "id": "a",
                        "title": "A",
                        "status": "delayed",
                        "next_release": "unknown",
                        "completed_volumes": 2,
                        "total_volumes": 4,
                        "source_notes": "</script><script>bad</script>",
                    }
                ],
            }
        )
    )
    report = build_report(load_dashboard(source), as_of="2026-09-07")
    assert report["series"][0]["progress_percent"] == 50
    assert report["series"][0]["date_bucket"] == "unknown"
    assert "</script><script>bad" not in render_html(report)
    assert "Source and verification notes" in render_html(report)
