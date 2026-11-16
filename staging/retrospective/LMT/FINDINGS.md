# LMT retrospective findings (hindsight)

Patterns seen in `outcome.json` for the LMT weekly dates: 105 from 2008-01-04 to 2009-12-31, all Lockheed Martin Corporation (NYSE: LMT).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its
point-in-time build was committed (ed562557a) and its decisions, controls, leak scan, sensitivities and firewall result were written to the
README and committed (659b33a07); the outcomes were computed on 2026-11-16. Every date has its 6-month, 1-, 2- and 3-year horizons (the last
ends 2012-12-28). Total returns include the quarterly dividends ($0.42 from the ex-date of 2007-11-29, $0.57 from 2008-11-26, $0.63 from
2009-11-27, $0.75 from 2010-11-29, $1.00 from 2011-11-29): $4.17-5.89 a share over two years, 3.6-8.8% of the entry price. No split falls
in any horizon, so every price is as traded. Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr
hurdle is +32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should clear the hurdle or beat the benchmark
(SPY). The 2008 table runs to 2008-12-26; 2009-01-02 closes the ISO week of 2008-12-29 and sits in the 2009 table.

Every date is CHEAP with tier BUY and all eight robustness variants agreeing, so the tables split the dates by latest print and by where
the price stood against the EPP floor, not by class.

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
