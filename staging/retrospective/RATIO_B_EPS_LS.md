# Long the lowest Ratio B, short falling EPS: optimised on half the years, judged on the other (hindsight)

**The book:** long 100% in the N lowest point-in-time Ratio B stocks. Short a sleeve of the stocks whose EPS is falling
(`EPP_SHORT.md`, "Adding a falling-EPS filter").
- **Rebalancing:** monthly; entry at the next day's close; dividends reinvested, and paid on the shorts.
- **Not modelled:** costs, borrow fees and cash interest.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/ratio_b_eps_ls.py`. The procedure was fixed in its docstring
before the first run.

**Settings searched** (216 combinations per universe):

| Setting | Values |
|---|---|
| N, long names | 2, 3, 4 |
| Bar falling-EPS stocks from the long side | no / yes |
| Short filter | E1 (last year's EPS down), E2 (EPS lower than 26 weeks ago), E3 (both) |
| Short hold | 1, 3, 6 months (overlapping cohorts) |
| Short size | 50% or 100% of the book |
| A cohort with no falling-EPS stock | cash, or short SPY |

**How it was optimised:** choose the best Sharpe on 2008-2016 and judge it untouched on 2017-2026, then the reverse.
Both universes, with tech (eleven) and without (seven).

**One caution comes before the numbers.** The "E3 short" idea was spotted in the previous step (`EPP_SHORT.md`,
"Post-hoc") on data covering all years. The time split tests the settings, not that discovery, so it overstates how
clean the result is.

## 1. Optimised on one half, judged on the other

Annual return / Sharpe / worst drawdown, from monthly data.

| Universe | Chosen on | Setting chosen | On its training years | **On the other years (untouched)** | Rank there, of 216 | Median setting there |
|---|---|---|---|---|---|---|
| with tech | 2008-2016 | N=4, E3, 6m, 50%, empty=SPY | +17.4% / 1.42 / -16% | **+26.6% / 1.71 / -12%** | 13 | +21.8% / 1.32 / -17% |
| with tech | 2017-2026 | N=3, E3, 6m, 50%, empty=SPY | +32.5% / 1.85 / -12% | **+19.7% / 1.33 / -19%** | 2 | +8.3% / 0.60 / -21% |
| without tech | 2008-2016 | N=2, E3, 6m, 50%, empty=cash | +12.8% / 0.91 / -26% | **+21.1% / 1.06 / -19%** | 36 | +15.9% / 0.85 / -19% |
| without tech | 2017-2026 | N=4, bar falling-EPS, E3, 6m, 50%, empty=SPY | +17.3% / 1.26 / -13% | **+4.8% / 0.50 / -21%** | 46 | +1.7% / 0.20 / -20% |

- **The good settings stayed good across halves.** The rank correlation of all 216 settings' Sharpe between 2008-2016 and
  2017-2026 is **+0.88** with tech and **+0.72** without.
- **Both halves chose nearly the same thing:** an E3 short, held 6 months, at half size. The optimiser found a broad
  plateau, not a lucky spike.
- **Out of sample, the chosen setting beat the median setting in all four tests.** It held up well with tech; without
  tech, one direction fell to +4.8% a year.

## 2. Where the plateau is

Average Sharpe of every setting sharing a value, over the full period (with tech / without tech). Each value held the
same order in both halves, except the "empty" setting.

| Setting | Best value | Worst value |
|---|---|---|
| short filter | **E3, both measures: 1.12 / 0.69** | E1, last year only: 0.75 / 0.43 |
| short hold | **6 months: 1.04 / 0.63** | 1 month: 0.81 / 0.43 |
| short size | **50%: 1.19 / 0.74** | 100%: 0.69 / 0.33 |
| bar falling-EPS stocks from the long side | **no: 1.05 / 0.59** | yes: 0.83 / 0.48 |
| N, long names | 3: 1.00 / 0.55 (2: 0.94 / 0.58) | 4: 0.86 / 0.47 |
| empty cohort | SPY and cash about equal (0.95 / 0.93 with tech) | |

## 3. The in-sample pick, and how it compares

The pick is the best full-period Sharpe among the settings that ranked in the top quarter of **both** halves (33 such
settings with tech, 28 without). It is in-sample, and labelled so.

| | **With tech** | **Without tech** |
|---|---|---|
| Setting | N=3, long unfiltered, short E3, hold 6m, 50%, empty=SPY | N=3, long unfiltered, short E3, hold 6m, 50%, empty=cash |
| 2008-2016 | +19.7% / 1.33 / -19% | +10.0% / 0.85 / -15% |
| 2017-2026 | +32.5% / 1.85 / -12% | +20.8% / 1.24 / -15% |
| **Full period** | **+26.2% / 1.61 / -19%** | **+15.5% / 1.06 / -15%** |
| Beta to SPY | 0.30 | 0.39 |
| Positive calendar years | 18 of 19 (2015: -0.7%) | 17 of 19 (2015: -14.6%, 2018: -4.8%) |
| Each ticker left out | +20.1% (no AVGO) to +26.1% | +12.6% (no XOM) to +15.1% |
| *Long 3 lowest Ratio B, no short* | *+31.0% / 1.46 / -33%* | *+16.9% / 0.95 / -25%* |
| *Long 3 lowest minus 100% SPY* | *+17.1% / 1.09 / -27%* | *+4.0% / 0.32 / -38%* |
| *SPY* | *+11.2% / 0.69 / -51%* | *+11.2% / 0.69 / -51%* |

- **Against the unhedged long book, the short sleeve kept most of the return and cut the worst drawdown sharply.** With
  tech: -33% to -19%, for 5 points a year less return. Without tech: -25% to -15%, for 1.4 points less.
- **It was a far better hedge than shorting SPY.** Without tech, the long book minus 100% SPY made only +4.0% a year
  (worst drawdown -38%). Shorting half the book in falling-EPS stocks made +15.5% (-15%). The short sleeve lagged the
  market, which is what makes it a good hedge.
- These statistics are monthly. The daily figures in `RATIO_B_HEDGE.md` and `RATIO_B_NONTECH.md` run lower on Sharpe and
  deeper on drawdown for the same book: the unhedged long book is Sharpe 1.46 and -33% monthly, against 1.29 and -35%
  daily.

## 4. The newest book (October 2026)

| Universe | Long | Short |
|---|---|---|
| With tech | ACN, LOW, AVGO | NKE (E3: last year's EPS down and EPS lower than 26 weeks ago) |
| Without tech | LOW, SHW, UNP | NKE |

ACN is still the open disruption case. This is the rule applied to point-in-time data, not advice.

## What to check before believing it

1. **The E3 idea came from these same years.** A clean test needs tickers not yet built, with the setting above frozen
   first.
2. **The list is still survivors picked in 2026.** That inflates the long side, most of all with tech. The short side
   lacks the companies that kept falling.
3. **Few names:** three longs and about one or two shorts a month. 69% of months had a falling-EPS short with tech, 60%
   without.
4. **Costs and borrow fees.** The long side turns over about 465% a year (`RATIO_B_BASKET.md`), roughly 0.5 points a year
   at 0.10% a trade. Borrowing large caps on half the book costs a few tenths more.
5. **Monthly statistics:** daily drawdowns would be deeper.
