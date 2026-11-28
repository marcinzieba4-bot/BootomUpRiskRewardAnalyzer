# FANG retrospective: findings (HINDSIGHT)

**Everything here is hindsight**, computed by `retro_tool.py outcome` after the 2014-2017 batch's build, validation outputs, README
section and firewall result were committed and pushed (retro/README.md, "FANG 2014-2017"). The outcomes are labels, never inputs: no
pattern below may feed `retro/facts/FANG.json`, `retro/build_fang.py`, the engine or a rule, and none was used to choose an encoding.
They are hypotheses to test on other tickers or periods. Tables: `python3 retro/generators/fang/findings_tables.py 2014,2015,2016,2017`.

## Totals (202 dates, 2014-02-21 to 2017-12-29; every date has its 2-year horizon)

- **Class FAIR 104, CHEAP 81, RICH 17; legacy tier BUY on all 202.** BUY cleared the 15%/yr hurdle over two years on 79 of 202 dates
  (12 of 45 in 2014, 34 of 53 in 2015, 33 of 52 in 2016, 0 of 52 in 2017).
- **By the 2-year call check:** CHEAP held on 52 of 81 (all 4 of late 2014 at a median +81.9%, 39 of 40 in 2015 at +42.7%, all 9 of
  early 2016 at +76.3%, none of the 28 of 2017 at +7.5%); FAIR held on 56 of 104; RICH (17, 2016) held on 9, as the stock still rose a
  median +29.7% in two years.
- **The anchor on a year already passed worked in the oil-price trough and failed after it.** Dates of 2015 and early 2016, priced on
  FY14's $3.64 while FY2015 and FY2016 were losses, returned a median +38% to +100% over two years; the dates of 2017, on the same $3.64,
  returned a median +3.9% (none cleared the hurdle or beat SPY; 3-year returns -7% to -79%).
- **Scenario landing at two years:** BEAR 188, BASE 14. The bear case here is flat EPS at the 10th-percentile multiple, and the price
  rose well above it on most dates; the landing counts are a property of the short-history bounds (BULL at +182%/yr is out of reach),
  not a test of the bear case.
- **Profile drift:** the models' CYCLICAL, risk 2 matches today's profile in `data/business_profiles.json` (CYCLICAL, risk 2, a 2026
  judgement), which was never an input.

Hypotheses (to test elsewhere, never to fold back here): a BUY tier that rests on a one-change EPS history (the bounds rule's BULL) says
little; the class (CHEAP/FAIR/RICH) carried more of the 2014-2016 information than the tier did.

## 2014 (45 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier BUY (2014-02-21 to 2014-12-19) | 41 | +19.3% | -5.5% to +68.2% | 8 | 28 | +3.9% | 33 |
| class CHEAP, legacy tier BUY (2014-11-28 to 2014-12-26) | 4 | +81.9% | +70.4% to +100.1% | 4 | 4 | +49.7% | 4 |
| FY14E $1.29 (FY13's) (2014-02-21 to 2014-12-26) | 45 | +20.3% | -5.5% to +100.1% | 12 | 32 | +4.8% | 37 |
| latest print Q4 2013 (2014-02-21 to 2014-05-02) | 11 | +18.3% | +9.2% to +21.5% | 0 | 8 | +8.6% | 11 |
| latest print Q1 2014 (2014-05-09 to 2014-08-01) | 13 | +6.5% | -5.5% to +23.0% | 0 | 4 | -10.5% | 13 |
| latest print Q2 2014 (2014-08-07 to 2014-10-31) | 13 | +22.9% | +12.8% to +62.5% | 4 | 12 | +6.1% | 9 |
| latest print Q3 2014 (2014-11-06 to 2014-12-26) | 8 | +70.4% | +39.1% to +100.1% | 8 | 8 | +43.7% | 4 |
3y (45 dates with one): 18 of 45 cleared, 26 beat SPY; range -3.1% to +112.6%
1y range -25.4 45.9 excess 2y -14.2 83.2
drawdown -42.6 -31.5

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2015-01-02 to 2015-12-31) | 40 | +42.7% | +16.0% to +88.7% | 29 | 39 | +34.9% | 39 |
| class FAIR, legacy tier BUY (2015-05-08 to 2015-11-27) | 13 | +30.7% | +12.1% to +44.6% | 5 | 9 | +27.1% | 12 |
| FY14E $1.29 (FY13's) (2015-01-02 to 2015-02-13) | 7 | +52.5% | +42.0% to +68.6% | 7 | 7 | +33.8% | 7 |
| FY15E $3.64 (FY14's) (2015-02-19 to 2015-12-31) | 46 | +37.9% | +12.1% to +88.7% | 27 | 41 | +30.5% | 44 |
| latest print Q3 2014 (2015-01-02 to 2015-02-13) | 7 | +52.5% | +42.0% to +68.6% | 7 | 7 | +33.8% | 7 |
| latest print Q4 2014 (2015-02-19 to 2015-05-01) | 11 | +31.6% | +20.9% to +48.8% | 5 | 11 | +21.7% | 11 |
| latest print Q1 2015 (2015-05-08 to 2015-07-31) | 13 | +25.6% | +12.1% to +45.9% | 3 | 9 | +28.0% | 12 |
| latest print Q2 2015 (2015-08-07 to 2015-10-30) | 13 | +37.9% | +22.8% to +46.6% | 10 | 12 | +41.7% | 13 |
| latest print Q3 2015 (2015-11-05 to 2015-12-31) | 9 | +44.6% | +38.4% to +88.7% | 9 | 9 | +29.8% | 8 |
3y (53 dates with one): 39 of 53 cleared, 50 beat SPY; range +26.7% to +113.4%
1y range -5.9 54.1 excess 2y -8.2 55.6
drawdown -31.5 -24.1

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2016-01-08 to 2016-03-04) | 9 | +76.3% | +67.8% to +115.6% | 9 | 9 | +48.7% | 9 |
| class FAIR, legacy tier BUY (2016-03-11 to 2016-12-30) | 26 | +44.0% | -13.4% to +65.3% | 16 | 14 | +30.2% | 11 |
| class RICH, legacy tier BUY (2016-04-29 to 2016-12-02) | 17 | +29.7% | +2.4% to +54.8% | 8 | 8 | +23.7% | 9 |
| FY15E $3.64 (FY14's) (2016-01-08 to 2016-02-12) | 6 | +99.8% | +67.8% to +115.6% | 6 | 6 | +53.6% | 6 |
| FY16E $3.64 (FY14's) (2016-02-18 to 2016-12-30) | 46 | +43.9% | -13.4% to +76.3% | 27 | 25 | +26.8% | 23 |
| latest print Q3 2015 (2016-01-08 to 2016-02-12) | 6 | +99.8% | +67.8% to +115.6% | 6 | 6 | +53.6% | 6 |
| latest print Q4 2015 (2016-02-18 to 2016-04-29) | 11 | +64.4% | +43.9% to +76.3% | 11 | 11 | +35.0% | 4 |
| latest print Q1 2016 (2016-05-05 to 2016-07-29) | 13 | +44.8% | +27.7% to +54.8% | 10 | 9 | +25.5% | 6 |
| latest print Q2 2016 (2016-08-04 to 2016-11-04) | 14 | +26.6% | +17.5% to +47.3% | 6 | 5 | +25.8% | 11 |
| latest print Q3 2016 (2016-11-09 to 2016-12-30) | 8 | +2.4% | -13.4% to +18.1% | 0 | 0 | +21.2% | 2 |
3y (52 dates with one): 3 of 52 cleared, 3 beat SPY; range -27.0% to +73.3%
1y range -11.5 70.6 excess 2y -28.2 68.0
drawdown -38.8 -24.1

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR, legacy tier BUY (2017-01-06 to 2017-12-29) | 24 | -3.8% | -30.7% to +8.1% | 0 | 0 | +10.4% | 0 |
| class CHEAP, legacy tier BUY (2017-02-24 to 2017-10-13) | 28 | +7.5% | -16.6% to +25.6% | 0 | 0 | +18.5% | 0 |
| FY16E $3.64 (FY14's) (2017-01-06 to 2017-02-10) | 6 | -1.1% | -7.5% to +4.0% | 0 | 0 | +17.4% | 0 |
| FY17E $3.64 (FY14's) (2017-02-16 to 2017-12-29) | 46 | +3.9% | -30.7% to +25.6% | 0 | 0 | +13.4% | 0 |
| latest print Q3 2016 (2017-01-06 to 2017-02-10) | 6 | -1.1% | -7.5% to +4.0% | 0 | 0 | +17.4% | 0 |
| latest print Q4 2016 (2017-02-16 to 2017-04-28) | 11 | +1.7% | -5.4% to +7.9% | 0 | 0 | +14.2% | 0 |
| latest print Q1 2017 (2017-05-04 to 2017-07-28) | 13 | +8.4% | +6.0% to +25.6% | 0 | 0 | +22.4% | 0 |
| latest print Q2 2017 (2017-08-03 to 2017-11-03) | 14 | +3.9% | -21.1% to +12.5% | 0 | 0 | +12.7% | 0 |
| latest print Q3 2017 (2017-11-08 to 2017-12-29) | 8 | -27.3% | -30.7% to -21.3% | 0 | 0 | -11.2% | 0 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -79.3% to -7.4%
1y range -28.3 56.9 excess 2y -54.2 -0.2
drawdown -47.0 -38.8
