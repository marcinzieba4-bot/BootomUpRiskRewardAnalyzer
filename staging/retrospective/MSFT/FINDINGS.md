# MSFT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the MSFT weekly dates: 983 from 2008-01-04 to 2026-10-30. They are **labels and hypotheses**: never
feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and pushed
(2008: 91273a1; 2009-2011: 26d3d5b; 2012-2014: 6bf73dc; 2015-2017: d81c719; 2018-2020: 567b23c; 2021-2023: 63b6804; 2024-2026:
3827093). The 2008-2011 outcomes were computed on 2026-11-03 and the 2012-2026 ones on 2026-11-04; the eleven dates of 2011 rebuilt for
the Q1 FY12 currency correction (retro/README.md, "MSFT 2012-2014") were re-scored on 2026-11-04 with unchanged values, and every
2009-2011 figure below still holds. The 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30), the 2009-2011
batch's by 2013-12-30 (2014-12-30), the 2012-2014 batch's by 2016-12-30 (2017-12-29), the 2015-2017 batch's by 2019-12-27 (2020-12-29),
the 2018-2020 batch's by 2022-12-30 (2023-12-29), the 2021-2023 batch's by 2025-12-29 (three-year: 2026-11-03; the eight dates from
2023-11-10 have none yet); prices end on 2026-11-03, so of the 2024-2026 batch only the 44 dates to 2024-11-01 have two years. Medians
of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

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

## 2012-2014 (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 109 | +51% | +21% to +94% | 93 | 81 | +29% | 95 |
| class FAIR | 35 | +38% | +23% to +52% | 27 | 35 | +17% | 3 |
| class RICH | 13 | +31% | +21% to +37% | 5 | 13 | +22% | 0 |
| legacy tier BUY | 106 | +51% | +21% to +94% | 91 | 78 | +28% | 86 |
| legacy tier ACCUMULATE | 37 | +38% | +28% to +52% | 33 | 37 | +22% | 9 |
| legacy tier WATCHLIST | 14 | +29% | +21% to +34% | 1 | 14 | +15% | 3 |
| FY11's $2.69 (2012-01-06 to 2012-07-13) | 28 | +32% | +21% to +51% | 14 | 0 | +14% | 14 |
| FY12's $2.00, after the impairment (2012-07-20 to 2013-07-12) | 52 | +58% | +32% to +94% | 51 | 52 | +41% | 52 |
| FY13's $2.58 (2013-07-19 to 2014-07-18) | 53 | +44% | +21% to +57% | 44 | 53 | +26% | 29 |
| FY14's $2.63 (2014-07-24 to 2014-12-31) | 24 | +34% | +23% to +40% | 16 | 24 | +15% | 3 |
| 2012 | 52 | +48% | +21% to +94% | 38 | 24 | +24% | 38 |
| 2013 | 52 | +52% | +31% to +84% | 50 | 52 | +36% | 52 |
| 2014 | 53 | +36% | +21% to +57% | 37 | 53 | +21% | 8 |
| verdict UNDERVALUED | 68 | +44% | +21% to +58% | 52 | 40 | +26% | 54 |
| verdict MODESTLY UNDERVALUED | 28 | +59% | +40% to +94% | 28 | 28 | +55% | 22 |
| verdict FAIRLY VALUED | 38 | +48% | +25% to +84% | 33 | 38 | +25% | 21 |
| verdict MODESTLY OVERVALUED | 10 | +33% | +23% to +40% | 7 | 10 | +15% | 1 |
| verdict OVERVALUED | 13 | +31% | +21% to +37% | 5 | 13 | +22% | 0 |

- **CHEAP held on 95 of 109 dates; FAIR on 3 of 35 and RICH on none of 13.** The CHEAP call held on all 91 dates from 2012-05-04 to
  2014-01-24 (entries $26.46-38.36, two-year returns +31% to +94%, ahead of SPY on 80) and on 2014-02-07. It failed on 14 of the 17
  dates from 2012-01-06 to 2012-04-27 (entries $28.25-32.60, the stock 13-25% below the floor that FY11's $2.69 set): MSFT returned
  +21% to +31% over two years while SPY returned +34% to +46%. From 2014-01-31 the class turned FAIR (35 dates) and RICH (13, from
  2014-04-25 to 2014-07-18), and MSFT beat SPY on all 48 by 12-39pp (+21% to +52% against SPY's +6% to +18%): FAIR held only where
  MSFT stayed within 15pp of SPY (2014-09-12, 2014-09-19, 2014-11-14), and RICH, which needs a miss of both the hurdle and SPY, held
  on none. MSFT beat SPY on 129 of the 157 dates (SPY +6% to +56%, median +32%). One-year returns had a median of +19% (-11.3% to
  +51.0%); three-year returns ran from +36.5% to +123.8% (median +77.5%).
- **The class followed the multiple up, and the multiple kept rising.** The FAIR and RICH dates traded at 14.6-18.9x the anchor
  (FY13's $2.58, then FY14's $2.63), the 47th-78th percentile of a ten-year range whose median had fallen to 14.7-14.9x and whose
  75th percentile to 18.0-19.8x as 2002-2004 left it; the price sat 46-89% above the floor (10x, the median of the calendar-year
  lows since 2004). The anchor barely moved ($2.58 to $2.63), so the class changed on the price alone. Every two-year price on those
  48 dates landed at 0.92-1.35 times BASE (BASE nearest on 46, BULL on 2). Hypothesis, not a rule: the mirror image of 2008-2011,
  when a window that spanned the bubble kept every date CHEAP; here a window made of the de-rated 2005-2013 years set the median and
  75th percentile low, and a franchise re-rating out of that range read FAIR and then RICH early. The test belongs on other tickers'
  re-rating phases, never on MSFT's own outcomes.
- **Only the entry price ranked the outcomes.** Spearman across the 157 dates, against the two-year return, the return to the m12-24
  average price and the three-year return: the entry price -0.60, -0.57 and -0.13; the EPP gap -0.31, -0.23 and +0.19; Ratio B
  -0.24, -0.17 and +0.09; the market composite -0.13, -0.04 and +0.28; the adjusted gap +0.10, +0.08 and -0.32; the proxy composite
  +0.25, +0.26 and -0.15 (2009-2011: Ratio B -0.75, -0.87 and -0.80). Within the 109 CHEAP dates the price measures ranked with the
  opposite sign (Ratio B +0.37 and the adjusted gap -0.64 on the two-year return; the entry price still -0.47): the 28 dates on FY11's
  $2.69, whose BULL was the FY02-FY11 CAGR (+21.1%/yr), had the lowest Ratio B (0.11-0.20) and the weakest returns (median +32%), and
  the 52 on FY12's GAAP $2.00, whose lower anchor cut every scenario price, had a higher Ratio B (0.49-0.93) and the strongest (+58%,
  the call held on all). Hypothesis, not a rule: a level change in the EPS anchor moves Ratio B with no change in the price, so across
  an anchor seam Ratio B ranks the encoding rather than the entry. Test it on other tickers' impairment years before reading anything
  into it; never fit it to MSFT's outcomes.
- **The verdict did not warn; it pointed the wrong way.** The 23 OVERVALUED and MODESTLY OVERVALUED dates (2014-04-25 to 2014-07-18,
  2014-10-31 to 2014-12-31) returned +21% to +40% and beat SPY on every one by 12-27pp; MODESTLY UNDERVALUED (28 dates, mostly on
  FY12's $2.00) did best (+41% to +94%, median +59%). In 2009-2011 the 19 dates the verdict did not call UNDERVALUED all failed, with
  the stock at its floor; in 2014 the stock sat far above a 10x floor and kept rising. Hypothesis: the verdict's warning carries where
  the price meets the floor, not where the floor has fallen away below it. Test it elsewhere.
- **BASE was the landing; BEAR came only from the FY11 anchor.** BASE was nearest the two-year price on 128 dates, BULL on 18 (16 entries
  from 2012-09-21 to 2013-01-25, and 2014-07-11 and 2014-07-18) and BEAR on 11 (2012-01-06 to 2012-03-16, where BEAR was $20 on FY11's
  $2.69). The two-year price ($35-64) was 1.75-4.13 times BEAR, 0.59-1.71 times BASE and 0.35-0.89 times BULL. No path went below
  BEAR (drawdowns of 14-20%); the two-year high reached BASE on 100 dates and BULL on none. From 2012-07-20, when the impairment
  year set BEAR at -24.2%/yr, the lowest two-year low was 1.95 times the BEAR price (1.32 on all dates): hindsight about
  one stock's path, and no reason to treat the year differently.
- **The encoding calls, seen afterwards.** The deferral reading is the one call that moves classes (retro/README.md, "MSFT
  2012-2014"): with the company's non-GAAP figures in both the BASE reads and the prints, 38 dates would change class (24 CHEAP to
  FAIR, 12 RICH to FAIR, 2 FAIR to CHEAP). On those dates the built classes held on 24 and the alternative's would have held on 12;
  that is hindsight on one stock, and neither confirms nor refutes a rule decided in 2008. GAAP FY12 against the company's $2.78 moved
  only tiers (ACCUMULATE or WATCHLIST to the next tier up on 23 dates that returned +21% to +52%). CLOUD changed only text, and the
  outcomes must not decide the registry question: that Microsoft's cloud business later grew is hindsight; the question stays a
  point-in-time one about its FY2010 10-K and the registry's basis, for the owner. The calls were decided before scoring and stay;
  changing a rule means a new method version tested elsewhere.

## 2015-2017 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR | 8 | +64% | +39% to +70% | 8 | 8 | +39% | 0 |
| class RICH | 148 | +83% | +47% to +108% | 148 | 148 | +55% | 0 |
| legacy tier ACCUMULATE | 3 | +39% | +39% to +42% | 3 | 3 | +18% | 0 |
| legacy tier WATCHLIST | 8 | +64% | +57% to +70% | 8 | 8 | +40% | 0 |
| legacy tier AVOID | 145 | +83% | +47% to +108% | 145 | 145 | +56% | 0 |
| FY14's $2.63 (2015-01-09 to 2015-07-17) | 28 | +58% | +39% to +70% | 28 | 28 | +33% | 0 |
| FY15's $2.63, as adjusted (2015-07-23 to 2016-07-15) | 52 | +76% | +50% to +108% | 52 | 52 | +46% | 0 |
| FY16's GAAP $2.10, after the Windows 10 deferrals (2016-07-21 to 2017-07-14) | 52 | +91% | +61% to +105% | 52 | 52 | +61% | 0 |
| FY17's GAAP $2.71 (2017-07-21 to 2017-07-28) | 2 | +98% | +90% to +98% | 2 | 2 | +58% | 0 |
| FY17's $3.25, the recast (2017-08-04 to 2017-12-29) | 22 | +87% | +72% to +95% | 22 | 22 | +56% | 0 |
| 2015 | 52 | +62% | +39% to +81% | 52 | 52 | +34% | 0 |
| 2016 | 52 | +92% | +61% to +108% | 52 | 52 | +61% | 0 |
| 2017 | 52 | +87% | +67% to +102% | 52 | 52 | +59% | 0 |
| verdict MODESTLY OVERVALUED | 9 | +64% | +39% to +70% | 9 | 9 | +39% | 0 |
| verdict OVERVALUED | 147 | +83% | +47% to +108% | 147 | 147 | +55% | 0 |

- **No call held: RICH on none of 148 dates, FAIR on none of 8.** MSFT returned +39% to +108% over two years, cleared the hurdle and
  beat SPY on every date, by 20-75pp (SPY +11% to +53%, median +25%): RICH needs a miss of both, FAIR a landing within 15pp of SPY,
  and neither came close. The weakest two-year return was the first date's (+38.6% from 2015-01-09), the strongest 2016-06-24's
  (+107.9%). One-year returns had a median of +34% (+5.2% to +55.8%); three-year returns ran from +77.7% to +214.9% (median +151.9%).
  Drawdowns within two years were 10.5-18.6%; no path went below BEAR, and the two-year high reached BASE on every date and BULL on 153.
- **The two-year price landed at XBULL on 130 dates,** BULL on 23 (from 2015-01-28 to 2015-07-10) and BASE on the three dates of
  January 2015; it was 3.92-10.68 times BEAR, 0.99-4.08 times BASE, 0.80-3.02 times BULL and 0.69-1.53 times XBULL. The scenario
  range, built from the window's P/E percentiles and the history's growth, sat below the path from mid-2015 on.
- **RICH came from the band, and the band's richest reading did best.** The class rests on the P/E against a ten-year range whose
  median was 14.7x on every date: 15.3-21.3x on $2.63 to 2016-07-15, 26.6-34.7x (the 99th-100th percentile) on FY16's GAAP $2.10 and
  22.3-26.7x on the recast $3.25. The dates on GAAP $2.10, the most extreme P/Es of the range, returned the most (median +91%, the
  price 1.55-1.99 times the entry two years on). Hypothesis, not a rule: once an own-history band's median comes from a franchise's
  de-rated years (2005-2013 here; the 2012-2014 mirror image of 2008-2011), the band reads a re-rating as RICH from its first months,
  and a deferral that depresses GAAP EPS pushes the reading to the top of the band (the company's figures give 20-26x on FY16: still
  RICH, retro/README.md, "MSFT 2015-2017"). The test belongs on other tickers' re-rating phases, never on MSFT's own outcomes.
- **What ranked the outcomes was the calendar.** Spearman across the 156 dates, against the two-year return, the return to the m12-24
  average price and the three-year return: Ratio B +0.64, +0.50 and +0.28 (the 73 finite values); the market composite +0.49, +0.61
  and +0.49; the entry price +0.47, +0.50 and +0.58; the EPP gap +0.48, +0.61 and +0.47; the adjusted gap -0.34, -0.53 and -0.12; the
  proxy composite +0.41, +0.42 and +0.58. The entry date itself ranks +0.63 against the two-year return and +0.73 against the
  three-year: every series that rose with the price over 2015-2017 ranks "right" by riding the trend. Within the two long anchor
  periods the signs turn or split: the entry price -0.28 (FY15's $2.63) and -0.23 (FY16's $2.10) against the two-year return, cheaper entries
  doing better as in 2012-2014, and the proxy composite -0.40 and +0.25. Hypothesis: across a sustained re-rating a level shift in any
  series lines up with the returns; read a rank correlation within an anchor period, not across one.
- **The signals that turned were the business ones, read twice by one accounting effect.** The proxy composite rose from 1.95-2.15 on
  the 2015 prints to 2.35-2.70 on Q2 FY17 to Q1 FY18: unearned revenue at BULL from Q2 FY16 (+17.8% to +38.5%) and the gross margin at
  BULL from Q3 FY17 (BASE or BEAR on every earlier print of the range), while reported revenue stayed at BEAR from Q3 FY15 to Q3 FY17
  under the deferrals and the strong dollar. The deferral itself moves unearned revenue up and revenue down, so the two signals partly read the same entry;
  that the business strengthened is hindsight about one stock, and the weights stay as frozen.
- **The encoding calls, seen afterwards.** No call moves more than two classes in 2015-2017 (retro/README.md, "MSFT 2015-2017"): the
  two that reported growth would move (2015-03-13 and 2015-04-17, FAIR to RICH) returned +63% and +64%, 43-47pp ahead of SPY, so they
  fail either way. The company's non-GAAP FY16 and FY17 lower the anchor's P/E by a quarter and leave every date RICH: the deferral
  reading did not decide these outcomes. CLOUD changed only text; that Microsoft's own cloud business grew through the range is
  hindsight and must not decide the registry question (the theme's market-pricing date and whether it applies to Microsoft stay
  point-in-time questions, for the owner). The calls were decided before scoring and stay; changing a rule means a new method version
  tested elsewhere.

## 2018-2020 (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 157 | +95% | +1% to +137% | 133 | 154 | +64% | 3 |
| legacy tier AVOID | 157 | +95% | +1% to +137% | 133 | 154 | +64% | 3 |
| FY17's $3.25, the recast (2018-01-05 to 2018-07-13) | 28 | +90% | +47% to +113% | 28 | 28 | +54% | 0 |
| FY18's $3.88, as adjusted (2018-07-20 to 2019-07-12) | 52 | +104% | +81% to +137% | 52 | 52 | +71% | 0 |
| FY19's $4.75, as adjusted (2019-07-19 to 2020-07-17) | 53 | +106% | +27% to +134% | 49 | 53 | +73% | 0 |
| FY20's GAAP $5.76 (2020-07-24 to 2020-12-31) | 24 | +17% | +1% to +42% | 4 | 21 | +34% | 3 |
| 2018 | 52 | +94% | +47% to +131% | 52 | 52 | +55% | 0 |
| 2019 | 52 | +114% | +94% to +137% | 52 | 52 | +76% | 0 |
| 2020 | 53 | +37% | +1% to +122% | 29 | 50 | +47% | 3 |
| verdict OVERVALUED | 157 | +95% | +1% to +137% | 133 | 154 | +64% | 3 |

- **RICH held on 3 of 157 dates, all in late 2020.** MSFT returned +1% to +137% over two years (median +95%), cleared the hurdle on
  133 dates and beat SPY on 154 (SPY -9% to +99%, median +35%). The call held only on 2020-10-16, 2020-10-29 and 2020-11-06 (entries
  $204.72-223.72, 35.5-38.8x FY20's $5.76), whose two-year windows end in the 2022 decline: +1.1% to +17.5%, 0.2-9.8pp behind SPY. The
  strongest two-year return was 2019-02-01's (+137.0%), the weakest 2020-11-06's (+1.1%). One-year returns had a median of +40% (+13.9%
  to +75.8%); three-year returns ran from +44.7% to +246.2% (median +105.6%). Drawdowns within two years were 18.3-37.6%; no path went
  below BEAR, and the two-year high passed BULL on every date. Across 2015-2020 the RICH reading held on 3 of the 305 dates that carried
  it.
- **The two-year price landed at XBULL on every date** (0.96-1.96 times XBULL; 1.31-2.67 times BULL, 1.64-3.29 times BASE). XBULL is
  the best two-year EPS run of the history at the 90th-percentile P/E; the path ran above it on most dates. At the COVID-19 low
  (2020-03-20, $137.35, 28.9x, the 94th percentile) the two-year return was +122%.
- **The band never caught up.** The window's median rose from 14.7x to 18.3x while the stock traded at 25-45x, the 94th-100th percentile
  on every date, and the EPS anchor moved from FY17's $3.29 to FY20's $5.76 (+20.5%/yr). Hypothesis, not a rule: a
  ten-year own-history band lags a franchise whose earnings compound at about 20% a year by most of a decade, so it reads RICH for as
  long as the compounding lasts, and the reading held only when the market itself fell (2022). The test belongs on other compounders'
  long re-ratings, never on MSFT's own outcomes.
- **Within an anchor period the price ranked the right way; across the range the calendar ranked the other way.** Spearman across the
  157 dates, against the two-year return, the return to the m12-24 average price and the three-year return: the entry price -0.46, -0.25
  and -0.85; the EPP gap -0.42, -0.63 and +0.28; the market composite -0.20, -0.25 and +0.04; the adjusted gap +0.22, +0.46 and +0.04; the
  proxy composite +0.16, +0.41 and +0.02 (Ratio B -0.71, -0.46, -0.71 on its 7 finite values). The entry date ranks -0.40 against the
  two-year return and -0.80 against the three-year, the mirror of 2015-2017 (+0.63, +0.73): late-2020 entries met 2022. Within the
  anchor periods the entry price and the P/E rank -0.37 (FY18's $3.88), -0.85 (FY19's $4.75) and -0.67 (FY20's $5.76) against the
  two-year return, and +0.35 on the 28 dates of FY17's $3.25: the higher the multiple within a period, the lower the return, as in
  2012-2017. Hypothesis: the valuation inputs rank entries within an anchor period while the class misreads the level; keep testing the
  split on other tickers.
- **The encoding calls, seen afterwards.** No call moves a class or a tier in 2018-2020 (retro/README.md, "MSFT 2018-2020"): GAAP FY18
  would have put the anchor at 46-65x instead of 25-36x on dates that returned +81% to +137%, and reported growth or GAAP FY19 change
  only the scenario numbers. CLOUD changed only text; that Microsoft's own cloud kept growing is hindsight and stays out of the registry
  question. The calls were decided before scoring and stay; changing a rule means a new method version tested elsewhere.

## 2021-2023 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 142 | +39% | +3% to +84% | 83 | 120 | +24% | 11 |
| class FAIR | 14 | +85% | +74% to +93% | 14 | 14 | +76% | 0 |
| legacy tier AVOID | 132 | +36% | +3% to +83% | 73 | 110 | +23% | 11 |
| legacy tier WATCHLIST | 19 | +77% | +54% to +87% | 19 | 19 | +70% | 0 |
| legacy tier ACCUMULATE | 5 | +87% | +86% to +93% | 5 | 5 | +81% | 0 |
| FY20's GAAP $5.76 (2021-01-08 to 2021-07-23) | 29 | +21% | +5% to +36% | 3 | 26 | +5% | 3 |
| FY21's $7.97, as adjusted (2021-07-29 to 2022-07-22) | 52 | +36% | +3% to +83% | 27 | 52 | +8% | 0 |
| FY22's $9.21, as adjusted (2022-07-28 to 2023-07-21) | 52 | +56% | +26% to +93% | 49 | 44 | +61% | 3 |
| FY23's $9.81, as adjusted (2023-07-27 to 2023-12-29) | 23 | +57% | +27% to +65% | 18 | 12 | +32% | 5 |
| 2021 | 52 | +13% | +3% to +36% | 3 | 49 | -2% | 3 |
| 2022 | 52 | +60% | +19% to +91% | 50 | 52 | +42% | 0 |
| 2023 | 52 | +49% | +26% to +93% | 44 | 33 | +35% | 8 |
| verdict OVERVALUED | 142 | +39% | +3% to +84% | 83 | 120 | +24% | 11 |
| verdict MODESTLY OVERVALUED | 12 | +85% | +74% to +91% | 12 | 12 | +75% | 0 |
| verdict FAIRLY VALUED | 2 | +93% | +87% to +93% | 2 | 2 | +87% | 0 |

- **RICH held on 11 of 142 dates; the 14 FAIR dates were the range's best entries.** MSFT returned +3% to +93% over two years (median
  +42%), cleared the hurdle on 97 dates and beat SPY on 134 (SPY -8% to +68%, median +36%). The RICH call held on 2021-01-08,
  2021-01-28 and 2021-02-05 (two-year windows ending in early 2023: +5% to +9%, 0.3-4.7pp behind SPY), on 2023-04-06, 2023-04-21 and
  2023-04-27 (+26% to +31%, 0.3-6.4pp behind) and on five dates from 2023-11-24 ($371-377 entries; +27% to +32%, 16-23pp behind SPY).
  The FAIR dates of 2022-09-23 to 2023-01-20 (entries $221-245, 24.0-26.6x FY22's $9.21, the 63rd-73rd percentile of its own range)
  returned +74% to +93% and beat SPY by 16-36pp, so the FAIR expectation (within 15pp of the benchmark) held on none: they missed on
  the upside. The weakest two-year return was 2021-10-28's (+3.3%, its window ending a year after the 2022 low), the strongest
  2023-01-06's (+92.8%). One-year returns had a median of +25% (-33% to +67%); three-year returns on 148 dates ran from +12% to +138%
  (median +61%). Drawdowns within two years were 15.5-37.6%; no path went below BEAR, and the two-year high passed BULL on every date.
- **The two-year price landed at XBULL on 132 dates and at BULL on 24** (0.74-1.18 times XBULL; 1.08-1.83 times BULL, 1.43-2.29 times
  BASE). The BULL landings are the entries whose two-year windows ended in a pullback: August-October 2021 (ending in the second half
  of 2023), August-November 2022 (the second half of 2024) and February-April 2023 (the spring of 2025).
- **The tiers ranked the entries in order, and so did the valuation inputs.** ACCUMULATE (5 dates) returned a median +87%, WATCHLIST (19)
  +77%, AVOID (132) +36%; FAIRLY VALUED +93%, MODESTLY OVERVALUED +85%, OVERVALUED +39%. Spearman across the 156 dates, against the
  two-year return, the return to the m12-24 average price and the three-year return (148 dates): the P/E -0.83, -0.91 and -0.44; the EPP
  gap -0.83, -0.93 and -0.32; the market composite -0.88, -0.93 and -0.51; the adjusted gap +0.76, +0.70 and +0.62; Ratio B -0.69, -0.93
  and -0.76 on its 90 finite values; the proxy composite -0.47, -0.62 and -0.25; the entry price -0.23, -0.37 and -0.82; the entry date
  +0.62, +0.62 and -0.09. Within the anchor periods the entry price ranks -0.79 (FY21's $7.97), -0.86 (FY22's $9.21) and -0.93 (FY23's
  $9.81) against the two-year return, and +0.51 on the 29 dates of FY20's $5.76 (-0.99 against the m12-24 average). In 2018-2020 the
  calendar overrode the valuation inputs across the range; here the 2022 drawdown put the lowest multiples and the best returns on the
  same dates.
- **The band caught up only at the low.** The window's median rose from 18.3x to 23.8x and the anchor from FY20's $5.76 to FY23's $9.81
  (+19.4%/yr), so the stock sat at the 97th-100th percentile through 2021 (86th-100th in the first half of 2022) and came down to the
  63rd-73rd only at the late-2022 low, where the class read FAIR, not CHEAP. Hypothesis, not a rule: when a compounder's multiple falls
  back toward its own ten-year band, the band's ranking turns useful even though its level still understates the outcome (FAIR entries
  beat SPY by 16-36pp). Test it on other compounders' drawdowns, never on MSFT's own outcomes.
- **The encoding calls, seen afterwards.** At GAAP ($8.05, $9.65, $9.68) instead of the company's figures, 7 classes would move
  (retro/README.md, "MSFT 2021-2023"): RICH to FAIR on 2022-09-16, 2022-11-11, 2022-11-25 and 2022-12-09 (+72% to +84%, 18-30pp ahead of
  SPY: still FAIR misses) and FAIR to CHEAP on 2022-10-27, 2022-11-04 and 2023-01-06 (+87% to +93%: CHEAP would have held). Reported
  growth instead of constant currency would turn four FAIR dates of September-October 2022 RICH (+75% to +87%: RICH misses). The 8-K of
  2022-06-02, the Q2 FY23 operating income and GENAI move no class; GENAI's 22 dates (from 2023-08-04, text only) returned +27% to +65%
  and beat SPY on 11. Whether generative AI proved a threat to Microsoft or a franchise for it is hindsight and stays out of the registry
  question. The calls were decided before scoring and stay; changing a rule means a new method version tested elsewhere.

## 2024-2026 (148 dates)

Prices end on 2026-11-03, so only the 44 dates to 2024-11-01 have two years, the 96 to 2025-10-31 one year and the 122 to 2026-05-01
six months; the 26 dates from 2026-05-08 have no outcome yet. Every date with two years is a 2024 date, RICH and AVOID. The 33 CHEAP
dates (from 2026-02-06) have at most six months.

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 44 | +6% | -15% to +30% | 0 | 0 | +10% | 44 |
| legacy tier AVOID | 44 | +6% | -15% to +30% | 0 | 0 | +10% | 44 |
| FY23's $9.81 (2024-01-05 to 2024-07-26) | 30 | -0% | -15% to +30% | 0 | 0 | +12% | 30 |
| FY24's GAAP $11.80 (2024-08-01 to 2024-11-01) | 14 | +25% | +13% to +30% | 0 | 0 | +7% | 14 |

| Group (one year) | Dates | Median 1-yr total return | Range | Cleared 15% hurdle | Beat SPY | Median price change to 2026-10-30 |
|---|---|---|---|---|---|---|
| class RICH | 94 | +4% | -25% to +29% | 21 | 20 | +23% |
| class FAIR | 2 | +16% | +5% to +16% | 1 | 0 | +45% |
| legacy tier AVOID | 87 | +5% | -25% to +29% | 21 | 20 | +22% |
| legacy tier WATCHLIST | 7 | -0% | -5% to +9% | 0 | 0 | +33% |
| legacy tier ACCUMULATE | 2 | +16% | +5% to +16% | 1 | 0 | +45% |
| FY23's $9.81 (2024-01-05 to 2024-07-26) | 30 | +7% | -15% to +22% | 3 | 2 | +25% |
| FY24's GAAP $11.80 (2024-08-01 to 2025-07-25) | 52 | +8% | -25% to +29% | 19 | 18 | +25% |
| FY25's GAAP $13.64, dates with a year (2025-08-01 to 2025-10-31) | 14 | +1% | -11% to +5% | 0 | 0 | +2% |
| 2024 | 52 | +12% | -15% to +29% | 20 | 20 | +25% |
| 2025, dates with a year | 44 | -1% | -25% to +16% | 2 | 0 | +13% |

- **RICH held on all 44 two-year dates.** The 2024 entries ($367.75-453.55, 30-48x the anchor) returned -15.0% (2024-06-28) to +30.3%
  (2024-01-05) over two years, median +6.1%, while SPY returned +24.0% to +50.0% (median +39.1%): none cleared the hurdle and each lagged
  SPY, by 4.9pp to 54.0pp, so RICH held on every one. The two-year price landed at BULL on 39 dates, XBULL on 3 and BASE on 2 (1.10-1.59
  times the BASE price); drawdowns within two years were 24.2% to 34.9%, the windows bottoming at the 2025-04-08 close ($354.56, 25
  dates) or the 2026-06-25 close ($352.83, 19). It is the first full year of RICH calls that held: from 2014 to 2023 RICH held on 14 of
  the 460 dates that carried it (none before late 2020). The entries sat at the 98th-100th percentile of the stock's own range on FY23's
  $9.81, and two declines (April 2025, 30x FY24's $11.80; June 2026, 26x FY25's $13.64) brought the multiple back toward the band's
  median (24-28x).
- **Over one year the order was weak; over six months the 2026 CHEAP dates led.** The 96 one-year dates returned a median +4.8% (-25.0%
  to +29.4%); 20 beat SPY (2024-07-19 to 2024-11-29, windows ending in the 2025 rally), the two FAIR dates of April 2025 returned +4.8%
  and +15.9% but lagged SPY by 20-27pp. Over six months (122 dates) RICH returned a median +0.8% (beating SPY on 26 of 104), FAIR +24.0%
  (4 of 7) and the 11 CHEAP dates with six months (2026-02-06 to 2026-05-01) +21.6% to +45.2% (median +26.4%), each ahead of SPY by 7.5pp
  to 29.6pp. To 2026-10-30 the price rose a median +30.0% from the 32 earlier CHEAP dates, +21.3% from the FAIR and +21.7% from the RICH
  ones. Six months is not a call check; the CHEAP calls are scored only in 2028.
- **The multiple and the floor distance ranked the two-year returns; the composites less so.** Spearman over the 44 two-year dates: the
  P/E -0.92, the EPP gap -0.92, the entry price -0.57, Ratio B -0.56 (16 finite values), the market composite -0.55, the adjusted gap
  +0.54 and the proxy composite -0.30. Over the 96 one-year dates the order is weaker (the P/E -0.37, the entry price -0.33, the market
  composite -0.33, the adjusted gap +0.31, the EPP gap -0.21, the proxy composite +0.05; the entry date -0.34), and over six months the
  entry price ranks -0.80. Hypothesis, as in 2021-2023: the valuation inputs rank entries well when the multiple swings inside the band;
  test it on other compounders, never on MSFT's own outcomes.
- **The encoding calls, seen afterwards.** The OpenAI call (GAAP FY25 and FY26 with the recurring losses and gains in; retro/README.md,
  "MSFT 2024-2026") moves 5 classes from CHEAP to FAIR in August-October 2026, dates with no outcome yet. The 2024 and 2026 investor-metrics
  decks, the Q2 FY24 comparison and GENAI move no class. That Microsoft's OpenAI stake and its AI business turned out as they did is
  hindsight and stays out of the GENAI question. The calls were decided before scoring and stay; changing a rule means a new method
  version tested elsewhere.
