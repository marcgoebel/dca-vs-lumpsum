# streamlit_app.py

import streamlit as st
from core.market_simulator import generate_price_series
from core.strategies import simulate_lump_sum, simulate_dca
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="DCA vs Lump Sum Simulator", layout="centered")

st.title("💸 DCA vs Lump Sum Investment Simulator")

# Input
investment = st.number_input("💰 Total Investment Amount", value=1200)
periods = st.slider("📆 Number of Periods (Months)", min_value=3, max_value=24, value=12)
volatility = st.slider("📉 Market Volatility", min_value=0.01, max_value=0.1, value=0.05)

# Simulate price series
start_price = st.number_input("📌 Start Price of Asset", value=100)
prices = generate_price_series(start_price=start_price, periods=periods, volatility=volatility, seed=42)
st.line_chart(prices)

# Run simulations
ls = simulate_lump_sum(investment, prices)
dca = simulate_dca(investment, prices)

# Output results
st.subheader("📊 Results")
st.write("**Lump Sum Final Value:**", round(ls["final_value"], 2))
st.write("**DCA Final Value:**", round(dca["final_value"], 2))

# Plot comparison
fig, ax = plt.subplots()
import pandas as pd

# Ergebnisvergleich in DataFrame
results_df = pd.DataFrame({
    "Strategy": ["Lump Sum", "DCA"],
    "Final Value": [ls["final_value"], dca["final_value"]]
})

# Prozentdifferenz
diff = round(((ls["final_value"] - dca["final_value"]) / dca["final_value"]) * 100, 2)
if diff > 0:
    st.success(f"📈 Lump Sum performed better by **{diff}%**")
elif diff < 0:
    st.success(f"📈 DCA performed better by **{abs(diff)}%**")
else:
    st.info("⚖️ Both strategies ended with the same value.")

# Plot mit Farben
fig, ax = plt.subplots()
colors = ["green" if ls["final_value"] > dca["final_value"] else "blue", "blue"]
ax.bar(results_df["Strategy"], results_df["Final Value"], color=colors)
ax.set_ylabel("Final Value (€)")
st.pyplot(fig)

# Vergleichstabelle anzeigen
st.subheader("📋 Strategy Comparison Table")

st.table(pd.DataFrame([
    {
        "Strategy": ls["strategy"],
        "Initial Investment": ls["initial_investment"],
        "Shares Bought": round(ls["shares_bought"], 2),
        "Final Value": round(ls["final_value"], 2),
    },
    {
        "Strategy": dca["strategy"],
        "Initial Investment": dca["initial_investment"],
        "Shares Bought": round(dca["shares_bought"], 2),
        "Final Value": round(dca["final_value"], 2),
    }
]))
