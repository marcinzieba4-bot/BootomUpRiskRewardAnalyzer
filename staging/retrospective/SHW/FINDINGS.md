# SHW retrospective findings (hindsight)

Patterns seen in `outcome.json` for the SHW weekly dates: 522 from 2008-01-04 to 2017-12-29. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: c486e3a; 2009-2011: c951197; 2012-2014: bf0acb6; 2015-2017: 0cc2306). Prices run to 2026-11-05 (2008, 2012-2014) and
2026-11-06 (2009-2011, 2015-2017); the two-year horizons end by 2019-12-27 (three-year: 2020-12-29).
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

## 2012-2014 (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH (all) | 157 | +53.8% | +4.5% to +106.8% | 136 | 151 | +37.3% | 5 |
| legacy tier AVOID (all) | 157 | +53.8% | +4.5% to +106.8% | 136 | 151 | +37.3% | 5 |
| 2012 | 52 | +65.8% | +41.3% to +106.8% | 52 | 52 | +44.1% | 0 |
| 2013 | 52 | +55.3% | +28.4% to +85.9% | 49 | 52 | +41.2% | 0 |
| 2014 | 53 | +37.8% | +4.5% to +59.1% | 35 | 47 | +30.2% | 5 |
| to 2014-10-24 | 147 | +54.7% | +23.9% to +106.8% | 136 | 147 | +38.3% | 0 |
| from the Q3 2014 print (2014-10-29) | 10 | +12.0% | +4.5% to +14.4% | 0 | 4 | +13.4% | 5 |
| lowest third by adjusted gap (-1.68 to -1.13) | 52 | +53.9% | | | | +46.6% | |
| middle third (-1.13 to -0.84) | 52 | +68.1% | | | | +38.2% | |
| highest third (-0.81 to -0.27) | 53 | +46.2% | | | | +32.7% | |

- **The call failed on 152 of 157 dates and held only at the very end.** RICH and AVOID on every date, and the stock returned +4.5% to
  +107% over two years (median +54%), cleared the hurdle on 136 and beat SPY on 151. Every date to 2014-10-24 beat SPY, by 2-63pp; the
  eleven of them under the hurdle (five from 2013-09-27 to 2014-01-17, six from 2014-09-19 to 2014-10-24) still returned +24% to +30%. From the Q3 2014
  print the two-year returns fell to +4.5% to +14.4% (SHW closed at $292 on 2015-05-19 and $219 on 2015-09-29, 25% lower): none cleared
  the hurdle and five lagged SPY, by 1.5-8.5pp, so the call held on 2014-11-07, 2014-12-12, 2014-12-19, 2014-12-26 and 2014-12-31
  (2014-12-05 tied SPY at -0.0pp and counts as a miss). One-year returns ran -0.4% to +73% (median +26.5%, ahead of SPY on 122);
  three-year returns +31% to +193% (median +71%), ahead of SPY on all 157. Over 2008-2014 the RICH call held on 6 of 340 RICH dates.
- **The two-year price landed beyond XBULL until 2014.** It landed nearest XBULL on 133 dates and BULL on 24 (all 2014). For the 2012
  dates the two-year price ($177-265) was 1.09-1.53 times XBULL ($127-200); for 2013 0.91-1.37 times; for 2014 0.67-1.02 times XBULL and
  1.10-1.52 times BULL. No path came near BEAR: the lowest close of every window was 2.0-2.8 times the BEAR price, and drawdowns ran 11-25%.
- **The multiple band re-rated, two to three years late.** Hypothesis for the method, not a rule. The price ran 17.6-30.2x the guided
  year (the 87th-100th percentile of its own ten-year range) while the window's median moved only from 14.1x to 15.8x and its 90th
  percentile from 17.4x to 24.1x, as the stock's own recent multiples entered it. Unlike 2008-2011 the anchor was no trough (FY12 guides
  $5.52-6.45, FY13 $7.15-7.50, FY14 $8.22-8.78, each above the year before), so the binding input was the band. The hurdle was missed only
  at 24-30x (1.6-1.9 times the window median) and the call held only at 27-30x (1.7-1.9 times), after the price had nearly tripled from
  $93; it cleared at 17.6-26.7x. Across the 157 dates the entry P/E ranks the two-year return at Spearman -0.80 (the m12-24 average price:
  -0.68): the multiple ranked the dates the right way while its level read RICH from 1.25 times the median. With 2009-2011 this makes one
  hypothesis: a band drawn only from the stock's own past decade cannot hold a re-rating that runs for years. Test a band that can re-rate on
  other tickers and periods before any method change; never fit it to SHW's outcomes.
- **Within the period, buying lower ranked the outcome; the composite gap did not.** The entry price ranks the return to the m12-24
  average price at Spearman -0.72 (the two-year endpoint: -0.58), the EPP gap at -0.51 (-0.53) and the conservative two-year case at
  +0.42 (+0.60), all the right way; Ratio B at -0.10 (-0.25), the right way but weak. The adjusted gap ranks it at -0.39 (-0.05) and the
  proxy composite at -0.29 (-0.13), the wrong way: the most-overvalued third returned +54% over two years, the middle +68%, the least
  overvalued +46%. The adjusted gap has now ranked SHW's dates -0.35 (2008), +0.70 (2009-2011) and -0.39 (2012-2014): for one stock it
  says when to buy, not whether, and not reliably even that.
- **The encoding calls, seen afterwards.** Every alternative in retro/README.md ("SHW 2012-2014") moves no class and no tier: BASE on
  reported growth, the Consumer Group signal at BEAR or XBULL, the pre-tax margin thresholds with 2000 at GAAP, FY2012 at GAAP $6.02,
  FY2011 before the IRS charge, and the FY2013 guide and Q4 2013 sales guide with or without Comex. No encoding choice reaches the result:
  the level of the call failed on 152 dates and held on 5, with no input deciding either. The calls were decided before scoring and stay.

## 2015-2017 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 125 | +38.7% | +3.8% to +81.6% | 91 | 104 | +27.0% | 17 |
| class FAIR | 22 | +58.8% | +31.8% to +73.3% | 21 | 22 | +32.8% | 4 |
| class CHEAP | 9 | +47.9% | +43.5% to +55.2% | 9 | 9 | +18.8% | 9 |
| legacy tier ACCUMULATE | 13 | +48.4% | +42.6% to +68.7% | 13 | 13 | +19.0% | 9 |
| legacy tier WATCHLIST | 26 | +57.4% | +31.8% to +73.3% | 25 | 26 | +40.9% | 4 |
| legacy tier AVOID | 117 | +38.3% | +3.8% to +81.6% | 83 | 96 | +25.9% | 17 |
| 2015 (RICH 51, FAIR 1) | 52 | +28.6% | +3.8% to +61.9% | 21 | 35 | +7.6% | 17 |
| 2016 (RICH 43, FAIR 9) | 52 | +50.2% | +32.2% to +81.6% | 52 | 48 | +38.6% | 3 |
| 2017 to 2017-07-14 (all RICH) | 28 | +38.6% | +23.6% to +45.8% | 25 | 28 | +31.6% | 0 |
| 2017-07-21 to 2017-10-20 (FAIR 11, RICH 3) | 14 | +54.6% | +31.8% to +63.5% | 13 | 14 | +28.0% | 1 |
| from 2017-10-25 (CHEAP 9, FAIR 1) | 10 | +47.9% | +42.6% to +55.2% | 10 | 10 | +18.8% | 9 |
| lowest third by adjusted gap (-1.13 to -0.62) | 52 | +28.7% | | | | +7.6% | |
| middle third (-0.61 to -0.25) | 52 | +45.8% | | | | +29.8% | |
| highest third (-0.24 to +0.60) | 52 | +48.4% | | | | +30.5% | |

- **RICH held on the 17 dates of early 2015 and failed on the other 108.** The stock returned +3.8% to +82% over two years (median +42%),
  cleared the hurdle on 121 and beat SPY on 135. The 17 held RICH calls run from 2015-01-09 to 2015-04-17, plus 2015-05-15 and 2015-05-29:
  two-year returns of +3.8% to +18.5%, 0.2-11.4pp behind SPY, as SHW fell 25% from its May 2015 high to $218.94 on 2015-09-29. Every
  other 2015 date under the hurdle (to 2015-08-21) still beat SPY. From 2016 every date cleared the hurdle but four of 2017
  (2017-01-27, 2017-05-26, 2017-06-02 and 2017-07-21, +24% to +32%), and only four (2016-04-29 to 2016-05-20) lagged SPY, by
  0.4-5.5pp. The FAIR call held on 4 of 22 (2016-02-05 to 2016-02-19 and 2017-07-21, 7-13pp ahead of SPY); the other 18 beat SPY by
  more than 15pp (15.5-40pp). One-year returns had a median of +15% (-11% to +65%); three-year returns ran +33% to +140% (median +68%),
  ahead of SPY on 155 of 156. Over 2008-2017 the RICH call held on 23 of 465 RICH dates.
- **The CHEAP call held on all 9 dates, through the acquisition, not the franchise.** From the Q3 2017 print BASE took the quarter's
  +37.4% reported growth, 32.8 points of it Valspar's acquired sales, as +41.1%/yr EPS growth on a FY2017 anchor that already held seven
  months of Valspar (retro/README.md, "SHW 2015-2017"). The two-year price ($572-593) landed at 0.93-0.96 times that BASE price
  ($618-621), the stock returning +44% to +55%, 19-30pp ahead of SPY. Every alternative that takes Valspar out of the inputs, decided and
  measured before scoring, turns those dates RICH or FAIR, and seen afterwards each turns held calls into failed ones: BASE on core growth
  (21 dates moved; 10 held before, 0 after), the Valspar items at GAAP (26; 10 and 0), the FY2017 anchor without Valspar (13; 8 and 0).
  The rule that put the acquisition into BASE has stood since 2008 (Q4 2010's +18.2% with 8.7 points of acquisitions) and stays; that it
  scored well here is one acquisition of one stock, and a growth rate that counts an acquisition's sales against an anchor that already
  includes the acquisition overstates growth by construction. Hypothesis for the method, not a rule: a fallback growth rate should net out
  stated acquired sales when the anchor year includes them. Test it on other tickers' acquisitions before any method change; never fit it
  to SHW's outcomes, which here favour the double count.
- **The band caught up; the price landed nearest BULL.** It landed nearest BULL on 134 dates, XBULL on 11 (2015-2016) and BASE on 11
  (2017's CHEAP dates and two more), at 0.64-0.90 times XBULL and 0.82-1.39 times BULL: the first SHW batch since 2008 where no two-year
  price went beyond XBULL. The window's median P/E rose from 15.8x to 20.8x and its 90th percentile held at 24-25x, so the bands now
  spanned the multiples the stock traded at (20-31x the guided year). No path came near BEAR: the lowest close of every window was
  1.9-2.7 times the BEAR price; drawdowns ran 15-25%.
- **RICH held only at the top of the band.** The held RICH calls entered at 24.7-31.3x the guided year, 1.55-1.98 times the window
  median and its 92nd-100th percentile (the January 2015 dates on FY2014's $8.775 until the Q4 2014 print); the failed ones at 20.3-26.1x,
  1.02-1.60 times the median and its 54th-97th percentile. Every date that missed the hurdle entered at 1.11-1.98 times the median; every
  date that cleared it at 0.99-1.49 times. With 2012-2014 (missed at 1.6-1.9 times the median, cleared at 17.6-26.7x) this sharpens the
  band hypothesis of 2009-2014: the RICH line sits about where the multiple is merely above its median, while SHW's two-year returns turned
  poor only near 1.5-2 times it. Test where the RICH line should sit on other tickers and periods before any method change; never fit it to
  SHW's outcomes.
- **This time the ranking ran the right way on most measures.** Across the 156 dates the entry P/E ranks the return to the m12-24
  average price at Spearman -0.92 (the two-year endpoint: -0.63), the EPP gap at -0.71 (-0.51), Ratio B at -0.65 (-0.71), the
  conservative two-year case at +0.50 (+0.50) and the adjusted gap at +0.35 (+0.52), all the right way; the entry price at -0.26
  (-0.20); the proxy composite at -0.09 (-0.09), nothing. The least-overvalued third by adjusted gap returned +48% against +29% for the
  most-overvalued. The adjusted gap has now ranked SHW's dates -0.35 (2008), +0.70 (2009-2011), -0.39 (2012-2014) and +0.35 (2015-2017);
  the entry multiple has ranked them the right way in the last two batches (-0.68 and -0.92 on the m12-24 outcome).
- **The encoding calls, seen afterwards.** Of the alternatives in retro/README.md ("SHW 2015-2017"), the Valspar ones decide the second
  half of 2017 (above). The Consumer Group signal at BEAR moves 17 classes toward RICH and would have held on 0 of them (10 held as
  built); at XBULL 5 RICH dates of 2016 turn FAIR, one of which would have held. The pre-tax margin thresholds with 2000 at GAAP move 2
  (one FAIR date to CHEAP would have held; 2016-10-26 RICH to FAIR would not). The revenue reclassification taken out of BASE moves 3
  toward RICH, all of which would have failed (one FAIR held as built). FY2016 at $12.45, BASE on reported growth and the FY2015 range not
  carried move nothing. The calls were decided before scoring and stay; changing a rule means a new method version tested elsewhere.
