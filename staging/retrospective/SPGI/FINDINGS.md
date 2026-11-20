# SPGI retrospective findings (hindsight)

Patterns seen in `outcome.json` for the SPGI weekly dates: 105 from 2008-01-04 to 2009-12-31, all The McGraw-Hill Companies, Inc. (NYSE:
MHP; SPGI is the series key). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was
scored only after its point-in-time build and its firewall result were committed (2008-2009: 7a7b5ac, firewall e1db42b); the push of those
two commits followed a few minutes after the outcome computation began, and no committed file changed in between. Outcomes were computed
on 2026-11-20; every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-28). Total returns include the quarterly
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
