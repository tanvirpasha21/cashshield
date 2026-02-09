import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import requests
from config import BACKEND_URL

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="CashShield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ CashShield – Financial Risk Dashboard")
st.markdown("Stress-test your finances in real-time and see interactive insights.")

# -------------------------------
# SIDEBAR INPUTS
# -------------------------------
with st.sidebar:
    st.header("💰 Your Monthly Reality")
    income = st.number_input("Monthly income (£)", 0.0, step=100.0, value=2800.0)
    fixed_expenses = st.number_input("Fixed bills (£)", 0.0, step=50.0, value=1800.0)
    variable_expenses = st.number_input("Flexible spending (£)", 0.0, step=50.0, value=700.0)
    savings = st.number_input("Current savings (£)", 0.0, step=100.0, value=5000.0)
    
    st.header("⚡ Life Shocks")
    job_loss_prob = st.slider("Chance of job loss (%)", 0, 20, 5) / 100
    job_loss_duration = st.slider("Months without income", 1, 6, 3)
    emergency_prob = st.slider("Chance of emergency (%)", 0, 20, 7) / 100
    emergency_cost = st.number_input("Emergency cost (£)", 200, 5000, 1200, step=100)

    st.header("🛠️ What-If Fixes")
    delta_income = st.number_input("Increase income (£)", -500, 1000, 0, step=100)
    delta_fixed = st.number_input("Reduce fixed bills (£)", -1000, 0, 0, step=100)
    delta_savings = st.number_input("Add to savings (£)", 0, 10000, 0, step=500)

    months = st.slider("Months to simulate", 6, 24, 12)
    runs = st.slider("Simulation runs", 500, 3000, 1500)

# -------------------------------
# RUN SIMULATION
# -------------------------------
if st.button("🔮 Run Survival Test", use_container_width=True):
    monthly_surplus = income - (fixed_expenses + variable_expenses)
    payload = {
        "income": income,
        "fixed_expenses": fixed_expenses,
        "variable_expenses": variable_expenses,
        "savings": savings,
        "months": months,
        "runs": runs,
        "job_loss_prob": job_loss_prob,
        "job_loss_duration": job_loss_duration,
        "emergency_prob": emergency_prob,
        "emergency_cost": emergency_cost,
        "delta_income": delta_income,
        "delta_fixed": delta_fixed,
        "delta_savings": delta_savings
    }

    with st.spinner("Running simulation..."):
        try:
            resp = requests.post(f"{BACKEND_URL}/simulate", json=payload, timeout=60)
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            st.error(f"Simulation failed: {e}")
            st.stop()

    failure_rate = result["failure_rate"]
    improved_rate = result["improved_rate"]
    median_path = result["median_path"]
    worst_case = result["worst_case"]
    median_fail = result["median_fail"]

    # -------------------------------
    # RISK INDICATOR
    # -------------------------------
    st.subheader("🚨 Financial Risk Summary")
    col1, col2 = st.columns(2)
    col1.metric("Failure Rate (Now)", f"{failure_rate:.0%}")
    col2.metric("Failure Rate (After Fix)", f"{improved_rate:.0%}", delta=f"{(failure_rate-improved_rate):.0%}")

    if failure_rate > 0.3:
        st.error("High Risk – take action now!")
        risk_level = "High Risk"
    elif failure_rate > 0.1:
        st.warning("Moderate Risk – monitor closely.")
        risk_level = "Moderate Risk"
    else:
        st.success("Low Risk – finances look healthy.")
        risk_level = "Low Risk"

    # -------------------------------
    # INTERACTIVE CHART (Plotly)
    # -------------------------------
    st.subheader("📊 Your Financial Future Paths")
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=median_path, mode="lines", name="Typical Path", line=dict(color="#1f77b4")))
    fig.add_trace(go.Scatter(y=worst_case, mode="lines", name="Bad-Case (10%)", line=dict(color="#ff7f0e", dash="dash")))
    fig.add_hline(y=0, line_color="red", line_dash="dot")
    fig.update_layout(xaxis_title="Month", yaxis_title="Balance (£)", height=400)
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # TIME TO FAILURE
    # -------------------------------
    st.subheader("⏱️ When Problems Usually Start")
    if median_fail:
        st.warning(f"Most failures happen around **month {median_fail}**.")
    else:
        st.success("Most futures survive the full period.")

    # -------------------------------
    # AI EXPLANATION
    # -------------------------------
    st.subheader("🤖 AI Explanation (Plain-English)")

    prompt = {
        "simulation_result": {
            "income": income,
            "fixed_expenses": fixed_expenses,
            "variable_expenses": variable_expenses,
            "savings": savings,
            "monthly_surplus": monthly_surplus,
            "failure_rate": failure_rate,
            "risk_level": risk_level
        }
    }

    with st.spinner("Getting AI explanation..."):
        try:
            ai_resp = requests.post(f"{BACKEND_URL}/explain", json=prompt, timeout=60)
            ai_resp.raise_for_status()
            explanation = ai_resp.json().get("explanation", "AI explanation unavailable.")
        except Exception as e:
            explanation = f"⚠️ AI explanation failed: {e}"

    st.write(explanation)

st.caption("CashShield v2.3 • API-driven • Interactive Dashboard • Human-readable Insights")
