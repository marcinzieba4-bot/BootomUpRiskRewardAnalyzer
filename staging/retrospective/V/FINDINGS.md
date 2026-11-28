# V retrospective findings (hindsight)

Patterns seen in `outcome.json` for the V weekly dates (Visa Inc., class A common stock, NYSE: V): 890 in all, 10 from 2009-10-29 to
2009-12-31, 209 from 2010-01-08 to 2013-12-31, 208 from 2014-01-10 to 2017-12-29, 209 from 2018-01-05 to 2021-12-31 and 254 from
2022-01-07 to 2026-11-13 (the later sections below), each priced as traded on
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

## 2018-2021 (209 dates)

Scored on 2026-11-20, after the point-in-time build was committed and pushed (7c5ed2b) and the firewall had passed at 23 cutoffs
(5b69851, also pushed). Every date has its 6-month, 1-, 2- and 3-year horizons (the last 3-year horizon ends in December 2024). Dividends
are $0.195 a quarter to January 2018, then $0.21, $0.25, $0.30, $0.32 and $0.375, and higher after. The class is RICH on 199 dates and FAIR
on 10 (the dates after the Q4 FY21 print), so the table splits by class, year and legacy tier; there is no BUY date.

| Group | Dates | Mean 2-yr total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all | 209 | +24.9% | +22.9% | -2.0pp | 96 | 91 | +18.5% | -31.1% | 82 |
| class RICH | 199 | +25.0% | +23.7% | -3.2pp | 86 | 90 | +18.9% | -31.4% | 82 |
| class FAIR | 10 | +21.8% | +21.6% | +21.7pp | 10 | 1 | +10.4% | -24.5% | 0 |
| 2018 | 52 | +48.0% | +45.7% | +26.7pp | 52 | 50 | +37.8% | -33.0% | 0 |
| 2019 | 52 | +35.2% | +36.5% | -14.8pp | 9 | 37 | +26.0% | -36.4% | 15 |
| 2020 | 53 | +9.0% | +7.9% | -23.8pp | 0 | 3 | +12.5% | -27.7% | 50 |
| 2021 | 52 | +7.6% | +4.7% | +4.4pp | 35 | 1 | -2.2% | -27.2% | 17 |
| tier ACCUMULATE | 6 | +43.4% | +41.6% | +2.0pp | 4 | 4 | +33.9% | -26.4% | 0 |
| tier WATCHLIST | 21 | +38.2% | +41.8% | +5.2pp | 16 | 12 | +29.3% | -30.7% | 2 |
| tier AVOID | 182 | +22.7% | +17.2% | -2.9pp | 76 | 75 | +16.7% | -31.2% | 80 |
| 2018, tier ACCUMULATE | 1 | +70.0% | +70.0% | +12.5pp | 1 | 1 | +55.6% | -36.4% | 0 |
| 2018, tier WATCHLIST | 5 | +55.2% | +56.8% | +12.1pp | 5 | 5 | +42.5% | -36.4% | 0 |
| 2018, tier AVOID | 46 | +46.7% | +44.6% | +28.6pp | 46 | 44 | +36.9% | -32.5% | 0 |
| 2019, tier WATCHLIST | 6 | +51.1% | +48.1% | +3.2pp | 4 | 6 | +40.7% | -36.4% | 0 |
| 2019, tier AVOID | 46 | +33.1% | +35.9% | -17.1pp | 5 | 31 | +24.0% | -36.4% | 15 |
| 2020, tier ACCUMULATE | 2 | +50.9% | +50.9% | -42.2pp | 0 | 2 | +49.7% | -24.2% | 0 |
| 2020, tier WATCHLIST | 3 | +30.0% | +27.1% | -34.8pp | 0 | 1 | +34.5% | -24.2% | 2 |
| 2020, tier AVOID | 48 | +5.9% | +5.9% | -22.3pp | 0 | 0 | +9.5% | -28.0% | 48 |
| 2021, tier ACCUMULATE | 3 | +29.6% | +30.4% | +27.9pp | 3 | 1 | +16.1% | -24.5% | 0 |
| 2021, tier WATCHLIST | 7 | +18.5% | +20.9% | +19.0pp | 7 | 0 | +8.0% | -24.5% | 0 |
| 2021, tier AVOID | 42 | +4.2% | +3.5% | +0.2pp | 25 | 0 | -5.2% | -27.9% | 17 |

What the labels say, as hypotheses only:

- **The RICH call held on 82 of its 199 dates, none of them in 2018.** RICH (miss the hurdle and lag the benchmark) needs both: 109 RICH
  dates missed the hurdle, 113 lagged SPY and 82 did both. From every 2018 date the stock returned +17.7% to +76.0% over two years and beat
  SPY (+8.2 to +46.7 points), so the call held on none; from 2019 it held on 15 (2019-08-30 on), from 2020 on 50 of 53 (V +9.0% against
  SPY's +32.8% on average; the three exceptions, 2020-03-20, 2020-03-27 and 2020-04-03, at the March-April lows, returned about +51% and
  cleared the hurdle while still lagging SPY by 36-48 points), and from 2021 on 17. The class was the same at much the same place in its
  own window (the 81st-100th percentile in 2018, the 73rd-100th in 2020) for entries that went on to return +48.0% and +9.0% on average.
- **The FAIR call held on none of its 10 dates, in the other direction.** From 2021-10-28 to 2021-12-31 the stock returned +10.8% to
  +32.4% over two years (one date cleared the hurdle) while SPY returned -7.7% to +12.9%, so it beat the benchmark by 17.5-28.4 points,
  beyond FAIR's 15-point band.
- **The tiers ordered total returns, not returns against SPY.** The mean 2-year total return is +43.4% for ACCUMULATE (6 dates), +38.2% for
  WATCHLIST (21) and +22.7% for AVOID (182), and the order holds within every year with more than one tier (2018 +70.0%, +55.2%, +46.7%; 2019
  WATCHLIST +51.1%, AVOID +33.1%; 2020 +50.9%, +30.0%, +5.9%; 2021 +29.6%, +18.5%, +4.2%). Against SPY the three tiers are +2.0, +5.2 and
  -2.9 points: the two ACCUMULATE dates of March-April 2020 lagged SPY's rebound. The ACCUMULATE and WATCHLIST dates fall at the price lows of
  late 2018 and early 2019, March-April 2020 and late 2021, so this order is largely the entry price itself.
- **The EPP gap did not order the outcomes this time.** Its correlation with the 2-year excess return is +0.29 across the 209 dates
  (2014-2017: -0.5) and changes sign by year (+0.08 in 2018, -0.36 in 2019, +0.77 in 2020, -0.88 in 2021). Against total return it is -0.30:
  the 9 dates 25-50% above the floor (5 at the 2020 lows) returned +49.6%, the 67 at 50-75% +25.1% and the 49 at 105-135% (30 of them in
  2021) +14.2%. The P/E's percentile in its own window carried nothing (correlation -0.03 with the excess return).
- **Scenario landing:** the price two years on sat in the XBULL band on 91 dates (49 of 2018's, 42 of 2019's), the BULL band on 107 (every
  2020 date and 41 of 2021's) and the BASE band on 11 (late 2021): unlike 2014-2017, the later entries reached only BULL or BASE.
- **Drawdowns were deep:** a mean maximum of -31.1% inside the two years (-19.3% to -36.4%); the 2-year low fell on 2020-03-23 for 60 dates
  and on 2022-09-30 for 66.
- **Three-year horizon:** a mean +37.7% (-7.3 points against SPY), +3.4% to +88.5%; by tier ACCUMULATE +60.4%, WATCHLIST +53.2%, AVOID
  +35.2%.
- **The calls the sensitivities name, against the outcomes, and stay as they are.** With the signals at their XBULL values 205 dates read
  CHEAP or FAIR (retro/README.md, "V 2018-2021"): that would have suited the 2018 entries and not the 2020 ones, which lagged SPY on all 53.
  The EPS calls move only the late-2021 dates: GAAP throughout makes 6 of the FAIR dates CHEAP and the company's fiscal 2020 non-GAAP
  figures 2, which their outcomes (17.5-28.4 points over SPY) would have suited; the FY2019-FY2020 seam is the batch's largest EPS call. A
  hypothesis for the live model: for V in these years neither the class nor the distance to the floor separated good entries from poor
  ones; the tiers' order is mostly the entry price. Never fold this back into the archive.

Not tested here: whether any of this holds for other payments networks or other periods. The four years share the 2020 crash and the 2022
decline inside their two-year windows, so they are far from independent, and the 10 FAIR dates are the only cross-sectional test of the class.

## 2022-2026 (254 dates)

Scored on 2026-11-20, after the point-in-time build was committed and pushed (a47d071) and the firewall had passed at 27 cutoffs
(d1da3b3, also pushed). The last close in the price data is 2026-11-19, so the horizons are partial: the 2-year horizon exists for the 150
dates from 2022-01-07 to 2024-11-15, the 1-year for 202 (to 2025-11-14), the 6-month for 228 (to 2026-05-15) and the 3-year for 98 (to
2023-11-17); the 26 newest dates have no horizon yet. Dividends are $0.375 a quarter to October 2022, then $0.45, $0.52, $0.59, $0.67 and
$0.78. The class is RICH on 185 dates, FAIR on 35 and CHEAP on 34, so the tables split by class, year and legacy tier.

Two years:

| Group | Dates | Mean 2y total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle | Mean m12-24 avg price | Mean max drawdown | Call held |
|---|---|---|---|---|---|---|---|---|---|
| all | 150 | +38.0% | +39.3% | -3.5pp | 59 | 98 | +27.3% | -17.1% | 71 |
| class RICH | 106 | +35.8% | +37.5% | -4.4pp | 44 | 61 | +26.2% | -17.6% | 35 |
| class FAIR | 28 | +41.3% | +41.4% | +1.0pp | 13 | 21 | +28.3% | -16.6% | 20 |
| class CHEAP | 16 | +47.4% | +49.0% | -5.3pp | 2 | 16 | +32.2% | -14.7% | 16 |
| 2022 | 52 | +37.8% | +35.2% | +0.5pp | 23 | 31 | +25.0% | -17.5% | 34 |
| 2023 | 52 | +48.0% | +48.3% | +0.0pp | 27 | 49 | +33.6% | -14.4% | 8 |
| 2024 | 46 | +27.1% | +27.1% | -11.9pp | 9 | 18 | +22.6% | -19.7% | 29 |
| tier BUY | 14 | +51.9% | +52.7% | -6.8pp | 1 | 14 | +38.6% | -13.2% | 14 |
| tier ACCUMULATE | 37 | +39.1% | +39.2% | -5.0pp | 10 | 29 | +28.6% | -16.9% | 24 |
| tier WATCHLIST | 88 | +36.5% | +38.0% | -2.5pp | 42 | 51 | +26.0% | -17.5% | 31 |
| tier AVOID | 11 | +28.9% | +24.6% | -2.0pp | 6 | 4 | +18.7% | -19.1% | 2 |
| 2022, class RICH | 15 | +26.7% | +26.7% | +5.3pp | 11 | 1 | +14.2% | -20.7% | 4 |
| 2022, class FAIR | 24 | +39.5% | +38.7% | +0.6pp | 11 | 17 | +27.8% | -17.2% | 17 |
| 2022, class CHEAP | 13 | +47.4% | +49.7% | -5.1pp | 1 | 13 | +32.4% | -14.3% | 13 |
| 2023, class RICH | 46 | +47.6% | +48.3% | +0.3pp | 25 | 43 | +33.6% | -14.5% | 3 |
| 2023, class FAIR | 4 | +52.4% | +52.1% | +3.6pp | 2 | 4 | +31.4% | -13.2% | 3 |
| 2023, class CHEAP | 2 | +48.9% | +48.9% | -13.4pp | 0 | 2 | +37.7% | -13.8% | 2 |
| 2024, class RICH | 45 | +26.7% | +24.3% | -12.4pp | 8 | 17 | +22.7% | -19.6% | 28 |
| 2024, class CHEAP | 1 | +44.4% | +44.4% | +8.9pp | 1 | 1 | +17.9% | -20.8% | 1 |

One year:

| Group | Dates | Mean 1y total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle |
|---|---|---|---|---|---|---|
| all | 202 | +15.4% | +18.5% | -2.4pp | 93 | 115 |
| class RICH | 158 | +14.4% | +17.0% | -4.5pp | 60 | 83 |
| class FAIR | 28 | +18.0% | +17.9% | +7.3pp | 21 | 18 |
| class CHEAP | 16 | +20.9% | +20.3% | +1.5pp | 12 | 14 |
| 2022 | 52 | +14.8% | +13.8% | +7.5pp | 47 | 25 |
| 2023 | 52 | +20.3% | +20.9% | -7.9pp | 2 | 42 |
| 2024 | 52 | +23.4% | +23.9% | +7.8pp | 39 | 43 |
| 2025 | 46 | +1.8% | -0.0% | -18.7pp | 5 | 5 |
| tier BUY | 14 | +24.5% | +25.1% | +3.3pp | 12 | 13 |
| tier ACCUMULATE | 40 | +20.8% | +20.1% | +3.1pp | 23 | 31 |
| tier WATCHLIST | 118 | +16.5% | +18.6% | -1.0pp | 51 | 69 |
| tier AVOID | 30 | -0.2% | -1.2% | -17.5pp | 7 | 2 |
| 2022, class RICH | 15 | +6.0% | +2.2% | +8.7pp | 14 | 0 |
| 2022, class FAIR | 24 | +16.9% | +16.8% | +8.9pp | 21 | 14 |
| 2022, class CHEAP | 13 | +20.9% | +20.5% | +3.6pp | 12 | 11 |
| 2023, class RICH | 46 | +19.9% | +20.8% | -8.3pp | 2 | 36 |
| 2023, class FAIR | 4 | +24.2% | +23.6% | -2.0pp | 0 | 4 |
| 2023, class CHEAP | 2 | +21.4% | +21.4% | -10.8pp | 0 | 2 |
| 2024, class RICH | 51 | +23.4% | +24.0% | +7.9pp | 39 | 42 |
| 2024, class CHEAP | 1 | +19.9% | +19.9% | -1.0pp | 0 | 1 |
| 2025, class RICH | 46 | +1.8% | -0.0% | -18.7pp | 5 | 5 |

Six months:

| Group | Dates | Mean 6m total return | Median | Mean vs SPY | Beat SPY | Cleared hurdle |
|---|---|---|---|---|---|---|
| all | 228 | +7.4% | +7.3% | -0.4pp | 113 | 115 |
| class RICH | 168 | +5.5% | +5.1% | -2.9pp | 63 | 73 |
| class FAIR | 30 | +9.1% | +7.3% | +6.6pp | 26 | 16 |
| class CHEAP | 30 | +16.6% | +14.8% | +6.5pp | 24 | 26 |
| 2022 | 52 | +4.5% | +5.5% | +4.9pp | 43 | 21 |
| 2023 | 52 | +10.6% | +10.4% | -1.9pp | 17 | 36 |
| 2024 | 52 | +12.4% | +13.6% | +5.2pp | 31 | 35 |
| 2025 | 52 | -2.4% | -3.2% | -13.4pp | 4 | 5 |
| 2026 | 20 | +19.2% | +19.6% | +8.2pp | 18 | 18 |
| tier BUY | 25 | +20.0% | +20.3% | +7.9pp | 20 | 25 |
| tier ACCUMULATE | 50 | +10.7% | +9.4% | +2.5pp | 33 | 31 |
| tier WATCHLIST | 123 | +5.9% | +6.1% | -0.7pp | 55 | 55 |
| tier AVOID | 30 | -2.0% | -3.0% | -11.1pp | 5 | 4 |
| 2022, class RICH | 15 | -5.4% | -6.2% | +3.0pp | 11 | 2 |
| 2022, class FAIR | 24 | +7.8% | +5.5% | +7.7pp | 23 | 10 |
| 2022, class CHEAP | 13 | +9.8% | +11.1% | +2.1pp | 9 | 9 |
| 2023, class RICH | 46 | +10.4% | +10.4% | -1.8pp | 16 | 30 |
| 2023, class FAIR | 4 | +11.6% | +12.2% | -1.6pp | 1 | 4 |
| 2023, class CHEAP | 2 | +14.6% | +14.6% | -4.5pp | 0 | 2 |
| 2024, class RICH | 51 | +12.3% | +13.3% | +4.9pp | 30 | 34 |
| 2024, class CHEAP | 1 | +19.6% | +19.6% | +21.4pp | 1 | 1 |
| 2025, class RICH | 52 | -2.4% | -3.2% | -13.4pp | 4 | 5 |
| 2026, class RICH | 4 | +6.1% | +6.5% | -2.6pp | 2 | 2 |
| 2026, class FAIR | 2 | +18.9% | +18.9% | +10.2pp | 2 | 2 |
| 2026, class CHEAP | 14 | +23.0% | +21.8% | +11.0pp | 14 | 14 |

What the labels say, as hypotheses only:

- **The class ordered total returns, not returns against SPY.** Over two years CHEAP returned +47.4% (16 dates, every one clearing the
  hurdle, so the call held on all 16), FAIR +41.3% (28; held on 20) and RICH +35.8% (106); against SPY the three are -5.3, +1.0 and -4.4
  points, and only 2 of the 16 CHEAP dates beat SPY. The order holds within 2022 (CHEAP +47.4%, FAIR +39.5%, RICH +26.7%), the one year
  with all three classes in numbers.
- **The RICH call held on 35 of 106 two-year dates, 3 of them in 2023.** RICH needs both a missed hurdle and a lag behind SPY: 45 RICH
  dates missed the hurdle, 62 lagged SPY and 35 did both. From the 46 RICH dates of 2023 the stock returned +47.6% on average and cleared
  the hurdle on 43; from the 45 of 2024 it returned +26.7% (-12.4 points against SPY) and the call held on 28. The same class at much the
  same place in its window (2023: 29.4-35.4x, the 65th-82nd percentile; 2024: 30.6-35.1x, the 66th-82nd) was followed by +47.6% and
  +26.7%.
- **2025 so far:** RICH on all 52 dates, and on the 46 with a 1-year horizon the stock returned +1.8% (median 0.0%), 18.7 points behind
  SPY, beating it on 5. The 2026 CHEAP dates (14 with a 6-month horizon, from the Q1 FY26 print) returned +23.0% in six months, 11.0 points
  ahead of SPY. Both horizons are short and overlap.
- **The tiers ordered both measures at six months and one year, and only total return at two.** At one year BUY returned +24.5%,
  ACCUMULATE +20.8%, WATCHLIST +16.5% and AVOID -0.2% (+3.3, +3.1, -1.0 and -17.5 points against SPY; AVOID is mostly 2025); at two years
  +51.9%, +39.1%, +36.5% and +28.9%, but -6.8, -5.0, -2.5 and -2.0 points against SPY. Over three years (98 dates) BUY +78.0%, ACCUMULATE
  +70.1%, WATCHLIST +52.5%, AVOID +55.1%. As in 2018-2021, the BUY dates (June and September-December 2022, 2023-10-26, February-June
  2026) sit mostly near price lows, so the order is largely the entry price.
- **The distance to the floor ordered total returns.** The EPP gap's correlation with the 2-year total return is -0.39 (1-year: -0.55):
  the 37 dates 25-40% above the floor returned +46.3%, the 77 at 40-55% +37.1%, the 16 at 55-70% +38.3% and the 20 at 70-90% +26.4%. Against
  SPY the sign flips (+0.25) and changes by year (+0.41 in 2022, +0.12 in 2023, -0.35 in 2024). The P/E's percentile in its own window
  carried little (+0.20 with the 2-year excess return, -0.16 with the 1-year).
- **Scenario landing:** the price two years on sat in the BULL band on 115 dates (every 2023 date) and the BASE band on 35 (19 of 2022's,
  16 of 2024's): never in XBULL or BEAR.
- **Drawdowns were shallower than in 2018-2021:** a mean maximum of -17.1% inside the two years (-12.6% to -24.5%); the 2-year low fell on
  2022-09-30 for 38 dates and on 2024-07-25 for 34.
- **Three-year horizon:** a mean +61.2% (-5.8 points against SPY), +35.3% to +95.7%.
- **The calls the sensitivities name, against the outcomes, and stay as they are.** GAAP every year would have made 57 of the two-year
  dates FAIR or CHEAP; they returned +42.4% (+0.5 points against SPY). The company's non-GAAP figures would have moved 33, which returned
  +48.7% (+3.9 points). The signals at their XBULL values would have moved 130 (+37.4%, -3.7 points) and at their BEAR values 44 to RICH
  (+43.5%). The FY2024 table read as numbers would have made 30 FY2024 dates CHEAP or FAIR, and those returned +30.1%, 13.9 points behind
  SPY, below the hurdle: the words reading suited them better. A hypothesis for the live model: for V in these years the class and the
  floor distance ordered absolute returns but not returns against the market; the RICH label at a 30-35x multiple was right in 2024-2025
  and wrong in 2023. Never fold this back into the archive.

Not tested here: whether any of this holds for other payments networks or other periods. The dates share overlapping windows (the 2022
low and the 2024 rally sit inside most two-year horizons), the 2-year horizon covers only the first 150 dates, and the 16 CHEAP and 28 FAIR
two-year dates are the only cross-sectional test of the class.
