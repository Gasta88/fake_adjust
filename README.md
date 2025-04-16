# Attribution Data API
====================================


## Description
---------------

This is an experiment to set up a fake attribution data API for a non-specific mobile application.
The `main.py` file contains the main API code using FastAPI. It defines an endpoint for fetching reporting data. Below are the details of the available query parameters and the structure of the data returned by the API.

#### Endpoint
- **GET** `/reporting`

#### Query Parameters
- `start_date` (str): The start date for the reporting period in `YYYY-MM-DD` format. Example: `2025-05-01`
- `end_date` (str): The end date for the reporting period in `YYYY-MM-DD` format. Example: `2025-05-01`
- `platform` (str): The platform for which the data is requested. Must be either `ios` or `android`.

#### Response Data
The API returns a JSON array of objects with the following fields:

- `installs` (int): Number of installs.
- `ad_spend` (float): Amount spent on ads.
- `clicks` (int): Number of ad clicks.
- `impressions` (int): Number of ad impressions.
- `click_convertion_rate` (float): Install to click conversion rate in percentage.
- `click_through_rate` (float): Click to impression conversion rate in percentage.
- `impressions_convertion_rate` (float): Install to impression conversion rate in percentage.
- `limit_ad_tracking_installs` (int): Number of installs with limited ad tracking.
- `uninstalls` (int): Number of uninstalls.
- `campaign_name` (str): Name of the campaign.
- `creative_name` (str): Name of the creative.
- `ad_network_name` (str): Name of the ad network.
- `start_date` (str): Start date of the data period.
- `end_date` (str): End date of the data period.
- `platform` (str): Platform for which the data is reported (`ios` or `android`).

This information helps users understand what query parameters they can use when making requests to the API and what kind of data they can expect in response.



## Content
------------

This repository contains the following:

* `main.py`: The main API code using FastAPI
* `Dockerfile`: The Dockerfile for building the API image
* `Makefile`: The Makefile for building and running the API
* `run_curl.py`: A Python script for testing and interacting with the API
* `requirements.txt`: The dependencies required by the API
* `raw_data/`: A directory containing sample data files


## How-To
--------

### Setting up the API

1. Build the Docker image using `make build`
2. Run the Docker container using `make run`
3. The API will be available at `http://127.0.0.1:8000`

Alternatively run `make all`

### Running API calls with the Python script

1. Navigate to the root directory of the repository using `cd`
2. Run the Python script using `python run_curl.py`
3. Inspect the content of `raw_data/` folder

### Tearing down the API

1. Stop and remove the Docker container adn image using `make clean`
2. Remove any temporary files or data created during testing