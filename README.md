# Fund Analysis

A Python script that compares four ETFs on return, risk and drawdown, using public price data from Yahoo Finance.

![Growth of 100 invested](output/growth.png)

## Results

These results use data from 4 January 2021 to 5 November 2026.

| Fund | Total return | Annual return (CAGR) | Volatility | Sharpe ratio | Max drawdown |
|---|---:|---:|---:|---:|---:|
| SPY | 114.6% | 14.0% | 16.7% | 0.69 | -24.5% |
| VT | 83.7% | 11.0% | 15.8% | 0.55 | -26.4% |
| AGG | -2.5% | -0.4% | 5.8% | -0.56 | -18.0% |
| GLD | 105.9% | 13.2% | 18.5% | 0.60 | -28.3% |

The Sharpe ratios assume a fixed risk-free rate of 3%.

## Key findings

The script writes these findings from the data each time it runs:

- SPY grew fastest at 14.0% a year. AGG grew slowest at -0.4% a year.
- SPY had the best return for its risk, with a Sharpe ratio of 0.69.
- GLD had the biggest price swings, with 18.5% volatility.
- GLD had the deepest fall from a peak, at -28.3%.
- VT moved most like SPY (correlation 0.97), and GLD moved least like it (0.17).
- An equal mix of the funds had 10.7% volatility, against a 14.2% average for the funds on their own.

## What this might mean

Over this period, what a fund invested in seemed to matter more for diversification than how many funds were held. VT moved almost in step with SPY, so it added little diversification, while gold and bonds moved much more independently. An equal mix of all four was noticeably less volatile than the average fund.

Low correlation didn't guarantee good results, though. AGG had a low correlation with SPY but still lost money overall and fell 18.0% from its peak.

These results have some limits:

- They cover one period of under six years, and a different period could change the picture.
- They exclude tax and trading costs.
- Past returns don't predict future returns.

![Drawdown from previous peak](output/drawdown.png)

![Correlation of daily returns](output/correlation.png)

## How to run it

```bash
pip install -r requirements.txt
python fund_analysis.py
```

The script saves the charts, a `summary.csv` file and a `findings.txt` file to the `output` folder.

To compare different funds or dates, change the settings at the top of `fund_analysis.py`.

This project is for learning and isn't investment advice.
