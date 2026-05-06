# GitHub Actions Scheduled Run — Design Spec

**Date:** 2026-04-27
**Project:** weather-api-pipeline

## Overview

Add a single GitHub Actions workflow that runs the weather pipeline daily and commits the updated CSV back to the repo.

## Trigger

- **Scheduled:** Daily at 8:00 AM UTC (`cron: "0 8 * * *"`)
- **Manual:** `workflow_dispatch` enabled so the workflow can be triggered on demand from the GitHub Actions tab

### Why daily?

The pipeline's purpose is to build a historical weather dataset for trend analysis. A daily cadence is the right fit for three reasons:

1. **Matches the data's natural grain.** Weather patterns are meaningfully compared day-over-day (highs, lows, conditions). Sub-daily snapshots would add noise without adding analytical value for this use case.
2. **Stays within free-tier API limits.** WeatherAPI's free tier allows 1 million calls/month. At 20 cities per run, daily scheduling uses ~600 calls/month — well under the limit. Hourly runs would consume ~14,400 calls/month and risk hitting the cap.
3. **Keeps the CSV manageable.** One row per city per day means the CSV grows at a predictable, readable rate (~20 rows/day) suitable for a class project.

## Environment

- **Runner:** `ubuntu-latest`
- **Python version:** 3.11
- **API key:** Stored as a GitHub Actions repository secret named `WEATHER_API_KEY`, injected as an environment variable at runtime. Never hardcoded.

## Steps

1. Checkout the repo (`actions/checkout@v4`)
2. Set up Python 3.11 (`actions/setup-python@v5`)
3. Install dependencies from `requirements.txt`
4. Run `weather.py` with `WEATHER_API_KEY` injected via `env`
5. Commit updated `weather_data.csv` back to main — skipped if no file changes

## Failure Notifications

GitHub Actions sends an email to the repo owner by default when a workflow fails. No additional configuration needed.

## File Location

`.github/workflows/weather_pipeline.yml`
