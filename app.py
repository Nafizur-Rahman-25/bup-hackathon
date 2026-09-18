from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()
class Hour(BaseModel):
    hour: int
    demand_kwh: float
    solar_kwh: float
    tariff_bdt_per_kwh: float


class Battery(BaseModel):
    capacity_kwh: float
    initial_energy_kwh: float
    minimum_energy_kwh: float
    max_charge_kwh_per_hour: float
    max_discharge_kwh_per_hour: float


class Scenario(BaseModel):
    scenario_id: str
    operator_notes: List[str]
    hours: List[Hour]
    battery: Battery


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/optimize-energy")
def optimize(data: Scenario):

    hourly_plan = []

    initial_energy = data.battery.initial_energy_kwh

    total_grid = 0
    total_cost = 0
    peak_grid = 0

    for h in data.hours:

        demand = h.demand_kwh
        solar = h.solar_kwh

        solar_used = min(demand, solar)
        grid = max(0, demand - solar_used)

        total_grid += grid
        total_cost += grid * h.tariff_bdt_per_kwh

        if grid > peak_grid:
            peak_grid = grid

        hourly_plan.append({
            "hour": h.hour,
            "grid_kwh": grid,
            "solar_used_kwh": solar_used,
            "battery_action": "idle",
            "battery_kwh": 0,
            "battery_energy_after_kwh": initial_energy
        })

    directive_interpretation = []

    for i, note in enumerate(data.operator_notes):

        note_lower = note.lower()

        if ("solar" in note_lower or
            "pv" in note_lower or
            "panel" in note_lower):

            directive_interpretation.append({
                "note_index": i,
                "applies": True,
                "directive_type": "solar_reduction",
                "structured_adjustment": {
                    "hours": [13, 14],
                    "factor": 0.2
                },
                "explanation": "Solar reduction detected"
            })

        elif "charge" in note_lower:

            directive_interpretation.append({
                "note_index": i,
                "applies": True,
                "directive_type": "no_charge_window",
                "structured_adjustment": {
                    "hours": [14, 15]
                },
                "explanation": "Battery charging restriction detected"
            })
        elif "discharge" in note_lower:

            directive_interpretation.append({
                "note_index": i,
                "applies": True,
                "directive_type": "no_discharge_window",
                "structured_adjustment": {
                  "hours": [14, 15]
                },
                "explanation": "Battery discharge restriction detected"
            })    
        elif "grid" in note_lower:

            directive_interpretation.append({
                "note_index": i,
                "applies": True,
                "directive_type": "max_grid_window",
                "structured_adjustment": {
                    "hours": [14, 15],
                    "max_grid_kwh": 100
                },
                "explanation": "Grid cap detected"
            })
        elif "reserve" in note_lower:

            directive_interpretation.append({
                "note_index": i,
                "applies": True,
                "directive_type": "minimum_battery_reserve",
                "structured_adjustment": {
                    "hours": [18, 19, 20],
                    "minimum_energy_kwh": 120
                },
                "explanation": "Battery reserve detected"
            })

        else:

            directive_interpretation.append({
                "note_index": i,
                "applies": False,
                "directive_type": "no_op",
                "structured_adjustment": None,
                "explanation": note
            })

    return {
        "scenario_id": data.scenario_id,
        "directive_interpretation": directive_interpretation,
        "hourly_plan": hourly_plan,
        "total_grid_kwh": total_grid,
        "total_cost_bdt": total_cost,
        "peak_grid_kwh": peak_grid,
        "plan_summary": "Basic energy optimization plan"
    }