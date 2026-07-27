# Unfinished Series Dashboard

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
