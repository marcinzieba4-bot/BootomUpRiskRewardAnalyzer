# V retrospective findings (hindsight)

Patterns seen in `outcome.json` for the V weekly dates (Visa Inc., class A common stock, NYSE: V): 219 in all, 10 from 2009-10-29 to
2009-12-31 and 209 from 2010-01-08 to 2013-12-31 (the later section below), as traded before the 2015 split. The 2009 dates are the only ones of 2008-2009 that method r2 can build (retro/README.md, "V": FY2008, Visa's first year with EPS, is a distorted year with
no figure excluding only one-offs, so no year is in the history until the Q4 FY09 print). They are **labels and hypotheses**: never feed
them back into the method or the fact sheet. The 2009 outcomes were computed on 2026-11-19, after the point-in-time build was committed
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

## 2010-2013 (209 dates)

Scored on 2026-11-20, after the point-in-time build was committed (b2099e9) and the firewall had passed at 25 cutoffs (705876c); the build
was not yet pushed when the outcomes were computed. Every date has its 6-month, 1-, 2- and 3-year horizons. Dividends are $0.125 a quarter
to October 2010, then $0.15, $0.22 (2011), $0.33 (2012) and $0.40 (from late 2013).

| Group | Dates | Mean 2-yr total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all | 209 | +80.3% | +75.0% | +46.5pp | 207 | 199 | +54.2% | -15.9% | 44 |
| 2010 | 52 | +63.9% | +66.6% | +38.1pp | 50 | 42 | +33.1% | -22.1% | 15 |
| 2010, CHEAP | 13 | +96.2% | +91.2% | +72.9pp | 13 | 13 | +61.7% | -16.1% | 13 |
| 2010, FAIR | 12 | +79.2% | +80.1% | +47.9pp | 12 | 12 | +47.4% | -17.6% | 0 |
| 2010, RICH | 27 | +41.5% | +35.2% | +17.0pp | 25 | 17 | +13.0% | -27.0% | 2 |
| 2011 | 52 | +120.4% | +117.9% | +85.6pp | 52 | 52 | +83.9% | -11.5% | 29 |
| 2011, CHEAP | 29 | +124.6% | +124.8% | +97.3pp | 29 | 29 | +85.4% | -11.9% | 29 |
| 2011, FAIR | 21 | +115.4% | +115.7% | +71.3pp | 21 | 21 | +82.2% | -10.9% | 0 |
| 2011, RICH | 2 | +112.4% | +112.4% | +67.2pp | 2 | 2 | +80.0% | -11.0% | 0 |
| 2012 | 52 | +79.1% | +76.1% | +34.5pp | 52 | 52 | +62.3% | -14.4% | 0 |
| 2012, FAIR | 5 | +116.7% | +119.7% | +70.0pp | 5 | 5 | +81.3% | -11.9% | 0 |
| 2012, RICH | 47 | +75.1% | +75.0% | +30.7pp | 47 | 47 | +60.3% | -14.6% | 0 |
| 2013 | 53 | +58.3% | +57.6% | +28.3pp | 53 | 53 | +38.0% | -15.6% | 0 |
| 2013, FAIR | 5 | +65.7% | +67.0% | +39.9pp | 5 | 5 | +46.3% | -15.6% | 0 |
| 2013, RICH | 48 | +57.6% | +56.5% | +27.1pp | 48 | 48 | +37.1% | -15.6% | 0 |
| all CHEAP | 42 | +115.8% | +118.9% | +89.7pp | 42 | 42 | +78.1% | -13.2% | 42 |
| all FAIR | 43 | +99.7% | +109.9% | +61.0pp | 43 | 43 | +68.2% | -13.4% | 0 |
| all RICH | 124 | +61.6% | +61.6% | +26.9pp | 122 | 114 | +41.3% | -17.6% | 2 |
| tier BUY | 85 | +109.3% | +114.4% | +75.7pp | 85 | 85 | +74.6% | -13.2% | 42 |
| tier ACCUMULATE | 54 | +72.0% | +73.6% | +33.2pp | 54 | 54 | +51.2% | -15.2% | 0 |
| tier WATCHLIST | 47 | +60.0% | +60.6% | +26.1pp | 47 | 47 | +43.0% | -15.8% | 0 |
| tier AVOID | 23 | +34.4% | +34.0% | +11.7pp | 21 | 13 | +8.9% | -27.7% | 2 |

What the labels say, as hypotheses only:

- **The classes and tiers ordered the outcomes; the absolute calls missed a compounder.** CHEAP dates returned a mean +115.8% over two
  years, FAIR +99.7%, RICH +61.6%; BUY +109.3%, ACCUMULATE +72.0%, WATCHLIST +60.0%, AVOID +34.4%. The order held within 2010 and within
  2011 as well. But the stock beat SPY from 207 of the 209 dates and cleared the 15%/yr hurdle from 199, so RICH (which should miss the
  hurdle and lag) held on 2 of 124 dates and FAIR (within 15 points of SPY) on none; CHEAP held on all 42. "Call held" reads 44 of 209.
- **The RICH years are 2012 and 2013, and both rest on the rules' anchors.** In 2012 the EPS and revenue outlooks were words, so FY11's
  $4.99 stood all year (the rollover rule) while the price rose from $100 to $151; FY2012 then came in at the company's $6.20 (+24%). In 2013
  the anchor was $6.20, then $7.44 from the Q2 FY13 guide, against a P/E window that starts in the 2008-2009 crisis (median 18-19x). Against
  that window and those anchors the price sat at the 71st-100th percentile; the RICH dates of 2012 and 2013 then returned a mean +75.1% and
  +57.6% over two years. A hypothesis for the live
  model: a short window anchored in a crisis, plus last-year EPS when the guide is in words, reads a steady compounder as expensive.
- **Scenario landing:** the price two years on sat in the XBULL band on 208 dates and the BULL band on 1: even the best two-year EPS run of
  the history (+26.9%/yr) at the window's 90th-percentile multiple fell short of the price reached.
- **Drawdowns were mild:** a mean maximum of -15.9% inside the two years (-9.2% to -32.2%), the deepest from the 2010 entries.
- **Three-year horizon:** a mean +128.3% (+77.4 points over SPY); CHEAP +186.8%, FAIR +147.8%, RICH +101.6%: the same order, larger.
- **The excluded year matters here too, in the direction of the outcome.** With FY2008 in the history the sensitivity moves 78 classes (37
  RICH to FAIR, 13 RICH to CHEAP, 28 FAIR to CHEAP) and 104 tiers toward BUY (retro/README.md, "V 2010-2013"), the direction these outcomes
  favour: CHEAP held on every date of these years. It is a rule choice made before the outcomes were computed, and it stays: never fold
  this back.

Not tested here: whether any of this holds for other payments networks or other periods. One stock through one bull market mostly tests
"buy lower" (retro/README.md, "Scoring a single stock"), and the class order is its only cross-sectional evidence.

