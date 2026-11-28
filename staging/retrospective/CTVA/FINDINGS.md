# CTVA retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 295 CTVA weekly dates, 2021-02-05 to 2026-09-25: Corteva, Inc. (NYSE: CTVA), from the first
date after its first full year of GAAP EPS to the last date before the 2026-10-01 distribution of its seed business.
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The series was scored only after its
point-in-time build was committed and pushed (32fb561; README and firewall result 0acd1f3). Outcomes were computed on 2026-11-16 from the
closes posted to 2026-11-13: 197 dates have a two-year outcome (the last, 2024-11-08, ends 2026-11-06), 249 a one-year outcome and the
return to the average price over months 12-24, and the 46 dates from 2025-11-07 none. Total returns include the $0.13-0.18 quarterly
dividends. Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.
"Call held" is `call_check_2y`, always the class's test (a tier row counts the class calls on its dates): CHEAP should clear the hurdle
or beat the benchmark (SPY), FAIR should land within ±15pp of it, and RICH should miss the hurdle and lag it. A row's "Dates" counts every
date of the group; where fewer have two years, the count with two years follows in brackets, and only those enter the two-year columns.

**Hindsight the model could not see:**
- **The separation.** Corteva announced on 2025-10-01 that it would separate its crop protection and seed businesses, and distributed the
  seed business on 2026-10-01. The announcement is in the record from 2025-10-01 but no input of the method reads it (it changes no guided
  number). Outcomes keep Yahoo's 6665:1000 factor for the distribution, so a holder's return after 2026-10-01 counts the distributed
  shares as reinvested in CTVA (the MAR rule); one-year outcomes from 2025-10 and the m12-24 averages from 2024-10 run across it.
- **Operating EPS.** The company's own measure rose from $1.50 (2020) to $2.15, $2.67, $2.69, $2.57 and $3.34 (2025) while GAAP EPS went
  $0.98, $2.44, $1.66, $1.30, $1.22, $1.75. The models read GAAP by rule (the recurring-amortization rule); the market's own reading of the
  years is not in any model.

## 2021 (48 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 48 | +24.3% | -8.4% to +47.8% | 12 | 43 | +32.7% | 5 |
| EPS anchor $0.98 (2021-02-05 to 2021-12-31) | 48 | +24.3% | -8.4% to +47.8% | 12 | 43 | +32.7% | 5 |
| latest print Q4 2020 (2021-02-05 to 2021-04-30) | 13 | +31.5% | +21.0% to +47.8% | 6 | 13 | +28.2% | 0 |
| latest print Q1 2021 (2021-05-06 to 2021-07-30) | 13 | +31.4% | +22.7% to +36.7% | 6 | 13 | +35.4% | 0 |
| latest print Q2 2021 (2021-08-06 to 2021-10-29) | 13 | +19.8% | +13.6% to +28.3% | 0 | 13 | +35.4% | 0 |
| latest print Q3 2021 (2021-11-05 to 2021-12-31) | 9 | +3.0% | -8.4% to +8.0% | 0 | 4 | +18.8% | 5 |

## 2022 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 46 | -1.6% | -15.3% to +10.5% | 0 | 0 | -10.0% | 0 |
| class FAIR, legacy tier BUY | 2 | -1.5% | -4.9% to -1.5% | 0 | 0 | -11.7% | 0 |
| class RICH, legacy tier AVOID | 4 | +0.2% | -2.7% to +3.0% | 0 | 0 | +13.5% | 4 |
| EPS anchor $0.98 (2022-01-07 to 2022-01-28) | 4 | +0.2% | -2.7% to +3.0% | 0 | 0 | +13.5% | 4 |
| EPS anchor $2.44 (2022-02-04 to 2022-12-30) | 48 | -1.6% | -15.3% to +10.5% | 0 | 0 | -10.1% | 0 |
| latest print Q3 2021 (2022-01-07 to 2022-01-28) | 4 | +0.2% | -2.7% to +3.0% | 0 | 0 | +13.5% | 4 |
| latest print Q4 2021 (2022-02-04 to 2022-04-29) | 13 | +1.0% | -9.9% to +10.5% | 0 | 0 | -5.5% | 0 |
| latest print Q1 2022 (2022-05-06 to 2022-07-29) | 13 | +0.4% | -10.0% to +5.2% | 0 | 0 | -5.9% | 0 |
| latest print Q2 2022 (2022-08-05 to 2022-10-28) | 13 | -5.5% | -15.3% to +5.1% | 0 | 0 | -15.4% | 0 |
| latest print Q3 2022 (2022-11-04 to 2022-12-30) | 9 | -3.1% | -10.9% to +0.8% | 0 | 0 | -17.5% | 0 |

## 2023 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 8 | +38.3% | +27.5% to +47.4% | 7 | 1 | +24.5% | 7 |
| class CHEAP, legacy tier BUY | 19 | +37.8% | -4.6% to +53.6% | 11 | 2 | +31.7% | 11 |
| class FAIR, legacy tier ACCUMULATE | 15 | +29.9% | +4.5% to +36.0% | 3 | 0 | +5.0% | 9 |
| class FAIR, legacy tier WATCHLIST | 7 | +3.4% | -4.5% to +7.1% | 0 | 0 | -6.0% | 0 |
| class RICH, legacy tier WATCHLIST | 3 | -1.5% | -3.1% to -0.9% | 0 | 0 | -10.3% | 3 |
| EPS anchor $2.44 (2023-01-06 to 2023-01-27) | 4 | +2.0% | -4.6% to +3.0% | 0 | 0 | -10.6% | 0 |
| EPS anchor $1.66 (2023-02-03 to 2023-12-29) | 48 | +31.3% | -4.5% to +53.6% | 21 | 3 | +10.5% | 30 |
| latest print Q3 2022 (2023-01-06 to 2023-01-27) | 4 | +2.0% | -4.6% to +3.0% | 0 | 0 | -10.6% | 0 |
| latest print Q4 2022 (2023-02-03 to 2023-04-28) | 13 | +3.4% | -4.5% to +11.5% | 0 | 0 | -6.0% | 3 |
| latest print Q1 2023 (2023-05-05 to 2023-07-28) | 13 | +31.3% | +9.4% to +37.2% | 4 | 0 | +5.4% | 9 |
| latest print Q2 2023 (2023-08-04 to 2023-11-03) | 14 | +36.5% | +26.0% to +50.0% | 9 | 3 | +27.3% | 10 |
| latest print Q3 2023 (2023-11-10 to 2023-12-29) | 8 | +44.4% | +37.8% to +53.6% | 8 | 0 | +41.9% | 8 |

## 2024 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 4 | +55.7% | +46.2% to +61.3% | 4 | 3 | +46.2% | 4 |
| class RICH, legacy tier AVOID | 48 (41 with 2 yrs) | +47.8% | +29.8% to +66.3% | 40 | 34 | +30.6% | 1 |
| EPS anchor $1.66 (2024-01-05 to 2024-01-26) | 4 | +55.7% | +46.2% to +61.3% | 4 | 3 | +46.2% | 4 |
| EPS anchor $1.30 (2024-02-02 to 2024-12-27) | 48 (41 with 2 yrs) | +47.8% | +29.8% to +66.3% | 40 | 34 | +30.6% | 1 |
| latest print Q3 2023 (2024-01-05 to 2024-01-26) | 4 | +55.7% | +46.2% to +61.3% | 4 | 3 | +46.2% | 4 |
| latest print Q4 2023 (2024-02-02 to 2024-04-26) | 13 | +44.6% | +39.4% to +58.5% | 13 | 10 | +25.7% | 0 |
| latest print Q1 2024 (2024-05-03 to 2024-07-26) | 13 | +51.2% | +42.4% to +66.3% | 13 | 11 | +34.4% | 0 |
| latest print Q2 2024 (2024-08-02 to 2024-11-01) | 14 | +48.9% | +29.8% to +61.3% | 13 | 12 | +32.8% | 1 |
| latest print Q3 2024 (2024-11-08 to 2024-12-27) | 8 (1 with 2 yrs) | +38.4% | +38.4% to +38.4% | 1 | 1 | +33.8% | 0 |

## 2025 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | - | 1-yr: +20.7% (45) | - | - | +20.8% | - |
| EPS anchor $1.30 (2025-01-03 to 2025-01-31) | 5 | - | 1-yr: +13.2% (5) | - | - | +29.1% | - |
| EPS anchor $1.22 (2025-02-07 to 2025-12-26) | 47 | - | 1-yr: +20.9% (40) | - | - | +20.2% | - |
| latest print Q3 2024 (2025-01-03 to 2025-01-31) | 5 | - | 1-yr: +13.2% (5) | - | - | +29.1% | - |
| latest print Q4 2024 (2025-02-07 to 2025-05-02) | 13 | - | 1-yr: +30.2% (13) | - | - | +32.8% | - |
| latest print Q1 2025 (2025-05-09 to 2025-08-01) | 13 | - | 1-yr: +12.2% (13) | - | - | +13.6% | - |
| latest print Q2 2025 (2025-08-08 to 2025-10-31) | 13 | - | 1-yr: +16.4% (13) | - | - | +15.2% | - |
| latest print Q3 2025 (2025-11-06 to 2025-12-26) | 8 | - | 1-yr: +26.7% (1) | - | - | +16.2% | - |

## 2026 (39 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 39 | - | 1-yr: - (0) | - | - | - | - |
| EPS anchor $1.22 (2026-01-02 to 2026-01-30) | 5 | - | 1-yr: - (0) | - | - | - | - |
| EPS anchor $1.75 (2026-02-05 to 2026-09-25) | 34 | - | 1-yr: - (0) | - | - | - | - |
| latest print Q3 2025 (2026-01-02 to 2026-01-30) | 5 | - | 1-yr: - (0) | - | - | - | - |
| latest print Q4 2025 (2026-02-05 to 2026-05-01) | 13 | - | 1-yr: - (0) | - | - | - | - |
| latest print Q1 2026 (2026-05-07 to 2026-07-24) | 12 | - | 1-yr: - (0) | - | - | - | - |
| latest print Q2 2026 (2026-07-31 to 2026-09-25) | 9 | - | 1-yr: - (0) | - | - | - | - |

## Across the series

| Group | Dates | Mean 2-yr total return | Mean 2-yr excess vs SPY | Mean m12-24 avg price | Call held |
|---|---|---|---|---|---|
| class CHEAP | 77 | +13.6% | -31.6pp | +5.4% | 22 of 77 |
| class FAIR | 24 | +15.7% | -25.2pp | +0.0% | 9 of 24 |
| class RICH | 194 (96 with 2 yrs, 148 with m12-24) | +32.0% | +12.5pp | +27.6% | 13 of 96 |

- **The calls ran backwards.** 44 of 197 two-year calls held (22%). The 96 RICH dates with two years returned a mean +32.0% and beat SPY
  by a mean +12.5pp; the 77 CHEAP dates returned +13.6% and trailed SPY by 31.6pp; FAIR's 24 returned +15.7% and trailed by 25.2pp. The
  one-year and m12-24 readings agree: RICH +24.1% and +27.6%, CHEAP +2.6% and +5.4%, FAIR -4.6% and 0.0%.
- **The class followed the GAAP anchor, and the anchor swung with items the company itself excludes.** 2021 was RICH on FY20's $0.98 (43-50x),
  and the stock beat SPY on 43 of 48 dates. 2022 was CHEAP on FY21's $2.44 (21-28x): none of the 46 CHEAP dates cleared the hurdle or beat
  SPY (median -1.6% over two years). 2024-2025 were RICH on FY23's $1.30 and FY24's $1.22 (39-63x), and the 2024 dates returned a median
  +47.8% over two years, beating SPY on 34 of 48. GAAP EPS halved from 2021 to 2024 while the company's Operating EPS rose by a fifth.
  Hypothesis, not a rule: for a company whose GAAP earnings carry large recurring purchase-accounting amortization and pension credits,
  the GAAP anchor can invert the class; test on other tickers and periods (an amortization-heavy history read both ways), never fit to
  CTVA's outcomes.
- **The Operating EPS reading, scored in hindsight.** Of the 129 dates the Operating EPS sensitivity re-classes, 86 have a two-year
  outcome: the variant's call held on 52 of them and the GAAP call on 18 (RICH to CHEAP: 22 of 24 against 2; CHEAP to RICH: 14 of 14
  against 0; RICH to FAIR: 11 of 12 against 7; FAIR to CHEAP: 3 of 22 against 9; CHEAP to FAIR: 0 of 12 against 0). This is the
  sensitivity's own outcome and must not change the archive's rule: a rule change is a new method version, decided before scoring and
  tested out of sample, and this evidence is one stock in one cycle.
- **Every valuation reading ranked the wrong way.** Across the 249 dates with an m12-24 average, the return to it ranks against the proxy
  composite at Spearman -0.42, the adjusted gap at -0.59 and Ratio B at +0.42 (all the wrong sign), the EPP gap at +0.14 and the entry
  price at -0.56 (buying lower helped, as usual).
- **The two-year price landed nearest BASE on 103 of 197 dates,** XBULL on 52, BULL on 29 and BEAR on 13; the median drawdown within two
  years was -24.0%. The EPP floor sat under the price on every date and the price never fell to it.
- **One stock, one agricultural cycle.** The dates span a crop-price boom (2021-2022), a crop protection destocking (2023-2024, the Q2 2023
  cut and the 2023-10-27 update) and a recovery with the separation announced (2025). The result mostly tests the EPS basis, not stock
  selection; it needs other agriculture and amortization-heavy names on the same dates.
