from pydantic import BaseModel
from typing import Optional

class SimulationInput(BaseModel):
    income: float
    fixed_expenses: float
    variable_expenses: float
    savings: float
    months: int
    runs: int
    job_loss_prob: float
    job_loss_duration: int
    emergency_prob: float
    emergency_cost: float
    delta_income: Optional[float] = 0
    delta_fixed: Optional[float] = 0
    delta_savings: Optional[float] = 0

class SimulationResult(BaseModel):
    base_paths: list
    improved_paths: list
    failure_rate: float
    improved_rate: float
    median_path: list
    worst_case: list
    median_fail: Optional[int]
