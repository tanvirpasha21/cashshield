# CashShield v2  
### Financial Risk Simulation & Decision Support Tool

CashShield is a **probabilistic financial resilience simulator** that helps users understand **how often their finances fail under uncertainty — and why**.

Unlike traditional budgeting tools that rely on averages and static assumptions, CashShield models **thousands of possible financial futures** to expose hidden risk, fragility, and timing effects.

> CashShield doesn’t predict the future.  
> It shows how often things go wrong — and what actually matters.

---

## 🚩 The Problem

Most personal finance tools assume:
- Stable income  
- Predictable expenses  
- Smooth monthly averages  

Real life is not like that.

Income fluctuates.  
Expenses spike unexpectedly.  
Job loss and emergencies happen at the worst times.

Two people with identical monthly budgets can have **radically different survival outcomes** — and most tools fail to reveal that risk.

---

## ✅ The Solution

CashShield uses **Monte Carlo simulation** to generate thousands of realistic financial paths, allowing users to:

- Estimate probability of financial failure
- Identify when and why failure occurs
- Compare “what-if” scenarios safely
- Understand risk without judgement or shame

Crucially, **simulation is authoritative**.  
AI is used only to *interpret* results — never to generate or modify them.

---

## 🧠 Core Design Principles (v2)

- **Simulation First**  
  All risk metrics come from deterministic, auditable models.

- **AI Is Non-Authoritative**  
  LLMs explain results but never influence calculations.

- **Risk > Advice**  
  The system highlights fragility instead of telling users what to do.

- **Emotionally Safe UX**  
  No moral framing. No “you should”. Just clarity.

- **Failure Is a System Property**  
  Not a personal flaw.

---

## 🔬 How It Works

1. User inputs income, expenses, savings, and risk parameters
2. Thousands of financial futures are simulated
3. Each path models:
   - Income volatility
   - Job loss events
   - Emergency expenses
   - Expense variability
4. Outcomes are aggregated into:
   - Failure probability
   - Time-to-failure distribution
   - Median and downside trajectories
5. Optional AI layer explains the results in plain language

---

## 📊 Features

- Monte Carlo cashflow simulation engine
- Financial survival probability analysis
- Failure month detection
- Visual future paths (median + downside)
- Scenario comparison (“what-if fixes”)
- Modular AI explanation layer (optional)
- Streamlit-based interactive interface

---

## 🛠 Tech Stack

- Python
- NumPy
- Pandas
- Streamlit
- Optional LLM integration (local or OpenRouter)
- Probabilistic modeling

---

## 📐 Architecture Overview

User Input
    ↓
Monte Carlo Simulation (Authoritative)
    ↓
Risk Metrics & Paths
    ↓
Visualisation Layer
    ↓
Optional AI Explanation (Non-authoritative)
```

**Key Principle:** AI **never** feeds back into the simulation.
---

## ⚠️ Disclaimer

CashShield is **not financial advice**.  
It is an educational and analytical tool designed to improve risk awareness and decision understanding.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/cashshield.git
cd cashshield
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

---

## 🧪 Example Use Cases

* Understanding financial fragility despite positive cashflow
* Comparing savings strategies under uncertainty
* Stress-testing lifestyle changes
* Teaching probabilistic thinking in finance
* Research into decision-making under risk

---

## 🧭 Roadmap

* User profile persistence
* Scenario comparison dashboard
* Research validation with user studies
* SaaS deployment
* Academic publication variant

---

## 👤 Author

**MD Tanvir Anjum**  
Builder focused on risk, simulation, and responsible AI design.

---

## 💡 Why This Project Matters

CashShield demonstrates:

* Product thinking under uncertainty
* Responsible AI architecture
* Simulation-based decision systems
* UX for emotionally sensitive domains
* Evolution from v1 → v2 driven by insight, not hype

---

## ⭐ If This Resonates

Feel free to star the repo, open issues, or reach out to discuss:

* FinTech
* Decision science
* AI ethics
* Simulation systems

---