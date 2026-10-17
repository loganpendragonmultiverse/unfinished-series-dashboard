# Changelog

## 1.3.2

- Validate canonical YYYY-MM-DD release/as-of dates consistently across supported Python versions.
- Guard browser exports against invalid dates and preserve unknown-date and stale-review behavior.

## 1.3.1 - 2026-10-17

- Distinguish JSON booleans from numbers recursively in objects and arrays
- Retain numeric equality for 1 and 1.0, object key-order independence and list order
- Add regressions against the public comparison entry point

## 1.3.0 - 2026-10-17

- Report added, removed, changed and unchanged series between two validated input snapshots
- Compare authored fields without derived date/progress noise
- Render comparison evidence in JSON, Markdown and escaped local HTML

## 1.2.0 - 2026-09-07

- Support unknown release dates and add a local series editor with progress bars, source notes and stale-date review.
- Added regression coverage for the audited behavior and invalid inputs.

## 1.1.0 - 2026-07-27

- Added owned, completed, and remaining-volume progress calculations.
- Added deterministic release-date buckets and filters for format, publisher, author, and reader status.
- Added a priority-sorted resume queue with explicit next actions.

## 1.0.0 - 2026-07-26

- Added validated version 1 series inventories.
- Added status filtering and deterministic Markdown or JSON reports.
- Added replacement-safe output handling and local-only operation.
