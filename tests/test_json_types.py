import pytest

from unfinished_series_dashboard.json_equality import json_equal


@pytest.mark.parametrize(
    "left,right", [(True, 1), (False, 0), ({"a": [True]}, {"a": [1]}), (None, ""), ([1, 2], [2, 1])]
)
def test_json_type_or_value_change(left, right):
    assert not json_equal(left, right)


@pytest.mark.parametrize(
    "left,right", [(1, 1.0), ({"a": True, "b": [None, 1]}, {"b": [None, 1.0], "a": True}), ([], [])]
)
def test_equal_json_values(left, right):
    assert json_equal(left, right)


def test_snapshot_comparison_distinguishes_nested_boolean_and_number():
    from unfinished_series_dashboard.comparison import compare_snapshots

    report = compare_snapshots(
        [{"id": "a", "extra": {"flag": True}}], [{"id": "a", "extra": {"flag": 1}}]
    )
    assert report["changed"][0]["fields"][0]["field"] == "extra" and not report["unchanged_ids"]
