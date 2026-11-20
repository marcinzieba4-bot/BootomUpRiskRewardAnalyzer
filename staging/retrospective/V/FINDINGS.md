# V retrospective findings (hindsight)

Patterns seen in `outcome.json` for the V weekly dates (Visa Inc., class A common stock, NYSE: V): 427 in all, 10 from 2009-10-29 to
2009-12-31, 209 from 2010-01-08 to 2013-12-31 and 208 from 2014-01-10 to 2017-12-29 (the later sections below), each priced as traded on
its date (before 2015-03-19 on the basis before the four-for-one split). The 2009 dates are the only ones of 2008-2009 that method r2 can build (retro/README.md, "V": FY2008, Visa's first year with EPS, is a distorted year with
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

## 2014-2017 (208 dates)

Scored on 2026-11-20, after the point-in-time build was committed and pushed (7a6f58d) and the firewall had passed at 26 cutoffs
(364ff91, also pushed). Every date has its 6-month, 1-, 2- and 3-year horizons (the last 3-year horizon ends in December 2020). Dividends
are $0.40 a quarter to October 2014, then $0.48 ($0.12 on the split basis), $0.14, $0.165 and $0.195, and higher after. Every date is RICH,
so the table splits by year and legacy tier.

| Group | Dates | Mean 2-yr total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all (RICH) | 208 | +56.8% | +58.9% | +33.1pp | 208 | 186 | +39.3% | -15.3% | 0 |
| 2014 | 51 | +43.2% | +47.5% | +30.6pp | 51 | 37 | +35.7% | -15.7% | 0 |
| 2015 | 53 | +39.3% | +38.7% | +16.1pp | 53 | 45 | +21.4% | -15.7% | 0 |
| 2016 | 52 | +72.2% | +72.9% | +36.6pp | 52 | 52 | +48.9% | -10.7% | 0 |
| 2017 | 52 | +72.8% | +71.2% | +49.6pp | 52 | 52 | +51.5% | -19.3% | 0 |
| tier BUY | 7 | +58.3% | +57.8% | +42.7pp | 7 | 7 | +46.6% | -15.8% | 0 |
| tier ACCUMULATE | 8 | +57.6% | +54.4% | +42.1pp | 8 | 8 | +45.9% | -15.3% | 0 |
| tier WATCHLIST | 45 | +67.4% | +70.3% | +40.6pp | 45 | 44 | +49.2% | -14.7% | 0 |
| tier AVOID | 148 | +53.5% | +50.4% | +29.9pp | 148 | 127 | +35.6% | -15.5% | 0 |
| 2014, tier BUY | 7 | +58.3% | +57.8% | +42.7pp | 7 | 7 | +46.6% | -15.8% | 0 |
| 2014, tier ACCUMULATE | 7 | +53.1% | +54.2% | +39.6pp | 7 | 7 | +42.0% | -15.8% | 0 |
| 2014, tier WATCHLIST | 10 | +49.0% | +51.0% | +36.0pp | 10 | 9 | +39.9% | -15.8% | 0 |
| 2014, tier AVOID | 27 | +34.5% | +32.4% | +23.1pp | 27 | 14 | +29.7% | -15.5% | 0 |
| 2016, tier WATCHLIST | 22 | +71.2% | +71.4% | +35.7pp | 22 | 22 | +51.6% | -11.5% | 0 |
| 2016, tier AVOID | 29 | +72.4% | +76.2% | +36.4pp | 29 | 29 | +46.1% | -10.1% | 0 |
| 2017, tier WATCHLIST | 13 | +74.9% | +75.6% | +52.6pp | 13 | 13 | +52.3% | -19.3% | 0 |
| 2017, tier AVOID | 39 | +72.1% | +68.5% | +48.7pp | 39 | 39 | +51.2% | -19.3% | 0 |

(2015 is AVOID on all 53 dates; 2016 has one ACCUMULATE date, +89.2%.)

What the labels say, as hypotheses only:

- **The RICH call was wrong on every date.** The stock beat SPY over two years from all 208 dates (+4.8 to +62.4 points) and cleared the
  15%/yr hurdle from 186, so RICH (miss the hurdle and lag the benchmark) held on none. The 22 dates that missed the hurdle are entries
  near the 2014 and early-2015 highs (2014-01-17 to 2014-03-14 and 2014-11-14 to 2015-02-27), and even they beat SPY. At one year 22 dates
  lagged SPY (by up to 12.0 points: 2014-01-17 and dates from 2015-07-31 to 2016-04-15), the only horizon where the call ever looked
  right.
- **How far above the EPP floor the price stood ordered the outcomes, though every date was RICH.** Grouped by the EPP gap, the mean
  2-year excess return falls from +41.7 points (gap 50-75%, 37 dates) to +37.7 (75-90%, 74), +28.3 (90-105%, 82) and +16.0 (105-130%, 15);
  the correlation across the 208 dates is -0.5. 2015, the year furthest above the floor (87-128%) and highest in its own window
  (95th-100th percentile), returned the least (+39.3%, +16.1 points over SPY).
- **The tiers ordered 2014 and not the later years.** In 2014 BUY returned +58.3%, ACCUMULATE +53.1%, WATCHLIST +49.0% and AVOID +34.5%:
  the 14 ACCUMULATE and BUY dates are the ones the Q3 FY14 EPS guide (FY14E $8.96) moved up. In 2016 and 2017 WATCHLIST and AVOID returned
  much the same (+71.2% and +72.4%; +74.9% and +72.1%). Across all four years WATCHLIST did best, a mix of years rather than an order.
- **Scenario landing:** the price two years on sat in the XBULL band on 183 dates and the BULL band on 25 (all 2014-2015 entries): with
  BULL at the FY09-to-latest CAGR (+20.7-25.3%/yr) and XBULL at +26.9%/yr, the scenarios again fell short of the price reached.
- **Drawdowns were mild:** a mean maximum of -15.3% inside the two years (-9.9% to -19.3%); the 2017 entries all share the -19.3% of
  late 2018.
- **Three-year horizon:** a mean +97.4% (+58.2 points over SPY), +42.6% to +153.3%; by tier BUY +103.5%, ACCUMULATE +102.0%, WATCHLIST
  +107.4%, AVOID +93.9%.
- **The calls the sensitivities name point the same way as the outcomes, and stay as they are.** With the signals at their XBULL values,
  149 dates read CHEAP or FAIR (retro/README.md, "V 2014-2017"); with FY2008 in the history, 1 class and 41 tiers move toward buying. By
  2014 the excluded year no longer decides the class: the window that starts in the 2008-2009 crisis does (EPP floor 15-17x, against a
  stock at 23-34x). A hypothesis for the live model, as in 2010-2013: a window anchored in a crisis reads a steady compounder as
  expensive, and only the distance to the floor, not the class, carried information here. Never fold this back into the archive.

Not tested here: whether any of this holds for other payments networks or other periods. With every date RICH there is no
cross-sectional test of the class at all; the EPP-gap and 2014 tier orders are within one stock and one bull market.

