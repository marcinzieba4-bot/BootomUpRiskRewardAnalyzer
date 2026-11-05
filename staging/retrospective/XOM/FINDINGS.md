# XOM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the XOM weekly dates: 53 from 2008-01-04 to 2008-12-31. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: ae6e2c7). Prices run to 2026-11-04; the 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30).
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 53 | -18.7% | -32.2% to +8.6% | 0 | 0 | -18.4% | 0 |
| legacy tier BUY | 53 | -18.7% | -32.2% to +8.6% | 0 | 0 | -18.4% | 0 |
| FY06's $6.55 anchor (to 2008-01-25) | 4 | -17.7% | -21.4% to -15.0% | 0 | 0 | -17.1% | 0 |
| FY07's $7.28, Q4 2007 print (2008-02-01 to 2008-04-25) | 13 | -19.3% | -24.2% to -15.4% | 0 | 0 | -19.1% | 0 |
| FY07's $7.28, Q1 2008 print (2008-05-02 to 2008-07-25) | 13 | -27.4% | -32.2% to -20.7% | 0 | 0 | -21.9% | 0 |
| FY07's $7.28, Q2 2008 print (2008-08-01 to 2008-10-24) | 13 | -17.1% | -22.5% to +8.6% | 0 | 0 | -14.9% | 0 |
| FY07's $7.28, Q3 2008 print (from 2008-10-31) | 10 | -2.5% | -9.4% to +1.0% | 0 | 0 | -14.3% | 0 |
| January-September | 39 | -21.0% | -32.2% to -14.5% | 0 | 0 | -19.1% | 0 |
| October-December | 14 | -1.3% | -15.4% to +8.6% | 0 | 0 | -13.6% | 0 |

- **CHEAP and BUY on every date; the call failed on all 53.** No date cleared the hurdle and none beat SPY over two years. From January
  to September SPY returned -19% to -1% over the two years and XOM lagged it by 0.5-18.2pp, returning -32.2% to -14.5%; from October SPY
  returned +8% to +57% and XOM -15.4% to +8.6%, 23-59pp behind. One-year returns had a median of -11% (-27% to +14%); three-year returns
  ran from -13% to +31% (median +2%), ahead of SPY on 10 of 53 dates, all from February to mid-September 2008.
- **Every two-year price landed nearest BEAR, but no path reached it.** The two-year price ($57-73) was 1.35-1.85 times the BEAR price
  ($38-42), 0.29-0.64 times BASE and 0.20-0.36 times BULL. The lowest close inside each two-year window ($57-62: 2009-03-05 for the
  earlier dates, mid-2010 for the later ones) stayed 1.35-1.64 times above BEAR, after drawdowns of 31-36%. The outcome sits between
  BEAR and the EPP floor: the two-year price was 0.65-0.92 times the floor, the lowest close 0.65-0.79 times.
- **The scenario band sat above every price the stock reached.** From the Q4 2007 print BASE was $178-207 and BULL $257-292 (BASE
  growth +32-43%/yr, BULL equal to BASE); the highest close in any window was $94.56 (2008-05-20), 0.88 times the lowest BASE of January
  and half of the BASE from February on. Hypothesis for the method, not a rule: for a commodity producer, the no-guide rules anchor on
  the last full year's EPS, which at a price peak is a peak, and the revenue fallback carries the commodity price into BASE; the
  ten-year P/E window then prices that peak at multiples the stock earned on trough earnings (1998-2002 lows of 15-27x on $1.19-2.37
  of EPS), so the bands assume a mean reversion in the multiple that a cyclical's earnings undo. The BASE call itself did not decide the
  class (BASE on production growth, -5.5% to +3.3%/yr, keeps every date CHEAP; retro/README.md, "XOM"). Test it on other cyclicals and
  on other periods before any method change; never fit it to XOM's outcomes.
- **The entry price and the floor distance ranked the endpoint-robust outcome; the composites did not.** Across the 53 dates the entry
  price ranks the return to the m12-24 average price at Spearman -0.94, the EPP gap at -0.87 and Ratio B at -0.86 (the two-year endpoint:
  -0.78, -0.67, -0.60). The adjusted gap ranks it at +0.41, the wrong way, and the proxy composite at -0.15: it read 2.00 on the four
  January dates (median two-year return -18%), 2.65 on the 13 of the Q4 2007 print (-19%) and 2.10 on the 36 from the Q1 2008 print
  (-18%). The production signal at BEAR from May (-5.6% to -8.2%) and the revenue signal at XBULL (+30-40%) pulled against each other
  and netted to 2.10. One stock through one crash mostly tests "buy lower"; ranking the dates says when to buy, not whether.
- **The encoding calls, seen afterwards.** None of the alternatives in retro/README.md ("XOM") changes a 2008 class or tier, so the
  outcomes say nothing about them. CYCLICAL (the first ticker not filed DURABLE) changes only the label, which read "CYCLICAL, RISK
  PRICED IN" on all 53 dates; the price state, not the label, failed. The calls were decided before scoring and stay; changing a rule
  means a new method version tested elsewhere.

## 2009-2012 (209 dates)

Scored only after the point-in-time build was committed and pushed (12ca906). Two-year horizons end by 2014-12-31.

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| all | 209 | +22.4% | +1.8% to +57.6% | 46 | 58 | +10.5% | 52 |
| class CHEAP | 148 | +22.9% | +1.8% to +57.6% | 35 | 33 | +9.2% | 40 |
| class FAIR | 28 | +18.2% | +4.4% to +42.2% | 3 | 3 | +8.2% | 1 |
| class RICH | 33 | +27.3% | +4.2% to +40.0% | 8 | 22 | +18.2% | 11 |
| tier BUY | 90 | +23.6% | +1.8% to +57.5% | 21 | 20 | +9.8% | 26 |
| tier ACCUMULATE | 74 | +20.4% | +5.0% to +57.6% | 12 | 11 | +8.8% | 14 |
| tier WATCHLIST | 20 | +11.7% | +4.2% to +46.4% | 3 | 3 | +9.7% | 10 |
| tier AVOID | 25 | +29.0% | +20.1% to +40.0% | 10 | 24 | +20.1% | 2 |
| 2009 (all CHEAP) | 52 | +16.2% | +1.8% to +38.2% | 3 | 3 | +5.6% | 6 |
| 2010 CHEAP | 30 | +47.2% | +27.6% to +57.6% | 28 | 30 | +34.3% | 30 |
| 2010 FAIR | 3 | +35.0% | +33.8% to +42.2% | 3 | 3 | +24.1% | 1 |
| 2010 RICH | 19 | +30.0% | +21.9% to +40.0% | 8 | 19 | +20.3% | 0 |
| 2011 CHEAP | 48 | +18.7% | +5.0% to +35.0% | 2 | 0 | +9.6% | 2 |
| 2011 RICH | 4 | +20.4% | +20.1% to +21.7% | 0 | 3 | +11.3% | 1 |
| 2012 CHEAP | 18 | +22.5% | +12.6% to +35.3% | 2 | 0 | +8.8% | 2 |
| 2012 FAIR | 25 | +17.7% | +4.4% to +29.3% | 0 | 0 | +7.6% | 0 |
| 2012 RICH | 10 | +13.4% | +4.2% to +16.7% | 0 | 0 | +11.7% | 10 |

- **The call held on 52 of 209 dates; XOM lagged the market's rebound on most of the rest.** SPY returned +10% to +99% over the two years
  from the 2009 dates and +17% to +61% from the 2011-2012 dates; XOM returned +2% to +38% and +4% to +35%, behind SPY on all but 6 of those
  157 dates. CHEAP held on 6 of the 52 dates of 2009 (the three that cleared the hurdle, 2009-03-06 to 2009-05-01, and three in late
  December) and on 4 of the 66 CHEAP dates of 2011-2012. RICH held on the 10 dates of the Q3 2012 print (XOM +4% to +17%, 35-42pp behind
  SPY) and on 1 of the 23 RICH dates of 2010-2011. One-year returns had a median of +9%, three-year returns of +31%.
- **In 2010 the class followed the revenue fallback and the stock did not.** The 12 dates after the Q4 2009 print were RICH and AVOID (BASE
  +9.9%/yr on Q4 2009 revenue +6.1%, BEAR -52.5%/yr): XOM returned +27% to +40% over two years and beat SPY on all 12 by 5.5-12.6pp, so none
  held. Three months later the Q1 and Q2 2010 prints (revenue +41% and +24%) turned the same stock CHEAP and BUY or ACCUMULATE on the same
  FY09 anchor: +33% to +58%, ahead of SPY by 11-24pp, all 26 held. The Q3 2010 print (revenue +16%) made 11 of 14 dates RICH again (+20% to
  +30%; 1 held). The point-in-time sensitivity already showed that BASE on production growth would move 70 of these classes; the outcomes add
  that the flips carried little about the next two years (RICH and CHEAP dates three months apart returned within the same range).
  Hypothesis for the method, not a rule: for a commodity producer with no guide, the latest quarter's revenue growth carries the commodity
  price into BASE and flips the class with it, without information about the two-year return. Test it on other commodity producers and
  periods; never fit it to XOM's outcomes.
- **The 2009 trough set a BEAR that nothing approached.** From 2010-02-02 BEAR was the 2009 fall applied for two years (-52.5%/yr): BEAR
  prices of $9, $13 and $18 against a lowest close of $56.57 in any window (4.3-7.6 times BEAR). From 2009-05-01 to 2010-01-29 BASE (-42.7% to -36.9%/yr from the
  Q1-Q3 2009 prints) lay below BEAR on 40 dates (BASE $33-40 against BEAR $42-45), and two-year prices landed nearest BEAR on 39 of the 52
  dates while sitting 1.2-1.3 times above it at their lows.
- **Ranking: the entry price again; the composites the other way round from 2008.** The entry price ranks the return to the m12-24 average
  at Spearman -0.53 (the two-year endpoint -0.69). The proxy composite ranks it at +0.50 (+0.40 on the endpoint, +0.56 on the excess over
  SPY), where in 2008 it read -0.15: the 2010 prints with production at BULL or XBULL (XTO, project start-ups) preceded the best returns.
  The EPP gap (+0.33), Ratio B (+0.22) and the adjusted gap (+0.33) rank it the wrong way or barely. Two batches that disagree are not a
  pattern; record both, conclude nothing.
- **The encoding calls, seen afterwards.** BASE on production growth would have made most of 2010-2011 RICH; those dates returned +5% to
  +58% and mostly lagged SPY after 2010, so neither encoding reads as right on these outcomes. GAAP EPS would have moved 21 classes, 20 of them
  from December 2011 to June 2012 (CHEAP to FAIR; those dates returned +13% to +35%, 15-29pp behind SPY, where FAIR's ±15pp band also
  fails). The calls were
  decided before scoring and stay.
