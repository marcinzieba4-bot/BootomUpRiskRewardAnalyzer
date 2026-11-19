# V retrospective findings (hindsight)

Patterns seen in `outcome.json` for the V weekly dates (Visa Inc., class A common stock, NYSE: V): 10 in all, 2009-10-29 to 2009-12-31,
the only dates of 2008-2009 that method r2 can build (retro/README.md, "V": FY2008, Visa's first year with EPS, is a distorted year with
no figure excluding only one-offs, so no year is in the history until the Q4 FY09 print). They are **labels and hypotheses**: never feed
them back into the method or the fact sheet. The outcomes were computed on 2026-11-19, after the point-in-time build was committed
(6548d21) and the firewall had passed at 4 cutoffs (08b9b3b); the build was not yet pushed when they were computed. Every date has its
6-month, 1-, 2- and 3-year horizons. Total returns include dividends ($0.125 a quarter, then higher). Prices are as traded (before the
2015 four-for-one split). Medians of an even count are the mean of the two middle values. The 15%/yr hurdle is +32.2% over two years.
"Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY); FAIR should land within 15 points of the
benchmark; RICH should miss the hurdle and lag the benchmark.

## 2009 (10 dates, from the Q4 FY09 print)

| Group | Dates | Mean 2-yr total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all (RICH, tier AVOID) | 10 | +18.2% | +18.9% | +0.7pp | 6 | 0 | -1.4% | -32.2% | 4 |

What the labels say, as hypotheses only:

- **The RICH call was right about the hurdle and wrong about the index, narrowly.** No date cleared the hurdle (+10.9% to +24.5% over two
  years against +32.2%), and the price averaged over months 12-24 was -8.1% to +2.8% from the entry. But 6 of the 10 dates beat SPY,
  by 0.4 to 5.9 points (the other four lagged by 0.5 to 3.9), so by the scoring rule the call held on 4. Two years on, the stock had
  roughly kept pace with the index from a price the model called priced for perfection.
- **Every date shared one drawdown.** The 2-year low was $65.48 on 2010-09-13 for all ten entries ($77.28-88.97), a maximum drawdown of
  32.2% inside the two years, and the 1-year returns were +1.8% to -24.2%: the stock fell first and recovered later.
- **Scenario landing:** the price two years on ($89.02-102.48) sat in the XBULL band on 8 dates and the BULL band on 2. That says more
  about the scenarios than about the stock: with FY2009 alone, the bounds rule sets BULL and XBULL at BASE's 13%/yr, so the bull case was
  close to the guide, and a 2-year return of +11% to +25% still reached it.
- **Three-year horizon:** +71.9% to +86.6% (+33.7 to +52.6 points over SPY): over three years the RICH reading was clearly wrong.
- **The excluded year decides the reading, and the outcome does not settle it at two years.** With FY2008 in the history (the company's
  $2.25, the window from the listing; retro/README.md, "V", the sensitivity), the same dates read CHEAP on 7 and FAIR on 3, tier BUY on
  all 10; by the same scoring that reading holds on 7 of 10 (4 of the 7 CHEAP dates beat SPY; the 3 FAIR dates were within 4 points).
  Neither reading separates at two years; at three years the CHEAP reading would look right. A hypothesis for the live model, not a rule
  for this archive: a one-year history and a 13-month window that starts in the 2008 crisis make a stock look expensive against its own
  trough multiples, and the bounds rule then caps the bull case at the guide.

Not tested here: whether any of this holds for other payments networks or other periods, or for the 84 weeks of 2008-2009 the method
cannot build. Ten weekly dates of one stock over nine weeks are one observation.
