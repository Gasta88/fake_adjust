import random
from typing import Literal

import faker
import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI(
    title="Fake Adjust API",
    description="Synthetic Adjust-style attribution reporting feed (stage 1 of the FASS pipeline).",
    version="0.2.0",
)

fake = faker.Faker()

AD_NETWORKS = [
    "Google AdMob",
    "Facebook Audience Network",
    "Unity Ads",
    "InMobi",
    "AppLovin",
    "AdColony",
    "Vungle",
    "IronSource",
    "Chartboost",
    "Tapjoy",
    "AdMob Mediation",
    "AdThrive",
    "Fyber",
    "Mintegral",
    "AdTiming",
    "StartApp",
    "AdDuplex",
    "Liftoff",
    "Smaato",
    "AdYouLike",
]


class ReportingResponse(BaseModel):
    installs: int
    ad_spend: float
    clicks: int
    impressions: int
    # Field names are part of the wire contract consumed by
    # fake_adjust_serverless_service, including the "convertion" spelling.
    click_convertion_rate: float
    click_through_rate: float
    impressions_convertion_rate: float
    limit_ad_tracking_installs: int
    uninstalls: int
    campaign_name: str
    creative_name: str
    ad_network_name: str
    start_date: str
    end_date: str
    platform: str


def generate_report(
    start_date: str,
    end_date: str,
    platform: str,
) -> ReportingResponse:
    """Generate one report with a physically consistent attribution funnel.

    The sampled counts are monotonic (impressions >= clicks >= installs) and the
    conversion rates are derived from them, so they can never exceed 100%.
    """
    impressions = random.randint(10_000, 100_000)

    click_through_rate = random.uniform(0.01, 0.15)
    clicks = max(1, min(impressions, int(impressions * click_through_rate)))

    install_rate = random.uniform(0.02, 0.30)
    installs = max(1, min(clicks, int(clicks * install_rate)))

    uninstalls = random.randint(0, int(installs * 0.25))
    limit_ad_tracking_installs = random.randint(0, int(installs * 0.30))

    return ReportingResponse(
        installs=installs,
        ad_spend=round(random.uniform(0.01, 1000.00), 2),
        clicks=clicks,
        impressions=impressions,
        click_convertion_rate=(installs / clicks) * 100,
        click_through_rate=(clicks / impressions) * 100,
        impressions_convertion_rate=(installs / impressions) * 100,
        limit_ad_tracking_installs=limit_ad_tracking_installs,
        uninstalls=uninstalls,
        campaign_name=fake.bs(),
        creative_name=fake.catch_phrase(),
        ad_network_name=random.choice(AD_NETWORKS),
        start_date=start_date,
        end_date=end_date,
        platform=platform,
    )


@app.get("/reporting", response_model=list[ReportingResponse])
def get_reporting(
    start_date: str = Query(..., examples=["2025-05-01"]),
    end_date: str = Query(..., examples=["2025-05-01"]),
    platform: Literal["ios", "android"] = Query(...),
) -> list[ReportingResponse]:
    return [
        generate_report(start_date, end_date, platform)
        for _ in range(random.randint(1, 10))
    ]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
