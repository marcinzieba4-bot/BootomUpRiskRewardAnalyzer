# SPGI retrospective findings (hindsight)

Patterns seen in `outcome.json` for the SPGI weekly dates: 731 from 2008-01-04 to 2021-12-31, The McGraw-Hill Companies, Inc. (NYSE:
MHP; SPGI is the series key), McGraw Hill Financial, Inc. from 2013-05-06 and NYSE: MHFI from 2013-05-14, S&P Global Inc. from
2016-05-02 and NYSE: SPGI from 2016-06-30. They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was
scored only after its point-in-time build and its firewall result were committed (2008-2009: 7a7b5ac, firewall e1db42b); the push of those
two commits followed a few minutes after the outcome computation began, and no committed file changed in between. Outcomes were computed
on 2026-11-20; every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2016-12-30). 2010-2013 was scored only after
its build (51cf532) and its firewall result (23e3e2c) were committed and pushed; that batch was decided in the session that had written
the 2008-2009 sections below (disclosed in retro/README.md, "SPGI 2010-2013"). 2014-2017 was built in a new session that did not open these
findings, `SERIES.md` or any outcome first, and scored only after its build (5fffe7f) and its firewall result (0bcb78d) were committed
and pushed; its 3-year horizons end on 2020-12-29. 2018-2021 was decided in the session that had scored 2014-2017 (disclosed in
retro/README.md, "SPGI 2018-2021") and scored only after its build (2fe0ec6) and its firewall result (1138bf6) were committed and pushed;
its 3-year horizons end on 2024-12-30. Total returns include the quarterly
dividends as Yahoo records them (ex-dates); no split falls in any horizon, so every price is as traded. Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over
two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY); RICH should miss the hurdle and lag it; FAIR should land within +/-15pp of it.

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

## 2014 (51 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 51 | +36.1% | +8.0% to +60.8% | 32 | 51 | +22.1% | 0 |
| EPS $3.275 (2014-01-10 to 2014-01-31) | 4 | +16.6% | +11.7% to +20.1% | 0 | 4 | +29.9% | 0 |
| EPS $3.8 (2014-02-05 to 2014-07-25) | 25 | +33.5% | +8.0% to +48.0% | 15 | 25 | +22.2% | 0 |
| EPS $3.85 (2014-07-30 to 2014-10-24) | 13 | +54.0% | +47.7% to +60.8% | 13 | 13 | +24.0% | 0 |
| EPS $3.805 (2014-10-30 to 2014-12-26) | 9 | +31.3% | +24.3% to +42.5% | 4 | 9 | +17.7% | 0 |
| latest print Q3 2013 (2014-01-10 to 2014-01-31) | 4 | +16.6% | +11.7% to +20.1% | 0 | 4 | +29.9% | 0 |
| latest print Q4 2013 (2014-02-05 to 2014-04-25) | 12 | +28.5% | +8.0% to +40.9% | 5 | 12 | +26.3% | 0 |
| latest print Q1 2014 (2014-04-30 to 2014-07-25) | 13 | +37.7% | +22.6% to +48.0% | 10 | 13 | +18.3% | 0 |
| latest print Q2 2014 (2014-07-30 to 2014-10-24) | 13 | +54.0% | +47.7% to +60.8% | 13 | 13 | +24.0% | 0 |
| latest print Q3 2014 (2014-10-30 to 2014-12-26) | 9 | +31.3% | +24.3% to +42.5% | 4 | 9 | +17.7% | 0 |

- **RICH and AVOID on all 51 dates, and every one beat SPY, so the call missed on all 51.** Two-year returns of +8.0% to +60.8% against
  SPY's +5.8% to +17.9% (excess +1.9pp to +42.9pp); 32 cleared the hurdle. The 19 that did not are 2014-01-10 to 2014-03-21, 2014-06-13
  to 2014-07-03 and 2014-11-28 to 2014-12-26. The stock traded at 18.9-24.6x the current-FY EPS, the 41st-97th percentile of its own
  decade and 26-64% above the floor; the worst two-year drawdown from any date was -25.6%, against a BEAR of -39.1%/yr from the
  2007-2008 Education seam.
- **Within 2014, Ratio B and the adjusted gap ranked the dates** (Spearman -0.77 and +0.73 against the two-year return), the price did
  not (+0.07): the Q2 2014 print's 13 dates (20.4-22.4x the $3.85 guide) returned +47.7% to +60.8%, the Q4 2013 print's 12 +8.0% to
  +40.9%. Landing: BULL 40, XBULL 9, BASE 2.
- The guides were beaten on the company's figures: FY2013's $3.33 (the Q4 2013 release) against the $3.25-3.30 of the January dates, and
  FY2014's $3.88 against the $3.78-3.83 the models carried from the Q3 2014 print.

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 53 | +45.5% | +22.0% to +88.6% | 36 | 53 | +22.8% | 0 |
| EPS $3.805 (2015-01-02 to 2015-02-06) | 6 | +29.5% | +24.4% to +37.9% | 2 | 6 | +22.8% | 0 |
| EPS $4.4 (2015-02-13 to 2015-10-30) | 38 | +45.4% | +22.0% to +80.7% | 25 | 38 | +20.6% | 0 |
| EPS $4.475 (2015-11-04 to 2015-12-31) | 9 | +73.4% | +66.2% to +88.6% | 9 | 9 | +45.8% | 0 |
| latest print Q3 2014 (2015-01-02 to 2015-02-06) | 6 | +29.5% | +24.4% to +37.9% | 2 | 6 | +22.8% | 0 |
| latest print Q4 2014 (2015-02-13 to 2015-04-24) | 11 | +27.9% | +22.0% to +31.4% | 0 | 11 | +12.1% | 0 |
| latest print Q1 2015 (2015-04-29 to 2015-07-24) | 13 | +44.0% | +29.7% to +49.4% | 11 | 13 | +19.0% | 0 |
| latest print Q2 2015 (2015-07-28 to 2015-10-30) | 14 | +70.7% | +50.9% to +80.7% | 14 | 14 | +42.6% | 0 |
| latest print Q3 2015 (2015-11-04 to 2015-12-31) | 9 | +73.4% | +66.2% to +88.6% | 9 | 9 | +45.8% | 0 |

- **RICH and AVOID on all 53; every date beat SPY (by +5.3pp to +52.1pp), so the call missed on all 53.** 36 cleared the hurdle; the 17
  that did not are 2015-01-02 to 2015-05-08.
- **Within 2015 the multiple ranked the dates** (Spearman -0.83 for the P/E, -0.52 for the price, +0.83 for the adjusted gap): the Q4 2014
  print's 11 dates (23.1-24.7x the $4.40 guide, the 82nd-97th percentile) returned +22.0% to +31.4% and none cleared the hurdle; the Q2
  and Q3 2015 prints' 23 dates (20.3-23.1x) returned +50.9% to +88.6%. Landing: BULL 27, XBULL 26.
- FY2015's $4.53 (the company's figure) beat the $4.45-4.50 the models carried from the Q3 2015 print.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier AVOID | 1 | +120.1% | +120.1% to +120.1% | 1 | 1 | +72.0% | 0 |
| class FAIR, legacy tier WATCHLIST | 6 | +116.6% | +97.6% to +118.7% | 6 | 6 | +75.7% | 0 |
| class RICH, legacy tier AVOID | 45 | +76.3% | +43.0% to +108.3% | 45 | 45 | +57.3% | 0 |
| EPS $4.475 (2016-01-08 to 2016-01-29) | 4 | +116.6% | +103.7% to +117.2% | 4 | 4 | +75.7% | 0 |
| EPS $4.53 (2016-02-05 to 2016-12-30) | 48 | +82.8% | +43.0% to +120.1% | 48 | 48 | +58.4% | 0 |
| latest print Q3 2015 (2016-01-08 to 2016-01-29) | 4 | +116.6% | +103.7% to +117.2% | 4 | 4 | +75.7% | 0 |
| latest print Q4 2015 (2016-02-05 to 2016-04-22) | 12 | +100.2% | +89.8% to +120.1% | 12 | 12 | +64.3% | 0 |
| latest print Q1 2016 (2016-04-27 to 2016-07-22) | 13 | +87.4% | +76.3% to +101.4% | 13 | 13 | +58.4% | 0 |
| latest print Q2 2016 (2016-07-29 to 2016-10-28) | 14 | +69.3% | +43.0% to +76.4% | 14 | 14 | +50.8% | 0 |
| latest print Q3 2016 (2016-11-04 to 2016-12-30) | 9 | +51.6% | +48.3% to +61.2% | 9 | 9 | +66.0% | 0 |

- **No call held: RICH on 45 dates (AVOID), FAIR on 7 (6 WATCHLIST, 1 AVOID), and every date beat SPY by +13.6pp to +72.8pp and
  cleared the hurdle.** The FAIR run of 2016-01-15 to 2016-02-26 (18.6-19.7x, the 26th-39th percentile) returned +97.6% to +120.1%,
  52-73pp over SPY rather than within 15pp of it; the RICH dates +43.0% to +108.3%.
- **Within 2016 the price ranked the dates** (Spearman -0.85, the P/E -0.85, Ratio B -0.76): the year's cheapest dates returned the most.
  Landing XBULL on all 52.
- **The anchor was FY15's $4.53 all year** (the amortization rule: the company's guides also removed deal-related amortization). FY2016
  came in at the company's $5.35 on that basis, above its $5.15-5.25 guide, and at GAAP $7.94 with the divestiture gains. The ten dates
  the other reading moves (2016-02-05 to 2016-04-08: RICH to FAIR and FAIR to CHEAP, retro/README.md "SPGI 2014-2017") returned +95.6%
  to +120.1%.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +61.8% | +51.1% to +78.9% | 52 | 52 | +36.8% | 0 |
| EPS $4.53 (2017-01-06 to 2017-02-03) | 5 | +59.9% | +53.5% to +65.8% | 5 | 5 | +65.6% | 0 |
| EPS $5.775 (2017-02-08 to 2017-04-21) | 11 | +59.2% | +52.0% to +70.5% | 11 | 11 | +48.9% | 0 |
| EPS $5.82 (2017-04-26 to 2017-07-21) | 13 | +58.6% | +51.1% to +66.9% | 13 | 13 | +36.6% | 0 |
| EPS $5.905 (2017-07-28 to 2017-10-20) | 13 | +65.1% | +56.9% to +78.9% | 13 | 13 | +34.6% | 0 |
| EPS $6.265 (2017-10-27 to 2017-12-29) | 10 | +64.4% | +56.3% to +66.3% | 10 | 10 | +36.0% | 0 |
| latest print Q3 2016 (2017-01-06 to 2017-02-03) | 5 | +59.9% | +53.5% to +65.8% | 5 | 5 | +65.6% | 0 |
| latest print Q4 2016 (2017-02-08 to 2017-04-21) | 11 | +59.2% | +52.0% to +70.5% | 11 | 11 | +48.9% | 0 |
| latest print Q1 2017 (2017-04-26 to 2017-07-21) | 13 | +58.6% | +51.1% to +66.9% | 13 | 13 | +36.6% | 0 |
| latest print Q2 2017 (2017-07-28 to 2017-10-20) | 13 | +65.1% | +56.9% to +78.9% | 13 | 13 | +34.6% | 0 |
| latest print Q3 2017 (2017-10-27 to 2017-12-29) | 10 | +64.4% | +56.3% to +66.3% | 10 | 10 | +36.0% | 0 |

- **RICH and AVOID on all 52 at 21.7-27.4x the FY2017 GAAP guide (the 74th-100th percentile, 46-96% above the floor); every date
  returned +51.1% to +78.9%, beat SPY by +31.2pp to +53.9pp and cleared the hurdle.** No call held.
- **The price did not rank the dates within 2017** (Spearman +0.21, Ratio B +0.09): the dates at the 99th-100th percentile from
  2017-07-28 returned +56.3% to +78.9%. Landing: XBULL 38, BULL 14.
- BASE was the buyback alone on the reported revenue guide of 0% (divestitures; organic growth was guided in words), but no reading of the
  revenue words moves a class (retro/README.md, "SPGI 2014-2017"). FY2017's result is outside the series' facts (the Q4 2017 release is
  not in the fact sheet).

## 2014-2017 together (208 dates)

- **Every date beat SPY over two years (by +1.9pp to +72.8pp) and 172 of 208 cleared the 15%/yr hurdle; no call held.** RICH (201 dates)
  returned a median +56.8% (excess +34.3pp), FAIR (7) +116.6% (+64.8pp); three-year returns ran +47.8% to +167.0%. Across the four years
  the entry price barely ranks the return (Spearman +0.34 for the price, -0.07 for Ratio B), within 2014, 2015 and 2016 Ratio B does
  (-0.77, -0.73, -0.76): the rerating lifted every date, as in 2010-2013.
- **The RICH calls rested on a window that mixes companies.** The decade's P/E distribution carries 2004-2007 with McGraw-Hill Education
  and 2008-2012's trough multiples of the remaining business; the retained ratings, data and index company traded at the 74th-100th
  percentile of it from 2014 and kept rerating. Hypothesis, not a rule (it extends 2010-2013's): after a portfolio change, an own-history
  P/E window misplaces the retained business's multiple; test it on other tickers whose mix changed, never fit it to SPGI.
- **BEAR at the seam set every tier to AVOID.** -39.1%/yr is 2007's $2.94 with Education against 2008's $1.79 without it, a change of
  scope rather than a downturn; the worst drawdown within two years of any date was -26.0%. Hypothesis: a BEAR measured across a
  portfolio seam overstates the downside; a rule limiting BEAR to years on one basis would be a new method version, tested on other
  tickers first (the history-from-2008 reading moves 34 classes and 89 tiers here, which says only that the call is large).
- **The amortization rule held FY2016's anchor at FY15's $4.53** while the company's guides and its result on their basis were higher;
  the dates it affects most returned the most. Hypothesis for cross-ticker testing (CMCSA 2019, PFE, AVGO, SHW): whether a company that
  starts excluding recurring amortization mid-series is better read on its new basis than on GAAP; never fit it to SPGI.
- **The quarters as reported** (the Q4 2014 settlements, the 2016 gains and their 2017 lapping) moved no class but one: the signals do
  not carry these calls.
- Today's profile still files SPGI DURABLE with risk 1 where every point-in-time reading was DURABLE with risk 2; label only.

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 50 | +66.5% | +5.4% to +101.7% | 46 | 50 | +34.1% | 0 |
| class RICH, legacy tier WATCHLIST | 2 | +100.8% | +97.2% to +100.8% | 2 | 2 | +95.3% | 0 |
| EPS $6.265 (2018-01-05 to 2018-02-02) | 5 | +65.1% | +60.0% to +68.1% | 5 | 5 | +31.9% | 0 |
| EPS $8.225 (2018-02-07 to 2018-03-02) | 4 | +64.1% | +55.0% to +64.8% | 4 | 4 | +31.1% | 0 |
| EPS $8.025 (2018-03-09 to 2018-05-18) | 11 | +43.1% | +5.4% to +59.7% | 7 | 11 | +31.2% | 0 |
| EPS $7.825 (2018-05-25 to 2018-10-19) | 22 | +70.8% | +55.4% to +95.7% | 22 | 22 | +39.2% | 0 |
| EPS $7.82 (2018-10-26 to 2018-12-28) | 10 | +95.7% | +81.8% to +101.7% | 10 | 10 | +77.9% | 0 |
| latest print Q3 2017 (2018-01-05 to 2018-02-02) | 5 | +65.1% | +60.0% to +68.1% | 5 | 5 | +31.9% | 0 |
| latest print Q4 2017 (2018-02-07 to 2018-04-20) | 11 | +43.1% | +5.4% to +64.8% | 7 | 11 | +31.2% | 0 |
| latest print Q1 2018 (2018-04-27 to 2018-07-20) | 13 | +59.8% | +51.0% to +70.8% | 13 | 13 | +30.4% | 0 |
| latest print Q2 2018 (2018-07-27 to 2018-10-19) | 13 | +79.4% | +67.3% to +95.7% | 13 | 13 | +40.6% | 0 |
| latest print Q3 2018 (2018-10-26 to 2018-12-28) | 10 | +95.7% | +81.8% to +101.7% | 10 | 10 | +77.9% | 0 |

- **RICH on all 52 dates (AVOID on 50), and every one beat SPY, so the call missed on all 52.** Two-year returns of +5.4% to +101.7%
  against SPY's -9.3% to +57.5% (excess +14.7pp to +69.1pp); 48 cleared the hurdle, all but the four March 2018 dates. The stock traded at
  20.7-29.3x the current-FY EPS, the 53rd-100th percentile of its decade; the worst two-year drawdown was -38.3% (from the 2020 crash).
- **Within 2018 nothing ranked the dates well** (Spearman -0.29 for the price, -0.15 for Ratio B). The best were the Q3 2018 print's
  dates (+81.8% to +101.7%, 20.7-24.8x after the October 2018 fall, two of them on the WATCHLIST tier). Landing: XBULL 37, BULL 13,
  BASE 2.
- The guides were met on GAAP: FY2018 came in at $7.73 against the $7.77-7.87 range of the Q3 2018 print (just under), FY2017 at $5.78
  against the $6.19-6.34 the January dates carried (the Tax Act charge).

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 50 | +75.9% | +64.8% to +96.3% | 50 | 50 | +52.5% | 0 |
| class RICH, legacy tier WATCHLIST | 2 | +77.2% | +73.7% to +77.2% | 2 | 2 | +64.4% | 0 |
| EPS $7.82 (2019-01-04 to 2019-02-01) | 5 | +69.0% | +64.8% to +96.3% | 5 | 5 | +68.7% | 0 |
| EPS $8.6 (2019-02-08 to 2019-04-26) | 12 | +74.3% | +67.6% to +77.2% | 12 | 12 | +59.4% | 0 |
| EPS $8.26 (2019-05-03 to 2019-07-26) | 13 | +78.5% | +71.4% to +84.5% | 13 | 13 | +54.4% | 0 |
| EPS $8.275 (2019-08-02 to 2019-10-25) | 13 | +73.1% | +70.9% to +83.0% | 13 | 13 | +46.2% | 0 |
| EPS $8.61 (2019-10-30 to 2019-12-27) | 9 | +76.8% | +68.5% to +88.4% | 9 | 9 | +46.5% | 0 |
| latest print Q3 2018 (2019-01-04 to 2019-02-01) | 5 | +69.0% | +64.8% to +96.3% | 5 | 5 | +68.7% | 0 |
| latest print Q4 2018 (2019-02-08 to 2019-04-26) | 12 | +74.3% | +67.6% to +77.2% | 12 | 12 | +59.4% | 0 |
| latest print Q1 2019 (2019-05-03 to 2019-07-26) | 13 | +78.5% | +71.4% to +84.5% | 13 | 13 | +54.4% | 0 |
| latest print Q2 2019 (2019-08-02 to 2019-10-25) | 13 | +73.1% | +70.9% to +83.0% | 13 | 13 | +46.2% | 0 |
| latest print Q3 2019 (2019-10-30 to 2019-12-27) | 9 | +76.8% | +68.5% to +88.4% | 9 | 9 | +46.5% | 0 |

- **RICH and AVOID (50) or WATCHLIST (2) on all 52; every date beat SPY by +11.9pp to +45.7pp and cleared the hurdle, so no call held.**
  The stock traded at 22.0-32.4x, the 68th-100th percentile, 22-80% above the floor; two-year returns +64.8% to +96.3%.
- **Nothing ranked the dates** (Spearman +0.04 for the price, -0.04 for Ratio B): the rerating lifted every entry. Three-year returns
  range from +20.0% (2019-10-11, into the 2022 fall) to +171.6%. Landing: XBULL 44, BULL 8.
- FY2019's GAAP $8.60 sat inside the $8.56-8.66 range of the Q3 2019 print.

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 1 | +99.1% | +99.1% to +99.1% | 1 | 0 | +100.7% | 1 |
| class FAIR, legacy tier WATCHLIST | 2 | +74.9% | +73.3% to +74.9% | 2 | 0 | +76.3% | 2 |
| class RICH, legacy tier AVOID | 50 | +7.7% | -15.9% to +68.6% | 12 | 8 | +17.6% | 36 |
| EPS $8.61 (2020-01-03 to 2020-01-31) | 5 | +47.6% | +40.4% to +68.6% | 5 | 4 | +40.0% | 0 |
| EPS $10.1 (2020-02-07 to 2020-04-24) | 12 | +47.8% | +25.9% to +99.1% | 10 | 2 | +53.9% | 5 |
| EPS $9.6 (2020-04-29 to 2020-07-24) | 13 | +6.9% | +0.2% to +29.9% | 0 | 0 | +29.1% | 13 |
| EPS $10.35 (2020-07-29 to 2020-10-23) | 13 | +0.9% | -15.9% to +13.0% | 0 | 0 | +13.8% | 13 |
| EPS $10.075 (2020-10-28 to 2020-12-31) | 10 | +6.7% | -9.0% to +8.7% | 0 | 2 | +11.2% | 8 |
| latest print Q3 2019 (2020-01-03 to 2020-01-31) | 5 | +47.6% | +40.4% to +68.6% | 5 | 4 | +40.0% | 0 |
| latest print Q4 2019 (2020-02-07 to 2020-04-24) | 12 | +47.8% | +25.9% to +99.1% | 10 | 2 | +53.9% | 5 |
| latest print Q1 2020 (2020-04-29 to 2020-07-24) | 13 | +6.9% | +0.2% to +29.9% | 0 | 0 | +29.1% | 13 |
| latest print Q2 2020 (2020-07-29 to 2020-10-23) | 13 | +0.9% | -15.9% to +13.0% | 0 | 0 | +13.8% | 13 |
| latest print Q3 2020 (2020-10-28 to 2020-12-31) | 10 | +6.7% | -9.0% to +8.7% | 0 | 2 | +11.2% | 8 |

- **The call held on 39 of 53 dates, and the year splits at the COVID-19 crash.** The 11 RICH dates of January to mid-March (24.6-34.5x)
  returned +25.9% to +68.6% and held only on 2020-02-14 and 2020-02-21 (they lagged SPY and missed the hurdle). The CHEAP date (2020-03-20,
  $208.79, 20.7x, the 41st percentile) returned +99.1% and cleared the hurdle (held), the two FAIR dates (2020-03-27, 2020-04-03) +73.3%
  and +74.9%, within 15pp of SPY's rebound (held). The three RICH dates of 2020-04-09 to 2020-04-24 returned +35.8% to +47.8%,
  cleared the hurdle and lagged SPY by 17-19pp (missed). From the Q1 2020 print (2020-04-29) the 36 RICH dates (30.7-36.9x, the 94th-100th
  percentile) returned -15.9% to +29.9%, lagged SPY on all but two and held on 34.
- **Within 2020 the price ranked the dates** (Spearman -0.86, the P/E -0.66). Landing: BULL 42, BASE 6, XBULL 5.
- FY2020's GAAP $9.66 fell under the $10.00-10.15 range of the Q3 2020 print (lease impairments and merger costs in the fourth quarter).

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | -5.3% | -24.5% to +21.8% | 0 | 7 | -15.1% | 45 |
| EPS $10.075 (2021-01-08 to 2021-02-05) | 5 | +18.8% | +8.4% to +21.8% | 0 | 5 | +12.7% | 0 |
| EPS $9.66 (2021-02-10 to 2021-10-22) | 37 | -5.1% | -20.8% to +11.2% | 0 | 2 | -11.7% | 35 |
| EPS $12.575 (2021-10-27 to 2021-12-31) | 10 | -7.4% | -24.5% to -5.2% | 0 | 0 | -20.3% | 10 |
| latest print Q3 2020 (2021-01-08 to 2021-02-05) | 5 | +18.8% | +8.4% to +21.8% | 0 | 5 | +12.7% | 0 |
| latest print Q4 2020 (2021-02-10 to 2021-04-23) | 11 | -3.1% | -7.7% to +11.2% | 0 | 2 | +1.2% | 9 |
| latest print Q1 2021 (2021-04-30 to 2021-07-23) | 13 | -1.7% | -7.7% to +2.9% | 0 | 0 | -11.6% | 13 |
| latest print Q2 2021 (2021-07-30 to 2021-10-22) | 13 | -11.5% | -20.8% to -7.0% | 0 | 0 | -19.3% | 13 |
| latest print Q3 2021 (2021-10-27 to 2021-12-31) | 10 | -7.4% | -24.5% to -5.2% | 0 | 0 | -20.3% | 10 |

- **RICH and AVOID on all 52 at 30.4-46.9x (the 92nd-100th percentile); none cleared the hurdle, 45 lagged SPY, and the call held on 45.**
  Two-year returns of -24.5% to +21.8% against SPY's -6.7% to +12.9%, through the 2022 fall (the worst drawdown within two years -40.2%).
  The seven that did not hold are 2021-01-08 to 2021-02-19 (beating SPY by up to 12.6pp).
- **Within 2021 the price ranked the dates** (Spearman -0.77). The anchor was FY20's $9.66 to 2021-10-22 (no GAAP guide), so the P/E read
  34-47x; reading the adjusted ranges instead moves no class (retro/README.md, "SPGI 2018-2021"). Landing: BULL 43, BASE 9.
- FY2021's result is outside the series' facts (the Q4 2021 release is not in the fact sheet).

## 2018-2021 together (209 dates)

- **The RICH calls missed for two years and then held.** All 104 dates of 2018-2019 beat SPY (by +11.9pp to +69.1pp) and 100 cleared the
  hurdle, as in 2014-2017; of the 88 dates from the Q1 2020 print, 79 held (two-year returns -24.5% to +29.9%, excess -31.2pp to
  +12.6pp). Overall RICH held on 81 of 206 dates, the CHEAP and FAIR calls of March-April 2020 on all three. Across the four years the
  price ranks the two-year return (Spearman -0.82, the P/E -0.80, Ratio B -0.67).
- **What separated the two phases was the multiple's level, not its percentile.** In 2018-2019 the stock sat at the 53rd-100th percentile
  of its own decade at 20.7-32.4x and kept rerating; from April 2020 it sat at the 92nd-100th at 30-47x and the 2022 fall followed.
  Hypothesis, not a rule: an own-history percentile window that is itself rerating (the median rose from 20.1x to 23.0x across these
  dates) flags RICH too early; an absolute multiple or a distance from the window's median may separate the two phases better; test it on
  other tickers that rerated, never fit it to SPGI.
- **BEAR and the tiers rest on GAAP 2016's divestiture gains** (-27.2%/yr on every date from 2018-02-16, AVOID on 202 dates), while the
  worst drawdown within two years of any date was -40.2%, in 2022. The amortization reading moves 87 tiers and 12 classes (toward FAIR or
  CHEAP, 2018-04-27 to 2020-04-03); hypothesis for cross-ticker testing (with CMCSA 2019, PFE, AVGO, SHW), never fit to SPGI.
- **The COVID-19 low was the one cheap entry the method caught** (2020-03-20, CHEAP at 20.7x, +99.1%); the FAIR dates after it returned
  +73-75%. The rule for it existed already: the multiple fell into the lower half of the window.
- Today's profile still files SPGI DURABLE with risk 1 where every point-in-time reading was DURABLE with risk 2; label only.
