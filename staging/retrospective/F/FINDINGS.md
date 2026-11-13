# F retrospective findings (hindsight)

Patterns seen in `outcome.json` for the F weekly dates: 253 from 2022-01-07 to 2026-11-06 (Ford Motor Company, NYSE: F). They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. The point-in-time build was committed and pushed
(494f7fec7, then the README's firewall result in bff2caa67) before any outcome was computed. Outcomes were computed on 2026-11-13 from
the closes posted to 2026-11-09 (the session ran during the 2026-11-13 trading day). 149 dates have a two-year horizon (to 2024-11-08),
201 a one-year horizon and 97 a three-year horizon; for dates after 2024-11 the m12-24 average covers only the months that have passed.
Total returns include the regular $0.10 and $0.15 dividends and the supplemental $0.65, $0.18 and $0.15 (paid with the first-quarter
dividends of 2023-2025); no split falls in a horizon. Medians of an even count take the upper middle value (`statistics.median_high`).
The 15%/yr hurdle is +32.2% over two years and +15.0% over one. "Call held" is `call_check_2y`, the class's test (a tier row counts the
class calls on its dates): CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of it, and RICH should
miss the hurdle and lag it.

**Hindsight the model could not see:** over these windows SPY's median two-year total return was +42.7% and Ford's +5.3%. Ford's
adjusted EPS peaked at $2.01 (2023) and fell to $1.09 (2025, a year of tariffs and EV program charges); the stock spent 2023-2025 between
roughly $9 and $15 and rose in 2026.

## What the outcomes say (hypotheses)

- **The classes rank in the right order on two-year total return, and only that.** CHEAP +7.5% (87 dates), FAIR +5.3% (51), RICH -20.8%
  (11). The RICH calls with an outcome are all early 2022 and all held; the CHEAP calls cleared the hurdle on 19 of 87 dates and beat SPY
  on 7. Against the benchmark nearly every call to own Ford lost.
- **The January 2022 RICH calls were right for a mechanical reason.** They rest on FY20's $0.41, a COVID-year anchor (48-61x); the stock
  then fell 33-48% in two years. A builder should not read this as skill: a sounder anchor would have given a lower multiple at the same
  price. The rollover rule makes the first weeks after a depressed year read RICH whatever the business does.
- **"Cheap stayed cheap" in 2022-2023.** The 2023 dates were CHEAP on 48 of 52 at 5-8x FY22's $1.88; their median two-year return was
  +2.3%, 7 cleared the hurdle (all after the Q3 2023 print, entered at $9.86-11.01) and none beat SPY. The anchor did
  not grow: FY23 $2.01, FY24 $1.84, FY25 $1.09. A low multiple of a peak-ish anchor is the value-trap pattern; whether a cyclical label
  or a growth test should temper CHEAP for an automaker is a question for the live model, not this archive.
- **Entry price explains more than the class.** By the price on the date: below $11, +39.3% median over two years (17 dates); $11-13,
  +11.0% (81); $13-15, -5.4% (28); above $15, -18.2% (23). One stock over a few years mostly tests "buy lower" (README, "Scoring a single
  stock").
- **2024 CHEAP was the best set:** +35.8% median two-year return on 18 dates, 11 clearing the hurdle and 7 beating SPY, entered at
  $10.03-11.85 (January 2024, then from the Q2 2024 print to November) and ending in the 2026 rise.
- **The 2025 RICH calls missed on one year.** 27 of the 52 dates of 2025 are RICH (BULL turned flat or negative as the anchor fell to
  FY24's $1.84 and the decade CAGR went negative); 20 have a one-year outcome, with a median of +27.9% and 14 clearing the 15% hurdle. The
  RICH reading there came from the scenario arithmetic (Ratio B above 1 with BULL near the price), not from a high multiple (5-8x).
- **Robustness did not separate good calls from bad:** the dates where all eight variants agree have a median two-year return of +0.9%,
  those with five or fewer +6.9%.
- **The 2026 dates (all RICH on FY25's $1.09 at 10-16x) have no outcome yet.**

Hypotheses for the live model (not for this archive): an automaker's anchor year should be tested against its own cycle before a low
multiple reads CHEAP; a negative decade EPS CAGR makes BULL collapse onto BASE and turns Ratio B mechanical; the first weeks after a
crisis year need a sounder anchor than the crisis year itself.


## 2022 (52 dates)

| Group | Dates | With 2y | Median 2y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 21 | 21 | +5.0% | -26.5% to +36.9% | 1 | 0 | -3.8% | 1 |
| class FAIR | 22 | 22 | -1.8% | -16.0% to +26.0% | 0 | 0 | -13.6% | 0 |
| class RICH | 9 | 9 | -23.2% | -47.6% to -7.5% | 0 | 0 | -32.5% | 9 |
| legacy tier BUY | 16 | 16 | +2.6% | -26.5% to +30.7% | 0 | 0 | -4.2% | 0 |
| legacy tier ACCUMULATE | 12 | 12 | +6.4% | +1.2% to +36.9% | 1 | 0 | -3.7% | 1 |
| legacy tier WATCHLIST | 19 | 19 | -8.3% | -23.2% to +2.3% | 0 | 0 | -20.9% | 4 |
| legacy tier AVOID | 5 | 5 | -37.3% | -47.6% to -7.5% | 0 | 0 | -40.6% | 5 |
| FY2021E on FY20's (2022-01-07 to 2022-01-28) | 4 | 4 | -37.3% | -47.6% to -33.3% | 0 | 0 | -40.6% | 4 |
| FY2022E on FY21's (2022-02-04 to 2022-12-30) | 48 | 48 | -1.8% | -26.5% to +36.9% | 1 | 0 | -13.6% | 6 |
| latest print Q3 2021 (2022-01-07 to 2022-01-28) | 4 | 4 | -37.3% | -47.6% to -33.3% | 0 | 0 | -40.6% | 4 |
| latest print Q4 2021 (2022-02-04 to 2022-04-22) | 12 | 12 | -12.2% | -23.2% to +2.3% | 0 | 0 | -26.6% | 4 |
| latest print Q1 2022 (2022-04-29 to 2022-07-22) | 13 | 13 | +13.4% | +1.2% to +36.9% | 1 | 0 | -3.7% | 1 |
| latest print Q2 2022 (2022-07-29 to 2022-10-21) | 13 | 13 | -12.8% | -26.5% to +12.4% | 0 | 0 | -19.7% | 0 |
| latest print Q3 2022 (2022-10-28 to 2022-12-30) | 10 | 10 | -4.2% | -8.3% to +5.0% | 0 | 0 | -11.9% | 1 |
| robustness 8 of 8 | 17 | 17 | -14.7% | -47.6% to +12.4% | 0 | 0 | -21.6% | 4 |
| robustness 7 of 8 | 12 | 12 | +13.4% | -12.2% to +36.9% | 1 | 0 | -1.6% | 1 |
| robustness 6 of 8 | 6 | 6 | +2.4% | -16.0% to +5.0% | 0 | 0 | -13.4% | 0 |
| robustness 5 or fewer of 8 | 17 | 17 | -4.6% | -23.2% to +26.0% | 0 | 0 | -13.4% | 5 |

| Group | Dates | With 1y | Median 1y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 21 | 21 | +8.6% | -17.2% to +44.7% | 8 | 6 | -3.8% | - |
| class FAIR | 22 | 22 | -11.4% | -25.9% to +18.4% | 2 | 2 | -13.6% | - |
| class RICH | 9 | 9 | -26.6% | -47.5% to -20.6% | 0 | 0 | -32.5% | - |
| legacy tier BUY | 16 | 16 | +5.7% | -17.2% to +44.7% | 4 | 4 | -4.2% | - |
| legacy tier ACCUMULATE | 12 | 12 | +15.6% | -7.3% to +36.6% | 6 | 4 | -3.7% | - |
| legacy tier WATCHLIST | 19 | 19 | -17.1% | -26.6% to +9.5% | 0 | 0 | -20.9% | - |
| legacy tier AVOID | 5 | 5 | -37.5% | -47.5% to -22.3% | 0 | 0 | -40.6% | - |

## 2023 (52 dates)

| Group | Dates | With 2y | Median 2y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 48 | 48 | +2.3% | -18.2% to +49.0% | 7 | 0 | -11.6% | 7 |
| class FAIR | 4 | 4 | -5.0% | -7.7% to -1.5% | 0 | 0 | -7.7% | 0 |
| class RICH | 0 | 0 | - | - | - | - | - | - |
| legacy tier BUY | 13 | 13 | +0.9% | -8.4% to +49.0% | 2 | 0 | -7.2% | 2 |
| legacy tier ACCUMULATE | 31 | 31 | +4.4% | -17.8% to +40.3% | 5 | 0 | -13.0% | 5 |
| legacy tier WATCHLIST | 8 | 8 | -1.5% | -18.2% to +26.3% | 0 | 0 | -8.9% | 0 |
| legacy tier AVOID | 0 | 0 | - | - | - | - | - | - |
| FY2022E on FY21's (2023-01-06 to 2023-01-27) | 4 | 4 | -5.0% | -7.7% to -1.5% | 0 | 0 | -7.7% | 0 |
| FY2023E on FY22's (2023-02-03 to 2023-12-29) | 48 | 48 | +2.3% | -18.2% to +49.0% | 7 | 0 | -11.6% | 7 |
| latest print Q3 2022 (2023-01-06 to 2023-01-27) | 4 | 4 | -5.0% | -7.7% to -1.5% | 0 | 0 | -7.7% | 0 |
| latest print Q4 2022 (2023-02-03 to 2023-04-28) | 13 | 13 | -9.9% | -17.8% to +2.3% | 0 | 0 | -10.1% | 0 |
| latest print Q1 2023 (2023-05-04 to 2023-07-21) | 12 | 12 | -7.8% | -18.2% to +5.4% | 0 | 0 | -22.8% | 0 |
| latest print Q2 2023 (2023-07-28 to 2023-10-20) | 13 | 13 | +8.6% | -4.5% to +18.6% | 0 | 0 | -14.2% | 0 |
| latest print Q3 2023 (2023-10-27 to 2023-12-29) | 10 | 10 | +38.8% | +21.4% to +49.0% | 7 | 0 | +2.7% | 7 |
| robustness 8 of 8 | 18 | 18 | +3.5% | -8.4% to +49.0% | 7 | 0 | -3.3% | 7 |
| robustness 7 of 8 | 28 | 28 | -4.5% | -18.2% to +26.3% | 0 | 0 | -13.8% | 0 |
| robustness 6 of 8 | 2 | 2 | +21.5% | +21.4% to +21.5% | 0 | 0 | -9.0% | 0 |
| robustness 5 or fewer of 8 | 4 | 4 | -5.0% | -7.7% to -1.5% | 0 | 0 | -7.7% | 0 |

| Group | Dates | With 1y | Median 1y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 48 | 48 | +2.1% | -17.3% to +19.2% | 4 | 0 | -11.6% | - |
| class FAIR | 4 | 4 | +0.4% | -4.7% to +4.1% | 0 | 0 | -7.7% | - |
| class RICH | 0 | 0 | - | - | - | - | - | - |
| legacy tier BUY | 13 | 13 | +12.1% | +4.2% to +19.2% | 3 | 0 | -7.2% | - |
| legacy tier ACCUMULATE | 31 | 31 | -1.1% | -17.3% to +15.0% | 1 | 0 | -13.0% | - |
| legacy tier WATCHLIST | 8 | 8 | -4.7% | -13.7% to +4.1% | 0 | 0 | -8.9% | - |
| legacy tier AVOID | 0 | 0 | - | - | - | - | - | - |

## 2024 (52 dates)

| Group | Dates | With 2y | Median 2y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 23 | 18 | +35.8% | +24.3% to +59.8% | 11 | 7 | +23.9% | 11 |
| class FAIR | 27 | 25 | +19.5% | -4.2% to +54.9% | 4 | 1 | -1.5% | 10 |
| class RICH | 2 | 2 | +11.4% | +9.4% to +11.4% | 0 | 0 | -7.9% | 2 |
| legacy tier BUY | 0 | 0 | - | - | - | - | - | - |
| legacy tier ACCUMULATE | 15 | 12 | +35.8% | +26.6% to +59.8% | 8 | 5 | +24.4% | 8 |
| legacy tier WATCHLIST | 33 | 29 | +24.0% | -0.3% to +54.9% | 7 | 3 | +1.3% | 13 |
| legacy tier AVOID | 4 | 4 | +9.4% | -4.2% to +11.4% | 0 | 0 | -8.6% | 2 |
| FY2023E on FY22's (2024-01-05 to 2024-02-02) | 5 | 5 | +31.4% | +26.4% to +35.8% | 2 | 0 | -2.0% | 2 |
| FY2024E on FY23's (2024-02-08 to 2024-12-27) | 47 | 40 | +24.3% | -4.2% to +59.8% | 13 | 8 | +2.4% | 21 |
| latest print Q3 2023 (2024-01-05 to 2024-02-02) | 5 | 5 | +31.4% | +26.4% to +35.8% | 2 | 0 | -2.0% | 2 |
| latest print Q4 2023 (2024-02-08 to 2024-04-19) | 11 | 11 | +10.8% | -4.2% to +25.8% | 0 | 0 | -5.5% | 3 |
| latest print Q1 2024 (2024-04-26 to 2024-07-19) | 13 | 13 | +20.1% | +6.4% to +54.9% | 4 | 1 | +1.3% | 8 |
| latest print Q2 2024 (2024-07-26 to 2024-10-25) | 14 | 14 | +39.8% | +17.0% to +59.8% | 9 | 7 | +24.4% | 10 |
| latest print Q3 2024 (2024-10-30 to 2024-12-27) | 9 | 2 | +29.9% | +24.3% to +29.9% | 0 | 0 | +27.4% | 0 |
| robustness 8 of 8 | 3 | 1 | +59.8% | +59.8% to +59.8% | 1 | 1 | +29.7% | 1 |
| robustness 7 of 8 | 19 | 16 | +31.4% | +9.4% to +50.9% | 7 | 4 | +23.9% | 9 |
| robustness 6 of 8 | 3 | 3 | +39.8% | +36.1% to +40.5% | 3 | 2 | +16.9% | 3 |
| robustness 5 or fewer of 8 | 27 | 25 | +19.5% | -4.2% to +54.9% | 4 | 1 | -1.5% | 10 |

| Group | Dates | With 1y | Median 1y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 23 | 23 | +16.3% | -10.0% to +43.9% | 14 | 9 | +24.4% | - |
| class FAIR | 27 | 27 | -10.5% | -22.2% to +31.8% | 3 | 3 | -0.5% | - |
| class RICH | 2 | 2 | -10.7% | -14.8% to -10.7% | 0 | 0 | -7.9% | - |
| legacy tier BUY | 0 | 0 | - | - | - | - | - | - |
| legacy tier ACCUMULATE | 15 | 15 | +16.3% | -10.0% to +43.9% | 10 | 5 | +24.8% | - |
| legacy tier WATCHLIST | 33 | 33 | -7.9% | -21.9% to +31.9% | 7 | 7 | +1.8% | - |
| legacy tier AVOID | 4 | 4 | -14.8% | -22.2% to -10.7% | 0 | 0 | -8.6% | - |

## 2025 (52 dates)

| Group | Dates | With 2y | Median 2y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 15 | 0 | - | - | - | - | - | - |
| class FAIR | 10 | 0 | - | - | - | - | - | - |
| class RICH | 27 | 0 | - | - | - | - | - | - |
| legacy tier BUY | 0 | 0 | - | - | - | - | - | - |
| legacy tier ACCUMULATE | 8 | 0 | - | - | - | - | - | - |
| legacy tier WATCHLIST | 11 | 0 | - | - | - | - | - | - |
| legacy tier AVOID | 33 | 0 | - | - | - | - | - | - |
| FY2024E on FY23's (2025-01-03 to 2025-01-31) | 5 | 0 | - | - | - | - | - | - |
| FY2025E on FY24's (2025-02-07 to 2025-12-26) | 47 | 0 | - | - | - | - | - | - |
| latest print Q3 2024 (2025-01-03 to 2025-01-31) | 5 | 0 | - | - | - | - | - | - |
| latest print Q4 2024 (2025-02-07 to 2025-05-02) | 13 | 0 | - | - | - | - | - | - |
| latest print Q1 2025 (2025-05-07 to 2025-07-25) | 12 | 0 | - | - | - | - | - | - |
| latest print Q2 2025 (2025-08-01 to 2025-10-17) | 12 | 0 | - | - | - | - | - | - |
| latest print Q3 2025 (2025-10-24 to 2025-12-26) | 10 | 0 | - | - | - | - | - | - |
| robustness 8 of 8 | 2 | 0 | - | - | - | - | - | - |
| robustness 7 of 8 | 26 | 0 | - | - | - | - | - | - |
| robustness 6 of 8 | 17 | 0 | - | - | - | - | - | - |
| robustness 5 or fewer of 8 | 7 | 0 | - | - | - | - | - | - |

| Group | Dates | With 1y | Median 1y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 15 | 15 | +41.4% | +23.1% to +58.4% | 15 | 14 | +37.9% | - |
| class FAIR | 10 | 10 | +28.8% | +11.9% to +51.1% | 9 | 6 | +31.1% | - |
| class RICH | 27 | 20 | +27.9% | -11.8% to +73.8% | 14 | 13 | +12.6% | - |
| legacy tier BUY | 0 | 0 | - | - | - | - | - | - |
| legacy tier ACCUMULATE | 8 | 8 | +45.1% | +36.4% to +57.5% | 8 | 8 | +37.9% | - |
| legacy tier WATCHLIST | 11 | 11 | +28.8% | +21.2% to +58.4% | 11 | 8 | +36.2% | - |
| legacy tier AVOID | 33 | 26 | +27.9% | -11.8% to +73.8% | 19 | 17 | +12.7% | - |

## 2026 (45 dates)

| Group | Dates | With 2y | Median 2y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 0 | 0 | - | - | - | - | - | - |
| class FAIR | 0 | 0 | - | - | - | - | - | - |
| class RICH | 45 | 0 | - | - | - | - | - | - |
| legacy tier BUY | 0 | 0 | - | - | - | - | - | - |
| legacy tier ACCUMULATE | 0 | 0 | - | - | - | - | - | - |
| legacy tier WATCHLIST | 0 | 0 | - | - | - | - | - | - |
| legacy tier AVOID | 45 | 0 | - | - | - | - | - | - |
| FY2025E on FY24's (2026-01-02 to 2026-02-06) | 6 | 0 | - | - | - | - | - | - |
| FY2026E on FY25's (2026-02-12 to 2026-11-06) | 39 | 0 | - | - | - | - | - | - |
| latest print Q3 2025 (2026-01-02 to 2026-02-06) | 6 | 0 | - | - | - | - | - | - |
| latest print Q4 2025 (2026-02-12 to 2026-04-24) | 11 | 0 | - | - | - | - | - | - |
| latest print Q1 2026 (2026-05-01 to 2026-07-24) | 13 | 0 | - | - | - | - | - | - |
| latest print Q2 2026 (2026-07-30 to 2026-10-23) | 13 | 0 | - | - | - | - | - | - |
| latest print Q3 2026 (2026-10-30 to 2026-11-06) | 2 | 0 | - | - | - | - | - | - |
| robustness 8 of 8 | 39 | 0 | - | - | - | - | - | - |
| robustness 7 of 8 | 6 | 0 | - | - | - | - | - | - |
| robustness 6 of 8 | 0 | 0 | - | - | - | - | - | - |
| robustness 5 or fewer of 8 | 0 | 0 | - | - | - | - | - | - |

| Group | Dates | With 1y | Median 1y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 0 | 0 | - | - | - | - | - | - |
| class FAIR | 0 | 0 | - | - | - | - | - | - |
| class RICH | 45 | 0 | - | - | - | - | - | - |
| legacy tier BUY | 0 | 0 | - | - | - | - | - | - |
| legacy tier ACCUMULATE | 0 | 0 | - | - | - | - | - | - |
| legacy tier WATCHLIST | 0 | 0 | - | - | - | - | - | - |
| legacy tier AVOID | 45 | 0 | - | - | - | - | - | - |

## All dates

| Group | Dates | With 2y | Median 2y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 107 | 87 | +7.5% | -26.5% to +59.8% | 19 | 7 | -7.9% | 19 |
| class FAIR | 63 | 51 | +5.3% | -16.0% to +54.9% | 4 | 1 | -7.7% | 10 |
| class RICH | 83 | 11 | -20.8% | -47.6% to +11.4% | 0 | 0 | -32.0% | 11 |
| legacy tier BUY | 29 | 29 | +0.9% | -26.5% to +49.0% | 2 | 0 | -7.2% | 2 |
| legacy tier ACCUMULATE | 66 | 55 | +9.6% | -17.8% to +59.8% | 14 | 5 | -9.7% | 14 |
| legacy tier WATCHLIST | 71 | 56 | +8.0% | -23.2% to +54.9% | 7 | 3 | -5.8% | 17 |
| legacy tier AVOID | 87 | 9 | -7.5% | -47.6% to +11.4% | 0 | 0 | -19.2% | 7 |
| FY2021E on FY20's (2022-01-07 to 2022-01-28) | 4 | 4 | -37.3% | -47.6% to -33.3% | 0 | 0 | -40.6% | 4 |
| FY2022E on FY21's (2022-02-04 to 2023-01-27) | 52 | 52 | -4.2% | -26.5% to +36.9% | 1 | 0 | -13.4% | 6 |
| FY2023E on FY22's (2023-02-03 to 2024-02-02) | 53 | 53 | +4.4% | -18.2% to +49.0% | 9 | 0 | -10.6% | 9 |
| FY2024E on FY23's (2024-02-08 to 2025-01-31) | 52 | 40 | +24.3% | -4.2% to +59.8% | 13 | 8 | +2.4% | 21 |
| FY2025E on FY24's (2025-02-07 to 2026-02-06) | 53 | 0 | - | - | - | - | - | - |
| FY2026E on FY25's (2026-02-12 to 2026-11-06) | 39 | 0 | - | - | - | - | - | - |
| robustness 8 of 8 | 79 | 36 | +0.9% | -47.6% to +59.8% | 8 | 1 | -7.2% | 12 |
| robustness 7 of 8 | 91 | 56 | +9.6% | -18.2% to +50.9% | 8 | 4 | -11.6% | 10 |
| robustness 6 of 8 | 28 | 11 | +5.0% | -16.0% to +40.5% | 3 | 2 | -9.0% | 3 |
| robustness 5 or fewer of 8 | 55 | 46 | +6.9% | -23.2% to +54.9% | 4 | 1 | -5.7% | 15 |

| Group | Dates | With 1y | Median 1y total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|---|
| class CHEAP | 107 | 107 | +11.1% | -17.3% to +58.4% | 41 | 29 | -1.6% | - |
| class FAIR | 63 | 63 | -7.9% | -25.9% to +51.1% | 14 | 11 | -5.1% | - |
| class RICH | 83 | 31 | +9.3% | -47.5% to +73.8% | 14 | 13 | +1.3% | - |
| legacy tier BUY | 29 | 29 | +9.4% | -17.2% to +44.7% | 7 | 4 | -7.2% | - |
| legacy tier ACCUMULATE | 66 | 66 | +3.2% | -17.3% to +57.5% | 25 | 17 | -3.7% | - |
| legacy tier WATCHLIST | 71 | 71 | -8.0% | -26.6% to +58.4% | 18 | 15 | -2.9% | - |
| legacy tier AVOID | 87 | 35 | +18.8% | -47.5% to +73.8% | 19 | 17 | +6.6% | - |

## F 2008-2011 (hindsight)

Patterns seen in `outcome.json` for the 209 weekly dates from 2008-01-04 to 2011-12-30. **Labels and hypotheses**: never feed them back into
the method or the fact sheet. The point-in-time build (3d3e2d059) and the README's decisions, controls, leak scan and firewall result
(a296995b4) were committed before any of these outcomes was computed (2026-11-13). Every date has one-, two- and three-year horizons. The
dividend reinstated in December 2011 ($0.05 a quarter) is in the total returns of the 2010-2011 dates; no split falls in a horizon. Medians of an
even count take the upper middle value. The hurdle is +32.2% over two years; "call held" is `call_check_2y` (`hit`).

**Hindsight the model could not see:** Ford took no government bridge loan and did not file for bankruptcy; the stock fell to $1.43 (2008
close, among these dates) and $1.58 (2009), rose to $18.65 by January 2011 and ended 2011 near $10. SPY's median two-year total return over
these windows was +25.5%; Ford's +50.1%.

- **The classes rank in the right order, and two of three held.** Two-year median total return: CHEAP +70.3% (160 dates; held 121, cleared
  the hurdle on 119, beat SPY on 119), FAIR -8.8% (29; held 8), RICH -25.4% (20; held 19). Legacy tiers in the same order: BUY +79.8% (146),
  ACCUMULATE +13.1% (13), WATCHLIST -8.9% (30), AVOID -25.4% (20).
- **2008-2009: CHEAP on 96 of 105 dates, all 96 held** (+136.1% and +142.7% two-year medians). The anchor was 2005's $1.00, three years
  stale and from before three loss years: the method bought a loss-making automaker at 1.4-10x a pre-crisis figure, and it paid because Ford
  survived. **That is a survivor's result.** The same rule on an automaker that went bankrupt in 2009 would have read CHEAP as well; F alone
  cannot test the rule, only show that it does not protect against a stale anchor. Do not read the 2008 calls as skill.
- **2010: the stale anchor cut the other way.** On the same $1.00, 10-19x as the price recovered: RICH 16 (all held, -26.1%), FAIR 21 (1 held,
  -13.0%), CHEAP 15 (none held, -7.5%). Every 2010 entry lost over two years whatever its class; the classes still ranked in order.
- **2011: CHEAP on 49 of 52 at 5-8.6x FY10's $1.91** (from the Q4 2010 print): two-year median +31.0%, 25 held (24 cleared the hurdle, 23 beat
  SPY), but the m12-24 average price was -6.3%: the stock fell through 2011-2012 before recovering, so the result depends on the endpoint.
- **Entry price explains more than the class** (two-year median): below $3, +632.8% (24 dates); $3-6, +151.9% (34); $6-10, +63.9% (49);
  $10-14, +3.8% (68); above $14, -15.5% (34). Over one stock and four years that mostly tests "buy lower", as the README warns.
- **What to test elsewhere (never here):** whether an anchor more than two years old should suspend CHEAP and RICH for a cyclical, and whether
  a near-zero year readmitted to the P/E window (2009's $0.01, 158-1,020x) should be capped. Both would be rule changes: a new method version
  and a full re-run, not an edit to this archive.

## F 2012-2014 (hindsight)

Patterns seen in `outcome.json` for the 156 weekly dates from 2012-01-06 to 2014-12-26. **Labels and hypotheses**, never inputs. The build
(1600913fd) and the README's decisions, controls, leak scan, firewall result and class sensitivities (32b893135) were committed before any of
these outcomes was computed (2026-11-13). Every date has one-, two- and three-year horizons; total returns include the $0.05-$0.15 quarterly
dividends paid in them. The hurdle is +32.2% over two years; "call held" is `call_check_2y` (`hit`).

**Hindsight the model could not see:** Ford earned $1.41-1.62 a share excluding special items in 2012-2014 and the stock ranged from about $9 (mid
2012) to about $18 (early 2014); SPY's median two-year total return over these windows was +31.8%, Ford's +0.7%.

- **The classes ranked in order and the calls mostly held.** CHEAP +46.1% two-year median (51 dates, all in 2012; held 42, cleared the hurdle on
  42, beat SPY on 27), FAIR +19.8% (3; held none), RICH -7.3% (102; held 98, lagged SPY on all 102). 140 of 156 calls held.
- **2012 CHEAP at 5.9-9.3x FY11's $1.51 worked;** the entries below $12 cleared the hurdle on every date. 36 of these CHEAP calls (2012-01-27 to
  2013-01-25) depend on 2009's readmitted $0.01 (they read FAIR without it): the call that is mechanically weakest was, here, on the right side.
  That is not evidence for the readmission rule.
- **RICH from 2013 held because the price did not grow into the multiple.** FY12's $1.41 and FY13's $1.62 against $12-18 prices read RICH on 100
  consecutive dates; the 2014 entries lost 11.1% over two years (all 52 held), the 2013 entries were flat (+0.3%). A low decade EPS CAGR made BULL
  small, so Ratio B was large: a stock that is RICH on its own slow EPS history.
- **Entry price again explains the most** (two-year median): below $10 +91.6% (11), $10-12 +47.1% (27), $12-14 +28.7% (32), $14-16 -5.5% (39),
  above $16 -12.0% (47).
- **Across 2008-2014 (hypotheses for elsewhere):** CHEAP, FAIR and RICH ranked two-year returns in order in every year but 2009 (its one RICH
  date gained 120%); in 2010 they ranked in order while every class lost, the stale 2005 anchor reading a recovering stock as RICH and FAIR;
  the near-zero 2009 year distorted the upside scenarios from 2011 on. A rule that caps a
  readmitted near-zero year, or one that suspends the class when the anchor is old, would need a new method version and a full re-run.
