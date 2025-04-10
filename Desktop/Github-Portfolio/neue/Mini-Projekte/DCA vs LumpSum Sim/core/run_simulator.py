# run_simulation.py

from core.market_simulator import generate_price_series
from core.strategies import simulate_lump_sum, simulate_dca

# Markt generieren
prices = generate_price_series(seed=42)
print("📈 Preisreihe:", prices)

# Simulation durchführen
lump_sum_result = simulate_lump_sum(1200, prices)
dca_result = simulate_dca(1200, prices)

print("\n💰 Lump Sum Ergebnis:", lump_sum_result)
print("📆 DCA Ergebnis:", dca_result)
