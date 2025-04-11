# streamlit_app.py

import streamlit as st
from core.market_simulator import generate_price_series
from core.strategies import simulate_lump_sum, simulate_dca
import matplotlib.pyplot as plt

st.set_page_config(page_title="DCA vs Lump Sum Simulator", layout="centered")

st.title("💸 DCA vs Lump Sum Investment Simulator")

# Input
investment = st.number_input("💰 Total Investment Amount", value=1200)
periods = st.slider("📆 Number of Periods (Months)", min_value=3, max_value=24, value=12)
volatility = st.slider("📉 Market Volatility", min_value=0.01, max_value=0.1, value=0.05)

# Simulate price series
prices = generate_price_series(start_price=100, periods=periods, volatility=volatility, seed=42)
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
ax.bar(["Lump Sum", "DCA"], [ls["final_value"], dca["final_value"]])
ax.set_ylabel("Final Value (€)")
st.pyplot(fig)
