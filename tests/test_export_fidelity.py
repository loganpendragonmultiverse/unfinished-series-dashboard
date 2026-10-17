import json
from pathlib import Path

import pytest

from unfinished_series_dashboard.cli import main
from unfinished_series_dashboard.core import build_report, load_dashboard


def source_file(path, **fields):
    path.write_text(
        json.dumps(
            {"version": 1, "series": [{"id": "a", "title": "A", "status": "delayed", **fields}]}
        )
    )
    return path


@pytest.mark.parametrize("fmt", ["json", "markdown", "html"])
def test_concurrent_output_is_preserved(tmp_path, monkeypatch, capsys, fmt):
    source = source_file(tmp_path / "input.json")
    before = source.read_bytes()
    target = tmp_path / "report"
    original_open = Path.open

    def racing_open(path, mode="r", *args, **kwargs):
        if path == target and mode in {"w", "x"}:
            with original_open(path, "w", encoding="utf-8") as stream:
                stream.write("Concurrent report")
        return original_open(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, "open", racing_open)
    assert main([str(source), "--format", fmt, "--output", str(target)]) == 2
    assert "error:" in capsys.readouterr().err
    assert target.read_text() == "Concurrent report"
    assert source.read_bytes() == before


@pytest.mark.parametrize("after", [None, "", "missing"])
def test_authored_unknown_date_changes_survive_comparison(tmp_path, capsys, after):
    old = source_file(tmp_path / "old.json", next_release="unknown")
    new = source_file(
        tmp_path / "new.json", **({} if after == "missing" else {"next_release": after})
    )
    before = (old.read_bytes(), new.read_bytes())
    assert main([str(new), "--compare", str(old), "--format", "json"]) == 0
    change = json.loads(capsys.readouterr().out)["comparison"]["changed"][0]["fields"][0]
    assert change["field"] == "next_release" and change["before"] == "unknown"
    assert change["after_present"] == (after != "missing")
    assert change["after"] == (None if after == "missing" else after)
    assert (old.read_bytes(), new.read_bytes()) == before
    report = build_report(load_dashboard(old), as_of="2026-10-17")
    assert report["series"][0]["date_bucket"] == "unknown"
    assert report["series"][0]["next_release"] == "unknown"
