# LMT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the LMT weekly dates: 314 from 2008-01-04 to 2013-12-31 (105 to 2009-12-31, 209 from 2010-01-08), all
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
