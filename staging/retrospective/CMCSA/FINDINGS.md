# CMCSA retrospective findings (hindsight)

Patterns seen in `outcome.json` for the CMCSA weekly dates: 105 from 2008-01-04 to 2009-12-31, all Comcast Corporation (Nasdaq: CMCSA,
the Class A shares). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored
only after its point-in-time build was committed and pushed (573d484). Outcomes were computed on 2026-11-11 from the closes posted to
2026-11-10; every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-28). Total returns include the $0.0625 and then
$0.0675 quarterly dividends from April 2008; the prices are on the as-traded basis of the models (Yahoo's series times its 2017 split and
its 2026 factor, both after every horizon). Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr
hurdle is +32.2% over two years. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should
land within ±15pp of it, and RICH should miss the hurdle and lag it.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | -3.8% | -21.3% to +53.8% | 9 | 28 | -16.9% | 35 |
| FY07E: FY06's $0.60 stands (2008-01-04 to 2008-02-08) | 6 | +0.9% | -11.1% to +4.0% | 0 | 6 | -12.3% | 6 |
| FY08E: FY07's $0.74 stands (2008-02-15 to 2008-12-31) | 47 | -4.6% | -21.3% to +53.8% | 9 | 22 | -18.1% | 29 |
| latest print Q3 2007 (2008-01-04 to 2008-02-08) | 6 | +0.9% | -11.1% to +4.0% | 0 | 6 | -12.3% | 6 |
| latest print Q4 2007 (2008-02-15 to 2008-04-25) | 11 | -6.6% | -21.3% to +0.1% | 0 | 8 | -22.4% | 8 |
| latest print Q1 2008 (2008-05-02 to 2008-07-25) | 13 | -7.4% | -18.5% to +1.6% | 0 | 11 | -25.0% | 11 |
| latest print Q2 2008 (2008-07-31 to 2008-10-24) | 13 | -8.7% | -17.0% to +53.8% | 1 | 2 | -16.9% | 2 |
| latest print Q3 2008 (2008-10-30 to 2008-12-31) | 10 | +40.0% | +20.3% to +50.7% | 8 | 1 | +15.8% | 8 |

- **CHEAP held on 35 of 53 dates, and the entry month decided which.** The six dates before the Q4 2007 print ($16.84-18.55) returned
  -11.1% to +4.0% over two years and beat SPY (-18.4% to -10.2%) by 7.3-20.4pp. The 34 dates from 2008-02-15 to 2008-10-03 ($18.33-22.50,
  from 15% under to 5% over the 29x floor) returned -21.3% to +1.6% while SPY returned -18.7% to +8.0%: 20 beat it, 14 lagged by up to
  7.9pp, none cleared the hurdle. The 13 dates from 2008-10-10 ($13.07-17.41, 19-39% under the floor) returned +20.3% to +53.8%; 9
  cleared the hurdle, but only 2 beat SPY's rebound (+27.7% to +56.9%), so 4 missed. Every 2008 date sat through a 38-51% drawdown; the
  low close was $11.22 on 2009-03-09, 12.3x FY08's $0.91. Over three years (to the end of 2011) the 2008 dates returned -4.1% to +97.0%
  (median +31.7%); 49 beat SPY and 7 cleared the three-year hurdle (+52.1%).
- **The floor sat far above where the stock bottomed.** The EPP floor was 29x the standing EPS on every 2008 date ($17.40, then $21.46
  from the Q4 2007 print), the median of calendar-year lows that include 63.0x (2004) and 69.1x (2005): GAAP multiples on $0.28 and $0.25
  of EPS, after $1.8-1.9 billion of interest a year, in years before EPS tripled to $0.74 (2007) and $0.91 (2008). The stock then fell to
  48% under that floor. The PFE shape again, from another cause: there a multiple falling on a shrinking franchise, here a multiple
  compressing while earnings rose from a depressed base. Hypothesis, not a rule: a floor (and a window) built on years whose EPS later
  multiplies overstates the multiple the market will pay at a trough; test on other tickers and periods, never fit it to CMCSA.
- **BULL and Ratio B said nothing.** BULL grew EPS at the 2004-2006 and then the 2004-2007 CAGR (+46.4% and +38.3%/yr) to the 75th-percentile multiple, $94-103; the
  two-year price was 0.15-0.22 times it and landed nearest BEAR on all 53 dates (0.90-1.48 times the BEAR price). Ratio B was -0.03 to
  0.08 on every date, so the legacy tier read BUY throughout. Hypothesis: a scenario growth rate measured from a depressed first year of
  the history inflates BULL and XBULL without bound; whether a bound helps is a cross-ticker question.
- **Entry price ranks the outcome, as in every one-stock crash.** Across the 53 dates the entry price ranks the return to the m12-24
  average price at Spearman -0.89 and the two-year return at -0.87; the EPP gap at -0.79 and Ratio B at -0.79 (the right signs, both
  driven by the price); the adjusted gap at +0.24 (right sign) and the proxy composite at -0.32 (the wrong sign: the composite was
  highest early in 2008, at the higher prices).

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +66.8% | +26.0% to +125.5% | 51 | 50 | +49.1% | 52 |
| FY08E: FY07's $0.74 stands (2009-01-09 to 2009-02-13) | 6 | +61.5% | +43.2% to +80.7% | 6 | 4 | +29.1% | 6 |
| FY09E: FY08's $0.91 stands (2009-02-19 to 2009-12-31) | 46 | +67.0% | +26.0% to +125.5% | 45 | 46 | +49.6% | 46 |
| latest print Q3 2008 (2009-01-09 to 2009-02-13) | 6 | +61.5% | +43.2% to +80.7% | 6 | 4 | +29.1% | 6 |
| latest print Q4 2008 (2009-02-19 to 2009-04-24) | 10 | +92.9% | +73.8% to +125.5% | 10 | 10 | +49.2% | 10 |
| latest print Q1 2009 (2009-05-01 to 2009-07-31) | 14 | +76.7% | +64.6% to +98.2% | 14 | 14 | +52.7% | 14 |
| latest print Q2 2009 (2009-08-07 to 2009-10-30) | 13 | +42.3% | +26.0% to +70.1% | 12 | 13 | +49.1% | 13 |
| latest print Q3 2009 (2009-11-05 to 2009-12-31) | 9 | +46.6% | +33.2% to +65.9% | 9 | 9 | +45.0% | 9 |

- **CHEAP held on all 52 dates.** The 30 dates from January to July 2009 ($11.63-16.36) returned +43.2% to +125.5% over two years and all
  cleared the hurdle; 28 beat SPY (the two that lagged, 2009-01-09 and 2009-01-16, by 4.5-4.6pp, still cleared the hurdle). The 22
  dates from August ($14.20-17.64) returned +26.0% to +70.1% and beat SPY (+10.4% to +28.7%) by 11.0-47.9pp; 21 cleared the hurdle.
  Every date was 15-51% under the floor.
- **The three-year read is stronger still.** Measured to January-December 2012, the 2009 dates returned +61.3% to +173.6% (median
  +125.7%); all 52 cleared the three-year hurdle and beat SPY.
- **The class never moved while the inputs did.** Through 2009 video subscriber growth went from -2.3% to -2.7%, revenue growth from
  +9.4% to +3.0%, BASE from +12.8% to +6.4%/yr and the proxy composite between 1.75 and 2.05, and the price state stayed CHEAP. Within
  the year the entry price ranks the two-year return at Spearman -0.91 and the return to the m12-24 average price at -0.62, the EPP gap
  at -0.78; the proxy composite (+0.18), the adjusted gap (+0.06) and Ratio B (-0.10) rank it barely at all.
- **The two-year price landed nearest BEAR on all 52 dates,** at 1.51-2.13 times the BEAR price, 0.51-0.69 times BASE and 0.17-0.24
  times BULL: the scenarios' spread, not the direction, failed.

## The encoding calls, seen afterwards

No judgement call recorded in retro/README.md ("CMCSA") moves a class or a tier: GAAP or company-adjusted EPS, the 2004-2005 adjusted
income, the FY2007 one-sided bound read as a point, the FY2008 guide used or not, and every signal at its BEAR or XBULL value leave all 105 dates CHEAP
and BUY, and a window starting in 2006 leaves the 46 dates it can be built on (from 2009-02-19) unchanged. Across them the call held on 87 (35 in 2008, 52 in 2009). All 18 misses are 2008
entries: 14 between February and early October at $18.33-22.50, near the floor that 2004-2005's GAAP multiples set, which lagged SPY by
up to 7.9pp, and 4 in October-November that gained 20-29% but lagged SPY's rebound. What decided the outcomes was where the stock entered
the crash; the floor's anchoring on a depressed-EPS base and the unbounded BULL growth are hypotheses to test across tickers, never a
reason to re-encode CMCSA.
