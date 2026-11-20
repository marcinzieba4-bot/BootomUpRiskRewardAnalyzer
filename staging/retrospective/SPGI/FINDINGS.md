# SPGI retrospective findings (hindsight)

Patterns seen in `outcome.json` for the SPGI weekly dates: 314 from 2008-01-04 to 2013-12-31, The McGraw-Hill Companies, Inc. (NYSE:
MHP; SPGI is the series key), McGraw Hill Financial, Inc. from 2013-05-06 and NYSE: MHFI from 2013-05-14. They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was
scored only after its point-in-time build and its firewall result were committed (2008-2009: 7a7b5ac, firewall e1db42b); the push of those
two commits followed a few minutes after the outcome computation began, and no committed file changed in between. Outcomes were computed
on 2026-11-20; every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2016-12-30). 2010-2013 was scored only after
its build (51cf532) and its firewall result (23e3e2c) were committed and pushed; that batch was decided in the session that had written
the 2008-2009 sections below (disclosed in retro/README.md, "SPGI 2010-2013"). Total returns include the quarterly
dividends as Yahoo records them (ex-dates); no split falls in any horizon, so every price is as traded. Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over
two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY).

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | -12.5% | -34.3% to +83.2% | 13 | 29 | -20.6% | 29 |
| FY07E: FY06's $2.40 stands (2008-01-04 to 2008-01-18) | 3 | -13.3% | -16.8% to -9.3% | 0 | 2 | -31.3% | 2 |
| FY08E: $3.11, +3-5% on FY07's $2.99 (2008-01-25 to 2008-04-25) | 14 | -5.6% | -16.2% to +3.5% | 0 | 12 | -20.8% | 12 |
| FY08E: $2.65-2.75, midpoint $2.70 (2008-04-30 to 2008-10-24) | 26 | -22.5% | -34.3% to +83.2% | 3 | 5 | -22.2% | 5 |
| FY08E: $2.63-2.65, midpoint $2.64 (2008-10-29 to 2008-12-31) | 10 | +64.5% | +44.6% to +77.3% | 10 | 10 | +39.1% | 10 |
| latest print Q3 2007 (2008-01-04 to 2008-01-18) | 3 | -13.3% | -16.8% to -9.3% | 0 | 2 | -31.3% | 2 |
| latest print Q4 2007 (2008-01-25 to 2008-04-25) | 14 | -5.6% | -16.2% to +3.5% | 0 | 12 | -20.8% | 12 |
| latest print Q1 2008 (2008-04-30 to 2008-07-25) | 13 | -24.0% | -34.3% to -13.3% | 0 | 0 | -22.4% | 0 |
| latest print Q2 2008 (2008-07-30 to 2008-10-24) | 13 | -19.3% | -31.5% to +83.2% | 3 | 5 | -22.1% | 5 |
| latest print Q3 2008 (2008-10-29 to 2008-12-31) | 10 | +64.5% | +44.6% to +77.3% | 10 | 10 | +39.1% | 10 |

- **CHEAP held on 29 of 53 dates, and the print decided which.** The three January dates ($38.58-42.71, 16.1-17.8x FY06's $2.40) returned
  -16.8% to -9.3% over two years against SPY's -16.3% to -10.2%. The 14 dates from the Q4 2007 print ($35.60-44.06, 11.4-14.2x the FY08
  guide of $3.11) returned -16.2% to +3.5% and beat SPY (-18.4% to -6.8%) on 12. The 13 dates from the Q1 2008 print ($36.11-44.50,
  13.4-16.5x the $2.70 range) returned -34.3% to -13.3%, behind SPY on all 13, and the call missed on every one; the 13 from the Q2 2008
  print ranged from -31.5% (summer) to +83.2% (2008-10-24, $20.87). The 10 from the Q3 2008 print ($20.72-25.00, 7.8-9.5x the $2.64
  guide) returned +44.6% to +77.3%, cleared the hurdle and beat SPY by 8-36pp. The 36 dates to 2008-09-05 sat through a 62% drawdown to
  the low close of $17.39 on 2009-03-09.
- **The EPS anchors were met; the multiple was not.** FY08 came in at $2.51 with $0.14 of restructuring (the Q4 2008 release), so the
  $2.63-2.65 the models carried from October excluding restructuring was the company's figure, and FY09 at $2.33 (the Q4 2009 release,
  2010-01-26, outside the series) above its $2.20-2.25 guide. The CHEAP reading rested on the decade's multiples (median 21.5-22.6x,
  10th percentile 15.9-18.6x) and a floor of 17-18x lifted by GAAP 2001; the stock traded at 7.7-17.8x through 2008 and stayed 1-57% under
  the floor on every date. All 53 dates landed nearest BEAR at two years. Hypothesis, not a rule: an own-history P/E window that spans a
  credit-issuance boom overstates cheapness for a ratings franchise once issuance collapses, and a floor set by calendar-year lows of the
  boom is no floor; test on other financial-information and capital-markets franchises and periods, never fit it to SPGI.
- **The price ranked the dates; the composite less so.** Across the 53 dates the entry price ranks the two-year return at Spearman -0.90
  and the return to the m12-24 average price at -0.95; the EPP gap at -0.92 and -0.86, Ratio B at -0.95 and -0.84, the adjusted gap at
  +0.87 and +0.58; the proxy composite at +0.50 and +0.33 (2.65 on the January dates, 1.50 from the Q4 2007 print, 1.65 from Q3 2008).
  Over three years 39 of the 53 beat SPY (median +8.6%) and 13 cleared the three-year hurdle.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +46.5% | +26.5% to +126.7% | 47 | 33 | +29.7% | 51 |
| FY08E: $2.63-2.65, midpoint $2.64 (2009-01-09 to 2009-01-23) | 3 | +83.5% | +68.3% to +94.4% | 3 | 3 | +54.2% | 3 |
| FY09E: $2.20-2.30, midpoint $2.25 (2009-01-28 to 2009-07-24) | 26 | +47.2% | +27.4% to +126.7% | 25 | 8 | +21.4% | 25 |
| FY09E: $2.20-2.25, midpoint $2.225 (2009-07-29 to 2009-12-31) | 23 | +45.3% | +26.5% to +89.5% | 19 | 22 | +29.7% | 23 |
| latest print Q3 2008 (2009-01-09 to 2009-01-23) | 3 | +83.5% | +68.3% to +94.4% | 3 | 3 | +54.2% | 3 |
| latest print Q4 2008 (2009-01-28 to 2009-04-24) | 13 | +68.2% | +39.7% to +126.7% | 13 | 8 | +39.6% | 13 |
| latest print Q1 2009 (2009-04-29 to 2009-07-24) | 13 | +40.8% | +27.4% to +50.7% | 12 | 0 | +14.5% | 12 |
| latest print Q2 2009 (2009-07-29 to 2009-10-23) | 13 | +46.7% | +26.5% to +89.5% | 11 | 12 | +31.4% | 13 |
| latest print Q3 2009 (2009-10-27 to 2009-12-31) | 10 | +41.4% | +29.7% to +58.7% | 8 | 10 | +28.3% | 10 |

- **CHEAP held on 51 of 52 dates.** From the Q4 2008 print to April ($17.64-29.47, 7.8-13.1x FY09's $2.25 guide) the stock returned
  +39.7% to +126.7% over two years; SPY's rebound from its March 2009 low (+51.2% to +98.7%) beat it on 5 of those 13. The 13 dates from the
  Q1 2009 print ($29.38-33.71) returned +27.4% to +50.7% against SPY's +38.9% to +61.2%: the hurdle cleared on 12, SPY beaten on none, and
  the one miss is 2009-05-08 (+27.4%, SPY +49.1%). From the Q2 2009 print ($23.67-34.82) all 23 dates returned +26.5% to +89.5% and 22
  beat SPY. Over three years 48 of the 52 cleared the three-year hurdle (+52.1%) and 48 beat SPY (median +79.7%).
- **The two-year price landed nearest BASE on 49 dates and BEAR on 3** (BASE was the revenue guide plus the buyback, +1.0% to -4.5%/yr, at
  the window's median multiple of 20.5-21.5x: the median multiple carried the call, not the growth).
- **The composite pointed the wrong way within 2009.** The entry price ranks the two-year return at Spearman -0.88 (m12-24 -0.87), the EPP
  gap at -0.86 and -0.84, Ratio B at -0.81 and -0.72, the adjusted gap at +0.73 and +0.54; the proxy composite at -0.18 and -0.46 (1.65 on
  the Q3 2008 and Q1 2009 prints, the latter the dates that lagged SPY most; 1.45 on the others). The signals read the quarter's declines, which the price had
  already discounted at the March low.
- **Today's profile files SPGI DURABLE with risk 1** ("Ratings duopoly + indices flywheel", `profile_drift` in every outcome), where the
  point-in-time reading was DURABLE with risk 2; the kind and risk change the label only, so no price state above depends on them.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +58.4% | +35.6% to +83.0% | 52 | 52 | +34.8% | 52 |
| EPS $2.225 (2010-01-08 to 2010-01-22) | 3 | +44.5% | +41.2% to +44.9% | 3 | 3 | +23.8% | 3 |
| EPS $2.6 (2010-01-27 to 2010-10-22) | 39 | +59.4% | +35.6% to +83.0% | 39 | 39 | +44.8% | 39 |
| EPS $2.625 (2010-10-27 to 2010-12-31) | 10 | +57.1% | +38.0% to +62.8% | 10 | 10 | +34.4% | 10 |
| latest print Q3 2009 (2010-01-08 to 2010-01-22) | 3 | +44.5% | +41.2% to +44.9% | 3 | 3 | +23.8% | 3 |
| latest print Q4 2009 (2010-01-27 to 2010-04-23) | 13 | +39.1% | +35.6% to +53.6% | 13 | 13 | +20.6% | 13 |
| latest print Q1 2010 (2010-04-28 to 2010-07-16) | 12 | +64.2% | +49.2% to +69.6% | 12 | 12 | +51.6% | 12 |
| latest print Q2 2010 (2010-07-23 to 2010-10-22) | 14 | +72.0% | +58.4% to +83.0% | 14 | 14 | +49.9% | 14 |
| latest print Q3 2010 (2010-10-27 to 2010-12-31) | 10 | +57.1% | +38.0% to +62.8% | 10 | 10 | +34.4% | 10 |

- **CHEAP held on all 52 dates.** $27.34-39.31, 10.5-15.3x the standing EPS, the 5th-23rd percentile of the window and 10-38% under the
  floor: every date returned +35.6% to +83.0% over two years, cleared the hurdle and beat SPY (+15.7% to +38.6%) by 8.5-48.5pp; over three
  years the median was +109.5% (47 cleared the three-year hurdle, 50 beat SPY). Every date landed nearest BASE at two years (BASE -4.5% to
  +8.0%/yr at the window's 19.5-20.4x median): the median multiple carried the call, as in 2009. The low close of the two years was $27.02
  (2010-06-01).
- **The guides were met:** FY2010 came in at $2.69 excluding one-offs against the $2.60-2.625 the models carried (the Q4 2010 release).
- **The price ranked the dates** (Spearman -0.57 against the two-year return, -0.80 against the m12-24 average price; the EPP gap -0.61
  and -0.84); the adjusted gap (-0.01) and the proxy composite (-0.15) did not.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 49 | +50.5% | +27.3% to +93.5% | 46 | 49 | +29.8% | 49 |
| class FAIR, legacy tier BUY | 1 | +66.7% | +66.7% to +66.7% | 1 | 1 | +24.1% | 0 |
| class RICH, legacy tier BUY | 2 | +82.8% | +79.1% to +82.8% | 2 | 2 | +31.4% | 0 |
| EPS $2.625 (2011-01-07 to 2011-01-28) | 4 | +58.2% | +56.4% to +60.4% | 4 | 4 | +31.2% | 4 |
| EPS $2.84 (2011-02-02 to 2011-10-14) | 37 | +44.8% | +27.3% to +78.2% | 34 | 37 | +28.0% | 37 |
| EPS $2.835 (2011-10-21 to 2011-12-30) | 11 | +79.4% | +66.7% to +93.5% | 11 | 11 | +31.6% | 8 |
| latest print Q3 2010 (2011-01-07 to 2011-01-28) | 4 | +58.2% | +56.4% to +60.4% | 4 | 4 | +31.2% | 4 |
| latest print Q4 2010 (2011-02-02 to 2011-04-21) | 12 | +41.7% | +27.3% to +71.0% | 9 | 12 | +30.4% | 12 |
| latest print Q1 2011 (2011-04-27 to 2011-07-22) | 13 | +44.7% | +37.5% to +50.5% | 13 | 13 | +22.7% | 13 |
| latest print Q2 2011 (2011-07-29 to 2011-10-14) | 12 | +63.5% | +49.3% to +78.2% | 12 | 12 | +32.4% | 12 |
| latest print Q3 2011 (2011-10-21 to 2011-12-30) | 11 | +79.4% | +66.7% to +93.5% | 11 | 11 | +31.6% | 8 |

- **CHEAP held on all 49 CHEAP dates; the three FAIR and RICH calls missed.** The CHEAP dates ($36.75-45.29, 12.9-15.9x) returned +27.3%
  to +93.5% and beat SPY on all 49; three of them (2011-02-11 to 2011-02-25, +27.3% to +31.6%) fell short of the hurdle but beat SPY by
  10-15pp. FAIR on 2011-10-21 and RICH on 2011-12-23 and 2011-12-30 came from Q3 2011's BASE of +0.1% (revenue -2.5%, McGraw-Hill
  Education -11.1%, the Financial Services line +6.4%); those dates returned +66.7%, +79.1% and +82.8%.
- **The guides were beaten:** FY2011 came in at $2.91 excluding one-offs without Broadcasting against the $2.835-2.84 the models carried.
- **Within 2011 the price ranked the dates the other way** (Spearman +0.35 against the two-year return): the dates before the August low ($35.35 on
  2011-08-10) carried it in their two-year windows, and the later, higher-priced dates started nearer the rebound. Landing: BASE 41,
  BULL 11.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 1 | +86.9% | +86.9% to +86.9% | 1 | 1 | +54.3% | 1 |
| class CHEAP, legacy tier BUY | 29 | +84.5% | +57.8% to +107.3% | 29 | 29 | +53.1% | 29 |
| class FAIR, legacy tier ACCUMULATE | 5 | +73.3% | +68.3% to +85.0% | 5 | 5 | +50.8% | 0 |
| class FAIR, legacy tier BUY | 3 | +68.4% | +64.3% to +69.3% | 3 | 3 | +52.2% | 0 |
| class RICH, legacy tier ACCUMULATE | 7 | +67.8% | +64.3% to +75.9% | 7 | 7 | +42.2% | 0 |
| class RICH, legacy tier BUY | 2 | +78.3% | +76.3% to +78.3% | 2 | 2 | +30.0% | 0 |
| class RICH, legacy tier WATCHLIST | 5 | +57.0% | +50.3% to +74.3% | 5 | 5 | +40.5% | 0 |
| EPS $2.835 (2012-01-06 to 2012-01-27) | 4 | +76.3% | +67.3% to +78.3% | 4 | 4 | +30.0% | 0 |
| EPS $3.3 (2012-02-01 to 2012-10-26) | 39 | +73.5% | +50.3% to +107.3% | 39 | 39 | +42.2% | 27 |
| EPS $3.375 (2012-11-02 to 2012-12-28) | 9 | +75.0% | +68.3% to +89.0% | 9 | 9 | +51.5% | 3 |
| latest print Q3 2011 (2012-01-06 to 2012-01-27) | 4 | +76.3% | +67.3% to +78.3% | 4 | 4 | +30.0% | 0 |
| latest print Q4 2011 (2012-02-01 to 2012-04-20) | 12 | +77.2% | +57.8% to +87.4% | 12 | 12 | +36.4% | 11 |
| latest print Q1 2012 (2012-04-25 to 2012-07-20) | 13 | +89.3% | +61.7% to +107.3% | 13 | 13 | +58.4% | 13 |
| latest print Q2 2012 (2012-07-27 to 2012-10-26) | 14 | +68.4% | +50.3% to +84.1% | 14 | 14 | +44.4% | 3 |
| latest print Q3 2012 (2012-11-02 to 2012-12-28) | 9 | +75.0% | +68.3% to +89.0% | 9 | 9 | +51.5% | 3 |

- **CHEAP held on all 30 CHEAP dates; all 22 FAIR and RICH calls missed.** The CHEAP dates returned +57.8% to +107.3%; the FAIR and RICH
  dates, 15 of them on the low-BASE quarters (Q3 2011's +0.1%, Q2 2012's +2.2%: revenue -0.6% with Education -11.7% and the Financial
  Services line +4.3%) and 7 on Q4 2011's +4.4% and Q3 2012's +5.2% at higher prices, returned +50.3% to +85.0% and
  beat SPY on all 22 (the year's excess +13.4pp to +58.1pp).
- **FY2012's guide is not comparable:** it was consolidated, and the Q4 2012 release reports the year from continuing operations without
  McGraw-Hill Education ($2.75), so no comparison is made.
- **The two-year price landed nearest BULL on 50 dates and XBULL on 2;** the adjusted gap ranked the dates (Spearman +0.78; the proxy
  composite +0.41, and +0.84 against the m12-24 average price), the price did too (-0.70).

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 15 | +93.9% | +59.3% to +102.6% | 15 | 15 | +65.5% | 15 |
| class CHEAP, legacy tier BUY | 12 | +118.3% | +103.0% to +135.8% | 12 | 12 | +77.6% | 12 |
| class CHEAP, legacy tier WATCHLIST | 5 | +66.0% | +57.2% to +83.8% | 5 | 5 | +57.0% | 5 |
| class FAIR, legacy tier ACCUMULATE | 3 | +65.8% | +65.1% to +71.3% | 3 | 3 | +51.5% | 0 |
| class FAIR, legacy tier WATCHLIST | 5 | +39.0% | +35.9% to +44.2% | 5 | 5 | +47.3% | 1 |
| class RICH, legacy tier AVOID | 11 | +33.4% | +26.8% to +41.6% | 7 | 11 | +32.5% | 0 |
| class RICH, legacy tier WATCHLIST | 2 | +65.2% | +57.3% to +65.2% | 2 | 2 | +44.9% | 0 |
| EPS $3.375 (2013-01-04 to 2013-02-08) | 6 | +65.8% | +57.3% to +134.1% | 6 | 6 | +51.5% | 1 |
| EPS $3.15 (2013-02-13 to 2013-07-19) | 23 | +102.6% | +83.3% to +135.8% | 23 | 23 | +69.9% | 23 |
| EPS $3.2 (2013-07-26 to 2013-10-18) | 13 | +59.3% | +35.9% to +78.5% | 13 | 13 | +52.0% | 9 |
| EPS $3.275 (2013-10-23 to 2013-12-31) | 11 | +33.4% | +26.8% to +41.6% | 7 | 11 | +32.5% | 0 |
| latest print Q3 2012 (2013-01-04 to 2013-02-08) | 6 | +65.8% | +57.3% to +134.1% | 6 | 6 | +51.5% | 1 |
| latest print Q4 2012 (2013-02-13 to 2013-04-26) | 11 | +118.1% | +103.0% to +135.8% | 11 | 11 | +74.5% | 11 |
| latest print Q1 2013 (2013-05-01 to 2013-07-19) | 12 | +94.6% | +83.3% to +102.6% | 12 | 12 | +67.6% | 12 |
| latest print Q2 2013 (2013-07-26 to 2013-10-18) | 13 | +59.3% | +35.9% to +78.5% | 13 | 13 | +52.0% | 9 |
| latest print Q3 2013 (2013-10-23 to 2013-12-31) | 11 | +33.4% | +26.8% to +41.6% | 7 | 11 | +32.5% | 0 |

- **CHEAP held on all 32 CHEAP dates; the FAIR and RICH calls missed on 20 of 21.** The CHEAP dates (2013-02-08 to 2013-09-13, $42.67-62.76, 12.6-19.6x)
  returned +57.2% to +135.8%, those from the Q4 2012 print +103.0% to +135.8% (the Education sale closed on 2013-03-22). FAIR from
  2013-09-20 (5 WATCHLIST dates) returned +35.9% to +44.2%: the call held only on 2013-10-11 (+35.9%, which the check counts as held). The
  11 RICH and AVOID dates from the Q3 2013 print ($70.77-78.20, 21.6-23.9x FY2013's $3.275, the 77th-94th percentile, 44-59% above the
  floor) returned +26.8% to +41.6%, beat SPY on all 11 by 11-19pp and fell short of the hurdle on four (2013-12-13 to 2013-12-31).
- **The price ranked the dates almost perfectly within 2013** (Spearman -0.96 against the two-year return, Ratio B -0.97, the adjusted
  gap +0.80): the class and tier groups mostly ordered the medians (CHEAP BUY +118.3%, CHEAP ACCUMULATE +93.9%, CHEAP WATCHLIST +66.0%, FAIR
  WATCHLIST +39.0%, RICH AVOID +33.4%), though every group beat SPY. Landing: BULL 32, XBULL 15, BASE 6.
- FY2013's result is outside the series' facts (the Q4 2013 release is not in the fact sheet), so the 2013 guides are not checked here.

## 2010-2013 together (209 dates)

- **Every date beat SPY over two years, and 202 of 209 cleared the 15%/yr hurdle.** CHEAP (163 dates) returned a median +65.3% (excess
  +34.1pp) and held on all 163; FAIR (17) +66.7% (+21.9pp) and RICH (29) +57.3% (+18.7pp), so 45 of the 46 FAIR and RICH calls missed.
  The legacy tiers order the medians only loosely (BUY +64.3%, ACCUMULATE +74.6%, WATCHLIST +57.2%, AVOID +33.4%), and across the four
  years the entry price barely ranks the return (Spearman +0.16): the rerating lifted every date.
- **The FAIR and RICH calls of October 2011 to February 2013 rested on BASE from consolidated revenue in quarters that McGraw-Hill
  Education dragged** (Q3 2011, Q2 2012), while the retained businesses grew; the separation into two companies had been announced on
  2011-09-12 and Education was sold in March 2013. Hypothesis, not a rule: once a company announces the separation of a segment, BASE on
  the consolidated quarter understates the growth of what remains; test it on other tickers' announced separations and spin-offs (a
  rule that used it would need the retained segments' growth as published from the announcement), never fit it to SPGI.
- **The RICH and AVOID dates of late 2013 sat at the 77th-94th percentile of a window that mixes two companies** (2004-2012 prices with
  Education and the Broadcasting stations, EPS without Education from 2008): the stock went on to beat SPY from every one of them.
  Hypothesis: after a portfolio change, the decade's own-history P/E window may misplace the retained business's multiple; test on other
  tickers whose mix changed, never fit it here.
- **Today's profile files SPGI DURABLE with risk 1** ("Ratings duopoly + indices flywheel", `profile_drift`), where every point-in-time
  reading was DURABLE with risk 2; label only.
