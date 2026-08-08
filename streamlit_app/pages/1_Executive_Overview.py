import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_gold_churn_data

# Page configuration
st.set_page_config(
    page_title="Executive Overview",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Churn & Revenue Risk")

# 1. Safe Data Ingestion
try:
    df = load_gold_churn_data()
except Exception as e:
    st.error(f"Failed to load Gold churn data: {e}")
    st.stop()

# 2. Guardrail: Validate DataFrame state
if df is None or df.empty:
    st.warning("No customer data found in the Gold Iceberg layer.")
    st.stop()

# 3. Guardrail: Ensure all expected columns exist
required_cols = {
    "customer_id": 0,
    "recency_days": 0,
    "frequency": 1,
    "monetary": 0.0,
    "churn_probability": 0.0,
    "churn_prediction": 0
}

for col, default_val in required_cols.items():
    if col not in df.columns:
        df[col] = default_val

# 4. Data Cleaning & Type Formatting
df["churn_prediction"] = df["churn_prediction"].fillna(0).astype(int)
df["churn_probability"] = df["churn_probability"].fillna(0.0).astype(float)
df["monetary"] = df["monetary"].fillna(0.0).astype(float)
df["recency_days"] = df["recency_days"].fillna(0).astype(int)
df["frequency"] = df["frequency"].fillna(1).clip(lower=1)  # Ensure size > 0 for Plotly

# Categorical mapping for reliable Plotly discrete legends
df["churn_status"] = df["churn_prediction"].map({0: "0 (Retained)", 1: "1 (At Risk)"})

# 5. KPI Calculations
total_cust = len(df)
churn_count = int((df["churn_prediction"] == 1).sum())
churn_rate = (churn_count / total_cust * 100.0) if total_cust > 0 else 0.0
at_risk_rev = df[df["churn_prediction"] == 1]["monetary"].sum()

# 6. Render KPI Banner
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{total_cust:,}")
col2.metric("High Risk Churns", f"{churn_count:,}")
col3.metric("Churn Rate", f"{churn_rate:.1f}%")
col4.metric("Revenue at Risk", f"${at_risk_rev:,.2f}")

st.divider()

# 7. Render Charts
c1, c2 = st.columns(2)

color_map = {
    "0 (Retained)": "#2ecc71",  # Green
    "1 (At Risk)": "#e74c3c"    # Red
}

with c1:
    st.subheader("Churn Probability Distribution")
    fig_hist = px.histogram(
        df,
        x="churn_probability",
        nbins=20,
        color="churn_status",
        color_discrete_map=color_map,
        labels={
            "churn_probability": "Churn Risk Score",
            "churn_status": "Status",
            "count": "Customer Count"
        },
        template="plotly_dark"
    )
    fig_hist.update_layout(bargap=0.1, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.subheader("Monetary Value vs. Recency")
    fig_scatter = px.scatter(
        df,
        x="recency_days",
        y="monetary",
        size="frequency",
        color="churn_status",
        color_discrete_map=color_map,
        labels={
            "recency_days": "Recency (Days)",
            "monetary": "Monetary Value ($)",
            "churn_status": "Status",
            "frequency": "Order Frequency"
        },
        hover_data=["customer_id"],
        template="plotly_dark"
    )
    fig_scatter.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_scatter, use_container_width=True)