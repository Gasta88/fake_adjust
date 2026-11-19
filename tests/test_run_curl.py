import datetime as dt

import pytest

from run_curl import build_url, parse_args


def test_build_url_uses_reporting_endpoint():
    url = build_url("http://127.0.0.1:8000", dt.date(2025, 4, 1), "ios")

    assert url == (
        "http://127.0.0.1:8000/reporting"
        "?start_date=2025-04-01&end_date=2025-04-01&platform=ios"
    )


def test_build_url_strips_trailing_slash():
    url = build_url("https://example.test/api/", dt.date(2025, 4, 2), "android")

    assert url.startswith("https://example.test/api/reporting?")
    assert "platform=android" in url


def test_parse_args_defaults_to_localhost():
    args = parse_args([])

    assert args.base_url == "http://127.0.0.1:8000"
    assert args.start_date == dt.date(2025, 4, 1)
    assert args.end_date == dt.date(2025, 4, 14)


def test_parse_args_accepts_overrides():
    args = parse_args(
        [
            "--base-url",
            "https://example.test",
            "--start-date",
            "2025-06-01",
            "--end-date",
            "2025-06-03",
            "--output-dir",
            "out",
        ]
    )

    assert args.base_url == "https://example.test"
    assert args.start_date == dt.date(2025, 6, 1)
    assert args.end_date == dt.date(2025, 6, 3)
    assert str(args.output_dir) == "out"


def test_parse_args_rejects_malformed_date():
    with pytest.raises(SystemExit):
        parse_args(["--start-date", "01-06-2025"])
