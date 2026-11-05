# XOM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the XOM weekly dates: 835 from 2008-01-04 to 2023-12-29. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: ae6e2c7; 2009-2012: 12ca906; 2013-2017: a700fce; 2018-2020: 24123ad; 2021-2023: b9c3f2a). Prices run to 2026-11-04; the 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30).
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

## 2013-2017 (260 dates)

Scored only after the point-in-time build was committed and pushed (a700fce). Two-year horizons end by 2019-12-27; three-year horizons
of the 2017 dates run into 2020.

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| all | 260 | -1.2% | -20.1% to +24.8% | 0 | 0 | -3.9% | 215 |
| class CHEAP | 5 | -7.6% | -10.7% to -2.5% | 0 | 0 | -0.3% | 0 |
| class FAIR | 40 | -1.3% | -20.1% to +11.6% | 0 | 0 | +2.3% | 0 |
| class RICH | 215 | -1.2% | -18.0% to +24.8% | 0 | 0 | -4.9% | 215 |
| tier ACCUMULATE | 22 | +1.2% | -11.3% to +11.6% | 0 | 0 | +7.3% | 0 |
| tier WATCHLIST | 32 | -6.2% | -20.1% to +8.5% | 0 | 0 | -2.2% | 9 |
| tier AVOID | 206 | -1.2% | -18.0% to +24.8% | 0 | 0 | -5.2% | 206 |
| 2013 CHEAP | 5 | -7.6% | -10.7% to -2.5% | 0 | 0 | -0.3% | 0 |
| 2013 FAIR | 36 | -0.2% | -16.1% to +11.6% | 0 | 0 | +2.4% | 0 |
| 2013 RICH | 10 | +0.5% | -16.4% to +8.5% | 0 | 0 | -1.2% | 10 |
| 2014 FAIR | 4 | -16.1% | -20.1% to -13.4% | 0 | 0 | -16.8% | 0 |
| 2014 RICH | 48 | -5.8% | -9.7% to +11.8% | 0 | 0 | -15.8% | 48 |
| 2015 RICH | 53 | +4.7% | -4.8% to +19.8% | 0 | 0 | +2.2% | 53 |
| 2016 RICH | 52 | -1.4% | -18.0% to +24.8% | 0 | 0 | -7.2% | 52 |
| 2017 RICH | 52 | -1.7% | -12.5% to +8.4% | 0 | 0 | -4.0% | 52 |

- **XOM lagged SPY on every one of the 260 dates, so every RICH call held and no FAIR or CHEAP call did.** Over two years XOM returned
  -20% to +25% (median -1%) while SPY returned +6% to +53%; the gap was 5-47pp. No date cleared the hurdle. RICH held on all 215 dates; the
  36 FAIR and 5 CHEAP dates of 2013 and the 4 FAIR dates of January 2014 returned -20% to +12%, 23-39pp behind SPY, outside FAIR's ±15pp
  band. One-year returns had a median of +2%, three-year returns of -3% (the 2017 dates' three-year windows end in 2020: -49% to -8%).
- **The 2013 FAIR and CHEAP calls rested on 2012's gains.** FY12's $9.70 anchored all of them and included $9.9 billion of divestment and
  restructuring gains that the company did not call special items and published no per-share figure without. The point-in-time
  sensitivity (README, "XOM 2013-2017") already showed that removing them, a derived figure the method forbids as an input, would have
  made all 45 of those dates RICH; on these outcomes that would have held. Hypothesis for the method, not a rule: a large one-off gain
  left in the latest year's EPS, because no figure excluding it was published, can flip a stock from RICH to FAIR for a year; test it on
  other tickers' disclosed but unquantified one-offs, never on XOM's outcomes.
- **From 2016 the RICH call held by lagging, not by falling.** From the Q4 2015 print (100 dates) the anchors were the trough years
  (FY15's $3.85, FY16's $1.88), so the BEAR, BASE and BULL prices fell to $4-8, $23-41 and $37-65 while XOM traded at $77-95. Two years
  later XOM stood at $67-85, 1.1-2.2 times BULL and above every scenario but XBULL, and its lowest close in any of those windows ($65.51)
  was 8-16 times the BEAR price. The scenario prices undershot the stock badly; the class held because SPY rose 11-49% over the same
  windows. The 2009 fall as BEAR (-52.5%/yr for two years) was never approached in this batch either (lowest closes 3.4-16 times BEAR).
- **Ranking: the entry price again, and the valuation metrics the right way round this time.** The entry price ranks the return to the
  m12-24 average at Spearman -0.64 (the two-year endpoint -0.58). The EPP gap (-0.48), Ratio B (-0.49) and the adjusted gap (+0.37) rank
  it in the expected direction, where in 2009-2012 they ranked it the wrong way or barely; the proxy composite ranks it at -0.44 (+0.50 in
  2009-2012, -0.15 in 2008). Against the excess over SPY every metric is near zero (-0.13 to -0.04): within this batch they sort the
  absolute return, which followed the oil price and the entry price, and say nothing about the return relative to the market. Three
  batches that disagree are not a pattern; record them, conclude nothing.
- **The encoding calls, seen afterwards.** GAAP EPS in every year would have made 14 dates of July 2013 to January 2014 RICH instead of
  FAIR or CHEAP; they returned -20% to -3%, 23-38pp behind SPY, so all 14 would have held (none holds now). BASE on production growth would
  have made 11 RICH dates FAIR (6 in 2013, 5 in 2015); they returned -12% to +19%, 13-37pp behind SPY, so 3 would have held instead of 11.
  Both together: 9 of the 20 changed dates hold either way. In 2009-2012 neither encoding read as right; here GAAP reads better on 14 dates
  and the production fallback worse on 8. Two batches with different answers are not evidence for either.
  ENERGY_TRANSITION was text only (0 classes either way); ExxonMobil's later derating lies outside these two-year windows. The calls were
  decided before scoring and stay.

## 2018-2020 (157 dates)

Scored only after the point-in-time build was committed and pushed (24123ad). Two-year horizons end by 2022-12-30, so the 2020 dates'
windows run into the 2022 energy-price rise.

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| all | 157 | -10.2% | -52.4% to +264.0% | 49 | 48 | -20.0% | 74 |
| class CHEAP | 18 | -25.1% | -48.1% to +264.0% | 6 | 6 | -35.5% | 6 |
| class FAIR | 30 | -38.4% | -52.4% to +141.1% | 2 | 2 | -15.9% | 0 |
| class RICH | 109 | -1.3% | -40.6% to +230.4% | 41 | 40 | -18.6% | 68 |
| tier ACCUMULATE | 16 | +161.6% | -38.7% to +264.0% | 8 | 8 | +93.1% | 3 |
| tier WATCHLIST | 44 | -36.7% | -52.4% to +232.8% | 12 | 12 | -13.7% | 3 |
| tier AVOID | 97 | -7.7% | -40.6% to +180.5% | 29 | 28 | -21.7% | 68 |
| 2018 CHEAP | 8 | -38.4% | -48.1% to -28.3% | 0 | 0 | -37.4% | 0 |
| 2018 FAIR | 28 | -38.8% | -52.4% to -11.1% | 0 | 0 | -27.9% | 0 |
| 2018 RICH | 16 | -34.6% | -40.6% to -11.3% | 0 | 0 | -21.6% | 16 |
| 2019 CHEAP | 4 | -25.0% | -32.0% to -24.9% | 0 | 0 | -38.9% | 0 |
| 2019 RICH | 48 | -9.4% | -31.7% to +4.3% | 0 | 0 | -35.0% | 48 |
| 2020 CHEAP | 6 | +232.8% | +149.5% to +264.0% | 6 | 6 | +136.8% | 6 |
| 2020 FAIR | 2 | +141.1% | +129.8% to +141.1% | 2 | 2 | +64.8% | 0 |
| 2020 RICH | 45 | +119.7% | +0.3% to +230.4% | 41 | 40 | +63.4% | 4 |

- **Three regimes, and the call held on 74 of 157.** From the 2018 dates XOM returned -52% to -11% over two years, into the COVID fall,
  while SPY returned -9% to +58%: RICH held on all 16, and the 28 FAIR and 8 CHEAP dates lagged SPY by 36-86pp (none held). From the 2019
  dates XOM returned -32% to +4% against SPY's +43% to +61%: RICH held on all 48, the 4 CHEAP dates of January 2019 lagged by 70-83pp.
  From the 2020 dates XOM returned +0.3% to +264% and beat SPY on 48 of 53: RICH held on only 4 (the January 2020 dates before the COVID
  fall), CHEAP held on all 6 (March and November 2020: +150% to +264%), and FAIR's ±15pp band failed on both FAIR dates (2020-03-13 and 2020-04-03: +141% and +130%).
  One-year returns had a median of -6%, three-year returns of +35%.
- **The 2018 FAIR and CHEAP calls rested on BASE's revenue growth.** FY17's $4.63 (with the tax-reform gain) and revenue +16% to +27% put
  BASE at +19% to +29%/yr; the point-in-time sensitivity showed that BASE on production growth would move 81 classes. On these outcomes
  the production encoding would have held on 47 of the 81 changed dates, the revenue encoding holds on 12: the opposite of 2013-2017 (3
  against 11) and of 2010-2011 (neither). Three batches, three answers about the fallback: record it, conclude nothing.
- **COVID made the BEAR case briefly visible and then irrelevant.** The 2018 dates' two-year windows end in 2020, so their prices landed
  nearest BEAR on 41 of 52 dates; the lowest close in any window ($31.45, March 2020) was still 2.9 times the BEAR price ($10-11), and
  BEAR (2009's, then 2016's fall applied for two years) was never reached. From the 2020 dates the prices landed nearest BULL on 51 of 53.
- **The re-file preceded the largest gains of the batch.** The 18 dates from 2020-09-04 carry the TRANSITION labels (14 TRANSITION-EXPOSED,
  NOT CHEAP; 4 TRANSITION-FEAR BASKET); XOM returned +153% to +264% over two years from them, 142-253pp ahead of SPY, as the energy-price
  rise of 2022 reversed the derating (the theme registry's own hindsight note). The re-file changes the label only; the class held on the
  4 CHEAP dates. A label read as "the market prices decarbonisation" sat at the bottom of the cycle: a hypothesis about index-removal
  evidence, not a rule.
- **Ranking: the entry price, strongest yet; the composites the wrong way.** The entry price ranks the return to the m12-24 average at
  Spearman -0.74 (the two-year endpoint -0.88, the excess over SPY -0.67). The proxy composite ranks it at -0.64 and the adjusted gap at
  -0.50, both the wrong way (the 2018 prints' revenue growth lifted both before the fall); the EPP gap ranks it the expected way (-0.42),
  Ratio B not at all (-0.23). Four batches that disagree on everything but the entry price; record them, conclude nothing.
- **The encoding calls, seen afterwards.** GAAP EPS changes nothing here. The derived test without the one-offs (2017-2019) would have
  moved 71 classes and held on 19 of them, where the published encoding holds on 47; FY2019 alone, 8 classes, 0 against 6. In 2013-2017
  the derived 2012 figure would have done better; here the GAAP figures do. The calls were decided before scoring and stay.

## 2021-2023 (156 dates)

Scored only after the point-in-time build was committed and pushed (b9c3f2a). Two-year horizons end by 2025-12-29; three-year horizons
exist for 148 dates (to 2026-11-04).

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| all | 156 | +35.3% | -4.4% to +173.5% | 84 | 73 | +22.2% | 51 |
| class CHEAP | 123 | +23.6% | -4.4% to +127.4% | 51 | 40 | +11.0% | 51 |
| class FAIR | 4 | +76.8% | +72.4% to +87.3% | 4 | 4 | +71.6% | 0 |
| class RICH | 29 | +94.6% | +69.4% to +173.5% | 29 | 29 | +77.3% | 0 |
| tier BUY | 124 | +23.8% | -4.4% to +127.4% | 52 | 41 | +11.0% | 48 |
| tier ACCUMULATE | 3 | +46.4% | +44.4% to +49.1% | 3 | 3 | +49.7% | 3 |
| tier AVOID | 29 | +94.6% | +69.4% to +173.5% | 29 | 29 | +77.3% | 0 |
| FY19's $3.36, Q3 2020 print (January 2021) | 4 | +158.6% | +151.0% to +173.5% | 4 | 4 | +103.3% | 0 |
| FY19's restated $2.25, Q4 2020 print (2021-02-03 to 2021-04-23) | 12 | +117.3% | +85.3% to +150.9% | 12 | 12 | +79.0% | 0 |
| $2.25, Q1 2021 print (2021-04-30 to 2021-07-23) | 13 | +85.4% | +69.4% to +119.1% | 13 | 13 | +71.2% | 0 |
| $2.25, Q2 and Q3 2021 prints (2021-07-30 to 2022-01-28) | 27 | +83.9% | +44.4% to +127.4% | 27 | 27 | +78.3% | 23 |
| FY21's $5.38 (2022-02-02 to 2023-01-27) | 52 | +33.5% | +1.8% to +52.0% | 28 | 17 | +17.4% | 28 |
| FY22's $14.06 (from 2023-02-01) | 48 | +9.2% | -4.4% to +28.4% | 0 | 0 | +4.9% | 0 |

- **The call held on 51 of 156, and it read the cycle backwards at both ends.** The 29 RICH dates of January to July 2021 were followed
  by +69% to +174% over two years, 65-161pp ahead of SPY (-8% to +13%): RICH failed on all 29. The CHEAP calls from the Q2 2021 print to
  the spring of 2022 held (all 23 on the Q2 and Q3 2021 prints and every date to 2022-05-20); the 4 FAIR dates of October-November
  2021 failed, their +72% to +87% far outside FAIR's ±15pp band. From mid-2022 the hits thin out, the misses coming at entry prices of
  $93-116 (28 of 52 held on FY21's anchor; none of the 15 dates from 2022-10-21), and the 48 CHEAP dates on FY22's $14.06 at 7-8x returned -4% to +28%, 19-55pp behind SPY (+27% to +70%):
  CHEAP failed on all 48. One-year returns had a median of +24%, three-year returns of +55%.
- **Peak-year anchors at a low multiple, trough-year anchors at a high one.** In 2021 FY2020 was excluded (a loss), so FY19's restated
  $2.25, a down year, anchored the multiple: $45-65 was 21-29x (the 70th-78th percentile) and RICH, at the start of the 2021-2022 energy
  rise. In 2023 FY22's $14.06, the record year, anchored it: $100-119 was 7-8x (the 8th-19th percentile) and CHEAP, after the rise. The
  same shape appeared before: CHEAP on FY07's peak in 2008 (0 of 53 held), FAIR or CHEAP on FY12's gains in 2013 (0 of 41), RICH on the trough
  years in 2016-2017 (held only because SPY rose faster). Hypothesis for the method, not a rule: for a commodity producer the trailing
  year's EPS sets the class against the cycle, cheap at peak earnings and rich near trough earnings; test it on other cyclical tickers'
  outcomes, never on XOM's.
- **The scenario band missed the move in both directions.** On the RICH dates XOM's price already exceeded BULL ($37-67) on 13 of 29;
  two years later it stood at $100-119, 1.5-3.1 times BULL (0.4-0.5 times XBULL). On the Q2-Q3 2021 dates the two-year price landed
  nearest BASE on all 27 (0.6-1.0 times BASE's $103-173). From the Q4 2021 print BASE ran at +53% to +84%/yr ($210-300), then at $121-298 on FY22's
  anchor, and BULL at $284-411, while the two-year prices ($102-125) landed nearest BEAR on 59 dates, the lowest close in each window still 4.2-7.5 times
  the BEAR price ($11-23): BEAR, 2019's restated fall applied for two years, was never approached.
- **The TRANSITION label sat on the best-performing years.** All 156 dates carry the re-filed labels (TRANSITION-FEAR BASKET on the 123
  CHEAP dates); the theme registry's own hindsight note records that the 2022 energy shock reversed the derating. The label changes
  no class, and the method has no rule that ends a re-file when the evidence reverses: a question for the owner, not an input.
- **Ranking: the entry price almost perfectly, the valuation metrics the wrong way.** The entry price ranks the return to the m12-24
  average at Spearman -0.99 (the two-year endpoint -0.98, the excess over SPY -0.96): the batch is one price path up and then sideways.
  The EPP gap ranks it at +0.59 and Ratio B at +0.19 (both the wrong way), the adjusted gap at -0.22 (the wrong way), the proxy composite
  not at all (+0.07). Five batches that disagree on everything but the entry price; record them, conclude nothing.
- **The encoding calls, seen afterwards.** BASE on production growth would have moved 77 classes and held on 27 of them, where the
  revenue fallback holds on 49 (2018-2020: 47 against 12; 2013-2017: 3 against 11; 2010-2011: neither): the answers alternate. GAAP EPS, or 2019
  at GAAP without the restatement, would have moved only the 4 FAIR dates of late 2021 to CHEAP and held on all 4 (0 as published).
  FY2020's exclusion has no tested alternative: a loss has no P/E. The calls were decided before scoring and stay.
