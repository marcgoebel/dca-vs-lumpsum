# tests/test_multi_sim.py

from core.market_simulator import generate_price_series
from core.strategies import simulate_lump_sum, simulate_dca
from streamlit_app import run_multiple_simulations  # ← falls dort definiert

def test_run_multiple_simulations():
    results = run_multiple_simulations(
        n_runs=5,
        investment=1000,
        start_price=100,
        periods=12,
        volatility=0.05
    )
    assert len(results["lump_sum"]) == 5
    assert len(results["dca"]) == 5
    assert len(results["price_series"]) == 5
    assert all(isinstance(val, float) for val in results["lump_sum"])
    assert all(isinstance(val, float) for val in results["dca"])
