# Stops and S&P 500 hedges on the combined book with the yield tilt (hindsight)

**The question:** which risk controls improve `COMBO_BOOK.md`'s combined book, and is the S&P's 100-day average the best
hedge signal?
- **The book:** 2 growth picks plus 2 value picks, 75/25 toward the sleeve the 10-year yield trend favours, held 1 month.
- **Per-position stops:** 11, from none to fixed, trailing, re-entry and volatility-sized.
- **Portfolio overlays:** 15, from SPY shorts on 50/100/200-day averages to cash, a death cross, a 10% drawdown,
  volatility spikes, volatility targeting and the book's own trend.

**The book is post-hoc** (`COMBO_BOOK.md`). This test only ranks controls, under a rule fixed before the first run.
Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/combo_risk.py`, from daily total-return data, 2008-01-07 to
2026-11-17.
- **Fixed in its docstring:** the grid and the rule.
- **The one fix after the first run:** volatility-sized stops fall back to 15% where the price file has under 20 days of
  history (the first weeks of 2008).
- **The engine check:** its trailing-15% book reproduces `combo_book.py`'s +27.47%.

**The rule.** A control improves the book if, after costs:
- its Sharpe is higher in both 2008-2016 and 2017-2026;
- its worst drawdown is shallower.

The highest full-period Sharpe among those that pass is the best.

**Mechanics:**
- **Hedge:** a short in SPY worth the stated share of the book, traded at the close after the S&P signal.
- **Costs:** 0.10% on each change in hedge or exposure.
- **Cash and the short earn nothing.**

## A. Stops (no hedge)

| Stop | Annual | Sharpe | Worst drawdown | Sharpe 2008-16 | Sharpe 2017-26 | Passes |
|---|---|---|---|---|---|---|
| none | +26.5% | 1.08 | -58.3% | 0.86 | 1.32 | baseline |
| **fixed -10%** | **+27.7%** | **1.22** | -40.2% | 1.04 | 1.41 | **yes, best** |
| fixed -15% | +27.5% | 1.16 | -40.6% | 1.00 | 1.34 | yes |
| fixed -20% | +27.8% | 1.15 | -47.9% | 0.98 | 1.32 | no |
| trailing -10% | +25.7% | 1.19 | -37.3% | 1.00 | 1.38 | yes |
| trailing -15% (`COMBO_BOOK.md`'s main) | +27.5% | 1.19 | -38.7% | 1.00 | 1.39 | yes |
| trailing -20% | +27.4% | 1.15 | -46.5% | 0.99 | 1.31 | no |
| trailing -15%, re-entry above the 50-day | +27.7% | 1.19 | -41.8% | 1.00 | 1.40 | yes |
| trailing -20%, re-entry | +27.5% | 1.15 | -46.5% | 0.99 | 1.31 | no |
| trailing 2x monthly volatility | +25.5% | 1.07 | -60.0% | 0.78 | 1.39 | no |
| trailing 3x monthly volatility | +26.7% | 1.10 | -58.1% | 0.87 | 1.34 | yes (barely) |

- **Any 10-15% stop per stock cuts the worst drawdown from -58% to about -37% to -42%** at no cost in return.
- **The differences between the 10-15% stops are small:** Sharpe 1.16-1.22.
- **20% stops and volatility-sized stops did little.**

## B. Overlays on the book with the 15% trailing stop

| Overlay | Annual | Sharpe | Worst drawdown | Sharpe 2008-16 | Sharpe 2017-26 | Passes | Days on | Changes a year |
|---|---|---|---|---|---|---|---|---|
| none | +27.5% | 1.19 | -38.7% | 1.00 | 1.39 | baseline | 0% | 0 |
| short 50% below the 50-day | +23.1% | 1.16 | -29.5% | 1.00 | 1.33 | no | 31% | 17.8 |
| short 100% below the 50-day | +18.0% | 0.95 | -29.9% | 0.81 | 1.08 | no | 31% | 17.8 |
| **short 50% below the 100-day** | +24.9% | 1.24 | -28.8% | 1.05 | 1.43 | yes | 26% | 11.2 |
| short 100% below the 100-day | +21.6% | 1.10 | -28.5% | 0.92 | 1.28 | no | 26% | 11.2 |
| **short 50% below the 200-day** | +25.7% | 1.27 | **-26.6%** | 1.13 | 1.40 | yes | 23% | 5.7 |
| short 100% below the 200-day | +23.2% | 1.17 | -23.9% | 1.08 | 1.25 | no | 23% | 5.7 |
| short at the book's beta below the 100-day | +21.8% | 1.12 | -29.3% | 0.90 | 1.33 | no | 26% | 69.2 |
| all cash below the 100-day | +16.9% | 1.06 | -25.1% | 0.68 | 1.37 | no | 26% | 11.2 |
| half cash below the 100-day | +22.5% | 1.22 | -26.9% | 0.97 | 1.46 | no | 26% | 11.2 |
| short 50% while the 50-day is under the 200-day | +26.0% | 1.25 | -26.4% | 1.15 | 1.35 | no | 24% | 1.0 |
| **short 50% while the S&P is 10% off its high** | +25.7% | 1.26 | -29.0% | 1.10 | 1.41 | yes | 20% | 4.7 |
| **short 50% while S&P 21-day volatility > 25%** | **+27.3%** | **1.29** | -30.5% | 1.17 | 1.40 | **yes, best** | 12% | 1.8 |
| volatility target 20% | +22.8% | 1.19 | -30.1% | 1.10 | 1.28 | no | 38% | 98.3 |
| volatility target 25% | +25.4% | 1.22 | -30.5% | 1.11 | 1.32 | no | 22% | 55.5 |
| half cash when the book is below its own 100-day | +23.2% | 1.18 | -29.2% | 0.96 | 1.40 | no | 21% | 7.8 |

**On the other bases:**
- **With no stop:**
  - The same volatility-spike hedge won: +26.7%, Sharpe 1.22, -45.1%.
  - Also passing: half hedges on the 50/100/200-day, a 100% hedge on the 100/200-day, half cash below the 100-day, the
    10%-off-high hedge, and the book's own trend.
  - A hedge alone is a poor substitute for the stop. Without a stop, a half hedge left at best a -43.8% drawdown. Only a
    100% hedge got it near -28%, at a cost of 3.6-5.1 points a year.
- **On the fixed -10% stop:**
  - The volatility hedge missed the rule by about 0.01 of Sharpe in 2017-2026 (1.40 against 1.41).
  - The 10%-off-high hedge won instead: +25.9%, Sharpe 1.28, -27.1%.
- **That near-tie is the point:** the rule cannot separate the good hedges from one another.

**The combined pick (C): fixed -10% stop + short 50% while 10% off the high.** +25.9% / Sharpe 1.28 / -27.1%, Calmar
0.96.

## Stress windows (descriptive)

| Spell | No stop, no hedge | Trailing -15% | + volatility hedge | + 100-day hedge | Fixed -10% + off-high hedge | SPY |
|---|---|---|---|---|---|---|
| Lehman crash (Sep 2008 to Mar 2009) | -55.5% | -36.0% | -16.4% | -14.1% | -16.0% | -46.4% |
| US downgrade (Jul to Oct 2011) | -11.3% | -9.6% | -6.5% | -1.5% | +3.8% | -17.9% |
| China / oil (Aug 2015 to Feb 2016) | -14.4% | -14.4% | -13.3% | -12.8% | -21.7% | -12.1% |
| Q4 2018 (Sep to Dec 2018) | -25.5% | -26.2% | -26.2% | -20.7% | -21.6% | -19.3% |
| Covid crash (Feb to Mar 2020) | -29.1% | -19.4% | -6.7% | -5.0% | -2.4% | -33.7% |
| 2022 bear (Jan to Oct 2022) | -7.5% | -5.9% | -1.2% | -3.0% | -1.5% | -24.5% |
| Tariff shock (Feb to Apr 2025) | -15.7% | -15.1% | -14.4% | -7.9% | -14.2% | -18.8% |

- **The volatility hedge catches fast crashes** (2008, 2020) and misses slow slides (Q4 2018, 2025).
- **The 100-day hedge catches both kinds**, but costs about 2.6 points a year in whipsaws. Its worst years against the
  unhedged book are 2010 (+8.7% against +15.2%), 2012 (+11.7% against +20.5%) and 2019 (+36.2% against +48.7%).
- **2018 is not fixable by any control.** Every version lost 18-22%, because the value picks fell in a market that
  dropped only 5%.

## Summary

1. **Keep a 10-15% stop on each stock.** It does most of the risk work: the worst drawdown falls from -58% to about -39%
   with no loss of return.
2. **Add a half SPY hedge (short 50% of the book's value) in bad markets.** On the trailing-stop book it takes the worst
   drawdown to about -27% to -31% and the Sharpe to 1.24-1.29.
   - **Best by the rule:** short while S&P 21-day volatility is above 25%. It costs only 0.2 points a year but only
     protects in crashes.
   - **The 200-day average:** about -27%, for 1.8 points a year.
   - **The 100-day average:** about -29%, for 2.6 points a year.
   - **Full (100%) hedges, all-cash and fast (50-day) signals cost too much.**
3. **Combine a fast trigger with a slow one** to cover both crashes and slow slides: for example the volatility spike
   plus the 200-day average. That pairing is a natural next test, but it is untested here, and a small sample (about
   four crashes in 19 years) decides every ranking in this file.

## The signals now (S&P 500 close 7,334 on 2026-11-17)

| Signal | Reading | Hedge |
|---|---|---|
| 50-day average | 7,655 (S&P -4.2%) | on |
| 100-day average | 7,626 (-3.8%) | **on** |
| 200-day average | 7,344 (-0.1%) | on, by a hair |
| 50-day under the 200-day | no | off |
| Off the 252-day high | -6.2% | off |
| 21-day volatility | 21.9% | off |

These are hindsight hypotheses applied to point-in-time data, not advice.
