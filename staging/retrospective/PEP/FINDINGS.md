# PEP retrospective findings (hindsight)

Patterns seen in `outcome.json` for the PEP weekly dates: 53 from 2008-01-04 to 2008-12-31 and 104 from 2009-01-09 to 2010-12-31.
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed and pushed (2008: 4b429b6; 2009-2010: 88ba341, documented in 55a6818). Prices run to 2026-10-30;
the 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30), the 2009-2010 batch's by 2012-12-28 (three-year:
2013-12-30). Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two
years.

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
