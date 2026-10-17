import json
from pathlib import Path

import pytest

from unfinished_series_dashboard.cli import main
from unfinished_series_dashboard.core import build_report, load_dashboard
from unfinished_series_dashboard.preview import render_html


def inventory(tmp_path: Path, value):
    path = tmp_path / "series.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "series": [{"id": "a", "title": "A", "status": "delayed", "next_release": value}],
            }
        )
    )
    return path


@pytest.mark.parametrize(
    "value", ["20261017", "2026-W42-6", "2026-02-30", "2026-1-1", "0000-01-01", False, 0, []]
)
def test_invalid_release_date_is_actionable_and_writes_nothing(tmp_path, capsys, value):
    source = inventory(tmp_path, value)
    before = source.read_bytes()
    target = tmp_path / "report.json"
    assert main([str(source), "--output", str(target)]) == 2
    assert "next_release must be YYYY-MM-DD" in capsys.readouterr().err
    assert not target.exists() and source.read_bytes() == before


@pytest.mark.parametrize("value", ["20261017", "2026-W42-6", "2026-02-30", ""])
def test_as_of_has_the_same_canonical_contract(tmp_path, capsys, value):
    source = inventory(tmp_path, None)
    assert main([str(source), "--as-of", value]) == 2
    assert "as_of must be YYYY-MM-DD" in capsys.readouterr().err


@pytest.mark.parametrize("value", [None, "", "unknown"])
def test_unknown_dates_remain_supported(tmp_path, value):
    source = inventory(tmp_path, value)
    report = build_report(load_dashboard(source), as_of="2026-10-17")
    assert report["series"][0]["date_bucket"] == "unknown"


def test_canonical_date_buckets_and_browser_export_guard(tmp_path):
    source = inventory(tmp_path, "2026-01-01")
    report = build_report(load_dashboard(source), as_of="2026-10-17")
    assert report["series"][0]["date_bucket"] == "overdue"
    html = render_html(report)
    assert "function validDate" in html and "!validDate(item.next_release)" in html
    assert "YYYY-MM-DD or blank" in html
