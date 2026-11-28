# FANG 2022-2026: hindsight findings (labels, never inputs)

**HINDSIGHT.** Everything below uses prices after each as-of date (`outcome.json`). It is a label set for the 256 models of
"FANG 2022-2026" (retro/README.md), written after the build, validation, README section and firewall result were committed and pushed.
Nothing here may feed a fact sheet, a builder, a rule or another ticker's models; a rule changed because of it would be a new method
version with a full re-run. Built in a new session that did not open the 2014-2021 outcomes or findings, and they were not opened here.

Coverage on 2026-11-28: 255 of 256 dates have an outcome (2026-11-27 has no later close); 151 have a two-year horizon (2022-01-07 to
2024-11-22), 203 a one-year one (to 2025-11-21). Tables from `retro/generators/fang/findings_tables.py 2022,2023,2024`.

## Summary

- **CHEAP (173 dates) did best:** two-year median +26.6% on 114 dates with a horizon (range -6.4% to +110.1%; 36 beat SPY), one-year median
  +24.1% on 153 (100 beat SPY). 2022's CHEAP dates (FY21's $12.30, then the anchor well below the 2022 earnings) returned +51% over two
  years; 2023's, on FY22's $24.61 (the peak year), only +10%, clearing the hurdle on 5 of 52 and beating SPY on none.
- **RICH (66 dates) did worst:** two-year median +3.0% on 34 (none beat SPY; the call "held" on every one), one-year median -21.8% on 43.
  RICH in 2024 came on FY23's $17.34 against a window median that had fallen to 9x.
- **FAIR (17)** sat between: +10.8% two-year on 3, -1.8% one-year on 7.
- **2025** (one year only): CHEAP 39 dates +40.5% median, FAIR 3 +10.3%, RICH 5 -8.8%.
- **Scenario landing (two years):** BEAR 93, BASE 58 of 151, none at BULL: the BUY tier on 221 dates rests on BULL's EPS CAGR, which the
  stock did not reach.

Hypotheses only (to test on other tickers or later dates, never to fold back): the anchor's position in the cycle (a trough-year
anchor in 2022, a peak-year one in 2023) mattered more than the class; the falling window median made 2024 RICH at prices that later held.

## 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2022-01-07 to 2022-12-30) | 52 | +51.2% | +22.3% to +110.1% | 40 | 36 | +23.0% | 42 |
| FY21E $8.06 (FY18's) (2022-01-07 to 2022-02-18) | 7 | +34.5% | +24.4% to +49.4% | 5 | 7 | +12.2% | 7 |
| FY22E $12.30 (FY21's) (2022-02-24 to 2022-12-30) | 45 | +57.3% | +22.3% to +110.1% | 35 | 29 | +26.3% | 35 |
| latest print Q3 2021 (2022-01-07 to 2022-02-18) | 7 | +34.5% | +24.4% to +49.4% | 5 | 7 | +12.2% | 7 |
| latest print Q4 2021 (2022-02-24 to 2022-04-29) | 10 | +59.2% | +43.9% to +78.5% | 10 | 10 | +13.8% | 10 |
| latest print Q1 2022 (2022-05-04 to 2022-07-29) | 13 | +68.4% | +35.2% to +110.1% | 13 | 12 | +35.4% | 13 |
| latest print Q2 2022 (2022-08-03 to 2022-11-04) | 14 | +57.8% | +22.3% to +76.1% | 11 | 7 | +32.1% | 11 |
| latest print Q3 2022 (2022-11-09 to 2022-12-30) | 8 | +30.4% | +25.8% to +41.5% | 1 | 0 | +34.6% | 1 |
3y (52 dates with one): 3 of 52 cleared, 7 beat SPY; range -0.3% to +71.4%

## 2023 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2023-01-06 to 2023-12-29) | 52 | +9.9% | -6.4% to +39.8% | 5 | 0 | +23.2% | 5 |
| FY22E $12.30 (FY21's) (2023-01-06 to 2023-02-17) | 7 | +30.6% | +19.2% to +34.6% | 3 | 0 | +27.4% | 3 |
| FY23E $24.61 (FY22's) (2023-02-23 to 2023-12-29) | 45 | +8.6% | -6.4% to +39.8% | 2 | 0 | +11.7% | 2 |
| latest print Q3 2022 (2023-01-06 to 2023-02-17) | 7 | +30.6% | +19.2% to +34.6% | 3 | 0 | +27.4% | 3 |
| latest print Q4 2022 (2023-02-23 to 2023-04-28) | 10 | +14.0% | -3.3% to +39.8% | 2 | 0 | +31.4% | 2 |
| latest print Q1 2023 (2023-05-03 to 2023-07-28) | 13 | +15.8% | +9.3% to +28.6% | 0 | 0 | +30.3% | 0 |
| latest print Q2 2023 (2023-08-02 to 2023-11-03) | 14 | +1.9% | -6.4% to +9.4% | 0 | 0 | +1.8% | 0 |
| latest print Q3 2023 (2023-11-08 to 2023-12-29) | 8 | +3.7% | +1.5% to +14.2% | 0 | 0 | -4.0% | 0 |
3y (47 dates with one): 15 of 52 cleared, 2 beat SPY; range +14.5% to +75.5%

## 2024 (47 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2024-01-05 to 2024-11-01) | 10 | +13.8% | +1.1% to +25.3% | 0 | 0 | -3.3% | 0 |
| class FAIR, legacy tier BUY (2024-02-22 to 2024-09-20) | 3 | +10.8% | +6.5% to +15.4% | 0 | 0 | -3.7% | 0 |
| class RICH, legacy tier BUY (2024-03-01 to 2024-11-22) | 27 | +4.2% | -5.1% to +16.0% | 0 | 0 | -18.1% | 27 |
| class RICH, legacy tier ACCUMULATE (2024-06-28 to 2024-10-11) | 7 | -0.9% | -10.9% to +6.6% | 0 | 0 | -18.6% | 7 |
| FY23E $24.61 (FY22's) (2024-01-05 to 2024-02-16) | 7 | +6.1% | +1.1% to +17.5% | 0 | 0 | -4.7% | 0 |
| FY24E $17.34 (FY23's) (2024-02-22 to 2024-11-22) | 40 | +5.5% | -10.9% to +25.3% | 0 | 0 | -15.7% | 34 |
| latest print Q3 2023 (2024-01-05 to 2024-02-16) | 7 | +6.1% | +1.1% to +17.5% | 0 | 0 | -4.7% | 0 |
| latest print Q4 2023 (2024-02-22 to 2024-04-26) | 10 | +1.4% | -5.1% to +7.0% | 0 | 0 | -23.8% | 9 |
| latest print Q1 2024 (2024-05-02 to 2024-08-02) | 14 | +6.2% | -10.9% to +12.3% | 0 | 0 | -18.6% | 14 |
| latest print Q2 2024 (2024-08-07 to 2024-11-01) | 13 | +12.1% | -0.9% to +25.3% | 0 | 0 | -3.7% | 8 |
| latest print Q3 2024 (2024-11-06 to 2024-11-22) | 3 | +1.9% | -0.6% to +9.5% | 0 | 0 | -0.7% | 3 |
3y: none yet
