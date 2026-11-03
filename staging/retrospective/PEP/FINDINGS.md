# PEP retrospective findings (hindsight)

Patterns seen in `outcome.json` for the PEP weekly dates: 53 from 2008-01-04 to 2008-12-31, 104 from 2009-01-09 to 2010-12-31, 157
from 2011-01-07 to 2013-12-31, 156 from 2014-01-10 to 2016-12-30, 209 from 2017-01-06 to 2020-12-31 and 156 from 2021-01-08 to
2023-12-29. They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only
after its point-in-time build was committed and pushed (2008: 4b429b6; 2009-2010: 88ba341, documented in 55a6818; 2011-2013: 29c50f2,
documented in b02f4d4; 2014-2016: bc27375, documented in 03bc69c; 2017-2020: 53e0347, documented in b1ed84f; 2021-2023: e58b7d3,
documented in 17258fc). Prices run to 2026-10-30 (2017-2020 and 2021-2023: 2026-11-02); the 2008 batch's two-year horizons end by
2010-12-30 (three-year: 2011-12-30), the 2009-2010 batch's by 2012-12-28 (2013-12-30), the 2011-2013 batch's by 2015-12-30
(2016-12-30), the 2014-2016 batch's by 2018-12-28 (2019-12-30), the 2017-2020 batch's by 2022-12-30 (2023-12-29), the 2021-2023
batch's by 2025-12-29 (three-year horizons only for the 147 dates to 2023-10-27, ending by 2026-10-27). Medians of an even count take
the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 53 | -0% | -18% to +37% | 2 | 38 | -10% | 39 |
| legacy tier BUY | 52 | +0% | -14% to +37% | 2 | 38 | -10% | 39 |
| legacy tier ACCUMULATE | 1 | -18% | -18% | 0 | 0 | -29% | 0 |
| FY06 EPS anchor (to the Q4 2007 print) | 5 | -8% | -18% to -7% | 0 | 4 | -22% | 4 |
| FY07 anchor, February to September | 34 | -1% | -11% to +4% | 0 | 33 | -11% | 33 |
| October-December | 14 | +27% | +2% to +37% | 2 | 1 | +18% | 2 |

- **CHEAP on every date; the call held on 39 of 53, mostly by beating a falling market.** On the 39 dates from January to
  September SPY returned -19% to -1% over two years and PEP beat it on 37, by up to 19pp, while its own two-year return was -18% to
  +4% and none cleared the hurdle. From October PEP returned +2% to +37% (median +27%), but SPY returned +8% to +57% over the same
  windows, so the call held on 2 of those 14: 2008-10-15 ($51.25, +37%) and 2008-10-24 ($51.76, +33%), the two that cleared the
  hurdle. One-year returns had a median of -16%; three-year returns ran from -10% to +35% (median +6%).
- **The floor distance and the entry price ranked the outcomes; the signal composite ranked them backwards.** Across the 53 dates
  the EPP gap ranks the two-year returns at Spearman -0.92 (-0.93 on the m12-24 average), the entry price at -0.88 and Ratio B at
  -0.83; the adjusted gap barely ranks them (+0.17). The proxy composite ranks them at -0.54: it read 2.30 on the five FY06-anchored
  dates (median two-year return -8%), 2.50 on the 23 dates of the Q4 2007 and Q2 2008 prints (-2%), 2.10 on the 13 of Q1 2008 (+1%)
  and 1.75 on the 12 of Q3 2008 (+28%). The weakest trailing signals came with the best entries, as in NKE's and AAPL's 2008 batches.
  Hypothesis for the method, not a rule: last-quarter operating signals lag the price and lean pro-cyclical. Test it on other
  tickers and years before any method change; never fit it to PEP's outcomes. One stock through one crash mostly tests "buy lower".
- **Every two-year price landed nearest BEAR, and every path went below it.** The two-year price ($59-67) was 1.07-1.25 times the
  BEAR price, 0.56-0.78 times BASE and 0.43-0.55 times BULL. Every date's two-year window included the 2009-03-09 close ($45.81),
  below its BEAR price ($50-55): drawdowns of 18-42%. BASE (+6.7% to +16.0%/yr at the median multiple of 23-24x) was the far-off
  anchor, not the near one.
- **The one ACCUMULATE date was the highest entry.** 2008-01-11 ($77.78, Ratio B 0.77) returned -18% over two years, the least of
  the 53, and is the only January-September date where the call failed (SPY -15%).
- **The encoding calls, seen afterwards.** None of the alternatives in retro/README.md ("PEP") changes a 2008 class. Reading "at
  least" as a point, or keeping FY1997, would each have turned 2008-01-11 from ACCUMULATE to BUY, and that date returned -18%. That
  is a fact about one date, not a reason to change an encoding: the calls were decided before scoring and stay; changing a rule
  means a new method version tested elsewhere.

## 2009-2010 (104 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 104 | +16% | +3% to +48% | 20 | 2 | +6% | 22 |
| legacy tier BUY | 104 | +16% | +3% to +48% | 20 | 2 | +6% | 22 |
| FY07 anchor (to the Q4 2008 print) | 5 | +36% | +26% to +37% | 4 | 0 | +26% | 4 |
| FY08 at GAAP, Q4 2008 print | 10 | +34% | +28% to +42% | 6 | 0 | +26% | 6 |
| Q1 2009 print | 13 | +35% | +28% to +48% | 10 | 0 | +22% | 10 |
| Q2 2009 print | 11 | +17% | +8% to +23% | 0 | 1 | +15% | 1 |
| Q3 2009 print and the FY09 revenue guide | 18 | +11% | +6% to +19% | 0 | 1 | +7% | 1 |
| FY09 at GAAP, Q4 2009 print | 10 | +6% | +3% to +11% | 0 | 0 | +0% | 0 |
| Q1 2010 print | 13 | +15% | +7% to +22% | 0 | 0 | +2% | 0 |
| Q2 2010 print (BASE +38%/yr) | 11 | +16% | +12% to +20% | 0 | 0 | +0% | 0 |
| Q3 2010 print (BASE +42%/yr) | 13 | +13% | +10% to +16% | 0 | 0 | +4% | 0 |
| below the BEAR price (Ratio B < 0) | 14 | +40% | +26% to +48% | 12 | 0 | +30% | 12 |
| above the EPP floor | 13 | +9% | +6% to +19% | 0 | 0 | +6% | 0 |

- **CHEAP on every date; the call held on 22 of 104, all in 2009.** On the 27 dates to 2009-07-10 ($47-56) PEP returned +26% to
  +48% over two years (median +35%) and 20 cleared the hurdle, but SPY's rebound returned +39% to +99% over the same windows, so
  PEP beat it on none. On the 77 dates from 2009-07-17 PEP returned +3% to +28% (median +13%) against SPY's +10% to +45%: the call
  held on 2, 2009-08-21 and 2009-12-18, each 0.7pp ahead of SPY. All 52 dates of 2010 failed: +3% to +22% (median +13%), 1.7 to
  22.5pp behind SPY, with one-year returns below zero on 14 of them. Three-year returns ran from +18% to +47% (median +36%), ahead
  of SPY on one date (2010-04-23).
- **The floor distance and the entry price ranked 2009, not 2010.** Across the 104 dates the EPP gap ranks the two-year returns at
  Spearman -0.76, Ratio B at -0.81 and the entry price at -0.74 (-0.97 on the m12-24 average); the adjusted gap at +0.14 and the
  proxy composite at -0.49. Within 2009 they rank them at -0.92, -0.89 and -0.94 (adjusted gap +0.54, proxy -0.78); within 2010,
  when the price stayed between $59.51 and $67.00, at -0.26, -0.41 and -0.48 (adjusted gap +0.07, proxy +0.10). The 14 dates below
  the BEAR price (January to May 2009) had a median of +40% and 12 cleared the hurdle; the 13 above the EPP floor (October 2009 to
  February 2010) had +9% and none did. As in 2008, the outcome followed the entry price: the batch mostly tests "buy lower".
- **The proxy composite again ranked 2009 backwards.** It read 1.45 on the Q4 2008 print (median two-year return +34%), 2.15 on Q1
  and Q2 2009 (+31%), 2.45 on Q3 2009 (+11%) and 2.30 on Q4 2009 (+6%). In 2010 it rose to 3.05 and 3.10 on the acquired servings
  and revenue (medians +16% and +13%), no better than the 1.75 of Q1 2010 (+15%). The 2008 hypothesis (last-quarter operating
  signals lag the price and lean pro-cyclical) gains a second: acquired growth lifts the operating signals without saying anything
  about the business owned before. Test both on other tickers and years; never fit them to PEP's outcomes.
- **Two-year prices landed nearest BEAR on 80 dates and BASE on 24** (2009-04-21 to 2009-07-23 and 2009-12-04 to 2010-02-05). The
  two-year price ($60-73) was 1.18-1.44 times BEAR, 0.42-0.88 times BASE and 0.39-0.67 times BULL. The 20 dates to 2009-05-22 saw
  the path go below their BEAR price (the 2009-03-09 close of $45.81 and the April-May lows); no later date did. From Q2 2010 BASE
  ($153-161, the acquired growth compounded for two years) was 2.1-2.4 times the two-year price: the encoding call flagged in
  retro/README.md, seen afterwards. It moved no class.
- **Across 2008-2010 (157 dates) CHEAP held on 61:** 39 in 2008 by losing less than a falling market, 22 in 2009 by clearing the
  hurdle from near the bottom, none from 2010-01-08 on. The two-year return was positive on every 2009-2010 date, but the call asks
  for the hurdle or the market, and PEP met neither after mid-2009. Hypothesis, not a rule: for a durable, slow-growing stock, CHEAP
  against its own P/E history marked limited downside more than outperformance, and the absolute payoff came only from entries near
  or below the BEAR price. Test it on other tickers before any method change.
- **The encoding calls, seen afterwards.** None of the six alternatives in retro/README.md ("PEP 2009-2010") changes a 2009-2010
  class or tier, so the outcomes say nothing about them. The calls were decided before scoring and stay.

## 2011-2013 (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 107 | +34% | +11% to +50% | 64 | 19 | +22% | 78 |
| class RICH | 50 | +25% | +18% to +41% | 3 | 17 | +16% | 30 |
| legacy tier BUY | 111 | +34% | +11% to +50% | 65 | 19 | +21% | 81 |
| legacy tier ACCUMULATE | 2 | +37% | +36% to +37% | 2 | 0 | +20% | 0 |
| legacy tier WATCHLIST | 18 | +27% | +20% to +31% | 0 | 6 | +19% | 12 |
| legacy tier AVOID | 26 | +22% | +18% to +29% | 0 | 11 | +14% | 15 |
| FY09 anchor (to the Q4 2010 print) | 5 | +16% | +11% to +20% | 0 | 1 | +4% | 1 |
| FY10 anchor, Q4 2010 print | 11 | +27% | +20% to +29% | 0 | 11 | +8% | 11 |
| Q1 2011 print | 12 | +24% | +22% to +30% | 0 | 2 | +6% | 2 |
| Q2 2011 print | 12 | +38% | +32% to +41% | 11 | 2 | +22% | 11 |
| Q3 2011 print | 17 | +35% | +24% to +44% | 11 | 0 | +23% | 11 |
| FY11 anchor, Q4 2011 print | 11 | +33% | +32% to +36% | 7 | 0 | +27% | 7 |
| Q1 2012 print | 13 | +35% | +32% to +37% | 10 | 0 | +21% | 10 |
| Q2 2012 print | 12 | +35% | +27% to +42% | 8 | 1 | +18% | 11 |
| Q3 2012 print | 17 | +44% | +36% to +50% | 17 | 2 | +25% | 17 |
| FY12 anchor, Q4 2012 print | 9 | +29% | +26% to +41% | 3 | 0 | +19% | 6 |
| Q1 2013 print | 14 | +22% | +18% to +25% | 0 | 0 | +14% | 14 |
| Q2 2013 print | 12 | +24% | +18% to +30% | 0 | 6 | +19% | 6 |
| Q3 2013 print | 12 | +27% | +20% to +29% | 0 | 11 | +16% | 1 |
| 2011 | 52 | +29% | +11% to +44% | 20 | 16 | +10% | 34 |
| 2012 | 52 | +35% | +24% to +50% | 38 | 2 | +23% | 41 |
| 2013 | 53 | +25% | +18% to +43% | 9 | 18 | +17% | 33 |
| above the EPP floor | 58 | +26% | +18% to +43% | 9 | 18 | +17% | 36 |

- **CHEAP on 107 dates; the call held on 78, mostly by clearing the hurdle** (64 cleared it, 19 beat SPY; median two-year return
  +34%). In 2011 it held on 34 of 52: the 11 dates from the Q4 2010 print to April beat SPY (+20% to +29% against +17% to +26%) and
  22 of the 29 from 2011-07-22 to 2012-02-03 cleared the hurdle, while January 2011 (+11% to +19%) and mid-May to mid-July 2011
  (+22% to +30%, SPY +21% to +34%) missed both. In 2012 it held on 38 of 49, every one by clearing the hurdle: PEP returned +24% to
  +50%, SPY +34% to +56%, and PEP beat it on 2. The 6 CHEAP dates of January-February 2013 all held (+36% to +43%).
- **RICH, new in this range, on 50 dates: the call held on 30.** RICH expects the stock to miss the hurdle and lag SPY. It held on
  the three August 2012 dates (+27% to +32% against SPY's +42% to +46%) and on 27 of the 47 dates from 2013-02-15. It failed on
  2013-02-15 to 2013-03-01, which cleared the hurdle (+36% to +41%), and on the 17 dates from 2013-08-23 whose two-year windows
  ended in late 2015, when SPY returned +15% to +23% and PEP +20% to +29%. The RICH dates still returned +18% to +41% (median +25%)
  and a median +38% over three years, ahead of SPY on 39 of 50: RICH marked a lower return, not a loss.
- **The floor distance ranked 2011 and 2013, not 2012.** Across the 157 dates the EPP gap ranks the two-year returns at Spearman
  -0.53, the entry price at -0.43, Ratio B at -0.26, the adjusted gap at +0.16 and the proxy composite at -0.38. Within 2011 the EPP
  gap reads -0.72, within 2013 -0.65, within 2012 +0.10: that year the price stayed between $62.52 and $73.39 and every entry did
  well. By distance: entries 10-20% below the floor returned a median +36.5% (20 of 24 cleared the hurdle), 0-10% below +32.5% (38
  of 75), 0-10% above +35.6% (6 of 11), more than 10% above +24.7% (3 of 47). The batch again mostly tests "buy lower".
- **The proxy composite ranked 2011 backwards again** (-0.78): 3.10, 2.90 and 3.55 with the acquired servings and revenue (to July
  2011) came with +11% to +30%, 2.30 and 1.95 (Q2 and Q3 2011, gross margin -175bp and -290bp) with +24% to +44%. Within 2012 and
  2013 it ranks nothing (+0.06, -0.09). The 2008-2010 hypotheses stand untested elsewhere: trailing operating signals lag the price,
  and acquired growth lifts them without saying anything about the business owned before.
- **Two-year prices landed nearest BASE on 65 dates, BULL on 64 and BEAR on 28.** The BEAR landings are the dates to July 2011, when
  BASE and BULL compounded the acquired growth ($131-161): the two-year price ($69-85) was 0.43-0.65 times BASE. From the Q2 2012
  print BASE was too low (+1% to +5%/yr, the refranchisings in it): the two-year price ($88-102) was 1.06-1.29 times BASE, nearest
  BULL from the Q3 2012 print. No two-year path went below its BEAR price, the first range since 2008 where none did.
- **Across 2008-2013 (314 dates) CHEAP held on 139 of 264 and RICH on 30 of 50.** CHEAP held by losing less than a falling market in
  2008 and by clearing the hurdle from low entries in 2009 and 2011-2013; it beat SPY on 59 of 264. Hypothesis, not a rule: for PEP
  the method worked as a "buy lower" filter against an absolute hurdle, and lagged the market in every rising stretch. Test it on
  other tickers and years before any method change; never fit it to PEP's outcomes.
- **The encoding calls, seen afterwards.** The core basis would have made 4 RICH dates CHEAP (2012-08-03, 2012-08-17, 2012-08-24 and
  2013-02-15), and FY11 without the extra week would have made 3 CHEAP dates RICH (2012-08-10, 2012-08-31 and 2012-09-07). Those
  dates returned +27% to +41% against the 32.2% hurdle and SPY's +42% to +47%, so each alternative trades holds for misses at the
  margin: facts about seven dates, not reasons to change an encoding. The calls were decided before scoring and stay; changing a
  rule means a new method version tested elsewhere.

## 2014-2016 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 2 | +34% | +33% to +34% | 2 | 2 | +24% | 2 |
| class RICH | 154 | +22% | -0% to +34% | 5 | 73 | +11% | 80 |
| legacy tier BUY | 2 | +34% | +33% to +34% | 2 | 2 | +24% | 2 |
| legacy tier ACCUMULATE | 6 | +30% | +28% to +32% | 1 | 6 | +19% | 0 |
| legacy tier WATCHLIST | 9 | +27% | +23% to +32% | 0 | 9 | +15% | 0 |
| legacy tier AVOID | 139 | +20% | -0% to +34% | 4 | 58 | +10% | 80 |
| FY12 anchor (to the Q4 2013 print) | 5 | +24% | +21% to +30% | 0 | 5 | +19% | 0 |
| FY13 anchor, Q4 2013 print | 9 | +31% | +28% to +34% | 3 | 9 | +19% | 2 |
| Q1 2014 print | 14 | +27% | +21% to +28% | 0 | 14 | +13% | 0 |
| Q2 2014 print | 11 | +24% | +19% to +30% | 0 | 11 | +10% | 0 |
| Q3 2014 print | 18 | +16% | +8% to +23% | 0 | 8 | +7% | 10 |
| FY14 anchor, Q4 2014 print | 10 | +22% | +12% to +24% | 0 | 7 | +10% | 3 |
| Q1 2015 print | 11 | +28% | +22% to +33% | 1 | 11 | +12% | 0 |
| Q2 2015 print | 13 | +27% | +22% to +34% | 2 | 10 | +14% | 3 |
| Q3 2015 print | 18 | +24% | +13% to +33% | 1 | 0 | +13% | 17 |
| FY15 anchor, Q4 2015 print | 10 | +16% | +10% to +20% | 0 | 0 | +14% | 10 |
| Q1 2016 print | 11 | +5% | -0% to +12% | 0 | 0 | +10% | 11 |
| Q2 2016 print | 12 | +12% | +7% to +15% | 0 | 0 | +3% | 12 |
| Q3 2016 print | 14 | +12% | +5% to +27% | 0 | 0 | +6% | 14 |
| 2014 | 51 | +24% | +8% to +34% | 3 | 46 | +12% | 7 |
| 2015 | 53 | +23% | +10% to +34% | 3 | 29 | +11% | 24 |
| 2016 | 52 | +12% | -0% to +33% | 1 | 0 | +9% | 51 |

- **RICH on 154 dates; the call held on 80, and which ones held followed the market, not PEP.** RICH expects the stock to miss the
  hurdle and lag SPY. PEP missed the hurdle on 149 of the 154 (two-year returns -0.5% to +34%, median +22%), so the call turned on
  SPY. It failed on all 42 RICH dates to 2014-11-07, whose two-year windows ended in 2016, when SPY returned +6% to +18% and PEP
  +16% to +32%; held on 13 of the 16 from 2014-11-14 to 2015-02-27 (PEP +8% to +17%, SPY +10% to +19%); failed on all 28 from
  2015-03-06 to 2015-09-11 (PEP +20% to +34%, SPY +16% to +33%); and held on 20 of the 21 from 2015-09-18 to 2016-02-05 and on all
  47 from 2016-02-12, as SPY returned +11% to +53% (median +34%) and PEP -0.5% to +33%. 2016-01-22 failed by clearing the hurdle
  (+33.2%) while lagging SPY by 20pp.
- **RICH marked a lower return, not a loss.** The RICH dates' largest drawdown within two years was -9.9% to -21.0% (median
  -10.7%); their one-year returns had a median of +10.8%, their three-year returns ran from +7.8% to +48% (median +31%), ahead of
  SPY on 35 of 154. The two CHEAP dates, 2014-02-14 and 2014-02-21 ($78.09 and $78.22, the weeks after FY13's EPS came in), returned
  +33% and +34%, cleared the hurdle and beat SPY (+6% and +9%): both held, and returned +48% and +50% over three years.
- **The floor distance and the entry price ranked the outcomes again, step by step.** Across the 156 dates the EPP gap ranks the
  two-year returns at Spearman -0.73, the entry price at -0.76, Ratio B at -0.72, the adjusted gap at +0.08 and the proxy composite
  at -0.06. Within 2014 the EPP gap reads -0.87, within 2015 -0.45, within 2016 -0.51. By distance above the floor: 0-20% (7 dates)
  returned a median +31.0%, 20-30% (19) +26.6%, 30-40% (39) +23.7%, 40-50% (43) +22.3% and more than 50% (48: every date from
  2016-02-12, when FY15's GAAP EPS put the floor at $58.72, and 2015-12-31) +11.3%, none of those 48 clearing the hurdle or beating
  SPY. The worst entries were in May 2016 at 27-29x GAAP EPS: 2016-05-13 ($104.18) returned -0.5%, 2016-05-06 +0.2%.
- **The proxy composite ranked the right way within 2014 (+0.54) and 2015 (+0.59), the first years it did in PEP's batches** (2010's
  +0.10 and 2012's +0.06 ranked nothing), and the adjusted gap within them too (+0.76 and +0.62, as in 2009); within 2016 both read
  -0.19. But their best readings came with the lowest prices: the composite's 2.50 (February to April 2014) with +28% to +34%, its
  2.70 (Q4 2015: margins up, no servings) with +10% to +20%. Across the batch neither ranks anything. The earlier hypothesis
  stands untested elsewhere: trailing operating signals lag the price.
- **Two-year prices landed nearest XBULL on 85 dates and BULL on 71, never nearest BASE or BEAR.** The two-year prices
  ($93.93-121.94) were 1.09-1.67 times BASE and 0.94-1.43 times BULL. From the Q4 2015 print BASE ($72-74) and BULL ($82-85) started
  from FY15's GAAP $3.67, with the Venezuela charges, and grew it at +2.1% to +2.9%/yr with the deconsolidation in the growth: the
  two-year prices ($97-122) were 1.32-1.67 times BASE. No two-year path went below its BEAR price.
- **Across 2008-2016 (470 dates) CHEAP held on 141 of 266 and RICH on 110 of 204.** RICH's absolute half nearly always came true:
  PEP missed the 32.2% hurdle on 196 of the 204 RICH dates, but beat SPY on 90 of them, so RICH held only when the market outran
  PEP. CHEAP cleared the hurdle on 88 of 266 (RICH on 8 of 204) and beat SPY on 61, though the medians were close (+23.9% and
  +22.5%: CHEAP includes 2008's entries). Hypothesis, not a rule: for PEP the price state said more about the absolute two-year
  return than about the return against the market, which followed the market's own path. Test it on other tickers and years before
  any method change; never fit it to PEP's outcomes.
- **The encoding calls, seen afterwards.** The core figures in the history alone move no class here, and FY15 without the Venezuela
  charges moves nothing. With the core guides also read as points, the 7 RICH dates from 2014-02-28 to 2014-04-11 would have been
  CHEAP: they returned +28% to +32% against SPY's +9% to +17%, so as CHEAP they would have held (one, 2014-04-04 at +32.3%, also
  cleared the hurdle) where as RICH they failed. Facts about seven dates, not reasons to change an encoding: the calls were decided
  before scoring and stay; changing a rule means a new method version tested elsewhere.

## 2017-2020 (209 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 52 | +22% | +13% to +36% | 2 | 0 | +8% | 2 |
| class FAIR | 1 | +65% | +65% | 1 | 0 | +51% | 0 |
| class RICH | 156 | +28% | +6% to +47% | 50 | 83 | +18% | 57 |
| legacy tier BUY | 52 | +22% | +13% to +36% | 2 | 0 | +8% | 2 |
| legacy tier WATCHLIST | 1 | +65% | +65% | 1 | 0 | +51% | 0 |
| legacy tier AVOID | 156 | +28% | +6% to +47% | 50 | 83 | +18% | 57 |
| FY15 anchor (to the Q4 2016 print) | 6 | +13% | +12% to +13% | 0 | 0 | +6% | 6 |
| FY16 anchor, Q4 2016 print | 10 | +14% | +10% to +18% | 0 | 0 | -0% | 10 |
| Q1 2017 print | 11 | +20% | +14% to +21% | 0 | 0 | -0% | 11 |
| Q2 2017 print | 12 | +22% | +16% to +28% | 0 | 5 | +3% | 7 |
| Q3 2017 print | 19 | +24% | +20% to +37% | 2 | 11 | +9% | 8 |
| FY17 anchor, Q4 2017 print | 10 | +27% | +6% to +42% | 4 | 10 | +22% | 0 |
| Q1 2018 print | 11 | +38% | +27% to +47% | 7 | 11 | +31% | 0 |
| Q2 2018 print | 12 | +27% | +21% to +32% | 0 | 12 | +19% | 0 |
| Q3 2018 print | 19 | +33% | +24% to +42% | 11 | 4 | +22% | 7 |
| FY18 anchor, Q4 2018 print | 9 | +22% | +18% to +25% | 0 | 0 | +16% | 0 |
| Q1 2019 print | 12 | +20% | +15% to +22% | 0 | 0 | +7% | 0 |
| Q2 2019 print | 12 | +26% | +17% to +28% | 0 | 0 | +8% | 0 |
| Q3 2019 print | 19 | +27% | +13% to +36% | 2 | 0 | +8% | 2 |
| FY19 anchor, Q4 2019 print | 11 | +31% | +19% to +65% | 5 | 0 | +19% | 6 |
| Q1 2020 print | 11 | +34% | +26% to +37% | 8 | 5 | +23% | 2 |
| Q2 2020 print | 11 | +33% | +29% to +38% | 8 | 11 | +21% | 0 |
| Q3 2020 print | 14 | +32% | +23% to +43% | 6 | 14 | +19% | 0 |
| 2017 | 52 | +20% | +10% to +34% | 1 | 12 | +3% | 40 |
| 2018 | 52 | +30% | +6% to +47% | 19 | 41 | +21% | 7 |
| 2019 | 52 | +22% | +13% to +39% | 4 | 0 | +8% | 2 |
| 2020 | 53 | +32% | +19% to +65% | 29 | 30 | +20% | 10 |

- **CHEAP on 52 dates; the call held on 2, and the cheapness was FY2018's tax benefits.** Every CHEAP date (2019-02-15 to
  2020-02-07) is anchored on FY18's GAAP $8.78, which carries $5.1 billion of non-cash tax benefits (13.1-16.6x it). PEP returned
  +12.9% to +35.6% over two years (median +22.2%) while SPY returned +37.3% to +61.0% (median +49.6%): none beat SPY, and only
  2020-01-03 ($135.63, +33.6%) and 2020-01-10 ($134.53, +35.6%) cleared the hurdle. Every two-year price landed nearest BASE, at 0.75-0.98
  times a BASE price ($175-180) built on $8.78. One-year returns had a median of +6.7%; three-year returns ran from +26.8% to +54.5%
  (median +41.7%), ahead of SPY on 23 of 52; every window held the 2020-03-20 close ($103.93), a 29.3% drawdown from the February
  peak.
- **RICH on 156 dates; the call held on 57, and which ones held followed SPY again.** PEP missed the hurdle on 106 of the 156
  (two-year returns +6.2% to +46.7%, median +28.2%) and beat SPY on 83, so the call turned on the market's path, as in 2014-2016. It
  held on all 34 from 2017-01-06 to 2017-08-25 (PEP +10% to +22%, SPY +15% to +29%); failed on the 11 from 2017-09-01 to 2017-11-10
  (PEP +24% to +34% against SPY +20% to +25%); held on 8 of the 9 to 2018-01-12; failed on all 40 from 2018-01-19 to 2018-10-19,
  whose two-year windows ended in 2020, through the crash (SPY -9.3% to +31.8%, PEP +6.2% to +46.7%); held on 7 of the 16 to
  2019-02-08 (the 8 from 2018-12-07 to 2019-01-25 failed by clearing the hurdle while lagging SPY); and held on 8 of the 46 in 2020,
  failing on all 30 from 2020-06-12, whose windows ended in 2022 (PEP +23% to +43%, SPY +5.5% to +33.9%). RICH marked neither a loss
  nor a lag: its median two-year return (+28.2%) was above CHEAP's (+22.2%); its largest drawdowns within two years were -13.1% to
  -29.3% (median -21.0%); one-year returns had a median of +15.0%, three-year returns +11.1% to +72.1% (median +40.8%), ahead of SPY on
  36 of 156.
- **Nothing ranked the outcomes across the batch, and the floor broke with its anchor.** Across the 209 dates the EPP gap ranks the
  two-year returns at Spearman +0.11 (+0.21 on the m12-24 average), the entry price at +0.03, Ratio B at +0.07, the adjusted gap at
  -0.11 and the proxy composite at -0.01, where each earlier batch had the gap and the entry price at -0.43 to -0.92. Within years the entry
  price still ranks 2018 (-0.62) and 2020 (-0.54). The floor moved with the GAAP anchor, from $54.08 (16x FY17's $3.38, after the Tax
  Act charge) to $131.70 (15x FY18's $8.78, with the tax benefits) within a year: the 22 dates below it (2019-02-15 to 2019-08-23)
  returned a median +21.8%, none clearing the hurdle or beating SPY, the reverse of 2008-2016, when nearness to the floor marked the
  best entries; the 121 dates more than 50% above it (mostly 2017-2018, on FY16's and FY17's GAAP EPS) returned +25.9%.
- **The COVID low was the best entry, and FAIR.** 2020-03-20 ($103.93, 20.0x FY19's $5.20, the 51st percentile) returned +64.7% and
  cleared the hurdle, but lagged SPY's +99.3% by 34.5pp, so FAIR (within 15pp of SPY) failed. The RICH dates either side: 2020-03-13
  ($127.45, +27.2%) held; 2020-03-27 ($120.46, +44.1%) failed by clearing the hurdle.
- **Two-year prices landed nearest XBULL on 100 dates, BULL on 57 and BASE on 52 (the CHEAP dates), never nearest BEAR.** RICH's
  two-year prices were 0.99-1.79 times BULL and 1.18-2.26 times BASE, mostly built on GAAP anchors that one-offs had lowered (FY15's
  Venezuela charges to 2017-02-10, FY17's Tax Act charge through 2018). No two-year path went below its BEAR price.
- **Across 2008-2020 (679 dates) CHEAP held on 143 of 318, RICH on 167 of 360 and FAIR on 0 of 1.** CHEAP cleared the hurdle on 90 and
  beat SPY on 61; RICH cleared it on 58 and beat SPY on 173; the median two-year returns are +23.4% and +24.1%. In 2017-2020 the price
  state no longer said even the absolute part: CHEAP's median (+22%) trailed RICH's (+28%), because CHEAP was the tax benefit.
- **The encoding calls, seen afterwards.** The core figures in the history, or FY18 without its stated tax benefits, turn the 52
  CHEAP dates RICH: as RICH they would have held on 50 (failing only on 2020-01-03 and 2020-01-10, which cleared the hurdle), against 2
  as CHEAP. With the core guides also read as points, 2018-05-11 and 2018-05-18 would have been CHEAP and held (+45.7%, +46.7%),
  2018-05-04, 2018-05-25 and 2018-06-01 FAIR and failed (PEP beat SPY by 23-29pp), 2020-03-20 CHEAP and held, and 2020-03-27 FAIR and
  failed. FY17 without the Tax Act charge, or organic growth, makes 2020-03-20 RICH, which fails too. Facts about these dates, not
  reasons to change an encoding: the 2008 core rule and the distorted-year test were frozen before PEP was built and applied before
  scoring, and they stay; changing a rule means a new method version, tested elsewhere first.
- **Hypothesis for the method, not a rule:** a year's GAAP EPS moved by large one-off tax items (FY17's charge, FY18's benefits, 42%
  of that year's net income) set the P/E anchor, the floor and every scenario more than the market did, and the distorted-year test
  only removes one-offs larger than the year's income without them. Whether a lower bound, or a company-adjusted figure where its only
  other exclusion is a recurring timing item (PEP's commodity mark-to-market), predicts better is a question for other tickers and
  years, with the change made as a new method version; never fit it to PEP's outcomes.

## 2021-2023 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR | 1 | -6% | -6% | 0 | 0 | -8% | 0 |
| class RICH | 155 | +5% | -28% to +43% | 16 | 51 | +1% | 103 |
| legacy tier WATCHLIST | 1 | -6% | -6% | 0 | 0 | -8% | 0 |
| legacy tier AVOID | 155 | +5% | -28% to +43% | 16 | 51 | +1% | 103 |
| FY19 anchor (to the Q4 2020 print) | 5 | +30% | +26% to +32% | 0 | 5 | +22% | 0 |
| FY20 anchor, Q4 2020 print | 9 | +37% | +32% to +43% | 8 | 9 | +29% | 0 |
| Q1 2021 print | 13 | +33% | +29% to +40% | 8 | 13 | +20% | 0 |
| Q2 2021 print | 12 | +23% | +18% to +28% | 0 | 12 | +16% | 0 |
| Q3 2021 print | 18 | +5% | +1% to +11% | 0 | 12 | +8% | 5 |
| FY21 anchor, Q4 2021 print | 11 | +6% | +3% to +13% | 0 | 0 | +5% | 11 |
| Q1 2022 print | 11 | +9% | +0% to +17% | 0 | 0 | +2% | 11 |
| Q2 2022 print | 13 | +6% | +2% to +12% | 0 | 0 | -0% | 13 |
| Q3 2022 print | 17 | -7% | -14% to +7% | 0 | 0 | -6% | 17 |
| FY22 anchor, Q4 2022 print | 11 | -12% | -18% to -3% | 0 | 0 | -6% | 11 |
| Q1 2023 print | 11 | -24% | -28% to -21% | 0 | 0 | -16% | 11 |
| Q2 2023 print | 13 | -14% | -22% to -6% | 0 | 0 | -16% | 12 |
| Q3 2023 print | 12 | -6% | -9% to +3% | 0 | 0 | -13% | 12 |
| 2021 | 52 | +29% | +3% to +43% | 16 | 51 | +19% | 0 |
| 2022 | 52 | +5% | -11% to +17% | 0 | 0 | +1% | 52 |
| 2023 | 52 | -12% | -28% to +3% | 0 | 0 | -14% | 51 |

- **RICH on 155 dates; the call held on 103, and the year decided which.** None of the 52 RICH dates of 2021 held: PEP returned
  +3.2% to +43.0% over two years (median +28.6%) while SPY returned -7.8% to +12.9% (median +3.3%) over windows that ran through the
  market's 2022 fall, so PEP beat SPY on 51 (2021-12-17 tied at +4.9%) and cleared the hurdle on 16 (2021-02-12 to 2021-06-25). All 52
  of 2022 and all 51 RICH dates of 2023 held: PEP returned -11.4% to +17.1% (median +5.4%) and -27.5% to +2.8% (median -12.2%) while SPY
  returned +3.2% to +64.4% and +26.9% to +70.3%. As in 2014-2020, the call turned on the market's path: RICH's relative half failed
  whenever the market fell, while its absolute half (missing the hurdle) held on 139 of 155.
- **The FAIR date lost money.** 2023-10-06 ($160.29, 25.0x FY22's $6.42, the 39th percentile; the last date before the Q3 2023 print)
  returned -6.1% against SPY's +59.7%: 65.8pp outside FAIR's ±15pp band. The RICH dates either side, 2023-09-29 (-10.9%) and 2023-10-11
  (-1.1%), held.
- **The entry price ranked the outcomes; the signals did not.** Across the 156 dates the entry price ranks the two-year returns at
  Spearman -0.90 (-0.87 on the m12-24 average) and within each year at -0.81 to -0.92. The EPP gap ranks them at -0.66 to -0.89 within
  years but +0.12 across the batch, because the floor rose with the anchor (20x FY21's $5.49 = $110, then 21x FY22's $6.42 = $135 from
  2023-02-10) while the price fell. Ratio B ranks them at +0.27, the adjusted gap at -0.29 and the proxy composite at -0.24. One stock over
  three years mostly tests "buy lower" again.
- **2023's dates were the worst, on the highest anchor.** From 2023-02-10 every date was anchored on FY22's $6.42 (GAAP, with the Juice
  Transaction gain of $2.08 a share and the impairment and other charges of $2.12 nearly offsetting), at 24.9-30.5x. Their two-year returns ran from -27.5%
  (2023-05-12) to +2.8% (median -12.2%), with drawdowns of 25.4% to 33.5% within two years (median 30.1%); the 27 windows from 2023-06-30
  held the 2025-06-25 close ($128.02). One-year returns had a median of -1.7%; three-year returns (to 2023-10-27, 43 dates) ran from
  -20.4% to +5.7%, behind SPY on all 43.
- **Two-year prices landed nearest BULL on 59 dates and BASE on 97, never nearest BEAR or XBULL.** BULL was BASE on every date (+8.8% to
  +19.0%/yr); the 2021 dates landed nearest it (45 of 52), the 2023 dates nearest BASE (all 52) but far below it (BASE prices of
  $180-219, at +10.0% to +15.2%/yr). BEAR (-40.8%/yr from FY2018's tax benefits: $27-41) was never approached: the lowest close inside any
  window was $128.02.
- **Across 2008-2023 (835 dates) CHEAP held on 143 of 318, RICH on 270 of 515 and FAIR on 0 of 2.** CHEAP cleared the hurdle on 90 and
  beat SPY on 61 (median two-year return +23.4%); RICH cleared it on 74 and beat SPY on 224 (median +21.8%). No 2021-2023 date was CHEAP.
- **The encoding calls, seen afterwards.** The core figures with the core guides read as points would have turned 15 RICH dates of
  August-December 2023 CHEAP or FAIR and 2023-10-06 CHEAP: all 16 would have failed (PEP -15.8% to +2.8% over two years against SPY's
  +46.1% to +70.3%), where 15 held as RICH. Their 69 tier upgrades (AVOID to WATCHLIST, ACCUMULATE or BUY from 2021-07-14) fell on dates
  with a median two-year return of -6.7%, none clearing the hurdle and 11 beating SPY. The core figures alone make 2023-09-29 FAIR (which
  fails; it held as RICH) and, for every year of the window, 2023-10-06 CHEAP (which fails, as FAIR did) with 31 tier upgrades on dates
  that returned a median -7.7%; the organic revenue guides read as revenue guides make 2023-10-06 RICH, which would have held. Facts about
  these dates, not reasons to change an encoding: the 2008 core rule was frozen before PEP was built and applied before scoring, and it
  stays.
- **GLP-1, seen afterwards.** GLP1 stayed off the watch list in August-December 2023 because no PepsiCo filing named it. The outcomes
  cannot say what the 2023 losses reflected: re-filing a date under the theme changes its class label only, and the 2023 RICH calls held
  either way.
- **Hypothesis for the method, not a rule:** the servings slot was empty for all three years and scored BASE (the AAPL Mac-unit rule),
  while the releases' own unit volume, which no rule reads, turned negative: convenient foods -1.5%, -2%, -3%, -3% and -1.5% from Q3
  2022 to Q3 2023, beverages 3%, flat, +1%, -1% and flat. Whether a company's segment unit volumes should stand in for a headline volume
  measure it stops reporting is a question for other tickers and years, with the change made as a new method version; never fit it to
  PEP's outcomes.
