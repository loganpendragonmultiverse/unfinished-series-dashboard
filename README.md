# Unfinished Series Dashboard

> ⭐ **Gold Star Project**
> I consider this project complete. Fixes, maintenance and good new ideas are still welcome.
> [About Gold Stars](https://www.loganpendragonforge.com/open-source/?gold=1)
>
> Keep track of unfinished book series, update your reading progress and compare saved copies of your list.

## What you can do

- Track series and reading progress in a local list.
- Edit progress in the browser and save a new copy.
- Compare saved lists to see added, removed and changed records.


## Current release 1.4.0

The local browser editor can add series with a unique stable ID and title, update their details, and remove records before downloading a new version 1 input. It checks required fields, supported status, non-negative safe integer counts and real calendar dates before saving. Edits do not rewrite your input file. Filtered reports still contain and export only their selected records; use an unfiltered report to maintain the full inventory.

Reports use exclusive file creation. If another process creates the destination just before export, the command returns an error and preserves that file and the input.

Snapshot comparisons preserve authored unknown-date values: `unknown`, null, blank and missing remain distinct, while all four still use the unknown date bucket. Browser downloads retain unchanged authored values.

## Earlier release 1.3.2

Release dates and `--as-of` require exact calendar dates in `YYYY-MM-DD` form on every supported Python version. Compact dates, ISO week dates, invalid days and non-text dates are rejected before output. Unknown release dates may still be null, blank or `unknown`. The browser editor validates dates before downloading; canonical dates keep stale-date filtering consistent with the CLI.

## JSON comparisons in 1.3.1

Comparisons now tell the difference between booleans and numbers, even inside nested values.

JSON true differs from 1 and false differs from 0, including inside nested metadata. Numeric 1 and 1.0 compare equally; object key order does not matter, while array order does. Existing field-presence and privacy rules still apply.

## Snapshot comparisons in 1.3.0

Compare saved copies of your series list to see what changed.

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

## Updates in 1.2.0

Support unknown release dates and add a local series editor with progress bars, source notes and stale-date review.

```bash
series-dashboard examples/series.json --format html --output editor.html
```

Unknown release dates may be null, blank or `unknown`. The local HTML editor supports title, completed/total/owned counts, publication status, publisher and source notes. It downloads a new version 1 JSON input; run the CLI again to validate the edited record. The selected report's records are exported, so a filtered report does not contain omitted series. Stale-date review compares author-supplied dates with the report's explicit as-of date; no dates are scraped or invented. Exact README commands and the shipped sample are exercised by regression tests.
