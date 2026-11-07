# WMT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the WMT weekly dates: 53 from 2008-01-04 to 2008-12-31. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: 339c071). Prices run to 2026-11-06; the 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30).
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
