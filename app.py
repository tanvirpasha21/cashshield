import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import requests

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="CashShield",
    page_icon="🛡️",
    layout="centered"
)

st.title("🛡️ CashShield")
st.caption("See financial risk before it hits. Then change it.")

st.markdown("""
CashShield stress-tests your finances against **real life**,  
so you can understand risk *without shame or jargon*.
""")

# -------------------------------------------------
# OPENROUTER LLM
# -------------------------------------------------
def run_llm(prompt: str) -> str:
    """
    Sends a prompt to OpenRouter and returns the response.
    Fails gracefully if the API is unavailable.
    """
    api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not api_key:
        return "⚠️ OpenRouter API key not found."

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://cashshield.app",
        "X-Title": "CashShield"
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a calm, supportive financial guide. "
                    "Explain financial risk without jargon or shame. "
                    "Be clear, honest, and practical."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.4,
        "max_tokens": 400
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception:
        return "⚠️ AI explanation unavailable. Results shown without commentary."


# =================================================
# STEP 1 — CORE FINANCES
# =================================================
st.header("1️⃣ Your Monthly Reality")

with st.expander("Enter your real numbers", expanded=True):
    income = st.number_input("Monthly income (£)", 0.0, step=100.0, value=2800.0)
    fixed_expenses = st.number_input("Fixed bills (£)", 0.0, step=50.0, value=1800.0)
    variable_expenses = st.number_input("Flexible spending (£)", 0.0, step=50.0, value=700.0)
    savings = st.number_input("Current savings (£)", 0.0, step=100.0, value=5000.0)

monthly_surplus = income - (fixed_expenses + variable_expenses)

# =================================================
# STEP 2 — TIME & REALISM
# =================================================
st.header("2️⃣ Stress Test Settings")

with st.expander("How hard should we stress-test?", expanded=True):
    months = st.slider("Months to simulate", 6, 24, 12)
    runs = st.slider("Number of simulated futures", 500, 3000, 1500)

# =================================================
# STEP 3 — LIFE SHOCKS
# =================================================
st.header("3️⃣ Real-Life Shocks")

with st.expander("Things that happen to normal people"):
    col1, col2 = st.columns(2)

    with col1:
        job_loss_prob = st.slider("Chance of job loss per month (%)", 0, 20, 5) / 100
        job_loss_duration = st.slider("Months without income", 1, 6, 3)

    with col2:
        emergency_prob = st.slider("Chance of emergency per month (%)", 0, 20, 7) / 100
        emergency_cost = st.number_input("Emergency cost (£)", 200, 5000, 1200, step=100)

# =================================================
# STEP 4 — WHAT IF FIXES
# =================================================
st.header("4️⃣ Try a What-If Fix")

with st.expander("Test changes safely"):
    delta_income = st.number_input("Increase income (£)", -500, 1000, 0, step=100)
    delta_fixed = st.number_input("Reduce fixed bills (£)", -1000, 0, 0, step=100)
    delta_savings = st.number_input("Add to savings (£)", 0, 10000, 0, step=500)

# =================================================
# MONTE CARLO ENGINE
# =================================================
def monte_carlo(
    income, fixed, variable, savings,
    months, runs,
    job_loss_prob, job_loss_duration,
    emergency_prob, emergency_cost
):
    paths = []
    fail_months = []

    for _ in range(runs):
        balance = savings
        unemployed = 0
        path = []
        failed = None

        for m in range(months):
            # Job loss event
            if unemployed == 0 and np.random.rand() < job_loss_prob:
                unemployed = job_loss_duration

            # Income & expenses
            income_real = 0 if unemployed else np.random.normal(income, income * 0.05)
            expense_real = np.random.normal(
                fixed + variable,
                (fixed + variable) * 0.1
            )

            # Emergency event
            if np.random.rand() < emergency_prob:
                expense_real += emergency_cost

            # Update balance
            balance += max(0, income_real) - max(0, expense_real)
            path.append(balance)

            # Track failure month
            if balance < 0 and failed is None:
                failed = m + 1

            unemployed = max(0, unemployed - 1)

        paths.append(path)
        fail_months.append(failed)

    return np.array(paths), fail_months

# =================================================
# RUN ANALYSIS
# =================================================
if st.button("🔮 Run Survival Test", use_container_width=True):

    if income <= 0:
        st.error("Income must be greater than zero.")
        st.stop()

    base, fail_months = monte_carlo(
        income, fixed_expenses, variable_expenses, savings,
        months, runs,
        job_loss_prob, job_loss_duration,
        emergency_prob, emergency_cost
    )

    improved, _ = monte_carlo(
        income + delta_income,
        fixed_expenses + delta_fixed,
        variable_expenses,
        savings + delta_savings,
        months, runs,
        job_loss_prob, job_loss_duration,
        emergency_prob, emergency_cost
    )

    failure_rate = np.mean(base.min(axis=1) < 0)
    improved_rate = np.mean(improved.min(axis=1) < 0)

    median_path = np.median(base, axis=0)
    worst_case = np.percentile(base, 10, axis=0)

    fail_clean = [m for m in fail_months if m]
    median_fail = int(np.median(fail_clean)) if fail_clean else None

    # =================================================
    # RESULTS — RISK FIRST
    # =================================================
    st.header("🚨 Your Financial Risk")

    if failure_rate > 0.3:
        risk = "High Risk"
        st.error(f"High risk — you fail in **{failure_rate:.0%}** of futures.")
    elif failure_rate > 0.1:
        risk = "Moderate Risk"
        st.warning(f"Moderate risk — failure in **{failure_rate:.0%}** of futures.")
    else:
        risk = "Low Risk"
        st.success(f"Low risk — survival in **{100 - failure_rate*100:.0f}%** of futures.")

    # =================================================
    # VISUAL
    # =================================================
    st.subheader("📉 What Your Future Could Look Like")

    fig, ax = plt.subplots()
    ax.plot(median_path, label="Typical path")
    ax.plot(worst_case, "--", label="Bad-case (10%)")
    ax.axhline(0)
    ax.legend()
    st.pyplot(fig)

    # =================================================
    # TIME TO FAILURE
    # =================================================
    st.subheader("⏱️ When Problems Usually Start")

    if median_fail:
        st.warning(f"Most failures happen around **month {median_fail}**.")
    else:
        st.success("Most futures survive the full period.")

    # =================================================
    # ROOT CAUSES
    # =================================================
    st.subheader("🧩 Why Risk Exists")

    if monthly_surplus < 0:
        st.write("• You spend more than you earn.")
    if fixed_expenses > income * 0.6:
        st.write("• Fixed bills are too high to adjust quickly.")
    if savings < fixed_expenses * 2:
        st.write("• Your cash buffer is too thin.")
    if monthly_surplus > 0 and savings > fixed_expenses * 3:
        st.write("• Risk mainly comes from bad timing, not habits.")

    # =================================================
    # ACTION IMPACT
    # =================================================
    st.subheader("📊 Do Your Changes Help?")

    col1, col2 = st.columns(2)
    col1.metric("Failure Rate (Now)", f"{failure_rate:.0%}")
    col2.metric(
        "Failure Rate (After Fix)",
        f"{improved_rate:.0%}",
        delta=f"{(failure_rate - improved_rate):.0%}"
    )

    # =================================================
    # AI EXPLANATION
    # =================================================
    st.subheader("🤖 Plain-English Explanation")

    prompt = f"""
Income: £{income}
Fixed expenses: £{fixed_expenses}
Variable spending: £{variable_expenses}
Savings: £{savings}
Monthly surplus: £{monthly_surplus}
Failure rate: {failure_rate:.2%}
Risk level: {risk}

Explain:
1. What’s happening financially
2. The real danger
3. Three practical actions
"""

    with st.spinner("Thinking…"):
        st.write(run_llm(prompt))

st.caption("CashShield v2.3 • OpenRouter • Clear Risk • Human Explanations")
