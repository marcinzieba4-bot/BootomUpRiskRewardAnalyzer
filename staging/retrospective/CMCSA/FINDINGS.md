# CMCSA retrospective findings (hindsight)

Patterns seen in `outcome.json` for the CMCSA weekly dates: 732 from 2008-01-04 to 2021-12-31, all Comcast Corporation (Nasdaq: CMCSA,
the Class A shares). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored
only after its point-in-time build was committed and pushed (2008-2009: 573d484; 2010-2013: 99b3102; 2014-2017: 33c01d6; 2018-2021: 5e0e68d). Outcomes were
computed on 2026-11-11 from the closes posted to 2026-11-10; every date has its 6-month, 1-, 2- and 3-year horizons (the last ends
2024-12-30). Total returns include the quarterly dividends from April 2008 ($0.0625, then $0.0675, $0.0945, $0.1125, $0.1625, $0.195,
$0.225, $0.25, $0.275 and $0.315 before the 2017 split, then $0.1575, $0.19, $0.21, $0.23 and $0.25 to 2021, and the later rates); every price and dividend is on the as-traded basis of its
own model's date (Yahoo's series times its factors after that date: the 2017 split for dates before 2017-02-21, the 2026 factor for
all). Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years. "Call held" is
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

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 38 | +25.0% | +15.2% to +32.3% | 2 | 38 | +14.0% | 38 |
| class FAIR, legacy tier BUY | 10 | +22.4% | +8.6% to +26.3% | 0 | 9 | +9.4% | 9 |
| class RICH, legacy tier BUY | 4 | +9.2% | +4.2% to +13.7% | 0 | 0 | +12.4% | 4 |
| FY2013E: FY12's $1.93 stands (2014-01-03 to 2014-01-24) | 4 | +9.2% | +4.2% to +13.7% | 0 | 0 | +12.4% | 4 |
| FY2014E: FY13's $2.47 stands (2014-01-29 to 2014-12-26) | 48 | +24.2% | +8.6% to +32.3% | 2 | 47 | +13.3% | 47 |
| latest print Q3 2013 (2014-01-03 to 2014-01-24) | 4 | +9.2% | +4.2% to +13.7% | 0 | 0 | +12.4% | 4 |
| latest print Q4 2013 (2014-01-29 to 2014-04-17) | 12 | +20.7% | +8.6% to +32.2% | 1 | 11 | +16.2% | 12 |
| latest print Q1 2014 (2014-04-23 to 2014-07-18) | 13 | +23.1% | +19.0% to +27.4% | 0 | 13 | +13.7% | 13 |
| latest print Q2 2014 (2014-07-23 to 2014-10-17) | 13 | +27.0% | +18.7% to +32.3% | 1 | 13 | +11.8% | 13 |
| latest print Q3 2014 (2014-10-24 to 2014-12-26) | 10 | +25.5% | +15.2% to +29.9% | 0 | 10 | +12.3% | 9 |

- **The classes ordered the outcomes and held on 51 of 52.** CHEAP ($47.96-55.35) returned +15.2% to +32.3% over two years and beat SPY
  (+6.2% to +17.9%) on all 38, by 5.9-19.2pp, though only 2 cleared the hurdle; FAIR ($53.06-58.39) +8.6% to +26.3%, within 15pp of SPY on
  9 of 10 (2014-12-05 beat it by 15.2pp); the four January RICH dates ($51.07-53.54, on FY12's stand-in EPS) +4.2% to +13.7%, lagging SPY
  by 1.8-2.9pp. Over three years (to 2017) every CHEAP date beat SPY and 21 of 38 cleared the three-year hurdle.
- **A modest year for an absolute call:** CHEAP at the 52nd-65th percentile of its own range, 29-49% above the floor, was a relative call
  that held; the two-year price landed nearest BASE on all 52 dates (0.95-1.34 times the BASE price, 0.37-0.55 times BULL).
- **Within the year the entry price ranks the m12-24 return at Spearman -0.85** and the EPP gap at -0.86, but barely the two-year return
  (-0.09); the adjusted gap ranks it at +0.48 (the right sign), the proxy composite at +0.22.

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 35 | +37.9% | +23.2% to +51.2% | 25 | 31 | +22.2% | 32 |
| class FAIR, legacy tier BUY | 18 | +29.6% | +17.6% to +45.7% | 4 | 13 | +14.8% | 13 |
| FY2014E: FY13's $2.47 stands (2015-01-02 to 2015-02-20) | 8 | +32.3% | +24.5% to +45.7% | 4 | 8 | +12.9% | 3 |
| FY2015E: FY14's $2.93 stands (2015-02-25 to 2015-12-31) | 45 | +33.1% | +17.6% to +51.2% | 25 | 36 | +21.2% | 42 |
| latest print Q3 2014 (2015-01-02 to 2015-02-20) | 8 | +32.3% | +24.5% to +45.7% | 4 | 8 | +12.9% | 3 |
| latest print Q4 2014 (2015-02-25 to 2015-05-01) | 10 | +31.1% | +27.5% to +37.9% | 3 | 10 | +14.3% | 10 |
| latest print Q1 2015 (2015-05-05 to 2015-07-17) | 11 | +40.2% | +25.5% to +46.1% | 8 | 11 | +18.7% | 11 |
| latest print Q2 2015 (2015-07-24 to 2015-10-23) | 14 | +38.0% | +21.6% to +51.2% | 9 | 10 | +27.1% | 12 |
| latest print Q3 2015 (2015-10-28 to 2015-12-31) | 10 | +36.5% | +17.6% to +46.3% | 5 | 5 | +25.8% | 9 |

- **CHEAP held on 32 of 35:** +23.2% to +51.2% over two years, 25 cleared the hurdle; the three misses (2015-10-09, 2015-10-16,
  2015-11-13) gained 23-29% but lagged SPY's 2016-2017 rally by 1.9-7.0pp. Over three years (to 2018) the CHEAP dates returned only
  +11.9% to +38.1% and 2 beat SPY.
- **FAIR missed on 5 of 18, all by doing too well:** the January-February dates ($53.15-59.62, on FY13's $2.47 before the Q4 2014 print)
  returned +24.5% to +45.7% and beat SPY by 11.4-27.2pp, five of them by more than the 15pp the FAIR band allows. The ten FAIR dates of
  July and October-November ($61.59-64.27) landed within the band (-10.2 to +8.7pp).
- **The adjusted gap ranks the outcome:** Spearman +0.72 for the two-year return and +0.81 for m12-24; the entry price -0.67 and -0.30;
  the proxy composite +0.15 and -0.14. Every two-year price landed nearest BASE.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 24 | +23.9% | +7.2% to +61.9% | 8 | 4 | +29.5% | 8 |
| class FAIR, legacy tier ACCUMULATE | 1 | +19.4% | +19.4% to +19.4% | 0 | 0 | +8.3% | 1 |
| class FAIR, legacy tier BUY | 3 | +4.9% | +2.2% to +6.1% | 0 | 0 | +19.4% | 0 |
| class RICH, legacy tier ACCUMULATE | 19 | +10.3% | +3.0% to +17.3% | 0 | 0 | +9.4% | 19 |
| class RICH, legacy tier BUY | 1 | +16.5% | +16.5% to +16.5% | 0 | 0 | +12.2% | 1 |
| class RICH, legacy tier WATCHLIST | 4 | +11.6% | -0.7% to +12.0% | 0 | 0 | +3.8% | 4 |
| FY2015E: FY14's $2.93 stands (2016-01-08 to 2016-01-29) | 4 | +59.3% | +52.4% to +61.9% | 4 | 4 | +40.8% | 4 |
| FY2016E: FY15's $3.25 stands (2016-02-04 to 2016-12-30) | 48 | +12.6% | -0.7% to +45.3% | 4 | 0 | +13.5% | 29 |
| latest print Q3 2015 (2016-01-08 to 2016-01-29) | 4 | +59.3% | +52.4% to +61.9% | 4 | 4 | +40.8% | 4 |
| latest print Q4 2015 (2016-02-04 to 2016-04-22) | 12 | +26.1% | +10.6% to +45.3% | 4 | 0 | +30.4% | 4 |
| latest print Q1 2016 (2016-04-28 to 2016-07-22) | 13 | +7.2% | +2.2% to +13.7% | 0 | 0 | +19.7% | 4 |
| latest print Q2 2016 (2016-07-28 to 2016-10-21) | 13 | +11.3% | +7.2% to +16.7% | 0 | 0 | +9.5% | 13 |
| latest print Q3 2016 (2016-10-27 to 2016-12-30) | 10 | +16.9% | -0.7% to +28.6% | 0 | 0 | +4.8% | 8 |

- **The worst year for the calls: 33 of 52 held.** The eight CHEAP dates of January-February ($53.89-58.21, at the early-2016 low)
  returned +39.9% to +61.9% and cleared the hurdle. The 14 CHEAP dates of March-June ($59.16-62.37) and the 3 FAIR dates of May-June
  ($62.80-63.56) returned +2.2% to +29.5% over two years against SPY's +31.6% to +42.1%: the two-year endpoint fell in the first half of
  2018 ($66-73 on the pre-split basis), after the high of 2018-01-24 ($85.98), so none held, though the m12-24 average price was 19-32% above entry. The two CHEAP
  dates after the Rio-Olympics print (2016-10-27 and 2016-11-04, BASE at +16.8%/yr on the Olympics quarter) also lagged SPY by 6.5-10.1pp:
  the sensitivity without the Olympics quarter's growth files 2016-10-27 FAIR.
- **RICH held on all 24 from July 2016** ($64.06-70.65): -0.7% to +17.3% over two years against SPY's +11.0% to +40.3%, lagging by
  9.1-30.1pp; the m12-24 average price was only 1.6-13.5% above entry. The class's turn to RICH came with 2005 leaving the history
  (BULL from +29% to +21%/yr), a mechanical change that the outcome agreed with.
- **Entry price ranks the m12-24 return at Spearman -0.98,** Ratio B at -0.98, the EPP gap at -0.95 and the adjusted gap at +0.80, all the
  right signs; the proxy composite at -0.26.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 24 | +13.6% | +1.1% to +20.3% | 0 | 0 | -2.9% | 24 |
| class RICH, legacy tier WATCHLIST | 28 | +15.0% | -2.1% to +31.0% | 0 | 11 | -2.2% | 17 |
| FY2016E: FY15's $3.25 stands (2017-01-06 to 2017-01-20) | 3 | +2.2% | +1.8% to +5.9% | 0 | 0 | -2.2% | 3 |
| FY2017E: FY16's $3.48 stands (2017-01-27 to 2017-02-17) | 4 | +3.8% | -2.1% to +4.0% | 0 | 0 | -6.4% | 4 |
| FY2017E: FY16's $1.74 stands (2017-02-24 to 2017-12-29) | 45 | +14.7% | +1.1% to +31.0% | 0 | 11 | -2.5% | 34 |
| latest print Q3 2016 (2017-01-06 to 2017-01-20) | 3 | +2.2% | +1.8% to +5.9% | 0 | 0 | -2.2% | 3 |
| latest print Q4 2016 (2017-01-27 to 2017-04-21) | 13 | +8.8% | -2.1% to +15.1% | 0 | 0 | -5.9% | 13 |
| latest print Q1 2017 (2017-04-28 to 2017-07-21) | 13 | +13.9% | +1.1% to +17.7% | 0 | 0 | -6.2% | 13 |
| latest print Q2 2017 (2017-07-28 to 2017-10-20) | 13 | +20.3% | +8.1% to +31.0% | 0 | 6 | +3.6% | 7 |
| latest print Q3 2017 (2017-10-27 to 2017-12-29) | 10 | +26.8% | +11.9% to +29.8% | 0 | 5 | +11.3% | 5 |

- **RICH held on 41 of 52.** The 34 dates of January-August ($70.27-75.95 before the split, $37.14-41.99 after) returned -2.1% to +17.7% and
  lagged SPY by 8.4-22.5pp; their m12-24 average price was 11.5% under to 1.6% over entry, through the 2018 fall (a 28.8% drawdown within
  two years on every 2017 date). The 11 misses (2017-09-08 to 2017-11-24, $35.68-38.21) gained 21.7-31.0% to the 2019 recovery and beat
  SPY by 0.1-10.5pp, while staying under the hurdle: the RICH calls were right about the hurdle on every date and wrong about SPY on 11.
- **The BULL case was low enough to be reached:** the two-year price landed nearest BULL on 29 dates (0.75-1.00 times it), the first
  CMCSA year where it did, after 2005 left the history.
- Within the year the entry price ranks the two-year return at Spearman -0.73 and the proxy composite ranks the m12-24 return at +0.76.

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 26 | +25.1% | +5.9% to +54.3% | 6 | 25 | +26.7% | 26 |
| class FAIR, legacy tier BUY | 2 | +53.8% | +28.0% to +53.8% | 1 | 1 | +24.8% | 2 |
| class RICH, legacy tier ACCUMULATE | 4 | +20.1% | +9.0% to +33.2% | 1 | 0 | +8.9% | 3 |
| class RICH, legacy tier AVOID | 3 | +13.1% | +9.8% to +15.5% | 0 | 0 | +0.5% | 3 |
| class RICH, legacy tier BUY | 16 | +27.0% | +5.1% to +45.0% | 4 | 9 | +13.8% | 4 |
| class RICH, legacy tier WATCHLIST | 1 | +9.6% | +9.6% to +9.6% | 0 | 0 | +1.8% | 1 |
| FY2017E: FY16's $1.74 stands (2018-01-05 to 2018-01-19) | 3 | +13.1% | +9.8% to +15.5% | 0 | 0 | +0.5% | 3 |
| FY2018E: FY17's $2.06 stands (2018-01-25 to 2018-12-28) | 49 | +25.0% | +5.1% to +54.3% | 12 | 35 | +20.0% | 36 |
| latest print Q3 2017 (2018-01-05 to 2018-01-19) | 3 | +13.1% | +9.8% to +15.5% | 0 | 0 | +0.5% | 3 |
| latest print Q4 2017 (2018-01-25 to 2018-04-20) | 13 | +11.0% | +5.1% to +20.9% | 0 | 8 | +19.3% | 10 |
| latest print Q1 2018 (2018-04-26 to 2018-07-20) | 13 | +22.4% | +16.4% to +39.5% | 2 | 13 | +29.0% | 13 |
| latest print Q2 2018 (2018-07-27 to 2018-10-19) | 13 | +27.4% | +22.3% to +37.8% | 3 | 13 | +18.3% | 8 |
| latest print Q3 2018 (2018-10-26 to 2018-12-28) | 10 | +37.8% | +14.5% to +54.3% | 7 | 1 | +13.5% | 5 |

- **The classes held on 39 of 52.** CHEAP held on all 26 (late March to mid-August 2018, three dates of late September-October and 2018-12-21, $31.26-35.60): +5.9% to
  +54.3% over two years, beating SPY on 25 by up to 19.4pp; over three years every CHEAP date cleared the three-year hurdle and 24 beat
  SPY. The two FAIR dates (2018-10-19 and 2018-12-28) returned +28.0% and +53.8%, within 1pp of SPY.
- **RICH held on 11 of 24.** The three January dates (on FY16's stand-in EPS) gained 9.8-15.5% and lagged SPY. The 13 misses are entries
  at 17-19x FY17's $2.06: three in March 2018 and five in late August-September that beat SPY by 0.4-14.1pp (their two-year endpoints fell
  in the March 2020 and autumn 2020 markets), and five in November-December that cleared the hurdle (+32.8% to +45.0%) by the end of
  2020.
- **Within the year the entry price ranks the m12-24 return at Spearman -0.99** and the adjusted gap at +0.95, but barely the two-year
  point return (-0.13); the proxy composite ranks neither.

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 49 | +35.6% | +13.8% to +49.9% | 31 | 4 | +16.1% | 31 |
| class RICH, legacy tier BUY | 3 | +45.3% | +39.3% to +49.5% | 3 | 0 | +19.9% | 0 |
| FY2018E: FY17's $2.06 stands (2019-01-04 to 2019-01-18) | 3 | +45.3% | +39.3% to +49.5% | 3 | 0 | +19.9% | 0 |
| FY2019E: FY18's $2.55 stands (2019-01-24 to 2019-12-27) | 49 | +35.6% | +13.8% to +49.9% | 31 | 4 | +16.1% | 31 |
| latest print Q3 2018 (2019-01-04 to 2019-01-18) | 3 | +45.3% | +39.3% to +49.5% | 3 | 0 | +19.9% | 0 |
| latest print Q4 2018 (2019-01-24 to 2019-04-18) | 13 | +42.4% | +33.5% to +49.9% | 13 | 4 | +13.5% | 13 |
| latest print Q1 2019 (2019-04-26 to 2019-07-19) | 13 | +35.6% | +30.3% to +44.2% | 11 | 0 | +13.6% | 11 |
| latest print Q2 2019 (2019-07-26 to 2019-10-18) | 13 | +35.6% | +18.8% to +45.3% | 7 | 0 | +18.9% | 7 |
| latest print Q3 2019 (2019-10-25 to 2019-12-27) | 10 | +21.0% | +13.8% to +24.0% | 0 | 0 | +23.2% | 0 |

- **Held on 31 of 52.** From the Q4 2018 print every date was CHEAP, BASE carrying Sky's acquisition growth (+20-29%/yr). The 49 CHEAP
  dates ($36.24-46.88) returned +13.8% to +49.9% over two years (median +35.6%) and 31 cleared the hurdle, but only 4 beat SPY (+42.7% to
  +61.0% over the same two years). The 18 misses are entries of late April-May and September-December 2019 ($43.08-46.88) that gained
  13.8-31.8% and lagged SPY by 15.9-36.8pp. Over three years (to 2022) no CHEAP date beat SPY or cleared the three-year hurdle.
- The three January RICH dates (FY17's $2.06, before the Q4 2018 print) gained 39.3-49.5%: misses, clearing the hurdle while lagging SPY
  by 1.1-5.9pp. The two-year price landed nearest BASE on 43 of the 49 CHEAP dates and nearest BEAR on 6.
- Within the year the entry price ranks the two-year return at Spearman -0.79; the adjusted gap +0.28, the proxy composite -0.20.

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 30 | +16.5% | -19.5% to +46.3% | 3 | 0 | +30.9% | 3 |
| class FAIR, legacy tier BUY | 1 | +7.0% | +7.0% to +7.0% | 0 | 0 | +18.7% | 0 |
| class RICH, legacy tier BUY | 22 | -26.2% | -30.6% to -4.0% | 0 | 0 | -1.2% | 22 |
| FY2019E: FY18's $2.55 stands (2020-01-03 to 2020-01-17) | 3 | +16.6% | +12.8% to +16.9% | 0 | 0 | +21.7% | 0 |
| FY2020E: FY19's $2.83 stands (2020-01-24 to 2020-12-31) | 50 | +3.6% | -30.6% to +46.3% | 3 | 0 | +18.7% | 25 |
| latest print Q3 2019 (2020-01-03 to 2020-01-17) | 3 | +16.6% | +12.8% to +16.9% | 0 | 0 | +21.7% | 0 |
| latest print Q4 2019 (2020-01-24 to 2020-04-24) | 14 | +21.7% | +6.0% to +46.3% | 3 | 0 | +37.7% | 3 |
| latest print Q1 2020 (2020-05-01 to 2020-07-24) | 13 | +7.5% | +1.7% to +20.9% | 0 | 0 | +30.4% | 0 |
| latest print Q2 2020 (2020-07-31 to 2020-10-23) | 13 | -16.2% | -30.6% to -4.0% | 0 | 0 | +4.1% | 13 |
| latest print Q3 2020 (2020-10-30 to 2020-12-31) | 10 | -26.4% | -29.4% to -19.5% | 0 | 0 | -19.3% | 9 |

- **The worst year for the calls: 25 of 53 held.** The 30 CHEAP dates (January to July 2020 and 2020-10-30, $33.37-47.50, on FY18's $2.55
  in January and FY19's GAAP $2.83 from the Q4 2019 print, through the COVID fall) returned -19.5% to +46.3% over two years (median +16.5%) and beat SPY on none; only the three entries at
  the March-April 2020 low (2020-03-20, 2020-03-27, 2020-04-03; +41.9% to +46.3%) cleared the hurdle. Their m12-24 average price was 2.3%
  to 61.7% above entry (median +30.9%): the stock rose into 2021 and gave it back by the two-year endpoints of 2022. The FAIR date
  (2020-02-14) returned +7.0%, 26.4pp behind SPY: a miss.
- **RICH held on all 22,** from the Q2 2020 print, when BASE turned negative (-9.4%/yr, then -2.5%): $42.80-52.40 entries lost 4.0-30.6%
  over two years against SPY's +5.5% to +30.2%, the two-year price nearest BEAR on 20, a 39-54% drawdown within two years.
- **The adjusted gap ranks the outcome:** Spearman +0.92 for the two-year return and +0.94 for m12-24; the entry price -0.75 and -0.90; the
  proxy composite +0.77 and +0.68.

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 49 | -20.9% | -34.5% to -4.2% | 0 | 0 | -31.6% | 49 |
| class RICH, legacy tier BUY | 3 | -15.8% | -22.4% to -14.9% | 0 | 0 | -18.6% | 3 |
| FY2020E: FY19's $2.83 stands (2021-01-08 to 2021-01-22) | 3 | -15.8% | -22.4% to -14.9% | 0 | 0 | -18.6% | 3 |
| FY2021E: FY20's $2.28 stands (2021-01-29 to 2021-12-31) | 49 | -20.9% | -34.5% to -4.2% | 0 | 0 | -31.6% | 49 |
| latest print Q3 2020 (2021-01-08 to 2021-01-22) | 3 | -15.8% | -22.4% to -14.9% | 0 | 0 | -18.6% | 3 |
| latest print Q4 2020 (2021-01-29 to 2021-04-23) | 13 | -26.7% | -34.5% to -15.9% | 0 | 0 | -30.0% | 13 |
| latest print Q1 2021 (2021-04-30 to 2021-07-23) | 13 | -25.2% | -27.9% to -21.4% | 0 | 0 | -35.5% | 13 |
| latest print Q2 2021 (2021-07-30 to 2021-10-22) | 13 | -18.8% | -22.4% to -14.8% | 0 | 0 | -35.8% | 13 |
| latest print Q3 2021 (2021-10-29 to 2021-12-31) | 10 | -12.4% | -18.6% to -4.2% | 0 | 0 | -20.7% | 10 |

- **RICH held on all 52.** From the Q4 2020 print the class stood on FY20's GAAP $2.28, the COVID year, as current-year EPS: entries at
  $48.45-61.72 lost 4.2-34.5% over two years (median -20.9%) and lagged SPY by 9.0-37.1pp; the m12-24 average price was 15.8-38.6% under
  entry, the three-year return -30.6% to -0.4%, the drawdown within two years 44.5-53.6%. The three January dates before the print (BUY,
  on FY19's $2.83) lost 14.9-22.4%.
- Within the year Ratio B ranks the two-year return at Spearman -0.89 and the entry price ranks the m12-24 return at -0.98.

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

In 2014-2017 the calls held on 170 of 209 dates (51, 45, 33 and 41), and the classes ordered the outcomes: CHEAP held on 78 of 97 (median
two-year return +28.6%, +10.5pp over SPY), FAIR on 23 of 32 (+24.5%, +7.6pp) and RICH on 69 of 80 (+11.8%, -12.6pp). The judgement calls,
scored afterwards: GAAP EPS moves 33 classes, of which 19 held as built and 25 would have held as moved (176 of 209 in all, against 170);
the history from 2004 in every vintage moves 26 (15 held as built, 17 as moved); the growth excluding the Olympics and the Super Bowl
moves 5 (1 and 2); every signal at its BEAR value moves 124 (96 held as built, 42 as moved) and at its XBULL value 73 (60 and 30). No
call's moved set would have done much better, and the signal extremes would have done far worse. The STREAMING watch list (126 dates from
2015-08-07) changed no class; the calls on those dates held on 93. The mechanical turn of 2016, when 2005's $0.25 left the history and
BULL fell from +29% to +21%/yr, is what took the class from CHEAP to RICH; the RICH calls held on 69 of 80, the misses being late-2017
entries that beat SPY's return to the 2019 recovery. Across all 523 dates the call held on 465. Hypotheses only, never a reason to
re-encode CMCSA: a history whose first year is a depressed base keeps BULL high and the class CHEAP until that year leaves the window,
and the ten-year cut then moves the class by itself, whatever the business did that quarter.

In 2018-2021 the calls held on 147 of 209 dates (39, 31, 25 and 52), and the classes ordered the absolute outcomes: CHEAP held on 60 of
105 (median two-year return +27.0%, -15.7pp against SPY), FAIR on 2 of 3, RICH on 85 of 101 (-17.6%, -25.0pp). The CHEAP calls of
2019-2020 rose but lagged SPY's 2019-2021 run: the class ranks CMCSA against its own history, and CHEAP rarely beat the market here. The
judgement calls, scored afterwards: Sky's pro forma growth moves 41 classes, of which 20 held as built and 22 would have held as moved (149
of 209 in all, against 147); every signal at its BEAR value moves 68 (33 held as built, 36 as moved; 150 in all) and at its XBULL value
54 (37 and 21; 131); the history from 2004 moves 27 (14 and 14); the company's redefined Adjusted EPS 20 (19 and 6; 134); GAAP throughout
15 (9 and 6; 144); the growth without the Olympics 5 (5 and 2). No call's moved set would have done much better, and the redefined figure
would have done worse. The STREAMING watch list (all 209 dates) changed no class. Across all 732 dates the call held on 612. Hypotheses
only, never a reason to re-encode CMCSA: a CHEAP class carried by acquired growth (Sky here, NBCUniversal in 2011) cleared the hurdle more
often than it beat the market, and a depressed latest year standing as current-year EPS (2020) put the class at RICH ahead of a fall.
