# CAT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the CAT weekly dates: 783 from 2008-01-04 to 2022-12-30 (105 in 2008-2009, 209 in 2010-2013,
208 in 2014-2017, 261 in 2018-2022), all
Caterpillar Inc. (NYSE: CAT). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was
scored only after its point-in-time build was committed and pushed (2008-2009: 26e9995; 2010-2013: a1a4479; 2014-2017: 6b020c8; 2018-2022: e2fcc32). Outcomes were computed on
2026-11-11; every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2025-12-30). Total returns include the quarterly
dividends ($0.36, then $0.42 from July 2008, $0.44 from July 2010, $0.46 from July 2011, $0.52 from July 2012, $0.60 from July 2013,
$0.70 from July 2014, $0.77 from July 2015, $0.78 from July 2017, $0.86 from July 2018, $1.03
from July 2019, $1.11 from July 2021 and $1.20 from July 2022, ex-dates); no split falls in any horizon, so every price is as traded. Medians of an even
count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call
held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of the benchmark, and
RICH should miss the hurdle and lag the benchmark.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 36 | +14.0% | -21.6% to +152.0% | 14 | 32 | -7.9% | 32 |
| class CHEAP, legacy tier ACCUMULATE | 14 | -14.7% | -23.6% to -7.7% | 0 | 2 | -35.3% | 2 |
| class FAIR, legacy tier ACCUMULATE | 2 | -13.5% | -18.5% to -13.5% | 0 | 0 | -37.2% | 2 |
| class FAIR, legacy tier WATCHLIST | 1 | -18.1% | -18.1% to -18.1% | 0 | 0 | -41.3% | 1 |
| FY07E: guide midpoint $5.40 (2008-01-04 to 2008-01-18) | 3 | +1.0% | -9.8% to +2.1% | 0 | 3 | -35.8% | 3 |
| FY08E: $5.91, up 5-15% on FY07 (2008-01-25 to 2008-07-18) | 26 | -14.7% | -23.6% to -2.5% | 0 | 7 | -35.4% | 10 |
| FY08E: about $6.00 (2008-07-23 to 2008-12-31) | 24 | +110.4% | -2.1% to +152.0% | 14 | 24 | +54.5% | 24 |
| latest print Q3 2007 (2008-01-04 to 2008-01-18) | 3 | +1.0% | -9.8% to +2.1% | 0 | 3 | -35.8% | 3 |
| latest print Q4 2007 (2008-01-25 to 2008-04-11) | 12 | -14.7% | -21.6% to -8.3% | 0 | 3 | -36.6% | 4 |
| latest print Q1 2008 (2008-04-18 to 2008-07-18) | 14 | -13.7% | -23.6% to -2.5% | 0 | 4 | -33.4% | 6 |
| latest print Q2 2008 (2008-07-23 to 2008-10-17) | 13 | +14.0% | -2.1% to +110.4% | 3 | 13 | -7.9% | 13 |
| latest print Q3 2008 (2008-10-22 to 2008-12-31) | 11 | +124.9% | +113.5% to +152.0% | 11 | 11 | +68.1% | 11 |

- **CHEAP held on 34 of 50 dates, and the entry month decided which.** The three January dates ($62.81-68.53, at 11.6-12.7x FY07's
  guided $5.40) returned -9.8% to +2.1% over two years and beat SPY (-16.3% to -10.2%). The 26 dates from the Q4 2007 print to
  2008-07-18 ($65.93-85.28, 11-14x the FY08 guide, 1-31% over the floor) returned -23.6% to -2.5% while SPY returned -18.7% to -6.8%:
  7 beat it, none cleared the hurdle, and the call held on 10 (the three FAIR dates among them, which landed within 15pp of SPY). The 24 dates from the Q2 2008 print ($34.67-72.42) returned -2.1% to +152.0% and all beat SPY; the 11 from 2008-10-22 (5.8-7.4x
  the $6.00 guide, 32-48% under the floor) returned +113.5% to +152.0% and all cleared the hurdle. Every 2008 date sat through a 53-74%
  drawdown; the low close was $22.17 on 2009-03-02. Over three years every 2008 date beat SPY (+21.0% to +177.8%, median +49.8%) and 24
  cleared the three-year hurdle.
- **The EPS anchor was right for 2008 and blind to 2009.** FY08 came in at $5.66 against the $5.91-6.00 the models carried (the Q4 2008
  release), so the 6-7x of October-December was on a real number; but the multiple a capital-goods maker earns at a peak year's EPS is not
  the multiple its history earned on average years, and the price was already discounting the 2009 fall (FY09: $1.43 reported, $2.18
  excluding redundancy costs, in the Q4 2009 release outside the series). Hypothesis, not a rule: a current-year P/E at a cyclical peak
  overstates cheapness; test on other cyclicals and periods, never fit it to CAT.
- **Ratio B and the adjusted gap ranked the dates, through the price.** Across the 53 dates the entry price ranks the two-year return at
  Spearman -0.87 and the return to the m12-24 average price at -0.82; the EPP gap at -0.89 and -0.85, Ratio B at -0.89 and -0.90 and the
  adjusted gap at +0.90 and +0.95 (all the right signs); the proxy composite at +0.70 and +0.77 (the right sign: 2.55-2.70 from Q1 2008
  to Q3 2008, 2.20 on Q4 2007). The two-year price landed nearest BASE on 35 dates and BEAR on 18 (0.51-0.87 times the BASE price, 1.8-3.4
  times BEAR).

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 13 | +262.5% | +124.8% to +358.3% | 13 | 13 | +152.1% | 13 |
| class CHEAP, legacy tier ACCUMULATE | 1 | +209.6% | +209.6% to +209.6% | 1 | 1 | +121.7% | 1 |
| class FAIR, legacy tier ACCUMULATE | 1 | +209.5% | +209.5% to +209.5% | 1 | 1 | +118.8% | 0 |
| class RICH, legacy tier AVOID | 37 | +89.8% | +47.3% to +272.9% | 37 | 37 | +99.4% | 0 |
| FY08E: about $6.00 (2009-01-09 to 2009-01-23) | 3 | +145.2% | +124.8% to +169.7% | 3 | 3 | +78.2% | 3 |
| FY09E: $2.50 (2009-01-27 to 2009-04-17) | 12 | +270.7% | +209.5% to +358.3% | 12 | 12 | +159.7% | 11 |
| FY09E: about $1.25 (2009-04-22 to 2009-07-17) | 13 | +207.1% | +165.7% to +272.9% | 13 | 13 | +149.4% | 0 |
| FY09E: $1.15-2.25, midpoint $1.70 (2009-07-22 to 2009-10-16) | 13 | +80.2% | +47.3% to +181.0% | 13 | 13 | +96.5% | 0 |
| FY09E: $1.85-2.05, midpoint $1.95 (2009-10-21 to 2009-12-31) | 11 | +68.2% | +56.4% to +82.3% | 11 | 11 | +67.0% | 0 |

- **CHEAP held on all 14 dates to 2009-04-17** ($23.23-43.20): +124.8% to +358.3% over two years, all clearing the hurdle and beating SPY
  by 77-260pp. The one FAIR date (2009-02-06, $33.28) returned +209.5%, so its call missed.
- **RICH failed on all 37 dates from the Q1 2009 print.** At 23-32x the FY09 guide (the 93rd-100th percentile of the window) and 90-174%
  over the floor, the stock returned +47.3% to +272.9% over two years, cleared the hurdle and beat SPY on every date (by 35-215pp); over
  three years +51.0% to +248.3%. The two-year price landed nearest XBULL on all 37, at 6.7-12.8 times the BASE price and 1.7-3.5 times
  BULL. The call rested on two numbers that were trough numbers: EPS guided at $1.25-1.95 (the year's low multiple sets its own entry in
  the floor), and BASE growth taken from a sales guide down 25-39% and carried forward two years, which put the BASE price under the BEAR
  price. Hypothesis, not a rule: a current-year P/E at a cyclical trough, and a fiscal-year revenue guide extended as a two-year growth
  rate, read a recovery as richness; whether a normalized EPS or a one-year cap on a negative guide helps is a cross-ticker question for
  a new method version, never a CAT fit.
- **The price ranked the outcome; the composite did not.** Within 2009 the entry price ranks the two-year return at Spearman -0.95 and the
  m12-24 return at -0.93; the EPP gap at -0.76 and -0.67, Ratio B at -0.85 and -0.72, the adjusted gap at +0.77 and +0.63; the proxy
  composite, at its floor of 1.15 on every date from the Q1 2009 print (every signal at BEAR), at +0.09 and -0.13. The signals read the
  quarter that had just collapsed, not the recovery the price was already paying for.
- **Today's profile files CAT CYCLICAL** (`profile_drift` in every outcome), where the point-in-time rule read the 10-Ks' words as DURABLE
  to 2011-02-18; the kind changes the label only, so no price state above depends on it.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier WATCHLIST | 4 | +35.7% | +12.0% to +37.0% | 2 | 1 | +38.5% | 4 |
| class FAIR, legacy tier AVOID | 6 | +27.4% | +9.7% to +36.7% | 1 | 0 | +35.3% | 6 |
| class RICH, legacy tier AVOID | 42 | +50.4% | -2.7% to +127.1% | 27 | 28 | +51.2% | 14 |
| latest print Q3 2009, EPS $1.95 (2010-01-08 to 2010-01-22) | 3 | +75.6% | +64.5% to +101.3% | 3 | 3 | +61.4% | 0 |
| latest print Q4 2009, EPS $2.50 (2010-01-28 to 2010-04-23) | 13 | +91.9% | +60.7% to +127.1% | 13 | 13 | +66.6% | 0 |
| latest print Q1 2010, EPS $2.875 (2010-04-27 to 2010-07-16) | 12 | +49.8% | +31.9% to +62.3% | 11 | 12 | +58.5% | 0 |
| latest print Q2 2010, EPS $3.50 (2010-07-23 to 2010-10-15) | 13 | +27.0% | +8.5% to +37.0% | 3 | 1 | +32.3% | 13 |
| latest print Q3 2010, EPS $3.90 (2010-10-22 to 2010-12-31) | 11 | +4.1% | -2.7% to +13.4% | 0 | 0 | +12.1% | 11 |

- **RICH failed on all 28 dates to 2010-07-16 again, as in 2009.** At $51.75-68.78, 20-31x the FY09 and FY10 guides ($1.95, $2.50,
  $2.875), the stock returned +31.9% to +127.1% over two years, beat SPY on all 28 and cleared the hurdle on 27; the two-year price landed
  nearest BULL on 15 and XBULL on 13 (1.25-8.8 times the BASE price). The guides trailed the recovery: FY2010 came in at $4.15 (the Q4
  2010 release), 66% over January's $2.50, and FY2011 at $7.40. A second sighting of the 2009 hypothesis (a current-year P/E at a cyclical
  trough reads a recovery as richness); still a cross-ticker question, never a CAT fit.
- **From the Q2 2010 print every call held** (24 dates, $65.90-94.45 on the $3.50 and $3.90 guides): the 10 FAIR dates landed within 15pp
  of SPY, and the 14 RICH dates returned -2.7% to +30.7%, lagged SPY by 3-21pp and cleared no hurdle; all 24 landed nearest BASE
  (0.88-1.14 times its price).
- **Only the price ranked the year.** The entry price ranks the two-year return at Spearman -0.93 and the m12-24 return at -0.99; the
  proxy composite at -0.97 and -0.93, the wrong sign (it rose from 1.15 to 3.50 as the recovery was priced in), and the EPP gap (+0.42,
  +0.29), Ratio B (+0.57, +0.43) and the adjusted gap (-0.85, -0.78) all with the wrong sign.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 35 | -1.0% | -22.9% to +20.6% | 0 | 0 | -5.8% | 0 |
| class CHEAP, legacy tier ACCUMULATE | 6 | -10.9% | -14.6% to -8.5% | 0 | 0 | -11.3% | 0 |
| class CHEAP, legacy tier WATCHLIST | 3 | -13.5% | -13.8% to -11.6% | 0 | 0 | -16.2% | 0 |
| class FAIR, legacy tier WATCHLIST | 5 | -20.2% | -23.1% to -16.5% | 0 | 0 | -20.3% | 0 |
| class RICH, legacy tier AVOID | 3 | +6.1% | +5.2% to +9.4% | 0 | 0 | +0.1% | 3 |
| latest print Q3 2010, EPS $3.90 (2011-01-07 to 2011-01-21) | 3 | +6.1% | +5.2% to +9.4% | 0 | 0 | +0.1% | 3 |
| latest print Q4 2010, EPS $6.00 (2011-01-28 to 2011-04-21) | 13 | -9.2% | -22.9% to +5.9% | 0 | 0 | -12.7% | 0 |
| latest print Q1 2011, EPS $6.50 (2011-04-29 to 2011-07-15) | 12 | -13.8% | -23.1% to -8.5% | 0 | 0 | -16.2% | 0 |
| latest print Q2 2011, EPS $6.50 (2011-07-22 to 2011-10-21) | 14 | +6.2% | -14.4% to +20.6% | 0 | 0 | +2.6% | 0 |
| latest print Q3 2011, EPS $6.75 (2011-10-25 to 2011-12-30) | 10 | -1.0% | -8.1% to +5.0% | 0 | 0 | -5.8% | 0 |

- **CHEAP failed on all 44 dates.** -22.9% to +20.6% over two years against SPY's +16.9% to +60.6%: none cleared the hurdle or beat SPY,
  and over three years none beat it either (-6.3% to +44.3%). The 5 FAIR dates of the Q1 2011 period also failed (-23.1% to -16.5%,
  42-49pp behind SPY); only the 3 RICH dates of January, still on FY10's $3.90, held. The low close was $70.55 on 2011-10-03.
- **The 13 dates of the Q4 2010 print rested on two readings, and landed nearest BEAR.** CHEAP and BUY at $95.68-113.12 with BASE at
  +62.9%/yr (the "to exceed $50 billion" bound gave no field, so BASE took Q4 2010's +62.2% sales growth, with "near $6.00" as the EPS):
  -22.9% to +5.9% over two years, 0.35-0.42 times the BASE price. Hypothesis, not a rule: when a one-sided bound falls back to the latest
  quarter's growth, a boom quarter becomes a two-year growth rate; whether a cap or the bound itself as a level helps is a cross-ticker
  question for a new method version, never a CAT fit. (The README's sensitivity shows either reading the other way makes these dates FAIR
  or RICH; that is no reason to change the reading for CAT.)
- **The EPS anchor was right and the multiple fell.** From the Q2 2011 print (27 dates to 2012-01-20, $73.84-105.64, 11.4-16.2x the $6.50
  and $6.75 guides) the stock returned -14.4% to +20.6%, landing nearest BEAR on all 27 (0.46-0.51 times BASE), while FY2011 came in at
  $7.40, above the guides, and FY2012 at $8.48 after a $0.87 Siwei charge.
- **Ranking:** the entry price at -0.91 (two-year) and -0.97 (m12-24); the EPP gap at -0.59 and -0.69, Ratio B at -0.30 and -0.29, the
  adjusted gap at +0.38 and +0.42 (the right signs, weaker than the price); the composite at -0.57 and -0.61 (the wrong sign).

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 40 | +23.7% | -3.0% to +41.9% | 7 | 0 | +9.6% | 7 |
| class CHEAP, legacy tier ACCUMULATE | 12 | -9.9% | -15.1% to -0.4% | 0 | 0 | -22.2% | 0 |
| latest print Q3 2011, EPS $6.75 (2012-01-06 to 2012-01-20) | 3 | -8.2% | -9.3% to -3.0% | 0 | 0 | -15.3% | 0 |
| latest print Q4 2011, EPS $9.25 (2012-01-27 to 2012-04-20) | 13 | -9.9% | -15.1% to +0.6% | 0 | 0 | -22.2% | 0 |
| latest print Q1 2012, EPS $9.50 (2012-04-26 to 2012-07-20) | 13 | +28.0% | +4.6% to +41.9% | 5 | 0 | +4.9% | 5 |
| latest print Q2 2012, EPS $9.60 (2012-07-26 to 2012-10-19) | 13 | +22.1% | +16.8% to +33.3% | 1 | 0 | +11.0% | 1 |
| latest print Q3 2012, EPS $9.125 (2012-10-23 to 2012-12-28) | 10 | +23.8% | +7.1% to +32.2% | 1 | 0 | +16.7% | 1 |

- **CHEAP held on 7 of 52, and beat SPY on none.** The 7 are among the lowest entries ($80.95-85.33 from 2012-06-22 to 2012-07-20,
  2012-08-31 and 2012-11-23), which cleared the hurdle at +32.2% to +41.9%; SPY returned +34.3% to +55.5%, 8-54pp more than CAT on every
  date, and over three years CAT returned -23.4% to +12.5%, behind SPY on all 52. The 13 dates of the Q4 2011 print ($105.87-116.00,
  11.4-12.5x the $9.25 guide) returned -15.1% to +0.6%.
- **A second sighting of the 2008 hypothesis.** At 8.5-12.5x a guided EPS that came in close ($8.48 reported after the $0.87 Siwei charge,
  against $9.125-9.60), the stock was not cheap: the year after fell (FY2013 $5.75, the Q4 2013 release, outside the series). A
  current-year P/E at a cyclical peak overstates cheapness; test across cyclicals and periods, never fit to CAT.
- **Ranking:** the entry price at -0.88 and -0.91; the EPP gap (-0.88, -0.77) and Ratio B (-0.91, -0.67) with the right sign, through the
  price; the adjusted gap (-0.28, -0.38) and the composite (-0.61, -0.70) with the wrong sign. The two-year price landed nearest BASE on
  41 dates and BEAR on 11.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 4 | +1.3% | -5.2% to +10.0% | 0 | 0 | +6.2% | 0 |
| class CHEAP, legacy tier ACCUMULATE | 2 | +0.8% | -9.0% to +0.8% | 0 | 0 | +15.6% | 0 |
| class FAIR, legacy tier ACCUMULATE | 2 | +3.0% | -2.6% to +3.0% | 0 | 0 | +14.5% | 0 |
| class RICH, legacy tier ACCUMULATE | 14 | -1.5% | -13.8% to +11.6% | 0 | 0 | +11.8% | 14 |
| class RICH, legacy tier WATCHLIST | 20 | -1.5% | -16.1% to +8.8% | 0 | 0 | +6.9% | 20 |
| class RICH, legacy tier AVOID | 11 | -10.2% | -20.6% to -5.8% | 0 | 0 | -4.1% | 11 |
| latest print Q3 2012, EPS $9.125 (2013-01-04 to 2013-01-25) | 4 | -3.4% | -9.0% to +1.3% | 0 | 0 | +5.8% | 0 |
| latest print Q4 2012, EPS $8.00 (2013-01-29 to 2013-04-19) | 12 | -2.6% | -13.8% to +10.0% | 0 | 0 | +11.2% | 8 |
| latest print Q1 2013, EPS $7.00 (2013-04-23 to 2013-07-19) | 13 | +7.0% | +0.2% to +11.6% | 0 | 0 | +10.7% | 13 |
| latest print Q2 2013, EPS $6.50 (2013-07-25 to 2013-10-18) | 13 | -5.9% | -16.1% to -0.4% | 0 | 0 | +5.5% | 13 |
| latest print Q3 2013, EPS $5.50 (2013-10-24 to 2013-12-31) | 11 | -10.2% | -20.6% to -5.8% | 0 | 0 | -4.1% | 11 |

- **RICH held on all 45, at 10.9-16.5x.** -20.6% to +11.6% over two years, 22-53pp behind SPY and never clearing the hurdle; over three
  years -28.7% to +23.4%, behind SPY on all 45; the two-year price landed nearest BASE on all 45 (0.76-1.39 times its price). The low
  close in the windows was $63.79 on 2015-09-28. Unlike 2009, the falling guides kept falling: FY2013 came in at $5.75 against the
  $5.50-8.00 midpoints the models carried. The call rested on the negative BASE and the signals at BEAR together (README: at XBULL, 38 of
  the 45 turn CHEAP or FAIR).
- **The 6 CHEAP and 2 FAIR dates failed** (January 2013 at $94.92-97.62 on FY12's $9.125, and the dips of March and April 2013 at
  $80.43-86.97): -9.0% to +10.0%, 29-50pp behind SPY.
- **Ranking:** the entry price ranked little (-0.31, -0.24); the EPP gap (-0.59, -0.77), Ratio B (-0.56, -0.74) and the adjusted gap
  (+0.54, +0.72) carried the right sign beyond the price; the composite (-0.44, -0.21) did not.

## 2008-2013: what the cycle shows (hindsight)

- **Calls held:** 2010-2013, CHEAP 7 of 102, FAIR 10 of 17, RICH 62 of 90; with 2008-2009, CHEAP 55 of 166, FAIR 13 of 21, RICH 62 of 127,
  130 of 314 in all.
- **The class turned with the guide, not ahead of it.** CHEAP through 2008 and in 2011-2012, at peak earnings; RICH from the Q1 2009 print
  to the Q1 2010 print, at trough earnings, and again as the guide fell in 2013. The RICH calls failed while the guide sat at its low
  (2009 to mid-2010) and held once it had caught up (late 2010) or kept falling (2013); the CHEAP calls held where the price had already
  fallen with the cycle (July 2008 to April 2009) and failed at peak earnings in 2011-2012, when it had not.
- **Over 2010-2013 the model's own numbers did not rank the outcomes.** Pooled over the 209 dates the entry price ranks the two-year
  return at -0.77 and the m12-24 return at -0.91; the P/E on the guided EPS at +0.06 and +0.16, the EPP gap at +0.05 and +0.20, Ratio B at
  +0.15 and +0.36, the adjusted gap at -0.26 and -0.50 and the composite at -0.31 and -0.49 (each the wrong sign or none). The composite,
  which reads the latest quarter, was highest (3.0-3.7) from Q2 2010 to Q4 2011, dates followed by some of the worst returns.
- **Hypotheses, not rules** (each needs other cyclicals and periods, and a new method version with a full re-run, never a CAT fit): for a
  capital-goods cyclical, a P/E on the current-year guide is pro-cyclical (cheap at peaks, rich at troughs); a normalized or mid-cycle EPS
  would read the cycle differently; and a composite of year-on-year quarterly changes is late at turning points.
- **Today's profile** files CAT CYCLICAL, risk 1 (`profile_drift` in every outcome): from 2011-02-23 the point-in-time kind agrees and
  only the risk score differs (2 then, 1 today).

## 2014 (51 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 51 | -18.5% | -29.0% to +11.7% | 0 | 0 | -26.7% | 51 |
| latest print Q3 2013, EPS $5.5 (2014-01-10 to 2014-01-24) | 3 | -24.0% | -28.3% to -22.6% | 0 | 0 | -13.5% | 3 |
| latest print Q4 2013, EPS $5.85 (2014-01-28 to 2014-04-17) | 12 | -20.3% | -28.7% to -16.2% | 0 | 0 | -22.2% | 12 |
| latest print Q1 2014, EPS $6.1 (2014-04-25 to 2014-07-18) | 13 | -24.0% | -29.0% to -20.3% | 0 | 0 | -31.9% | 13 |
| latest print Q2 2014, EPS $6.2 (2014-07-25 to 2014-10-17) | 13 | -14.3% | -19.3% to +1.1% | 0 | 0 | -30.2% | 13 |
| latest print Q3 2014, EPS $6.5 (2014-10-24 to 2014-12-26) | 10 | +0.3% | -11.8% to +11.7% | 0 | 0 | -24.2% | 10 |

- **RICH held on all 51.** At $86.17-111.08, 13.9-18.2x the FY14 guide, the stock returned -29.0% to +11.7% over two years, 5-42pp behind
  SPY, and cleared no hurdle; every date landed nearest BASE (0.74-1.19 times its price) and sat through a 39-48% drawdown to the low close
  of $57.91 on 2016-01-25. The guide was not the problem for the year itself: FY2014 came in at $6.38 excluding restructuring costs,
  above every guide the models carried ($5.85-6.50); the next two years fell (FY2015 $4.64, FY2016 $3.42, both in the fact sheet's later
  prints). Over three years they returned -0.5% (2014-04-17) to +75.7% (2014-12-26, into the 2017 rally), 14 of 51 ahead of SPY.
- **Ranking:** the P/E on the guide (-0.64, -0.80), the EPP gap (-0.64, -0.80) and Ratio B (-0.42, -0.85) carried the right sign; the
  entry price ranked the two-year return weakly (-0.26) and the m12-24 return strongly (-0.98); the composite ranked nothing (+0.17, -0.07).

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 53 | +34.7% | +7.5% to +141.0% | 27 | 51 | +9.2% | 2 |
| latest print Q3 2014, EPS $6.5 (2015-01-02 to 2015-01-23) | 4 | +17.5% | +7.5% to +19.0% | 0 | 2 | -6.0% | 2 |
| latest print Q4 2014, EPS $4.75 (2015-01-28 to 2015-04-17) | 12 | +24.6% | +18.9% to +31.3% | 0 | 12 | +4.0% | 0 |
| latest print Q1 2015, EPS $5 (2015-04-24 to 2015-07-17) | 13 | +27.8% | +20.9% to +38.8% | 3 | 13 | +4.0% | 0 |
| latest print Q2 2015, EPS $5 (2015-07-24 to 2015-10-16) | 13 | +70.2% | +50.3% to +100.8% | 13 | 13 | +33.5% | 0 |
| latest print Q3 2015, EPS $4.6 (2015-10-23 to 2015-12-31) | 11 | +105.0% | +92.1% to +141.0% | 11 | 11 | +52.5% | 0 |

- **RICH failed on 51 of 53.** Only 2015-01-02 and 2015-01-09 held (+7.5% and +12.3%, 3-6pp behind SPY). From the Q4 2014 print to the Q1
  2015 period ($79.23-88.63, 16.4-17.9x the $4.75 and $5.00 guides) the stock returned +18.9% to +38.8%, ahead of SPY on all 25; from the Q2 2015
  print (24 dates, $64.98-78.63, 13.0-16.1x the $5.00 and $4.60 guides) +50.3% to +141.0%, every one clearing the hurdle. Over three years
  every 2015 date beat SPY (+66.8% to +151.6%). The two-year price landed nearest BULL on 49 dates (up to 3.1 times the BASE price).
- **Ranking:** the entry price at -0.87 and -0.92; the P/E (-0.49, -0.54), the EPP gap (-0.62, -0.63) and Ratio B (-0.49, -0.50) with the
  right sign; the adjusted gap (-0.68, -0.68) and the composite (-0.79, -0.80) with the wrong one.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +94.2% | +34.1% to +193.5% | 52 | 52 | +75.1% | 0 |
| latest print Q3 2015, EPS $4.6 (2016-01-08 to 2016-01-22) | 3 | +190.4% | +172.1% to +193.5% | 3 | 3 | +91.1% | 0 |
| latest print Q4 2015, EPS $4 (2016-01-29 to 2016-04-15) | 12 | +125.9% | +97.6% to +171.2% | 12 | 12 | +73.7% | 0 |
| latest print Q1 2016, EPS $3.7 (2016-04-22 to 2016-07-22) | 14 | +105.7% | +80.3% to +131.7% | 14 | 14 | +82.4% | 0 |
| latest print Q2 2016, EPS $3.55 (2016-07-27 to 2016-10-21) | 13 | +77.0% | +59.5% to +97.3% | 13 | 13 | +72.8% | 0 |
| latest print Q3 2016, EPS $3.25 (2016-10-26 to 2016-12-30) | 10 | +43.8% | +34.1% to +60.6% | 10 | 10 | +57.5% | 0 |

- **RICH failed on all 52, as in 2009.** From the January low ($59.87 on 2016-01-15) to $95.81 on 2016-11-25, at 13.0-29.5x a guide falling
  from $4.60 to $3.25, the stock returned +34.1% to +193.5% over two years, cleared the hurdle and beat SPY on every date (by 10-141pp);
  the two-year price landed nearest XBULL on 40 and BULL on 12, at 3.0-4.0 times the BASE price. The sales guides fell to $39 billion
  (BASE -9% to -16%/yr) while the order cycle turned; within 2017 the FY17 guide itself rose from $2.90 to $6.25. A third sighting of the
  2009-2010 hypothesis: a current-year P/E at a cyclical trough, and a falling fiscal-year sales guide carried as two-year growth, read a
  recovery as richness; still a cross-ticker question for a new method version, never a CAT fit.
- **Ranking:** the entry price at -0.96 and -0.80; the P/E on the guide (-0.96, -0.69), the EPP gap (-0.96, -0.69) and the adjusted gap
  (+0.94, +0.64) with the right sign, all through the price; the composite (-0.83, -0.57) with the wrong one (it sat at 1.15-1.30, every
  signal at or near BEAR, while the recovery was priced in).

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +24.3% | -1.4% to +58.9% | 24 | 29 | +25.5% | 23 |
| latest print Q3 2016, EPS $3.25 (2017-01-06 to 2017-01-20) | 3 | +46.6% | +44.6% to +51.3% | 3 | 3 | +51.8% | 0 |
| latest print Q4 2016, EPS $2.9 (2017-01-27 to 2017-04-21) | 13 | +49.8% | +40.2% to +58.9% | 13 | 13 | +47.1% | 0 |
| latest print Q1 2017, EPS $3.75 (2017-04-26 to 2017-07-21) | 13 | +32.9% | +19.3% to +46.1% | 8 | 13 | +28.0% | 0 |
| latest print Q2 2017, EPS $5 (2017-07-26 to 2017-10-20) | 13 | +8.2% | +0.7% to +23.1% | 0 | 0 | +11.6% | 13 |
| latest print Q3 2017, EPS $6.25 (2017-10-25 to 2017-12-29) | 10 | +7.3% | -1.4% to +13.7% | 0 | 0 | -5.4% | 10 |

- **RICH failed on the 29 dates to 2017-07-21 and held on the 23 from the Q2 2017 print.** The January to July dates ($92.15-108.77, 26.6-34.1x
  the $2.90 and $3.75 guides, the 97th-100th percentile) returned +19.3% to +58.9% and beat SPY by 1-31pp; the two-year price landed
  nearest XBULL or BULL. From the Q2 2017 print ($112.85-157.58, 21.8-26.3x the $5.00 and $6.25 guides, BASE +13% to +16%/yr) they returned -1.4% to
  +23.1%, 3-26pp behind SPY, after the high close of $170.89 on 2018-01-22. Over three years (to the end of 2020) 12 of 52 beat SPY.
- **Ranking:** the entry price at -0.92 and -0.99; the P/E (+0.79, +0.82), the EPP gap (+0.79, +0.82) and Ratio B (+0.69, +0.78) with the
  wrong sign (the multiple was highest on the trough guide of January, the best entries); the adjusted gap (-0.83, -0.88) and the
  composite (-0.89, -0.97) with the wrong sign as well.

## 2014-2017: what the downturn and recovery show (hindsight)

- **Calls held:** RICH 76 of 208 (2014: 51 of 51; 2015: 2 of 53; 2016: 0 of 52; 2017: 23 of 52). With 2008-2013: CHEAP 55 of 166, FAIR 13
  of 21, RICH 138 of 335, 206 of 522 in all.
- **One class for four years, so the class carried no timing.** Every 2014-2017 date was RICH, and the point-in-time sensitivity (README,
  "CAT 2014-2017") shows no encoding or signal setting changes that: 2009's -61.5% year sits in the history as BEAR through 2018, so the
  downside to BEAR is 88-95% on every date, and the falling guides pull BULL to or under the price. The same call was right at the 2014
  top and wrong from the 2015 lows through mid-2017. Hypothesis, not a rule: one extreme year as BEAR for a decade makes Ratio B
  insensitive for a deep cyclical; whether a BEAR drawn from more than one year, or capped, would discriminate is a cross-ticker question
  for a new method version, never a CAT fit.
- **The model's numbers did not rank the outcomes pooled.** Over the 208 dates the entry price ranks the two-year return at -0.79 and the
  m12-24 return at -0.67; the P/E on the guide at +0.06 and +0.28, the EPP gap at -0.03 and +0.20, Ratio B at +0.23 and +0.35, the
  adjusted gap at -0.63 and -0.72 and the composite at -0.75 and -0.76 (each the wrong sign or none), as in 2010-2013. Within years the
  P/E, the EPP gap and Ratio B carried the right sign in 2014-2016 and the wrong one in 2017; across 2008-2017 (522 dates) the entry price
  ranks at -0.68 and -0.64 and every model metric with the wrong sign (P/E +0.25 and +0.33, Ratio B +0.27 and +0.31, the adjusted gap -0.41
  and -0.49, the composite -0.43 and -0.51).
- **The trough pattern repeats.** The RICH calls failed where the guided EPS sat at its low and the price had already turned (2009 to
  mid-2010; mid-2015 to mid-2017) and held where the guide was near its high (2014, late 2017). Together with 2008 and 2011-2012 (CHEAP at
  peak guides that failed), CAT gives four sightings of the same hypothesis: for a capital-goods cyclical a P/E on the current-year guide
  is pro-cyclical. It needs other cyclicals and periods before any method change.
- **Today's profile** files CAT CYCLICAL, risk 1 (`profile_drift` in every outcome); the point-in-time kind agrees on every 2014-2017
  date and only the risk score differs (2 then, 1 today).

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 3 | -9.0% | -10.0% to -4.0% | 0 | 0 | -21.5% | 3 |
| class CHEAP, legacy tier ACCUMULATE | 13 | -12.0% | -35.6% to -5.7% | 0 | 0 | -14.2% | 0 |
| class CHEAP, legacy tier BUY | 36 | +5.2% | -25.0% to +57.1% | 11 | 8 | -6.6% | 11 |
| latest print Q3 2017, EPS $6.25 (2018-01-05 to 2018-01-19) | 3 | -9.0% | -10.0% to -4.0% | 0 | 0 | -21.5% | 3 |
| latest print Q4 2017, EPS $8.75 (2018-01-26 to 2018-04-20) | 13 | -12.0% | -35.6% to -5.7% | 0 | 0 | -14.2% | 0 |
| latest print Q1 2018, EPS $10.75 (2018-04-25 to 2018-07-27) | 14 | -6.5% | -25.0% to +4.0% | 0 | 0 | -10.5% | 0 |
| latest print Q2 2018, EPS $11.5 (2018-07-31 to 2018-10-19) | 12 | +9.0% | -2.1% to +32.8% | 1 | 1 | -7.5% | 1 |
| latest print Q3 2018, EPS $11.5 (2018-10-24 to 2018-12-28) | 10 | +48.3% | +33.8% to +57.1% | 10 | 7 | +10.5% | 10 |

- **CHEAP failed on the 38 dates from the Q4 2017 print to 2018-10-12 and held on the 11 after it.** From the Q4 2017 print to the Q2 2018
  period ($131.32-167.06, 11.4-19.1x guides of $8.75-11.50, with BASE at +24% to +36%/yr from the quarters' sales growth) the stock
  returned -35.6% to +19.9% over two years, 9-37pp behind SPY, and landed nearest BEAR on 26 dates (as low as 0.38 times the BASE price):
  the 2011 pattern again, a boom quarter carried as two-year growth (Q4 2017's +34.7%). The guided EPS was right (FY2018 came in at $11.22
  against the $8.75-11.50 the models carried); the price fell with the 2019-2020 slowdown. The 11 dates from 2018-10-19 ($112.34-136.86, 9.8-11.9x,
  under the floor) returned +32.8% to +57.1% and cleared the hurdle. The 3 RICH dates of January held (-10.0% to -4.0%).
- **Ranking:** the P/E on the guide (-0.85, -0.89), the EPP gap (-0.85, -0.89), Ratio B (-0.69, -0.83) and the adjusted gap (+0.78, +0.88)
  carried the right sign, as did the entry price (-0.78, -0.98); the composite (-0.65, -0.37) the wrong one (it was 3.0-3.2 all year).

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 51 | +64.7% | +38.1% to +108.1% | 51 | 41 | +41.5% | 51 |
| class CHEAP, legacy tier ACCUMULATE | 1 | +44.8% | +44.8% to +44.8% | 1 | 0 | +42.6% | 1 |
| latest print Q3 2018, EPS $11.5 (2019-01-04 to 2019-01-25) | 4 | +48.3% | +42.8% to +52.7% | 4 | 2 | +6.2% | 4 |
| latest print Q4 2018, EPS $12.25 (2019-01-29 to 2019-04-18) | 12 | +69.3% | +50.9% to +80.4% | 12 | 12 | +14.2% | 12 |
| latest print Q1 2019, EPS $12.25 (2019-04-25 to 2019-07-19) | 13 | +75.1% | +55.2% to +108.1% | 13 | 13 | +38.2% | 13 |
| latest print Q2 2019, EPS $12.25 (2019-07-25 to 2019-10-18) | 13 | +66.4% | +55.4% to +94.1% | 13 | 13 | +60.5% | 13 |
| latest print Q3 2019, EPS $10.84 (2019-10-24 to 2019-12-27) | 10 | +46.9% | +38.1% to +56.2% | 10 | 1 | +44.7% | 10 |

- **CHEAP held on all 52.** At 9.3-13.7x the $12.25 and $10.84 guides (the 0th-35th percentile) the stock returned +38.1% to +108.1% over two
  years, cleared the hurdle on every date and beat SPY on 41; every date landed nearest BASE (0.75-1.51 times its price), through a 39%
  drawdown to the low close of $91.85 on 2020-03-23. Over three years 43 of 52 beat SPY.
- **Ranking:** the P/E (-0.75, -0.42), the EPP gap (-0.75, -0.43) and Ratio B (-0.86, -0.42) with the right sign; the composite (-0.03, -0.93),
  falling from 2.8 to 1.8 as the quarters slowed, the wrong one.

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 2 | +59.9% | +45.1% to +59.9% | 2 | 1 | +44.1% | 2 |
| class CHEAP, legacy tier BUY | 12 | +99.0% | +57.4% to +140.2% | 12 | 12 | +86.6% | 12 |
| class FAIR, legacy tier ACCUMULATE | 4 | +59.6% | +56.2% to +68.1% | 4 | 4 | +71.9% | 1 |
| class RICH, legacy tier ACCUMULATE | 11 | +43.9% | +18.5% to +71.3% | 8 | 11 | +49.2% | 0 |
| class RICH, legacy tier WATCHLIST | 7 | +28.9% | +15.3% to +51.0% | 3 | 7 | +32.4% | 0 |
| class FAIR, legacy tier BUY | 4 | +82.5% | +58.6% to +87.9% | 4 | 4 | +74.2% | 0 |
| class RICH, legacy tier BUY | 3 | +46.6% | +46.3% to +57.9% | 3 | 3 | +62.3% | 0 |
| class RICH, legacy tier AVOID | 10 | +36.5% | +10.8% to +42.9% | 7 | 10 | +15.3% | 0 |
| latest print Q3 2019, EPS $10.84 (2020-01-03 to 2020-01-24) | 4 | +58.7% | +45.1% to +59.9% | 4 | 3 | +45.4% | 4 |
| latest print Q4 2019, EPS $9.25/$11.06 (2020-01-31 to 2020-04-24) | 13 | +80.4% | +46.1% to +140.2% | 13 | 13 | +75.5% | 8 |
| latest print Q1 2020, EPS $11.06 (2020-04-29 to 2020-07-24) | 13 | +71.3% | +32.1% to +99.1% | 12 | 13 | +69.5% | 3 |
| latest print Q2 2020, EPS $11.06 (2020-07-31 to 2020-10-23) | 13 | +27.9% | +10.8% to +55.8% | 5 | 13 | +36.8% | 0 |
| latest print Q3 2020, EPS $11.06 (2020-10-28 to 2020-12-31) | 10 | +39.5% | +31.7% to +51.0% | 9 | 10 | +15.3% | 0 |

- **CHEAP held on all 14, RICH failed on all 31.** The CHEAP dates (January on the FY19 guide, and the March-May fall at 9.5-11.3x, $95.50-125.03)
  returned +45.1% to +140.2% over two years. The 31 RICH dates (2 in February, 6 in May and June, and every date from 2020-07-02, on FY19's $11.06
  with BASE at -19.5% to -29.2%/yr from the pandemic quarters) returned +10.8% to +71.3% and beat SPY on all 31 (by 3-39pp), landing
  nearest BULL. A fourth sighting of the
  trough pattern (2009, 2010, 2016 and now 2020): a falling quarter's sales growth carried as two-year growth reads a recovery as richness.
  Of the 8 FAIR dates, 1 held. Over three years every 2020 date beat SPY (+47.4% to +144.5%).
- **Ranking:** the entry price (-0.84, -0.99), the P/E (-0.75, -0.89), the EPP gap (-0.77, -0.92), Ratio B (-0.81, -0.90) and the adjusted gap
  (+0.84, +0.88) all with the right sign; the composite (+0.69, +0.69) too, for once (it was lowest on the RICH dates of the second half).

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +29.0% | -9.7% to +49.6% | 21 | 40 | +5.8% | 12 |
| latest print Q3 2020, EPS $11.06 (2021-01-08 to 2021-01-22) | 3 | +34.8% | +32.7% to +37.4% | 3 | 3 | +5.8% | 0 |
| latest print Q4 2020, EPS $6.56 (2021-01-29 to 2021-04-23) | 13 | +3.1% | -5.4% to +49.6% | 2 | 7 | -5.5% | 6 |
| latest print Q1 2021, EPS $6.56 (2021-04-30 to 2021-07-23) | 13 | +10.7% | -9.7% to +27.5% | 0 | 7 | -3.3% | 6 |
| latest print Q2 2021, EPS $6.56 (2021-07-30 to 2021-10-22) | 13 | +39.4% | +29.0% to +45.3% | 11 | 13 | +13.3% | 0 |
| latest print Q3 2021, EPS $6.56 (2021-10-29 to 2021-12-31) | 10 | +32.3% | +19.1% to +47.7% | 5 | 10 | +21.0% | 0 |

- **RICH held on 12 of 52.** On FY2020's $6.56 (no outlook) the stock stood at 28-37x and returned -9.7% to +49.6% over two years; the
  12 that held are the dates from 2021-03-19 to 2021-06-04 ($225.29-244.02, -9.7% to +2.2%, 2-11pp behind SPY); the 40 others beat SPY by 2-45pp
  as FY2021 came in at $10.81 and the multiple on it fell to 15-22x. Over three years every 2021 date beat SPY (+40.2% to +112.8%).
  Hypothesis, not a rule: with no guide, the last full year's EPS at a trough overstates the multiple; the rollover rule was written for
  the weeks between a year-end and its Q4 print, not for years without guidance; whether a different anchor helps is a cross-ticker
  question for a new method version, never a CAT fit.
- **Ranking:** the entry price (-0.82, -0.85), the P/E (-0.82, -0.84), the EPP gap (-0.78, -0.81), Ratio B (-0.72, -0.78) and the adjusted
  gap (+0.65, +0.74) with the right sign, all through the price; the composite (+0.49, +0.60) with the right sign as well.

## 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 24 | +70.9% | +31.1% to +110.8% | 23 | 22 | +45.4% | 0 |
| class FAIR, legacy tier WATCHLIST | 18 | +83.3% | +53.7% to +130.1% | 18 | 18 | +67.6% | 0 |
| class CHEAP, legacy tier WATCHLIST | 4 | +132.2% | +72.8% to +144.6% | 4 | 4 | +92.2% | 4 |
| class CHEAP, legacy tier ACCUMULATE | 1 | +78.4% | +78.4% to +78.4% | 1 | 1 | +37.4% | 1 |
| class FAIR, legacy tier AVOID | 5 | +64.8% | +63.7% to +82.8% | 5 | 5 | +20.3% | 0 |
| latest print Q3 2021, EPS $6.56 (2022-01-07 to 2022-01-21) | 3 | +33.2% | +31.1% to +37.8% | 2 | 3 | +11.4% | 0 |
| latest print Q4 2021, EPS $10.81 (2022-01-28 to 2022-04-22) | 13 | +64.8% | +53.7% to +78.4% | 13 | 13 | +25.1% | 3 |
| latest print Q1 2022, EPS $10.81 (2022-04-29 to 2022-07-29) | 14 | +79.5% | +53.1% to +105.2% | 14 | 14 | +53.7% | 0 |
| latest print Q2 2022, EPS $10.81 (2022-08-03 to 2022-10-21) | 12 | +102.6% | +75.9% to +144.6% | 12 | 12 | +72.4% | 2 |
| latest print Q3 2022, EPS $10.81 (2022-10-28 to 2022-12-30) | 10 | +72.1% | +55.9% to +82.8% | 10 | 8 | +45.7% | 0 |

- **RICH and FAIR failed on all 47, CHEAP held on all 5.** On FY2021's $10.81 (no outlook) at 15-22x, the stock returned +31.1% to +130.1%
  over two years; with the 5 CHEAP dates, 51 of the 52 cleared the hurdle and 50 beat SPY. The FAIR dates landed 20-70pp above SPY,
  outside the ±15pp band. The 5
  CHEAP dates (2022-02-18 to 2022-09-30 dips) returned +72.8% to +144.6%. Every date landed nearest BULL (1.22-1.91 times the BASE price);
  the low close was $162.44 on 2022-09-27. Over three years every 2022 date beat SPY (+33.3% to +205.0%).
- **Ranking:** the entry price (-0.75, -0.65), the P/E (-0.80, -0.71) and the EPP gap (-0.80, -0.71) with the right sign; Ratio B (-0.56,
  -0.37) too; the adjusted gap (-0.03, -0.11) none; the composite (-0.60, -0.58) the wrong one.

## 2018-2022: what the second cycle shows (hindsight)

- **Calls held:** CHEAP 82 of 120, FAIR 1 of 31, RICH 15 of 110, 98 of 261 (2018: 14 of 52; 2019: 52 of 52; 2020: 15 of 53; 2021: 12 of 52;
  2022: 5 of 52). With 2008-2017: CHEAP 137 of 286, FAIR 14 of 52, RICH 153 of 445, 304 of 783 in all.
- **Within each year the valuation metrics ranked the outcomes; across years they did not.** In every year from 2018 to 2022 the P/E on the
  guide, the EPP gap and Ratio B carried the right sign (-0.42 to -0.92 on the m12-24 return), unlike 2010-2017. Pooled over 2018-2022 the
  entry price ranks at -0.29 and -0.31, the P/E at -0.41 and -0.36, the EPP gap at -0.44 and -0.40, Ratio B at -0.35 and -0.26 (the right
  sign, weakly), the adjusted gap at +0.06 and -0.22 and the composite at -0.33 and -0.52 (none or the wrong sign). Across 2008-2022
  (783 dates) only the adjusted gap (-0.26, -0.38), the composite (-0.38, -0.48) and the entry price (-0.21, -0.27) are clearly signed, and
  the first two the wrong way.
- **The level of the call was set by the anchor, not by the price.** CHEAP held where the EPS anchor was a guide near the cycle's level
  (late 2018, 2019, early 2020); RICH failed where the anchor was a trough quarter's growth (the second half of 2020) or a trough year
  with no outlook (2021, 2022). The boom quarter of Q4 2017 made the early-2018 CHEAP calls fail as in 2011.
- **Hypotheses, not rules** (other cyclicals and periods first, then a new method version with a full re-run, never a CAT fit): BASE from
  one quarter's sales growth misreads both a boom (2011, 2018) and a bust (2009, 2020) for a deep cyclical; and the rollover rule's
  last-full-year EPS, applied for years when a company gives no outlook, anchors the multiple to a trough.
- **Today's profile** files CAT CYCLICAL, risk 1 (`profile_drift`); the point-in-time kind agrees on every 2018-2022 date and only the risk
  score differs (2 then, 1 today).
