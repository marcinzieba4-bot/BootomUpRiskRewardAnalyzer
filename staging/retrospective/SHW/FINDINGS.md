# SHW retrospective findings (hindsight)

Patterns seen in `outcome.json` for the SHW weekly dates: 209 from 2008-01-04 to 2011-12-30. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: c486e3a; 2009-2011: c951197). Prices run to 2026-11-05 (2008) and 2026-11-06 (2009-2011); the two-year horizons end by
2013-12-30 (three-year: 2014-12-30).
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 19 | +27.9% | +10.0% to +50.1% | 7 | 19 | +8.5% | 19 |
| class FAIR | 2 | +41.1% | +39.3% to +41.1% | 2 | 2 | +8.5% | 0 |
| class RICH | 32 | +37.7% | +18.9% to +59.1% | 23 | 27 | +24.3% | 1 |
| legacy tier BUY | 28 | +35.6% | +10.0% to +59.1% | 16 | 28 | +10.2% | 19 |
| legacy tier ACCUMULATE | 13 | +39.7% | +33.2% to +55.9% | 13 | 10 | +26.8% | 0 |
| legacy tier WATCHLIST | 6 | +33.2% | +22.0% to +45.5% | 3 | 4 | +19.4% | 1 |
| legacy tier AVOID | 6 | +24.8% | +18.9% to +26.6% | 0 | 6 | +10.8% | 0 |
| FY07 guide $4.725 (to 2008-01-25) | 4 | +16.5% | +10.0% to +19.2% | 0 | 4 | +3.5% | 4 |
| FY08 guide $5.075 (2008-01-30 to 2008-03-20) | 8 | +26.6% | +17.8% to +35.6% | 1 | 8 | +9.4% | 8 |
| FY08 guide $4.775 (2008-03-28 to 2008-05-30) | 10 | +39.3% | +29.8% to +50.1% | 9 | 10 | +10.2% | 7 |
| FY08 guide $3.85 (2008-06-06 to 2008-10-10) | 19 | +35.7% | +18.9% to +59.1% | 11 | 19 | +23.9% | 0 |
| FY08 guide $4.07 (from 2008-10-17) | 12 | +39.7% | +31.7% to +55.9% | 11 | 7 | +26.8% | 1 |
| January-September | 39 | +30.8% | +10.0% to +59.1% | 19 | 39 | +10.8% | 19 |
| October-December | 14 | +43.0% | +31.7% to +55.9% | 13 | 9 | +26.8% | 1 |

- **CHEAP held on all 19 dates; RICH failed on 31 of 32.** Every CHEAP date (January to 2008-04-23, and 2008-05-23 and 2008-05-30)
  beat SPY over two years, by 24-60pp, though only 7 cleared the hurdle (two-year returns +10% to +50%). From June the class turned
  RICH and the stock kept outperforming: two-year returns of +19% to +59% (median +38%), the hurdle cleared on 23 of 32 and SPY beaten on
  27. The one RICH date that held, 2008-11-28, returned +31.7%, just under the hurdle, and lagged SPY's rebound by 5pp. The two FAIR
  dates (2008-05-02, 2008-05-09) beat SPY by 54-56pp, outside the ±15pp band. From January to September SPY returned -19% to -1% over
  the two years and SHW +10% to +59%; from October SPY returned +8% to +57% and SHW +32% to +56%, 14pp behind to 38pp ahead. One-year
  returns had a median of +6.5% (-13.8% to +22.7%); three-year returns ran from +25% to +89% (median +60%), ahead of SPY on all 53 dates.
- **The two-year price landed nearest BULL on every RICH-era date.** The two-year price ($59-84) landed nearest BULL on 32 dates, BASE on
  19 and BEAR on 2. For the RICH dates it was 1.14-1.38 times BASE and 0.86-1.12 times BULL ($72-90); for the CHEAP dates 0.78-1.15 times
  BASE and 0.66-0.88 times BULL ($88-96). The lowest close of every window was 2009-03-06's $42.98 (as traded), a 30-32% drawdown: it
  touched the BEAR price of January-May ($43-46; 0.93-1.00 times) and stayed above the BEAR of June-December ($35-37).
- **The class followed the EPS guide, and the guide was the trough.** The P/E window hardly moved all year (median 13.5-13.7x); what
  moved was the current-FY EPS, cut from $5.075 to $4.775 (2008-03-24) and $3.85 (2008-06-03). The price held at $47-63, so the same
  price that read 10-12x (CHEAP) in January-May read 13-16x (up to the 96th percentile, RICH) from June, with BULL cut from $88-96 to
  $72-75. The market priced through the guided year. Hypothesis for the method, not a rule: a current-year EPS anchor reads a cyclical
  turn backwards. XOM in 2008 anchored on a peak year (FY07) and read CHEAP before a fall; SHW anchored on a guided trough (FY08) and
  read RICH before a recovery. Both point at the same input: the year the EPP and the multiple are anchored on, for businesses whose own
  10-K ties demand to a cycle (SHW: "segments of the economy that are cyclical in nature, particularly segments relating to construction,
  housing and manufacturing"). Test a normalized anchor on other tickers and other periods before any method change; never fit it to
  SHW's or XOM's outcomes.
- **Within the year the signals ranked the outcome the wrong way.** Across the 53 dates the entry price ranks the return to the m12-24
  average price at Spearman -0.46 (the two-year endpoint: -0.45). The proxy composite ranks it at -0.64: it read 2.35 on the 16 dates to
  2008-04-18 (median two-year return +27%), 1.65 from the Q1 2008 print (comparable-store sales -6.5% and -4.5% and the pre-tax margin
  -297bp and -230bp at BEAR) and 1.45 from Q3 2008, so the weakest readings came before the best returns. The adjusted gap ranks it at
  -0.35, the EPP gap at +0.28 and Ratio B at +0.33, all the wrong way. One stock through one crash mostly tests "buy lower"; ranking the
  dates says when to buy, not whether.
- **The encoding calls, seen afterwards.** The alternatives in retro/README.md ("SHW") move only May-July classes. Seen against the
  outcomes: BASE on reported growth would have turned 2 FAIR dates CHEAP (both would have held) and 2 RICH dates FAIR (both would still
  miss); the pre-tax margin thresholds with 2000 at GAAP would have held on 5 more dates; the Consumer Group signal at XBULL on 6 more,
  at BEAR on 3 fewer. None reaches 2008-07-18 to 2008-12-31, where 24 of the 31 failed RICH calls sit. DURABLE changes only the label ("QUALITY,
  PRICED FOR PERFECTION" on the RICH dates); the price state, not the label, failed. The calls were decided before scoring and stay;
  changing a rule means a new method version tested elsewhere.

## 2009-2011 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 151 | +84.4% | +16.7% to +149.7% | 142 | 144 | +48.3% | 0 |
| class FAIR | 5 | +114.0% | +92.8% to +159.1% | 5 | 5 | +74.9% | 0 |
| legacy tier ACCUMULATE | 4 | +145.7% | +86.0% to +159.1% | 4 | 3 | +134.5% | 0 |
| legacy tier WATCHLIST | 22 | +106.5% | +44.0% to +149.7% | 22 | 19 | +70.1% | 0 |
| legacy tier AVOID | 130 | +77.5% | +16.7% to +142.5% | 121 | 127 | +44.7% | 0 |
| 2009 (all RICH) | 52 | +52.3% | +16.7% to +95.0% | 43 | 45 | +38.0% | 0 |
| 2010 (all RICH and AVOID) | 52 | +84.0% | +52.1% to +118.1% | 52 | 52 | +40.6% | 0 |
| 2011 (RICH 47, FAIR 5) | 52 | +119.6% | +92.8% to +159.1% | 52 | 52 | +90.9% | 0 |
| lowest third by adjusted gap (-2.50 to -1.68) | 52 | +53.4% | | | | +32.2% | |
| middle third (-1.65 to -1.09) | 52 | +90.7% | | | | +56.3% | |
| highest third (-1.07 to -0.20) | 52 | +111.2% | | | | +74.7% | |

- **Every call failed.** RICH on 151 dates and FAIR on 5, and the stock returned +17% to +159% over two years (median +89%), cleared the
  hurdle on 147 and beat SPY on 149. The seven that lagged SPY are all from January to early May 2009 (by 0.5-11.5pp, while returning
  +44% to +95%); the nine under the hurdle are August to early October 2009 (+17% to +31%). From 2010 every date cleared the hurdle and
  beat SPY, by 27-98pp (2010) and 57-105pp (2011). The five FAIR dates of 2011 returned +93% to +159%, 76-104pp ahead of SPY. Three-year
  returns ran +64% to +216% and beat SPY on all 156 dates. The legacy tier ranked them the right way round (AVOID +78%, WATCHLIST +107%,
  ACCUMULATE +146%) but never left the cautious tiers.
- **The two-year price landed at or beyond XBULL.** It landed nearest XBULL on 152 dates and BULL on 4 (2009-01-09, 2009-01-16, 2009-08-21, 2009-09-25). In 2010 it was
  0.96-1.52 times the XBULL price and in 2011 1.25-1.56 times ($154-195 against XBULL's $105-127): beyond the scenario that compounds
  the decade's best two-year EPS run at the 90th-percentile multiple of the stock's own decade. The lowest close of any window was
  2009-03-06's $42.98; no path came near BEAR after March 2009 (the lowest close 1.16-2.17 times the BEAR price; drawdowns 13-28%).
- **A tight own-history multiple capped the bands.** Hypothesis for the method, not a rule. SHW's P/E over 1999-2010 ranged little
  (10th to 90th percentile about 11.6x to 15-17x), so BULL and XBULL multiples sat at 14-17x, and the guided EPS anchor of 2009-2011
  ($3.50-4.85) put the price at 12-20x, the top of that range. The market paid more than the decade's ceiling for the same company
  through and after the recovery. Two inputs read the recovery backwards together: the guided trough year as the anchor (the 2008
  finding) and a P/E window that cannot hold a multiple above its own decade's range. Test an anchor and a multiple band that can
  re-rate on other tickers and periods before any method change; never fit either to SHW's outcomes.
- **The relative ranking held; the level did not.** Across the 156 dates the adjusted gap ranks the return to the m12-24 average price
  at Spearman +0.70 (the two-year endpoint: +0.76), Ratio B at -0.59 and the EPP gap at -0.33, all the right way: the least-overvalued
  third returned +111% over two years against +53% for the most-overvalued third. The proxy composite barely ranks it (+0.12); the entry
  price ranks it +0.49, because the stock kept compounding (later dates had better returns). In 2008 the same adjusted gap ranked the
  outcome the wrong way (-0.35): one stock through one cycle says when to buy, not whether.
- **The encoding calls, seen afterwards.** The alternatives in retro/README.md ("SHW 2009-2011") move at most 10 classes, mostly from RICH to
  FAIR; a FAIR call would have held on one of them (2009-03-06, 3.7pp behind SPY) and failed on the rest; the IRS-settlement guide and the Good Friday print move no class. No encoding
  choice of this batch reaches the result: the level of the call, not an input, failed. The calls were decided before scoring and stay.

