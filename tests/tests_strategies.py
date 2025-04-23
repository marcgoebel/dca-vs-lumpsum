# tests/test_strategies.py

from core.strategies import simulate_lump_sum, simulate_dca

def test_simulate_lump_sum():
    prices = [100, 105, 110]
    result = simulate_lump_sum(1000, prices)
    assert result["shares_bought"] == 10
    assert round(result["final_value"], 2) == 1100.00

def test_simulate_dca():
    prices = [100, 105, 110]
    result = simulate_dca(300, prices)
    # Erwartete Shares ≈ (100/100 + 100/105 + 100/110) = 2.87…
    assert round(result["shares_bought"], 2) == 2.87
    assert round(result["final_value"], 2) == round(2.87 * 110, 2)
