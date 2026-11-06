"""
Fund Analysis: compare a small set of ETFs on return, risk and drawdown
using public price data from Yahoo Finance (via yfinance).

Run:  python fund_analysis.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # saves charts to files, no display needed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---- Settings you can change -------------------------------------------
TICKERS = ["SPY", "VT", "AGG", "GLD"]  
START = "2021-01-01"
END = None                              
RISK_FREE_RATE = 0.03                   
TRADING_DAYS = 252
OUTPUT_DIR = Path("output")
# -------------------------------------------------------------------------


def load_prices(tickers, start, end=None, retries=3):
    """Download adjusted close prices one ticker at a time, with retries."""
    import time
    import yfinance as yf

    series = {}
    for ticker in tickers:
        for attempt in range(1, retries + 1):
            try:
                df = yf.download(ticker, start=start, end=end,
                                 auto_adjust=True, progress=False, threads=False)
                close = df["Close"]
                if hasattr(close, "columns"):  # newer yfinance returns a one-column table
                    close = close.iloc[:, 0]
                if not close.dropna().empty:
                    series[ticker] = close
                    break
            except Exception as e:
                print(f"{ticker}: attempt {attempt} failed ({e})")
            time.sleep(3)
        else:
            print(f"{ticker}: could not be downloaded")

    missing = [t for t in tickers if t not in series]
    if missing:
        raise SystemExit(f"No data for {missing}. Check your connection or try again later.")

    return pd.DataFrame(series).ffill().dropna()


def compute_metrics(prices, risk_free=RISK_FREE_RATE):
    """Return a summary table, daily returns and drawdown series."""
    returns = prices.pct_change().dropna()
    years = (prices.index[-1] - prices.index[0]).days / 365.25

    total_return = prices.iloc[-1] / prices.iloc[0] - 1
    cagr = (1 + total_return) ** (1 / years) - 1
    volatility = returns.std() * np.sqrt(TRADING_DAYS)
    sharpe = (returns.mean() * TRADING_DAYS - risk_free) / volatility

    drawdown = prices / prices.cummax() - 1
    max_drawdown = drawdown.min()

    summary = pd.DataFrame({
        "Total return": total_return,
        "Annualised return (CAGR)": cagr,
        "Annualised volatility": volatility,
        "Sharpe ratio": sharpe,
        "Max drawdown": max_drawdown,
    })
    return summary, returns, drawdown


def plot_growth(prices, path):
    (prices / prices.iloc[0] * 100).plot(figsize=(10, 5))
    plt.title("Growth of 100 invested")
    plt.ylabel("Value")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def plot_drawdown(drawdown, path):
    drawdown.plot(figsize=(10, 5))
    plt.title("Drawdown from previous peak")
    plt.ylabel("Drawdown")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def plot_correlation(returns, path):
    corr = returns.corr()
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(corr, vmin=-1, vmax=1, cmap="RdYlGn")
    ax.set_xticks(range(len(corr)), corr.columns)
    ax.set_yticks(range(len(corr)), corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
    fig.colorbar(im)
    ax.set_title("Correlation of daily returns")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()


def run(prices, output_dir=OUTPUT_DIR):
    output_dir.mkdir(exist_ok=True)
    summary, returns, drawdown = compute_metrics(prices)

    summary.to_csv(output_dir / "summary.csv")
    plot_growth(prices, output_dir / "growth.png")
    plot_drawdown(drawdown, output_dir / "drawdown.png")
    plot_correlation(returns, output_dir / "correlation.png")

    print(summary.round(3).to_string())
    return summary


if __name__ == "__main__":
    run(load_prices(TICKERS, START, END))
