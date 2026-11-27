# SCHW retrospective findings (hindsight)

Patterns seen in `outcome.json` for the SCHW weekly dates: 105, from 2008-01-04 to 2009-12-31, all The Charles Schwab Corporation
(Nasdaq: SCHW). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after
its point-in-time build, validation outputs, README section and firewall result were committed and pushed (076c155, 8c17cc4, 0f13269,
601f677); the outcomes were computed on 2026-11-27. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-31).
Total returns include dividends; no split falls in any horizon, so every price is as traded. Medians of an even count take the upper
middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY). Every date was CHEAP and legacy tier BUY, so these tables test
one call against the calendar and the inputs it rested on.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2008-01-04 to 2008-12-31) | 53 | -15.3% | -43.7% to +14.9% | 0 | 16 | -15.0% | 16 |
| FY07E $0.69 (FY06's) (2008-01-04 to 2008-01-11) | 2 | -13.2% | -15.5% to -13.2% | 0 | 2 | -24.5% | 2 |
| FY08E $0.92 (FY07's) (2008-01-17 to 2008-12-31) | 51 | -15.3% | -43.7% to +14.9% | 0 | 14 | -14.6% | 14 |
| latest print Q3 2007 (2008-01-04 to 2008-01-11) | 2 | -13.2% | -15.5% to -13.2% | 0 | 2 | -24.5% | 2 |
| latest print Q4 2007 (2008-01-17 to 2008-04-11) | 13 | -4.3% | -14.2% to +7.5% | 0 | 12 | -10.1% | 12 |
| latest print Q1 2008 (2008-04-16 to 2008-07-11) | 13 | -22.9% | -29.1% to -3.2% | 0 | 2 | -15.6% | 2 |
| latest print Q2 2008 (2008-07-17 to 2008-10-10) | 13 | -35.3% | -43.7% to -27.3% | 0 | 0 | -24.0% | 0 |
| latest print Q3 2008 (2008-10-16 to 2008-12-31) | 12 | -5.8% | -28.2% to +14.9% | 0 | 0 | -0.4% | 0 |

- **CHEAP held on 16 of the 53 dates of 2008, all on the benchmark and none on the hurdle.** The entries of 2008-01-04 to 2008-04-25
  (but 2008-01-17) returned -15.5% to +7.5% over two years and beat SPY by 0.8 to 14.3pp, SPY's own two-year return being negative on each of
  those dates. From 2008-05-02 every entry lagged SPY (by 0.1 to 64.1pp); those after the Q2 2008 print ($20.20-25.25,
  July to early October 2008) returned -27.3% to -43.7%. Over three years no 2008 entry cleared the hurdle or beat SPY (-49.9% to +4.0%),
  and each sat through a 36-56% drawdown within two years.
- **The current year's EPS was the stale part.** Every 2008 date after the Q4 2007 print read FY08E as FY07's $0.92 (no EPS guide: the
  rollover rule); FY2008 came in at $1.06, so the 2008 multiple was, if anything, overstated. The miss came after: see 2009.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2009-01-09 to 2009-12-31) | 52 | -8.5% | -37.8% to +68.5% | 6 | 0 | -8.0% | 6 |
| FY08E $0.92 (FY07's) (2009-01-09 to 2009-01-09) | 1 | +18.8% | +18.8% to +18.8% | 0 | 0 | +6.0% | 0 |
| FY09E $1.06 (FY08's) (2009-01-16 to 2009-12-31) | 51 | -8.6% | -37.8% to +68.5% | 6 | 0 | -8.1% | 6 |
| latest print Q3 2008 (2009-01-09 to 2009-01-09) | 1 | +18.8% | +18.8% to +18.8% | 0 | 0 | +6.0% | 0 |
| latest print Q4 2008 (2009-01-16 to 2009-04-09) | 13 | +31.6% | +11.0% to +68.5% | 6 | 0 | +16.4% | 6 |
| latest print Q1 2009 (2009-04-16 to 2009-07-10) | 13 | +2.4% | -8.7% to +8.8% | 0 | 0 | -8.1% | 0 |
| latest print Q2 2009 (2009-07-17 to 2009-10-09) | 13 | -30.1% | -37.8% to -4.1% | 0 | 0 | -9.4% | 0 |
| latest print Q3 2009 (2009-10-16 to 2009-12-31) | 12 | -32.4% | -37.7% to -23.1% | 0 | 0 | -13.4% | 0 |

- **CHEAP held on 6 of the 52 dates of 2009, all on the hurdle and none on the benchmark.** The entries of 2009-01-30 and 2009-02-13 to
  2009-03-13, around the series low ($11.36 on 2009-03-06), returned +34.4% to +68.5% over two years, yet trailed SPY's rebound by 15.1 to
  41.7pp. Every 2009 entry lagged SPY over two years (by 15.1 to 60.3pp), and from the Q2 2009 print (2009-07-17 on, $16.60-19.49)
  the two-year returns were -4.1% to -37.8%. Over three years no 2009 entry cleared the 52.1% hurdle or beat SPY (-30.0% to +25.8%).
- **What the 2009 dates assumed, and what came:** FY09E stood at FY08's $1.06 on all 51 dates from the Q4 2008 print, with BEAR at -10.3%/yr
  (the history's one down year, FY2003 to FY2004). FY2009 came in at $0.68 (the Q4 2009 release, 2010-01-19, outside the series: net
  revenues $4,193M, -19%, with $224M of money market fund fee waivers) and FY2010 at $0.38 (the Q4 2010 release, 2011-01-18): -36% and
  then -44%. The two-year price landed in the BEAR band on 101 of the 105 dates and in BASE on 4 (2009-04-16 to 2009-05-08); none above.
- **The signals turned, the class did not.** The proxy composite fell from 2.85 (Q3 and Q4 2007) to 1.80 (Q1 and Q2 2009), client assets
  growth sat at BEAR on the Q4 2008 to Q2 2009 prints, and BASE growth went negative from the Q3 2008 print (-0.3% to -15.9%/yr). But the
  price state rests on the multiple of the last full year's EPS against the 2003-2009 P/E history and the EPP floor on that same EPS, so
  in 2009 the price sat 8-46% under a 20x floor on every date and the call stayed CHEAP. The sensitivity run showed the same: only the
  signals at their BEAR values moved classes (13).
  Hypothesis, not a rule: for an earnings stream tied to short-term interest rates and client asset levels (net interest revenue and
  money market fund fees), the rollover rule ("no guide, the last full year stands") overstates the current year after a collapse in
  rates, and a P/E window and EPS history drawn from a rising-rate period (2003-2008 here) set a BEAR case that cannot see a rate-driven
  earnings fall. Test it on other rate-sensitive financials and periods (as a cross-ticker study), never fit it to SCHW.

## Across the series

- `profile_drift` (hindsight): DURABLE, risk 2 on every date; today's 2026 profile in `data/business_profiles.json` also files SCHW
  DURABLE, risk 2 (its one-line "why" was first seen in an outcome output, after every SCHW model had been built, validated and
  committed). It was never an input.
- Where the series sat against its own floors: under the EPP floor on 12 dates of 2008 and all 51 dates from the Q4 2008 print, and under
  the BEAR case (Ratio B negative) on 13 (2008-12-19 to 2009-03-27). The six hurdle hits of 2009 come from inside that last stretch; the
  dates under the floor after it (April to December 2009) returned -37.8% to +8.8% over two years.
