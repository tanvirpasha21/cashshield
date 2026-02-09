import numpy as np
from typing import Tuple, List

def monte_carlo(
    income, fixed, variable, savings,
    months, runs,
    job_loss_prob, job_loss_duration,
    emergency_prob, emergency_cost
) -> Tuple[np.ndarray, List[int]]:
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
            expense_real = np.random.normal(fixed + variable, (fixed + variable) * 0.1)

            # Emergency
            if np.random.rand() < emergency_prob:
                expense_real += emergency_cost

            # Update balance
            balance += max(0, income_real) - max(0, expense_real)
            path.append(balance)

            if balance < 0 and failed is None:
                failed = m + 1

            unemployed = max(0, unemployed - 1)

        paths.append(path)
        fail_months.append(failed)

    return np.array(paths), fail_months

def run_simulation(data) -> dict:
    # Base scenario
    base, fail_months = monte_carlo(
        data.income, data.fixed_expenses, data.variable_expenses, data.savings,
        data.months, data.runs,
        data.job_loss_prob, data.job_loss_duration,
        data.emergency_prob, data.emergency_cost
    )

    # Improved scenario (what-if fixes)
    improved, _ = monte_carlo(
        data.income + data.delta_income,
        data.fixed_expenses + data.delta_fixed,
        data.variable_expenses,
        data.savings + data.delta_savings,
        data.months, data.runs,
        data.job_loss_prob, data.job_loss_duration,
        data.emergency_prob, data.emergency_cost
    )

    failure_rate = float(np.mean(base.min(axis=1) < 0))
    improved_rate = float(np.mean(improved.min(axis=1) < 0))

    median_path = base.mean(axis=0).tolist()
    worst_case = np.percentile(base, 10, axis=0).tolist()

    fail_clean = [m for m in fail_months if m]
    median_fail = int(np.median(fail_clean)) if fail_clean else None

    return {
        "base_paths": base.tolist(),
        "improved_paths": improved.tolist(),
        "failure_rate": failure_rate,
        "improved_rate": improved_rate,
        "median_path": median_path,
        "worst_case": worst_case,
        "median_fail": median_fail
    }
