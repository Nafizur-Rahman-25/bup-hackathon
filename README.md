# BUP CSE Fest 2026

Smart Campus Energy Optimization Challenge

## Run

pip install -r requirements.txt

python -m uvicorn app:app --reload

## Endpoints

GET /health

POST /optimize-energy
## Supported Directives

- solar_reduction
- minimum_battery_reserve
- no_charge_window
- no_discharge_window
- max_grid_window
- no_op