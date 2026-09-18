from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("/optimize-energy")
def optimize(data: dict):

    hourly_plan = []

    initial_energy = data["battery"]["initial_energy_kwh"]

    total_grid = 0
    total_cost = 0
    peak_grid = 0

    for h in data["hours"]:

        demand = h["demand_kwh"]
        solar = h["solar_kwh"]

        solar_used = min(demand, solar)
        grid = max(0, demand - solar_used)

        total_grid += grid
        total_cost += grid * h["tariff_bdt_per_kwh"]

        if grid > peak_grid:
            peak_grid = grid

        hourly_plan.append({
            "hour": h["hour"],
            "grid_kwh": grid,
            "solar_used_kwh": solar_used,
            "battery_action": "idle",
            "battery_kwh": 0,
            "battery_energy_after_kwh": initial_energy
        })

    directive_interpretation = []

    for i, note in enumerate(data["operator_notes"]):

        directive_interpretation.append({
            "note_index": i,
            "applies": False,
            "directive_type": "no_op",
            "structured_adjustment": None,
            "explanation": note
        })

    return {
        "scenario_id": data["scenario_id"],
        "directive_interpretation": directive_interpretation,
        "hourly_plan": hourly_plan,
        "total_grid_kwh": total_grid,
        "total_cost_bdt": total_cost,
        "peak_grid_kwh": peak_grid,
        "plan_summary": "Basic energy optimization plan"
    }