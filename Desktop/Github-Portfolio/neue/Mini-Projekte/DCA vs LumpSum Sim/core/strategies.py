# core/strategies.py

import numpy as np

def simulate_lump_sum(investment_amount, price_series):
    """Simuliert eine Einmalanlage."""
    shares_bought = investment_amount / price_series[0]
    final_value = shares_bought * price_series[-1]
    return {
        "strategy": "Lump Sum",
        "initial_investment": investment_amount,
        "shares_bought": shares_bought,
        "final_value": final_value,
    }

def simulate_dca(total_investment, price_series):
    """Simuliert monatliches Investieren (DCA)."""
    n_periods = len(price_series)
    investment_per_period = total_investment / n_periods

    shares_bought = sum(investment_per_period / price for price in price_series)
    final_value = shares_bought * price_series[-1]

    return {
        "strategy": "DCA",
        "initial_investment": total_investment,
        "shares_bought": shares_bought,
        "final_value": final_value,
    }
