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

## 1.3.1 acceptance

Report boolean-to-number changes accurately in JSON comparison evidence.

JSON true differs from 1 and false differs from 0, including inside nested metadata. Numeric 1 and 1.0 compare equally; object key order does not matter, while array order does. Existing field-presence and privacy rules still apply.

## Gold Star review — October 17, 2026

Keep track of unfinished book series, update your reading progress and compare saved copies of your list.

Logan considers this project complete. Continue fixes and maintenance, and consider good new ideas. The catalog records the reviewed release.

Definition: https://www.loganpendragonforge.com/open-source/?gold=1

## 1.3.2 canonical dates

Require exact YYYY-MM-DD calendar dates for next_release and as_of across Python 3.10 and newer; retain null/blank/unknown release dates. Reject compact/week/non-text/invalid dates before creating output. Verify the browser download guard and canonical stale-date filtering, with original bytes unchanged.

## 1.4.0 output and snapshot fidelity

Create JSON, Markdown and HTML reports exclusively and preserve a destination created immediately before opening. Keep authored unknown, null, blank and missing release dates distinct in snapshot comparisons while treating each as an unknown date for dashboard filtering. Preserve source bytes and unchanged browser-export values.

The browser editor supports adding and removing records, including an empty inventory. Reject duplicate/blank IDs and titles, invalid statuses, fractional/negative/unsafe counts and invalid dates before download. Preserve untouched authored values and extra fields. Test add/edit/remove/download and CLI revalidation in Chromium, Firefox and WebKit, including filtered reports; original input bytes must stay unchanged.

Confirm removals before changing records. Warn on navigation/reload with unsaved record edits or an unfinished new-series form. A download does not prove persistence: only the user's saved-download acknowledgment clears the record-edit warning, and further edits require another export. Exercise accept/cancel, export, acknowledgment, rearming and reload in all three browser engines; do not use persistent browser storage.

## 1.4.1 unknown volume totals

Preserve `total_volumes: null` as an unknown total when downloading an unchanged generated editor. This exception applies only to the total, not owned/completed counts or priority. Keep fractional, negative, boolean, non-finite and unsafe browser numbers blocked. Exercise generated HTML, untouched download and CLI reimport in Chromium, Firefox and WebKit; preserve original input bytes.
