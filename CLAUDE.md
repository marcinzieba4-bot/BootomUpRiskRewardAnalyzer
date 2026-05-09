# BottomUp Risk/Reward Analyzer — Developer Notes

## Current Stock Price

**ALWAYS fetch the current price from the internet before building or updating any signal model.**

Claude's training data has a knowledge cutoff (currently August 2025). Any hardcoded price in a model file is stale by definition. Do not guess or estimate the price from training data.

### How to get a live price

Use the `WebSearch` or `WebFetch` tool to look up the ticker before writing `CURRENT_PRICE`:

```
WebSearch: "ISRG stock price today"
WebFetch:  https://finance.yahoo.com/quote/ISRG/
```

Acceptable sources: Yahoo Finance, Google Finance, Marketwatch, Bloomberg.

Record the price, date, and source in a comment next to `CURRENT_PRICE` in the model file:

```python
CURRENT_PRICE = 512.34   # ISRG — fetched from Yahoo Finance, 2026-05-09
```

This rule applies to **every ticker** in this repo (AVGO, SYK, ISRG, MSFT, etc.).

## Model File Conventions

- One file per ticker: `{ticker_lower}_signal_model.py`
- All prices in USD
- EPS figures are non-GAAP (normalized), full fiscal year
- EPP = EPS × min-viable trough P/E (the floor, not the target)
- Horizon is 2 years from the analysis date unless noted otherwise
