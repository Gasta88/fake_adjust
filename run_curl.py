"""Fetch reporting data from a running Fake Adjust API and write it to disk."""

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path

import requests

DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_START_DATE = dt.date(2025, 4, 1)
DEFAULT_END_DATE = dt.date(2025, 4, 14)
PLATFORMS = ("ios", "android")


def build_url(base_url: str, report_date: dt.date, platform: str) -> str:
    """Build the /reporting URL for one day and one platform."""
    base = base_url.rstrip("/")
    day = report_date.isoformat()
    return (
        f"{base}/reporting?start_date={day}&end_date={day}&platform={platform}"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Fake Adjust reports into a local directory.",
    )
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help=f"API root (default: {DEFAULT_BASE_URL})",
    )
    parser.add_argument(
        "--start-date",
        type=dt.date.fromisoformat,
        default=DEFAULT_START_DATE,
        help=f"First reporting day, YYYY-MM-DD (default: {DEFAULT_START_DATE})",
    )
    parser.add_argument(
        "--end-date",
        type=dt.date.fromisoformat,
        default=DEFAULT_END_DATE,
        help=f"Last reporting day, YYYY-MM-DD (default: {DEFAULT_END_DATE})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("raw_data"),
        help="Directory that receives one JSON file per day and platform.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds (default: 30)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    if args.end_date < args.start_date:
        raise SystemExit("--end-date must be on or after --start-date")

    if args.output_dir.exists():
        shutil.rmtree(args.output_dir)
    args.output_dir.mkdir(parents=True)

    days = (args.end_date - args.start_date).days + 1
    for offset in range(days):
        report_date = args.start_date + dt.timedelta(days=offset)
        for platform in PLATFORMS:
            url = build_url(args.base_url, report_date, platform)
            response = requests.get(url, timeout=args.timeout)
            response.raise_for_status()

            target = args.output_dir / f"{report_date.isoformat()}_{platform}.json"
            target.write_text(json.dumps(response.json(), indent=2))
            print(f"wrote {target}")


if __name__ == "__main__":
    main()
