# Development

Run `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build` before publishing.

Every release must update the package version, changelog, public GitHub release, and Logan Pendragon Forge catalog together.

## 1.2.0 improvement session

Support unknown release dates and add a local series editor with progress bars, source notes and stale-date review.

Unknown release dates may be null, blank or `unknown`. The local HTML editor supports title, completed/total/owned counts, publication status, publisher and source notes. It downloads a new version 1 JSON input; run the CLI again to validate the edited record. The selected report's records are exported, so a filtered report does not contain omitted series. Stale-date review compares author-supplied dates with the report's explicit as-of date; no dates are scraped or invented. Exact README commands and the shipped sample are exercised by regression tests.

Local formatting, lint, strict types and regression tests pass. Public release completion requires the protected CI/CodeQL matrix, tagged artifacts and matching Forge catalog/detail deployment.

## 1.3.0 acceptance

Compare saved series inventories by stable ID without looking up or inventing publication facts.

Use `series-dashboard current.json --compare previous.json --format html --output comparison.html`. Both files must be version 1 input inventories, not rendered reports. Comparison is deterministic by ID and covers full snapshots; dashboard filters cannot be combined with comparison. Missing fields differ from explicit null, list order is significant, and changing an ID appears as removal/addition. Notes in comparison evidence remain private local text; neither input is rewritten.
