# LOW retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 835 weekly dates from 2008-01-04 to 2023-12-29. They are **labels and
hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time
build was committed: 2008 in 88b0255, 2009-2010 in bfe09e0, 2011-2012 in 0b9b6f8, 2013-2014 in 7eeed23, 2015-2016 in
304d9dc, 2017-2018 in fe7f63f, 2019-2020 in bc1e818, 2021-2023 in e9d57e8. Prices run to 2026-10-23 for the earlier
batches, 2026-10-26 from 2013 and 2026-10-28 from 2017; every horizon used here ends by 2025-12-29. Medians of an even
count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle over two years is +32.2%.

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

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 23 | +96% | +68% to +120% | 23 | 23 | +68% | 23 |
| class FAIR | 5 | +78% | +56% to +121% | 5 | 5 | +41% | 0 |
| class RICH | 24 | +93% | +66% to +118% | 24 | 24 | +63% | 0 |
| legacy tier BUY | 37 | +96% | +72% to +121% | 37 | 37 | +65% | 21 |
| legacy tier ACCUMULATE | 8 | +78% | +56% to +118% | 8 | 8 | +45% | 2 |
| legacy tier WATCHLIST | 5 | +85% | +73% to +90% | 5 | 5 | +44% | 0 |
| legacy tier AVOID | 2 | +74% | +66% to +74% | 2 | 2 | +35% | 0 |
| to 2019-02-22 (FY2018 guide, $5.08-5.13) | 7 | +75% | +66% to +90% | 7 | 7 | +43% | 0 |
| 2019-02-28 to 2019-03-29 (FY2019 guide; FY18 at GAAP $2.84) | 5 | +76% | +56% to +78% | 5 | 5 | +41% | 2 |
| 2019-04-05 to 2019-05-17 (FY2018 vintage, BEAR flat) | 7 | +81% | +72% to +102% | 7 | 7 | +40% | 7 |
| 2019-05-23 to 2019-11-15 ($5.45-5.65, +20 to +50bp) | 26 | +96% | +84% to +114% | 26 | 26 | +66% | 11 |
| from 2019-11-21 ($5.63-5.70, +40 to +60bp) | 7 | +118% | +109% to +121% | 7 | 7 | +66% | 3 |

- **Every date won, as in 2011-2013.** All 52 dates cleared the hurdle and beat SPY (median excess +43pp, lowest
  +15.7pp). Their two-year endpoints fall in 2021, at $160-257, and 47 landed nearest XBULL. Every date first lived
  through the 48.6% fall to the 2020-03-18 low. CHEAP returned +96%, RICH +93% and FAIR +78%. The CHEAP call held on all
  23 and RICH, which expects a miss, on none of its 24.
- **The endpoint set the order.** The best entries were the last: the dates from the Q3 FY19 print, at $116-120, returned
  +109% to +121% and end in November-December 2021 near the peak. The worst were 2019-02-22 to 2019-03-08, at $99-106:
  +56% to +69%, with endpoints in February-March 2021. Against the two-year return, the price ranked the dates
  backwards (+0.28) and Ratio B weakly (-0.31). On the m12-24 average price Ratio B gave -0.57, the gap +0.24 and the price
  -0.15.
- **FY18's GAAP weeks.** On the five dates to 2019-03-29 FY18 sat in the history at GAAP $2.84, so BEAR applied -35.3%
  twice and the tier read ACCUMULATE on all five (CHEAP on two). Taking the 10-K's adjusted $5.11 from the Q4 print
  would have read CHEAP on all five and BUY on four (README, "LOW 2019-2020"). They returned +56% to +78%, the least of
  the year, which is the February-March 2021 endpoint more than the encoding.
- **The watch list tests nothing here.** ECOMMERCE stayed on the watch list and changed no number.

## 2020 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 25 | +73% | +22% to +263% | 16 | 25 | +79% | 25 |
| class FAIR | 13 | +36% | +10% to +57% | 9 | 12 | +56% | 8 |
| class RICH | 14 | +41% | +10% to +109% | 11 | 14 | +49% | 0 |
| legacy tier BUY | 18 | +107% | +28% to +263% | 14 | 18 | +102% | 18 |
| legacy tier ACCUMULATE | 13 | +52% | +22% to +109% | 9 | 13 | +67% | 6 |
| legacy tier WATCHLIST | 14 | +35% | +10% to +57% | 8 | 13 | +40% | 9 |
| legacy tier AVOID | 7 | +34% | +10% to +41% | 5 | 7 | +40% | 0 |
| to 2020-02-21 (FY2019 guide, $5.63-5.70) | 7 | +98% | +82% to +109% | 7 | 7 | +68% | 1 |
| 2020-02-27 to 2020-05-15 (FY2020 guide, $6.45-6.65) | 12 | +118% | +73% to +263% | 12 | 12 | +121% | 12 |
| 2020-05-21 to 2020-11-13 (guide withdrawn) | 26 | +33% | +10% to +58% | 14 | 25 | +39% | 16 |
| 2020-11-19 to 2020-12-04 (fourth-quarter guide) | 3 | +45% | +41% to +48% | 3 | 3 | +39% | 0 |
| from 2020-12-11 (FY2020 guide $8.62-8.72, +170bp) | 4 | +30% | +28% to +32% | 0 | 4 | +27% | 4 |

- **The crash dates made the year, and the model read them CHEAP and BUY.** The 12 dates on the February guide, through
  the COVID crash, all read CHEAP and BUY and returned +73% to +263% (median +118%). 2020-03-20, at $66.36 and under the
  BEAR price, returned +263%. CHEAP led the year (+73%, against +41% for RICH and +36% for FAIR) and the tier ranked in
  order (BUY +107%, ACCUMULATE +52%, WATCHLIST +35%, AVOID +34%). The price alone ranked it better: -0.95 against -0.62 for Ratio
  B and -0.11 for the gap (on the m12-24 average, -0.99, -0.60 and -0.06).
- **After the withdrawal the class ranked nothing.** From 2020-05-21 the no-guide rules set BASE from the latest
  quarter's sales (+10.9%, then +30.1%) on FY19's $5.74, until the fourth-quarter guide. On the 29 dates from the
  withdrawal to the December guide (2020-05-21 to 2020-12-04) CHEAP returned a median +31% (8 dates), FAIR +36% (13) and
  RICH +34% (8). The CHEAP dates of late August to November, at $156-162, did no better than the FAIR
  and RICH dates around them; the fallback carried the boom quarter for two years. The encoding that was rejected before
  any outcome existed, keeping the withdrawn February guide, would have read CHEAP on 11 of these dates (May-July and
  the fourth-quarter-guide weeks), FAIR on 5 and RICH on 13 (August-November). In hindsight it ranks them in order:
  +46%, +34% and +24%. That is one window of one stock, and it does not change the rule; it is recorded because the
  call that moved the most classes is also the one most exposed to the charge of hindsight, and here it scored worse
  than its alternative.
- **The December guide projected the windfall twice.** The 2020-12-09 guide ($8.67, +170bp adjusted margin) set BASE at
  +40%/yr, the margin step carried as growth for two years: BASE and BULL EPS of $16.99 for FY2022. The four December
  dates read CHEAP and BUY at 18.2-18.8x and returned +28% to +32%. They beat SPY, so the CHEAP call held, but none cleared
  the hurdle (2020-12-11 missed it by 0.2pp), and they landed nearest BEAR ($139) against a BASE price of $316. This is
  2018's Orchard step in reverse, and hypothesis 2 below.
- **Landing:** XBULL 23, BASE 13, BULL 12, BEAR 4. 51 of 52 dates beat SPY (2020-10-23, $172.14, lagged by 1.9pp).

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 32 | +19% | +0% to +32% | 0 | 30 | +5% | 30 |
| class RICH | 20 | -7% | -18% to +17% | 0 | 7 | -8% | 13 |
| legacy tier BUY | 32 | +19% | +0% to +32% | 0 | 30 | +5% | 30 |
| legacy tier ACCUMULATE | 8 | +12% | +0% to +17% | 0 | 7 | +1% | 1 |
| legacy tier WATCHLIST | 2 | -7% | -14% to -7% | 0 | 0 | -4% | 2 |
| legacy tier AVOID | 10 | -14% | -18% to -6% | 0 | 0 | -16% | 10 |
| to 2021-02-19 (FY2020 guide, $8.62-8.72) | 7 | +26% | +22% to +28% | 0 | 7 | +17% | 7 |
| 2021-02-25 to 2021-05-14 (no FY21 guide; Q4 FY20 sales +26.7%) | 12 | +8% | +0% to +32% | 0 | 10 | +3% | 10 |
| 2021-05-20 to 2021-08-13 (12% margin; Q1 FY21 sales +24.1%) | 13 | +19% | +10% to +26% | 0 | 13 | +4% | 13 |
| 2021-08-19 to 2021-11-12 ($92 billion, 12.2%) | 13 | +5% | -18% to +17% | 0 | 7 | +0% | 6 |
| from 2021-11-18 ($95 billion, 12.4%) | 7 | -14% | -17% to -6% | 0 | 0 | -16% | 7 |

- **No date cleared the hurdle.** The best entry, 2021-02-25 at $158.52, returned +31.5% against +32.2%. Every date sat
  through a fall of about 34%, from the 2021-12-10 high ($261.38) to the 2022-06-16 low ($171.61). SPY's two-year return
  from these dates ran from -7.8% to +12.9%, so beating it took little.
- **The class and the tier ranked in order.** CHEAP returned +19% and beat SPY on 30 of 32 dates; RICH returned -7% and
  its call held on 13 of 20. The tier fell step by step: BUY +19%, ACCUMULATE +12%, WATCHLIST -7%, AVOID -14%. Ratio B
  ranked the dates at -0.90 and the gap at +0.90, the price alone at -0.88; on the m12-24 average all three were near
  -0.97. The RICH dates were the year's highest prices ($202-261), so the classes mostly restate the entry price.
- **The fallback read CHEAP, and the stock went nowhere.** On the 25 dates from the Q4 FY20 print to 2021-08-13 no guide
  gave sales, so BASE carried the latest quarter's +26.7%, then +24.1%, for two years (32.8% and 40.4%/yr). All read
  CHEAP and BUY. They returned +0.4% to +31.5% and beat SPY on 23, but none cleared the hurdle, and 24 landed nearest
  BEAR. The case the model weighted most was the farthest from the outcome. This is hypothesis 7 again, now on a boom
  quarter.
- **The EPS anchor read RICH, and RICH held.** From the Q2 FY21 print the multiple sat on FY20's $8.86 at the 95th-100th
  percentile of its own range (FY2021 had no EPS guide). The 20 RICH dates returned -18% to +17%. The ten AVOID dates from
  late October, at $234-261, returned -6% to -18%, and all ten missed the hurdle and lagged SPY.
- **Landing:** BEAR 37, BASE 15, BULL and XBULL none. BULL and XBULL equalled BASE on the CHEAP dates. From August BULL
  was the decade CAGR (22.5%) or BASE where higher, and XBULL the 2018-2020 run (31.7%).

## 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 45 | +27% | +7% to +56% | 13 | 4 | +13% | 17 |
| class RICH | 7 | -1% | -12% to +6% | 0 | 0 | -8% | 7 |
| legacy tier BUY | 45 | +27% | +7% to +56% | 13 | 4 | +13% | 17 |
| legacy tier ACCUMULATE | 1 | +6% | +6% to +6% | 0 | 0 | -5% | 1 |
| legacy tier WATCHLIST | 4 | +1% | -6% to +2% | 0 | 0 | -7% | 4 |
| legacy tier AVOID | 2 | -7% | -12% to -7% | 0 | 0 | -14% | 2 |
| to 2022-02-18 (FY2021 guides, $8.86) | 7 | -1% | -12% to +6% | 0 | 0 | -8% | 7 |
| 2022-02-24 to 2022-08-12 (FY2022 guide, $13.10-13.60) | 25 | +23% | +7% to +36% | 1 | 4 | +11% | 5 |
| 2022-08-18 to 2022-11-11 (the same ranges in words) | 13 | +39% | +15% to +56% | 9 | 0 | +17% | 9 |
| from 2022-11-17 (adjusted guide, $13.65-13.80) | 7 | +31% | +27% to +40% | 3 | 0 | +17% | 3 |

- **The class ranked in order; SPY ran away.** The seven RICH dates of January-February, still on the fiscal 2021 guides
  and $8.86 at 25-28x, returned -12% to +6%; all missed the hurdle and lagged SPY. The 45 CHEAP dates on the fiscal 2022
  guide, at 13-18x, returned +7% to +56% and cleared the hurdle on 13. But SPY's two-year return from these dates reached
  +39% at the median, so CHEAP beat it on only 4 (2022-03-25 to 2022-04-22) and its call held on 17.
- **The endpoint again set the order within CHEAP.** The entries from 2022-08-18 end in August-December 2024, near the
  2024-10-16 high ($284.05), and returned +15% to +56%. The spring entries end in spring and summer 2024 and returned
  +7% to +36%. Ratio B ranked the year at -0.46, the gap at +0.22 and the price at -0.64 (on the m12-24 average -0.73,
  +0.52 and -0.88).
- **The BEAR case sat at the market.** No year of the decade's history fell, so BEAR was flat EPS at the 10th-percentile
  multiple: $200-215 on the fiscal 2022 guide, about the price. Ratio B ran from -0.15 to 0.11 and the tier read BUY on all
  45. Every CHEAP date still lived through a fall of 22-27% inside its two years. Across the year the stock landed
  nearest BEAR on 31 dates and BASE on 21; BULL (the decade CAGR, 23.7-24.4%) and XBULL (the 2019-2021 run, 44.8%) never.

## 2023 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 46 | +22% | +2% to +38% | 2 | 0 | +18% | 2 |
| class FAIR | 1 | +1% | +1% to +1% | 0 | 0 | +7% | 0 |
| class RICH | 5 | +13% | -2% to +14% | 0 | 0 | +6% | 5 |
| legacy tier BUY | 52 | +19% | -2% to +38% | 2 | 0 | +18% | 7 |
| to 2023-02-24 (adjusted FY2022 guide) | 8 | +27% | +21% to +37% | 1 | 0 | +19% | 1 |
| 2023-03-02 to 2023-05-19 (FY2023 guide, $13.60-14.00) | 12 | +19% | +5% to +32% | 0 | 0 | +23% | 0 |
| 2023-05-24 to 2023-11-17 (adjusted, $13.20-13.60) | 26 | +15% | -2% to +38% | 1 | 0 | +14% | 3 |
| from 2023-11-22 (adjusted, about $13.00) | 6 | +22% | +13% to +25% | 0 | 0 | +15% | 3 |

- **No date beat SPY.** SPY returned +27% to +70% over the two years from these dates, the stock -2% to +38%; the median
  shortfall was 30 points. Two CHEAP dates cleared the hurdle: 2023-01-27 at $202.49 (+37.0%) and 2023-10-27 at $183.62
  (+37.7%), the year's lowest weekly close. The CHEAP call held on 2 of 46, and RICH, which expects a miss, held on all 5.
- **The class still ranked CHEAP above RICH** (+22% against +13%; the one FAIR date, 2023-07-14, returned +1%). The RICH
  dates were the July and December highs ($223-235). Ratio B ranked the year at -0.63, the gap at +0.73 and the price at
  -0.64; on the m12-24 average -0.98, +0.82 and -0.99, again mostly the price.
- **The low BASE came closest.** The fiscal 2023 sales guides, read against FY22's 53 weeks with the Canadian business,
  set BASE at +2.7% to -3.5%/yr, and BASE was the nearest case on 36 dates (BEAR on 16). The multiple's percentile read
  CHEAP and the BEAR price (flat EPS at 14.5-14.7x) put the tier at BUY on all 52, yet the median date returned +19%.
- **Three-year returns** exist for the dates to 2023-10-27. They run from -8% (2023-09-01) to +45% (2023-02-24), and nine
  of the sixteen entries from 2023-07-14 to 2023-10-27 are negative.

## 2008-2023 together (835 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 329 | +31% | -14% to +263% | 156 | 211 | +22% | 232 |
| class FAIR | 130 | +37% | -11% to +121% | 75 | 96 | +24% | 47 |
| class RICH | 376 | +41% | -18% to +146% | 217 | 239 | +24% | 124 |
| legacy tier BUY | 381 | +30% | -17% to +263% | 170 | 218 | +20% | 230 |
| legacy tier ACCUMULATE | 139 | +44% | -12% to +129% | 86 | 112 | +26% | 70 |
| legacy tier WATCHLIST | 124 | +42% | -14% to +107% | 82 | 91 | +28% | 39 |
| legacy tier AVOID | 191 | +39% | -18% to +99% | 110 | 125 | +31% | 64 |

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
| 2019 | +96% (23) | +78% (5) | +93% (24) | +96% (37) | +78% (15) |
| 2020 | +73% (25) | +36% (13) | +41% (14) | +107% (18) | +36% (34) |
| 2021 | +19% (32) | none | -7% (20) | +19% (32) | -7% (20) |
| 2022 | +27% (45) | none | -1% (7) | +27% (45) | -1% (7) |
| 2023 | +22% (46) | +1% (1) | +13% (5) | +19% (52) | none |

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
| 2019 | -0.31 | +0.08 | +0.28 |
| 2020 | -0.62 | -0.11 | -0.95 |
| 2021 | -0.90 | +0.90 | -0.88 |
| 2022 | -0.46 | +0.22 | -0.64 |
| 2023 | -0.63 | +0.73 | -0.64 |

- **The class ranked some years and not the cycle.** CHEAP beat RICH in 2008-2010, and RICH beat CHEAP in 2011-2012. No
  date read CHEAP in 2013-2015. FAIR beat RICH in 2013-2014; RICH held on 46 of 52 dates in 2015; in 2016 CHEAP and RICH
  tied (+52%, +53%) and FAIR, at the year's high prices, did worst. In 2017 every class beat SPY and CHEAP did worst
  (+35%, against +43% for FAIR and +40% for RICH). In 2018 RICH beat CHEAP (+46% against +18%) on endpoints set by the
  2020 crash. In 2019 every class won (CHEAP +96%, RICH +93%, FAIR +78%); in 2020 CHEAP led (+73%) on the crash dates.
  In 2021-2023 CHEAP beat RICH every year (+19% against -7%, +27% against -1%, +22% against +13%), but from 2022 it
  lagged SPY on 87 of 91 dates. Pooled: RICH +41%, FAIR +37%, CHEAP +31%.
- **The tier ranked better, mostly as a price.** A lower Ratio B went with a higher return in thirteen of sixteen years
  (2012, 2017 and 2018 the exceptions; 2018 ranks the right way on the m12-24 average). The price alone ranked the dates
  as well or better in ten of 2008-2020; in 2021-2023 the two ranked about equally (-0.90 and -0.88, -0.46 and -0.64,
  -0.63 and -0.64). Ratio B clearly beat the price only in 2015, when the guide rollover moved Ratio B without the price,
  and in 2019, when the endpoints at the 2021 peak made the price rank backwards. The pooled tier rows mix years: 176 of
  the 191 AVOID dates fall in 2012-2015, 2018 and 2021-2022, and 129 of the 381 BUY dates in 2021-2023, which is why AVOID
  shows +39% against BUY's +30%.
- **One mechanism under the failures: the model projects from where the latest regime stands.** In the fact sheet the
  EBIT margin went from 10.98% (FY06) and 9.74% (FY07) to 6.53-7.29% in FY09-FY11. It then recovered: 7.05% (FY12),
  7.77% (FY13), 8.53% (FY14), 9.31% adjusted (FY15), 8.99% (FY16); the FY17 operating margin was 9.60%, and FY20-FY22's
  10.77%, 12.56% and 13.04% (adjusted). EPS went from $1.98 to $1.21-1.43, then to $3.29, $3.99 and $4.39 adjusted, and
  on to $8.86, $12.04 and $13.81 in FY20-FY22. Method r2 projects from that base in three ways:
  - it carries the latest guided margin step for two years, in 2018 a step made mostly of exit charges (-180bp became
    BASE -12.2%/yr);
  - it takes BULL from the decade's EPS CAGR on the latest EPS (21-25% in 2008, 8.5-11% in 2011-2012), and once BASE
    exceeds that CAGR, BULL can add nothing to BASE (from 2012-02-28 to 2018-02-23);
  - it scores net sales against rule T's BASE line of +10% or more, set from the fiscal 1997-2006 growth decade.

  The net-sales signal read BEAR on 720 of the 835 dates, which held the proxy composite at 1.30-2.70 until 2020 and at
  1.60-2.20 from August 2021. Any rally then opened a gap to the market composite and read RICH. In 2020 the pandemic
  quarters (+30.1%, +28.3%) scored XBULL, the proxy composite reached 3.70, and with no guide in force the fallback carried
  those quarters as BASE growth. 2021 repeated it: with no sales guide the fallback carried +26.7%, then +24.1%, for two
  years on 25 CHEAP dates, none of which cleared the hurdle. And from the Q4 FY21 print BULL and XBULL rest on the
  2019-2021 surge (the decade CAGR 23-24%, the best two-year run 44.8%): no date of 2021-2023 landed nearest either.
- **The P/E window lags a regime change, but 2015 shows the cost of reading that as a rule.** In 2008 the window
  (1998-2007) held a growth decade's 14-43x, so 11-17x read as the 0th-27th percentile: CHEAP, while the stock went
  nowhere. In 2013-2014 the window held the crisis's 11-15x, so 17-26x read as the 56th-100th percentile: RICH, while the
  stock landed nearest the XBULL price on 83 of 104 dates. In 2015 the same window read 20-27x as the 85th-100th
  percentile, and this time RICH held: the stock lagged SPY on 46 of 52 dates and landed near BASE. January-February 2018
  repeats it: at the 92nd-100th percentile RICH held on 4 of 8 dates. The recovery that beat every case in 2011-2014
  (BULL or XBULL on 208 of 209 dates) had run its course by 2015; in 2015-2017, 120 of 156 dates landed nearest BASE.
  2021-2023 show both sides again: at the 95th-100th percentile (late 2021, on FY20's EPS) RICH held on 13 of 20 dates,
  and at the 2nd-39th percentile (2022-2023) CHEAP returned +27% and +22% at the median but lagged SPY on 87 of 91 dates.
  UNP's 2010 (FINDINGS there: the P/E on trough EPS read RICH while earnings recovered) is the same pattern on another
  ticker.
- **Hypotheses for a new method version.** Test each on other tickers' cycles before any change, and never fit it to
  LOW's outcomes:
  1. When the latest margin sits far below the decade median, show BASE and BULL on mid-cycle (decade-median) margin
     EPS as well as on the latest.
  2. Carry a guided margin step for one year, not two (2009, 2018 and December 2020 pointed here too).
  3. Re-derive the signal thresholds on a rolling window, so that one growth era does not set the BEAR line for the
     next.
  4. Put the class change on a band, so that a 3% move cannot flip CHEAP and RICH (2011).
  5. Read the own-history P/E against a longer window or the market's multiple, so that one regime (a growth decade, a
     crisis) does not set the percentiles for the next (2008 and 2013-2014). 2015 and January-February 2018 cut the
     other way: at the same window's top percentiles the stock did lag. Any replacement must keep that call.
  6. When a guide states the charges inside its margin step, project growth from the step without them and treat the
     charges as a one-year level change. The Q3 FY18 release gave them in basis points; the Q2 FY18 release gave them
     only in dollars, so this would mean deriving a figure the company did not publish, a change to the Fremont rule.
  7. When no guide stands, test a fallback that does not carry one quarter's sales growth for two years: the trailing
     four quarters, or a withdrawn guide's last numbers kept in the note. LOW's withdrawn-guide window of 2020 ranked in
     order under the rejected encoding and not under the applied one; UNP's fallback carried its 2009 and 2020 trough
     quarters the same way (its README, "Seen in the build"). 2021 adds a boom case: the fallback carried +26.7% and
     +24.1% on 25 CHEAP dates, none of which cleared the hurdle. One stock: test it on other tickers' 2020 withdrawals
     before any change.
  8. When the decade's history has no down year, the BEAR case is flat EPS at the 10th-percentile multiple. In 2022-2023
     that BEAR price sat at the market: Ratio B ran from -0.15 to 0.22 and the tier read BUY on all 97 dates from
     2022-02-24, while the stock lagged SPY by 14 and 30 points at the median. 2008 was the same (FINDINGS above: no down
     year, BUY all year, the stock ended at BEAR). Test a BEAR case built from the decade's worst margin on the guided
     sales, beside the worst EPS year, on other tickers with a decade of uninterrupted growth.

  The tier's better ranking is itself an outcome pattern. Treat it as a question for the other tickers, not as a rule.
- **What 835 dates can and cannot show.** The weekly dates overlap: sixteen years hold about eight non-overlapping two-year
  windows of one stock in one housing cycle. The class and tier patterns above are at best a few independent
  observations, and within a year they mostly restate the entry price. 2018 adds a warning about the yardstick: one event
  at the horizon (the 2020 crash) reversed a year's ranking, so read the m12-24 average beside the endpoint. 2020 is the
  same event at the entry: the price alone ranked its dates at -0.95. 2022-2023 add the benchmark: the CHEAP call failed
  on 72 of 91 dates that returned +22-27% at the median, because SPY returned +39% and +49% at the median over the same
  two years. Testing selection needs many tickers on the same dates.
