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

# 2010-2013 (hindsight)

Patterns seen in `outcome.json` for the 209 weekly dates from 2010-01-08 to 2013-12-31: FPL Group, Inc. to 2010-05-21, NextEra Energy, Inc.
from 2010-05-28 (NYSE: FPL to 2010-06-18, NYSE: NEE from 2010-06-25). The same terms as above: **labels and hypotheses**, never inputs. The
batch was scored only after its point-in-time build, validation outputs, README section and firewall result were committed and pushed
(0079ee851, d36a78442, 323194876, ab84a39ba), on 2026-11-27; this session had scored 2008-2009 before deciding it (disclosed in
retro/README.md, "NEE 2010-2013"). The `profile_drift` line (the 2026 profile) was already seen in the 2008-2009 scoring and enters nothing.
Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2016-12-30). Total returns include the quarterly dividends as traded
($0.50 from the ex-date of 2010-02-24, $0.55 from 2011-03-02, $0.60 from 2012-02-29, $0.66 from 2013-02-27, $0.725 from 2014-02-26, $0.77 from
2015-02-25, $0.87 from 2016-02-24): $3.70-5.98 a share over two years, 6.6-9.2% of the entry price. No split falls in any horizon (the next is
2020-10-27). The hurdle, the medians and "call held" are as above.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 23 | +37.4% | +28.9% to +49.6% | 21 | 23 | +18.3% | 23 |
| class CHEAP, legacy tier ACCUMULATE | 10 | +41.7% | +38.3% to +45.4% | 10 | 10 | +24.0% | 10 |
| class FAIR, legacy tier ACCUMULATE | 11 | +35.4% | +31.4% to +40.8% | 10 | 8 | +14.2% | 10 |
| class FAIR, legacy tier WATCHLIST | 5 | +34.5% | +31.3% to +37.3% | 4 | 4 | +14.5% | 5 |
| class RICH, legacy tier BUY | 3 | +25.3% | +19.9% to +31.9% | 0 | 3 | +10.3% | 0 |
| EPS anchor $3.97 (2010-01-27 to 2010-12-31) | 49 | +37.4% | +28.9% to +49.6% | 45 | 45 | +16.3% | 48 |
| EPS anchor $4.07 (2010-01-08 to 2010-01-22) | 3 | +25.3% | +19.9% to +31.9% | 0 | 3 | +10.3% | 0 |
| latest print Q3 2009 (2010-01-08 to 2010-01-22) | 3 | +25.3% | +19.9% to +31.9% | 0 | 3 | +10.3% | 0 |
| latest print Q4 2009 (2010-01-27 to 2010-04-23) | 13 | +35.9% | +28.9% to +41.7% | 11 | 13 | +18.3% | 13 |
| latest print Q1 2010 (2010-04-28 to 2010-07-16) | 12 | +40.5% | +32.8% to +49.6% | 12 | 12 | +15.2% | 12 |
| latest print Q2 2010 (2010-07-23 to 2010-10-22) | 14 | +37.2% | +31.3% to +45.0% | 12 | 10 | +14.5% | 14 |
| latest print Q3 2010 (2010-10-29 to 2010-12-31) | 10 | +41.7% | +32.9% to +45.4% | 10 | 10 | +25.8% | 9 |

- **CHEAP held on all 33 dates, FAIR on 15 of 16.** On FY09's $3.97 (11.5-14.0x) the CHEAP dates returned +28.9% to +49.6% over two years and
  beat SPY on every one; the FAIR dates returned +31.3% to +40.8%, inside the ±15pp band except 2010-11-05 (+15.5pp over SPY).
- **RICH missed on its 3 dates** (2010-01-08 to 2010-01-22, on FY08's $4.07 and BASE from Q3 2009's revenue, -17.0%): +19.9% to +31.9%,
  under the hurdle, but 4.2-7.6pp ahead of SPY.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 21 | +58.8% | +51.9% to +74.0% | 21 | 20 | +39.2% | 21 |
| class CHEAP, legacy tier ACCUMULATE | 1 | +43.9% | +43.9% to +43.9% | 1 | 1 | +26.4% | 1 |
| class FAIR, legacy tier BUY | 2 | +48.9% | +48.0% to +48.9% | 2 | 0 | +32.1% | 2 |
| class FAIR, legacy tier ACCUMULATE | 2 | +40.9% | +39.9% to +40.9% | 2 | 2 | +22.3% | 0 |
| class RICH, legacy tier BUY | 26 | +47.0% | +39.4% to +58.9% | 26 | 26 | +24.7% | 0 |
| EPS anchor $3.97 (2011-01-07 to 2011-01-21) | 3 | +40.9% | +39.9% to +43.9% | 3 | 3 | +22.3% | 1 |
| EPS anchor $4.74 (2011-01-26 to 2011-12-30) | 49 | +51.9% | +39.4% to +74.0% | 49 | 46 | +29.6% | 23 |
| latest print Q3 2010 (2011-01-07 to 2011-01-21) | 3 | +40.9% | +39.9% to +43.9% | 3 | 3 | +22.3% | 1 |
| latest print Q4 2010 (2011-01-26 to 2011-04-21) | 13 | +43.0% | +39.4% to +52.7% | 13 | 13 | +23.6% | 0 |
| latest print Q1 2011 (2011-04-29 to 2011-07-22) | 13 | +48.1% | +43.0% to +58.9% | 13 | 13 | +26.3% | 0 |
| latest print Q2 2011 (2011-07-28 to 2011-10-28) | 14 | +57.9% | +52.1% to +74.0% | 14 | 14 | +39.5% | 14 |
| latest print Q3 2011 (2011-11-04 to 2011-12-30) | 9 | +59.6% | +48.0% to +72.1% | 9 | 6 | +37.5% | 9 |

- **RICH missed on all 26 dates of the Q4 2010 and Q1 2011 prints** (2011-01-26 to 2011-07-22, on FY10's $4.74 at 11.1-12.8x, with BASE at
  -8.5% and -15.7%/yr from the quarters' revenue and the proxy at 1.50-1.55): +39.4% to +58.9% over two years, every one over the hurdle and
  14.8-32.2pp ahead of SPY. These are the batch's worst calls, and the multiple did not make them: it sat at 11.1-12.4x, under its ten-year
  median. On
  every one the price fell under the EPP floor ($52.14, 11x) at the 2011-08-08 low ($50.17), the only time in the batch it did.
- **CHEAP held on all 22 dates,** 2011-01-07 (+43.9%) and the 21 from the Q2 2011 print (2011-07-28 to 2011-12-30: +51.9% to +74.0%, the
  best returns of the series; 2011-08-12 at $52.69: +71.6%, 23.3pp over SPY). FAIR held on 2 of 4; 2011-01-14 and 2011-01-21 ran 20.0-22.8pp ahead of SPY.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 16 | +60.3% | +51.8% to +65.3% | 16 | 16 | +35.9% | 16 |
| class CHEAP, legacy tier ACCUMULATE | 3 | +59.6% | +58.9% to +62.3% | 3 | 3 | +34.7% | 3 |
| class FAIR, legacy tier ACCUMULATE | 5 | +56.6% | +53.5% to +58.0% | 5 | 5 | +32.3% | 5 |
| class FAIR, legacy tier WATCHLIST | 5 | +50.6% | +47.6% to +55.3% | 5 | 4 | +28.7% | 5 |
| class RICH, legacy tier ACCUMULATE | 4 | +62.4% | +54.3% to +63.5% | 4 | 4 | +39.6% | 0 |
| class RICH, legacy tier WATCHLIST | 19 | +46.8% | +39.0% to +68.2% | 19 | 16 | +33.6% | 0 |
| EPS anchor $4.59 (2012-01-27 to 2012-12-28) | 49 | +56.4% | +39.0% to +68.2% | 49 | 45 | +34.2% | 26 |
| EPS anchor $4.74 (2012-01-06 to 2012-01-20) | 3 | +55.1% | +51.8% to +56.3% | 3 | 3 | +35.9% | 3 |
| latest print Q3 2011 (2012-01-06 to 2012-01-20) | 3 | +55.1% | +51.8% to +56.3% | 3 | 3 | +35.9% | 3 |
| latest print Q4 2011 (2012-01-27 to 2012-04-20) | 13 | +61.5% | +53.4% to +65.3% | 13 | 13 | +36.2% | 13 |
| latest print Q1 2012 (2012-04-26 to 2012-07-20) | 13 | +55.6% | +47.6% to +62.3% | 13 | 12 | +32.0% | 13 |
| latest print Q2 2012 (2012-07-27 to 2012-10-19) | 13 | +45.9% | +39.0% to +54.3% | 13 | 10 | +31.0% | 0 |
| latest print Q3 2012 (2012-10-25 to 2012-12-28) | 10 | +59.3% | +48.8% to +68.2% | 10 | 10 | +37.8% | 0 |

- **CHEAP held on all 19 dates and FAIR on all 10 to 2012-07-20** (FY10's $4.74 to 2012-01-20, then FY11's $4.59): +47.6% to +65.3%.
- **RICH missed on all 23 dates from the Q2 2012 print** (2012-07-27 to 2012-12-28; BASE -9.5% and -14.4%/yr): +39.0% to +68.2%, every one
  over the hurdle; 20 beat SPY, by up to 14.3pp.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier WATCHLIST | 3 | +58.3% | +56.3% to +59.0% | 3 | 3 | +36.1% | 0 |
| class RICH, legacy tier AVOID | 50 | +32.2% | +20.0% to +59.4% | 25 | 39 | +25.9% | 6 |
| EPS anchor $4.56 (2013-01-30 to 2013-12-31) | 49 | +31.7% | +20.0% to +59.4% | 24 | 38 | +25.6% | 6 |
| EPS anchor $4.59 (2013-01-04 to 2013-01-25) | 4 | +58.6% | +56.3% to +59.0% | 4 | 4 | +36.1% | 0 |
| latest print Q3 2012 (2013-01-04 to 2013-01-25) | 4 | +58.6% | +56.3% to +59.0% | 4 | 4 | +36.1% | 0 |
| latest print Q4 2012 (2013-01-30 to 2013-04-26) | 13 | +42.7% | +35.9% to +59.4% | 13 | 11 | +33.7% | 0 |
| latest print Q1 2013 (2013-05-01 to 2013-07-26) | 13 | +32.6% | +27.8% to +43.0% | 8 | 6 | +25.9% | 4 |
| latest print Q2 2013 (2013-07-31 to 2013-10-25) | 13 | +30.7% | +25.6% to +39.7% | 3 | 12 | +25.6% | 1 |
| latest print Q3 2013 (2013-11-01 to 2013-12-31) | 10 | +24.5% | +20.0% to +29.8% | 0 | 9 | +21.0% | 1 |

- **RICH held on 6 of 53.** At 15.8-19.4x FY12's $4.56 (the 75th-97th percentile of a 13.4-14.1x median), the two-year return fell as the
  price rose through the year, from +42.7% (median, the Q4 2012 print's dates) to +24.5% (the Q3 2013 print's), and the dates from 2013-06-28 on
  mostly missed the hurdle (24 of 28 did). The six that held (five of 2013-06-14 to 2013-07-31, and 2013-11-08) returned +20.2% to +31.7%,
  0.6-7.3pp behind SPY. The other 19 that missed the hurdle beat SPY by up to 13.7pp. 33 of the 53 landed at the XBULL scenario price (EPS
  at the best two-year run, the P/E at its 90th percentile), 20 at BULL. Three-year returns ran
  +40.3% to +75.0% (median +60.9%, 26.5pp over SPY).

## Across 2010-2013

- **Calls held on 107 of 209:** CHEAP 74 of 74, FAIR 27 of 30, RICH 6 of 105. 177 dates cleared the hurdle and 187 beat SPY; the largest
  drawdown within two years was -9.4% to -15.3% on every date. The BEAR price ($35-46) was never reached; the EPP floor was reached only at the
  2011-08-08 low (28 dates, 2011-01-26 to 2011-08-05).
- **Against SPY the legacy tiers ranked in order; in absolute terms they did not:** median two-year excess BUY +17.4pp (91 dates),
  ACCUMULATE +11.2pp (36), WATCHLIST +5.3pp (32), AVOID +5.0pp (50); median two-year total return +49.6%, +41.7%, +48.8% and +32.2%;
  three-year +84.6%, +72.4%, +58.5% and +61.9%. AVOID (2013-01-25 to 2013-12-31) still beat SPY at the median.
- **The 2008-2009 hypotheses, scored here as labels:** (1) the adjusted outlook as the anchor (the "GAAP anchor makes a utility look rich"
  hypothesis) moves 29 classes in 2010-2013 (retro/README.md, "NEE 2010-2013"); scored on these outcomes, those 29 hold on 18 instead of 26,
  so the batch would hold on 99 instead of 107: no support here. (2) BASE on the year-to-date revenue moves 6 classes, which hold on 2
  instead of 6: no support either. Neither is a rule, and neither changes anything.
- **What missed was the signal set and the multiple's regime.** Every signal at its XBULL value would hold on 162 dates, at its BEAR value on
  12: the RICH calls of 2011-2012 came from falling quarterly revenue and weak energy sales (BASE -8.5% to -15.7%/yr; the proxy at 1.50-1.55
  in 2011), while EPS rose from $3.97 (FY09) to $4.56 (FY12) and the price from $45-55 to $72-89. And the 2013 calls came from a ten-year
  median (13.4-14.1x) set in years of higher rates, which the stock left for good. Hypotheses, not rules: (3) for a regulated utility,
  revenue that falls with fuel prices passed through to customers is no earnings signal, so BASE and the revenue signal misread it; (4) a
  ten-year P/E median can lag a lasting change in what the market pays for a sector. Test both on SO and on other periods; never fit them to NEE.

## Across 2008-2013

- **Calls held on 145 of 314:** CHEAP 76 of 106, FAIR 31 of 50, RICH 38 of 158. RICH held mostly in 2008 (25 of 30 before the crash) and
  rarely after it (6 of 105 in 2010-2013); CHEAP held rarely in 2008-2009 (2 of 32) and always in 2010-2012 (74 of 74). The same rules and
  thresholds read both periods; the outcomes turned with the market, not with any change in the method.

# 2014-2017 (hindsight)

Patterns seen in `outcome.json` for the 208 weekly dates from 2014-01-10 to 2017-12-29 (NextEra Energy, Inc., NYSE: NEE). The same terms as
above: **labels and hypotheses**, never inputs. The batch was built in a new session that opened no NEE outcome, finding or series file of
2008-2013 before its own outcomes were computed; it was scored only after its point-in-time build, validation outputs, README section and
firewall result were committed and pushed (a1b1ad067, 6f03df63f, 4a10e087b, 6f317e4c1), on 2026-11-27. The earlier sections of this file
were read only afterwards, to write this one. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2020-12-29; the
4-for-1 split of 2020-10-27 falls inside the 3-year horizons of late 2017, handled by `retro_tool outcome`). Total returns include the
quarterly dividends as traded. The hurdle, the medians and "call held" are as above.

## 2014 (51 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2014-01-10 to 2014-12-26) | 51 | +30.8% | +15.1% to +42.0% | 18 | 51 | +12.5% | 0 |
| FY13E $4.56 (FY12's) (2014-01-10 to 2014-01-24) | 3 | +27.4% | +26.9% to +29.3% | 0 | 3 | +17.4% | 0 |
| FY14E $4.47 (FY13's) (2014-01-29 to 2014-12-26) | 48 | +31.4% | +15.1% to +42.0% | 18 | 48 | +12.4% | 0 |
| latest print Q3 2013 (2014-01-10 to 2014-01-24) | 3 | +27.4% | +26.9% to +29.3% | 0 | 3 | +17.4% | 0 |
| latest print Q4 2013 (2014-01-29 to 2014-04-25) | 13 | +30.4% | +23.5% to +32.6% | 1 | 13 | +9.8% | 0 |
| latest print Q1 2014 (2014-05-01 to 2014-07-25) | 13 | +32.0% | +23.7% to +38.5% | 5 | 13 | +9.8% | 0 |
| latest print Q2 2014 (2014-07-30 to 2014-10-24) | 13 | +37.8% | +30.8% to +42.0% | 12 | 13 | +18.2% | 0 |
| latest print Q3 2014 (2014-10-31 to 2014-12-26) | 9 | +18.7% | +15.1% to +31.9% | 0 | 9 | +13.6% | 0 |

Three years: 31 of 51 cleared the hurdle, 51 beat SPY, total return +42.8% to +72.8%.
One year: total return -2.7% to +29.1%. Two years against SPY: +2.6 to +29.4 points.
Worst drawdown within two years: -15.3% to -15.3%.

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2015-01-02 to 2015-12-31) | 33 | +47.2% | +14.5% to +65.5% | 29 | 31 | +25.2% | 2 |
| class CHEAP, legacy tier WATCHLIST (2015-01-28 to 2015-01-28) | 1 | +16.4% | +16.4% to +16.4% | 0 | 0 | +9.6% | 0 |
| class CHEAP, legacy tier ACCUMULATE (2015-02-06 to 2015-04-24) | 10 | +29.8% | +23.3% to +33.5% | 3 | 10 | +17.4% | 10 |
| class CHEAP, legacy tier BUY (2015-03-06 to 2015-03-13) | 2 | +39.2% | +36.4% to +39.2% | 2 | 2 | +23.4% | 2 |
| class FAIR, legacy tier WATCHLIST (2015-06-05 to 2015-12-11) | 6 | +65.5% | +50.7% to +71.1% | 6 | 6 | +36.5% | 0 |
| class RICH, legacy tier WATCHLIST (2015-12-04 to 2015-12-04) | 1 | +66.5% | +66.5% to +66.5% | 1 | 1 | +40.7% | 0 |
| FY14E $4.47 (FY13's) (2015-01-02 to 2015-01-23) | 4 | +17.1% | +14.5% to +18.1% | 0 | 2 | +12.1% | 2 |
| FY15E $5.60 (FY14's) (2015-01-28 to 2015-12-31) | 49 | +46.8% | +16.4% to +71.1% | 41 | 48 | +25.1% | 12 |
| latest print Q3 2014 (2015-01-02 to 2015-01-23) | 4 | +17.1% | +14.5% to +18.1% | 0 | 2 | +12.1% | 2 |
| latest print Q4 2014 (2015-01-28 to 2015-04-24) | 13 | +29.8% | +16.4% to +39.2% | 5 | 12 | +17.4% | 12 |
| latest print Q1 2015 (2015-04-30 to 2015-07-31) | 14 | +45.6% | +39.0% to +53.2% | 14 | 14 | +24.9% | 0 |
| latest print Q2 2015 (2015-08-04 to 2015-10-23) | 12 | +55.3% | +42.2% to +66.3% | 12 | 12 | +31.4% | 0 |
| latest print Q3 2015 (2015-10-29 to 2015-12-31) | 10 | +61.5% | +55.8% to +71.1% | 10 | 10 | +36.6% | 0 |

Three years: 50 of 53 cleared the hurdle, 53 beat SPY, total return +48.8% to +100.0%.
One year: total return +0.1% to +33.7%. Two years against SPY: -2.4 to +36.9 points.
Worst drawdown within two years: -15.3% to -13.7%.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2016-01-08 to 2016-12-30) | 52 | +43.7% | +33.0% to +66.1% | 52 | 41 | +27.8% | 0 |
| FY15E $5.60 (FY14's) (2016-01-08 to 2016-01-22) | 3 | +49.8% | +47.7% to +52.5% | 3 | 1 | +34.5% | 0 |
| FY16E $6.06 (FY15's) (2016-01-29 to 2016-12-30) | 49 | +43.0% | +33.0% to +66.1% | 49 | 40 | +27.4% | 0 |
| latest print Q3 2015 (2016-01-08 to 2016-01-22) | 3 | +49.8% | +47.7% to +52.5% | 3 | 1 | +34.5% | 0 |
| latest print Q4 2015 (2016-01-29 to 2016-04-22) | 13 | +42.5% | +40.3% to +47.2% | 13 | 7 | +27.0% | 0 |
| latest print Q1 2016 (2016-04-29 to 2016-07-22) | 13 | +39.1% | +33.0% to +46.0% | 13 | 10 | +24.2% | 0 |
| latest print Q2 2016 (2016-07-28 to 2016-10-28) | 14 | +44.8% | +37.2% to +49.1% | 14 | 14 | +29.2% | 0 |
| latest print Q3 2016 (2016-11-01 to 2016-12-30) | 9 | +60.9% | +41.9% to +66.1% | 9 | 9 | +40.9% | 0 |

Three years: 52 of 52 cleared the hurdle, 52 beat SPY, total return +65.3% to +114.9%.
One year: total return +10.9% to +41.1%. Two years against SPY: -6.2 to +43.5 points.
Worst drawdown within two years: -13.7% to -8.8%.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID (2017-01-06 to 2017-12-29) | 52 | +52.5% | +45.1% to +64.6% | 52 | 52 | +29.4% | 0 |
| FY16E $6.06 (FY15's) (2017-01-06 to 2017-01-20) | 3 | +54.6% | +52.5% to +54.7% | 3 | 3 | +39.6% | 0 |
| FY17E $6.25 (FY16's) (2017-01-27 to 2017-12-29) | 49 | +52.5% | +45.1% to +64.6% | 49 | 49 | +29.3% | 0 |
| latest print Q3 2016 (2017-01-06 to 2017-01-20) | 3 | +54.6% | +52.5% to +54.7% | 3 | 3 | +39.6% | 0 |
| latest print Q4 2016 (2017-01-27 to 2017-04-13) | 12 | +52.5% | +49.3% to +57.3% | 12 | 12 | +32.8% | 0 |
| latest print Q1 2017 (2017-04-21 to 2017-07-21) | 14 | +51.2% | +45.1% to +54.5% | 14 | 14 | +28.9% | 0 |
| latest print Q2 2017 (2017-07-27 to 2017-10-20) | 13 | +53.1% | +50.1% to +64.6% | 13 | 13 | +27.4% | 0 |
| latest print Q3 2017 (2017-10-27 to 2017-12-29) | 10 | +55.5% | +49.0% to +63.2% | 10 | 10 | +29.4% | 0 |

Three years: 52 of 52 cleared the hurdle, 52 beat SPY, total return +65.9% to +130.8%.
One year: total return +11.8% to +33.2%. Two years against SPY: +20.9 to +44.8 points.
Worst drawdown within two years: -8.8% to -8.3%.

## Across 2014-2017

- **Calls held on 14 of 208:** CHEAP 12 of 13, FAIR 0 of 6, RICH 2 of 189. Every RICH call of 2014, 2016 and 2017 missed: the stock
  returned +15% to +66% over two years from those dates and beat SPY on 176 of the 189, while the model read 19-25x against a ten-year
  median of 14-16x. The 13 CHEAP calls of early 2015 held, but they rested on BASE reading the Q4 2014 quarter's reported revenue (+28.5%,
  NEER's hedge marks in), not on the multiple: right for a reason the README already names as fragile.
- **Scenario landing:** XBULL on 191 dates, BASE 13, BULL 4: the two-year price beat even the best two-year EPS run of the decade on
  almost every date, so the outcome came from the multiple rising, not from earnings beating the scenarios.
- **The miss looks like the 2010-2013 one, continued:** the stock re-rated for good above the decade median that the method uses as its
  centre (hypothesis 4 above: a ten-year P/E median can lag a lasting change in what the market pays). Seen again, not proven: it is one
  stock, one rate cycle and one rerating; test it on SO and the other utilities and periods, and never fit a rule to NEE. The GAAP anchor
  and the adjusted outlook were close in these years (FY16E adjusted $5.85-6.35 against GAAP FY15 $6.06), so the anchor choice moved only 5
  classes and does not explain the miss.
- **`profile_drift`** (the 2026 profile, read only by `retro_tool outcome`): DURABLE then and now, risk 2 then and 1 today. It enters nothing.
