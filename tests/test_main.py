import random

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def fetch_rows(start_date="2025-04-01", end_date="2025-04-01", platform="ios"):
    response = client.get(
        "/reporting",
        params={
            "start_date": start_date,
            "end_date": end_date,
            "platform": platform,
        },
    )
    assert response.status_code == 200
    return response.json()


@pytest.mark.parametrize("seed", range(10))
def test_funnel_is_physically_consistent(seed):
    random.seed(seed)
    rows = fetch_rows()

    assert 1 <= len(rows) <= 10
    for row in rows:
        assert 0 < row["installs"] <= row["clicks"] <= row["impressions"]
        assert 0 <= row["uninstalls"] <= row["installs"]
        assert 0 <= row["limit_ad_tracking_installs"] <= row["installs"]

        assert 0 <= row["click_convertion_rate"] <= 100
        assert 0 <= row["click_through_rate"] <= 100
        assert 0 <= row["impressions_convertion_rate"] <= 100

        assert row["click_convertion_rate"] == pytest.approx(
            row["installs"] / row["clicks"] * 100
        )
        assert row["click_through_rate"] == pytest.approx(
            row["clicks"] / row["impressions"] * 100
        )
        assert row["impressions_convertion_rate"] == pytest.approx(
            row["installs"] / row["impressions"] * 100
        )


def test_request_parameters_are_echoed():
    rows = fetch_rows(
        start_date="2025-04-01", end_date="2025-04-02", platform="android"
    )

    assert rows
    for row in rows:
        assert row["start_date"] == "2025-04-01"
        assert row["end_date"] == "2025-04-02"
        assert row["platform"] == "android"


def test_platform_accepts_only_ios_and_android():
    for platform in ("ios", "android"):
        assert fetch_rows(platform=platform)

    response = client.get(
        "/reporting",
        params={
            "start_date": "2025-04-01",
            "end_date": "2025-04-01",
            "platform": "windows",
        },
    )
    assert response.status_code == 422
