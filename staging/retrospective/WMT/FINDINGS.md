# WMT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the WMT weekly dates: 984 from 2008-01-04 to 2026-11-06 (the newest without full horizons). They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: 339c071; 2009-2011: 7be709f; 2012-2014: 4080783; 2015-2017: d2f2e6f; 2018-2020: ec73369; 2021-2023: 5748a2e; 2024-2026: b2877b9). Outcomes
to 2020 were computed on 2026-11-07 and those from 2021 on 2026-11-08, from the closes posted to 2026-11-06 (the 2021-2023 and 2024-2026
sections give their horizons).
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP (every date) | 53 | +0.2% | -13.1% to +23.1% | 0 | 35 | -5.8% | 35 |
| legacy tier BUY (every date) | 53 | +0.2% | -13.1% to +23.1% | 0 | 35 | -5.8% | 35 |
| FY08 guide $3.15 (to 2008-02-15) | 7 | +14.2% | +8.5% to +23.1% | 0 | 7 | +5.3% | 7 |
| FY09 guide $3.365 (2008-02-20 to 2008-08-08) | 25 | -4.5% | -11.4% to +13.2% | 0 | 25 | -7.8% | 25 |
| FY09 guide $3.465 (2008-08-15 to 2008-11-07) | 13 | -7.2% | -13.1% to +11.2% | 0 | 3 | -11.8% | 3 |
| FY09 guide $3.44 (from 2008-11-14) | 8 | +1.7% | -2.3% to +7.0% | 0 | 0 | -4.2% | 0 |
| January-September | 39 | -4.5% | -13.1% to +23.1% | 0 | 35 | -7.8% | 35 |
| October-December | 14 | +3.4% | -6.9% to +11.2% | 0 | 0 | -3.0% | 0 |

- **CHEAP held on 35 of 53 dates, only against a falling market, and never cleared the hurdle.** The 39 dates from January to September
  returned -13% to +23% over two years while SPY returned -19% to -1%, so 35 beat it (all but 2008-09-05 to 2008-09-26, 2-6pp behind).
  The 14 dates from October met SPY's rebound (+8% to +57%) with WMT at -7% to +11%, 15-50pp behind, so the call failed on every one.
  No date reached the +32.2% hurdle. One-year returns had a median of -6.1% (-17% to +27%), ahead of SPY on 36; three-year returns ran
  from -11% to +27% (median +3.1%), ahead of SPY on 21. A defensive stock bought in a crash: relative strength while the market fell,
  little absolute return afterwards.
- **The two-year price landed on BEAR, every time.** The two-year price ($48-56, as traded) landed nearest BEAR on all 53 dates, at
  0.92-1.11 times the BEAR price and 0.43-0.55 times BASE. The lowest close of 52 windows was 2009-02-04's $46.42 (0.88-0.95 times BEAR); the
  model's own BEAR (flat EPS at the 10th-percentile P/E, $49-53) was in effect the outcome. The outcomes record prices, not EPS, so they
  do not say whether the earnings stayed flat or the multiple fell further.
- **The floor was a decade of de-rating.** CHEAP came from the EPP floor, the median of the calendar-year P/E lows over the ten-year
  window: 21-22x, because the window still held 1999-2004 (lows of 32.1x falling to 20.9x), while every low since 2005 was 13.4-15.6x and
  the stock traded at 14.5-18.0x in 2008. The price sat 18-33% under the floor on every date, and the floor did not hold up as a value
  anchor: two years later the stock traded about where the 10th-percentile multiple put it. Hypothesis for the method, not a rule: a
  floor taken as the median of a decade in which the multiple fell nearly every year sits above where the stock now trades and reads
  CHEAP by construction. It is the mirror of SHW's 2008 lesson (a guided trough year read RICH) on the same input family, the anchor of
  the EPP floor. Test a trend-aware or shorter-window floor on other tickers and periods before any method change; never fit it to WMT's
  outcomes.
- **Within the year, the price ranked the outcome; the composite ranked it the wrong way.** Across the 53 dates the entry price ranks the
  return to the m12-24 average price at Spearman -0.99 (the two-year endpoint: -0.94), so cheaper entries did better. The EPP gap (-0.92)
  and Ratio B (-0.98) rank it the right way only because their anchors barely moved, which leaves them as the price. The proxy composite
  ranks it at -0.49: 1.95 on the Q3 FY08 print (median two-year return +14%), then 2.05, 2.15 and 2.55 on the Q2 FY09 print (comparable
  sales +5.0% and gross margin +31.5bp at BULL; median -7%), the strongest reading before the weakest returns. The adjusted gap ranks it at
  +0.24, weakly the right way. One stock through one crash mostly tests "buy lower".
- **The encoding calls, seen afterwards.** None of the alternatives in retro/README.md ("WMT") moves a class or a tier, not even every
  signal at BEAR, so the outcomes cannot tell them apart. DURABLE changes only the label ("COMPOUNDER AT LOW PRICE"); the price state,
  set by the floor, carried the call. The calls were decided before scoring and stay; changing a rule means a new method version tested
  elsewhere.

## 2009-2011 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, tier BUY (every date) | 156 | +32.0% | +1.0% to +61.7% | 76 | 72 | +16.7% | 88 |
| 2009 (EPP floor 18-20x) | 52 | +12.6% | +1.0% to +25.2% | 0 | 3 | +6.8% | 3 |
| 2010 (EPP floor 15x) | 52 | +36.0% | +13.7% to +52.7% | 30 | 33 | +16.7% | 33 |
| 2011 (EPP floor 14x) | 52 | +46.7% | +27.7% to +61.7% | 46 | 36 | +32.1% | 52 |
| deepest under the floor (EPP gap -33% to -20%) | 52 | +12.6% | | | | +6.8% | |
| middle third (-19% to -12%) | 52 | +47.4% | | | | +31.6% | |
| nearest the floor (-12% to 0%) | 52 | +33.7% | | | | +20.7% | |
| highest third by adjusted gap (+1.22 to +1.57) | 52 | +15.3% | | | | +4.9% | |
| middle third (+0.58 to +1.22) | 52 | +44.6% | | | | +16.7% | |
| lowest third (+0.11 to +0.55) | 52 | +43.7% | | | | +25.1% | |

- **CHEAP held on 88 of 156 dates: almost never in 2009, from mid-2010 always.** In 2009 the stock returned +1% to +25% over two years
  while SPY, measured from the March 2009 low onward, returned +10% to +99%; the call held only on 2009-10-09, 2009-12-18 and 2009-12-24,
  by 0.2-0.6pp, and no 2009 date cleared the hurdle. The 19 dates from January to 2010-05-14 returned +14% to +22% and trailed SPY by
  0.1-14pp. Every date from 2010-05-19 held: the rest of 2010 beat SPY, and all of 2011 returned +28% to +62% (46 of 52 over the hurdle;
  the six January-February dates under it, at +28% to +32%, beat SPY by 6-13pp). Three-year returns ran +20% to +65% and beat SPY on 63
  of 156. The pattern of 2008 carried into early 2009: a defensive stock that held up in the fall did little in the rebound.
- **The two-year price walked up from BEAR to BASE.** It landed nearest BEAR on all 52 dates of 2009 (0.96-1.15 times the BEAR price), on
  22 of 2010 (BASE on 30) and on 2 of 2011 (BASE on 50, at 0.82-0.98 times BASE). Drawdowns were 12-16%, the lows at $47.57 (2009-07-10),
  $48.00 (2010-07-02) and $48.41 (2011-08-10), about the BEAR prices of $51-59.
- **The call held once the floor came down to where the stock traded.** Hypothesis for the method, not a rule. In 2009 the EPP floor
  still held the 1999-2004 lows (20x, then 18x) and the price sat 17-33% under it: the deepest third under the floor returned a median
  +12.6%. By 2011 the window had lost those years, the floor was 14x and the price 0-20% under it: the middle and nearest thirds returned
  +47% and +34%. This is the 2008 finding seen from the other side: a floor taken from a decade in which the multiple fell nearly every
  year sits above where the stock trades and reads CHEAP regardless; once the window holds only the de-rated years, the floor and the
  price agree. The market's own move (the 2009 rebound, which a defensive stock lagged) is confounded with it. Test a trend-aware or
  shorter-window floor on other tickers and periods before any method change; never fit it to WMT's outcomes.
- **The signals ranked the outcome the wrong way again.** Across the 156 dates the proxy composite ranks the return to the m12-24 average
  price at Spearman -0.83 (the two-year endpoint: -0.68): its best readings (2.05-2.35: gross margin up 35-85bp, the operating margin
  up and inventories growing slower than sales through FY10) came in 2009 and early 2010, before the weakest returns, and its worst
  (1.30-1.50: comparable sales negative, gross margin down, inventories growing faster than sales) in late 2010 and 2011, before the best. The adjusted gap ranks it at -0.65 (the highest third returned +15%, the lowest
  +44%). Ratio B (-0.51) ranks it the right way, the EPP gap (+0.18) and the entry price (+0.18) hardly at all. In 2008 the proxy
  composite ranked it at -0.49: for this stock the quarter's operating signals have pointed the wrong way in both batches.
- **The encoding calls, seen afterwards.** None of the alternatives in retro/README.md ("WMT 2009-2011") moves a class or a tier, so the
  outcomes cannot tell them apart. What failed in 2009 was the level of the call, set by the floor; the calls were decided before scoring
  and stay.

## 2012-2014 (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 51 | +22.7% | +2.9% to +40.8% | 9 | 1 | +12.6% | 9 |
| class FAIR | 3 | +18.2% | +17.7% to +35.7% | 1 | 0 | +9.5% | 1 |
| class RICH | 103 | -3.3% | -23.9% to +33.8% | 1 | 0 | -6.2% | 102 |
| tier BUY | 140 | +4.4% | -23.9% to +40.8% | 11 | 1 | +3.5% | 95 |
| tier ACCUMULATE | 8 | -1.8% | -21.3% to -1.1% | 0 | 0 | -12.5% | 8 |
| tier WATCHLIST | 1 | -6.4% | | 0 | 0 | -13.7% | 1 |
| tier AVOID | 8 | -12.7% | -15.4% to -9.8% | 0 | 0 | -18.7% | 8 |
| 2012 (CHEAP 49, RICH 3) | 52 | +22.7% | +2.9% to +40.8% | 9 | 1 | +12.6% | 12 |
| 2013 (CHEAP 2, FAIR 3, RICH 47) | 52 | +1.9% | -23.9% to +35.7% | 2 | 0 | +4.5% | 47 |
| 2014 (RICH 53) | 53 | -5.2% | -17.1% to +5.7% | 0 | 0 | -12.5% | 53 |
| highest third by adjusted gap (-0.46 to +0.60) | 52 | +22.7% | | | | +12.6% | |
| middle third (-1.08 to -0.48) | 53 | +1.9% | | | | +4.4% | |
| lowest third (-2.24 to -1.09) | 52 | -5.6% | | | | -12.5% | |

- **RICH held on 102 of 103 dates; CHEAP on 9 of 51.** From late 2012 the stock traded above where BASE leaves room for the hurdle,
  and the call held: the RICH dates returned -24% to +34% over two years (median -3.3%) and never beat SPY (+6% to +51%). The one miss,
  2013-01-25, returned +33.8%, just over the +32.2% hurdle, still 7.4pp behind SPY. The AVOID dates (2014-11-14 to 2014-12-31, $83-88)
  returned -10% to -15% while SPY returned +10% to +17%. The CHEAP dates of 2012 returned +3% to +41% (median +22.7%) while SPY returned
  +34% to +56%: the call held on the eight cheapest entries of January-May 2012 ($58.70-60.67, 5-13% under the floor), which cleared
  the hurdle, and on 2012-12-28; only 2012-04-27 beat SPY (+1.8pp). One-year returns beat SPY on 17 of the 52 dates of 2012, none of
  2013 and 7 of 2014; over three years no date of 2012-2014 beat SPY (2012 median +10.4%, 2013 +0.4%, 2014 +9.9%).
- **The classes ranked the outcome the right way, for once.** CHEAP's median two-year return was +22.7%, FAIR's +18.2%, RICH's -3.3%;
  by adjusted gap the highest third returned +22.7%, the middle +1.9% and the lowest -5.6%. Across the 157 dates the adjusted gap ranks
  the return to the m12-24 average price at Spearman +0.93 (the two-year endpoint: +0.81), Ratio B at -0.94 (-0.82) and the market
  composite at -0.96 (-0.83), a little better than the entry price itself (-0.86, -0.82) and the EPP gap (-0.86, -0.81). The anchors
  moved this time (BASE $83-96, floor $62.72-68.90), but the ranking is still mostly "buy lower": the stock rose from $59 to $88.
- **A defensive stock in a bull market: up in absolute terms, behind in relative ones.** CHEAP's expectation is to clear the hurdle or
  beat SPY; in 2012 it failed on 40 of 49 CHEAP dates at +3% to +31%, as SPY ran +34% to +56%. This is the 2009 pattern again (a
  defensive stock lagging a rebound), and the 2008 one reversed (ahead while the market fell). Two of three WMT batches now say the
  class read a defensive stock's absolute value correctly and its relative value wrongly; whether the hurdle-or-benchmark test is the
  right label for such a stock is a question for the method, not a rule.
- **The two-year price walked down from BASE to BEAR.** It landed nearest BASE on 32 of the 52 dates of 2012 (0.78-1.00 times BASE),
  BEAR on 33 of 2013 (0.66-1.03 times BASE) and BEAR on all 53 of 2014 (0.97-1.18 times the BEAR price, $61-74). The lowest close of the
  windows was 2015-11-13's $56.42, and drawdowns reached 37.6% (from $90.47 on 2015-01-08) on the 60 dates from 2013-11-15. The outcomes record prices, not EPS, so they do
  not say whether the earnings or the multiple carried it.
- **The operating signals ranked the outcome the wrong way again in 2012.** Within 2012 the proxy composite ranks the return to the
  m12-24 average price at Spearman -0.70 (the two-year endpoint: -0.77); across 2013-2014 at -0.11 (-0.37); across all 157 dates at
  +0.11 (+0.05). With every signal at its BEAR value (a sensitivity run before scoring), 31 dates of June 2012 to March 2013 read RICH,
  and 29 of them would have held as RICH, against 2 that held as CHEAP or FAIR. For this stock the quarter's operating signals pointed
  the wrong way in all three batches (2008 -0.49, 2009-2011 -0.83, 2012 -0.70). Hypothesis for the method, not a rule: test whether
  comparable-sales and margin signals carry information for a mature, low-growth retailer on other tickers before any change; never
  fit them to WMT's outcomes.
- **The encoding calls, seen afterwards.** The release's own constant-currency rate (acquisitions out; retro/README.md, "WMT
  2012-2014") would have moved five CHEAP dates (2012-08-03 to 2012-10-26) to FAIR and 2013-03-08 from FAIR to RICH: the five returned
  +3% to +8% and lagged SPY by 30-40pp, so they fail as FAIR too, and 2013-03-08 (+17.7%, 20.5pp behind SPY) would have held as RICH.
  FY14 at reported EPS moves tiers only. The calls were decided before scoring and stay; changing a rule means a new method version
  tested elsewhere.

## 2015-2017 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 4 | +70.1% | +58.9% to +73.2% | 4 | 4 | +32.6% | 4 |
| class FAIR | 1 | +59.0% | | 1 | 1 | +27.6% | 0 |
| class RICH | 151 | +36.6% | -20.2% to +74.7% | 89 | 92 | +24.2% | 53 |
| tier BUY | 22 | +66.3% | +19.0% to +74.7% | 16 | 16 | +27.6% | 10 |
| tier ACCUMULATE | 15 | +15.3% | +5.6% to +71.2% | 3 | 4 | +0.2% | 11 |
| tier WATCHLIST | 3 | +9.1% | -0.5% to +10.6% | 0 | 0 | -6.1% | 3 |
| tier AVOID | 116 | +38.6% | -20.2% to +68.3% | 75 | 77 | +24.9% | 33 |
| 2015 (RICH 47, CHEAP 4, FAIR 1) | 52 | +13.0% | -20.2% to +73.2% | 13 | 14 | -0.2% | 42 |
| 2016 (RICH 52) | 52 | +38.1% | +20.0% to +74.7% | 36 | 31 | +26.1% | 15 |
| 2017 (RICH 52) | 52 | +44.5% | +25.4% to +56.9% | 45 | 52 | +27.3% | 0 |
| the reset window, 2015-10-16 to 2016-01-22 | 15 | +68.0% | +52.4% to +74.7% | 15 | 15 | +28.8% | 4 |
| highest third by adjusted gap (-1.90 to -0.24) | 52 | +43.6% | | 34 | 34 | +25.2% | |
| middle third (-2.08 to -1.90) | 52 | +36.6% | | 34 | 29 | +26.2% | |
| lowest third (-2.46 to -2.08) | 52 | +32.6% | | 26 | 34 | +16.8% | |

- **RICH held on 53 of 151 dates: before the October 2015 reset, not after it.** The 40 RICH dates to 2015-10-09 ($63-89) returned -20%
  to +33% over two years and held on 38 (the misses, 2015-08-19 and 2015-09-18, beat SPY by 0.7pp and 0.2pp). From the reset the stock
  re-rated: the 15 dates from 2015-10-16 to 2016-01-22 ($56-63) returned +52% to +75%, every one over the hurdle and ahead of SPY; the
  four CHEAP dates held and the ten RICH ones and the FAIR one failed. In 2016 RICH held on 15 dates (2016-03-24, 2016-04-15 and
  2016-05-20 to 2016-08-12, $68-74, +20% to +32%, 0.1-16pp behind SPY) and failed on 37; in 2017 it failed on all 52, which returned +25% to
  +57% and beat SPY (+15% to +29%) every time. Three-year returns ran +13% to +96% (median +63.6%) and beat SPY on 122 of 156.
- **The two-year price landed on XBULL from 2016 on.** It landed nearest BEAR on 6 dates of 2015, BASE on 26, BULL on 10 and XBULL on 10,
  then XBULL on all 104 dates of 2016-2017, at 1.13-1.54 times the BULL price and 1.20-1.67 times BASE ($82-120 two years on, against BULL
  prices of $73-81). The lowest close of the windows was 2015-11-13's $56.42 again (44 dates), and drawdowns ran 12-37%.
- **A decade of low multiples capped the upside the model could see.** Hypothesis for the method, not a rule. The scenarios take their
  multiples from the stock's own ten-year P/E range: from 2015 that window held only the de-rated years (median 14.6-14.9x, 90th
  percentile 16.5-17.2x), and BULL was held at BASE's rate once FY16's down year cut the decade CAGR. The stock then re-rated well past the
  90th percentile; the outcomes record prices, not EPS, so they do not say how much was multiple and how much earnings, but the two-year
  prices sat 23-54% over the BULL prices of 2017. This is the 2008 finding in reverse: there a decade of falling multiples put the EPP
  floor above the price and read CHEAP by construction; here a decade of low multiples put every scenario multiple below where the stock
  went and read RICH by construction. Test a percentile window that can see a regime change (or a cross-sectional multiple) on other
  tickers and periods before any method change; never fit it to WMT's outcomes.
- **The ranks agree only within 2015.** Within 2015 the entry price ranks the return to the m12-24 average price at Spearman -0.99, Ratio B
  and the EPP gap at -0.99, the adjusted gap at +0.71: "buy lower" again, with the October 2015 low as the best entry. Across all 156 dates
  the adjusted gap ranks it at +0.41 (+0.38 for the two-year endpoint) and the thirds in the right order (+43.6%, +36.6%, +32.6%), but all
  three cleared the hurdle at the median; Ratio B (+0.01) and the market composite (-0.05) rank it not at all, and the tiers out of order
  (BUY +66.3% first, then AVOID +38.6% ahead of ACCUMULATE +15.3% and WATCHLIST +9.1%).
- **The operating signals: wrong in 2015-2016, right in 2017.** The proxy composite ranks the return to the m12-24 average price at -0.31
  within 2015 and -0.38 within 2016, then +0.60 within 2017 (all dates: +0.39). After four batches in which the quarter's operating
  signals pointed the wrong way (2008 -0.49, 2009-2011 -0.83, 2012 -0.70), 2017 is the first year they ranked it the right way (the
  lowest reading, 1.50 on the Q3 FY18 print, came before the year's lowest returns). With every signal at its BEAR value (the sensitivity
  run before scoring) the four CHEAP dates and the FAIR one read RICH and would all have failed; the signals added nothing the price did not.
- **The theme, seen afterwards.** ECOMMERCE stayed on the watch list and DURABLE stood (retro/README.md, "WMT 2015-2017"); the stock
  re-rated through and after the registry's 2017-06-16 sell-off date, as a beneficiary rather than a casualty (2017-06-16's two-year return
  +50.5%). The label carried no price-state input, so it neither helped nor hurt the call; re-filing it as AMAZON-FEAR would have changed
  the label only.
- **The encoding calls, seen afterwards.** Reading the FY16 "relatively flat" as words (the +1-2% standing) would have moved 2015-10-23
  from FAIR to RICH and 2015-10-30 and 2015-12-11 from CHEAP to FAIR: all three returned +59% to +70% and beat SPY by 31-34pp, so they fail
  under that reading and hold or fail as encoded (two CHEAP held, the FAIR one failed). Reported EPS with GAAP ranges would have made
  2015-10-23 CHEAP (it would have held) and 2015-11-06 FAIR (it would still have failed). The constant-currency reading thus did better
  on these dates, which says nothing about the rule: it was decided before scoring, the dates are few and the re-rating swamped every
  call. The calls stay; changing a rule means a new method version tested elsewhere.

## 2018-2020 (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, tier AVOID (every date) | 157 | +30.0% | -6.9% to +72.4% | 75 | 55 | +23.7% | 79 |
| 2018 | 52 | +49.7% | +9.4% to +72.4% | 43 | 46 | +30.7% | 6 |
| 2019 | 52 | +35.4% | +18.5% to +61.4% | 30 | 9 | +27.7% | 22 |
| 2020 | 53 | +5.9% | -6.9% to +34.9% | 2 | 0 | +8.7% | 51 |
| FY18 anchor (to 2018-02-16) | 7 | +16.5% | +9.4% to +21.9% | 0 | 1 | +5.9% | 6 |
| FY19 guides (2018-02-21 to 2019-02-15) | 52 | +51.5% | +23.9% to +72.4% | 50 | 52 | +32.8% | 0 |
| FY20, FY19's EPS standing (2019-02-20 to 2020-02-14) | 52 | +30.0% | +17.3% to +45.4% | 23 | 2 | +24.1% | 29 |
| FY21 guide (2020-02-19 to 2020-05-15) | 13 | +28.0% | +21.0% to +34.9% | 2 | 0 | +19.0% | 11 |
| after the withdrawal (from 2020-05-20) | 33 | +1.9% | -6.9% to +8.3% | 0 | 0 | +1.0% | 33 |
| highest third by adjusted gap (-1.77 to -0.75) | 52 | +5.9% | | 19 | 19 | +14.4% | 33 |
| middle third (-2.22 to -1.77) | 52 | +42.4% | | 35 | 23 | +33.5% | 17 |
| lowest third (-2.54 to -2.22) | 53 | +28.9% | | 21 | 13 | +23.6% | 29 |

- **RICH held on 79 of 157 dates, almost all through the benchmark.** A RICH call expects the stock to miss the +32.2% hurdle and lag
  SPY. On the 69 dates from 2018-02-21 to 2019-06-14 it did neither: the dates under the FY19 guides ($82-106) returned +24% to +72% over
  two years and beat SPY on every one, by 3 to 48 points (SPY -9% to +58%), and those of February to June 2019 cleared the hurdle. From
  mid-2019 the stock kept rising, but SPY rose faster: the 40 dates held between 2019-06-21 and 2020-05-15 returned +17% to +32% while SPY
  returned +32% to +99% (2020-03-20, the COVID low); the misses among them (2019-08-02 to 2019-09-06, 2020-03-27 and 2020-04-09) cleared
  the hurdle. After the withdrawal the 33 dates from 2020-05-20 ($118-152) returned -7% to +8% and held every time. Three-year returns
  ran +8% to +80% (median +34.0%) and beat SPY on 47 of 157.
- **The two-year price landed above XBULL almost every time.** It landed nearest XBULL on 149 dates and BULL on 8 (from 2020-05-20), at
  1.05-1.76 times the BULL price and 1.22-1.93 times BASE: $107-157 two years on (as traded), against BULL prices that the decade's EPS
  CAGR kept at BASE's rate. Drawdowns were 14-26%, the lowest closes 2018-12-24's $85.82 and 2020-03-12's $104.05. The 2015-2017
  hypothesis carries on: a ten-year own-P/E window in which the multiple had been low capped every scenario multiple (the 90th percentile
  near 17x) below where the stock traded, and the stock re-rated past it. Here the call still held about half the time, because the
  benchmark rallied harder than this stock did from mid-2019; that is the outcome of the label's benchmark leg, not of the valuation.
  Test a percentile window that can see a regime change, or a cross-sectional multiple, on other tickers before any method change.
- **Within each year, cheaper entries still did better; across the three years the anchors told little.** The entry price ranks the
  return to the m12-24 average price at Spearman -0.80 within 2018, -0.98 within 2019 and -1.00 within 2020 (all dates: -0.87); the EPP gap
  at -0.90 over all dates. The adjusted gap ranks it at +0.28 and +0.38 within 2018 and 2019 but -0.79 within 2020, and -0.26 over all
  dates: its least negative third, mostly the COVID quarters after the withdrawal, returned the least (+5.9%). Ratio B, infinite on every
  date from 2019, ranks nothing.
- **The operating signals: right in 2019, wrong in 2020.** The proxy composite ranks the return to the m12-24 average price at +0.19
  within 2018, +0.55 within 2019 and -0.82 within 2020 (all dates: -0.24). Its 2020 readings were the strongest of any WMT batch (3.10 on
  Q2 FY21: comparable sales +9.0%, gross margin +63bp, operating margin +45bp, inventories 13 points behind sales), all from the pandemic's
  pull-forward of demand, and they came before the weakest returns. Over the six WMT batches the proxy composite has ranked the outcome the
  wrong way in 2008, 2009-2011, 2012, 2015, 2016 and 2020, and the right way in 2017, 2018 (weakly) and 2019. Hypothesis for the method,
  not a rule: test whether quarterly comparable-sales and margin signals carry information for a mature retailer on other tickers.
- **The encoding calls, seen afterwards.** None of the alternatives in retro/README.md ("WMT 2018-2020") moves a class or a tier, so the
  outcomes cannot tell them apart. The withdrawal mattered only to the text and to BASE (+9-12.5% on the COVID quarters), which could not
  bring the price within RICH's line. The calls were decided before scoring and stay; changing a rule means a new method version tested
  elsewhere.

## 2021-2023 (156 dates)

Scored on 2026-11-08, from the closes posted to 2026-11-06, after the point-in-time build (5748a2e) was pushed. The two-year horizons end
by 2025-12-29; the three-year horizons exist for the 148 dates to 2023-11-03. Prices are on the as-of share basis (the 2024 three-for-one
split undone).

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH (every date) | 156 | +63.9% | -0.9% to +132.9% | 85 | 144 | +32.4% | 12 |
| tier AVOID | 149 | +61.7% | -0.9% to +132.9% | 78 | 137 | +30.7% | 12 |
| tier WATCHLIST (2022-05-18 to 2022-07-08) | 7 | +68.9% | +61.3% to +74.9% | 7 | 7 | +36.5% | 0 |
| 2021 | 52 | +12.0% | -0.9% to +20.0% | 0 | 46 | +1.1% | 6 |
| 2022 | 52 | +63.9% | +11.3% to +102.7% | 33 | 46 | +32.4% | 6 |
| 2023 | 52 | +94.9% | +68.8% to +132.9% | 52 | 52 | +69.1% | 0 |
| FY20's EPS standing after the withdrawal (to 2021-02-12) | 6 | +3.1% | -0.9% to +5.2% | 0 | 0 | -4.2% | 6 |
| FY22, FY21's EPS standing (2021-02-19 to 2021-08-13) | 26 | +12.0% | +5.4% to +18.4% | 0 | 26 | +0.7% | 0 |
| FY22 guides (2021-08-18 to 2022-02-11) | 26 | +15.2% | +8.9% to +28.4% | 0 | 26 | +5.9% | 0 |
| FY23, FY22's EPS standing (2022-02-18 to 2022-05-13) | 13 | +25.6% | +16.8% to +32.0% | 0 | 7 | +9.2% | 6 |
| FY23 growth guides (2022-05-18 to 2023-02-17) | 40 | +78.8% | +56.3% to +118.2% | 40 | 40 | +37.4% | 0 |
| FY24 guides (from 2023-02-22) | 45 | +94.6% | +68.8% to +132.9% | 45 | 45 | +70.1% | 0 |
| highest third by adjusted gap (-1.54 to -1.25) | 52 | +83.3% | | 33 | 46 | +66.1% | 6 |
| middle third (-1.82 to -1.56) | 52 | +17.8% | | 16 | 46 | +6.8% | 6 |
| lowest third (-2.24 to -1.82) | 52 | +78.5% | | 36 | 52 | +36.7% | 0 |

- **RICH failed on 144 of 156 dates.** A RICH call expects the stock to miss the +32.2% hurdle and lag SPY. It held only on the six dates
  of January and February 2021 (two-year returns of -1% to +5%, 2 to 8 points behind SPY) and the six of 2022-04-08 to 2022-05-13 (+17% to
  +32%, 2 to 7 points behind). The other 2021 dates returned only +5% to +20% but beat SPY, which returned -8% to +13% through the 2022 bear
  market, by up to 19 points. From the Q1 FY23 print (2022-05-18) every date cleared the hurdle and beat SPY, by 16 to 85 points: the 40
  dates under the FY23 growth guides returned +56% to +118%, the 45 under the FY24 guides +69% to +133%. The
  seven WATCHLIST dates ($118-125, the period's cheapest entries) returned +61% to +75%. One-year returns ran -15% to +92% (median +13.3%,
  ahead of SPY on 103); three-year returns +13% to +180% (median +114.1%, ahead of SPY on 141 of 148).
- **The two-year price landed past BULL every time.** It landed nearest XBULL on 140 dates and BULL on 16, at 1.00-2.09 times the BULL price
  and 1.25-2.52 times BASE: $137-350 two years on (as traded on the as-of basis). Drawdowns within the two years were 11-26%, the lowest close
  2022-06-17's $118.29. For the third batch running the stock re-rated past every scenario multiple drawn from its own ten-year P/E window
  (the 90th percentile 23.5-24.3x): the 2015-2017 hypothesis carries on, now without the benchmark leg to rescue the call as it partly did in
  2019-2020. The outcomes record prices, not EPS, so they cannot say how much of the move was earnings and how much multiple. Hypothesis
  for the method, not a rule: test a P/E window that can register a regime change, or a cross-sectional multiple, on other tickers before
  any method change.
- **Within each year the rankings flip.** The entry price ranks the return to the m12-24 average price at Spearman -0.49 within 2021 and
  -0.58 within 2022 (cheaper entries did better) but +0.56 within 2023 (all dates: +0.39, the later and dearer entries rode the re-rating).
  The EPP gap ranks it at -0.83, -0.10 and +0.02 (all dates: -0.60). The adjusted gap ranks it at -0.45, -0.27 and +0.65 (all dates: -0.06),
  and its thirds are not ordered (+83%, +18%, +79%). Ratio B, infinite on 65 dates, ranks nothing.
- **The operating signals: wrong in 2021 and 2022, right in 2023.** The proxy composite ranks the return to the m12-24 average price at
  -0.52 within 2021, -0.69 within 2022 and +0.66 within 2023 (all dates: -0.12). Its highest readings (2.55-2.60, the lapping pandemic
  quarters and Q1 FY22) came before the weakest returns, and its lowest (1.55, the inventory glut of the Q1 and Q2 FY23 prints) before the strongest. Over
  the seven WMT batches the proxy composite has now ranked the outcome the wrong way in 2008, 2009-2011, 2012, 2015, 2016, 2020, 2021 and
  2022, and the right way in 2017, 2018 (weakly), 2019 and 2023. Hypothesis for the method, not a rule: for a mature retailer, quarterly
  comparable-sales and margin signals look contrarian more often than confirming; test it on other tickers before any change.
- **The encoding calls, seen afterwards.** Only reported EPS moves classes (retro/README.md, "WMT 2021-2023"): its 12 FAIR dates of 2023
  returned +89% to +133%, 40 to 85 points ahead of SPY, so FAIR (within 15 points of SPY) would have failed on every one as well. The
  divestiture and growth-guide alternatives move only tiers, and on dates that all cleared the hurdle. The calls were decided before
  scoring and stay; changing a rule means a new method version tested elsewhere.

## 2024-2026 (149 dates; outcomes so far)

Scored on 2026-11-08, from the closes posted to 2026-11-06, after the point-in-time build (b2877b9) was pushed. The horizons are partial:
two-year returns exist for the 44 dates to 2024-11-01, one-year for the 96 to 2025-10-31 and six-month for the 122 to 2026-05-01; the 26
dates after that have none, and 2026-11-06 has no later close, so no outcome file. Prices are on each date's own share basis (the split
of 2024-02-26 undone for the eight earlier dates). Every date was RICH and AVOID.

| Group | Dates | Median return | Range | Cleared the hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| two years (2024-01-05 to 2024-11-01) | 44 | +83.4% | +31.1% to +138.9% | 43 | 40 | +69.9% | 1 |
| two years, before the split (to 2024-02-21) | 8 | +122.7% | +115.5% to +138.9% | 8 | 8 | +83.8% | 0 |
| two years, after the split (2024-03-01 to 2024-11-01) | 36 | +73.6% | +31.1% to +123.0% | 35 | 32 | +67.5% | 1 |
| one year (to 2025-10-31; hurdle +15%) | 96 | +30.8% | +3.1% to +84.7% | 82 | 77 | | |
| one year, 2024 dates | 52 | +42.2% | +20.5% to +84.7% | 52 | 52 | | |
| one year, 2025 dates | 44 | +23.0% | +3.1% to +52.4% | 30 | 25 | | |
| six months (to 2026-05-01; hurdle +7.2%) | 122 | +18.8% | -19.2% to +49.5% | 82 | 81 | | |
| six months, 2026 dates | 18 | -9.9% | -19.2% to -0.4% | 0 | 0 | | |

- **RICH failed again wherever two years have passed.** The 44 dates of January to October 2024 returned +31% to +139% over two years and
  cleared the +32.2% hurdle on 43; SPY returned +24% to +50%, so the stock beat it on 40, by up to 100 points. The call held on one date
  (2024-10-04: +31.1%, 5.8 points behind SPY); 2024-08-30, 2024-09-06 and 2024-09-13 also trailed SPY by about 3 points but cleared the
  hurdle. The eight dates before the split ($157-174 as traded) returned +116% to +139%. The two-year price landed past XBULL on all 44, at
  1.32-1.95 times the XBULL price and 1.66-2.38 times BULL; drawdowns within the two years were 22-24%.
- **One year on, the 2025 entries were already weaker.** Every 2024 date returned +20% to +85% over one year and beat SPY; of the 44 dates
  of 2025 with a one-year return, 19 (2025-05-23 to 2025-10-17, $94-108) trailed SPY by up to 14 points, returning +3% to +26%.
- **The first RICH dates that look right, over six months only.** The 18 dates of January to April 2026 ($103-134, 36-51x guided EPS, the
  85th-100th percentile of the window) returned -0.4% to -19.2% over six months, 10 to 35 points behind SPY; the 2025-11-28 to 2025-12-26
  dates had already trailed it. Six months is the horizon the archive weights least, and the two-year verdicts of these dates fall in
  2028: treat this as unscored.
- **What ranked the outcome.** Over the 96 dates with a one-year return, the EPP gap ranks it at Spearman -0.86 (the less the price sat
  above the floor, the better), the P/E percentile at -0.36, the adjusted gap at +0.64 and the proxy composite at +0.66 (both the right
  way); over the 44 two-year dates the EPP gap ranks the return to the m12-24 average price at -0.96 and the adjusted gap and proxy
  composite at -0.34 and -0.57. In this regime the distance from the floor sorted the entries well even though every class was wrong.
- **The 2015-2017 hypothesis, a fourth batch.** From 2015 the stock re-rated past every multiple its own ten-year P/E window allowed: on the
  44 dates scored over two years the 90th percentile was 24-25x while the stock traded at 24-39x, and every two-year price landed past
  XBULL. The window only catches up as the re-rating enters it (its 90th percentile reaches 25-35x in 2025 and 35-39x in 2026). Hypothesis for the
  method, not a rule: an own-history P/E window cannot register a lasting re-rating of a mature company; test a window that can see a
  regime change, or a cross-sectional multiple, on other tickers before any method change.
- **The encoding calls, seen afterwards.** Only reported EPS moves classes (retro/README.md, "WMT 2024-2026"): its eight FAIR and CHEAP
  dates of early 2024 are the ones that returned +116% to +139% over two years, so a cheaper class would have been right there. That is a
  hindsight observation on eight dates and changes nothing: the calls were decided before scoring and stay; changing a rule means a new
  method version tested elsewhere.
