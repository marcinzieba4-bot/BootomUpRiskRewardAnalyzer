# MSFT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the MSFT weekly dates: 209 from 2008-01-04 to 2011-12-30. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: 91273a1; 2009-2011: 26d3d5b). Prices run to 2026-11-03; the 2008 batch's two-year horizons end by 2010-12-30
(three-year: 2011-12-30), the 2009-2011 batch's by 2013-12-30 (2014-12-30). Medians of an even count take the upper middle value
(`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

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

## 2009-2011 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 156 | +20% | -13% to +77% | 52 | 24 | +12% | 55 |
| legacy tier BUY | 156 | +20% | -13% to +77% | 52 | 24 | +12% | 55 |
| FY09E $2.05 anchor (2009-01-09 and 2009-01-16) | 2 | +52% | +49% to +52% | 2 | 1 | +38% | 2 |
| FY08's $1.87 after the withdrawal (2009-01-23 to 2009-07-17) | 26 | +38% | +6% to +77% | 15 | 2 | +34% | 15 |
| FY09's $1.62 (2009-07-24 to 2010-07-16) | 52 | +10% | -13% to +37% | 1 | 1 | -6% | 2 |
| FY10's $2.10 (2010-07-23 to 2011-07-15) | 52 | +20% | -1% to +57% | 15 | 15 | +14% | 17 |
| FY11's $2.69 (2011-07-22 to 2011-12-30) | 24 | +38% | +21% to +62% | 19 | 5 | +20% | 19 |
| 2009 | 52 | +15% | -13% to +77% | 17 | 3 | +10% | 17 |
| 2010 | 52 | +15% | -4% to +37% | 5 | 3 | +9% | 6 |
| 2011 | 52 | +36% | -1% to +62% | 30 | 18 | +16% | 32 |
| verdict UNDERVALUED | 137 | +24% | -1% to +77% | 52 | 24 | +14% | 55 |
| verdict MODESTLY UNDERVALUED | 12 | +3% | -13% to +12% | 0 | 0 | -5% | 0 |
| verdict FAIRLY VALUED | 7 | -10% | -12% to -4% | 0 | 0 | -14% | 0 |

- **CHEAP and BUY on every date; the call held on 55 of 156, in three stretches of low entries.** It held on 17 of the 18 dates from
  2009-01-09 to 2009-05-08 (entries $15.28-20.91, two-year returns +27% to +77%; SPY's rebound, +48% to +99%, beat MSFT on 15 of
  them), on 6 of the 12 from 2010-06-25 to 2010-09-10 (entries $23.27-25.81) and on 32 of the 37 from 2011-04-21 to 2011-12-30
  (entries $23.71-27.53, +21% to +62%; ahead of SPY on 18). It failed on all 58 dates from 2009-05-15 to 2010-06-18 (entries
  $19.75-31.00, two-year returns -13% to +30%, 5-38pp behind SPY) and all 31 from 2010-09-17 to 2011-04-15 (entries $24.38-28.60, -1%
  to +30%, 2-21pp behind). MSFT beat SPY on 24 of the 156 dates (SPY +10% to +99%, median +28%). One-year returns had a median of +9%
  (-15.7% to +90.5%); three-year returns ran from -6.7% to +118.5% (median +46.5%).
- **Within the class, the price measures ranked the outcomes; the signal composite did not.** Spearman across the 156 dates, against
  the two-year return, the return to the m12-24 average price and the three-year return: Ratio B -0.75, -0.87 and -0.80; the market
  composite -0.73, -0.84 and -0.76; the entry price -0.65, -0.81 and -0.54; the EPP gap -0.46, -0.68 and -0.39 (weaker than 2008's
  -0.95 on the m12-24 average, as the floor itself fell from 23x to 14x); the adjusted gap +0.23, +0.29 and +0.19; the proxy composite
  +0.02, -0.02 and -0.13. The proxy composite's highest reads did worst: 3.00 on the 12 dates of the Q2 FY10 print (lifted by the
  $1.71 billion recognition) returned a median +14% and 2.80 on the 13 of Q1 FY11 (against the deferral quarter) +3%, holding the call
  on none; the 1.80 of Q2 FY11 (against the recognition) returned +15%, and the 2.00 of Q2 FY09 (entries at $15-20) and of Q1 FY12
  (at 9-10x the anchor) returned +52% and +49%. Hypothesis for the method, as in 2008, not a rule: last-quarter operating signals
  read against distorted year-ago quarters carry little; a class that never changes carries nothing, and the information sat in
  where the price stood within the class. Test it on other tickers and years before any method change; never fit it to MSFT's
  outcomes.
- **The verdict flagged the worst stretch; the class did not.** The 19 dates the valuation verdict did not call UNDERVALUED (MODESTLY
  UNDERVALUED from 2009-09-18 to 2009-11-27 and on 2010-01-22, FAIRLY VALUED from 2009-12-04 to 2010-01-15), when the stock had risen
  to $25-31 and the floor had fallen to 19-23x, returned -13% to +12% (FAIRLY VALUED: -12% to -4%) and held on none; the 137
  UNDERVALUED dates returned a median +24% and held on 55. But 82 UNDERVALUED dates failed too, and the adjusted gap ranks the outcomes
  only weakly (+0.23). Hypothesis, not a rule: when the price reached the floor, the verdict, not the class, carried the warning. Test
  it elsewhere before reading anything into it.
- **The earnings came; the multiple did not.** The trailing anchor rose from FY09's $1.62 to FY11's $2.69 (the fact sheet's own
  figures, +29%/yr), but the price on 2011-12-30 ($25.96) was below its level on 2009-10-23 ($28.02): the P/E on the anchor fell from
  14-19x on the FY09 dates to 9-10x on the FY11 dates. Every two-year price ($23.71-38.71) landed nearest BEAR (99 dates) or BASE (57),
  never BULL: 1.49-3.01 times BEAR, 0.34-0.96 times BASE and 0.22-0.45 times BULL. No path went below BEAR (drawdowns of 18-27%),
  unlike 2008. BASE was nearest on 27 of the 40 dates where it was negative (the Q3 FY09, Q4 FY09 and Q1 FY10 reads, $30-57) and on
  30 with positive reads from 2010-02-19 to 2011-07-15; the two-year high ($31.39, on 2009-12-29 and again on 2010-04-22) reached BASE
  only on 16 of the negative-BASE dates. BASE and BULL take the window's median and 75th-percentile P/E (19-34x and 27-50x); the stock
  traded at 8-19x on its anchor throughout. Hypothesis, not a rule: as in 2008, a window whose multiples still carry 1999-2003 until
  2010 places BASE and BULL where the stock does not go; on these dates the forecast that failed was the multiple, not the earnings.
  The test belongs on other tickers' series, never on MSFT's own outcomes.
- **The encoding calls, seen afterwards.** None of the alternatives in retro/README.md ("MSFT 2009-2011") changes a 2009-2011 class
  or tier, so the outcomes say nothing about them. The deferrals swung BASE (-14.0% to -9.7%/yr on the 27 dates of the Q4 FY09 and Q1
  FY10 prints, +16.3%/yr on the 12 of Q2 FY10) and the proxy composite (1.85 against 3.00) without moving a class; those dates returned
  a median +3% and +14%. The withdrawn guide left FY08's $1.87 as the anchor on 26 dates that returned +6% to +77%, CHEAP either way.
  The outcomes must not decide the CLOUD registry question either: that Microsoft later grew a cloud business (the 2026 profile reads
  "Azure + M365 + OpenAI", DURABLE, risk 1) is hindsight; the question stays a point-in-time one about the FY2010 10-K's risk factor
  and the registry's basis, for the owner. The calls were decided before scoring and stay; changing a rule means a new method version
  tested elsewhere.
