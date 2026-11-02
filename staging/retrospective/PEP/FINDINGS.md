# PEP retrospective findings (hindsight)

Patterns seen in `outcome.json` for the PEP weekly dates: 53 from 2008-01-04 to 2008-12-31. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: 4b429b6). Prices run to 2026-10-30; the 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30).
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

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
