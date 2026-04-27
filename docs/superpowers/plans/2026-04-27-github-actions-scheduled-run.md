# GitHub Actions Scheduled Run Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a GitHub Actions workflow that runs the weather pipeline daily at 8 AM UTC and commits the updated CSV back to the repo.

**Architecture:** A single workflow file handles scheduling, Python setup, pipeline execution, and committing the CSV output. The API key is stored as a GitHub Actions repository secret and injected at runtime.

**Tech Stack:** GitHub Actions, Python 3.11, ubuntu-latest runner

---

### Task 1: Write the workflow file

**Files:**
- Create: `.github/workflows/weather_pipeline.yml`

- [ ] **Step 1: Create the workflows directory**

```bash
mkdir -p .github/workflows
```

- [ ] **Step 2: Write the workflow file**

Create `.github/workflows/weather_pipeline.yml` with this exact content:

```yaml
name: Weather Pipeline

on:
  schedule:
    - cron: "0 8 * * *"  # Daily at 8:00 AM UTC
  workflow_dispatch:       # Allow manual runs from GitHub UI

jobs:
  run-pipeline:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run weather pipeline
        env:
          WEATHER_API_KEY: ${{ secrets.WEATHER_API_KEY }}
        run: python weather.py

      - name: Commit updated CSV
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add weather_data.csv
          git diff --cached --quiet || git commit -m "chore: update weather data $(date -u '+%Y-%m-%d')"
          git push
```

- [ ] **Step 3: Commit the workflow file**

```bash
git add .github/workflows/weather_pipeline.yml
git commit -m "feat: add scheduled GitHub Actions workflow"
```

- [ ] **Step 4: Push to GitHub**

```bash
git push
```

---

### Task 2: Add the API key as a GitHub Actions secret

**This is a manual step performed in the GitHub web UI.**

- [ ] **Step 1: Navigate to your repo on GitHub**

Go to: `Settings` → `Secrets and variables` → `Actions`

- [ ] **Step 2: Add the secret**

Click **New repository secret** and fill in:
- **Name:** `WEATHER_API_KEY`
- **Value:** your WeatherAPI key (from weatherapi.com)

Click **Add secret**.

---

### Task 3: Verify the workflow runs correctly

- [ ] **Step 1: Trigger a manual run**

On GitHub, go to `Actions` → `Weather Pipeline` → `Run workflow` → `Run workflow`.

- [ ] **Step 2: Confirm the run succeeds**

Wait for the run to complete. All steps should show a green checkmark. Expected duration: ~30–60 seconds for setup + ~30 seconds for the pipeline (20 cities × 1s sleep).

- [ ] **Step 3: Confirm the CSV was committed**

Check the repo's commit history — you should see a new commit:
```
chore: update weather data YYYY-MM-DD
```
authored by `github-actions[bot]`.

- [ ] **Step 4: Confirm scheduled runs**

After the first scheduled run at 8:00 AM UTC, verify it appears in the `Actions` tab with a `schedule` trigger label.
