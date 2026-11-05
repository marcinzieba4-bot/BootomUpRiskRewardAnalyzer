# XOM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the XOM weekly dates: 53 from 2008-01-04 to 2008-12-31. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and
pushed (2008: ae6e2c7). Prices run to 2026-11-04; the 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30).
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
