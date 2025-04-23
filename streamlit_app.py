# -------------------------------------
# 📊 DCA vs Lump Sum Simulator
# Streamlit App
# -------------------------------------

from datetime import datetime
import streamlit as st
from core.market_simulator import generate_price_series
from core.strategies import simulate_lump_sum, simulate_dca
import matplotlib.pyplot as plt
import pandas as pd

def run_multiple_simulations(n_runs, investment, start_price, periods, volatility):
    results = {"lump_sum": [], "dca": []}

    for i in range(n_runs):
        prices = generate_price_series(
            start_price=start_price,
            periods=periods,
            volatility=volatility,
            seed=i  # unterschiedliche Seeds für Vielfalt
        )
        ls = simulate_lump_sum(investment, prices)
        dca = simulate_dca(investment, prices)
        results["lump_sum"].append(ls["final_value"])
        results["dca"].append(dca["final_value"])

    return results

seed_input = st.number_input("🧪 Random Seed (optional)", min_value=0, value=42)

st.set_page_config(page_title="DCA vs Lump Sum Simulator", layout="centered")

st.title("💸 DCA vs Lump Sum Investment Simulator")

st.markdown("""
### 📘 What does this tool do?

This mini app simulates and compares two common investment strategies:

- **Lump Sum**: Investing the full amount at once
- **Dollar Cost Averaging (DCA)**: Spreading the investment over regular intervals

It helps visualize which approach performs better under simulated market conditions.
""")

# Input
investment = st.number_input("💰 Total Investment Amount", value=1200, help="This is the total amount you'll invest. It will be used for both strategies.")
periods = st.slider("📆 Number of Periods (Months)", min_value=3, max_value=24, value=12, help="How many months you want to split the investment across (used in DCA).")
volatility = st.slider("📉 Market Volatility", min_value=0.01, max_value=0.1, value=0.05, help="Controls the randomness of the market simulation. Higher means more fluctuation.")
start_price = st.number_input("📌 Start Price of Asset", value=100, help="The initial simulated price of the asset.")


# Simulate price series
start_price = st.number_input("📌 Start Price of Asset", value=100)
prices = generate_price_series(start_price=start_price, periods=periods, volatility=volatility, seed=seed_input)
st.line_chart(prices)

# 🧠 Strategy Selection
strategy_choice = st.selectbox("Select strategy to simulate", ["Both", "Lump Sum", "DCA"])
multi_sim = st.checkbox("🔁 Run multiple simulations (average over 10)")

# 📅 Aktuelles Datum und Uhrzeit anzeigen
now = datetime.now().strftime("%B %d, %Y – %H:%M")
st.caption(f"🕒 Simulation run on: {now}")

# Run simulations
# Run simulations based on selection
ls = dca = None

if multi_sim:
    sim_results = run_multiple_simulations(
        n_runs=10,
        investment=investment,
        start_price=start_price,
        periods=periods,
        volatility=volatility
    )
    avg_ls = sum(sim_results["lump_sum"]) / len(sim_results["lump_sum"])
    avg_dca = sum(sim_results["dca"]) / len(sim_results["dca"])

    st.subheader("📊 Average Results from 10 Simulations")
    st.write(f"💰 Lump Sum Avg Final Value: {round(avg_ls, 2)}")
    st.write(f"💰 DCA Avg Final Value: {round(avg_dca, 2)}")

else:
    if strategy_choice in ["Both", "Lump Sum"]:
        ls = simulate_lump_sum(investment, prices)
    if strategy_choice in ["Both", "DCA"]:
        dca = simulate_dca(investment, prices)


st.subheader("📊 Results")


if ls:
    gain_ls = round(ls["final_value"] - ls["initial_investment"], 2)
    if gain_ls >= 0:
        st.success(f"💰 Lump Sum Final Value: {round(ls['final_value'], 2)} (+{gain_ls})")
    else:
        st.error(f"📉 Lump Sum Final Value: {round(ls['final_value'], 2)} ({gain_ls})")

if dca:
    gain_dca = round(dca["final_value"] - dca["initial_investment"], 2)
    if gain_dca >= 0:
        st.success(f"💰 DCA Final Value: {round(dca['final_value'], 2)} (+{gain_dca})")
    else:
        st.error(f"📉 DCA Final Value: {round(dca['final_value'], 2)} ({gain_dca})")



# Plot comparison
fig, ax = plt.subplots()
import pandas as pd

# Ergebnisvergleich in DataFrame
if ls and dca:
    # 💡 Performance summary
    percent_diff = round(((ls["final_value"] - dca["final_value"]) / dca["final_value"]) * 100, 2)

    if percent_diff > 0:
        st.markdown(f"💡 **Lump Sum outperformed DCA by +{percent_diff}%**")
    elif percent_diff < 0:
        st.markdown(f"💡 **DCA outperformed Lump Sum by +{abs(percent_diff)}%**")
    else:
        st.markdown("💡 **Both strategies performed equally.**")

    # Ergebnisvergleich in DataFrame
    results_df = pd.DataFrame({
        "Strategy": ["Lump Sum", "DCA"],
        "Final Value": [ls["final_value"], dca["final_value"]]
    })

    diff = round(((ls["final_value"] - dca["final_value"]) / dca["final_value"]) * 100, 2)
    if diff > 0:
        st.success(f"📈 Lump Sum performed better by **{diff}%**")
    elif diff < 0:
        st.success(f"📈 DCA performed better by **{abs(diff)}%**")
    else:
        st.info("⚖️ Both strategies ended with the same value.")

    fig, ax = plt.subplots()
    colors = ["green" if ls["final_value"] > dca["final_value"] else "blue", "blue"]
    ax.bar(results_df["Strategy"], results_df["Final Value"], color=colors)
    ax.set_ylabel("Final Value (€)")
    st.pyplot(fig)

    # Comparison table
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

# 📤 Download-Button für CSV Export
csv = results_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Results as CSV",
    data=csv,
    file_name='strategy_results.csv',
    mime='text/csv',
)

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

def run_multiple_simulations(n_runs, investment, start_price, periods, volatility):
    results = {
        "lump_sum": [],
        "dca": [],
        "price_series": []
    }

    for i in range(n_runs):
        prices = generate_price_series(
            start_price=start_price,
            periods=periods,
            volatility=volatility,
            seed=i
        )
        ls = simulate_lump_sum(investment, prices)
        dca = simulate_dca(investment, prices)
        results["lump_sum"].append(ls["final_value"])
        results["dca"].append(dca["final_value"])
        results["price_series"].append(prices)

    return results


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
# 🧠 Strategy Insights
st.markdown("---")
st.subheader("📚 Strategy Insights")

with st.expander("💡 When is Lump Sum better?"):
    st.write("""
    - When the market is trending upward
    - When you want immediate full exposure
    - When you're confident in your timing
    """)

with st.expander("💡 When is DCA better?"):
    st.write("""
    - When the market is volatile or uncertain
    - When you're risk-averse
    - When you prefer smoother entry points
    """)
# ---
st.markdown("---")
st.markdown(
    "Made with ❤️ by Marc Göbel • [View on GitHub](https://github.com/marcgoebel/dca-vs-lumpsum)",
    unsafe_allow_html=True
)
