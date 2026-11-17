# LMT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the LMT weekly dates: 731 from 2008-01-04 to 2021-12-31 (105 to 2009-12-31, 209 from 2010-01-08 to
2013-12-31, 208 from 2014-01-10 to 2017-12-29, 209 from 2018-01-05), all
Lockheed Martin Corporation (NYSE: LMT). They are **labels and hypotheses**: never feed them back into the method or the fact sheet. Each
batch has its own section below.

# 2008-2009 (105 dates)

The 2008-2009 batch was scored only after its point-in-time build was committed (ed562557a) and its decisions, controls, leak scan,
sensitivities and firewall result were written to the README and committed (659b33a07); the outcomes were computed on 2026-11-16. Every date
has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-28). Total returns include the quarterly dividends ($0.42 from the
ex-date of 2007-11-29, $0.57 from 2008-11-26, $0.63 from 2009-11-27, $0.75 from 2010-11-29, $1.00 from 2011-11-29): $4.17-5.89 a share over
two years, 3.6-8.8% of the entry price. No split falls in any horizon, so every price is as traded. Medians of an even count take the upper
middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`:
CHEAP should clear the hurdle or beat the benchmark (SPY). The 2008 table runs to 2008-12-26; 2009-01-02 closes the ISO week of 2008-12-29
and sits in the 2009 table.

Every 2008-2009 date is CHEAP with tier BUY and all eight robustness variants agreeing, so the tables split the dates by latest print and by
where the price stood against the EPP floor, not by class.

## 2008 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | -20.4% | -35.9% to +2.8% | 0 | 0 | -25.4% | 0 |
| latest print Q3 2007 (2008-01-04 to 2008-01-18) | 3 | -23.9% | -26.8% to -20.6% | 0 | 0 | -28.4% | 0 |
| latest print Q4 2007 (2008-01-25 to 2008-04-18) | 13 | -17.8% | -26.9% to -8.8% | 0 | 0 | -26.5% | 0 |
| latest print Q1 2008 (2008-04-23 to 2008-07-18) | 13 | -20.4% | -22.8% to -15.4% | 0 | 0 | -25.0% | 0 |
| latest print Q2 2008 (2008-07-23 to 2008-10-17) | 13 | -30.8% | -35.9% to -14.4% | 0 | 0 | -30.7% | 0 |
| latest print Q3 2008 (2008-10-22 to 2008-12-26) | 10 | -5.1% | -10.5% to +2.8% | 0 | 0 | -2.4% | 0 |
| price over the EPP floor | 41 | -22.2% | -35.9% to -8.8% | 0 | 0 | -26.8% | 0 |
| price at or under the EPP floor | 11 | -5.3% | -14.4% to +2.8% | 0 | 0 | -3.8% | 0 |

- **CHEAP held on none of the 52.** The 40 dates to 2008-10-03 ($99.62-117.27, 13.7-16.2x the FY07 and FY08 guides, 6-20% over the floor)
  returned -35.9% to -8.8% over two years, dividends included, 0.2-37.1pp behind SPY (which returned -18.7% to +8.0%), and their m12-24
  average price was 22-34% under the entry; each sat through a 45-51% drawdown to the 2009-03-11 low ($58.18). Over three years they returned
  -33.4% to -11.9%, 15-32pp behind SPY.
- **The dates from the crash on fell less but lagged more.** The 12 dates from 2008-10-10 to 2008-12-26 ($72.26-90.75, from 0.5% over
  the floor to 21% under it) returned -17.6% to +2.8% over two years while SPY's rebound from its 2009 low gave +27.0% to +56.9%, so they
  trailed it by 36-58pp.
- **Every date of 2008 landed at the BEAR scenario price after two years** (the nearest of the four), and the two-year price was under the
  BEAR price on every one of them.

## 2009 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 53 | +6.0% | -12.5% to +44.5% | 3 | 1 | -0.9% | 4 |
| latest print Q3 2008 (2009-01-02 to 2009-01-16) | 3 | -3.3% | -12.5% to -2.7% | 0 | 0 | -8.0% | 0 |
| latest print Q4 2008 (2009-01-23 to 2009-04-17) | 13 | +16.8% | +1.4% to +44.5% | 3 | 0 | +3.3% | 3 |
| latest print Q1 2009 (2009-04-22 to 2009-07-17) | 13 | +3.5% | -5.3% to +10.8% | 0 | 0 | -7.6% | 0 |
| latest print Q2 2009 (2009-07-22 to 2009-10-16) | 13 | +2.1% | -0.4% to +11.4% | 0 | 0 | +0.2% | 0 |
| latest print Q3 2009 (2009-10-21 to 2009-12-31) | 11 | +9.0% | +4.1% to +19.0% | 0 | 1 | +0.8% | 1 |
| price at or under the EPP floor | 53 | +6.0% | -12.5% to +44.5% | 3 | 1 | -0.9% | 4 |

- **CHEAP held on 4 of 53: three by the hurdle at the low, one by 0.2pp.** The dates of 2009-02-27, 2009-03-06 and 2009-03-13 ($58.85-63.11,
  26-31% under the floor) cleared the hurdle (+35.1% to +44.5%), though SPY's +77.8% to +98.7% left them 38-54pp behind; 2009-10-21 ($69.66,
  the day after the Q3 2009 print, 23% under the floor) returned +19.0% against SPY's +18.9%. The other 49 returned -12.5% to +28.0%,
  0.4-68pp behind SPY.
- **The gap closed only at the end of the year.** The 31 dates from 2009-03-20 to 2009-10-16 trailed SPY by 7-57pp over two years and 4-48pp
  over three; the 11 dates from the Q3 2009 print were within 11pp of SPY over two years (one ahead), and over three they returned +29.8%
  to +48.8%, from 4.2pp behind SPY to 7.6pp ahead (5 of the 11 ahead).
- **The price ended near the BEAR case again.** Every 2009 date landed at the BEAR scenario price after two years, and the two-year price
  ($68.80-86.92 across both years) was under it on 48 of the 53.

## Across both years (hypotheses, not rules)

- **CHEAP held on 4 of 105; the call was robust to every variant and still wrong.** All eight robustness variants agreed on every date,
  and every encoding in the README's sensitivity list but one left all 105 calls CHEAP. The variants share the scenario frame, so their
  agreement says nothing about that frame.
- **The upside came from the history's start, not from the business.** With FY2002 excluded, BULL is the FY2003-FY2006 to FY2003-FY2008 EPS
  CAGR (+35.3% to +27.4%/yr) and XBULL +43.2%/yr, while BEAR is the 0% cap: Ratio B was 0.03-0.16 to 2008-10-03 and -0.20 to +0.03
  after, so the tier was BUY at any price the stock traded at. No date came near the BULL price; all 105 ended nearest the
  BEAR one. Hypothesis: a history that begins at a trough right after an excluded year turns a recovery into the BULL and XBULL rates. Test
  it on the other series whose history starts after excluded years (ACN and AAPL from FY2003, AVGO), never by changing LMT's rules.
- **The floor was set by a higher-multiple era.** The calendar-year lows of the 2003-2007 window (11.0-17.6x) put the floor at 12-14x;
  the stock traded at 8-12x the current-year guide from October 2008 to the end of 2009. Hypothesis: a
  five- to seven-year window that starts in a re-rating period sets the floor above the next trough; compare the windows of the other
  series that start in 2002-2003.
- **Buying lower helped in absolute terms only.** The dates at or under the floor returned a median of -5.3% (2008) and +6.0% (2009) over
  two years against -22.2% for the dates over it, but they lagged SPY's rebound on 63 of 64. One stock over two years mostly tests "buy
  lower" (retro/README.md, "Scoring a single stock").
- **The signals would have pointed the other way in 2008, by construction of the sensitivity only.** Every one of the 40 dates to
  2008-10-03 missed the hurdle and lagged SPY; with every signal at BEAR (the README's sensitivity) 37 of them would have been RICH. That is
  an observation about one stock and one year, not a reason to read the 2008 signals differently: test signal sets across tickers on the
  same dates.

# 2010-2013 (209 dates)

The 209 weekly dates from 2010-01-08 to 2013-12-31 were scored only after their point-in-time build was committed (6c6e1cee3) and their
decisions, controls, leak scan, sensitivities and firewall result were written to the README and committed (6085cda81); the outcomes were
computed on 2026-11-16, and nothing below was read for any 2010-2013 decision. Every date has its 6-month, 1-, 2- and 3-year horizons (the
last ends 2016-12-30). Total returns include the quarterly dividends ($0.63 to the ex-date of 2010-11-29, then $0.75, $1.00 from 2011-11-29,
$1.15 from 2012-11-29, $1.33 from 2013-11-27, $1.50 from 2014-11-26, $1.65 from 2015-11-27 and $1.82 from 2016-11-29): $5.26-11.64 a share
over two years, 6.8-12.0% of the entry price. No split falls in any horizon. The hurdle, the call checks and the medians are as above;
FAIR should land within 15pp of SPY over two years and RICH should miss the hurdle and lag SPY.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +26.0% | +10.3% to +45.8% | 21 | 18 | +8.3% | 21 |
| latest print Q3 2009 (2010-01-08 to 2010-01-22) | 3 | +13.9% | +13.6% to +17.3% | 0 | 0 | +2.5% | 0 |
| latest print Q4 2009 (2010-01-29 to 2010-04-16) | 12 | +16.8% | +10.3% to +23.6% | 0 | 0 | -3.5% | 0 |
| latest print Q1 2010 (2010-04-22 to 2010-07-23) | 14 | +14.0% | +10.5% to +26.8% | 0 | 0 | +2.4% | 0 |
| latest print Q2 2010 (2010-07-28 to 2010-10-15) | 12 | +38.8% | +27.4% to +44.3% | 10 | 7 | +18.0% | 10 |
| latest print Q3 2010 (2010-10-20 to 2010-12-31) | 11 | +41.2% | +38.0% to +45.8% | 11 | 11 | +26.0% | 11 |
| price over the EPP floor | 15 | +14.0% | +10.3% to +16.8% | 0 | 0 | -4.3% | 0 |
| price at or under the EPP floor | 37 | +36.5% | +13.3% to +45.8% | 21 | 18 | +15.0% | 21 |

- **CHEAP held on 21 of 52, all from 2010-08-13.** The 31 dates to 2010-08-06 ($73.93-86.90, 8% under to 11% over the floor) returned
  +10.3% to +28.7% over two years, 0.5-15.5pp behind SPY (+15.7% to +38.6%); each sat through the fall to the 2011-08-10 low ($66.87,
  a 19-23% drawdown). The 21 dates from 2010-08-13 ($68.80-73.27, 3-13% under the floor) returned +34.1% to +45.8%, every one over the
  hurdle and 18 ahead of SPY (by up to 27.0pp); over three years they returned +82.4% to +127.7%, 20.5-74.5pp ahead.
- **The dates under the BEAR price split the same way.** The three of January 2010 ($75.58-76.76) returned +13.6% to +17.3% and lagged
  SPY by 2.1-7.9pp; the five of September 2010 to 2010-10-01 ($69.61-73.13) returned +34.1% to +44.3%, 2.6-13.7pp ahead.
- **The two-year price landed at BEAR on 32 dates and BASE on 20,** never under BEAR and never over BASE ($79.98-94.10).

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +49.0% | +16.2% to +99.4% | 39 | 46 | +20.8% | 46 |
| latest print Q3 2010 (2011-01-07 to 2011-01-21) | 3 | +36.0% | +28.0% to +38.0% | 2 | 3 | +19.7% | 3 |
| latest print Q4 2010 (2011-01-28 to 2011-04-21) | 13 | +23.7% | +16.2% to +33.8% | 1 | 7 | +11.7% | 7 |
| latest print Q1 2011 (2011-04-27 to 2011-07-22) | 13 | +45.6% | +34.9% to +56.4% | 13 | 13 | +17.2% | 13 |
| latest print Q2 2011 (2011-07-27 to 2011-10-21) | 13 | +82.1% | +65.5% to +89.8% | 13 | 13 | +38.5% | 13 |
| latest print Q3 2011 (2011-10-27 to 2011-12-30) | 10 | +91.0% | +88.3% to +99.4% | 10 | 10 | +39.9% | 10 |
| price over the EPP floor | 24 | +32.0% | +16.2% to +56.4% | 11 | 18 | +14.1% | 18 |
| price at or under the EPP floor | 28 | +87.4% | +36.0% to +99.4% | 28 | 28 | +38.1% | 28 |

- **CHEAP held on 46 of 52.** The six misses, 2011-02-04 to 2011-03-18 ($79.85-81.81, 6-9% over the floor), returned +16.2% to +24.4% over
  two years, 0.8-2.1pp behind SPY; over three years they returned +98.7% to +123.4%, 58-75pp ahead.
- **The dates from the Q2 2011 print did best.** The 23 dates from 2011-07-27 to 2011-12-30 ($69.12-81.41, up to 16% under the floor; the
  2011-08-10 low falls among them) returned +65.5% to +99.4% over two years, 27.3-46.9pp ahead of SPY.
- **Every 2011 date beat SPY over three years** (+98.7% to +170.8%, 57.9-100.1pp ahead) and cleared the three-year hurdle. The two-year
  price landed at BASE on 44 dates and BULL on 8, over the BASE price on 28.

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +99.3% | +82.6% to +126.7% | 52 | 52 | +66.5% | 52 |
| latest print Q3 2011 (2012-01-06 to 2012-01-20) | 3 | +96.1% | +94.1% to +96.6% | 3 | 3 | +40.6% | 3 |
| latest print Q4 2011 (2012-01-27 to 2012-04-20) | 13 | +89.0% | +82.6% to +97.8% | 13 | 13 | +41.2% | 13 |
| latest print Q1 2012 (2012-04-27 to 2012-07-20) | 13 | +104.7% | +86.6% to +113.3% | 13 | 13 | +67.0% | 13 |
| latest print Q2 2012 (2012-07-25 to 2012-10-19) | 13 | +99.8% | +92.7% to +108.9% | 13 | 13 | +66.5% | 13 |
| latest print Q3 2012 (2012-10-25 to 2012-12-28) | 10 | +117.9% | +104.4% to +126.7% | 10 | 10 | +80.2% | 10 |
| price over the EPP floor | 52 | +99.3% | +82.6% to +126.7% | 52 | 52 | +66.5% | 52 |

- **CHEAP held on all 52, every date by both tests.** $79.98-94.37 (4-18% over the floor, 10.4-11.8x the guides) returned +82.6% to
  +126.7% over two years, 43.7-73.4pp ahead of SPY (+34.3% to +55.5%), and +128.7% to +167.5% over three. The largest drawdown within two
  years was 9.8-11.9%.
- **The two-year price passed the BULL case.** Every date landed at BULL, and the two-year price ($146.28-196.84) was over the BULL price
  on 26 of the 52.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 28 | +117.1% | +82.3% to +143.1% | 28 | 28 | +85.0% | 28 |
| class FAIR, legacy tier ACCUMULATE | 3 | +71.4% | +71.2% to +78.0% | 3 | 3 | +52.3% | 0 |
| class FAIR, legacy tier BUY | 8 | +77.9% | +72.9% to +83.6% | 8 | 8 | +57.2% | 0 |
| class RICH, legacy tier ACCUMULATE | 5 | +71.5% | +66.5% to +74.8% | 5 | 5 | +50.5% | 0 |
| class RICH, legacy tier AVOID | 2 | +55.7% | +55.4% to +55.7% | 2 | 2 | +36.6% | 0 |
| class RICH, legacy tier WATCHLIST | 7 | +65.0% | +55.2% to +68.5% | 7 | 7 | +43.7% | 0 |
| latest print Q3 2012 (2013-01-04 to 2013-01-18) | 3 | +118.1% | +116.8% to +119.1% | 3 | 3 | +81.6% | 3 |
| latest print Q4 2012 (2013-01-25 to 2013-04-19) | 13 | +127.7% | +113.4% to +143.1% | 13 | 13 | +92.6% | 13 |
| latest print Q1 2013 (2013-04-24 to 2013-07-19) | 13 | +88.2% | +82.3% to +110.9% | 13 | 13 | +72.0% | 12 |
| latest print Q2 2013 (2013-07-24 to 2013-10-18) | 13 | +75.8% | +66.5% to +82.4% | 13 | 13 | +53.5% | 0 |
| latest print Q3 2013 (2013-10-23 to 2013-12-31) | 11 | +65.0% | +55.2% to +74.8% | 11 | 11 | +43.7% | 0 |
| price over the EPP floor | 53 | +83.6% | +55.2% to +143.1% | 53 | 53 | +71.6% | 28 |

- **CHEAP held on all 28** (2013-01-04 to 2013-07-12, $87.22-112.53): +82.3% to +143.1% over two years, 48.5-99.3pp ahead of SPY.
- **FAIR held on none of 11 and RICH on none of 14, because the stock kept going.** The FAIR dates ($115.55-127.25, 42-51% over the floor)
  returned +71.2% to +83.6%, 47.8-57.8pp ahead of SPY, far outside FAIR's 15pp; the RICH dates ($128.00-148.66, 52-73% over the floor)
  returned +55.2% to +74.8%, cleared the hurdle and beat SPY by 39.2-51.4pp. The two AVOID dates (2013-12-27 and 2013-12-31, $148.13-148.66,
  15.6x the FY13 guide) returned +55.4% to +55.7% over two years and +80.5% to +81.8% over three.
- **Every 2013 date landed at BULL and over the BULL price** (two-year price $187.30-226.06).

## Across 2010-2013 (hypotheses, not rules)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 184 | +84.0% | +10.3% to +143.1% | 140 | 144 | +37.6% | 147 |
| class FAIR | 11 | +77.4% | +71.2% to +83.6% | 11 | 11 | +55.9% | 0 |
| class RICH | 14 | +66.5% | +55.2% to +74.8% | 14 | 14 | +44.9% | 0 |
| legacy tier BUY | 192 | +82.5% | +10.3% to +143.1% | 148 | 152 | +39.1% | 147 |
| legacy tier ACCUMULATE | 8 | +71.5% | +66.5% to +78.0% | 8 | 8 | +52.0% | 0 |
| legacy tier WATCHLIST | 7 | +65.0% | +55.2% to +68.5% | 7 | 7 | +43.7% | 0 |
| legacy tier AVOID | 2 | +55.7% | +55.4% to +55.7% | 2 | 2 | +36.6% | 0 |

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| CHEAP, price at or under the floor | 65 | +43.0% | +13.3% to +99.4% | 49 | 46 | +22.3% | 49 |
| CHEAP, 0-10% over the floor | 63 | +41.5% | +10.3% to +143.1% | 36 | 43 | +15.3% | 43 |
| CHEAP, 10-20% over the floor | 43 | +97.9% | +12.0% to +132.4% | 42 | 42 | +66.5% | 42 |
| CHEAP, over 20% over the floor | 13 | +90.1% | +82.3% to +117.1% | 13 | 13 | +72.0% | 13 |
| CHEAP, Ratio B under 0.1 | 45 | +38.0% | +13.1% to +89.8% | 28 | 25 | +18.3% | 28 |
| CHEAP, Ratio B 0.1-0.2 | 42 | +82.1% | +10.3% to +143.1% | 27 | 28 | +37.2% | 28 |
| CHEAP, Ratio B 0.2-0.4 | 89 | +95.3% | +16.2% to +126.7% | 77 | 83 | +53.5% | 83 |
| CHEAP, Ratio B 0.4 or more | 8 | +87.5% | +82.3% to +90.8% | 8 | 8 | +71.9% | 8 |

- **The order was right, the levels were not.** CHEAP held on 147 of 184 and FAIR and RICH on none of 25, yet the medians fall in class
  order (CHEAP +84.0%, FAIR +77.4%, RICH +66.5% over two years) and in tier order (BUY +82.5%, ACCUMULATE +71.5%, WATCHLIST +65.0%, AVOID
  +55.7%). Every FAIR and RICH date is one of the last 25 (from 2013-07-19), so the ordering is also the calendar: what came later returned
  less. Hypothesis: in a re-rating, FAIR and RICH read off the window's median and upper percentiles fire early; test it on other series
  whose multiples rose through their windows, never by changing LMT's rules.
- **The same CHEAP call that missed 101 of 105 in 2008-2009 held on 147 of 184.** The dates of 2008 lost money and then lagged SPY's rebound
  from March 2009; the dates from August 2010 on won as the price rose from $68.80-94.37 (9-12x the guides) to $148.66 at the end of 2013
  (15.6x) and $187-226 two years after the 2013 dates. The landing moved with it: BEAR on every date to 2009-12-31 and 32 dates of 2010,
  BASE on 20 of 2010 and 44 of 2011, BULL on 8 of 2011 and all of 2012-2013 (over the BULL price on 79). Hypothesis: the scenario frame says
  where the price could go, not when; the CHEAP call held only for dates from August 2010, almost two years after the price first fell to
  the floor (October 2008).
- **Buying under the floor helped within 2010 and 2011, not across the period.** In 2010 the dates at or under the floor returned a median
  of +36.5% against +14.0% over it, and in 2011 +87.4% against +32.0%; across the four years, CHEAP dates under the floor returned less
  (+43.0%) than those 10-20% over it (+97.9%), and those with Ratio B under 0.1 less (+38.0%) than those at 0.2-0.4 (+95.3%). Both splits
  mostly sort dates by year, as in 2008-2009: one stock tests "buy lower" within a year, not across years.
- **Signals at BEAR would have hurt here; in 2008 they would have helped.** The README's sensitivity with every signal at its BEAR value
  moves 106 classes from 2011-01-21 to 2013-10-11: as built 89 of them held, and as moved 13 would have (CHEAP to RICH: 76 held as built, 6
  as moved). Every signal at XBULL moves 25 FAIR and RICH dates of 2013 toward CHEAP: 0 held as built, 13 as moved. With the 2008
  observation above this is one stock, two regimes and opposite answers: no reason to read the signals differently.

# 2014-2017 (208 dates)

The 208 weekly dates from 2014-01-10 to 2017-12-29 were scored only after their point-in-time build was committed (0ebda7172) and their
decisions, controls, leak scan, sensitivities and firewall result were written to the README and committed (a9966ccba); the outcomes were
computed on 2026-11-17, and nothing below was read for any 2014-2017 decision. Every date has its 6-month, 1-, 2- and 3-year horizons (the
last ends 2020-12-29). Total returns include the quarterly dividends: $10.95-17.20 a share over two years, 5.3-7.9% of the entry price. No
split falls in any horizon; the 2016 exchange offer for Leidos shares was a choice offered to holders, not a distribution, so no price is
adjusted. The hurdle, the call checks and the medians are as above: RICH should miss the hurdle and lag SPY over two years.

Every 2014-2017 date is RICH, so the tables split the dates by tier, by latest print and by where the price stood against the EPP floor.

## 2014 (51 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 44 | +47.4% | +33.4% to +65.3% | 44 | 44 | +28.9% | 0 |
| class RICH, legacy tier WATCHLIST | 7 | +53.8% | +44.1% to +66.3% | 7 | 7 | +35.4% | 0 |
| latest print Q3 2013 (2014-01-10 to 2014-01-17) | 2 | +50.3% | +48.0% to +50.3% | 2 | 2 | +36.0% | 0 |
| latest print Q4 2013 (2014-01-24 to 2014-04-17) | 13 | +44.1% | +33.7% to +53.8% | 13 | 13 | +29.8% | 0 |
| latest print Q1 2014 (2014-04-23 to 2014-07-18) | 13 | +54.2% | +47.4% to +66.3% | 13 | 13 | +30.7% | 0 |
| latest print Q2 2014 (2014-07-23 to 2014-10-17) | 13 | +46.6% | +39.2% to +64.8% | 13 | 13 | +30.6% | 0 |
| latest print Q3 2014 (2014-10-22 to 2014-12-26) | 10 | +43.7% | +33.4% to +50.0% | 10 | 10 | +24.4% | 0 |
| price 0-100% over the EPP floor | 51 | +47.5% | +33.4% to +66.3% | 51 | 51 | +30.1% | 0 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 53 | +49.5% | +36.0% to +58.8% | 53 | 53 | +29.1% | 0 |
| latest print Q3 2014 (2015-01-02 to 2015-01-23) | 4 | +37.4% | +36.0% to +38.8% | 4 | 4 | +23.0% | 0 |
| latest print Q4 2014 (2015-01-28 to 2015-04-17) | 12 | +40.9% | +36.4% to +45.3% | 12 | 12 | +24.3% | 0 |
| latest print Q1 2015 (2015-04-22 to 2015-07-17) | 13 | +52.1% | +44.9% to +57.0% | 13 | 13 | +33.8% | 0 |
| latest print Q2 2015 (2015-07-21 to 2015-10-16) | 13 | +54.8% | +46.8% to +58.7% | 13 | 13 | +29.4% | 0 |
| latest print Q3 2015 (2015-10-21 to 2015-12-31) | 11 | +52.0% | +45.3% to +58.8% | 11 | 11 | +30.6% | 0 |
| price 0-100% over the EPP floor | 20 | +49.0% | +36.0% to +57.0% | 20 | 20 | +32.1% | 0 |
| price 100% or more over the EPP floor | 33 | +50.1% | +36.4% to +58.8% | 33 | 33 | +28.8% | 0 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +39.9% | +9.1% to +75.4% | 36 | 34 | +32.9% | 15 |
| latest print Q3 2015 (2016-01-08 to 2016-01-22) | 3 | +61.9% | +60.8% to +62.3% | 3 | 3 | +35.7% | 0 |
| latest print Q4 2015 (2016-01-27 to 2016-04-22) | 13 | +62.9% | +54.3% to +75.4% | 13 | 13 | +38.2% | 0 |
| latest print Q1 2016 (2016-04-27 to 2016-07-15) | 12 | +38.8% | +24.5% to +44.1% | 8 | 7 | +31.7% | 4 |
| latest print Q2 2016 (2016-07-20 to 2016-10-21) | 14 | +43.6% | +24.2% to +55.2% | 11 | 10 | +32.7% | 3 |
| latest print Q3 2016 (2016-10-26 to 2016-12-30) | 10 | +20.3% | +9.1% to +33.1% | 1 | 1 | +29.0% | 8 |
| price 0-100% over the EPP floor | 2 | +74.7% | +72.8% to +74.7% | 2 | 2 | +44.1% | 0 |
| price 100% or more over the EPP floor | 50 | +39.6% | +9.1% to +75.4% | 34 | 32 | +32.7% | 15 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +27.7% | +8.9% to +36.9% | 10 | 38 | +10.0% | 14 |
| latest print Q3 2016 (2017-01-06 to 2017-01-20) | 3 | +15.3% | +8.9% to +15.8% | 0 | 0 | +24.6% | 3 |
| latest print Q4 2016 (2017-01-25 to 2017-04-21) | 13 | +20.6% | +14.8% to +21.7% | 0 | 2 | +16.5% | 11 |
| latest print Q1 2017 (2017-04-26 to 2017-07-14) | 12 | +31.8% | +25.1% to +36.9% | 5 | 12 | +12.1% | 0 |
| latest print Q2 2017 (2017-07-19 to 2017-10-20) | 14 | +30.4% | +21.7% to +33.2% | 4 | 14 | +6.9% | 0 |
| latest print Q3 2017 (2017-10-25 to 2017-12-29) | 10 | +28.0% | +24.0% to +32.5% | 1 | 10 | +7.8% | 0 |
| price 0-100% over the EPP floor | 11 | +21.3% | +14.8% to +27.4% | 0 | 2 | +16.4% | 9 |
| price 100% or more over the EPP floor | 41 | +28.5% | +8.9% to +36.9% | 10 | 36 | +8.3% | 5 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 208 | +41.3% | +8.9% to +75.4% | 150 | 176 | +27.9% | 29 |
| legacy tier AVOID | 201 | +40.8% | +8.9% to +75.4% | 143 | 169 | +27.5% | 29 |
| legacy tier WATCHLIST | 7 | +53.8% | +44.1% to +66.3% | 7 | 7 | +35.4% | 0 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| RICH, 0-75% over the floor | 29 | +51.7% | +33.7% to +66.3% | 29 | 29 | +31.2% | 0 |
| RICH, 75-100% over the floor | 55 | +40.9% | +14.8% to +74.7% | 44 | 46 | +26.2% | 9 |
| RICH, 100-125% over the floor | 89 | +44.5% | +20.6% to +75.4% | 68 | 87 | +26.8% | 1 |
| RICH, 125-1000000000.0% over the floor | 35 | +26.7% | +8.9% to +40.2% | 9 | 14 | +25.8% | 19 |
| RICH, Ratio B finite | 93 | +48.2% | +33.4% to +75.4% | 93 | 93 | +31.0% | 0 |
| RICH, Ratio B infinite (price over BULL) | 115 | +31.8% | +8.9% to +70.9% | 57 | 83 | +24.3% | 29 |

- **RICH held on none of the 51.** $147.76-196.84 (14.2-17.7x the FY13 and FY14 guides, 58-96% over the floor) returned +33.4% to +66.3%
  over two years, 20.9-53.5pp ahead of SPY (+5.8% to +17.9%), and +72.2% to +93.5% over three, 37.4-60.9pp ahead. The largest drawdown
  within two years was 10.2-13.5%.
- **The seven WATCHLIST dates did no worse than the AVOID ones** (+44.1% to +66.3% against +33.4% to +65.3%).
- **Every 2014 date landed at BULL and over the BULL price** (two-year price $206.08-267.24); none passed XBULL.

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 53 | +49.5% | +36.0% to +58.8% | 53 | 53 | +29.1% | 0 |
| latest print Q3 2014 (2015-01-02 to 2015-01-23) | 4 | +37.4% | +36.0% to +38.8% | 4 | 4 | +23.0% | 0 |
| latest print Q4 2014 (2015-01-28 to 2015-04-17) | 12 | +40.9% | +36.4% to +45.3% | 12 | 12 | +24.3% | 0 |
| latest print Q1 2015 (2015-04-22 to 2015-07-17) | 13 | +52.1% | +44.9% to +57.0% | 13 | 13 | +33.8% | 0 |
| latest print Q2 2015 (2015-07-21 to 2015-10-16) | 13 | +54.8% | +46.8% to +58.7% | 13 | 13 | +29.4% | 0 |
| latest print Q3 2015 (2015-10-21 to 2015-12-31) | 11 | +52.0% | +45.3% to +58.8% | 11 | 11 | +30.6% | 0 |
| price 0-100% over the EPP floor | 20 | +49.0% | +36.0% to +57.0% | 20 | 20 | +32.1% | 0 |
| price 100% or more over the EPP floor | 33 | +50.1% | +36.4% to +58.8% | 33 | 33 | +28.8% | 0 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +39.9% | +9.1% to +75.4% | 36 | 34 | +32.9% | 15 |
| latest print Q3 2015 (2016-01-08 to 2016-01-22) | 3 | +61.9% | +60.8% to +62.3% | 3 | 3 | +35.7% | 0 |
| latest print Q4 2015 (2016-01-27 to 2016-04-22) | 13 | +62.9% | +54.3% to +75.4% | 13 | 13 | +38.2% | 0 |
| latest print Q1 2016 (2016-04-27 to 2016-07-15) | 12 | +38.8% | +24.5% to +44.1% | 8 | 7 | +31.7% | 4 |
| latest print Q2 2016 (2016-07-20 to 2016-10-21) | 14 | +43.6% | +24.2% to +55.2% | 11 | 10 | +32.7% | 3 |
| latest print Q3 2016 (2016-10-26 to 2016-12-30) | 10 | +20.3% | +9.1% to +33.1% | 1 | 1 | +29.0% | 8 |
| price 0-100% over the EPP floor | 2 | +74.7% | +72.8% to +74.7% | 2 | 2 | +44.1% | 0 |
| price 100% or more over the EPP floor | 50 | +39.6% | +9.1% to +75.4% | 34 | 32 | +32.7% | 15 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +27.7% | +8.9% to +36.9% | 10 | 38 | +10.0% | 14 |
| latest print Q3 2016 (2017-01-06 to 2017-01-20) | 3 | +15.3% | +8.9% to +15.8% | 0 | 0 | +24.6% | 3 |
| latest print Q4 2016 (2017-01-25 to 2017-04-21) | 13 | +20.6% | +14.8% to +21.7% | 0 | 2 | +16.5% | 11 |
| latest print Q1 2017 (2017-04-26 to 2017-07-14) | 12 | +31.8% | +25.1% to +36.9% | 5 | 12 | +12.1% | 0 |
| latest print Q2 2017 (2017-07-19 to 2017-10-20) | 14 | +30.4% | +21.7% to +33.2% | 4 | 14 | +6.9% | 0 |
| latest print Q3 2017 (2017-10-25 to 2017-12-29) | 10 | +28.0% | +24.0% to +32.5% | 1 | 10 | +7.8% | 0 |
| price 0-100% over the EPP floor | 11 | +21.3% | +14.8% to +27.4% | 0 | 2 | +16.4% | 9 |
| price 100% or more over the EPP floor | 41 | +28.5% | +8.9% to +36.9% | 10 | 36 | +8.3% | 5 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 208 | +41.3% | +8.9% to +75.4% | 150 | 176 | +27.9% | 29 |
| legacy tier AVOID | 201 | +40.8% | +8.9% to +75.4% | 143 | 169 | +27.5% | 29 |
| legacy tier WATCHLIST | 7 | +53.8% | +44.1% to +66.3% | 7 | 7 | +35.4% | 0 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| RICH, 0-75% over the floor | 29 | +51.7% | +33.7% to +66.3% | 29 | 29 | +31.2% | 0 |
| RICH, 75-100% over the floor | 55 | +40.9% | +14.8% to +74.7% | 44 | 46 | +26.2% | 9 |
| RICH, 100-125% over the floor | 89 | +44.5% | +20.6% to +75.4% | 68 | 87 | +26.8% | 1 |
| RICH, 125-1000000000.0% over the floor | 35 | +26.7% | +8.9% to +40.2% | 9 | 14 | +25.8% | 19 |
| RICH, Ratio B finite | 93 | +48.2% | +33.4% to +75.4% | 93 | 93 | +31.0% | 0 |
| RICH, Ratio B infinite (price over BULL) | 115 | +31.8% | +8.9% to +70.9% | 57 | 83 | +24.3% | 29 |

- **RICH held on none of the 53.** $187.30-226.06 (17.0-20.0x the FY15 and FY16 guides, the 95th-100th percentile, 89-122% over the floor)
  returned +36.0% to +58.8% over two years, 15.6-38.3pp ahead of SPY, and every date beat SPY over three years too (+22.5% to +93.0%,
  1.5-55.6pp ahead; 44 cleared the three-year hurdle).
- **The price passed the scenarios built on it.** Every 2015 date ended over the BULL price ($249.94-322.76 two years on), 47 nearest XBULL
  and 7 over the XBULL price itself, while Ratio B was infinite (the price already over BULL) on 25 of them.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +39.9% | +9.1% to +75.4% | 36 | 34 | +32.9% | 15 |
| latest print Q3 2015 (2016-01-08 to 2016-01-22) | 3 | +61.9% | +60.8% to +62.3% | 3 | 3 | +35.7% | 0 |
| latest print Q4 2015 (2016-01-27 to 2016-04-22) | 13 | +62.9% | +54.3% to +75.4% | 13 | 13 | +38.2% | 0 |
| latest print Q1 2016 (2016-04-27 to 2016-07-15) | 12 | +38.8% | +24.5% to +44.1% | 8 | 7 | +31.7% | 4 |
| latest print Q2 2016 (2016-07-20 to 2016-10-21) | 14 | +43.6% | +24.2% to +55.2% | 11 | 10 | +32.7% | 3 |
| latest print Q3 2016 (2016-10-26 to 2016-12-30) | 10 | +20.3% | +9.1% to +33.1% | 1 | 1 | +29.0% | 8 |
| price 0-100% over the EPP floor | 2 | +74.7% | +72.8% to +74.7% | 2 | 2 | +44.1% | 0 |
| price 100% or more over the EPP floor | 50 | +39.6% | +9.1% to +75.4% | 34 | 32 | +32.7% | 15 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +27.7% | +8.9% to +36.9% | 10 | 38 | +10.0% | 14 |
| latest print Q3 2016 (2017-01-06 to 2017-01-20) | 3 | +15.3% | +8.9% to +15.8% | 0 | 0 | +24.6% | 3 |
| latest print Q4 2016 (2017-01-25 to 2017-04-21) | 13 | +20.6% | +14.8% to +21.7% | 0 | 2 | +16.5% | 11 |
| latest print Q1 2017 (2017-04-26 to 2017-07-14) | 12 | +31.8% | +25.1% to +36.9% | 5 | 12 | +12.1% | 0 |
| latest print Q2 2017 (2017-07-19 to 2017-10-20) | 14 | +30.4% | +21.7% to +33.2% | 4 | 14 | +6.9% | 0 |
| latest print Q3 2017 (2017-10-25 to 2017-12-29) | 10 | +28.0% | +24.0% to +32.5% | 1 | 10 | +7.8% | 0 |
| price 0-100% over the EPP floor | 11 | +21.3% | +14.8% to +27.4% | 0 | 2 | +16.4% | 9 |
| price 100% or more over the EPP floor | 41 | +28.5% | +8.9% to +36.9% | 10 | 36 | +8.3% | 5 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 208 | +41.3% | +8.9% to +75.4% | 150 | 176 | +27.9% | 29 |
| legacy tier AVOID | 201 | +40.8% | +8.9% to +75.4% | 143 | 169 | +27.5% | 29 |
| legacy tier WATCHLIST | 7 | +53.8% | +44.1% to +66.3% | 7 | 7 | +35.4% | 0 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| RICH, 0-75% over the floor | 29 | +51.7% | +33.7% to +66.3% | 29 | 29 | +31.2% | 0 |
| RICH, 75-100% over the floor | 55 | +40.9% | +14.8% to +74.7% | 44 | 46 | +26.2% | 9 |
| RICH, 100-125% over the floor | 89 | +44.5% | +20.6% to +75.4% | 68 | 87 | +26.8% | 1 |
| RICH, 125-1000000000.0% over the floor | 35 | +26.7% | +8.9% to +40.2% | 9 | 14 | +25.8% | 19 |
| RICH, Ratio B finite | 93 | +48.2% | +33.4% to +75.4% | 93 | 93 | +31.0% | 0 |
| RICH, Ratio B infinite (price over BULL) | 115 | +31.8% | +8.9% to +70.9% | 57 | 83 | +24.3% | 29 |

- **RICH held on 15 of 52, all from the summer.** The 16 dates to 2016-04-22, from the January low ($206.08, 17.8x the first FY16 guide)
  to the Q4 2015 print, returned +54.3% to +75.4% over two years, 8.6-29.5pp ahead of SPY. Of the 29 dates from 2016-06-17 ($230.52-267.62),
  18 trailed SPY by 0.6-11.8pp and 15 of those also missed the hurdle (+9.1% to +31.5%): the call held there.
- **The IS&GS seam's 13 dates (2016-10-26 to 2017-01-20) are where it held most:** 8 of the 10 of 2016 held, and the three of January 2017
  below. The README's sensitivity reading the guide on the pro forma 2015 base moves no class there, so this says nothing for or against
  either reading.
- **Over three years the misses narrow.** 43 of the 52 beat SPY over three years (+37.3% to +75.5%; -8.1pp to +31.3pp), 30 cleared the
  three-year hurdle. The two-year price was over the BULL price on all 52 and over XBULL on 48.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH, legacy tier AVOID | 52 | +27.7% | +8.9% to +36.9% | 10 | 38 | +10.0% | 14 |
| latest print Q3 2016 (2017-01-06 to 2017-01-20) | 3 | +15.3% | +8.9% to +15.8% | 0 | 0 | +24.6% | 3 |
| latest print Q4 2016 (2017-01-25 to 2017-04-21) | 13 | +20.6% | +14.8% to +21.7% | 0 | 2 | +16.5% | 11 |
| latest print Q1 2017 (2017-04-26 to 2017-07-14) | 12 | +31.8% | +25.1% to +36.9% | 5 | 12 | +12.1% | 0 |
| latest print Q2 2017 (2017-07-19 to 2017-10-20) | 14 | +30.4% | +21.7% to +33.2% | 4 | 14 | +6.9% | 0 |
| latest print Q3 2017 (2017-10-25 to 2017-12-29) | 10 | +28.0% | +24.0% to +32.5% | 1 | 10 | +7.8% | 0 |
| price 0-100% over the EPP floor | 11 | +21.3% | +14.8% to +27.4% | 0 | 2 | +16.4% | 9 |
| price 100% or more over the EPP floor | 41 | +28.5% | +8.9% to +36.9% | 10 | 36 | +8.3% | 5 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 208 | +41.3% | +8.9% to +75.4% | 150 | 176 | +27.9% | 29 |
| legacy tier AVOID | 201 | +40.8% | +8.9% to +75.4% | 143 | 169 | +27.5% | 29 |
| legacy tier WATCHLIST | 7 | +53.8% | +44.1% to +66.3% | 7 | 7 | +35.4% | 0 |
| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| RICH, 0-75% over the floor | 29 | +51.7% | +33.7% to +66.3% | 29 | 29 | +31.2% | 0 |
| RICH, 75-100% over the floor | 55 | +40.9% | +14.8% to +74.7% | 44 | 46 | +26.2% | 9 |
| RICH, 100-125% over the floor | 89 | +44.5% | +20.6% to +75.4% | 68 | 87 | +26.8% | 1 |
| RICH, 125-1000000000.0% over the floor | 35 | +26.7% | +8.9% to +40.2% | 9 | 14 | +25.8% | 19 |
| RICH, Ratio B finite | 93 | +48.2% | +33.4% to +75.4% | 93 | 93 | +31.0% | 0 |
| RICH, Ratio B infinite (price over BULL) | 115 | +31.8% | +8.9% to +70.9% | 57 | 83 | +24.3% | 29 |

- **RICH held on 14 of 52, from 2017-01-06 to 2017-04-21.** Those dates ($254.46-273.09, 20.5-22.0x the FY16 and FY17 guides) returned
  +8.9% to +21.7% over two years, 0.2-9.1pp behind SPY; the other two of that stretch (2017-01-25 and 2017-02-10) beat SPY by 0.5-0.6pp.
  Over three years the 14 returned +17.5% to +76.3%, 6.7-28.2pp ahead of SPY. From its 2018 high the price fell 32.1% to $245.22 on
  2018-12-24, inside every 2017 date's two-year window.
- **The 36 dates from the Q1 2017 print on beat SPY over two years** ($270.35-322.82, 22.0-25.7x the FY17 guides, the 99th-100th
  percentile): +21.7% to +36.9%, 0.1-11.8pp ahead, so RICH missed by beating SPY while 26 of them missed the hurdle. Over three years they
  returned +17.9% to +56.8%, from 26.7pp behind SPY to 26.2pp ahead.
- **Every 2017 date ended over the BULL price** (two-year price $265.04-393.60), 42 nearest XBULL and 13 over it.

## Across 2014-2017 (hypotheses, not rules)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH | 208 | +41.3% | +8.9% to +75.4% | 150 | 176 | +27.9% | 29 |
| legacy tier AVOID | 201 | +40.8% | +8.9% to +75.4% | 143 | 169 | +27.5% | 29 |
| legacy tier WATCHLIST | 7 | +53.8% | +44.1% to +66.3% | 7 | 7 | +35.4% | 0 |

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| RICH, 0-75% over the floor | 29 | +51.7% | +33.7% to +66.3% | 29 | 29 | +31.2% | 0 |
| RICH, 75-100% over the floor | 55 | +40.9% | +14.8% to +74.7% | 44 | 46 | +26.2% | 9 |
| RICH, 100-125% over the floor | 89 | +44.5% | +20.6% to +75.4% | 68 | 87 | +26.8% | 1 |
| RICH, 125% or more over the floor | 35 | +26.7% | +8.9% to +40.2% | 9 | 14 | +25.8% | 19 |
| RICH, Ratio B finite | 93 | +48.2% | +33.4% to +75.4% | 93 | 93 | +31.0% | 0 |
| RICH, Ratio B infinite (price over BULL) | 115 | +31.8% | +8.9% to +70.9% | 57 | 83 | +24.3% | 29 |

- **RICH was the call on all 208 dates and held on 29, all from mid-2016.** The stock returned a median of +41.3% over two years, cleared
  the hurdle on 150 dates and beat SPY on 176; over three years it beat SPY on 174 and cleared the three-year hurdle on 135. Every one of
  the 208 ended over the BULL price two years on (140 nearest XBULL, 68 over the XBULL price). With 2010-2013's FAIR and RICH dates
  (0 of 25 held), the method's FAIR and RICH calls on LMT held on 29 of 233, all of them at 20.5-22.1x the current-year guide.
- **The window's median was the de-rated era's.** The P/E window of 2014-2017 holds 2008-2012, when the stock traded at 8-12x the guides,
  so the median stayed at 12.6-13.6x while the stock re-rated from 14x to 25x; from 2015 every date sat at the 92nd-100th percentile, and
  the valuation factor and the BASE exit at the median priced a return to the 2008-2012 multiple that never came. Hypothesis: after a
  re-rating, a ten-year window anchored in the de-rated years reads every later price as rich; it mirrors 2008-2009, where a window from
  the 2003-2007 re-rating set the floor above the next trough. Test it on other series whose windows straddle a re-rating (the 2010-2013
  note above), never by changing LMT's rules.
- **The more over the floor, the lower the return, but not by enough to make RICH right.** Dates under 75% over the floor returned a
  median of +51.7% and held on none; dates 125% or more over it +26.7%, holding on 19 of 35. The split is mostly the calendar again (the
  highest gaps came last, in late 2016 and 2017).
- **Ratio B infinite (the price over BULL) marked the lower returns,** +31.8% median against +48.2% for the finite dates, and all 29 held
  calls are infinite-Ratio-B dates. One stock, one re-rating: a hypothesis for the cross-ticker tests, not a rule.
- **The signals did not decide it.** Every signal at BEAR moves no class; every signal at XBULL moves 22 dates of 2014 to FAIR, and none of
  those would have held as FAIR (each beat SPY by at least 25.9pp, outside FAIR's 15pp). The proxy composite (1.55-2.55) was below the market
  composite (2.69-3.93) on every date.

# 2018-2021 (209 dates)

The 209 weekly dates from 2018-01-05 to 2021-12-31 were scored only after their point-in-time build was committed (806b18c2f) and their
decisions, controls, leak scan, sensitivities and firewall result were written to the README and committed (acfb06dcc); the outcomes were
computed on 2026-11-17, and nothing below was read for any 2018-2021 decision. Every date has its 6-month, 1-, 2- and 3-year horizons (the
last ends 2024-12-30). Total returns include the quarterly dividends: $16.00-23.55 a share over two years,
4.5-7.3% of the entry price. No split falls in any horizon. The hurdle, the call checks and the medians are as above:
CHEAP should clear the hurdle or beat SPY, FAIR land within 15pp of SPY and RICH miss the hurdle and lag SPY, over two years.

## 2018 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 2 | +43.5% | +42.8% to +43.5% | 2 | 0 | +48.5% | 2 |
| class CHEAP, legacy tier WATCHLIST | 2 | +33.5% | +30.9% to +33.5% | 1 | 0 | +33.9% | 1 |
| class FAIR, legacy tier AVOID | 1 | +26.2% | +26.2% to +26.2% | 0 | 0 | +23.5% | 1 |
| class FAIR, legacy tier WATCHLIST | 4 | +31.3% | +23.9% to +31.8% | 0 | 0 | +28.2% | 4 |
| class RICH, legacy tier AVOID | 43 | +23.3% | -12.5% to +34.1% | 3 | 31 | +16.8% | 11 |
| latest print Q3 2017 (2018-01-05 to 2018-01-26) | 4 | +30.7% | +28.2% to +33.4% | 1 | 4 | +5.9% | 0 |
| latest print Q4 2017 (2018-01-30 to 2018-04-20) | 12 | +15.2% | -12.5% to +33.7% | 1 | 8 | +8.8% | 4 |
| latest print Q1 2018 (2018-04-25 to 2018-07-20) | 13 | +26.2% | +16.5% to +34.1% | 1 | 11 | +20.1% | 1 |
| latest print Q2 2018 (2018-07-25 to 2018-10-19) | 13 | +23.3% | +15.9% to +30.1% | 0 | 8 | +17.2% | 5 |
| latest print Q3 2018 (2018-10-24 to 2018-12-28) | 10 | +31.3% | +22.1% to +43.5% | 3 | 0 | +29.6% | 9 |
| price 25-50% over the EPP floor | 4 | +42.8% | +30.9% to +43.5% | 3 | 0 | +45.6% | 3 |
| price 50% or more over the EPP floor | 48 | +24.3% | -12.5% to +34.1% | 3 | 31 | +17.2% | 16 |

- **RICH held on 11 of 43.** The dates to 2018-11-09 ($295-361, 17.9-26.5x the FY17 and FY18 guides) returned -12.5% to +34.1% over two
  years, ahead of SPY on 31 (SPY's two years ran into the 2020 crash and rebound: -9.3% to +57.5%); the 11 that held are the ones whose
  two years ended around the February-March 2020 sell-off or from July to November 2020, when the stock lagged the rebound. Over three years no 2018 date cleared the hurdle or beat SPY (-0.4% to +46.7%, 22.9-57.6pp behind).
- **The four CHEAP dates of December 2018 ($256.55-287.70)** cleared the hurdle on three (+30.9% to +43.5%) but lagged SPY, which rose from
  its December 2018 low; the five FAIR dates of October and November all landed within 15pp of SPY.
- The two-year price landed at BULL on 36 dates, XBULL on 8 and BASE on 8, and over the BULL price on 34.

## 2019 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 11 | +23.5% | +16.0% to +37.1% | 1 | 0 | +23.1% | 1 |
| class CHEAP, legacy tier WATCHLIST | 6 | +26.2% | +14.0% to +31.4% | 0 | 0 | +19.0% | 0 |
| class FAIR, legacy tier AVOID | 3 | +8.4% | +7.9% to +9.9% | 0 | 0 | +0.2% | 0 |
| class FAIR, legacy tier WATCHLIST | 25 | +3.4% | -7.7% to +30.8% | 0 | 0 | -2.1% | 0 |
| class RICH, legacy tier WATCHLIST | 7 | -6.9% | -8.3% to -5.3% | 0 | 0 | -7.7% | 7 |
| latest print Q3 2018 (2019-01-04 to 2019-01-25) | 4 | +29.4% | +26.2% to +37.1% | 1 | 0 | +36.2% | 1 |
| latest print Q4 2018 (2019-01-30 to 2019-04-18) | 12 | +23.5% | +14.0% to +31.5% | 0 | 0 | +21.6% | 0 |
| latest print Q1 2019 (2019-04-24 to 2019-07-19) | 13 | +16.7% | +7.9% to +21.4% | 0 | 0 | +5.4% | 0 |
| latest print Q2 2019 (2019-07-24 to 2019-10-18) | 13 | -1.2% | -7.7% to +8.5% | 0 | 0 | -4.2% | 0 |
| latest print Q3 2019 (2019-10-23 to 2019-12-27) | 10 | -6.6% | -8.3% to +5.8% | 0 | 0 | -7.1% | 7 |
| price under 25% over the EPP floor | 15 | +26.2% | +14.0% to +37.1% | 1 | 0 | +23.1% | 1 |
| price 25-50% over the EPP floor | 23 | +8.5% | -7.4% to +30.8% | 0 | 0 | +2.3% | 3 |
| price 50% or more over the EPP floor | 14 | -3.7% | -8.3% to +9.9% | 0 | 0 | -5.0% | 4 |

- **Every 2019 date lagged SPY over two years** (SPY +42.5% to +61.0%, the stock -8.3% to +37.1%), so CHEAP held on 1 of 17 (by the
  hurdle, 2019-01-04) and FAIR on none of 28 (each 17-61pp behind, outside its 15pp).
- **RICH held on all 7, at the multiple's high:** 2019-11-15 to 2019-12-27 ($386.47-393.60) returned -8.3% to -5.3% over two years, 52.8-61.8pp
  behind SPY, and +26.7% to +34.0% over three. Every 2019 date landed at BASE two years on, under the BASE price on 42.

## 2020 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier ACCUMULATE | 2 | +29.4% | +22.9% to +29.4% | 0 | 1 | +10.2% | 1 |
| class CHEAP, legacy tier BUY | 18 | +39.3% | +23.4% to +53.5% | 13 | 11 | +13.0% | 15 |
| class FAIR, legacy tier ACCUMULATE | 23 | +14.8% | +5.5% to +30.0% | 0 | 1 | +1.3% | 15 |
| class FAIR, legacy tier WATCHLIST | 3 | +12.9% | -4.9% to +21.7% | 0 | 0 | -6.4% | 0 |
| class RICH, legacy tier AVOID | 5 | -7.7% | -9.4% to -4.7% | 0 | 0 | -15.5% | 5 |
| class RICH, legacy tier WATCHLIST | 2 | -6.0% | -7.0% to -6.0% | 0 | 0 | -17.0% | 2 |
| latest print Q3 2019 (2020-01-03 to 2020-01-24) | 4 | -7.7% | -9.4% to -7.3% | 0 | 0 | -13.3% | 4 |
| latest print Q4 2019 (2020-01-29 to 2020-04-17) | 12 | +25.2% | -7.0% to +53.5% | 4 | 0 | -1.2% | 7 |
| latest print Q1 2020 (2020-04-22 to 2020-07-17) | 13 | +20.7% | +12.9% to +26.5% | 0 | 1 | +3.7% | 4 |
| latest print Q2 2020 (2020-07-22 to 2020-10-16) | 13 | +13.8% | +5.5% to +18.4% | 0 | 1 | +2.2% | 12 |
| latest print Q3 2020 (2020-10-21 to 2020-12-31) | 11 | +39.8% | +29.4% to +44.7% | 9 | 11 | +14.9% | 11 |
| price under 25% over the EPP floor | 5 | +39.9% | +22.9% to +53.5% | 3 | 1 | +12.5% | 3 |
| price 25-50% over the EPP floor | 42 | +20.6% | -9.4% to +44.7% | 10 | 12 | +3.8% | 31 |
| price 50% or more over the EPP floor | 6 | +12.9% | -9.0% to +21.7% | 0 | 0 | -6.1% | 4 |

- **RICH held on all 7 again** (2020-01-03 to 2020-02-14, $413.74-439.17, the price's high before the pandemic sell-off): -9.4% to -4.7% over
  two years, 40.4-61.1pp behind SPY.
- **CHEAP held on 16 of 20 and FAIR on 15 of 26.** The CHEAP dates (around the March 2020 low, in May to July and from the Q3 2020
  print; $291-375) returned +22.9% to +53.5%; the FAIR dates between them ($368.50-427.80) returned -4.9% to +30.0%, within 15pp of SPY on
  15. Over three
  years only 9 of the 53 beat SPY. Every 2020 date landed at BASE two years on, under the BASE price on all 53.

## 2021 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 52 | +32.4% | +19.8% to +51.3% | 27 | 52 | +28.1% | 52 |
| latest print Q3 2020 (2021-01-08 to 2021-01-22) | 3 | +36.9% | +35.9% to +47.3% | 3 | 3 | +28.5% | 3 |
| latest print Q4 2020 (2021-01-27 to 2021-04-16) | 12 | +44.8% | +30.3% to +51.3% | 11 | 12 | +30.6% | 12 |
| latest print Q1 2021 (2021-04-21 to 2021-07-23) | 14 | +25.7% | +21.1% to +30.4% | 0 | 14 | +18.2% | 14 |
| latest print Q2 2021 (2021-07-27 to 2021-10-22) | 13 | +29.0% | +19.8% to +33.2% | 3 | 13 | +28.4% | 13 |
| latest print Q3 2021 (2021-10-27 to 2021-12-31) | 10 | +38.0% | +34.2% to +41.7% | 10 | 10 | +34.4% | 10 |
| price under 25% over the EPP floor | 52 | +32.4% | +19.8% to +51.3% | 27 | 52 | +28.1% | 52 |

- **CHEAP held on all 52**, every date by beating SPY: $330.25-394.10 (12.2-15.0x the FY21 guides, the 8th-34th percentile, 5-25% over
  the floor) returned +19.8% to +51.3% over two years against SPY's -6.7% to +11.6%, 16.9-47.7pp ahead; 27 also cleared the hurdle. Over
  three years 37 of the 52 beat SPY. Every date landed at BASE, under the BASE price.

## Across 2018-2021 (hypotheses, not rules)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 93 | +31.2% | +14.0% to +53.5% | 44 | 64 | +22.5% | 72 |
| class FAIR | 59 | +13.8% | -7.7% to +31.8% | 0 | 1 | +1.1% | 20 |
| class RICH | 57 | +21.2% | -12.5% to +34.1% | 3 | 31 | +10.6% | 25 |
| legacy tier ACCUMULATE | 38 | +18.3% | +5.5% to +43.5% | 3 | 2 | +3.8% | 19 |
| legacy tier AVOID | 52 | +22.7% | -12.5% to +34.1% | 3 | 31 | +13.8% | 17 |
| legacy tier BUY | 70 | +33.5% | +19.8% to +53.5% | 40 | 63 | +22.5% | 67 |
| legacy tier WATCHLIST | 49 | +7.2% | -8.3% to +33.5% | 1 | 0 | -2.1% | 14 |

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| CHEAP, under 25% over the floor | 71 | +30.6% | +14.0% to +53.5% | 31 | 53 | +26.1% | 56 |
| CHEAP, 25-50% over the floor | 22 | +34.9% | +20.1% to +44.7% | 13 | 11 | +13.0% | 16 |
| FAIR, under 25% over the floor | 1 | +25.2% | +25.2% to +25.2% | 0 | 0 | -3.9% | 0 |
| FAIR, 25-50% over the floor | 39 | +14.2% | -7.4% to +30.8% | 0 | 1 | +2.2% | 13 |
| FAIR, 50% or more over the floor | 19 | +9.9% | -7.7% to +31.8% | 0 | 0 | -0.1% | 7 |
| RICH, 25-50% over the floor | 8 | -6.9% | -9.4% to -4.7% | 0 | 0 | -13.2% | 8 |
| RICH, 50% or more over the floor | 49 | +22.7% | -12.5% to +34.1% | 3 | 31 | +13.8% | 17 |
| Ratio B 0-0.5 | 43 | +33.5% | +19.8% to +53.5% | 25 | 42 | +29.1% | 43 |
| Ratio B 0.5-1.0 | 56 | +25.6% | +6.3% to +44.7% | 18 | 23 | +11.2% | 41 |
| Ratio B 1.0-2.0 | 66 | +9.9% | -9.4% to +33.5% | 1 | 0 | +0.4% | 21 |
| Ratio B 2.0 or more | 30 | +23.3% | -9.0% to +34.1% | 1 | 21 | +18.2% | 8 |
| Ratio B infinite | 14 | +26.2% | -12.5% to +33.7% | 2 | 10 | +6.7% | 4 |

- **CHEAP did best, then RICH, then FAIR.** CHEAP held on 72 of 93 (median +31.2% over two years), FAIR on 20 of 59 (+13.8%) and RICH on 25
  of 57 (+21.2%); by tier BUY returned +33.5%, AVOID +22.7%, ACCUMULATE +18.3% and WATCHLIST +7.2%. RICH returned more than FAIR because
  most RICH dates are 2018's, before the 2020 crash and rebound, and most FAIR dates 2019's, whose two years ended at the 2021 high of SPY;
  the class order is again largely the calendar.
- **The RICH calls held at the multiple's highs.** The 14 RICH dates from 2019-11-15 to 2020-02-14 ($386-439, the stock's high to the end
  of 2021) all held, losing 4.7-9.4% over two years; the 43 of 2018 held on 11. With 2014-2017 (29 of 208) and 2010-2013 (0 of 25), LMT's FAIR
  and RICH calls have held on 74 of 349, the CHEAP calls on 223 of 382 (2008-2021).
- **The two largest encodings, checked against the outcome (hindsight, never a reason to change them):** of the 85 classes that FY2017 at
  GAAP would move, 38 held as built and 43 would have held as moved; of the 94 that the IS&GS history on one basis would move (toward
  CHEAP), 37 held as built and 22 would have. Every signal at BEAR moves 121 classes: 61 held as built, 78 as moved; at XBULL 41: 28 held as
  built, 2 as moved. As in 2008-2009 the BEAR signals would have helped and as in 2010-2013 they would not: one stock, opposite answers.
- **Ratio B and the gap over the floor sort mostly by year again.** Ratio B under 0.5 (43 dates, 2020-03-20 to 2021-12-31) held on all 43; Ratio
  B 1-2 (66, mostly 2019) held on 21. The floor gaps split the same way. One stock over four years mostly tests "buy lower" within a year,
  not across years (retro/README.md, "Scoring a single stock").
