# Fake Adjust — Attribution Data API

[![CI](https://github.com/Gasta88/fake_adjust/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Gasta88/fake_adjust/actions/workflows/ci.yml)

A small FastAPI service that serves **synthetic Adjust-style attribution reports** over
HTTP. It is **stage 1 of a three-stage data pipeline**: downstream stages need a
realistic, predictable feed to schedule against, load into a warehouse and model — this
is that feed. It is not connected to any real ad network, does not collect real data and
stores nothing.

## Pipeline context

1. **fake_adjust** (this repository) — serves synthetic reports at `/reporting`; deployed
   separately from the downstream stages.
2. **[fake_adjust_serverless_service](https://github.com/Gasta88/fake_adjust_serverless_service)**
   — schedules calls to this API, downloads the reports and loads them into BigQuery.
3. **Dataform** — builds the materialised views on top of the BigQuery tables (outside
   this repository).

The stage-2 consumer maps the response fields into its BigQuery schema. The field names
below — including the `convertion` spelling — are therefore a **frozen wire contract**;
renaming them would break the downstream load.

## Quickstart

### Docker (recommended)

```bash
make all     # docker build + run on http://127.0.0.1:8000
curl "http://127.0.0.1:8000/reporting?start_date=2025-05-01&end_date=2025-05-01&platform=ios"
make clean   # remove the container and image
```

### Local Python 3.11+

```bash
python3 -m venv .venv
source .venv/bin/activate
make install-dev
uvicorn main:app --reload
```

## API

### `GET /reporting`

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `start_date` | string | yes | First day of the report, `YYYY-MM-DD`. |
| `end_date` | string | yes | Last day of the report, `YYYY-MM-DD`. |
| `platform` | string | yes | `ios` or `android`. Any other value returns `422`. |

A request returns between 1 and 10 report rows, one per generated campaign/creative.

```bash
curl "http://127.0.0.1:8000/reporting?start_date=2025-05-01&end_date=2025-05-01&platform=ios"
```

```json
[
  {
    "installs": 1731,
    "ad_spend": 442.71,
    "clicks": 9880,
    "impressions": 74301,
    "click_convertion_rate": 17.52,
    "click_through_rate": 13.30,
    "impressions_convertion_rate": 2.33,
    "limit_ad_tracking_installs": 214,
    "uninstalls": 132,
    "campaign_name": "synergize sticky platforms",
    "creative_name": "Stand-alone zero tolerance framework",
    "ad_network_name": "AppLovin",
    "start_date": "2025-05-01",
    "end_date": "2025-05-01",
    "platform": "ios"
  }
]
```

### Data model

Every row describes one campaign/creative on one platform and is generated as a
physically consistent funnel:

- `impressions >= clicks >= installs`, and `uninstalls <= installs`.
- `limit_ad_tracking_installs <= installs`.
- `click_convertion_rate` = installs / clicks (%), `click_through_rate` = clicks /
  impressions (%), `impressions_convertion_rate` = installs / impressions (%); all
  three are in the range 0–100.

`start_date`, `end_date` and `platform` echo the request. `campaign_name`,
`creative_name` and `ad_network_name` are Faker-generated labels and do not refer to
real campaigns or advertisers.

## Repository contents

| Path | Purpose |
| --- | --- |
| `main.py` | FastAPI app and `/reporting` endpoint. |
| `run_curl.py` | Client that downloads reports for a date range into `raw_data/`. |
| `tests/` | Funnel invariants, parameter validation and client URL tests. |
| `Dockerfile`, `.dockerignore` | Runtime image. |
| `Makefile` | `install-dev`, `build`, `run`, `test`, `lint`, `clean`. |
| `requirements.txt`, `requirements-dev.txt` | Pinned runtime and development dependencies. |
| `pyproject.toml` | Ruff and pytest configuration. |
| `LICENSE` | MIT. |

`raw_data/` is **generated output**, not sample data: `run_curl.py` writes one JSON file
per day and platform there, and it is gitignored. No data files are shipped with the
repository.

## Running the downloader

With the API running locally:

```bash
python run_curl.py \
  --base-url http://127.0.0.1:8000 \
  --start-date 2025-05-01 \
  --end-date 2025-05-07 \
  --output-dir raw_data
```

Point `--base-url` at any deployment of this API. The script fails on a non-2xx
response rather than writing partial data.

## Development

```bash
make lint    # ruff
make test    # pytest
```

CI runs ruff, pytest on Python 3.11 and 3.12, and builds the Docker image on every pull
request and on every push to `main`.

## Limitations

- Synthetic random data with no persistence, authentication or pagination.
- A single endpoint; no write path, no deduplication and no notion of report latency.
- Faker-generated names are placeholders, not a real ad-network taxonomy.

## License

[MIT](LICENSE) © 2026 Francesco Gastaldello
