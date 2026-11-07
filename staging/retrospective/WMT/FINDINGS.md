# WMT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the WMT weekly dates: 209 from 2008-01-04 to 2011-12-30. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: 339c071; 2009-2011: 7be709f). Outcomes were computed on 2026-11-07 from the closes posted to 2026-11-06; the two-year
horizons end by 2013-12-30 (three-year: 2014-12-30).
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
