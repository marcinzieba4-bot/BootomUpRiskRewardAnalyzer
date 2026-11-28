# A disciplined pattern search over the twenty-four series (hindsight)

**The question:** which point-in-time readings ranked stocks' next six months correctly, in every part of the sample?

**Signals tested, 16 in all**, each public by its as-of date:
- the house model: Ratio B, EPP gap, upside to BASE, adjusted gap, the conservative two-year return, the business
  dashboard, obsolescence risk;
- valuation: the own 10-year P/E percentile;
- earnings: the last fiscal year's EPS growth, and the latest quarter's EPS growth (reported);
- price: the 1-month, 12-month and 12-minus-1 price change, the distance below the 52-week high, volatility;
- income: dividend yield.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/pattern_search_24.py`, with `RETRO_UNIVERSE=all`.
- **Rows:** the first as-of date of each month for all twenty-four tickers, 5,168 ticker-months, 2008-01 to 2026-10.
  Entry is at the next close; the target is the six-month total return.
- **Fixed in advance:** the signals, the test and the replication rule, in the script's docstring.
- **Added after the first run, and labelled where printed:** `capm`, `years` and `posthoc`.

**The test.** Each month, rank the stocks by the signal and correlate the ranks with the next six months' returns. A
signal **replicates** only if:
- the correlation has the same sign in all four cells: ORIGINAL eleven and NEW thirteen, each over 2008-2016 and
  2017-2026;
- and its t-stat on all twenty-four over the full period is 2 or more (Newey-West, lag 6).

## 1. Four signals replicate, and they are one pattern: growth beat value

| Signal | ORIGINAL 08-16 | ORIGINAL 17-26 | NEW 08-16 | NEW 17-26 | ALL 24: mean IC | t | Months above 0 |
|---|---|---|---|---|---|---|---|
| **epp_gap** (further above the floor did better) | +0.132 | +0.096 | +0.002 | +0.131 | +0.104 | +2.75 | 66% |
| **pe_pctl** (dearer vs own history did better) | +0.086 | +0.052 | +0.020 | +0.100 | +0.081 | +2.34 | 63% |
| **vol** (more volatile did better) | +0.251 | +0.155 | +0.029 | +0.118 | +0.129 | +2.71 | 65% |
| **dy** (lower dividend yield did better) | -0.121 | -0.111 | -0.032 | -0.133 | -0.109 | -2.36 | 32% |
| rb (Ratio B) | -0.077 | -0.033 | +0.063 | +0.074 | +0.009 | +0.28 | 53% |
| chg_12m (momentum) | -0.016 | +0.136 | -0.038 | +0.032 | +0.042 | +1.06 | 57% |
| eps_q_g (quarterly EPS growth) | -0.030 | +0.052 | -0.108 | +0.031 | -0.018 | -0.61 | 49% |

The script prints all sixteen signals; none of the other twelve replicates. The four that do describe one style:
- **Growth, quality and high beta** beat **cheap, high-dividend value**: dearer stocks, further above their floor, more
  volatile, paying less.
- It held in both ticker sets and both halves of 2008-2026, a long stretch in which value lagged.
- **The house's own valuation readings did not replicate as stock pickers:** Ratio B, the BASE upside, the adjusted gap
  and the conservative two-year return.

## 2. As portfolios: more return, mostly from more market exposure

Long the best three each month, held 6 months, ALL twenty-four (annual return / Sharpe / worst drawdown):

| Book | Full period | 2008-2016 | 2017-2026 | ORIGINAL only | NEW only | Beta | Return beyond beta x SPY (t) |
|---|---|---|---|---|---|---|---|
| EQUAL (reference) | +17.1% / 0.94 / -46% | +15.6% / 0.80 | +18.6% / 1.10 | +17.9% / 1.08 | +15.8% / 0.76 | 1.00 | +5.6% (3.35) |
| **pe_pctl, best 3** | **+21.1% / 0.98 / -47%** | +20.7% / 0.95 | +21.5% / 1.01 | +20.7% / 1.05 | +16.8% / 0.74 | **1.06** | **+8.8% (3.13)** |
| epp_gap, best 3 | +22.7% / 0.87 / -52% | +17.3% / 0.73 | +27.9% / 0.98 | +21.3% / 0.98 | +19.0% / 0.75 | 1.35 | +8.3% (2.25) |
| dy (lowest), best 3 | +24.0% / 0.79 / -62% | +14.1% / 0.52 | +33.8% / 1.10 | +18.3% / 0.87 | +24.9% / 0.80 | 1.64 | +7.9% (1.65) |
| vol, best 3 | +29.6% / 0.84 / -67% | +24.6% / 0.71 | +34.3% / 1.00 | +27.0% / 1.11 | +23.6% / 0.72 | 1.84 | +11.4% (2.09) |
| composite of the four, best 3 | +27.6% / 0.95 / -57% | +18.4% / 0.72 | +36.6% / 1.14 | +22.0% / 0.97 | +21.7% / 0.76 | 1.50 | +11.1% |

- **Every book beat EQUAL on return, in both ticker sets,** but only `pe_pctl` did it without taking more risk.
  Buying the three stocks trading dearest against their own history added 4 points a year, at a beta of 1.06, with
  about EQUAL's Sharpe and drawdown.
- **The others mostly bought more market exposure:** betas of 1.35-1.84 and drawdowns of -52% to -67%.
- **EQUAL itself earns +5.6% a year beyond its beta.** That is the hindsight in a list of twenty-four companies picked in
  2026. The signals' extra return over EQUAL is about 2-6 points a year.

**As long/shorts** (best three minus worst three) the spreads are not reliable once market exposure is removed:

| Long/short | Annual / Sharpe / worst drawdown | Beta | Return beyond beta x SPY (t) |
|---|---|---|---|
| pe_pctl | +2.5% / 0.23 / -63% | 0.09 | +4.8% (0.81) |
| epp_gap | +4.4% / 0.30 / -68% | 0.44 | +3.3% (0.51) |
| dy | +8.6% / 0.42 / -64% | 0.92 | +2.7% (0.40) |
| vol | +20.7% / 0.69 / -55% | 1.44 | +8.0% (1.28) |
| composite | +14.1% / 0.59 / -49% | - | - |

**And they broke in 2022, when value won.**

| 2022 | Long/short |
|---|---|
| pe_pctl | -34% |
| epp_gap | -39% |
| dy | -43% |
| vol | -25% |
| *EQUAL (reference)* | *-3%* |

The long books lost 24-35% that year, against 15% for SPY. That is the risk of a style bet: it pays for years and then
gives back a large share at once.

## 3. Within each stock, the other way round: buy it after it fell

The rank correlation of each signal with the same stock's next six months, ticker by ticker:

| Signal | Tickers where a lower reading did better | Median correlation |
|---|---|---|
| chg_1m (the last month) | **23 of 24** | -0.08 |
| dd_52w (below the 52-week high) | **20 of 24** (deeper did better) | -0.10 |
| chg_12m | 19 of 24 | -0.09 |
| dy (own yield high vs its history did better) | **20 of 24** the other way | +0.22 |

- **Across stocks, dear and strong won. Within one stock, the time to buy was after a fall:** after a weak month, deep
  below its high, or with its yield high against its own history.
- This repeats the long-horizon finding of `LONG_TERM_FINDINGS.md` and `CROSS_TICKER_OUT_OF_SAMPLE.md`. Much of it is
  every stock bouncing together after a market sell-off (2008-2009, 2020).

**Post-hoc combination** (chosen after reading sections 1-3; a lead, not a finding): take the composite's top eight,
then buy the three that just fell.

| Book | Return | Sharpe | Worst drawdown | Beta |
|---|---|---|---|---|
| Composite top 3 alone | +27.6% | 0.95 | -57% | 1.50 |
| Top 8, then the weakest last month (1m) | +25.8% | 0.96 | -52% | 1.33 |
| Top 8, then the deepest below the high (6m) | +28.5% | 0.97 | -61% | 1.54 |

Combining the two added nothing measurable.

## Summary

1. **The one pattern that replicated everywhere is a style:** growth, quality and high beta beat cheap, high-yield
   value in 2008-2026. Four readings show it: a high EPP gap, a high own P/E percentile, high volatility, a low dividend
   yield.
2. **Most of its extra return is market exposure.** As long/shorts, none is reliable beyond beta (t 0.4-1.3), and all
   broke in 2022.
3. **The most balanced version:** long the three stocks trading dearest against their own 10-year P/E history, held six
   months. It returned +21.1% a year against EQUAL's +17.1%, with the same Sharpe and drawdown, in both ticker sets.
4. **Timing within a stock** (buy it after a fall) held in 20-23 of 24 series. It is a reason to add on dips, not a way
   to pick between stocks.
5. **The house valuation readings (Ratio B, BASE upside, the adjusted gap) did not pick stocks** in the wider sample.

## The newest month (October 2026)

| Signal | Best three | Worst three |
|---|---|---|
| pe_pctl | AAPL, CAT, UNP | PEP, ACN, CMCSA |
| epp_gap | CAT, NVDA, AVGO | LOW, ACN, CMCSA |
| dy (lowest yield) | NVDA, AAPL, MSFT | F, BMY, PFE |
| vol | ACN, RCL, AVGO | PEP, KMI, SO |

These are hindsight hypotheses, not a model output or advice.

## Limits

- **Survivorship:** all twenty-four are companies chosen in 2026, and a sixteen-signal search will find something.
- **The replication rule** (four cells, |t| >= 2) limits false positives, but with sixteen signals one could pass by
  chance.
- **Period:** these years favoured growth over value. 2022 shows what a turn does to the style signals.
- **Not modelled:** costs and taxes. The books hold three names and turn over often.
