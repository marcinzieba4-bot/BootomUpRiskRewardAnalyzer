# CMCSA retrospective findings (hindsight)

Patterns seen in `outcome.json` for the CMCSA weekly dates: 314 from 2008-01-04 to 2013-12-31, all Comcast Corporation (Nasdaq: CMCSA,
the Class A shares). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored
only after its point-in-time build was committed and pushed (2008-2009: 573d484; 2010-2013: 99b3102). Outcomes were computed on
2026-11-11 from the closes posted to 2026-11-10; every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2016-12-30). Total
returns include the quarterly dividends from April 2008 ($0.0625, then $0.0675, $0.0945, $0.1125, $0.1625 and $0.195); the prices are on
the as-traded basis of the models (Yahoo's series times its 2017 split and its 2026 factor, both after every horizon). Medians of an even
count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of it, and RICH should miss the
hurdle and lag it.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | -3.8% | -21.3% to +53.8% | 9 | 28 | -16.9% | 35 |
| FY07E: FY06's $0.60 stands (2008-01-04 to 2008-02-08) | 6 | +0.9% | -11.1% to +4.0% | 0 | 6 | -12.3% | 6 |
| FY08E: FY07's $0.74 stands (2008-02-15 to 2008-12-31) | 47 | -4.6% | -21.3% to +53.8% | 9 | 22 | -18.1% | 29 |
| latest print Q3 2007 (2008-01-04 to 2008-02-08) | 6 | +0.9% | -11.1% to +4.0% | 0 | 6 | -12.3% | 6 |
| latest print Q4 2007 (2008-02-15 to 2008-04-25) | 11 | -6.6% | -21.3% to +0.1% | 0 | 8 | -22.4% | 8 |
| latest print Q1 2008 (2008-05-02 to 2008-07-25) | 13 | -7.4% | -18.5% to +1.6% | 0 | 11 | -25.0% | 11 |
| latest print Q2 2008 (2008-07-31 to 2008-10-24) | 13 | -8.7% | -17.0% to +53.8% | 1 | 2 | -16.9% | 2 |
| latest print Q3 2008 (2008-10-30 to 2008-12-31) | 10 | +40.0% | +20.3% to +50.7% | 8 | 1 | +15.8% | 8 |

- **CHEAP held on 35 of 53 dates, and the entry month decided which.** The six dates before the Q4 2007 print ($16.84-18.55) returned
  -11.1% to +4.0% over two years and beat SPY (-18.4% to -10.2%) by 7.3-20.4pp. The 34 dates from 2008-02-15 to 2008-10-03 ($18.33-22.50,
  from 15% under to 5% over the 29x floor) returned -21.3% to +1.6% while SPY returned -18.7% to +8.0%: 20 beat it, 14 lagged by up to
  7.9pp, none cleared the hurdle. The 13 dates from 2008-10-10 ($13.07-17.41, 19-39% under the floor) returned +20.3% to +53.8%; 9
  cleared the hurdle, but only 2 beat SPY's rebound (+27.7% to +56.9%), so 4 missed. Every 2008 date sat through a 38-51% drawdown; the
  low close was $11.22 on 2009-03-09, 12.3x FY08's $0.91. Over three years (to the end of 2011) the 2008 dates returned -4.1% to +97.0%
  (median +31.7%); 49 beat SPY and 7 cleared the three-year hurdle (+52.1%).
- **The floor sat far above where the stock bottomed.** The EPP floor was 29x the standing EPS on every 2008 date ($17.40, then $21.46
  from the Q4 2007 print), the median of calendar-year lows that include 63.0x (2004) and 69.1x (2005): GAAP multiples on $0.28 and $0.25
  of EPS, after $1.8-1.9 billion of interest a year, in years before EPS tripled to $0.74 (2007) and $0.91 (2008). The stock then fell to
  48% under that floor. The PFE shape again, from another cause: there a multiple falling on a shrinking franchise, here a multiple
  compressing while earnings rose from a depressed base. Hypothesis, not a rule: a floor (and a window) built on years whose EPS later
  multiplies overstates the multiple the market will pay at a trough; test on other tickers and periods, never fit it to CMCSA.
- **BULL and Ratio B said nothing.** BULL grew EPS at the 2004-2006 and then the 2004-2007 CAGR (+46.4% and +38.3%/yr) to the 75th-percentile multiple, $94-103; the
  two-year price was 0.15-0.22 times it and landed nearest BEAR on all 53 dates (0.90-1.48 times the BEAR price). Ratio B was -0.03 to
  0.08 on every date, so the legacy tier read BUY throughout. Hypothesis: a scenario growth rate measured from a depressed first year of
  the history inflates BULL and XBULL without bound; whether a bound helps is a cross-ticker question.
- **Entry price ranks the outcome, as in every one-stock crash.** Across the 53 dates the entry price ranks the return to the m12-24
  average price at Spearman -0.89 and the two-year return at -0.87; the EPP gap at -0.79 and Ratio B at -0.79 (the right signs, both
  driven by the price); the adjusted gap at +0.24 (right sign) and the proxy composite at -0.32 (the wrong sign: the composite was
  highest early in 2008, at the higher prices).

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +66.8% | +26.0% to +125.5% | 51 | 50 | +49.1% | 52 |
| FY08E: FY07's $0.74 stands (2009-01-09 to 2009-02-13) | 6 | +61.5% | +43.2% to +80.7% | 6 | 4 | +29.1% | 6 |
| FY09E: FY08's $0.91 stands (2009-02-19 to 2009-12-31) | 46 | +67.0% | +26.0% to +125.5% | 45 | 46 | +49.6% | 46 |
| latest print Q3 2008 (2009-01-09 to 2009-02-13) | 6 | +61.5% | +43.2% to +80.7% | 6 | 4 | +29.1% | 6 |
| latest print Q4 2008 (2009-02-19 to 2009-04-24) | 10 | +92.9% | +73.8% to +125.5% | 10 | 10 | +49.2% | 10 |
| latest print Q1 2009 (2009-05-01 to 2009-07-31) | 14 | +76.7% | +64.6% to +98.2% | 14 | 14 | +52.7% | 14 |
| latest print Q2 2009 (2009-08-07 to 2009-10-30) | 13 | +42.3% | +26.0% to +70.1% | 12 | 13 | +49.1% | 13 |
| latest print Q3 2009 (2009-11-05 to 2009-12-31) | 9 | +46.6% | +33.2% to +65.9% | 9 | 9 | +45.0% | 9 |

- **CHEAP held on all 52 dates.** The 30 dates from January to July 2009 ($11.63-16.36) returned +43.2% to +125.5% over two years and all
  cleared the hurdle; 28 beat SPY (the two that lagged, 2009-01-09 and 2009-01-16, by 4.5-4.6pp, still cleared the hurdle). The 22
  dates from August ($14.20-17.64) returned +26.0% to +70.1% and beat SPY (+10.4% to +28.7%) by 11.0-47.9pp; 21 cleared the hurdle.
  Every date was 15-51% under the floor.
- **The three-year read is stronger still.** Measured to January-December 2012, the 2009 dates returned +61.3% to +173.6% (median
  +125.7%); all 52 cleared the three-year hurdle and beat SPY.
- **The class never moved while the inputs did.** Through 2009 video subscriber growth went from -2.3% to -2.7%, revenue growth from
  +9.4% to +3.0%, BASE from +12.8% to +6.4%/yr and the proxy composite between 1.75 and 2.05, and the price state stayed CHEAP. Within
  the year the entry price ranks the two-year return at Spearman -0.91 and the return to the m12-24 average price at -0.62, the EPP gap
  at -0.78; the proxy composite (+0.18), the adjusted gap (+0.06) and Ratio B (-0.10) rank it barely at all.
- **The two-year price landed nearest BEAR on all 52 dates,** at 1.51-2.13 times the BEAR price, 0.51-0.69 times BASE and 0.17-0.24
  times BULL: the scenarios' spread, not the direction, failed.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +78.4% | +50.8% to +107.0% | 52 | 52 | +45.5% | 52 |
| FY09E: FY08's $0.91 stands (2010-01-08 to 2010-01-29) | 4 | +69.7% | +50.8% to +71.6% | 4 | 4 | +49.2% | 4 |
| FY10E: FY09's $1.26 stands (2010-02-04 to 2010-12-31) | 48 | +80.1% | +55.9% to +107.0% | 48 | 48 | +45.5% | 48 |
| latest print Q3 2009 (2010-01-08 to 2010-01-29) | 4 | +69.7% | +50.8% to +71.6% | 4 | 4 | +49.2% | 4 |
| latest print Q4 2009 (2010-02-04 to 2010-04-23) | 12 | +74.8% | +57.9% to +87.5% | 12 | 12 | +38.5% | 12 |
| latest print Q1 2010 (2010-04-29 to 2010-07-23) | 13 | +69.5% | +55.9% to +90.3% | 13 | 13 | +40.1% | 13 |
| latest print Q2 2010 (2010-07-29 to 2010-10-22) | 13 | +97.7% | +73.9% to +107.0% | 13 | 13 | +51.8% | 13 |
| latest print Q3 2010 (2010-10-28 to 2010-12-31) | 10 | +82.1% | +71.8% to +86.3% | 10 | 10 | +47.0% | 10 |

- **CHEAP held on all 52 dates, every one by clearing the hurdle and beating SPY.** Entries at $15.34-22.18 (12-19x the standing EPS,
  19-47% under the 23x floor) returned +50.8% to +107.0% over two years against SPY's +15.7% to +38.6%, ahead by 35-78pp; over three
  years (to December 2013) +115% to +168% (median +143.5%). Every 2010 entry sat through the same 26% fall, from the May 2011 high
  to the August 2011 low.
- **The calls ranked nothing within the year:** the entry price ranks the two-year return at Spearman +0.02 and the return to the m12-24
  average price at -0.21; the proxy composite at +0.36. The re-rating lifted every entry.
- **The two-year price landed nearest BASE on 32 dates and BEAR on 20,** at 2.06-3.13 times the BEAR price, 0.54-0.77 times BASE and
  0.17-0.24 times BULL.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +78.1% | +60.4% to +144.1% | 52 | 52 | +58.6% | 52 |
| FY10E: FY09's $1.26 stands (2011-01-07 to 2011-02-11) | 6 | +75.8% | +65.6% to +78.1% | 6 | 6 | +42.7% | 6 |
| FY11E: FY10's $1.31 stands (2011-02-17 to 2011-12-30) | 46 | +88.2% | +60.4% to +144.1% | 46 | 46 | +61.4% | 46 |
| latest print Q3 2010 (2011-01-07 to 2011-02-11) | 6 | +75.8% | +65.6% to +78.1% | 6 | 6 | +42.7% | 6 |
| latest print Q4 2010 (2011-02-17 to 2011-04-29) | 11 | +69.3% | +60.4% to +73.8% | 11 | 11 | +38.6% | 11 |
| latest print Q1 2011 (2011-05-05 to 2011-07-29) | 13 | +73.7% | +63.0% to +88.2% | 13 | 13 | +53.1% | 13 |
| latest print Q2 2011 (2011-08-04 to 2011-10-28) | 13 | +108.4% | +99.1% to +123.1% | 13 | 13 | +87.9% | 13 |
| latest print Q3 2011 (2011-11-03 to 2011-12-30) | 9 | +119.5% | +114.4% to +144.1% | 9 | 9 | +83.1% | 9 |

- **CHEAP held on all 52, again by clearing the hurdle and beating SPY.** The entries returned +60.4% to +144.1% over two years against
  SPY's +16.9% to +60.6%, ahead by 38-84pp; the 22 entries from 2011-08-04 ($19.96-24.33), during and after the August 2011 fall, did best (+99% to +144%). Over three years
  (to December 2014) +104% to +184% (median +137.0%).
- **The NBCUniversal-inflated BASE did not carry the call.** BASE ran at +35% to +58%/yr on NBCUniversal in growth, but the sensitivity
  with the releases' pro forma growth moves no 2011 class: the price under the floor did the work.
- **Within the year the entry price ranks the outcome** (Spearman -0.78 for both the two-year return and the m12-24 average price),
  and so do Ratio B (-0.87) and the adjusted gap (+0.85), with the right signs; the proxy composite (-0.03) does not.
- **The two-year price landed nearest BASE on 33 dates and BEAR on 19.**

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +73.3% | +41.5% to +112.4% | 52 | 51 | +53.5% | 52 |
| FY11E: FY10's $1.31 stands (2012-01-06 to 2012-02-10) | 6 | +110.9% | +99.6% to +112.4% | 6 | 6 | +68.6% | 6 |
| FY12E: FY11's $1.58 stands (2012-02-16 to 2012-12-28) | 46 | +69.9% | +41.5% to +92.4% | 46 | 45 | +53.0% | 46 |
| latest print Q3 2011 (2012-01-06 to 2012-02-10) | 6 | +110.9% | +99.6% to +112.4% | 6 | 6 | +68.6% | 6 |
| latest print Q4 2011 (2012-02-16 to 2012-04-27) | 11 | +74.8% | +67.6% to +92.4% | 11 | 11 | +55.4% | 11 |
| latest print Q1 2012 (2012-05-03 to 2012-07-27) | 13 | +76.3% | +73.3% to +87.5% | 13 | 13 | +56.1% | 13 |
| latest print Q2 2012 (2012-08-02 to 2012-10-19) | 12 | +61.0% | +41.5% to +67.8% | 12 | 12 | +45.0% | 12 |
| latest print Q3 2012 (2012-10-26 to 2012-12-28) | 10 | +57.2% | +48.8% to +63.8% | 10 | 9 | +42.7% | 10 |

- **CHEAP held on all 52, though the price was now above the floor.** From the Q4 2011 print the stock was 19-59% above a 15x floor at the
  39th-53rd percentile of its window; the CHEAP class came from Ratio B (0.07-0.29, the BULL case from 2004's EPS) and the adjusted gap.
  The entries returned +41.5% to +112.4% over two years; every one cleared the hurdle and 51 beat SPY (one lagged by 0.3pp). Three-year
  returns (to December 2015) +58.6% to +133.1% (median +99.2%).
- **The window's 2004-2005 multiples carried these calls.** The diagnostic with the history and window from 2006 (retro/README.md, "CMCSA
  2010-2013") turns 45 of the dates from August 2012 on to RICH and 17 to FAIR; as moved, 14 of its 71 moved dates would have held, against
  71 of 71 as built. The same multiples that made 2008's floor too high made 2012's class right. Hypothesis, never a rule: a window that
  keeps a depressed-earnings era reads a re-rating as cheapness for years after it; whether that helps or hurts depends on the re-rating,
  so test it across tickers.
- **Within the year the entry price ranks the outcome at Spearman -0.95** (m12-24) and -0.93 (two-year return); the EPP gap at -0.95, the
  adjusted gap at +0.82 and the proxy composite at +0.62, all the right signs.
- **The two-year price landed nearest BASE on 41 dates and BEAR on 11.**

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 40 | +46.3% | +30.4% to +56.5% | 39 | 40 | +33.2% | 40 |
| class FAIR, legacy tier BUY | 9 | +31.7% | +22.0% to +35.4% | 4 | 9 | +21.3% | 9 |
| class RICH, legacy tier BUY | 4 | +14.3% | +12.3% to +27.2% | 0 | 1 | +15.9% | 3 |
| FY12E: FY11's $1.58 stands (2013-01-04 to 2013-02-08) | 6 | +50.7% | +42.0% to +54.5% | 6 | 6 | +38.6% | 6 |
| FY13E: FY12's $1.93 stands (2013-02-14 to 2013-12-31) | 47 | +39.9% | +12.3% to +56.5% | 37 | 44 | +30.5% | 46 |
| latest print Q3 2012 (2013-01-04 to 2013-02-08) | 6 | +50.7% | +42.0% to +54.5% | 6 | 6 | +38.6% | 6 |
| latest print Q4 2012 (2013-02-14 to 2013-04-26) | 11 | +48.4% | +37.3% to +52.5% | 11 | 11 | +33.0% | 11 |
| latest print Q1 2013 (2013-05-02 to 2013-07-26) | 13 | +46.7% | +36.9% to +56.5% | 13 | 13 | +32.9% | 13 |
| latest print Q2 2013 (2013-08-01 to 2013-10-25) | 13 | +35.3% | +30.4% to +42.6% | 12 | 13 | +28.7% | 13 |
| latest print Q3 2013 (2013-10-31 to 2013-12-31) | 10 | +27.2% | +12.3% to +35.4% | 1 | 7 | +19.6% | 9 |

- **The classes ordered the outcomes.** CHEAP ($38.07-45.84) returned +30.4% to +56.5% over two years and held on all 40; FAIR
  ($46.06-49.52, 40-51% above the floor) +22.0% to +35.4%, within 4-13pp of SPY, held on all 9; RICH ($49.87-51.97) +12.3% to +27.2% and
  held on 3 of 4 (2013-11-29 beat SPY by 7.1pp). The RICH dates still gained 12-27%: they held on the relative test, not as a call to
  sell. Over three years (to December 2016) every 2013 date beat SPY and 28 of 53 cleared the hurdle.
- **Entry price ranks the outcome at Spearman -0.87** (two-year return) and -0.92 (m12-24); the EPP gap at -0.85 and the adjusted gap at
  +0.85; the proxy composite at -0.40, the wrong sign.
- **The two-year price landed nearest BASE on all 53 dates,** at 1.06-1.50 times the BASE price and 0.45-0.55 times BULL.

## The encoding calls, seen afterwards

In 2008-2009 no judgement call recorded in retro/README.md ("CMCSA") moves a class or a tier: GAAP or company-adjusted EPS, the 2004-2005 adjusted
income, the FY2007 one-sided bound read as a point, the FY2008 guide used or not, and every signal at its BEAR or XBULL value leave all 105 dates CHEAP
and BUY, and a window starting in 2006 leaves the 46 dates it can be built on (from 2009-02-19) unchanged. Across them the call held on 87 (35 in 2008, 52 in 2009). All 18 misses are 2008
entries: 14 between February and early October at $18.33-22.50, near the floor that 2004-2005's GAAP multiples set, which lagged SPY by
up to 7.9pp, and 4 in October-November that gained 20-29% but lagged SPY's rebound. What decided the outcomes was where the stock entered
the crash; the floor's anchoring on a depressed-EPS base and the unbounded BULL growth are hypotheses to test across tickers, never a
reason to re-encode CMCSA.

In 2010-2013 the calls held on 208 of 209 dates (52, 52, 52 and 52 of 53). No 2010-2013 judgement call moves many classes: the
releases' pro forma growth moves 2 (both would still have held as FAIR), GAAP EPS 16 (15 held as built, 14 would as moved), 2009 at GAAP
1; every signal at its BEAR value moves 56 dates that all held as built and of which 19 would have held as moved. The diagnostic window
from 2006 moves 71 (all held as built, 14 would as moved). Across all 314 dates the call held on 295 (35, 52, 52, 52, 52 and 52), and
18 of the 19 misses are 2008 entries: the depressed-earnings window that set 2008's floor too high is the one that kept 2010-2013 CHEAP through the
re-rating. Both are hypotheses to test across tickers, never a reason to re-encode CMCSA.
