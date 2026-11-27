# NEE retrospective findings (hindsight)

Patterns seen in `outcome.json` for the NEE weekly dates: 105 from 2008-01-04 to 2009-12-31, all FPL Group, Inc. (NYSE: FPL; NextEra Energy
from 2010). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build, validation outputs, README section and firewall result were committed and pushed (cbb8ccd, cdfb41b, 866d49d, ef4e08f,
e159e42), on 2026-11-27. The one-line 2026 profile that `retro_tool outcome` copies into each `outcome.json` (`profile_drift`, from
`data/business_profiles.json`) was first seen there, after every model had been built, validated and committed. Every date has its 6-month, 1-,
2- and 3-year horizons (the last ends 2013-01-02). Total returns include the quarterly dividends ($0.445 from the ex-date of 2008-02-27, $0.4725
from 2009-02-25, $0.50 from 2010-02-24, $0.55 from 2011-03-02, $0.60 from 2012-02-29; Yahoo prints $0.473 for $0.4725): $3.42-4.20 a share over
two years, 5.2-10.4% of the entry price. No split falls in any horizon (the next is 2020-10-27), so every price is as traded. Medians of an even
count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of the benchmark, and RICH should miss
the hurdle and lag the benchmark. A year's table runs to the last date of the calendar year.

## 2008 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 7 | +21.5% | +15.4% to +58.5% | 1 | 1 | +11.1% | 1 |
| class CHEAP, legacy tier ACCUMULATE | 2 | +12.1% | +12.1% to +12.1% | 0 | 0 | +5.7% | 0 |
| class FAIR, legacy tier ACCUMULATE | 1 | +10.3% | +10.3% to +10.3% | 0 | 0 | +1.9% | 0 |
| class RICH, legacy tier BUY | 2 | +41.5% | +37.2% to +41.5% | 2 | 1 | +22.5% | 0 |
| class RICH, legacy tier WATCHLIST | 1 | +20.3% | +20.3% to +20.3% | 0 | 1 | +5.7% | 0 |
| class RICH, legacy tier AVOID | 39 | -16.6% | -23.9% to +6.2% | 0 | 13 | -18.0% | 25 |
| EPS anchor $3.23 (2008-01-04 to 2008-01-25) | 4 | -15.8% | -21.0% to -14.9% | 0 | 0 | -16.4% | 4 |
| EPS anchor $3.27 (2008-01-29 to 2008-12-26) | 48 | -12.3% | -23.9% to +58.5% | 3 | 16 | -14.4% | 22 |
| latest print Q3 2007 (2008-01-04 to 2008-01-25) | 4 | -15.8% | -21.0% to -14.9% | 0 | 0 | -16.4% | 4 |
| latest print Q4 2007 (2008-01-29 to 2008-04-25) | 13 | -17.4% | -23.9% to -14.8% | 0 | 1 | -16.0% | 12 |
| latest print Q1 2008 (2008-05-01 to 2008-07-25) | 13 | -17.0% | -20.5% to -10.3% | 0 | 3 | -20.0% | 9 |
| latest print Q2 2008 (2008-08-01 to 2008-10-24) | 13 | +5.4% | -8.4% to +58.5% | 3 | 12 | -8.6% | 1 |
| latest print Q3 2008 (2008-10-28 to 2008-12-26) | 9 | +18.6% | +10.3% to +30.5% | 0 | 0 | +8.9% | 0 |

- **The RICH and AVOID calls of January to July 2008 held on 25 of 30.** On FY06's $3.23 and then FY07's $3.27 (18.4-22.1x, the 90th-100th
  percentile), the 30 dates returned -23.9% to -10.3% over two years, dividends included, against SPY's -18.7% to -6.8%; their m12-24 average
  price was 12-25% under the entry and every one sat through a 43-49% drawdown to the 2008-10-10 low ($37.08). The five misses (2008-01-29 and
  four dates of May-June 2008) matched or beat SPY by 0.0-4.5pp, the only way a RICH call that lost money could miss. Every one landed at the BASE (27) or
  BULL (3) scenario price.
- **From August to October 2008 the calls missed on 12 of 13.** The nine RICH and AVOID dates of August-September returned -8.4% to +6.2% and
  beat SPY by 0.5-13.4pp; RICH on 2008-10-17 and 2008-10-24 (BASE -10.4%/yr from Q2 2008's revenue) returned +41.5% and +37.2%, both over the
  hurdle. The one CHEAP date, 2008-10-10 at $37.08 (11.3x, 3% over the floor), returned +58.5% (+21.7pp over SPY), the best of the series.
- **The CHEAP and FAIR dates from the Q3 2008 print held on none of 13** (2008-10-28 to 2009-01-23): +8.2% to +30.5% over two years, none
  over the hurdle, all 0.6-41.6pp behind SPY's rebound from its March 2009 low; their m12-24 average price was -0.7% to +13.7%. The CHEAP
  reading rested on BASE +16.1%/yr from a quarter's revenue (+17.7%) that the next three quarters did not repeat.

## 2009 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 14 | +15.9% | +12.0% to +37.1% | 1 | 0 | +5.1% | 1 |
| class CHEAP, legacy tier ACCUMULATE | 9 | +12.2% | +8.1% to +16.5% | 0 | 0 | +2.6% | 0 |
| class FAIR, legacy tier ACCUMULATE | 8 | +8.4% | +6.5% to +15.0% | 0 | 0 | -0.6% | 3 |
| class FAIR, legacy tier WATCHLIST | 11 | +5.6% | -0.1% to +8.5% | 0 | 0 | -4.4% | 1 |
| class RICH, legacy tier BUY | 5 | +17.2% | +10.1% to +22.0% | 0 | 2 | +7.4% | 3 |
| class RICH, legacy tier ACCUMULATE | 5 | +13.7% | +9.7% to +23.2% | 0 | 2 | +4.3% | 3 |
| class RICH, legacy tier WATCHLIST | 1 | +0.5% | +0.5% to +0.5% | 0 | 0 | -5.7% | 1 |
| EPS anchor $3.27 (2009-01-02 to 2009-01-23) | 4 | +16.5% | +8.2% to +21.6% | 0 | 0 | +3.0% | 0 |
| EPS anchor $4.07 (2009-01-28 to 2009-12-31) | 49 | +12.5% | -0.1% to +37.1% | 1 | 4 | +0.8% | 12 |
| latest print Q3 2008 (2009-01-02 to 2009-01-23) | 4 | +16.5% | +8.2% to +21.6% | 0 | 0 | +3.0% | 0 |
| latest print Q4 2008 (2009-01-28 to 2009-04-24) | 13 | +15.8% | +12.0% to +37.1% | 1 | 0 | +4.3% | 1 |
| latest print Q1 2009 (2009-04-29 to 2009-07-24) | 13 | +8.4% | +2.4% to +15.4% | 0 | 0 | -4.0% | 0 |
| latest print Q2 2009 (2009-07-29 to 2009-10-23) | 13 | +7.9% | -0.1% to +14.0% | 0 | 0 | -0.4% | 5 |
| latest print Q3 2009 (2009-10-28 to 2009-12-31) | 10 | +17.2% | +9.7% to +23.2% | 0 | 4 | +6.5% | 6 |

- **CHEAP held on 1 of its 20 dates from the Q4 2008 print, FAIR on 4 of 19.** On FY08's $4.07 (10.5-14.8x) the CHEAP dates returned +8.1%
  to +37.1% over two years and none beat SPY (2.4-61.5pp behind); only 2009-03-06, the one date under the EPP floor ($42.82 against $44.77,
  three days before the 2009 low of $41.78), cleared the hurdle (+37.1%). The FAIR dates returned -0.1% to +15.0%, 6.7-44.3pp behind SPY: inside
  the ±15pp band only from 2009-08-28 to 2009-09-25. Every CHEAP and FAIR date of 2009 landed at the BASE scenario price.
- **RICH held on 7 of 11.** 2009-08-21 (+0.5%, 13.3pp behind SPY) and the ten dates from the Q3 2009 print (BASE -18.8%/yr from revenue -17.0%)
  returned +9.7% to +23.2%, under the hurdle, lagging SPY on six and beating it by 0.2-6.2pp on four (2009-11-06, 2009-11-20, 2009-12-24,
  2009-12-31). Nine landed at the BULL scenario price.

## Across both years

- **Calls held on 38 of 105:** RICH 32 of 53, FAIR 4 of 20, CHEAP 2 of 32. Only 4 dates cleared the hurdle (2008-10-10, 2008-10-17,
  2008-10-24 and 2009-03-06), all within a few weeks of the two market lows, and 20 beat SPY.
- **The legacy tiers ranked the absolute returns in order:** median two-year total return BUY +19.4% (28 dates), ACCUMULATE +12.1% (25),
  WATCHLIST +5.6% (13), AVOID -16.6% (39); median m12-24 average price +7.4%, +1.2%, -4.4% and -18.0%; median three-year return +38.8%,
  +34.3%, +29.4% and -3.8%. Against SPY the order breaks: the BUY, ACCUMULATE and WATCHLIST dates sit 25-35pp behind it (median), because they
  fall after the crash, when SPY rebounded harder, while AVOID's 2008 dates sit 3.2pp behind it.
- **The class turned with the anchor's age and with BASE.** The RICH calls of 2008 rest on a GAAP anchor a year behind the market's adjusted
  expectations (FY07's $3.27 against a $3.83-3.93 adjusted outlook for 2008; FY2008 came in at GAAP $4.07). The CHEAP calls rest on BASE read
  from a single quarter's revenue, which moved 23-27pp between consecutive prints (Q2 to Q3 2008: -8.8% to +17.7%; Q2 to Q3 2009: +6.3% to -17.0%). Hypotheses, not rules: (1) a GAAP anchor that excludes a company's guided basis makes a utility look rich in a rising-earnings year;
  (2) BASE from one quarter's revenue is noisy for a company whose revenue passes fuel costs and hedge marks through; test both on other utilities
  and other periods (the sensitivities in retro/README.md, "NEE", move 21 and 13 classes), never fit them to NEE.
- **The EPP floor was not reached except at the lows:** 11x on every date ($35.53-44.77); the price came within 3% of it on 2008-10-10 and
  fell under it on 2009-03-06 only. The BEAR price ($29-36, -12.6%/yr from 2002's fall) was never reached within two years.
