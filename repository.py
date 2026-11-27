"""SQLite-backed access to the actual CSV artifacts shipped with this project."""
import re
import pandas as pd
from .config import DATASETS
from .database import connection

def _safe_table(name: str) -> str:
    return "ds_" + re.sub(r"[^a-zA-Z0-9_]", "_", name)

def sync_dataset(name: str, force: bool = False) -> dict:
    if name not in DATASETS:
        raise KeyError(f"Unknown dataset: {name}")
    path = DATASETS[name]
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")
    table = _safe_table(name)
    with connection() as conn:
        meta = conn.execute(
            "SELECT source_mtime FROM dataset_registry WHERE dataset_name = ?",
            (name,)
        ).fetchone()
        mtime = path.stat().st_mtime
        if not force and meta and float(meta["source_mtime"]) == mtime:
            return {"dataset": name, "status": "already_current", "rows": conn.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]}
        frame = pd.read_csv(path, low_memory=False)
        frame.to_sql(table, conn, if_exists="replace", index=False)
        conn.execute(
            """INSERT INTO dataset_registry(dataset_name, source_file, source_mtime, row_count)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(dataset_name) DO UPDATE SET
               source_file=excluded.source_file, source_mtime=excluded.source_mtime,
               row_count=excluded.row_count""",
            (name, str(path.relative_to(path.parents[1])), mtime, len(frame))
        )
        conn.commit()
    return {"dataset": name, "status": "synced", "rows": len(frame)}

def initialize_database(force: bool = False) -> list[dict]:
    with connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS dataset_registry (
            dataset_name TEXT PRIMARY KEY, source_file TEXT NOT NULL,
            source_mtime REAL NOT NULL, row_count INTEGER NOT NULL,
            synced_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.commit()
    results = []
    for name, path in DATASETS.items():
        if path.exists():
            results.append(sync_dataset(name, force=force))
    return results

def read_dataset(name: str) -> pd.DataFrame:
    if name not in DATASETS:
        raise KeyError(f"Unknown dataset: {name}")
    if not DATASETS[name].exists():
        return pd.DataFrame()
    sync_dataset(name)
    table = _safe_table(name)
    with connection() as conn:
        return pd.read_sql_query(f'SELECT * FROM "{table}"', conn)

def database_status() -> list[dict]:
    with connection() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS dataset_registry (
            dataset_name TEXT PRIMARY KEY, source_file TEXT NOT NULL,
            source_mtime REAL NOT NULL, row_count INTEGER NOT NULL,
            synced_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )""")
        rows = conn.execute("SELECT dataset_name, source_file, row_count, synced_at FROM dataset_registry ORDER BY dataset_name").fetchall()
        return [dict(row) for row in rows]
