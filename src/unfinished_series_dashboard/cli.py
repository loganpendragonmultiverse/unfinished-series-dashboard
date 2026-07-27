from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import DATE_BUCKETS, STATUSES, build_report, load_dashboard, render_json, render_markdown


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Build a local unfinished-series dashboard.")
    result.add_argument("input", type=Path)
    result.add_argument("--status", action="append", choices=sorted(STATUSES))
    result.add_argument("--as-of")
    result.add_argument("--date-bucket", action="append", choices=sorted(DATE_BUCKETS))
    result.add_argument("--format-type", action="append")
    result.add_argument("--publisher", action="append")
    result.add_argument("--author", action="append")
    result.add_argument("--reader-status", action="append")
    result.add_argument("--format", choices=("markdown", "json"), default="markdown")
    result.add_argument("--output", type=Path)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        report = build_report(
            load_dashboard(args.input),
            set(args.status or []),
            as_of=args.as_of,
            date_buckets=set(args.date_bucket or []),
            formats=set(args.format_type or []),
            publishers=set(args.publisher or []),
            authors=set(args.author or []),
            reader_statuses=set(args.reader_status or []),
        )
        output = render_json(report) if args.format == "json" else render_markdown(report)
        if args.output:
            if args.output.exists():
                raise ValueError(f"output already exists: {args.output}")
            args.output.write_text(output, encoding="utf-8")
        else:
            sys.stdout.write(output)
    except (OSError, TypeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
