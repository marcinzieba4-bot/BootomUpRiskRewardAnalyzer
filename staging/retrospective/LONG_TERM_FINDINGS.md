# What worked over the long run (hindsight): eleven retrospective series, held 3-10 years

The earlier cross-ticker files (`CROSS_TICKER_FINDINGS.md`, `CROSS_TICKER_OUT_OF_SAMPLE.md`) score each date over at
most three years. This file asks two longer questions of the same eleven series (ACN, UNP, LOW, AAPL, AVGO, MSFT, NKE,
PEP, SHW, WMT, XOM):
1. Does an entry signal still matter 5-10 years later?
2. Did a simple monthly-investing rule, using only point-in-time readings, beat buying all eleven equally over
   2008-2026?

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number below is printed by `python3 staging/retrospective/long_term.py` (one section: `... long_term.py sim`). It
reads the point-in-time rows through `cross_ticker_oos.py` and daily closes and dividends through `retro_tool.fetch_prices`,
the same Yahoo source the outcome.json files use (it reproduces 40 of 40 sampled two-year outcomes exactly). Long
horizons **reinvest dividends**. The investing rules and their scoring were written into the script's docstring before
the first run, and every rule is reported, the losers included.

## The fact that dwarfs every rule: which stocks

Investing $1,000 a month from January 2008 to October 2026 ($226,000 in all), valued at the 2026-11-06 close:

| Rule | Final value | Annual return (IRR) |
|---|---|---|
| SPY (the S&P 500) | $987,464 | 13.9% |
| RSP (equal-weight S&P 500) | $809,351 | 12.2% |
| **EQUAL**: split equally across the eleven | **$2,292,503** | **21.2%** |

That 7.3-point lead is hindsight. The eleven were picked in 2026, and most are among the best large companies of the
period. Each one's median ten-year rate ran from +4.8%/yr (XOM) and +10.9% (PEP) to +27.1% (AAPL) and +37.1% (AVGO).
Choosing the businesses moved the result about seven times more than any timing rule below. This sample cannot show
that anyone could have chosen them in 2008. EQUAL is therefore the fair benchmark: every rule below draws on the same
eleven stocks.

## 1. Monthly investing: which rules beat EQUAL, and how consistently

Each month the $1,000 goes where the rule says, using only that date's point-in-time readings. Nothing is ever sold
(full rules in the script's docstring). "Windows" are every five-year (14) and ten-year (9) contribution run starting
in January, valued at its end. "Leave one out" re-runs the full period with each ticker removed in turn (11 runs).

| Rule | Full-period IRR | vs EQUAL | Beat EQUAL: 5y windows | 10y windows | Leave one out (worst) | Worst fall |
|---|---|---|---|---|---|---|
| **CRASH_FIRST**: equal across tickers in the crash zone, else EQUAL | 22.1% | **+0.9pp** | **13 of 14** | 7 of 9 | **11 of 11** (+0.2pp) | -37% |
| **FALL_RANKED**: more money the further below the 52-week high | 22.0% | **+0.8pp** | 10 of 14 | **8 of 9** | **11 of 11** (+0.7pp) | -37% |
| HOUSE_CHEAP: equal across class CHEAP, else EQUAL | 21.7% | +0.5pp | 9 of 14 | 7 of 9 | 10 of 11 (-0.3pp) | -33% |
| STRONG_RANKED: more money the stronger the 12-month gain | 21.0% | -0.2pp | 10 of 14 | 7 of 9 | 1 of 11 (-0.5pp) | -36% |
| SKIP_EXP_RUNNING: equal across tickers not expensive & running | 20.5% | **-0.7pp** | **1 of 14** | **0 of 9** | 1 of 11 (-1.0pp) | -36% |
| CHEAP_RANKED: more money the lower the own P/E percentile | 19.7% | **-1.5pp** | 6 of 14 | **1 of 9** | 1 of 11 (-1.9pp) | -33% |
| CHEAPEST_PE: all into the lowest own P/E percentile | 18.6% | **-2.6pp** | 6 of 14 | 4 of 9 | 1 of 11 (-3.8pp) | -44% |
| DEEPEST_FALL: all into the stock furthest below its high | 24.7% | +3.5pp | 7 of 14 | 6 of 9 | 11 of 11 (+2.6pp) | -38% |
| STRONGEST_12M: all into the largest 12-month gain | 26.7% | +5.4pp | 13 of 14 | 9 of 9 | 11 of 11 (+3.8pp) | -34% |

- **Adding to a durable holding when it is down worked, a little, almost everywhere.** CRASH_FIRST and FALL_RANKED
  kept every stock funded and moved new money toward the ones that had fallen. Each added under a point a year, but it
  survived every leave-one-out run and most windows. The drawdown was about EQUAL's.
- **Buying what was cheap against its own history cost money**: 1.5-2.6 points a year, beating EQUAL in 1 of 11
  leave-one-out runs.
- **Avoiding the expensive and rising cost money too**: it trailed EQUAL in 13 of 14 five-year windows and all nine
  ten-year windows. The stocks that looked expensive and kept rising were the ones that compounded.
- **The single-stock rules made the most and are the least trustworthy.**
  - DEEPEST_FALL put 21% of all its money into NKE and 21% into XOM. It beat EQUAL in only half the windows, and in
    2021-2025 it returned 6.6% a year against EQUAL's 18.3%.
  - STRONGEST_12M ended 61% in AVGO. In a sample of stocks picked because they ended up winners, "buy the one that ran
    most" is where the hindsight concentrates. Its diversified twin, STRONG_RANKED, showed no edge (1 of 11
    leave-one-out runs).
  - Treat both as untested until they are tried on a universe chosen without hindsight.

## 2. Single entries held 5-10 years: the fall still mattered, and less each year

Median annual rate minus the ticker's own base at the same horizon (share that beat the base). Start dates run to
2021-11 for five years and to 2016-11 for ten.

| Entry | 3y | 5y | 7y | 10y | vs SPY at 10y |
|---|---|---|---|---|---|
| crash (frozen rule) | +8.0pp (70%) | **+11.4pp (84%)** | +4.0pp (78%) | +2.5pp (70%) | +8.2pp/yr, 78% beat |
| cheap & falling (frozen rule) | +3.9pp (69%) | +5.4pp (81%) | +2.9pp (77%) | +1.6pp (71%) | +7.4pp/yr, 69% |
| 40%+ below the 52-week high | +21.6pp (76%) | +17.0pp (80%) | +5.3pp (74%) | +3.8pp (70%) | +9.2pp/yr, 96% |
| 30-40% below | +0.8pp (52%) | +4.3pp (79%) | +3.1pp (83%) | +1.4pp (70%) | +7.3pp/yr, 76% |
| within 10% of the high | -0.6pp (47%) | -1.0pp (43%) | -0.5pp (45%) | -0.4pp (46%) | +4.1pp/yr, 64% |
| expensive & running (frozen rule) | -2.2pp (43%) | **-3.0pp (33%)** | -1.3pp (36%) | -2.6pp (38%) | +5.5pp/yr, 82% |
| own P/E pctl 0-19 | +0.5pp (52%) | +0.3pp (52%) | +0.1pp (51%) | +0.7pp (63%) | +6.3pp/yr, 57% |
| own P/E pctl 80-100 | -1.6pp (45%) | -0.7pp (45%) | -0.3pp (47%) | -1.8pp (39%) | +4.6pp/yr, 71% |
| house tier BUY / AVOID | +0.6 / -0.9pp | -0.1 / -0.3pp | -0.0 / -0.0pp | +0.3 / -1.7pp | +7.5 / +2.3pp/yr |

- **A deep fall was still a better entry ten years on**, though the per-year edge shrinks as the early rebound is
  spread over more years. No crash or cheap & falling entry with a seven- or ten-year outcome lost money.
- **Expensive & running was a worse entry at every horizon** (-1.3 to -3.0 points a year against the stock's own base)
  and still beat SPY 76-84% of the time. It held the right stocks at a worse price.
- **Valuation shows up only at ten years, and weakly:** the 0-39th percentile beat its base 61-63% of the time, the
  80-100th 39%. The house tier did the same (BUY +0.3pp, AVOID -1.7pp).

Within each ticker's own series, the rank correlation of the trailing 12-month change with the forward annual rate is
positive in **11 of 11 at three, five and ten years** (9 of 11 at seven). The distance below the 52-week high is positive
in 9-10 of 11 at every horizon. The own P/E percentile is positive in 9 of 11 at three and five years and 7 of 11 at
seven and ten; MSFT and WMT are negative throughout, the re-rating case.

## Hypotheses (test before use)

1. **The long-run lever is the choice of businesses, then time in the market.** Timing rules moved the result by about
   a point a year; the choice of businesses moved it by about seven.
2. **Within a fixed list of durable businesses, adding new money to the ones furthest below their 52-week high (or in
   the crash zone) added under a point a year, consistently.** Keep every holding funded rather than going all-in on
   one faller (DEEPEST_FALL's 2021-2025 window, NKE).
3. **Do not tilt toward "cheap against its own history", and do not skip the expensive and rising.** Both cost money
   over 5-10 years in this sample.
4. **Test on a universe fixed in 2008 without hindsight** (for example that year's index members, failures included).
   Hypothesis 2 is price-only, so it can be tested there. Until then, hypothesis 2 and the single-stock rules rest on
   eleven companies chosen in 2026.

## What this cannot show

- **Survivorship.** All eleven exist, are large and were chosen in 2026. A buy-the-fall rule on a company that failed
  outright is not tested; NKE 2022-2024 is the nearest case.
- **The long horizons end early.** Ten-year outcomes start no later than 2016-11 and five-year ones no later than
  2021-11. The NKE 2022-2024 losses and ACN 2025-2026 are not in section 2's 5-10 year numbers. The crash entries at
  seven and ten years are mostly 2008-2009 and 2015-2016.
- **Overlap.** The five- and ten-year windows share most of their months, and the leave-one-out runs share ten of
  eleven stocks. They show consistency, not independent evidence.
- **No costs or taxes.** Monthly purchases with dividends reinvested, never sold.

Judgement calls that could carry hindsight: the rule list was fixed before the first run, but it was written after the
two earlier cross-ticker files had seen the two-year outcomes, which suggested looking at falls, cheapness and
strength. The 52-week buckets are the same in-sample cuts as `CROSS_TICKER_OUT_OF_SAMPLE.md`.
