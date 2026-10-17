# Unfinished Series Dashboard

> ⭐ **Gold Star Project — finished for its intended scope.**
> Scope reviewed for **v1.3.1** on **2026-10-17**. Actively maintained; meaningful future development can reopen the scope.
> [What Gold Star means](https://www.loganpendragonforge.com/open-source/gold-star/)
>
> Manually authored series inventories, progress reports, local editing and saved-snapshot comparison.

## Current release 1.3.1

Report boolean-to-number changes accurately in JSON comparison evidence.

JSON true differs from 1 and false differs from 0, including inside nested metadata. Numeric 1 and 1.0 compare equally; object key order does not matter, while array order does. Existing field-presence and privacy rules still apply.

## Current release 1.3.0

Compare saved series inventories by stable ID without looking up or inventing publication facts.

Use `series-dashboard current.json --compare previous.json --format html --output comparison.html`. Both files must be version 1 input inventories, not rendered reports. Comparison is deterministic by ID and covers full snapshots; dashboard filters cannot be combined with comparison. Missing fields differ from explicit null, list order is significant, and changing an ID appears as removal/addition. Notes in comparison evidence remain private local text; neither input is rewritten.

[![CI](https://github.com/loganpendragonmultiverse/unfinished-series-dashboard/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/unfinished-series-dashboard/actions/workflows/ci.yml)

Unfinished Series Dashboard turns a portable JSON reading list into a clear local report of incomplete, abandoned, delayed, still-writing, and completed series. It records both the publication state and the reader's own position without relying on a proprietary catalog.

## Three-minute start

Requires Python 3.10 or newer.

```bash
python -m pip install .
series-dashboard examples/series.json
series-dashboard examples/series.json --status delayed --format json
series-dashboard examples/series.json --as-of 2026-07-27 --date-bucket overdue
```

The input uses a version 1 object with a `series` array. Each entry requires a unique `id`, `title`, and supported `status`; `reader_status`, `next_release`, and notes remain user-controlled. Markdown and JSON output are deterministic, and output files are never replaced.

Version 1.1 accepts optional `owned_volumes`, `completed_volumes`, `total_volumes`, `priority`, `next_action`, `format`, `publisher`, and `author` fields. Filters can be repeated. Supplying `--as-of YYYY-MM-DD` makes upcoming, overdue, unknown, and stale date buckets fully reproducible.

## Boundaries

The tool does not scrape publication sites, guess whether a series has ended, or contact external services. All status judgments come from the supplied file. Everything runs locally with no telemetry or account requirement.

## Development

Run `python -m pip install -e ".[dev]"`, `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## Version 1.2.0: reviewed improvements

Support unknown release dates and add a local series editor with progress bars, source notes and stale-date review.

```bash
series-dashboard examples/series.json --format html --output editor.html
```

Unknown release dates may be null, blank or `unknown`. The local HTML editor supports title, completed/total/owned counts, publication status, publisher and source notes. It downloads a new version 1 JSON input; run the CLI again to validate the edited record. The selected report's records are exported, so a filtered report does not contain omitted series. Stale-date review compares author-supplied dates with the report's explicit as-of date; no dates are scraped or invented. Exact README commands and the shipped sample are exercised by regression tests.
