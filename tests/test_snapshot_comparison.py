import copy
import json
from pathlib import Path

from unfinished_series_dashboard.cli import main
from unfinished_series_dashboard.comparison import compare_snapshots


def test_snapshot_add_remove_change_and_reorder():
    before = [
        {"id": "a", "title": "Old", "status": "delayed"},
        {"id": "gone", "title": "Gone", "status": "complete"},
    ]
    after = [
        {"id": "new", "title": "New", "status": "incomplete"},
        {"id": "a", "title": "New title", "status": "complete"},
    ]
    original = copy.deepcopy((before, after))
    value = compare_snapshots(before, after)
    assert value["added"][0]["id"] == "new"
    assert value["removed"][0]["id"] == "gone"
    assert {x["field"] for x in value["changed"][0]["fields"]} == {"title", "status"}
    assert value == compare_snapshots(list(reversed(before)), list(reversed(after)))
    assert (before, after) == original
    assert compare_snapshots(after, after)["unchanged_ids"] == ["a", "new"]


def test_snapshot_cli_formats_validation_and_escaping(tmp_path: Path, capsys):
    old = tmp_path / "old.json"
    new = tmp_path / "new.json"
    old.write_text(
        json.dumps(
            {
                "version": 1,
                "series": [
                    {
                        "id": "a",
                        "title": "Before",
                        "status": "delayed",
                        "notes": "</script><img src=x>",
                    }
                ],
            }
        )
    )
    new.write_text(
        json.dumps({"version": 1, "series": [{"id": "a", "title": "After", "status": "complete"}]})
    )
    for fmt in ["json", "markdown", "html"]:
        assert main([str(new), "--compare", str(old), "--format", fmt]) == 0
        text = capsys.readouterr().out
        assert "comparison" in text.lower()
        if fmt == "html":
            assert "<img src=x>" not in text
    assert main([str(new), "--compare", str(old), "--status", "delayed"]) == 2
    old.write_text('{"version":1,"series":[{}]}')
    assert main([str(new), "--compare", str(old)]) == 2
