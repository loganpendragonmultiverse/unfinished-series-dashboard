import json

import pytest

from unfinished_series_dashboard.cli import main
from unfinished_series_dashboard.core import build_report, load_dashboard, render_markdown


def sample():
    return {
        "version": 1,
        "series": [
            {
                "id": "a",
                "title": "Long Wait",
                "status": "delayed",
                "reader_status": "book 2",
                "owned_volumes": 4,
                "completed_volumes": 2,
                "priority": 5,
                "next_release": "2026-01-01",
                "format": "ebook",
                "publisher": "North",
                "author": "Lee",
            },
            {"id": "b", "title": "Done", "status": "complete", "reader_status": "finished"},
        ],
    }


def test_report_filters_and_renders():
    report = build_report(sample(), {"delayed"})
    assert report["total"] == 1
    assert report["counts"]["delayed"] == 1
    assert report["version"] == 2 and report["resume_queue"][0]["title"] == "Long Wait"
    assert "Long Wait" in render_markdown(report)
    with pytest.raises(ValueError, match="unknown"):
        build_report(sample(), {"lost"})


def test_date_buckets_and_filters():
    report = build_report(
        sample(),
        as_of="2026-07-27",
        date_buckets={"overdue"},
        formats={"ebook"},
        publishers={"North"},
        authors={"Lee"},
        reader_statuses={"book 2"},
    )
    assert report["total"] == 1 and report["series"][0]["remaining_owned"] == 2
    with pytest.raises(ValueError, match="date bucket"):
        build_report(sample(), date_buckets={"later"})


def test_load_validates(tmp_path):
    path = tmp_path / "series.json"
    path.write_text(json.dumps(sample()), encoding="utf-8")
    assert load_dashboard(path)["series"][0]["id"] == "a"
    path.write_text('{"version": 1, "series": [{"id": "a"}]}', encoding="utf-8")
    with pytest.raises(ValueError, match="title"):
        load_dashboard(path)


@pytest.mark.parametrize(
    ("payload", "error"),
    [
        ({"version": 2}, ValueError),
        ({"version": 1, "series": {}}, TypeError),
        ({"version": 1, "series": [None]}, TypeError),
        ({"version": 1, "series": [{"id": "", "title": "A", "status": "complete"}]}, ValueError),
        ({"version": 1, "series": [{"id": "a", "title": "A", "status": "lost"}]}, ValueError),
    ],
)
def test_rejects_invalid_dashboard_shapes(tmp_path, payload, error):
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(error):
        load_dashboard(path)


def test_cli_json_and_refuses_replace(tmp_path, capsys):
    path = tmp_path / "series.json"
    path.write_text(json.dumps(sample()), encoding="utf-8")
    assert (
        main([str(path), "--format", "json", "--status", "complete", "--as-of", "2026-07-27"]) == 0
    )
    assert '"total": 1' in capsys.readouterr().out
    output = tmp_path / "report.md"
    output.write_text("keep", encoding="utf-8")
    assert main([str(path), "--output", str(output)]) == 2
    assert output.read_text(encoding="utf-8") == "keep"
    fresh = tmp_path / "fresh.md"
    assert main([str(path), "--output", str(fresh)]) == 0
    assert "Done" in fresh.read_text(encoding="utf-8")
