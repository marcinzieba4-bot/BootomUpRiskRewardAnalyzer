# JPM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 105 JPM weekly dates from 2008-01-04 to 2009-12-31 (JPMorgan Chase & Co., NYSE: JPM). They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. The outcomes were computed on 2026-11-19, after the
point-in-time build and its one text correction were committed (735d7d4, ed681b3) and the firewall had passed at 16 cutoffs; the build
was not yet pushed when they were computed. Every date has its 6-month, 1-, 2- and 3-year horizons. Total returns include dividends
($0.38 a quarter to February 2009, $0.05 after). Medians of an even count are the mean of the two middle values. The 15%/yr hurdle is
+32.2% over two years. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY); FAIR should land
within 15 points of the benchmark; RICH should miss the hurdle and lag the benchmark.

| Group | Dates | Mean 2-yr total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all | 105 | +14.6% | +4.0% | -6.4pp | 50 | 22 | +12.8% | -49.0% | 75 |
| 2008 | 53 | +6.2% | +1.4% | +4.7pp | 38 | 5 | +3.1% | -65.2% | 39 |
| 2008, CHEAP | 25 | +16.7% | +13.4% | +6.0pp | 16 | 5 | +16.4% | -62.7% | 20 |
| 2008, FAIR | 18 | +0.1% | -0.4% | +12.8pp | 18 | 0 | -8.6% | -68.1% | 13 |
| 2008, RICH | 10 | -9.3% | -9.6% | -13.2pp | 4 | 0 | -9.1% | -66.1% | 6 |
| 2009 | 52 | +23.1% | +16.8% | -17.7pp | 12 | 17 | +22.7% | -32.4% | 36 |
| 2009, CHEAP (2009-01-09) | 1 | +69.6% | +69.6% | +21.9pp | 1 | 1 | +55.4% | -42.5% | 1 |
| 2009, RICH | 51 | +22.2% | +16.4% | -18.5pp | 11 | 16 | +22.0% | -32.2% | 35 |
| tier BUY | 17 | +26.7% | +20.8% | +4.4pp | 9 | 6 | +25.6% | -59.2% | 13 |
| tier ACCUMULATE | 29 | -2.1% | -2.1% | +0.1pp | 21 | 0 | -2.3% | -63.4% | 25 |
| tier WATCHLIST | 20 | -12.3% | -13.3% | -13.5pp | 9 | 0 | -10.8% | -56.9% | 14 |
| tier AVOID | 39 | +35.4% | +25.3% | -12.3pp | 11 | 16 | +30.5% | -29.7% | 23 |

What the labels say, as hypotheses only:

- **2008: the class ordered the outcomes.** CHEAP dates returned a mean +16.7% over two years, FAIR +0.1%, RICH -9.3%; against SPY,
  +6.0, +12.8 and -13.2 points. Every 2008 date still had a drawdown of 50% to 68% inside its two years: the classes ranked entries, they
  did not avoid the fall. One stock over one year mostly tests "buy lower" (retro/README.md, "Scoring a single stock").
- **2009: the RICH call missed the recovery in absolute terms and held against the index.** All 51 dates from the Q4 2008 print are
  RICH, because the price is measured against FY08's $0.92. They returned a mean +22.2% over two years, 16 cleared the hurdle, and the 39
  AVOID dates returned +35.4%; the series low, 2009-03-06 at $15.93, is RICH and AVOID and returned +188% (+90 points against SPY). Yet
  40 of the 51 lagged SPY over two years, which is why "call held" reads 35 of 51: by the scoring rule a RICH call holds when the stock
  lags the benchmark or misses the hurdle.
- **The 2009 miss is the trough-year anchor.** With no EPS guide the last full year stands, so a year whose earnings fell 79% makes the
  multiple look high at the bottom of the price. A hypothesis
  for the live model: a P/E rule on last-year EPS reads a bank's credit trough as expensive.
- **Scenario landing:** the price two years on sat in the BASE band on 69 dates and the BULL band on 36, and never near BEAR, whose
  price was $8-9 in 2008 and $0.41 in 2009.
- **Three-year horizon:** a mean +13.1% for the 105 dates, 20.8 points behind SPY: over three years the stock lagged the index from
  most entries of both years.

Not tested here: whether any of this holds for other banks or other periods. One bank through one crisis is one observation.
