import numpy as np

def generate_price_series(start_price=100, periods=12, volatility=0.05, seed=None):
    """Erzeugt eine einfache Preisreihe mit zufälliger Schwankung."""
    if seed is not None:
        np.random.seed(seed)

    returns = np.random.normal(loc=0.005, scale=volatility, size=periods)
    prices = [start_price]

    for r in returns:
        prices.append(prices[-1] * (1 + r))

    return np.round(prices, 2)
