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

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🛡️ CashShield")
st.caption("Simulate your financial future. Understand risk. Get clear advice.")

st.markdown(
    """
CashShield runs **thousands of future scenarios** based on your real finances  
and explains what *actually* puts you at risk — in plain English.
"""
)

# -------------------------------------------------
# USER INPUTS
# -------------------------------------------------
st.subheader("Your Monthly Reality")

income = st.number_input("Income (£)", min_value=0.0, step=100.0, value=2800.0)
fixed_expenses = st.number_input("Fixed bills (£)", min_value=0.0, step=50.0, value=1800.0)
variable_expenses = st.number_input("Flexible spending (£)", min_value=0.0, step=50.0, value=700.0)
savings = st.number_input("Current savings (£)", min_value=0.0, step=100.0, value=5000.0)

months = st.slider("Months to simulate", 6, 24, 12)
runs = st.slider("Number of futures to simulate", 500, 3000, 1500)

# -------------------------------------------------
# MONTE CARLO SIMULATION
# -------------------------------------------------
def monte_carlo_simulation(
    income,
    fixed_expenses,
    variable_expenses,
    savings,
    months,
    runs
):
    all_runs = []

    for _ in range(runs):
        balance = savings
        path = []

        for _ in range(months):
            income_real = np.random.normal(income, income * 0.05)
            expense_real = np.random.normal(
                fixed_expenses + variable_expenses,
                (fixed_expenses + variable_expenses) * 0.1
            )

            balance += max(0, income_real) - max(0, expense_real)
            path.append(balance)

        all_runs.append(path)

    return np.array(all_runs)

# -------------------------------------------------
# GROK (xAI) LLM
# -------------------------------------------------
def run_llm(prompt):
    api_key = st.secrets["XAI_API_KEY"]

    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "grok-2-latest",
        "messages": [
            {
                "role": "system",
                "content": "You are a calm, supportive personal financial analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.4,
        "max_tokens": 400
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]

# -------------------------------------------------
# RUN ANALYSIS
# -------------------------------------------------
if st.button("🔮 Analyze My Financial Survival"):

    if income <= 0:
        st.error("Income must be greater than zero.")
        st.stop()

    results = monte_carlo_simulation(
        income,
        fixed_expenses,
        variable_expenses,
        savings,
        months,
        runs
    )

    final_balances = results[:, -1]
    failures = np.sum(results.min(axis=1) < 0)
    failure_rate = failures / runs

    median_path = np.median(results, axis=0)
    worst_case = np.percentile(results, 10, axis=0)

    # -------------------------------------------------
    # VISUALIZATION
    # -------------------------------------------------
    st.subheader("📉 Your Possible Futures")

    fig, ax = plt.subplots()
    ax.plot(median_path, label="Typical outcome")
    ax.plot(worst_case, linestyle="--", label="Bad-case scenario (10%)")
    ax.axhline(0)
    ax.set_xlabel("Months")
    ax.set_ylabel("Cash (£)")
    ax.legend()

    st.pyplot(fig)

    # -------------------------------------------------
    # RISK SUMMARY
    # -------------------------------------------------
    st.subheader("⚠️ Financial Risk Summary")

    if failure_rate > 0.3:
        risk = "High Risk"
        st.error(f"You run out of money in **{failure_rate:.0%}** of futures.")
    elif failure_rate > 0.1:
        risk = "Moderate Risk"
        st.warning(f"You run out of money in **{failure_rate:.0%}** of futures.")
    else:
        risk = "Low Risk"
        st.success(f"You survive **{100 - failure_rate*100:.0f}%** of futures.")

    monthly_surplus = income - (fixed_expenses + variable_expenses)

    # -------------------------------------------------
    # ROOT CAUSES
    # -------------------------------------------------
    st.subheader("🧩 Why Risk Exists")

    if monthly_surplus < 0:
        st.write("• You spend more than you earn — even small shocks cause failure.")
    if fixed_expenses > income * 0.6:
        st.write("• Fixed bills are too high and hard to adjust during bad months.")
    if savings < fixed_expenses * 2:
        st.write("• Cash buffer is too small to absorb bad timing.")
    if monthly_surplus > 0 and savings > fixed_expenses * 3:
        st.write("• Risk mainly comes from randomness, not behavior.")

    # -------------------------------------------------
    # AI EXPLANATION
    # -------------------------------------------------
    st.subheader("🤖 AI Financial Explanation")

    prompt = f"""
User data:
Income: £{income}
Fixed expenses: £{fixed_expenses}
Variable spending: £{variable_expenses}
Savings: £{savings}
Monthly surplus: £{monthly_surplus}
Failure rate: {failure_rate:.2%}
Risk level: {risk}

Explain:
1. Their financial situation in simple terms
2. What the real danger is (without shaming)
3. 3 clear, realistic actions they can take

Avoid jargon. Be human and practical.
"""

    with st.spinner("Thinking..."):
        ai_response = run_llm(prompt)

    st.write(ai_response)

    # -------------------------------------------------
    # FINAL ADVICE
    # -------------------------------------------------
    st.subheader("🛠️ What Improves Survival Fastest")

    st.markdown(
        """
- Build emergency cash before optimizing spending  
- Reduce **fixed** bills first — they create irreversible risk  
- Expect bad months to happen early, not later  
- Stability matters more than perfection
"""
    )

st.caption("CashShield • Monte Carlo simulation + Grok AI")
