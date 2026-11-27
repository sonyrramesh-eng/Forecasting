# Backend – Karnataka Dengue & Rainfall

This backend is connected to the existing Streamlit project and uses the actual CSV files already present in `data/` and `outputs/`. It does not download substitute data or fabricate records.

## Architecture
- **FastAPI** exposes REST endpoints for integrations and future frontends.
- **SQLite** persists synchronized copies of the existing project datasets in `data/database/karnataka_dengue.sqlite3`.
- **Repository layer** checks source-file modification times and refreshes the matching SQLite table when a CSV changes.
- **Streamlit integration**: `dashboard/app.py` loads its six primary dashboard datasets through `backend.repository.read_dataset()`.

The CSV artifacts remain the source of truth. SQLite is the queryable backend store/cache.

## Run

From the project root:

```bash
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

Open:
- API: http://127.0.0.1:8000/
- Interactive API docs: http://127.0.0.1:8000/docs
- Health/database status: http://127.0.0.1:8000/health

In a second terminal, start the connected dashboard:

```bash
python -m streamlit run dashboard/app.py
```

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/health` | API and SQLite/dataset status |
| GET | `/datasets` | Registered datasets |
| POST | `/admin/sync?force=true` | Re-import source CSV files |
| GET | `/summary` | Overall dengue totals |
| GET | `/districts` | District names |
| GET | `/daily?district=BENGALURU%20URBAN` | Daily combined data |
| GET | `/monthly` | Monthly dengue trend |
| GET | `/rainfall/monthly` | Monthly rainfall |
| GET | `/forecast/performance` | Saved model metrics |
| GET | `/forecast/predictions` | Saved actual/predicted values |
| GET | `/correlations` | Validated district correlations |
| GET | `/data-quality` | Reporting completeness and dataset registry |

## Data actually ingested

The backend synchronizes the following existing files when present:
- `outputs/karnataka_dengue_rainfall_combined.csv`
- `outputs/karnataka_monthly_dengue_trend.csv`
- `outputs/forecasting_model_predictions.csv`
- `outputs/forecasting_model_performance.csv`
- `outputs/karnataka_monthly_rainfall.csv`
- `outputs/validated_district_correlations.csv`
- `outputs/karnataka_primary_eda_dataset.csv`
- `outputs/karnataka_monthly_forecasting_dataset.csv`
- `outputs/monthly_reporting_completeness.csv`
- `data/processed/karnataka_district_daily_rainfall.csv`
- `data/raw/ka-dengue-daily-summary.csv`

If an output artifact is absent, it is not silently replaced with mock data. Run the existing preparation notebooks/scripts that create that artifact first.

## Important
The forecasting endpoints expose the project's saved experimental results. They do not claim a newly trained or clinically validated outbreak model. The reported test period is small, and the original project limitations still apply.
