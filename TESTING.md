# Testing

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`. CI also audits dependencies and runs the supported OS/Python matrix.

## 1.2.0 regression acceptance

Run the complete existing suite plus the new regression fixtures. Confirm the documented command produces the selected output, malformed input remains actionable, and source files remain unchanged. Support unknown release dates and add a local series editor with progress bars, source notes and stale-date review.

## 1.3.0 acceptance

Compare saved series inventories by stable ID without looking up or inventing publication facts.

Verify Report added, removed, changed and unchanged series between two validated input snapshots; Compare authored fields without derived date/progress noise; Render comparison evidence in JSON, Markdown and escaped local HTML. Run the full existing quality and build gates; release only through protected PR checks and verified tag artifacts.

## 1.3.1 acceptance

Report boolean-to-number changes accurately in JSON comparison evidence.

Verify Distinguish JSON booleans from numbers recursively in objects and arrays; Retain numeric equality for 1 and 1.0, object key-order independence and list order; Add regressions against the public comparison entry point. Run the full existing quality and build gates; release only through protected PR checks and verified tag artifacts.

## 1.3.2 canonical dates

Require exact YYYY-MM-DD calendar dates for next_release and as_of across Python 3.10 and newer; retain null/blank/unknown release dates. Reject compact/week/non-text/invalid dates before creating output. Verify the browser download guard and canonical stale-date filtering, with original bytes unchanged.

## 1.4.0 output and snapshot fidelity

Create JSON, Markdown and HTML reports exclusively and preserve a destination created immediately before opening. Keep authored unknown, null, blank and missing release dates distinct in snapshot comparisons while treating each as an unknown date for dashboard filtering. Preserve source bytes and unchanged browser-export values.

The browser editor supports adding and removing records, including an empty inventory. Reject duplicate/blank IDs and titles, invalid statuses, fractional/negative/unsafe counts and invalid dates before download. Preserve untouched authored values and extra fields. Test add/edit/remove/download and CLI revalidation in Chromium, Firefox and WebKit, including filtered reports; original input bytes must stay unchanged.

For optional real-browser acceptance, install Playwright and its Chromium, Firefox and WebKit browsers, then run `python scripts/check_editor_browser.py` against an installed candidate (or with `PYTHONPATH=src`). The script creates disposable inputs, exercises add/edit/remove/download and validates saved JSON with the CLI. Playwright is a test tool, not a runtime dependency.
