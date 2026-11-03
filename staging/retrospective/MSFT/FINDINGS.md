# MSFT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the MSFT weekly dates: 53 from 2008-01-04 to 2008-12-31. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: 91273a1). Prices run to 2026-11-03; the 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30).
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 53 | +3% | -10% to +54% | 7 | 41 | -0% | 44 |
| legacy tier BUY | 53 | +3% | -10% to +54% | 7 | 41 | -0% | 44 |
| FY08E $1.795 anchor (to the Q2 FY08 print) | 3 | -7% | -8% to -4% | 0 | 3 | -32% | 3 |
| FY08E $1.865 anchor (2008-01-25 to 2008-07-11) | 25 | +0% | -8% to +11% | 0 | 25 | -10% | 25 |
| FY09E $2.15 anchor (2008-07-18 to 2008-10-17) | 14 | -1% | -10% to +19% | 0 | 9 | +5% | 9 |
| FY09E $2.05 anchor (from the Q1 FY09 print) | 11 | +36% | +20% to +54% | 7 | 4 | +37% | 7 |
| January-September | 39 | -1% | -10% to +11% | 0 | 37 | -8% | 37 |
| October-December | 14 | +36% | -3% to +54% | 7 | 4 | +37% | 7 |

- **CHEAP and BUY on every date; the call held on 44 of 53, mostly by beating a falling market.** On the 39 dates from January to
  September SPY returned -19% to -1% over two years and MSFT beat it on 37, by up to 23pp, while its own two-year return was -10% to
  +11% and none cleared the hurdle; the two misses are 2008-09-12 (-9.9%, 1.9pp behind SPY) and 2008-09-26 (-5.8%, 4.5pp behind).
  From October MSFT returned -3% to +54% (median +36%), but SPY returned +8% to +57% over the same windows: the call held on the 7
  dates that cleared the hurdle (2008-11-14, 2008-11-21 and 2008-12-05 to 2008-12-31, +36% to +54%), and failed on the other 7, which
  lagged SPY's rebound by 3-21pp. One-year returns had a median of -13% (-46% to +65%); three-year returns ran from -14% to +45%
  (median -0%).
- **The entry price and the floor distance ranked the endpoint-robust outcome almost perfectly; the signal composite did not.** Across
  the 53 dates the EPP gap ranks the return to the m12-24 average price at Spearman -0.95, the entry price at -0.95 and Ratio B at
  -0.94 (the two-year endpoint: -0.55, -0.59, -0.56); the adjusted gap barely ranks either (-0.07 on the m12-24 average, -0.15 on
  the two-year endpoint). The proxy composite ranks
  the two-year returns at -0.01 and the m12-24 average at -0.38: it read 2.45 on the three Q1 FY08 dates (median two-year return -7%),
  3.15 on the 13 of the Q2 FY08 print (+6%), 1.90 on the 12 of Q3 FY08 (-1%), 3.05 on the 14 of Q4 FY08 (-1%) and 2.15 on the 11 of
  Q1 FY09 (+36%). The Q2 and Q4 FY08 reads, lifted by year-ago quarters with the technology-guarantee deferral and the Xbox 360
  charge, did no better than the Q3 FY08 read, depressed by the year-ago recognition and the fine. Hypothesis for the method, not a
  rule: last-quarter operating signals, read against distorted year-ago quarters, carry little about the next two years (the NKE,
  AAPL and PEP 2008 batches found them lagging the price). Test it on other tickers and years before any method change; never fit it
  to MSFT's outcomes. One stock through one crash mostly tests "buy lower".
- **Every two-year price landed nearest BEAR, and every path but one went below it.** The two-year price ($23-31) was 1.36-1.94
  times the BEAR price, 0.25-0.44 times BASE and 0.17-0.24 times BULL. Every date's two-year window included the 2009-03-09 close
  ($15.15), below its BEAR price ($15-18) on 52 of 53 dates (not 2008-12-31's $15): drawdowns of 27-56%.
- **The bubble years set a band the stock never came back to.** BASE ($69-107, at the window's 35-37x median) and the EPP floor
  ($53-65, at 26-30x, the median of calendar-year lows set by 1998-2003 multiples) sat far above every price the stock reached in
  the two years after each date ($15-35, 7-19x the EPS anchor; the highest was 64% of the floor and 47% of BASE). The call held where
  the market fell further, not because the stock re-rated toward the band. Hypothesis, not a rule: a ten-year P/E window that spans a bubble, together with a restatement seam in
  the EPS history, places BASE, BULL and the floor where the stock does not return, and keeps every date CHEAP. The test belongs on
  other tickers whose 2008 windows reach back into 1998-2001, never on MSFT's own outcomes.
- **The encoding calls, seen afterwards.** None of the alternatives in retro/README.md ("MSFT") changes a 2008 class or tier, so the
  outcomes say nothing about them. The technology-guarantee deferral swung BASE between +27.3%/yr (to 2008-01-18) and +1.3%/yr (from
  2008-01-25) without moving a class; the three January dates returned -8% to -4% over two years and the 13 of the Q2 FY08 print -8%
  to +11%. The calls were decided before scoring and stay; changing a rule means a new method version tested elsewhere.
