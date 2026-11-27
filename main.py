from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .repository import initialize_database, read_dataset, database_status, sync_dataset

def _records(frame, limit=None):
    if limit is not None:
        frame = frame.head(limit)
    return frame.astype(object).where(frame.notna(), None).to_dict("records")

app = FastAPI(
    title="Karnataka Dengue & Rainfall API",
    description="API backed by the supplied Karnataka dengue, rainfall and forecasting project datasets.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False,
    allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    initialize_database()

@app.get("/")
def root():
    return {"name": "Karnataka Dengue & Rainfall API", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok", "database": "SQLite", "datasets": database_status()}

@app.post("/admin/sync")
def sync(force: bool = False):
    try:
        return {"results": initialize_database(force=force)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/datasets")
def datasets():
    return {"datasets": database_status()}

@app.get("/summary")
def summary():
    try:
        df = read_dataset("daily")
        if df.empty:
            return {"total_cases": 0, "total_suspected": 0, "total_deaths": 0, "districts": 0, "records": 0}
        def total(col):
            return float(df[col].fillna(0).sum()) if col in df else 0
        return {
            "total_cases": total("daily_cases"),
            "total_suspected": total("daily_suspected"),
            "total_deaths": total("daily_deaths"),
            "districts": int(df["district"].nunique()) if "district" in df else 0,
            "records": len(df),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/districts")
def districts():
    df = read_dataset("daily")
    if df.empty or "district" not in df:
        return {"districts": []}
    return {"districts": sorted(df["district"].dropna().astype(str).unique().tolist())}

@app.get("/daily")
def daily(district: str | None = None, limit: int = Query(5000, ge=1, le=50000)):
    df = read_dataset("daily")
    if district and "district" in df:
        df = df[df["district"].astype(str).str.casefold() == district.casefold()]
    return {"count": min(len(df), limit), "data": df.head(limit).where(df.notna(), None).to_dict("records")}

@app.get("/monthly")
def monthly():
    return {"data": _records(read_dataset("monthly"))}

@app.get("/rainfall/monthly")
def rainfall_monthly():
    return {"data": _records(read_dataset("rainfall_monthly"))}

@app.get("/forecast/performance")
def forecast_performance():
    return {"data": _records(read_dataset("performance"))}

@app.get("/forecast/predictions")
def forecast_predictions():
    return {"data": _records(read_dataset("predictions"))}

@app.get("/correlations")
def correlations():
    return {"data": _records(read_dataset("correlations"))}


@app.get("/data/{dataset_name}")
def dataset_data(dataset_name: str, limit: int = Query(250000, ge=1, le=250000)):
    """Return a named, allow-listed project dataset from SQLite."""
    allowed = {
        "daily", "monthly", "predictions", "performance", "rainfall_monthly",
        "correlations", "primary_dengue", "forecasting_dataset",
        "reporting_completeness", "rainfall_daily", "dengue_raw",
    }
    if dataset_name not in allowed:
        raise HTTPException(status_code=404, detail="Unknown dataset")
    try:
        frame = read_dataset(dataset_name)
        return {"dataset": dataset_name, "count": min(len(frame), limit),
                "data": _records(frame, limit)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/district-analysis")
def district_analysis():
    """District-level totals derived from the supplied integrated daily dataset."""
    frame = read_dataset("daily")
    if frame.empty or "district" not in frame:
        return {"data": []}
    numeric = [c for c in ["daily_cases", "daily_suspected", "daily_deaths", "average_rainfall_mm"] if c in frame]
    result = frame.groupby("district", dropna=True)[numeric].agg("sum").reset_index()
    if "average_rainfall_mm" in numeric:
        means = frame.groupby("district", dropna=True)["average_rainfall_mm"].mean().rename("mean_daily_rainfall_mm")
        result = result.drop(columns=["average_rainfall_mm"]).merge(means, on="district", how="left")
    records = _records(result)
    return {"data": records}

@app.get("/data-quality")
def data_quality():
    return {
        "reporting_completeness": _records(read_dataset("reporting_completeness")),
        "datasets": database_status(),
    }
