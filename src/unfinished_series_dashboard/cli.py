from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .comparison import compare_snapshots, comparison_html, comparison_markdown
from .core import DATE_BUCKETS, STATUSES, build_report, load_dashboard, render_json, render_markdown
from .preview import render_html


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
    result.add_argument("--format", choices=("markdown", "json", "html"), default="markdown")
    result.add_argument("--output", type=Path)
    result.add_argument(
        "--compare",
        type=Path,
        help="Previous version 1 input snapshot; compare authored fields by ID",
    )
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        current = load_dashboard(args.input)
        if args.compare and any(
            (
                args.status,
                args.date_bucket,
                args.format_type,
                args.publisher,
                args.author,
                args.reader_status,
            )
        ):
            raise ValueError(
                "snapshot comparison requires full input files without dashboard filters"
            )
        report = build_report(
            current,
            set(args.status or []),
            as_of=args.as_of,
            date_buckets=set(args.date_bucket or []),
            formats=set(args.format_type or []),
            publishers=set(args.publisher or []),
            authors=set(args.author or []),
            reader_statuses=set(args.reader_status or []),
        )
        if args.compare:
            previous = load_dashboard(args.compare)
            report["comparison"] = compare_snapshots(previous["series"], current["series"])
        output = {"json": render_json, "markdown": render_markdown, "html": render_html}[
            args.format
        ](report)
        if args.compare and args.format == "markdown":
            output += comparison_markdown(report["comparison"])
        elif args.compare and args.format == "html":
            output = output.replace("</html>", comparison_html(report["comparison"]) + "</html>")
        if args.output:
            with args.output.open("x", encoding="utf-8") as stream:
                stream.write(output)
        else:
            sys.stdout.write(output)
    except (OSError, TypeError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0
