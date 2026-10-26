# LOW retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 157 weekly dates from 2008-01-04 to 2010-12-31. They are **labels and
hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time
build was committed: 2008 in 88b0255, 2009-2010 in bfe09e0. Prices run to 2026-10-23. Medians of an even count take the upper middle value
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

## 2008-2010 together (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 70 | +24% | -11% to +102% | 26 | 42 | +18% | 48 |
| class FAIR | 28 | +18% | -11% to +49% | 5 | 21 | -3% | 10 |
| class RICH | 59 | +12% | -17% to +74% | 10 | 5 | +9% | 44 |

- **The ranking held in every year and in the pool.** CHEAP beat RICH on the median 2-year return in 2008, 2009 and 2010,
  and matched or beat FAIR (2009's two FAIR dates tie it), and RICH beat SPY on 5 of 59 dates. Read the class as a ranking: on its own it cleared the hurdle on 26 of 70
  CHEAP dates.
- **Where it failed is the same place, twice.** In 2008 the own-history multiple and the decade CAGR were anchors from a
  growth decade, so the year read CHEAP and BUY while the stock went nowhere. In early 2009 the guided margin cut, carried
  for two years, made the trough read RICH. Both come from extrapolating the latest regime two years forward: the decade's
  in 2008, the trough guide's in 2009. UNP shows the second pattern with its no-guide fallback (2009, 2015-2016, 2020).
  Hypothesis for a new method version, to test on other tickers before any change: cap how far BASE may sit from the
  decade median growth, or carry a guided step for one year rather than two.

