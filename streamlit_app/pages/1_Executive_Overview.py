import streamlit as st
import plotly.express as px
from utils import load_gold_churn_data

st.set_page_config(page_title="Executive Overview", page_icon="📊", layout="wide")
st.title("📊 Executive Churn & Revenue Risk")

df = load_gold_churn_data()

# Top KPI Bar
col1, col2, col3, col4 = st.columns(4)
total_cust = len(df)
churn_count = df['churn_prediction'].sum()
churn_rate = (churn_count / total_cust) * 100 if total_cust > 0 else 0
at_risk_rev = df[df['churn_prediction'] == 1]['monetary'].sum()

col1.metric("Total Customers", f"{total_cust:,}")
col2.metric("High Risk Churns", f"{churn_count:,}")
col3.metric("Churn Rate", f"{churn_rate:.1f}%")
col4.metric("Revenue at Risk", f"${at_risk_rev:,.2f}")

st.divider()

# Charts
c1, c2 = st.columns(2)

with c1:
    st.subheader("Churn Probability Distribution")
    fig_hist = px.histogram(
        df,
        x="churn_probability",
        nbins=20,
        color="churn_prediction",
        color_discrete_sequence=["#2ecc71", "#e74c3c"],
        labels={"churn_probability": "Churn Risk Score", "churn_prediction": "Predicted Churn"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.subheader("Monetary Value vs. Recency")
    fig_scatter = px.scatter(
        df,
        x="recency_days",
        y="monetary",
        size="frequency",
        color="churn_prediction",
        color_discrete_sequence=["#2ecc71", "#e74c3c"],
        hover_data=["customer_id"]
    )
    st.plotly_chart(fig_scatter, use_container_width=True)