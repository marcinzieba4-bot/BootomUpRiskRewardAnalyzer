# CRM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the CRM weekly dates: 105, from 2008-01-04 to 2009-12-31, all salesforce.com, inc. (NYSE: CRM). They
are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time
build, validation outputs, README section and firewall result were committed and pushed (36669f3, 132ff2d, 200cf2e, 8ba1064); the outcomes
were computed on 2026-11-26. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-31). salesforce.com paid no
dividend, so total returns are price returns; no split falls in any horizon (the four-for-one split is 2013-04-18), so every price is as
traded. Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and
+52.1% over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within 15pp
of it either way. The 8 dates before the Q4 FY08 print were FAIR and the 97 from it CHEAP, every one legacy tier BUY, so these tables test
two calls against the calendar.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2008-02-29 to 2008-12-31) | 45 | +47.0% | +13.8% to +512.6% | 28 | 45 | +10.5% | 45 |
| class FAIR, legacy tier BUY (2008-01-04 to 2008-02-22) | 8 | +27.1% | +20.9% to +35.2% | 2 | 8 | -7.2% | 0 |
| FY08E $0.125 (2008-01-04 to 2008-02-22) | 8 | +27.1% | +20.9% to +35.2% | 2 | 8 | -7.2% | 0 |
| FY09E $0.325 (2008-02-29 to 2008-05-16) | 12 | +29.5% | +13.8% to +36.2% | 1 | 12 | -10.3% | 12 |
| FY09E $0.335 (2008-05-23 to 2008-08-15) | 13 | +32.8% | +19.7% to +56.5% | 7 | 13 | -1.9% | 13 |
| FY09E $0.295 (2008-08-22 to 2008-12-31) | 20 | +296.3% | +99.0% to +512.6% | 20 | 20 | +192.0% | 20 |
| latest print Q3 FY08 (2008-01-04 to 2008-02-22) | 8 | +27.1% | +20.9% to +35.2% | 2 | 8 | -7.2% | 0 |
| latest print Q4 FY08 (2008-02-29 to 2008-05-16) | 12 | +29.5% | +13.8% to +36.2% | 1 | 12 | -10.3% | 12 |
| latest print Q1 FY09 (2008-05-23 to 2008-08-15) | 13 | +32.8% | +19.7% to +56.5% | 7 | 13 | -1.9% | 13 |
| latest print Q2 FY09 (2008-08-22 to 2008-11-14) | 13 | +169.4% | +99.0% to +335.6% | 13 | 13 | +96.9% | 13 |
| latest print Q3 FY09 (2008-11-21 to 2008-12-31) | 7 | +358.3% | +313.1% to +512.6% | 7 | 7 | +201.8% | 7 |

- **CHEAP held on all 45 dates of 2008; FAIR failed on all 8, on the upside.** The January-February 2008 entries ($50.87-58.86, 407-471x
  FY08E $0.125, the 87th-98th percentile) returned +20.9% to +35.2% over two years while SPY fell, +34.9 to +49.9pp ahead of it: a FAIR
  call expects the stock within 15pp of SPY, so each missed by beating it (2 of the 8 cleared the hurdle; over three years all 8 returned
  +130.5% to +178.4%). The robustness block's other reading, RICH, would have missed by more. These entries sat through a 70.5% drawdown
  (the low close $21.96 on 2008-11-19), and the average price of months 12-24 was 3-23% under the entry.
- **The CHEAP dates of February-August 2008 held on the benchmark, not on the hurdle.** On FY09E $0.325 and $0.335 ($55.83-73.10, 172-218x)
  they returned +13.8% to +56.5% over two years, 8 of 25 clearing the hurdle and all 25 beating SPY (by 26.5-64.8pp); the average price of
  months 12-24 was -14.7% to +11.3% from the entry, and each fell 67-71% on the way. Over three years all 25 cleared the 52.1% hurdle
  (+79.5% to +140.9%). From the Q2 FY09 print (FY09E $0.295, $22.32-57.20, 76-194x) the 20 entries returned +99.0% to +512.6% (the best,
  2008-11-21, the series low at 75.7x, its own print's day).
- **The class flipped on a guide, not on the price.** 2008-02-22 ($52.34, FAIR at 419x FY08E $0.125) and 2008-02-29 ($59.72, CHEAP at
  184x FY09E $0.325) are a week and a higher price apart: the Q4 FY08 print moved the current year and its EPS guide, and the stock's
  multiple on it fell from the 89th to the 38th percentile of its own history. FY2010 then came in at $0.63 (the Q4 FY10 release,
  2010-02-24, outside the series; FY2009 was $0.35), so GAAP EPS went from FY2008's $0.15 to $0.63 in two years.
  Hypothesis, not a rule: for a company whose GAAP EPS is a few cents against its revenue (an operating margin of 3-6%, marketing and sales
  at half of revenue, stock-based compensation in), a P/E-percentile call is mostly a call on the next year's EPS level, and an
  own-history window of such years ranks the multiple against EPS that grows fast from a small base. Test it on other tickers and periods
  with small GAAP EPS and fast EPS growth, never fit it to CRM.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2009-01-09 to 2009-12-31) | 52 | +235.6% | +34.9% to +449.3% | 52 | 52 | +194.6% | 52 |
| FY09E $0.295 (2009-01-09 to 2009-02-20) | 7 | +394.6% | +351.1% to +449.3% | 7 | 7 | +271.8% | 7 |
| FY10E $0.545 (2009-02-27 to 2009-05-15) | 12 | +259.9% | +222.4% to +395.8% | 12 | 12 | +203.5% | 12 |
| FY10E $0.595 (2009-05-22 to 2009-08-14) | 13 | +267.6% | +184.6% to +320.5% | 13 | 13 | +211.0% | 13 |
| FY10E $0.605 (2009-08-21 to 2009-11-13) | 13 | +112.8% | +96.4% to +145.2% | 13 | 13 | +128.4% | 13 |
| FY10E $0.625 (2009-11-19 to 2009-12-31) | 7 | +65.9% | +34.9% to +95.8% | 7 | 7 | +103.1% | 7 |
| latest print Q3 FY09 (2009-01-09 to 2009-02-20) | 7 | +394.6% | +351.1% to +449.3% | 7 | 7 | +271.8% | 7 |
| latest print Q4 FY09 (2009-02-27 to 2009-05-15) | 12 | +259.9% | +222.4% to +395.8% | 12 | 12 | +203.5% | 12 |
| latest print Q1 FY10 (2009-05-22 to 2009-08-14) | 13 | +267.6% | +184.6% to +320.5% | 13 | 13 | +211.0% | 13 |
| latest print Q2 FY10 (2009-08-21 to 2009-11-13) | 13 | +112.8% | +96.4% to +145.2% | 13 | 13 | +128.4% | 13 |
| latest print Q3 FY10 (2009-11-19 to 2009-12-31) | 7 | +65.9% | +34.9% to +95.8% | 7 | 7 | +103.1% | 7 |

- **CHEAP held on all 52 dates of 2009.** From $26.05-73.77 (88-107x FY09E in January and February, 51-118x FY10E from the Q4 FY09 print)
  the entries returned +34.9% to +449.3% over two years and +113.4% to +412.0% over three, all clearing both hurdles and beating SPY (by
  +18.2 to +369.7pp over two years). The entries of 2009-01-09 to 2009-08-14 (the 1st-17th percentile) returned +184.6% to +449.3%; those
  from the Q2 FY10 print (FY10E $0.605-0.625, 86-118x, the 23rd-38th percentile) +34.9% to +145.2%. FY2010 came
  in at $0.63 against the $0.545-0.625 the models used.
- **The growth signals said BEAR while the stock rose.** Subscription and support growth (+43.7% falling to +21.1%) and deferred revenue
  growth (+37.8% falling to +14.5%) sat under their BASE lines on every print the 2009 dates read (Q3 FY09 to Q3 FY10), lines set by rule
  T at the slowest years of the start-up decade (61% and 68%), and the proxy composite stayed at 1.60-1.75; the price state, not the
  signals, carried the call. Hypothesis, not a rule: rule T over IPO-era years (here +60% to +328% growth) scores a maturing company as
  BEAR on every print and carries no information about its deceleration; test it across the other tickers whose rule-T decade holds
  start-up years (as a cross-ticker study, never inside CRM's archive).
- **Where the two-year price landed:** in the BASE band on 76 of the 105 dates, BEAR on 15 (CHEAP dates of 2008) and BULL on 14; none below
  BEAR or above BULL. `profile_drift` (hindsight): DURABLE, risk 2 on every date; today's 2026 profile files CRM as AI_EXPOSED (GENAI), risk
  3, a judgement made 17 years later and no input here.
