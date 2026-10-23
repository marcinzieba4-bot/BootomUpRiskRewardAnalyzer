# UNP retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 53 weekly dates from 2008-01-04 to 2008-12-31. They are **labels and
hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed: January-March in 68cbbb6, April-December in 0019904. Medians of an even count
take the upper middle value (`statistics.median_high`). Prices are on each date's share basis (2-for-1 split
effective 2008-05-29).

| Group | Dates | Median 2-yr total return | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price |
|---|---|---|---|---|---|
| class CHEAP | 13 | +85% | 13 | 13 | +48% |
| class FAIR | 8 | +22% | 1 | 8 | -5% |
| class RICH | 32 | +2% | 0 | 32 | -12% |
| legacy tier BUY | 7 | +100% | 7 | 7 | +60% |
| legacy tier ACCUMULATE | 5 | +53% | 5 | 5 | +22% |
| legacy tier WATCHLIST | 9 | +22% | 2 | 9 | -5% |
| legacy tier AVOID | 32 | +2% | 0 | 32 | -12% |
| price below the EPP floor | 6 | +102% | 6 | 6 | +62% |
| CHEAP, above the floor | 7 | +53% | 7 | 7 | +22% |

- **The calls ranked the outcomes in order.** CHEAP did better than FAIR, which did better than RICH, and the tier
  order was the same: BUY > ACCUMULATE > WATCHLIST > AVOID. All 13 CHEAP dates (2008-10-03 to 2008-12-31, except
  FAIR on 2008-10-31) cleared the hurdle. None of the 32 RICH dates did.
- **RICH was right on price, wrong against the market.** RICH dates lost money on the m12-24 average price (-12%) and
  were flat over two years. Every one still beat SPY, because the market fell further. So every RICH call "missed" its
  own test, which expects RICH to lag the benchmark. On this stock in 2008, RICH read "don't buy here", not "will
  underperform".
- **The turn came with the price, not the numbers.** The class moved from RICH (late September, 18-19x) to CHEAP
  (2008-10-03, 15.5x) as the stock fell. Q3 carloads were -5%, but revenue per car was +22% and the operating ratio
  improved. The six dates below the EPP floor (2008-11-21 and 2008-12-05 to 2008-12-31, at 10.7-11.9x) returned +98% to
  +122%.
- **The BEAR case never came.** All 53 two-year outcomes landed in BASE or BULL. The worst point (2009-03-09) was
  still above every date's BEAR price. The BEAR rule (the decade's worst EPS year, 2004 at -29%, repeated for two
  years) set Ratio B high on most RICH dates. Test it on other cyclicals before any method change.
- **One stock, one crash.** Nearly all the spread between classes comes from buying before or after the
  October-December 2008 decline. This mostly tests "buy lower". Testing selection needs many tickers on the same
  dates.
