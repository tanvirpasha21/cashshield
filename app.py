import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Cash Shield", layout="wide")

st.title("🛡️ Cash Shield")
st.caption("We replay your financial life many times to see if you survive real-world randomness.")

# -------------------------------------------------
# USER INPUTS — PLAIN LANGUAGE
# -------------------------------------------------

st.sidebar.header("Your Financial Reality")

starting_cash = st.sidebar.number_input("Cash you have right now (£)", 0, 100000, 5000)
months = st.sidebar.slider("How many months ahead?", 6, 24, 12)

income_avg = st.sidebar.number_input("Typical monthly income (£)", 0, 15000, 2800)
income_variation = st.sidebar.number_input("Income ups & downs (£)", 0, 5000, 400)

fixed_costs = st.sidebar.number_input("Fixed monthly bills (£)", 0, 10000, 1800)

spending_avg = st.sidebar.number_input("Flexible spending (£)", 0, 5000, 700)
spending_variation = st.sidebar.number_input("Spending ups & downs (£)", 0, 3000, 150)

shock_chance = st.sidebar.slider("Chance of a bad surprise each month", 0.0, 0.5, 0.2)
shock_size = st.sidebar.number_input("Cost of a bad surprise (£)", 0, 20000, 1500)

runs = st.sidebar.slider("How many possible futures to test?", 300, 3000, 1000)

# -------------------------------------------------
# WHAT-IF: JOB LOSS
# -------------------------------------------------

st.sidebar.header("What-If Scenarios")

job_loss = st.sidebar.checkbox("What if I lose my job?")
job_loss_month = st.sidebar.slider("Month job loss happens", 1, months, 3)
job_loss_income = st.sidebar.number_input("Income after job loss (£)", 0, 3000, 0)

# -------------------------------------------------
# CORE SIMULATION
# -------------------------------------------------

def simulate_life(start_cash):
    cash = start_cash
    lowest = cash

    for m in range(1, months + 1):

        if job_loss and m >= job_loss_month:
            income = job_loss_income
        else:
            income = max(0, np.random.normal(income_avg, income_variation))

        spending = max(0, np.random.normal(spending_avg, spending_variation))
        shock = shock_size if np.random.rand() < shock_chance else 0

        cash = cash + income - fixed_costs - spending - shock
        lowest = min(lowest, cash)

    return cash, lowest


# -------------------------------------------------
# MINIMUM SAFE BUFFER
# -------------------------------------------------

def find_safe_buffer(target_failure=0.05, step=250, max_cash=50000):
    for buffer in range(0, max_cash + step, step):
        failures = 0
        for _ in range(runs):
            _, low = simulate_life(buffer)
            if low < 0:
                failures += 1
        if failures / runs <= target_failure:
            return buffer, failures / runs
    return None, None


# -------------------------------------------------
# RUN MODEL
# -------------------------------------------------

if st.button("🔮 Predict My Cashflow Survival"):

    failures = 0
    ending_cash = []

    for _ in range(runs):
        end, low = simulate_life(starting_cash)
        ending_cash.append(end)
        if low < 0:
            failures += 1

    failure_rate = failures / runs

    # -------------------------------------------------
    # FINAL PREDICTION
    # -------------------------------------------------

    st.subheader("📉 Final Survival Prediction")

    if failure_rate > 0.3:
        st.error(f"High Risk — You run out of money in {failure_rate:.0%} of futures")
    elif failure_rate > 0.1:
        st.warning(f"Moderate Risk — Failure occurs in {failure_rate:.0%} of futures")
    else:
        st.success(f"Low Risk — You survive {100 - failure_rate*100:.0f}% of futures")

    # -------------------------------------------------
    # VISUAL
    # -------------------------------------------------

    fig, ax = plt.subplots()
    ax.hist(ending_cash, bins=30)
    ax.set_title("Where You End Up Across All Futures")
    ax.set_xlabel("Ending Cash (£)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # -------------------------------------------------
    # ROOT CAUSE RANKING
    # -------------------------------------------------

    st.subheader("🧩 Why Failure Happens (Ranked)")

    causes = []

    if starting_cash < fixed_costs * 2:
        causes.append(("Low cash buffer", "You have little protection against bad timing"))

    if fixed_costs > income_avg * 0.6:
        causes.append(("High fixed bills", "Bills dominate income during bad months"))

    if income_variation > income_avg * 0.25:
        causes.append(("Unstable income", "Income drops create cashflow gaps"))

    if shock_chance > 0.25:
        causes.append(("Frequent shocks", "Unexpected costs arrive often"))

    for i, (title, desc) in enumerate(causes, 1):
        st.markdown(f"**{i}. {title}** — {desc}")

    # -------------------------------------------------
    # AI NARRATIVE EXPLANATION
    # -------------------------------------------------

    st.subheader("🤖 AI Explanation")

    narrative = []

    if failure_rate > 0.25:
        narrative.append(
            "Your financial system is fragile. A few bad months in a row are enough to cause failure."
        )
    else:
        narrative.append(
            "Your finances are generally resilient, but randomness still matters."
        )

    if job_loss:
        narrative.append(
            "Job loss dramatically increases risk because income drops before expenses can adjust."
        )

    narrative.append(
        "The biggest threat is not overspending — it is bad timing combined with low cash buffers."
    )

    narrative.append(
        "Improving survival usually comes from increasing emergency cash or reducing fixed bills."
    )

    st.markdown("\n\n".join(narrative))

    # -------------------------------------------------
    # MINIMUM SAFE BUFFER RESULT
    # -------------------------------------------------

    st.subheader("🛡️ Minimum Safe Cash Buffer")

    safe_cash, safe_rate = find_safe_buffer()

    if safe_cash is not None:
        gap = max(0, safe_cash - starting_cash)
        st.success(
            f"To keep failure below 5%, you need **£{safe_cash}** in cash.\n\n"
            f"Your gap: **£{gap}**"
        )
    else:
        st.error("No safe buffer found within search range.")

    # -------------------------------------------------
    # ACTIONABLE FIXES
    # -------------------------------------------------

    st.subheader("🚑 What Improves Survival Fastest")

    st.markdown(
        """
- Increase emergency cash before optimising spending
- Reduce fixed bills first — they cause irreversibility
- Smooth income if possible
- Always plan for shocks happening early
"""
    )

st.caption("Cash Shield • Stochastic cashflow explained for humans")
