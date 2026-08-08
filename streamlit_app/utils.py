import streamlit as st
import pandas as pd
import duckdb
import os

# Update this path to where your local Iceberg gold table data/parquet lives
GOLD_TABLE_PATH = "warehouse/gold/churn_features/data/*.parquet"


@st.cache_data(ttl=600)
def load_gold_churn_data() -> pd.DataFrame:
    """Fast query over Gold Iceberg Parquet files using DuckDB."""
    if not os.path.exists(os.path.dirname(GOLD_TABLE_PATH.split('*')[0])):
        # Fallback dummy generator if running without data present
        return pd.DataFrame({
            "customer_id": range(1000, 1010),
            "recency_days": [5, 12, 45, 2, 80, 15, 30, 90, 4, 11],
            "frequency": [12, 4, 1, 20, 2, 8, 3, 1, 15, 6],
            "monetary": [1500.0, 300.0, 50.0, 2200.0, 120.0, 850.0, 400.0, 60.0, 1800.0, 500.0],
            "churn_probability": [0.05, 0.22, 0.85, 0.01, 0.92, 0.15, 0.45, 0.88, 0.02, 0.18],
            "churn_prediction": [0, 0, 1, 0, 1, 0, 0, 1, 0, 0]
        })

    # Fast read via DuckDB
    query = f"SELECT * FROM read_parquet('{GOLD_TABLE_PATH}')"
    return duckdb.query(query).to_df()