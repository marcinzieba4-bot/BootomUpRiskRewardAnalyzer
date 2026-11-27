# CHTR retrospective: findings (HINDSIGHT)

**Everything here is hindsight**, computed by `retro_tool.py outcome` after the 2018-2021 batch's build, validation outputs, README
section and firewall result were committed and pushed (retro/README.md, "CHTR 2018-2021"). The outcomes are labels, never inputs: no
pattern below may feed `retro/facts/CHTR.json`, `retro/build_chtr.py`, the engine or a rule, and none was used to choose an encoding.
They are hypotheses to test on other tickers or periods. Tables: `python3 retro/generators/chtr/findings_tables.py 2019,2020,2021`.

## Totals (153 dates, 2019-02-01 to 2021-12-31; every date has its 2-year horizon)

- **Class RICH 77, CHEAP 66, FAIR 10.** By the 2-year call check, the RICH calls held on 30 of 77 (the 25 RICH dates of 2020-07-31
  to 2021-01-22, the four of January 2020 and 2019-12-13) and failed on the other 47 of 2019, when the stock rose a median +76% in two years
  (46 of 48 cleared the 15%/yr hurdle). The CHEAP calls held on 1 of 66: the 17 of 2020 returned a median +10.7% in two years, the 49
  from the Q4 2020 print a median -44.5% (none cleared the hurdle or beat SPY; 3-year returns -37% to -62%). FAIR (10) returned -7.5%.
- **Scenario landing at two years:** XBULL 52 (2019 and January 2020), BASE 28, BEAR 73 (from the Q2 2020 print on).
- **Profile drift:** the models' DURABLE, risk 2 against today's profile in `data/business_profiles.json` (STRUCTURAL, risk 4, a 2026
  judgement: cable broadband losing share to fixed-wireless and fiber). That reading was never an input.


## 2019 (48 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2019-02-01 to 2019-12-27) | 47 | +76.1% | +27.4% to +106.9% | 46 | 38 | +59.9% | 1 |
| class RICH, legacy tier WATCHLIST (2019-03-08 to 2019-03-08) | 1 | +81.4% | +81.4% to +81.4% | 1 | 1 | +70.5% | 0 |
| FY19E $5.22 (FY18's) (2019-02-01 to 2019-12-27) | 48 | +76.3% | +27.4% to +106.9% | 47 | 39 | +60.6% | 1 |
| latest print Q4 2018 (2019-02-01 to 2019-04-26) | 13 | +76.3% | +70.4% to +83.5% | 13 | 13 | +65.4% | 0 |
| latest print Q1 2019 (2019-05-01 to 2019-07-19) | 12 | +81.5% | +72.7% to +87.5% | 12 | 12 | +58.7% | 0 |
| latest print Q2 2019 (2019-07-26 to 2019-10-18) | 13 | +86.4% | +60.6% to +106.9% | 13 | 13 | +61.2% | 0 |
| latest print Q3 2019 (2019-10-25 to 2019-12-27) | 10 | +42.7% | +27.4% to +58.2% | 9 | 1 | +45.6% | 1 |
3y (48 dates with one): 11 of 48 cleared, 7 beat SPY; range -35.1% to +77.0%
1y range 3.0 59.3 excess 2y -23.2 46.2
drawdown -31.5 -31.5

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2020-01-03 to 2020-01-24) | 4 | +20.9% | +14.4% to +31.0% | 0 | 0 | +36.2% | 4 |
| class CHEAP, legacy tier BUY (2020-01-31 to 2020-07-02) | 17 | +10.7% | -15.9% to +55.3% | 1 | 0 | +32.0% | 1 |
| class FAIR, legacy tier BUY (2020-02-07 to 2020-10-30) | 10 | -7.5% | -39.0% to +16.3% | 0 | 0 | +19.5% | 0 |
| class RICH, legacy tier BUY (2020-07-31 to 2020-12-18) | 17 | -39.3% | -53.2% to -21.0% | 0 | 0 | -10.2% | 17 |
| class RICH, legacy tier ACCUMULATE (2020-11-20 to 2020-12-31) | 5 | -42.9% | -49.1% to -41.5% | 0 | 0 | -27.7% | 5 |
| FY19E $5.22 (FY18's) (2020-01-03 to 2020-01-24) | 4 | +20.9% | +14.4% to +31.0% | 0 | 0 | +36.2% | 4 |
| FY20E $7.45 (FY19's) (2020-01-31 to 2020-12-31) | 49 | -15.9% | -53.2% to +55.3% | 1 | 0 | +9.7% | 23 |
| latest print Q3 2019 (2020-01-03 to 2020-01-24) | 4 | +20.9% | +14.4% to +31.0% | 0 | 0 | +36.2% | 4 |
| latest print Q4 2019 (2020-01-31 to 2020-04-24) | 13 | +16.3% | +0.6% to +55.3% | 1 | 0 | +37.1% | 1 |
| latest print Q1 2020 (2020-05-01 to 2020-07-24) | 13 | -9.3% | -17.6% to -6.3% | 0 | 0 | +21.9% | 0 |
| latest print Q2 2020 (2020-07-31 to 2020-10-23) | 13 | -32.6% | -51.1% to -21.0% | 0 | 0 | -5.4% | 13 |
| latest print Q3 2020 (2020-10-30 to 2020-12-31) | 10 | -41.6% | -53.2% to -39.0% | 0 | 0 | -24.5% | 9 |
3y (53 dates with one): 0 of 53 cleared, 0 beat SPY; range -42.5% to -6.2%
1y range -6.3 69.4 excess 2y -65.6 -19.8
drawdown -63.1 -31.5

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier BUY (2021-01-08 to 2021-01-22) | 3 | -38.7% | -42.0% to -38.2% | 0 | 0 | -28.0% | 3 |
| class CHEAP, legacy tier BUY (2021-01-29 to 2021-12-31) | 49 | -44.5% | -54.8% to -34.2% | 0 | 0 | -44.1% | 0 |
| FY20E $7.45 (FY19's) (2021-01-08 to 2021-01-22) | 3 | -38.7% | -42.0% to -38.2% | 0 | 0 | -28.0% | 3 |
| FY21E $15.40 (FY20's) (2021-01-29 to 2021-12-31) | 49 | -44.5% | -54.8% to -34.2% | 0 | 0 | -44.1% | 0 |
| latest print Q3 2020 (2021-01-08 to 2021-01-22) | 3 | -38.7% | -42.0% to -38.2% | 0 | 0 | -28.0% | 3 |
| latest print Q4 2020 (2021-01-29 to 2021-04-23) | 13 | -41.2% | -49.4% to -34.2% | 0 | 0 | -32.3% | 0 |
| latest print Q1 2021 (2021-04-30 to 2021-07-23) | 13 | -50.2% | -54.8% to -45.3% | 0 | 0 | -44.9% | 0 |
| latest print Q2 2021 (2021-07-30 to 2021-10-22) | 13 | -44.5% | -48.4% to -35.7% | 0 | 0 | -52.1% | 0 |
| latest print Q3 2021 (2021-10-29 to 2021-12-31) | 10 | -40.4% | -44.9% to -39.1% | 0 | 0 | -43.2% | 0 |
3y (52 dates with one): 0 of 52 cleared, 0 beat SPY; range -62.0% to -37.3%
1y range -58.9 -1.4 excess 2y -59.2 -34.5
drawdown -63.1 -53.5
landing {'XBULL': 52, 'BASE': 28, 'BEAR': 73}
drift {'{"then": {"kind": "DURABLE", "risk": 2}, "today": {"kind": "STRUCTURAL", "reviewed": "2026-09-22", "risk": 4, "why": "Cable broadband losing share to fixed-wire'}

## Hypotheses (not rules; test them elsewhere before using them)

1. **A short window on a fast-rising GAAP EPS mis-scales the multiple.** The window starts in 2018 (FY2017 excluded) and the anchor
   steps from .22 to .45 to 5.40. In 2019 the stock looked dear against a one-to-two-year window (65-97x) while it compounded; in 2021
   the doubled FY2020 EPS made the same price look cheap against a window built on the lower anchors, just before two years of -35% to
   -55%. Both errors come from the window, not the signals (the signals at BEAR or XBULL move 26 classes each, the FY2017 reading 56).
2. **CHEAP right after an EPS step-up is the weakest call here** (49 dates, 0 held). A test elsewhere: CHEAP calls in the first year
   after the anchor rises by more than half.
3. **The theme on the watch list was not the one that hit.** STREAMING (video) was company-acknowledged throughout, while the 2022-2023
   decline came with broadband customer losses; total customer relationships scored BASE or BULL on every print (+3.3% to +6.8%). Whether
   a broadband-substitution theme was dated public evidence before 2022 is a registry question for the owner, not an input here.
4. **The FY2017 exclusion decided the start, and the start mattered:** kept at GAAP, it would have built 52 dates of 2018 and moved 56
   classes of 2019-2021 (most CHEAP to FAIR or RICH). Without outcomes for 2018, nothing can be said about those dates.
