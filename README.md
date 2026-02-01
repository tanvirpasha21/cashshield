# 🛡️ CashShield

**CashShield** is a personal cashflow risk simulator that helps individuals understand
*whether their finances can survive real-world randomness*.

Instead of budgets and averages, CashShield runs **thousands of possible futures**
using Monte Carlo simulation and explains the results in clear, human language.

---

## 🔍 What Problem Does CashShield Solve?

Most personal finance tools assume:
- Income is stable
- Expenses are predictable
- Bad events happen “later”

Real life doesn’t work that way.

CashShield answers one simple but critical question:

> **“If randomness hits me, do I survive?”**

---

## 🧠 How It Works (Conceptually)

1. You enter your real financial situation  
2. CashShield simulates **hundreds to thousands of future timelines**
3. Each future includes:
   - Income volatility
   - Spending variability
   - Bad timing
4. Results are aggregated into:
   - Risk of running out of money
   - Typical vs worst-case trajectories
   - Clear, actionable insights

---

## ✨ Key Features

- 📉 Monte Carlo cashflow simulation
- 🔮 Risk-based survival analysis (not averages)
- 📊 Visual future trajectories
- 🤖 AI-generated plain-English explanations (local LLM)
- 🧩 Root-cause analysis of financial fragility
- 🛠 Actionable recommendations (not guilt-based budgeting)

---

## 🖥 Tech Stack

| Layer | Technology |
|----|----|
| Frontend | Streamlit |
| Simulation Engine | NumPy |
| Visualisation | Matplotlib |
| AI Reasoning | LLaMA 3 via Ollama (local) |
| Language | Python |

No cloud AI. No paid APIs. Privacy-first by design.

---

## 🚀 Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/cashshield.git
cd cashshield

### 2. Install dependecies
```bash
pip install -r requirements.txt

### 3. Install local AI
```bash
ollama run llama3
If Ollama is not installed, the simulation still works — only AI explanations are skipped.

### 4. Run the app
```bash
streamlit run app.py



## How to use Cashshield?

Enter your financial reality

Monthly income

Fixed monthly bills

Flexible spending

Current savings

Choose your simulation settings

How many months ahead to simulate

How many possible futures to test

Run the analysis

Click “Analyze My Financial Survival”

Review the results

Your probability of running out of money

Typical vs worst-case cash trajectories

Risk classification (Low / Moderate / High)

Key reasons your finances fail or survive

Read the AI explanation

Plain-English summary of your situation

What actually puts you at risk

3 clear, realistic actions to improve survival

Use the insights

Focus on reducing fixed costs

Increase emergency buffers

Plan for bad timing, not perfect months

⚠️ Important Notes

CashShield is for education and insight, not financial advice

Results depend on realistic inputs

Risk ≠ failure — it highlights vulnerability, not judgment



