# LOW retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 575 weekly dates from 2008-01-04 to 2018-12-31. They are **labels and
hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time
build was committed: 2008 in 88b0255, 2009-2010 in bfe09e0, 2011-2012 in 0b9b6f8, 2013-2014 in 7eeed23, 2015-2016 in
304d9dc, 2017-2018 in fe7f63f. Prices run to 2026-10-23 for the earlier batches, 2026-10-26 from 2013 and 2026-10-28
from 2017; every horizon used here ends by 2020-12-30. Medians of an even count take the upper middle value
(`statistics.median_high`). The 15%/yr hurdle over two years is +32.2%.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 30 | +10% | -11% to +32% | 1 | 19 | +7% | 20 |
| class FAIR | 15 | +6% | -11% to +18% | 0 | 11 | -6% | 4 |
| class RICH | 8 | -11% | -17% to +11% | 0 | 3 | -11% | 5 |
| legacy tier BUY (all dates) | 53 | +7% | -17% to +32% | 1 | 33 | -5% | 29 |
| January-September | 39 | +4% | -17% to +21% | 0 | 33 | -7% | 28 |
| October-December | 14 | +17% | +2% to +32% | 1 | 0 | +11% | 1 |
| CHEAP, January-September | 19 | +6% | -11% to +21% | 0 | 19 | -4% | 19 |
| CHEAP, October-December | 11 | +17% | +2% to +32% | 1 | 0 | +16% | 1 |

- **In absolute terms the year was a wash.** The median date returned +7% over two years. One date of 53 cleared the
  hurdle, and only just (2008-10-24 at $17.20: +32.3%). The legacy tier read BUY and the price sat below the EPP floor on
  every date, yet every date lived through a drawdown of 42-51% to the 2009-03-06 low ($13.39). Every two-year outcome
  landed closest to the BEAR scenario price.
- **The class ranked the outcomes in order.** CHEAP did better than FAIR, which did better than RICH, on both the 2-year
  return and the m12-24 average price. The eight RICH dates (16-17x, late April and mid-August to September) were the
  worst entries of the year (-17% to +11%).
- **Against SPY, the date decided the sign.** The 39 dates to September beat SPY on 33, because the market fell further.
  The 14 dates from October returned the most (median +17%) and beat SPY on none, because the market rebounded harder from
  its March 2009 low. So the CHEAP call "held" on all 19 CHEAP dates to September (it beat SPY) and on 1 of the 11 from
  October (it cleared the hurdle). The same class on the same stock passed or failed its test on the benchmark's path.
- **Why everything read cheap: the window's multiple belonged to a growth decade.** The P/E window (1998-2007) covers a
  decade in which net sales grew 18-20% in nine years of ten (rule T's own table) and the stock traded at 14-43x. In 2008,
  on guided EPS, it traded at 11-17x: the 0th-27th percentile of that range. The valuation factor (+0.38 to +0.5), the EPP
  floor (16-17x, the median of the decade's calendar-year lows) and the BULL case (the decade's 21-25% EPS CAGR at its
  75th-percentile P/E) all carried the growth era into a year whose guide was sales of +0-3%. The BEAR case (flat or -6.5%
  EPS at the 10th-percentile P/E, about 15x) is where the stock ended. The growth factor already read -0.5 on all 53 dates.
  Hypothesis for the method: when guided growth sits far below the decade median, the own-history multiple and the decade
  CAGR are stale anchors. Test it on other tickers with a growth-regime change before any method change; never fit it to
  LOW's outcomes.
- **Ratio B pointed the wrong way.** Method r2 carries the guided margin step (-130bp, then -180bp) as EPS growth for two
  years, so BASE sat at or below BEAR. With BULL on the decade CAGR, Ratio B stayed at or under 0.20 and the tier at BUY all
  year. This is UNP's 2008 lesson from the other side: there the BEAR rule (the decade's worst year) was the stale anchor;
  here, for a company whose decade held no down year, the BULL rule is.
- **One stock, one crash.** Most of the spread between dates is the entry price: the three lowest closes (2008-10-10,
  2008-10-24, 2008-11-14, at $17-18) returned +23% to +32%; the three September dates at $25-26 lost 12-15%. This mostly tests
  "buy lower". Testing selection needs many tickers on the same dates.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 10 | +32% | +17% to +102% | 5 | 1 | +26% | 5 |
| class FAIR | 2 | +32% | +25% to +32% | 0 | 0 | +24% | 0 |
| class RICH | 40 | +11% | -12% to +74% | 10 | 0 | +12% | 30 |
| legacy tier BUY | 40 | +29% | -8% to +102% | 15 | 1 | +19% | 23 |
| legacy tier ACCUMULATE | 12 | +8% | -12% to +12% | 0 | 0 | +4% | 12 |
| to 2009-02-13 (before the Q4 FY08 print) | 6 | +32% | +17% to +45% | 3 | 0 | +21% | 3 |
| 2009-02-20 to 2009-03-13 | 4 | +74% | +64% to +102% | 4 | 1 | +48% | 1 |
| from 2009-03-20 | 42 | +12% | -12% to +58% | 8 | 0 | +13% | 31 |

- **The ranking held, but the bottom read RICH.** CHEAP did better than RICH (+32% against +11%). The four dates around the
  low, 2009-02-20 to 2009-03-13 at $13-16, returned +64% to +102%: one was CHEAP (2009-03-06 at $13.39, the low of the whole
  cycle, +102%), three were RICH. They read RICH because the Q4 FY08 guide cut the margin another 170bp and put sales at -2% to
  +2%: method r2 carries that step for two years, so BASE fell to -28%/yr and the BASE price to $11, under the market. The
  BEAR case did the same with FY2008's -19.9% EPS year, applied twice.
- **LOW lagged the market's rebound all year.** One date of 52 beat SPY (2009-03-06). Even the CHEAP dates returned less than
  the index, which rose faster from its March low. RICH held its test (miss the hurdle and lag SPY) on 30 of 40.
- **Ratio B ranked the year better than the class.** BUY (Ratio B under 0.75) returned +29%, ACCUMULATE +8%: the ACCUMULATE
  dates are the higher prices of late July to September and mid-November to December 2009, among the worst entries of the
  year (-12% to +12%).
- **Outcomes moved off BEAR.** 33 of 52 landed nearest the BASE price and 13 nearest BULL; only the six dates before the Q4
  print (whose BEAR was still flat EPS at 15x) landed on BEAR.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 30 | +38% | +14% to +64% | 20 | 22 | +23% | 23 |
| class FAIR | 11 | +32% | +23% to +49% | 5 | 10 | -2% | 6 |
| class RICH | 11 | +22% | +14% to +30% | 0 | 2 | +2% | 9 |
| legacy tier BUY | 29 | +38% | +14% to +64% | 20 | 22 | +23% | 23 |
| legacy tier ACCUMULATE | 12 | +27% | +17% to +49% | 1 | 6 | +3% | 9 |
| legacy tier WATCHLIST | 10 | +26% | +16% to +47% | 4 | 6 | -0% | 5 |
| legacy tier AVOID | 1 | +14% | +14% | 0 | 0 | -14% | 1 |
| before 2010-02-23 (FY2009 guide) | 7 | +24% | +16% to +30% | 0 | 1 | +6% | 6 |
| from 2010-02-23 (FY2010 guide) | 45 | +35% | +14% to +64% | 25 | 33 | +18% | 32 |

- **The cleanest year of the three.** Class and tier both ranked the outcomes in order: CHEAP > FAIR > RICH and BUY >
  ACCUMULATE > WATCHLIST > AVOID. Two of three CHEAP dates cleared the hurdle; no RICH date did. The single AVOID date
  (2010-04-23, $28.22 at 20.7x, the 68th percentile) returned least (+14%).
- **It worked once the guide turned.** From the Q4 FY09 print the guided margin step was an increase (+40 to +70bp), so BASE
  was +9% to +15%/yr and the signals moved up (proxy composite 1.80-2.20). The 45 dates from then returned a median +35% and
  beat SPY on 33. The best entries were the CHEAP dates of October-November 2010 at $21-22 (+53% to +64%).
- **FAIR split by date, not by price.** The six FAIR dates of March to May ($24.5-25.6) returned +23% to +32% with an m12-24
  average price 2-6% below the entry; the five of December ($24.9-25.5) returned +42% to +49% with an average 15-18% above
  it. Same class, same price, different two-year path: one stock's endpoint again.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 27 | +77% | +44% to +153% | 27 | 27 | +44% | 27 |
| class FAIR | 8 | +53% | +44% to +60% | 8 | 8 | +20% | 0 |
| class RICH | 17 | +125% | +94% to +146% | 17 | 17 | +85% | 0 |
| legacy tier BUY | 31 | +107% | +51% to +153% | 31 | 31 | +67% | 21 |
| legacy tier ACCUMULATE | 13 | +50% | +44% to +129% | 13 | 13 | +20% | 6 |
| legacy tier WATCHLIST | 8 | +96% | +53% to +99% | 8 | 8 | +70% | 0 |
| to 2011-02-18 (FY2010 guide) | 7 | +53% | +46% to +60% | 7 | 7 | +20% | 0 |
| 2011-02-24 to 2011-08-12 (FY2011 guide, margin +30bp, then +10bp) | 25 | +75% | +44% to +141% | 25 | 25 | +34% | 24 |
| from 2011-08-16 (margin -30bp, then -80 to -90bp) | 20 | +136% | +94% to +153% | 20 | 20 | +86% | 3 |

- **Every date won, and the class ranked them backwards.** All 52 dates cleared the hurdle and beat SPY (median excess
  +52pp, lowest +22pp). 44 landed nearest the BULL price, 7 nearest XBULL and 1 nearest BASE. RICH returned +125%, CHEAP
  +77% and FAIR +53%. RICH "held" on no date, because a RICH call expects a miss.
- **The RICH dates were the year's lows.** From the Q2 FY11 print (2011-08-15) to the end of October the stock traded at
  $19-22, 12.5-14.7x guided FY11 EPS, the 2nd-14th percentile of its own range. The multiple did not drive the class; the
  signals did. The guide cut the margin step to -30bp, then to -80 to -90bp in November with the store closings, so BASE
  fell to -1% to -4%/yr. On the Q2 print rule T scored comps (-0.3%), gross margin (-37bp), net sales (+1.3%) and the
  margin step at BEAR. The proxy composite sat at 1.30, then 1.50, against a market composite of 1.95-2.79 back-solved
  from the price on the RICH dates. A gap of -0.5 or worse is RICH by rule. The 20 dates from the Q2 print returned +94%
  to +153% (median +136%), the best entries of the five years.
- **The class flipped on a 3% price move.** In August and September the gap sat on the -0.5 line. With the same guide
  and the same signals the class read RICH at $20.09 (08-16), CHEAP at $18.94 (09-02), RICH at $20.38 (09-16) and CHEAP at
  $19.34 (09-30). The line between CHEAP and RICH ran at about $19.5. The point-in-time robustness column flagged it: the
  RICH calls of 2011-08-16 to 2011-10-14 held in only 3 or 4 of the 8 price states, the CHEAP calls between them in 7.
  Pooled over five years, though, RICH at 4/8 or less (14 dates, +28%) shows no clean split from RICH at 5/8 or more
  (90 dates, +44%), because the years differ.
- **Ratio B ranked better than the class.** The tier stayed BUY through the August-October lows, because the BULL price
  ($36-39, the decade CAGR) sat far above the price. BUY returned +107%, against +50% for ACCUMULATE. Among the weakest
  entries were the seven ACCUMULATE dates of March-April 2011 at $26.25-27.19 (+44% to +52%). Six of them read CHEAP.

## 2012 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 19 | +78% | +59% to +92% | 19 | 19 | +70% | 19 |
| class FAIR | 6 | +56% | +50% to +60% | 6 | 6 | +46% | 4 |
| class RICH | 28 | +85% | +65% to +105% | 28 | 28 | +60% | 0 |
| legacy tier BUY | 16 | +83% | +59% to +92% | 16 | 16 | +72% | 16 |
| legacy tier ACCUMULATE | 10 | +60% | +50% to +105% | 10 | 10 | +48% | 7 |
| legacy tier WATCHLIST | 2 | +96% | +89% to +96% | 2 | 2 | +70% | 0 |
| legacy tier AVOID | 25 | +84% | +65% to +97% | 25 | 25 | +56% | 0 |
| to 2012-02-24 (FY2011 guides) | 8 | +83% | +72% to +90% | 8 | 8 | +64% | 0 |
| 2012-02-28 to 2012-08-17 (FY2012 guide, margin +100bp, then +90bp) | 25 | +74% | +50% to +92% | 25 | 25 | +66% | 23 |
| from 2012-08-21 (margin +45bp, then +40bp) | 20 | +88% | +65% to +105% | 20 | 20 | +54% | 0 |

- **Every date won again, and AVOID did as well as BUY.** All 53 dates cleared the hurdle and beat SPY (median excess
  +36pp, lowest +12pp). 28 landed nearest XBULL and 25 nearest BULL. RICH returned +85%, CHEAP +78% and FAIR +56%. AVOID
  returned +84% and BUY +83%.
- **The class followed the guide, and the period the model liked returned least.** The eight January-February dates were
  still on the FY2011 guides (a -80 to -90bp margin step) and read RICH and AVOID: +83%. The FY2012 guide of 2012-02-27
  (+100bp, EPS $1.75-1.85) put BASE at +16-17%/yr. It turned the class CHEAP or FAIR and the tier BUY or ACCUMULATE for 25
  dates: +74%, the lowest of the three periods. The Q2 FY12 print (2012-08-20) cut the step to +45bp, EPS to $1.64 and BASE
  to +9%/yr. The class read RICH on all 20 remaining dates: +88%. The worst entries were the FAIR dates of April-May at
  $31-32 (+50% to +59%).
- **Late 2012 passed the BULL price, and two years on it stood at or above XBULL.** From 2012-08-21 the price rose from
  $26 to $36. The multiple went from the 34th to the 95th percentile of its own range (16.1x to 22.0x guided FY12 EPS) and
  Ratio B from 1.1x to 43x (`inf` on 2012-11-30, with the price above the BULL case). The BULL case was $36-37: the
  decade's 8.5-9.2% EPS CAGR at the 75th-percentile P/E. Two years later these 20 dates traded at $52.5-68.6, at or above
  the XBULL price ($52-53, the best two-year run at the 90th-percentile P/E). The best entry of 2012 was the first of them,
  2012-08-21 at $26.43 (+105%).


## 2013 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR | 1 | +107% | +107% | 1 | 1 | +50% | 0 |
| class RICH | 51 | +67% | +39% to +103% | 51 | 51 | +45% | 0 |
| legacy tier WATCHLIST | 11 | +96% | +81% to +107% | 11 | 11 | +50% | 0 |
| legacy tier AVOID | 41 | +60% | +39% to +99% | 41 | 41 | +44% | 0 |
| to 2013-02-22 (FY2012 guide) | 7 | +88% | +80% to +99% | 7 | 7 | +38% | 0 |
| 2013-02-26 to 2013-08-16 (FY2013 guide, margin +60bp) | 25 | +75% | +56% to +107% | 25 | 25 | +48% | 0 |
| from 2013-08-22 (margin +65bp, then +75bp) | 20 | +54% | +39% to +67% | 20 | 20 | +44% | 0 |

- **Every date won, and every one landed at XBULL.** All 52 dates cleared the hurdle and beat SPY (median excess +43pp,
  lowest +22pp on 2013-11-15). Two years on the stock stood at $66.7-77.3, above the XBULL price on every date ($52-68:
  the decade's best two-year EPS run at the 90th-percentile P/E, 20.6-21.0x). No CHEAP date existed, and RICH, which
  expects a miss, held on none of its 51.
- **The class had nothing to rank.** 51 of 52 dates read RICH. The one FAIR date, 2013-02-26 at $36.59 (the day after the
  fiscal 2013 guide), was the best entry of the year (+107%).
- **Ratio B ranked the year, and so did the price alone.** WATCHLIST (Ratio B 1.2-1.7x, late February to June at
  $36.6-39.6) returned +96%, AVOID +60%. The rank correlation of Ratio B with the two-year return was -0.47, of the price
  alone -0.88. The return fell as the price rose through the year: +88% before the fiscal 2013 guide, +75% on it, +54% from
  the Q2 print. The worst entries were September to November at $47.8-51.8 (+39% to +49%).
- **The anchors capped the cases below where the market went.** BASE grew guided EPS at +15-20%/yr, and BULL could not
  exceed it (the decade CAGR was lower). Both sat on the window's P/E: the median (17x) for BASE, the 75th percentile
  (18.8x) for BULL. The ten-year window (from 2003) holds the 11-15x lows of 2007-2012, so the stock's 17.8-24.7x read as
  its 62nd to 99th percentile. The outcomes priced the earnings path at more than any percentile of that window.

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR | 17 | +74% | +65% to +79% | 17 | 17 | +54% | 0 |
| class RICH | 35 | +41% | +7% to +68% | 25 | 32 | +41% | 3 |
| legacy tier ACCUMULATE | 7 | +74% | +66% to +75% | 7 | 7 | +57% | 0 |
| legacy tier WATCHLIST | 18 | +68% | +40% to +79% | 18 | 18 | +51% | 0 |
| legacy tier AVOID | 27 | +37% | +7% to +59% | 17 | 24 | +40% | 3 |
| to 2014-02-21 (FY2013 guide) | 7 | +49% | +41% to +59% | 7 | 7 | +51% | 0 |
| 2014-02-27 to 2014-08-15 (FY2014 guide, margin +65bp) | 25 | +69% | +40% to +79% | 25 | 25 | +53% | 0 |
| from 2014-08-21 (sales cut to +4.5%, then margin +70-75bp) | 20 | +32% | +7% to +52% | 10 | 17 | +36% | 3 |

- **Class and tier both ranked in order, for the first time since 2010.** FAIR returned +74%, RICH +41%; ACCUMULATE +74%,
  WATCHLIST +68%, AVOID +37%. The rank correlations were the strongest of the seven years: -0.89 for Ratio B and +0.92 for
  the adjusted gap. The price alone gave -0.84. With the same guide all spring and summer, the gap moved mostly with the
  price.
- **The FAIR window was April to August at $45-48** (17.3-18.3x guided FY14 EPS, the 56th-73rd percentile). Its July
  dates at $47.4-47.8 were the best entries of the year (+76% to +79%). All 17 FAIR dates cleared the hurdle and beat SPY.
- **RICH held, at last, at the top.** The 20 dates from the Q2 print returned +32%: 10 cleared the hurdle and 17 beat
  SPY. The three December dates at $66.90-68.80 (25-26x, the 100th percentile, Ratio B 20-224x with the price at the BULL
  case) returned +7% to +12% and lagged SPY by 1-6pp: the RICH call held on these 3, its first hits since 2010.
- **The robustness column flagged the RICH dates that did best.** The two RICH dates at only 4 of 8 price states
  (2014-08-08 and 2014-08-15, $49.7-50.0) returned +68% and +67%; the 33 RICH dates at 5/8 or more, a median +40%.
- **The stock still finished above the bull case.** 31 dates landed nearest XBULL, 21 nearest BULL; none nearest BASE.

## 2015 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 52 | +15% | +4% to +27% | 0 | 6 | +6% | 46 |
| legacy tier WATCHLIST | 2 | +20% | +15% to +20% | 0 | 0 | +15% | 2 |
| legacy tier AVOID | 50 | +15% | +4% to +27% | 0 | 6 | +6% | 44 |
| to 2015-02-20 (FY2014 guide) | 7 | +8% | +4% to +12% | 0 | 0 | +6% | 7 |
| from 2015-02-26 (FY2015 guide, EPS $3.29) | 45 | +16% | +4% to +27% | 0 | 6 | +6% | 39 |

- **RICH held, for the first time since 2010, on almost the whole year.** Every date read RICH, and none cleared the
  hurdle: the median two-year return was +15% (+4% to +27%), with a median excess of -7.8pp against SPY. The call held
  on 46 of 52. The six that beat SPY were 2015-04-24 to 2015-05-29 (+0.6 to +11pp). Every date lived through the fall to
  $63.40 on 2016-02-11.
- **The outcomes landed on BASE, not above BULL.** 35 dates landed nearest BASE, 16 nearest BULL and one nearest XBULL.
  Two years on the stock stood at $71-93, against BASE prices of $63-81. From 2011 to 2014 it had landed at BULL or
  XBULL on 208 of 209 dates.
- **The signals ranked the year and the price did not.** The rank correlation with the two-year return was -0.46 for
  Ratio B and +0.51 for the adjusted gap, against -0.09 for the price alone. Most of it is the guide rollover. The seven
  January-February dates, still on FY14's $2.68 guide (Ratio B `inf` on four), returned +8%; the dates on the FY15 guide,
  +16%.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 11 | +52% | +44% to +66% | 11 | 11 | +31% | 11 |
| class FAIR | 33 | +24% | +12% to +45% | 7 | 8 | +11% | 23 |
| class RICH | 8 | +53% | +24% to +56% | 7 | 5 | +21% | 0 |
| legacy tier BUY | 5 | +45% | +44% to +58% | 5 | 5 | +37% | 5 |
| legacy tier ACCUMULATE | 16 | +43% | +21% to +66% | 11 | 10 | +21% | 13 |
| legacy tier WATCHLIST | 27 | +24% | +12% to +55% | 5 | 7 | +10% | 16 |
| legacy tier AVOID | 4 | +53% | +36% to +56% | 4 | 2 | +15% | 0 |
| to 2016-02-19 (FY2015 guide) | 7 | +53% | +36% to +56% | 7 | 4 | +16% | 0 |
| 2016-02-25 to 2016-08-12 (FY2016 guide, $4.00 then $4.11) | 25 | +23% | +12% to +46% | 1 | 1 | +9% | 16 |
| 2016-08-18 to 2016-11-11 (with RONA, $4.06) | 13 | +51% | +32% to +66% | 13 | 12 | +29% | 13 |
| from 2016-11-17 (GAAP guide, $3.52) | 7 | +32% | +24% to +42% | 4 | 7 | +33% | 5 |

- **CHEAP worked, and FAIR caught the top.** All 11 CHEAP dates cleared the hurdle and beat SPY (+44% to +66%). The
  best entries were September 2016 at $71-72 (+63% to +66%). The 24 FAIR dates of March to mid-August, at $70-82 on the
  fiscal 2016 guide, returned +12% to +32%. The worst entry was 2016-05-19 at $79.86 (+12%, 25.6pp behind SPY). From
  the Q4 FY15 print to mid-August, 1 of 25 dates cleared the hurdle.
- **RICH on a stale guide again.** The seven January-February dates were still on the fiscal 2015 guide ($3.29) and read
  RICH at 19.7-21.8x. They sat near the year's lowest prices ($65-72) and returned +36% to +56%. The fiscal 2016 guide
  ($4.00) turned the same prices FAIR or CHEAP from 2016-02-25: the class turned on the guide rollover, not on the
  price. The same January-February window returned +83% in 2012 but +8% in 2015, so it points no single way.
- **The tier ranked the guided dates.** BUY returned +45% and ACCUMULATE +43%, against +24% for WATCHLIST; the four AVOID
  dates are the January ones. The rank correlation was -0.31 for Ratio B and +0.17 for the gap, against -0.65 for the
  price alone. 42 dates landed nearest BASE, 8 nearest BULL and 2 nearest XBULL.
- **The watch list tests nothing here.** The 40 dates from 2016-04-01 carry ECOMMERCE on the watch list. The entry
  changed no number, so their outcomes (a median of +30%) say nothing about the theme.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 26 | +35% | +21% to +55% | 18 | 26 | +27% | 26 |
| class FAIR | 17 | +43% | +22% to +53% | 16 | 17 | +30% | 2 |
| class RICH | 9 | +40% | +34% to +44% | 9 | 9 | +24% | 0 |
| legacy tier BUY | 15 | +37% | +26% to +52% | 13 | 15 | +32% | 15 |
| legacy tier ACCUMULATE | 25 | +39% | +21% to +55% | 18 | 25 | +29% | 12 |
| legacy tier WATCHLIST | 11 | +39% | +33% to +44% | 11 | 11 | +24% | 1 |
| legacy tier AVOID | 1 | +34% | +34% | 1 | 1 | +14% | 0 |
| to 2017-02-24 (FY2016 guide, $3.52) | 8 | +37% | +33% to +44% | 8 | 8 | +31% | 1 |
| 2017-03-02 to 2017-05-19 (FY2017 guide, $4.64) | 12 | +35% | +24% to +48% | 8 | 12 | +19% | 12 |
| 2017-05-25 to 2017-08-18 ($4.30) | 13 | +33% | +21% to +46% | 8 | 13 | +32% | 13 |
| from 2017-08-24 ($4.20-4.30) | 19 | +46% | +34% to +55% | 19 | 19 | +27% | 2 |

- **Every date beat SPY, and the class hardly ranked them.** All 52 dates beat SPY (+0.5 to +33.1pp, median +15.1pp) and
  43 cleared the hurdle. CHEAP returned +35%, FAIR +43% and RICH +40%. The call held on all 26 CHEAP dates, on 2 of 17
  FAIR and on none of the 9 RICH. Every date lived through the same 26.4% fall, from $116.84 on 2018-09-21 into December
  2018.
- **The best and worst entries sat a few dollars apart.** 2017-08-24 and 2017-09-01, at $72.61-74.65 right after the Q2
  FY17 cut, returned +52% and +55%. 2017-05-25 and 2017-06-02, at $80-81 just after the cut to $4.30, returned +21-22%;
  January's dates at $71-73 returned +33-39%. The 12 CHEAP dates of March to May, at Ratio B 0.66-0.84 and $80-86,
  returned +24% to +48%.
- **The outcomes landed on BASE.** 43 dates landed nearest BASE and 9 nearest BULL: two years on the stock stood at
  $93-120, against BASE prices of $94-124.
- **The signals did not rank the year; the price did, on the average.** The rank correlation with the two-year return
  was +0.10 for Ratio B and -0.22 for the adjusted gap, against -0.23 for the price alone. With the m12-24 average price
  it was -0.18, -0.11 and -0.91.

## 2018 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 5 | +18% | -14% to +32% | 1 | 4 | +28% | 4 |
| class FAIR | 1 | +40% | +40% | 1 | 1 | +24% | 0 |
| class RICH | 47 | +46% | -12% to +92% | 35 | 41 | +16% | 6 |
| legacy tier BUY | 8 | +26% | -14% to +40% | 3 | 6 | +27% | 5 |
| legacy tier ACCUMULATE | 14 | +46% | -12% to +92% | 9 | 13 | +26% | 1 |
| legacy tier WATCHLIST | 10 | +56% | +33% to +76% | 10 | 10 | +16% | 0 |
| legacy tier AVOID | 21 | +46% | +16% to +84% | 15 | 17 | +12% | 4 |
| to 2018-02-23 (FY2017 guide) | 8 | +29% | +16% to +34% | 2 | 4 | +12% | 4 |
| 2018-03-01 to 2018-05-18 (FY2018 guide, $5.40-5.50, -30bp) | 12 | +18% | -14% to +40% | 3 | 9 | +26% | 6 |
| 2018-05-24 to 2018-08-17 ($5.40-5.50, -40bp) | 13 | +44% | +31% to +66% | 12 | 13 | +13% | 0 |
| 2018-08-23 to 2018-11-16 (GAAP guide with the Orchard charges, $4.50-4.60) | 13 | +57% | +40% to +84% | 13 | 13 | +13% | 0 |
| from 2018-11-21 (adjusted guide, $5.08-5.13) | 7 | +76% | +70% to +92% | 7 | 7 | +47% | 0 |

- **RICH failed on the two-year return.** The 47 RICH dates returned a median +46%; 35 cleared the hurdle, 41 beat SPY
  and the call held on 6. The 13 dates on the Q2 FY18 guide, which carries the Orchard exit charges (AVOID, Ratio B 1.83x
  to 61x, BASE price $64-65), returned +40% to +84% and landed nearest XBULL on all 13. Method r2 had projected the
  guide's -180bp, mostly charges, as two years of -23% EPS growth. The 7 dates on the adjusted Q3 FY18 guide did best:
  +70% to +92%.
- **The two-year endpoint decided the order.** The dates from 2018-03-16 to 2018-05-04 end between 2020-03-16 and
  2020-05-04, in and just after the COVID crash (low $65.02 on 2020-03-18). 2018-03-23, CHEAP and BUY at $83.77, returned
  -14%. The late-2018 dates end in late 2020 at $150-175. On the m12-24 average price, which averages the second year,
  the order reverses:
  - the rank correlation is -0.61 for Ratio B, +0.51 for the gap and -0.76 for the price, against +0.24, -0.33 and +0.20
    on the endpoint;
  - BUY +27%, ACCUMULATE +26%, WATCHLIST +16%, AVOID +12%; CHEAP +28% against RICH +16%.
- **At the top of the window RICH held, as in 2015.** The 8 January-February dates, still on the fiscal 2017 guide at
  22.3-25.3x (the 92nd-100th percentile), returned +16% to +34%. Four lagged SPY (by 2.0-2.8pp), two cleared the hurdle,
  and their m12-24 average was +1% to +14%.
- **Landing:** BULL 22, XBULL 17, BASE 12 and BEAR 2 (2018-03-16 and 2018-03-23, whose endpoints fell in the crash).
- **The watch list tests nothing here.** Every 2017 and 2018 date carries ECOMMERCE on the watch list. The entry changed
  no number, so their outcomes say nothing about the theme.

## 2008-2018 together (575 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 158 | +40% | -14% to +153% | 102 | 129 | +26% | 135 |
| class FAIR | 111 | +36% | -11% to +107% | 61 | 79 | +20% | 39 |
| class RICH | 306 | +41% | -17% to +146% | 182 | 194 | +24% | 99 |
| legacy tier BUY | 197 | +33% | -17% to +153% | 104 | 129 | +23% | 137 |
| legacy tier ACCUMULATE | 109 | +44% | -12% to +129% | 69 | 84 | +24% | 60 |
| legacy tier WATCHLIST | 99 | +44% | +12% to +107% | 69 | 73 | +25% | 24 |
| legacy tier AVOID | 170 | +46% | +4% to +99% | 103 | 116 | +36% | 52 |

Median 2-year total return by year (dates in brackets):

| Year | CHEAP | FAIR | RICH | tier BUY | other tiers |
|---|---|---|---|---|---|
| 2008 | +10% (30) | +6% (15) | -11% (8) | +7% (53) | none |
| 2009 | +32% (10) | +32% (2) | +11% (40) | +29% (40) | +8% (12) |
| 2010 | +38% (30) | +32% (11) | +22% (11) | +38% (29) | +26% (23) |
| 2011 | +77% (27) | +53% (8) | +125% (17) | +107% (31) | +53% (21) |
| 2012 | +78% (19) | +56% (6) | +85% (28) | +83% (16) | +81% (37) |
| 2013 | none | +107% (1) | +67% (51) | none | +67% (52) |
| 2014 | none | +74% (17) | +41% (35) | none | +52% (52) |
| 2015 | none | none | +15% (52) | none | +15% (52) |
| 2016 | +52% (11) | +24% (33) | +53% (8) | +45% (5) | +28% (47) |
| 2017 | +35% (26) | +43% (17) | +40% (9) | +37% (15) | +39% (37) |
| 2018 | +18% (5) | +40% (1) | +46% (47) | +26% (8) | +46% (45) |

Rank correlation (Spearman) with the two-year total return, within each year:

| Year | Ratio B | adjusted gap | price alone |
|---|---|---|---|
| 2008 | -0.43 | +0.37 | -0.67 |
| 2009 | -0.72 | +0.30 | -0.80 |
| 2010 | -0.44 | +0.69 | -0.45 |
| 2011 | -0.61 | -0.52 | -0.89 |
| 2012 | +0.18 | -0.15 | -0.18 |
| 2013 | -0.47 | +0.03 | -0.88 |
| 2014 | -0.89 | +0.92 | -0.84 |
| 2015 | -0.46 | +0.51 | -0.09 |
| 2016 | -0.31 | +0.17 | -0.65 |
| 2017 | +0.10 | -0.22 | -0.23 |
| 2018 | +0.24 | -0.33 | +0.20 |

- **The class ranked some years and not the cycle.** CHEAP beat RICH in 2008-2010, and RICH beat CHEAP in 2011-2012. No
  date read CHEAP in 2013-2015. FAIR beat RICH in 2013-2014; RICH held on 46 of 52 dates in 2015; in 2016 CHEAP and RICH
  tied (+52%, +53%) and FAIR, at the year's high prices, did worst. In 2017 every class beat SPY and CHEAP did worst
  (+35%, against +43% for FAIR and +40% for RICH). In 2018 RICH beat CHEAP (+46% against +18%) on endpoints set by the
  2020 crash. Pooled: RICH +41%, CHEAP +40%, FAIR +36%.
- **The tier ranked better, mostly as a price.** A lower Ratio B went with a higher return in eight of eleven years (2012,
  2017 and 2018 the exceptions; 2018 ranks the right way on the m12-24 average). The price alone ranked the dates as well
  or better in nine. Ratio B clearly beat it only in 2015, when the guide rollover moved Ratio B without the price. The
  pooled tier rows mix years: AVOID falls only in 2010-2018, which is why it shows +46% against BUY's +33%.
- **One mechanism under the failures: the model projects from where the latest regime stands.** In the fact sheet the
  EBIT margin went from 10.98% (FY06) and 9.74% (FY07) to 6.53-7.29% in FY09-FY11. It then recovered: 7.05% (FY12),
  7.77% (FY13), 8.53% (FY14), 9.31% adjusted (FY15), 8.99% (FY16); the FY17 operating margin was 9.60%. EPS went from
  $1.98 to $1.21-1.43, then to $3.29, $3.99 and $4.39 adjusted. Method r2 projects from that base in three ways:
  - it carries the latest guided margin step for two years, in 2018 a step made mostly of exit charges (-180bp became
    BASE -12.2%/yr);
  - it takes BULL from the decade's EPS CAGR on the latest EPS (21-25% in 2008, 8.5-11% in 2011-2012), and once BASE
    exceeds that CAGR, BULL can add nothing to BASE (from 2012-02-28 to 2018-02-23);
  - it scores net sales against rule T's BASE line of +10% or more, set from the fiscal 1997-2006 growth decade.

  The net-sales signal read BEAR on 525 of the 575 dates, which held the proxy composite at 1.30-2.70. Any rally then
  opened a gap to the market composite and read RICH.
- **The P/E window lags a regime change, but 2015 shows the cost of reading that as a rule.** In 2008 the window
  (1998-2007) held a growth decade's 14-43x, so 11-17x read as the 0th-27th percentile: CHEAP, while the stock went
  nowhere. In 2013-2014 the window held the crisis's 11-15x, so 17-26x read as the 56th-100th percentile: RICH, while the
  stock landed nearest the XBULL price on 83 of 104 dates. In 2015 the same window read 20-27x as the 85th-100th
  percentile, and this time RICH held: the stock lagged SPY on 46 of 52 dates and landed near BASE. January-February 2018
  repeats it: at the 92nd-100th percentile RICH held on 4 of 8 dates. The recovery that beat every case in 2011-2014
  (BULL or XBULL on 208 of 209 dates) had run its course by 2015; in 2015-2017, 120 of 156 dates landed nearest BASE.
  UNP's 2010 (FINDINGS there: the P/E on trough EPS read RICH while earnings recovered) is the same pattern on another
  ticker.
- **Hypotheses for a new method version.** Test each on other tickers' cycles before any change, and never fit it to
  LOW's outcomes:
  1. When the latest margin sits far below the decade median, show BASE and BULL on mid-cycle (decade-median) margin
     EPS as well as on the latest.
  2. Carry a guided margin step for one year, not two (2009 and 2018 pointed here too).
  3. Re-derive the signal thresholds on a rolling window, so that one growth era does not set the BEAR line for the
     next.
  4. Put the class change on a band, so that a 3% move cannot flip CHEAP and RICH (2011).
  5. Read the own-history P/E against a longer window or the market's multiple, so that one regime (a growth decade, a
     crisis) does not set the percentiles for the next (2008 and 2013-2014). 2015 and January-February 2018 cut the
     other way: at the same window's top percentiles the stock did lag. Any replacement must keep that call.
  6. When a guide states the charges inside its margin step, project growth from the step without them and treat the
     charges as a one-year level change. The Q3 FY18 release gave them in basis points; the Q2 FY18 release gave them
     only in dollars, so this would mean deriving a figure the company did not publish, a change to the Fremont rule.

  The tier's better ranking is itself an outcome pattern. Treat it as a question for the other tickers, not as a rule.
- **What 575 dates can and cannot show.** The weekly dates overlap: eleven years hold about five and a half
  non-overlapping two-year windows of one stock in one housing cycle. The class and tier patterns above are at best a
  few independent observations, and within a year they mostly restate the entry price. 2018 adds a warning about the
  yardstick: one event at the horizon (the 2020 crash) reversed a year's ranking, so read the m12-24 average beside the
  endpoint. Testing selection needs many tickers on the same dates.
