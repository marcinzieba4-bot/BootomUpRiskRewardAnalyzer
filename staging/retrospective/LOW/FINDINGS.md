# LOW retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 366 weekly dates from 2008-01-04 to 2014-12-31. They are **labels and
hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time
build was committed: 2008 in 88b0255, 2009-2010 in bfe09e0, 2011-2012 in 0b9b6f8, 2013-2014 in 7eeed23. Prices run to
2026-10-23 for the earlier batches and 2026-10-26 for 2013-2014; every horizon used here ends by 2017-12-29. Medians of
an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle over two years is +32.2%.

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

## 2008-2014 together (366 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 116 | +44% | -11% to +153% | 72 | 88 | +25% | 94 |
| class FAIR | 60 | +50% | -11% to +107% | 37 | 53 | +20% | 14 |
| class RICH | 190 | +54% | -17% to +146% | 131 | 133 | +43% | 47 |
| legacy tier BUY | 169 | +31% | -17% to +153% | 83 | 103 | +20% | 112 |
| legacy tier ACCUMULATE | 54 | +47% | -12% to +129% | 31 | 36 | +20% | 34 |
| legacy tier WATCHLIST | 49 | +69% | +16% to +107% | 43 | 45 | +49% | 5 |
| legacy tier AVOID | 94 | +59% | +7% to +99% | 83 | 90 | +44% | 4 |

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

- **The class ranked the downturn, inverted in the recovery, and had little to rank after it.** CHEAP beat RICH in
  2008, 2009 and 2010. RICH beat CHEAP in 2011 (+125% against +77%) and 2012 (+85% against +78%). In 2013 and 2014 no date
  read CHEAP; FAIR beat RICH in both years (+107% on one date, then +74% against +41%). Pooled, the order is upside down
  (RICH +54%, FAIR +50%, CHEAP +44%), because RICH dates crowd into the 2011-2014 recovery. Across the cycle the class did
  not rank LOW's outcomes.
- **The tier ranked better, but mostly as a price.** A lower Ratio B went with a higher return in six of seven years
  (Spearman -0.43 to -0.89; 2012 +0.18). The price alone ranked the dates as well or better in six of the seven years,
  and nearly as well in 2014 (-0.84 against -0.89). Within one stock and one year, Ratio B mostly says "buy lower". The pooled tier rows mix years: AVOID falls only in
  2010-2014, which is why it shows +59% against BUY's +31%.
- **One mechanism under the failures: the model projects from where the latest regime stands.** In the fact sheet the
  EBIT margin went from 10.98% (FY06) and 9.74% (FY07) to 6.53-7.29% in FY09-FY11, then 7.05% (FY12) and 7.77% (FY13), and
  EPS from $1.98 to $1.21-1.43, then $1.69 and $2.14. Method r2 projects from that base in three ways:
  - it carries the latest guided margin step for two years;
  - it takes BULL from the decade's EPS CAGR on the latest EPS (21-25% in 2008, 8.5-11% in 2011-2012), and once BASE
    exceeds that CAGR, BULL can add nothing to BASE (2013-2014);
  - it scores net sales against rule T's BASE line of +10% or more, set from the fiscal 1997-2006 growth decade.

  The net-sales signal read BEAR on 341 of the 366 dates, which held the proxy composite at 1.30-2.70. Any rally then
  opened a gap to the market composite and read RICH.
- **The P/E window lags a regime change in both directions.** In 2008 the window (1998-2007) held a growth decade's
  14-43x, so 11-17x read as the 0th-27th percentile: CHEAP, while the stock went nowhere. In 2013-2014 the ten-year
  window held the crisis's 11-15x, so 17-26x read as the 56th-100th percentile: RICH, while the stock landed nearest the
  XBULL price on 83 of 104 dates. In 2011-2014 the outcomes landed at BULL or XBULL on 208 of 209 dates: the market
  priced a recovery from trough earnings, and a re-rating, that no rule of the method projects. UNP's 2010 (FINDINGS
  there: the P/E on trough EPS read RICH while earnings recovered) is the same pattern on another ticker.
- **Hypotheses for a new method version.** Test each on other tickers' cycles before any change, and never fit it to
  LOW's outcomes:
  1. When the latest margin sits far below the decade median, show BASE and BULL on mid-cycle (decade-median) margin
     EPS as well as on the latest.
  2. Carry a guided margin step for one year, not two (2009 pointed here too).
  3. Re-derive the signal thresholds on a rolling window, so that one growth era does not set the BEAR line for the
     next.
  4. Put the class change on a band, so that a 3% move cannot flip CHEAP and RICH (2011).
  5. Read the own-history P/E against a longer window or the market's multiple, so that one regime (a growth decade, a
     crisis) does not set the percentiles for the next (2008 and 2013-2014).

  The tier's better ranking is itself an outcome pattern. Treat it as a question for the other tickers, not as a rule.
- **What 366 dates can and cannot show.** The weekly dates overlap: seven years hold about three and a half
  non-overlapping two-year windows of one stock in one housing cycle. The class and tier patterns above are at best a few
  independent observations, and within a year they mostly restate the entry price. Testing selection needs many tickers
  on the same dates.
