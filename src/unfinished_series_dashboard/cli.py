from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .core import STATUSES, build_report, load_dashboard, render_json, render_markdown


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Build a local unfinished-series dashboard.")
    result.add_argument("input", type=Path)
    result.add_argument("--status", action="append", choices=sorted(STATUSES))
    result.add_argument("--format", choices=("markdown", "json"), default="markdown")
    result.add_argument("--output", type=Path)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        report = build_report(load_dashboard(args.input), set(args.status or []))
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
