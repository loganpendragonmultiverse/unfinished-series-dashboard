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
