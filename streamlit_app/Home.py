import streamlit as st

st.set_page_config(
    page_title="MegaMart Intelligence Center",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 MegaMart Operations & Governance Portal")
st.caption("Local Gold Layer Analytics | PySpark + Iceberg + XGBoost Pipeline")

st.markdown("""
Welcome to the MegaMart ML & Data Control Center. Select a view from the sidebar:

* **📊 Executive Overview:** Revenue at risk, high-level churn metrics, and customer RFM breakdown.
* **👤 Customer 360:** Individual customer lookup, churn probability score, and SHAP feature drivers.
* **🛠️ Ops & Data Quality:** Iceberg table metrics, pipeline commit logs, and schema integrity.
* **🤖 ML Model Governance:** Population Stability Index (PSI) drift tracking and retraining triggers.
""")

st.info("System Status: Native local pipeline active | Local Storage Mode")