# LLY retrospective findings (hindsight)

Patterns seen in `outcome.json` for the LLY weekly dates: 105 from 2008-01-04 to 2009-12-31, all Eli Lilly and Company (NYSE: LLY).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build was committed and pushed (8d1f450, the empty-slot correction the firewall found 96e4c9f, firewall result 73b08d1);
the outcomes were computed on 2026-11-21. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-31). Total returns
include the quarterly dividends ($0.425 to the ex-date of 2008-02-13, $0.47 from it, $0.49 from 2009-02-11 and through every horizon). No
split falls in any horizon, so every price is as traded. Medians of an even count take the upper middle value
(`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should
clear the hurdle or beat the benchmark (SPY). Every date was CHEAP and BUY, so the tables test that one call against the calendar.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | -18.8% | -30.8% to +30.6% | 0 | 0 | -27.4% | 0 |
| FY07E $2.785 (2008-01-04 to 2008-01-25) | 4 | -23.4% | -30.8% to -22.0% | 0 | 0 | -33.8% | 0 |
| FY08E $3.875 (2008-01-30 to 2008-03-07) | 6 | -23.6% | -25.6% to -21.6% | 0 | 0 | -32.2% | 0 |
| FY08E $3.815 (2008-03-14 to 2008-04-18) | 6 | -21.6% | -23.5% to -16.8% | 0 | 0 | -31.5% | 0 |
| FY08E $3.975 (2008-04-22 to 2008-07-18) | 13 | -20.2% | -25.1% to -17.1% | 0 | 0 | -27.9% | 0 |
| FY08E $3.865 (2008-07-25 to 2008-10-17) | 13 | -15.6% | -20.7% to +30.6% | 0 | 0 | -25.1% | 0 |
| FY08E $2.465 (2008-10-24 to 2008-12-05) | 7 | +15.8% | +8.9% to +26.3% | 0 | 0 | +4.5% | 0 |
| FY08E $2.71 (2008-12-12 to 2008-12-31) | 4 | +3.1% | -3.3% to +6.8% | 0 | 0 | -7.4% | 0 |
| latest print Q3 2007 (2008-01-04 to 2008-01-25) | 4 | -23.4% | -30.8% to -22.0% | 0 | 0 | -33.8% | 0 |
| latest print Q4 2007 (2008-01-30 to 2008-04-18) | 12 | -22.4% | -25.6% to -16.8% | 0 | 0 | -32.2% | 0 |
| latest print Q1 2008 (2008-04-22 to 2008-07-18) | 13 | -20.2% | -25.1% to -17.1% | 0 | 0 | -27.9% | 0 |
| latest print Q2 2008 (2008-07-25 to 2008-10-17) | 13 | -15.6% | -20.7% to +30.6% | 0 | 0 | -25.1% | 0 |
| latest print Q3 2008 (2008-10-24 to 2008-12-31) | 11 | +11.2% | -3.3% to +26.3% | 0 | 0 | +3.3% | 0 |

- **CHEAP failed on all 53 dates of 2008.** From $30.43-56.81 the 2008 entries returned -30.8% to +30.6% over two years, dividends
  included, while SPY returned -18.7% to +56.9%: every one lagged it, by 1.7-47.5pp, and none cleared the hurdle. Over three years (to
  the end of 2011) they returned -28.3% to +41.2% (median -9.2%) and none beat SPY. Every 2008 date sat through a 32-52% drawdown (the
  low close $27.47 on 2009-03-05); two years on the price was $32.37-37.76.
- **The earnings were real; the multiple was not.** FY2009 came in at the guides the models used: reported $3.94 (the Q4 2009 release,
  2010-01-28, outside the series) against the $3.95-4.19 of 2009's guides. Two years on, the
  2008-2009 entries' prices ($32.37-41.64) were 8.2-10.6x that FY2009 figure, while every rule that reads the stock's own decade (the
  median P/E of 26.7-29.7x, the EPP floor of 20-22x from the 1998-2007 calendar-year lows of 17.6-31.1x) put the floor alone at
  1.08-3.10 times the entry price. The EPP floor
  ($54-88) was never reached within two years on any of the 105 dates, and the two-year price landed nearest the BEAR scenario on every
  date. Hypothesis, not a rule: a decade of a company's own multiples can sit far above what the market will pay once the company's own
  10-Ks name a wave of patent expirations a few years out ("several major products will lose intellectual property protection
  beginning in 2011", FY2007 10-K); method r2 reads those words only into the durability "why". Test it on other tickers and periods
  with a dated patent cliff, never fit it to LLY.
- **The best 2008 entries were the cheapest.** The Q3 2008 print's dates (2008-10-24 to 2008-12-31, $30.43-40.27) returned -3.3% to +26.3%,
  the January 2008 dates ($50.74-56.81) -30.8% to -22.0%.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +21.3% | +0.9% to +37.7% | 1 | 13 | +4.7% | 14 |
| FY08E $2.71 (2009-01-09 to 2009-01-23) | 3 | +1.8% | +0.9% to +3.4% | 0 | 0 | -7.9% | 0 |
| FY09E $4.125 (2009-01-30 to 2009-07-17) | 25 | +20.5% | +3.3% to +37.7% | 1 | 0 | +4.5% | 1 |
| FY09E $4.19 (2009-07-23 to 2009-10-16) | 13 | +22.3% | +15.1% to +27.0% | 0 | 8 | +7.4% | 8 |
| FY09E $3.95 (2009-10-22 to 2009-12-31) | 11 | +23.1% | +7.0% to +27.4% | 0 | 5 | +2.6% | 5 |
| latest print Q3 2008 (2009-01-09 to 2009-01-23) | 3 | +1.8% | +0.9% to +3.4% | 0 | 0 | -7.9% | 0 |
| latest print Q4 2008 (2009-01-30 to 2009-04-17) | 12 | +18.0% | +3.3% to +37.7% | 1 | 0 | +6.1% | 1 |
| latest print Q1 2009 (2009-04-21 to 2009-07-17) | 13 | +22.2% | +15.3% to +26.0% | 0 | 0 | +3.6% | 0 |
| latest print Q2 2009 (2009-07-23 to 2009-10-16) | 13 | +22.3% | +15.1% to +27.0% | 0 | 8 | +7.4% | 8 |
| latest print Q3 2009 (2009-10-22 to 2009-12-31) | 11 | +23.1% | +7.0% to +27.4% | 0 | 5 | +2.6% | 5 |

- **CHEAP held on 14 of 52 dates of 2009, mostly late in the year.** The 2009 entries ($27.98-38.48) returned +0.9% to +37.7% over two years
  against SPY's +10.4% to +98.7%: the dates from the March 2009 low to the summer lagged SPY's rebound by up to 63.6pp, and only
  2009-03-06, the low of the series ($27.98, 6.8x), cleared the hurdle (+37.7%). From 2009-08-21 the entries beat SPY on 13 dates (by
  up to 11.6pp). Over three years the 2009 entries returned +18.7% to +72.9% (median +45.0%); 20 beat SPY and 16 cleared the three-year
  hurdle.
- **Ratio B below zero was not a margin of safety.** The BEAR price exceeded the price on 44 dates (2008-10-10, 2008-10-17 and 2009-01-30
  to 2009-11-13: the price under even the BEAR case). Those dates returned +3.3% to +37.7% over two years, yet 35 of the 44 lagged SPY
  and the call held on only 10 (2008-10-10 and 2008-10-17, at +30.6% and +29.4%, missed SPY by 6.1 and 1.7pp); the BEAR case, at the
  window's 10th-percentile P/E (9.5-21.1x), was itself a multiple the market did not grant.

## Across the series

- **The ranks run through the price.** Across the 105 dates the entry price ranks the two-year return at Spearman -0.91 and the return to
  the m12-24 average price at -0.99; the P/E at -0.72 and -0.75 and the EPP gap at -0.73 and -0.76 (the right signs: the lower the
  multiple and the further under the floor, the better the return); Ratio B at -0.50 and -0.58 (right); the adjusted gap at -0.30 and
  -0.39 and the proxy composite at -0.29 and -0.41 (the wrong sign: a higher read went with lower returns); the P/E percentile at +0.50
  and +0.37 (wrong, as the 2009 window without FY2008's days had a lower median). One stock over two years mostly tests "buy lower"
  (retro/README.md, "Scoring a single stock").
- **The class carried no information here.** Every date was CHEAP and BUY with robustness 8 of 8, and no encoding the build tested moved a
  class (retro/README.md, "LLY"): the call rested entirely on the stock's own 1998-2007 P/E history, which the following years did not
  repeat. A series where a call never varies cannot separate good entries from bad ones; only the price did.
- **Profile drift:** the point-in-time profile (DURABLE, risk 2) against today's (DURABLE, risk 1, reviewed 2026-09-22) is a label only.
