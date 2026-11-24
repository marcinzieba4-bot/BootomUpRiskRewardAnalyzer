# UNH retrospective findings (hindsight)

Patterns seen in `outcome.json` for the UNH weekly dates: 105, from 2008-01-04 to 2009-12-31, all UnitedHealth Group Incorporated (NYSE:
UNH). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build, validation, README section and firewall result were committed and pushed (95bb426, the builder fix the firewall's first
run needed 36eb1c4, firewall result 4a203a3); the outcomes were computed on 2026-11-24. Every date has its 6-month, 1-, 2- and 3-year
horizons (the last ends 2012-12-28). Total returns include the dividends (the annual $0.03 to the ex-date of 2010-04-01, then quarterly:
$0.125 from 2010-06-03, $0.163 from 2011-06-03, $0.213 from 2012-06-13). No split falls in any horizon, so every price is as traded.
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1%
over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY). Every date was CHEAP and BUY, so the
tables test that one call against the calendar.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | +6.9% | -43.6% to +111.7% | 16 | 36 | -1.0% | 38 |
| FY07E $3.495 (2008-01-04 to 2008-01-18) | 3 | -41.0% | -43.6% to -37.8% | 0 | 0 | -52.9% | 0 |
| FY08E $3.975 (2008-01-23 to 2008-04-18) | 13 | -25.2% | -34.0% to -2.5% | 0 | 3 | -39.3% | 3 |
| FY08E $3.575 (2008-04-23 to 2008-06-27) | 10 | -7.6% | -17.2% to +16.2% | 0 | 9 | -11.4% | 8 |
| FY08E $3 (2008-07-03 to 2008-11-28) | 22 | +36.1% | -2.4% to +111.7% | 11 | 22 | +28.6% | 22 |
| FY08E $2.965 (2008-12-05 to 2008-12-31) | 5 | +37.7% | +34.0% to +78.7% | 5 | 2 | +25.1% | 5 |
| latest print Q3 2007 (2008-01-04 to 2008-01-18) | 3 | -41.0% | -43.6% to -37.8% | 0 | 0 | -52.9% | 0 |
| latest print Q4 2007 (2008-01-23 to 2008-04-18) | 13 | -25.2% | -34.0% to -2.5% | 0 | 3 | -39.3% | 3 |
| latest print Q1 2008 (2008-04-23 to 2008-07-18) | 13 | -5.8% | -17.2% to +36.1% | 1 | 12 | -9.9% | 11 |
| latest print Q2 2008 (2008-07-23 to 2008-10-10) | 12 | +17.5% | -2.4% to +99.8% | 3 | 12 | +7.9% | 12 |
| latest print Q3 2008 (2008-10-17 to 2008-12-31) | 12 | +64.0% | +34.0% to +111.7% | 12 | 9 | +39.2% | 12 |

- **CHEAP failed on 15 dates, all from 2008-01-04 to 2008-05-23, and held on the other 90.** The January 2008 entries ($54.40-56.00,
  15.6-16.0x the FY2007 guide) returned -43.6% to -37.8% over two years, the dates on the FY2008 guide of $3.975 (2008-01-23 to 2008-04-18,
  $34.40-50.35, 8.7-12.7x) -34.0% to -2.5%: 13 of these 16 lagged SPY (all but 2008-03-20, 2008-03-28 and 2008-04-04) and none cleared the
  hurdle; the other two misses are 2008-04-23 and 2008-05-23. From the Q1 2008 print the call held on 35 of 37 dates of 2008, and on
  every 2008 date from 2008-07-03 (FY08E $3.00 and $2.965, $17.15-33.01, 5.7-11.0x), which returned -2.4% to +111.7% (the 22 dates on
  FY08E $3.00: median +36.1%, every one beating SPY). Every 2008 entry sat through a 46-71% drawdown (the low close $16.30 on 2008-11-20); two years on
  the price was $28.30-37.82.
- **The guide fell faster than the price in early 2008.** FY08E went from $3.975 (January) to $3.575 (April), $3.00 (July) and $2.965
  (December), and FY2008 came in at the company's $2.95 (GAAP $2.40): the early-2008 dates were "cheap" on an EPS anchor 35% above what the year
  turned out to be. Once the anchor had been cut to where it ended, the same rules (the decade's 18.5-19.0x median, the 14x EPP floor)
  called a multiple of 6-11x, and those dates' price stood at $28.30-37.82 two years on (8.7-11.7x FY2009's $3.24). Hypothesis, not a rule: a CHEAP call on a guide that is being cut in successive releases (here three cuts in
  six months, each with a lower margin guide) is weaker than one on a guide that has stopped falling; method r2 reads each guide as it
  stands. Test it on other tickers and periods with repeated guide cuts, never fit it to UNH.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +83.5% | +45.7% to +151.5% | 52 | 46 | +53.7% | 52 |
| FY08E $2.965 (2009-01-09 to 2009-01-16) | 2 | +61.6% | +47.0% to +61.6% | 2 | 1 | +30.3% | 2 |
| FY09E $3.025 (2009-01-23 to 2009-07-17) | 26 | +106.5% | +45.7% to +151.5% | 26 | 21 | +57.6% | 26 |
| FY09E $3.075 (2009-07-22 to 2009-10-16) | 13 | +79.3% | +52.2% to +105.5% | 13 | 13 | +51.2% | 13 |
| FY09E $3.15 (2009-10-21 to 2009-12-31) | 11 | +65.0% | +51.2% to +94.2% | 11 | 11 | +54.5% | 11 |
| latest print Q3 2008 (2009-01-09 to 2009-01-16) | 2 | +61.6% | +47.0% to +61.6% | 2 | 1 | +30.3% | 2 |
| latest print Q4 2008 (2009-01-23 to 2009-04-17) | 13 | +88.5% | +45.7% to +151.5% | 13 | 8 | +48.6% | 13 |
| latest print Q1 2009 (2009-04-22 to 2009-07-17) | 13 | +106.5% | +75.4% to +125.1% | 13 | 13 | +57.6% | 13 |
| latest print Q2 2009 (2009-07-22 to 2009-10-16) | 13 | +79.3% | +52.2% to +105.5% | 13 | 13 | +51.2% | 13 |
| latest print Q3 2009 (2009-10-21 to 2009-12-31) | 11 | +65.0% | +51.2% to +94.2% | 11 | 11 | +54.5% | 11 |

- **CHEAP held on all 52 dates of 2009.** From $17.90-31.68 (5.9-10.1x FY09E) the 2009 entries returned +45.7% to +151.5% over two years
  and +78.9% to +211.0% over three, all clearing both hurdles and 46 beating SPY over two years (all 52 over three). FY2009 came in at $3.24
  (the Q4 2009 release, 2010-01-21, outside the series) against the $3.025-3.15 the models used, and two years on the price was
  $38.45-53.13.

Across the 105 dates:
- **Entry price explains most of the result.** The correlation of the entry price with the two-year total return is -0.81; the ten lowest
  entries (2008-10-10 to 2009-04-03, $17.15-21.36) returned a median +110.2%. One stock over two years mostly tests "buy lower" (retro/README.md,
  "Scoring a single stock"): judge the series by `return_to_avg_price_m12_m24_pct` (median -1.0% for 2008, +53.7% for 2009).
- **The BEAR and BASE scenarios bracketed the outcome; BULL never came.** The two-year price landed nearest the BEAR case on 46 dates
  (33 of 2008) and the BASE case on 59; never near BULL or XBULL, whose +25-39%/yr EPS paths (the 1997-2007 compounding) did not recur. The
  price went under the EPP floor within two years on every date (on most 2008-2009 dates it already was).
- **The signals added little.** The proxy composite was 1.80-2.45 on every date (premium growth at BEAR through Q2 2008, the settlement
  quarter's operating cost ratio at BEAR); the verdict came from the valuation and the EPP distance, as the BEAR- and XBULL-signal
  sensitivity runs showed before any outcome (no class moves either way).
- **Profile drift:** the kind (DURABLE, risk 2) matches today's profile, which records a later regulatory probe and Medicare Advantage
  exits (a 2026 analysis, read here only through `profile_drift`).
