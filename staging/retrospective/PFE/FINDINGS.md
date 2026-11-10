# PFE retrospective findings (hindsight)

Patterns seen in `outcome.json` for the PFE weekly dates: 105 from 2008-01-04 to 2009-12-31, all Pfizer Inc (NYSE: PFE). They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time
build was committed and pushed (40abcf7). Outcomes were computed on 2026-11-10 from the closes posted to 2026-11-09; every date has its
6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-28). Total returns include the $0.32 and then $0.16 quarterly dividends; the
prices are on the as-traded basis of the models (Yahoo's series times its 1.054 factor of 2020-11-17, after every horizon). Medians of an
even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of it, and RICH should miss the
hurdle and lag it.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 50 | -7.1% | -12.9% to +26.3% | 0 | 30 | -9.4% | 30 |
| class RICH, legacy tier AVOID | 3 | -8.0% | -12.9% to -4.1% | 0 | 3 | -31.1% | 0 |
| FY07E $1.055 (2008-01-04 to 2008-01-18) | 3 | -8.0% | -12.9% to -4.1% | 0 | 3 | -31.1% | 0 |
| FY08E $1.855 (2008-01-24 to 2008-04-11) | 12 | -9.0% | -12.5% to -6.2% | 0 | 9 | -23.8% | 9 |
| FY08E $1.805 (2008-04-18 to 2008-10-17) | 27 | -7.7% | -12.9% to +26.3% | 0 | 21 | -9.4% | 21 |
| FY08E $1.66 (2008-10-22 to 2008-12-31) | 11 | +10.2% | +7.2% to +16.9% | 0 | 0 | +0.6% | 0 |
| latest print Q3 2007 (2008-01-04 to 2008-01-18) | 3 | -8.0% | -12.9% to -4.1% | 0 | 3 | -31.1% | 0 |
| latest print Q4 2007 (2008-01-24 to 2008-04-11) | 12 | -9.0% | -12.5% to -6.2% | 0 | 9 | -23.8% | 9 |
| latest print Q1 2008 (2008-04-18 to 2008-07-18) | 14 | -7.8% | -12.0% to -1.8% | 0 | 14 | -7.6% | 14 |
| latest print Q2 2008 (2008-07-24 to 2008-10-17) | 13 | -2.1% | -12.9% to +26.3% | 0 | 7 | -9.4% | 7 |
| latest print Q3 2008 (2008-10-22 to 2008-12-31) | 11 | +10.2% | +7.2% to +16.9% | 0 | 0 | +0.6% | 0 |

- **CHEAP held on 30 of 50 dates, every one by beating SPY, none by clearing the hurdle.** The 37 CHEAP dates from 2008-01-24 to
  2008-10-03 ($17.28-23.59) returned -12.9% to +2.1% over two years, dividends included, while SPY returned -18.7% to +8.0%; 30 of them
  beat it, by up to 11.9pp, the other 7 lagged by up to 8.8pp. The 13 dates from 2008-10-10 ($15.14-17.71) returned +7.2% to +26.3% but
  lagged SPY's rebound (+27.0% to +56.9%) by 10.5-40.0pp. Every 2008 date sat through a 36-52% drawdown; the low close was $11.66 on
  2009-03-02, 7.0x FY08's $1.66 guide and 8.2x the first FY09 guide. Over three years (to the end of 2011) the 2008 dates returned
  -12.5% to +41.2% (median +15.0%) and 29 beat SPY; none cleared the three-year hurdle.
- **The floor was far above where the stock bottomed.** The EPP floor was 17x the reported-EPS guide ($28-32) on every 2008 date after
  the Q4 2007 print, set by the calendar-year lows of 2004-2007 (14.7-20.2x), which are GAAP multiples on years carrying $0.43 (2006) and $0.36
  (2007) a share of purchase-accounting adjustments, mostly recurring amortization, and the charges of the Pharmacia integration and the
  cost programmes. The price was already 25-51% under
  that floor and then fell to $11.66. The same pattern as RCL, MAR and BKR in early 2008: a floor from a window's earlier multiples, here
  without a cycle in the earnings. Hypothesis, not a rule: test a floor that discounts a window's own trend in multiples (the stock's
  P/E fell from 2004 to 2008 on a shrinking U.S. franchise) on other tickers and periods; never fit it to PFE's outcomes.
- **January 2008's RICH dates were right on the price and wrong on the test.** On FY07's depressed $1.055 the three dates ($22.50-24.02)
  were 21-23x and above a 20x floor; the stock lost 4-13% over two years and its m12-24 average price sat 30-34% under the entry, but
  SPY fell further (-10% to -16%), so RICH "lagging the benchmark" failed on all three. Under the alternative reading of the 2003
  exclusion (a ten-year window, retro/README.md "PFE") they would have been CHEAP and held. That is a hindsight observation about one
  judgement call, never a reason to re-encode it.
- **Entry price ranks the outcome, as in every one-stock crash.** Across the 53 dates the entry price ranks the return to the m12-24
  average price at Spearman -1.00 and the two-year return at -0.76; the EPP gap at -0.94; the proxy composite at +0.62 and the adjusted
  gap at +0.60 (the right signs). Ratio B ranks it at -0.31.
- **The two-year price landed nearest BEAR on 50 dates and BASE on 3,** at 1.05-2.17 times the BEAR price and 0.31-0.70 times BULL.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 51 | +29.9% | +9.4% to +66.6% | 25 | 21 | +16.0% | 39 |
| class CHEAP, legacy tier ACCUMULATE | 1 | +15.5% | +15.5% | 0 | 0 | +6.5% | 0 |
| FY08E $1.66 (2009-01-09 to 2009-01-23) | 3 | +13.9% | +13.5% to +13.9% | 0 | 0 | -4.2% | 0 |
| FY09E $1.415 (2009-01-27 to 2009-04-24) | 13 | +54.9% | +26.4% to +65.4% | 12 | 2 | +22.3% | 12 |
| FY09E $1.275 (2009-04-29 to 2009-07-17) | 12 | +49.0% | +41.6% to +66.6% | 12 | 5 | +21.2% | 12 |
| FY09E $1.375 (2009-07-23 to 2009-10-16) | 13 | +18.9% | +15.1% to +33.2% | 1 | 8 | +14.7% | 9 |
| FY09E $1.475 (2009-10-21 to 2009-12-31) | 11 | +22.3% | +9.4% to +27.3% | 0 | 6 | +5.9% | 6 |
| latest print Q3 2008 (2009-01-09 to 2009-01-23) | 3 | +13.9% | +13.5% to +13.9% | 0 | 0 | -4.2% | 0 |
| latest print Q4 2008 (2009-01-27 to 2009-04-24) | 13 | +54.9% | +26.4% to +65.4% | 12 | 2 | +22.3% | 12 |
| latest print Q1 2009 (2009-04-29 to 2009-07-17) | 12 | +49.0% | +41.6% to +66.6% | 12 | 5 | +21.2% | 12 |
| latest print Q2 2009 (2009-07-23 to 2009-10-16) | 13 | +18.9% | +15.1% to +33.2% | 1 | 8 | +14.7% | 9 |
| latest print Q3 2009 (2009-10-21 to 2009-12-31) | 11 | +22.3% | +9.4% to +27.3% | 0 | 6 | +5.9% | 6 |

- **CHEAP held on 39 of 52 dates.** The 25 dates from the Q4 2008 print (2009-01-27, the day after the Wyeth deal and the dividend cut)
  to 2009-07-17 ($12.31-15.82) returned +26.4% to +66.6%, 24 of them clearing the hurdle. The three dates of January 2009 before that
  print ($17.4-17.5) returned +13.5-13.9% and lagged SPY's rebound by 34-46pp; the 24 dates from 2009-07-23 ($15.77-18.60) returned +9.4%
  to +33.2%, clearing the hurdle once and beating SPY on 14. Only 21 dates beat SPY over two years: SPY's run from the March 2009 low
  outpaced the stock's.
- **The three-year read is stronger, unlike BKR's.** Measured to January-December 2012, the 2009 dates returned +37.7% to +90.7% (median
  +63.2%); 42 cleared the three-year hurdle (+52.1%) and 40 beat SPY, so 48 of 52 held at three years against 39 at two.
- **The class never moved while the inputs did.** Through 2009 the reported-EPS guide went from $1.34-1.49 to $1.20-1.35 and back up to
  $1.45-1.50, BASE from +3.3% to -3.8% and then +5.6%/yr and the proxy composite from 2.45 to 1.80 and then 2.10, and the price state stayed CHEAP: the price was 14-42%
  under a 15x floor on every date. Within the year the entry price ranks the return to the m12-24 average price at Spearman -0.92 and the
  two-year return at -0.88; the proxy composite ranks them at -0.74 and -0.79, the wrong sign, which is the calendar (the later prints were
  both stronger and higher-priced entries), not evidence against the signals.
- **The two-year price landed nearest BASE on 39 dates and BEAR on 13,** at 0.51-0.90 times the BASE price and 0.44-0.77 times BULL.

## The encoding calls, seen afterwards

Only one judgement call recorded in retro/README.md ("PFE") moves classes: the 2003 exclusion taking the history and the window with it.
Read as only 2003 leaving (a ten-year window), the three January 2008 dates are CHEAP instead of RICH, and by the two-year test they
would have held (each beat SPY) where the RICH call failed; no other date moves. Every signal at its BEAR value moves 2009-10-16 from
CHEAP to RICH (a +15.5% return that lagged SPY by 1.4pp, which RICH would have called). GAAP or adjusted EPS, 2008 kept or excluded,
the revenue guides used or not and the dividend's timing move no class. Across all 105 dates the call held on 69 (30 + 0 in 2008, 39 in
2009); what decided the outcomes was where the stock entered the crash, as with every one-stock series, and the floor that method r2
takes from a window whose multiples were falling. Both are hypotheses to test across tickers, never a reason to re-encode PFE.
