from fastapi import FastAPI, Query
from pydantic import BaseModel
import uvicorn
import random
import faker

app = FastAPI()
fake = faker.Faker()

class ReportingResponse(BaseModel):
    installs: int
    ad_spend: float
    clicks: int
    impressions: int
    limit_ad_tracking_installs: int
    uninstalls: int
    campaign_name: str
    creative_name: str
    ad_network_name: str
    start_date: str
    end_date: str

@app.get("/reporting", response_model=ReportingResponse)
def get_reporting(
    start_date: str = Query(..., example="2025-05-01"),
    end_date: str = Query(..., example="2025-05-01"),
    platform: str = Query(..., example="ios", regex="^(ios|android)$")
):
    # Generate fake data based on the query parameters
    installs = random.randint(1000, 10000)
    ad_spend = random.uniform(0.01, 1000.00)
    clicks = random.randint(100, 1000)
    impressions = random.randint(100, 1000)
    limit_ad_tracking_installs = random.randint(10, 100)
    uninstalls = random.randint(1000, 10000)
    campaign_name = fake.bs()
    creative_name = fake.catch_phrase()
    ad_network_name = f"{fake.company()} {fake.random_element(elements=('media', 'networks', 'advertising', 'solutions'))}"
    start_date = start_date
    end_date = end_date

    return ReportingResponse(
        installs=installs,
        ad_spend=ad_spend,
        clicks=clicks,
        impressions=impressions,
        limit_ad_tracking_installs=limit_ad_tracking_installs,
        uninstalls=uninstalls,
        campaign_name=campaign_name,
        creative_name=creative_name,
        ad_network_name=ad_network_name,
        start_date=start_date,
        end_date=end_date
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)