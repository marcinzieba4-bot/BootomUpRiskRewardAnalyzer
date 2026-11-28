# FANG 2018-2021: hindsight findings (labels, never inputs)

**HINDSIGHT.** Everything below uses prices after each as-of date (`outcome.json`, written by `retro_tool.py outcome` after the
build, validation, README section and firewall were committed and pushed). These are hypotheses for the owner, never inputs: no rule,
fact, parameter or encoding may be changed because of them (retro/README.md, "Outcomes"; CLAUDE.md). The 2014-2017 findings
(`FINDINGS.md`) were not opened in this session. Tables: `python3 retro/generators/fang/findings_tables.py 2018,2019,2020,2021`.

**What the models said:** CHEAP and BUY on all 209 dates (2018-01-05 to 2021-12-31), on FY14's $3.64 (to 2018-02-09), FY17's $4.94
(2018-02-15 to 2019-02-15) and FY18's $8.06 (2019-02-21 on, as FY2019 was excluded as distorted and FY2020 as a loss).

**What happened (2-year total returns):**
- 2018 dates: median -66.5% (-83.0% to -26.5%); none cleared the 15%/yr hurdle or beat SPY over two years (the 2020 oil collapse sits
  inside every 2018 window); 3-year: none cleared, range -56.7% to +24.2%; max drawdowns -47% to -89%.
- 2019 dates: median -16.5%; 7 of 52 cleared (the Q3 2019 print's dates, from November 2019); 3-year: 17 cleared, 22 beat SPY.
- 2020 dates: median +236.6%; 52 of 53 cleared, 51 beat SPY (the COVID lows bought on FY18's $8.06 at 2-6x); 3-year: all 53 cleared.
- 2021 dates: median +83.0%; all 52 cleared and beat SPY over two and three years.
- Scenario landing at two years: BEAR 186, BASE 23 of 209.

**Hypotheses (for the owner; not rules):**
1. A uniform CHEAP call across a commodity cycle is a coin on timing: the same call lost 66% (2018) and gained 237% (2020). The class
   did not separate the two regimes; only the price did.
2. Anchoring on the last kept GAAP year (FY18's $8.06) through two excluded years held a "cheap" reading through the 2020 trough, which
   paid off from 2020 dates but not from 2019 dates. The sensitivity's alternative (FY2019 kept at $1.47) would have made 76 dates of
   2020-2021 RICH, every one of which cleared the hurdle in hindsight; this is an observation about one cycle, not a reason to change the
   AAPL FY2002 test.
3. With no guide in numbers, BASE follows the latest quarter's revenue growth, which swung from -58% to +296%; the signals sat at BEAR
   or XBULL mechanically on the COVID comparison quarters. Neither moved the class.

## Tables
## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2018-01-05 to 2018-12-28) | 52 | -66.5% | -83.0% to -26.5% | 0 | 0 | -45.4% | 0 |
| FY17E $3.64 (FY14's) (2018-01-05 to 2018-02-09) | 6 | -29.0% | -38.4% to -26.5% | 0 | 0 | -24.2% | 0 |
| FY18E $4.94 (FY17's) (2018-02-15 to 2018-12-28) | 46 | -66.7% | -83.0% to -39.2% | 0 | 0 | -47.1% | 0 |
| latest print Q3 2017 (2018-01-05 to 2018-02-09) | 6 | -29.0% | -38.4% to -26.5% | 0 | 0 | -24.2% | 0 |
| latest print Q4 2017 (2018-02-15 to 2018-05-04) | 12 | -70.9% | -83.0% to -39.2% | 0 | 0 | -28.2% | 0 |
| latest print Q1 2018 (2018-05-10 to 2018-08-03) | 13 | -66.5% | -70.5% to -46.0% | 0 | 0 | -41.7% | 0 |
| latest print Q2 2018 (2018-08-10 to 2018-11-02) | 13 | -73.5% | -76.4% to -60.9% | 0 | 0 | -54.1% | 0 |
| latest print Q3 2018 (2018-11-08 to 2018-12-28) | 8 | -53.4% | -75.9% to -45.8% | 0 | 0 | -53.8% | 0 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -56.7% to +24.2%
1y range -36.9 -0.1 excess 2y -106.2 -48.4
drawdown -88.9 -47.0

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2019-01-04 to 2019-12-27) | 52 | -16.5% | -48.8% to +54.5% | 7 | 0 | -45.4% | 7 |
| FY18E $4.94 (FY17's) (2019-01-04 to 2019-02-15) | 7 | -41.5% | -48.8% to -26.4% | 0 | 0 | -58.4% | 0 |
| FY19E $8.06 (FY18's) (2019-02-21 to 2019-12-27) | 45 | -15.3% | -33.8% to +54.5% | 7 | 0 | -41.9% | 7 |
| latest print Q3 2018 (2019-01-04 to 2019-02-15) | 7 | -41.5% | -48.8% to -26.4% | 0 | 0 | -58.4% | 0 |
| latest print Q4 2018 (2019-02-21 to 2019-05-03) | 11 | -24.5% | -33.8% to -9.3% | 0 | 0 | -55.7% | 0 |
| latest print Q1 2019 (2019-05-09 to 2019-08-02) | 13 | -16.5% | -27.5% to -6.2% | 0 | 0 | -47.2% | 0 |
| latest print Q2 2019 (2019-08-08 to 2019-11-01) | 13 | -13.1% | -22.4% to +36.9% | 2 | 0 | -32.8% | 2 |
| latest print Q3 2019 (2019-11-07 to 2019-12-27) | 8 | +44.3% | +16.3% to +54.5% | 5 | 0 | -0.1% | 5 |
3y (52 dates with one): 17 of 52 cleared, 22 beat SPY; range +6.2% to +129.8%
1y range -80.7 -4.8 excess 2y -99.4 -1.2
drawdown -86.3 -83.9

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2020-01-03 to 2020-12-31) | 53 | +236.6% | +21.9% to +625.8% | 52 | 51 | +183.4% | 52 |
| FY19E $8.06 (FY18's) (2020-01-03 to 2020-02-14) | 7 | +48.1% | +21.9% to +79.7% | 6 | 5 | +7.1% | 6 |
| FY20E $8.06 (FY18's) (2020-02-20 to 2020-12-31) | 46 | +259.9% | +71.7% to +625.8% | 46 | 46 | +191.8% | 46 |
| latest print Q3 2019 (2020-01-03 to 2020-02-14) | 7 | +48.1% | +21.9% to +79.7% | 6 | 5 | +7.1% | 6 |
| latest print Q4 2019 (2020-02-20 to 2020-05-01) | 11 | +317.3% | +71.7% to +625.8% | 11 | 11 | +191.4% | 11 |
| latest print Q1 2020 (2020-05-06 to 2020-07-31) | 13 | +214.6% | +174.9% to +276.2% | 13 | 13 | +173.8% | 13 |
| latest print Q2 2020 (2020-08-05 to 2020-10-30) | 13 | +318.8% | +205.2% to +526.5% | 13 | 13 | +309.5% | 13 |
| latest print Q3 2020 (2020-11-04 to 2020-12-31) | 9 | +230.7% | +180.0% to +527.6% | 9 | 9 | +191.1% | 9 |
3y (53 dates with one): 53 of 53 cleared, 53 beat SPY; range +52.1% to +655.2%
1y range -47.1 321.8 excess 2y -29.8 526.5
drawdown -83.9 -33.5

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2021-01-08 to 2021-12-31) | 52 | +83.0% | +44.4% to +185.2% | 52 | 52 | +70.0% | 52 |
| FY20E $8.06 (FY18's) (2021-01-08 to 2021-02-19) | 7 | +148.3% | +121.7% to +185.2% | 7 | 7 | +112.6% | 7 |
| FY21E $8.06 (FY18's) (2021-02-24 to 2021-12-31) | 45 | +80.0% | +44.4% to +137.8% | 45 | 45 | +65.2% | 45 |
| latest print Q3 2020 (2021-01-08 to 2021-02-19) | 7 | +148.3% | +121.7% to +185.2% | 7 | 7 | +112.6% | 7 |
| latest print Q4 2020 (2021-02-24 to 2021-04-30) | 10 | +90.2% | +79.9% to +107.4% | 10 | 10 | +80.1% | 10 |
| latest print Q1 2021 (2021-05-05 to 2021-07-30) | 13 | +75.7% | +44.4% to +106.6% | 13 | 13 | +65.2% | 13 |
| latest print Q2 2021 (2021-08-04 to 2021-10-29) | 13 | +105.6% | +50.4% to +137.8% | 13 | 13 | +70.0% | 13 |
| latest print Q3 2021 (2021-11-03 to 2021-12-31) | 9 | +59.6% | +49.0% to +69.4% | 9 | 9 | +33.9% | 9 |
3y (52 dates with one): 52 of 52 cleared, 52 beat SPY; range +69.4% to +214.7%
1y range 24.6 130.1 excess 2y 39.9 172.3
drawdown -33.5 -33.5
