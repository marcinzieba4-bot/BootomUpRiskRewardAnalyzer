# PEP retrospective findings (hindsight)

Patterns seen in `outcome.json` for the PEP weekly dates: 53 from 2008-01-04 to 2008-12-31, 104 from 2009-01-09 to 2010-12-31, 157
from 2011-01-07 to 2013-12-31 and 156 from 2014-01-10 to 2016-12-30. They are **labels and hypotheses**: never feed them back into
the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and pushed (2008: 4b429b6;
2009-2010: 88ba341, documented in 55a6818; 2011-2013: 29c50f2, documented in b02f4d4; 2014-2016: bc27375, documented in 03bc69c).
Prices run to 2026-10-30; the 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30), the 2009-2010 batch's by
2012-12-28 (2013-12-30), the 2011-2013 batch's by 2015-12-30 (2016-12-30), the 2014-2016 batch's by 2018-12-28 (2019-12-30). Medians
of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

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
