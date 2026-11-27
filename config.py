from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "outputs"
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DATABASE_DIR = PROJECT_ROOT / "data" / "database"
DATABASE_PATH = Path(os.getenv("DENGUE_DB_PATH", DATABASE_DIR / "karnataka_dengue.sqlite3"))
DATABASE_URL = f"sqlite:///{DATABASE_PATH.as_posix()}"

# Existing project artifacts. These are the source-of-truth files.
DATASETS = {
    "daily": OUTPUT_DIR / "karnataka_dengue_rainfall_combined.csv",
    "monthly": OUTPUT_DIR / "karnataka_monthly_dengue_trend.csv",
    "predictions": OUTPUT_DIR / "forecasting_model_predictions.csv",
    "performance": OUTPUT_DIR / "forecasting_model_performance.csv",
    "rainfall_monthly": OUTPUT_DIR / "karnataka_monthly_rainfall.csv",
    "correlations": OUTPUT_DIR / "validated_district_correlations.csv",
    "primary_dengue": OUTPUT_DIR / "karnataka_primary_eda_dataset.csv",
    "forecasting_dataset": OUTPUT_DIR / "karnataka_monthly_forecasting_dataset.csv",
    "reporting_completeness": OUTPUT_DIR / "monthly_reporting_completeness.csv",
    "rainfall_daily": PROCESSED_DIR / "karnataka_district_daily_rainfall.csv",
    "dengue_raw": RAW_DIR / "ka-dengue-daily-summary.csv",
}
