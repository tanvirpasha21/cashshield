from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import SimulationInput, SimulationResult
from app.simulation import run_simulation
from app.ai import run_llm

app = FastAPI(title="CashShield API")

# Allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "CashShield API is running"}

@app.post("/simulate", response_model=SimulationResult)
def simulate(data: SimulationInput):
    result = run_simulation(data)
    return result

@app.post("/explain")
def explain(simulation_result: dict):
    prompt = f"""
    Here is the simulation result:
    {simulation_result}

    Explain in plain English:
    1. What’s happening financially
    2. The real danger
    3. Three practical actions
    """
    explanation = run_llm(prompt)
    return {"explanation": explanation}
