# CB retrospective findings (hindsight)

**Everything below is hindsight.** It is computed from `outcome.json` (prices and dividends after each as-of date, Yahoo's CB series and
SPY), which no model reads. These are hypotheses for the live model, to be tested on other tickers and periods; none may be folded into
the CB archive or any other ticker's models (retro/README.md, "The one rule"). The point-in-time build, its decisions and its judgement
calls are in retro/README.md, "CB"; they were committed and fire-walled before any outcome was computed.

The series is ACE Limited (NYSE: ACE), the company behind today's CB, on 314 weekly dates: 105 from 2008-01-04 to 2009-12-31 (the table
below) and 209 from 2010-01-08 to 2013-12-31 (their own section, scored after their build was committed, pushed and fire-walled). The
call check is the tool's: CHEAP should clear the 15%/yr hurdle or beat SPY over two years, FAIR should land within ±15pp of SPY, RICH should miss the
hurdle and lag SPY. Judge the series by the return to the average price of months 12-24 and treat the call check as a rough tick
(retro/README.md, "Scoring a single stock").

| | dates | 2-yr total return | vs SPY (mean / median) | to the m12-24 average | call check |
|---|---|---|---|---|---|
| 2008, all | 53 | +4.2% | +2.7 / +4.8pp | -7.3% | 43 of 53 |
| 2008, CHEAP | 47 | +6.5% | +3.0 / +5.1pp | -5.6% | 37 of 47 |
| 2008, FAIR | 6 | -13.4% | +0.8 / +1.1pp | -21.1% | 6 of 6 |
| 2009, all | 52 | +46.5% | +5.6 / +7.0pp | +30.4% | 2 of 52 |
| 2009, CHEAP (January) | 4 | +35.9% | -20.2 / -18.4pp | +17.6% | 2 of 4 |
| 2009, RICH (from the Q4 2008 print) | 48 | +47.4% | +7.8 / +7.1pp | +31.4% | 0 of 48 |
| all | 105 | +25.2% | +4.2 / +5.8pp | +11.4% | 45 of 105 |

## 2008 (53 dates)

- **CHEAP or FAIR on every date, and the stock roughly kept pace with SPY.** Over two years ACE returned +4.2% on average against a falling
  market (+2.7pp over SPY, +4.8pp at the median); over three years +12.8pp. Every 2008 date landed in the BASE scenario. The call check
  hits 43 of 53: the six FAIR dates all land within ±15pp, and 37 of the 47 CHEAP dates beat SPY or clear the hurdle.
- **Buying lower did not help inside the year.** The dates to mid-September (37, at 6.3-8.3x FY2007E $7.325 and then FY07's $7.66) beat
  SPY by +9.0pp on average over two years; the 20 dates from mid-September 2008 to January 2009, with the cheapest multiples of the series
  (5.3-8.6x, mostly 6-7x, under the EPP floor on four dates), lagged it by 13.4pp, because SPY's own rebound from its 2009 low lifted the benchmark more than ACE. The worst two-year excess
  of the series is a CHEAP date in that stretch (2009-01-16, -30.1pp). One stock over a few months mostly tests "buy lower", and here the
  benchmark's path dominates.
- **The FAIR dates were the expensive ones in absolute terms** (-13.4% over two years, -21.1% to the m12-24 average), but they kept pace with
  SPY, so the call holds; the absolute losses came from the 2008-2009 drawdown (-51.8% peak to trough from the 2008-01-04 date).

## 2009 (52 dates)

- **RICH on all 48 dates from the Q4 2008 print, and wrong on all 48.** From 2009-02-05 the model's multiple rests on FY08's GAAP $3.53,
  which carries $1,633M of pre-tax realized losses; at 9.2-15.5x that EPS the stock read RICH against a window median of 9.8-10.7x. ACE then returned
  +47.4% over two years on average (+7.8pp over SPY) and landed in the BULL scenario on every one of these dates. The low of the series,
  2009-03-06 at $32.50 (RICH, AVOID), doubled over two years (+100.5%, +1.9pp over SPY).
- **The four CHEAP dates of January 2009** (still on FY07's $7.66) returned +35.9% but lagged SPY's rebound by 20.2pp: two of four hits.
- **What the point-in-time tests already flagged.** The README's sensitivity test of the EPS basis (the company's operating figure, which
  removes realized gains and losses) moves 44 of the 48 RICH dates to CHEAP. The build chose GAAP by the existing rule (the company's figure
  removes recurring items), before any outcome; on these dates that choice is what made every 2009 call wrong.

## 2008-2009 together (105 dates)

- **The robustness block separated nothing useful.** The 95 dates whose class survives 7 or 8 of the 8 robustness variants hit 35 times;
  the 10 fragile ones (5 FAIR and 5 CHEAP, all from January to June 2008) hit all 10.
- **Legacy tiers:** BUY (41 dates) +0.5pp over SPY on average (+6.0pp median), ACCUMULATE (15) +3.0pp, WATCHLIST (1) -3.0pp, AVOID (48) +7.8pp:
  the AVOID tier, every 2009 date, beat the others.

## 2010-2013 (209 dates)

Scored on 2026-11-21, after the point-in-time build was committed and pushed (e1d3e3d) and the firewall had passed at 25 cutoffs
(e02dc5d). Every date has its 6-month, 1-, 2- and 3-year horizons; the 15%/yr hurdle is +32.2% over two years.

| | dates | 2-yr total return | vs SPY (mean / median) | to the m12-24 average | call check |
|---|---|---|---|---|---|
| 2010, all | 52 | +43.7% | +17.9 / +17.6pp | +28.8% | 40 of 52 |
| 2010, CHEAP | 30 | +46.6% | +19.5 / +20.8pp | +31.5% | 30 of 30 |
| 2010, FAIR | 18 | +37.1% | +12.5 / +14.2pp | +22.6% | 10 of 18 |
| 2010, RICH (January, on FY08's $3.53) | 4 | +51.8% | +30.3 / +32.6pp | +35.6% | 0 of 4 |
| 2011, all | 52 | +46.1% | +11.3 / +10.4pp | +26.8% | 37 of 52 |
| 2011, CHEAP | 18 | +50.2% | +12.4 / +9.4pp | +32.5% | 18 of 18 |
| 2011, FAIR | 34 | +44.0% | +10.7 / +11.2pp | +23.8% | 19 of 34 |
| 2012, all | 52 | +44.7% | -0.1 / -0.5pp | +30.5% | 4 of 52 |
| 2012, FAIR (January) | 4 | +43.5% | -1.0 / -0.7pp | +30.5% | 4 of 4 |
| 2012, RICH (from the Q4 2011 print) | 48 | +44.8% | -0.0 / -0.5pp | +30.5% | 0 of 48 |
| 2013, all | 53 | +25.3% | -4.8 / -4.3pp | +18.2% | 35 of 53 |
| 2013, FAIR | 12 | +20.0% | -3.8 / -3.8pp | +19.2% | 12 of 12 |
| 2013, RICH | 41 | +26.8% | -5.1 / -5.9pp | +17.9% | 23 of 41 |
| class CHEAP | 48 | +47.9% | +16.8 / +20.2pp | +31.9% | 48 of 48 |
| class FAIR | 68 | +37.9% | +8.0 / +8.2pp | +23.1% | 45 of 68 |
| class RICH | 93 | +37.2% | -1.0 / -1.1pp | +25.1% | 23 of 93 |
| all | 209 | +39.9% | +6.0 / +2.9pp | +26.0% | 116 of 209 |

- **The classes and the tiers ordered the relative outcomes.** Against SPY over two years: CHEAP +16.8pp, FAIR +8.0pp, RICH -1.0pp; over
  three years +21.9pp, +10.9pp and +4.5pp; over one year +7.4pp, +5.8pp and +0.5pp. The legacy tiers fall in order too: BUY (19 dates)
  +24.1pp, ACCUMULATE (56) +12.0pp, WATCHLIST (41) +5.4pp, AVOID (93) -1.0pp, unlike 2008-2009, when the AVOID tier beat the others. Every
  CHEAP date (48 of 48) beat SPY.
- **In absolute terms everything rose,** so the call check fails most RICH dates: the RICH dates returned +37.2% over two years and cleared
  the hurdle on 62 of 93. ACE's two-year return is positive on every date (+10.5% to +64.3%, under +20% only on 15 dates of the second
  half of 2013); its largest drawdown within two years averages -13%.
- **2010-2011: CHEAP and FAIR on the anchors FY09's $7.55 and FY10's $9.11 (6.4-8.2x),** and the stock beat SPY by +17.3pp (dates on
  FY09) and +9.5pp (on FY10) on average; the 25 CHEAP dates of February to July 2010, under or near the EPP floor, beat it by +21.5pp. The
  FAIR misses (8 of 18 in 2010, 15 of 34 in 2011) are all dates that beat SPY by more than 15 points (+15.3 to +24.2pp).
- **2012: RICH on all 48 dates from the Q4 2011 print, on FY11's $4.65 (15-18x).** ACE then returned +44.8% over two years, exactly SPY's
  +44.8%: in relative terms the call was neither right nor wrong, but the stock cleared the hurdle on every date, so the check scores 0 of
  48. FY2011's GAAP EPS carries $791M of realized losses after tax and the year's $859M of pre-tax catastrophe losses; the multiple on it
  was a trough multiple, as in 2009.
- **2013: RICH on 41 dates and FAIR on 12, on FY12's $7.89 (10.8-13.1x),** the 63rd-73rd percentile. The RICH dates of January to July
  lagged SPY by 8.3pp (19 of 25 hits); those of October to December kept pace (+0.5pp, 4 of 12). The 12 FAIR dates from the Q2 2013 print
  landed within 9 points of SPY (-8.6 to +0.7pp).
- **The trough-anchored RICH call was again the biggest miss:** the lowest price of the batch, 2010-01-08 at $47.50 (RICH, AVOID, on
  FY08's $3.53), is its best two-year excess (+36.6pp, +52.3%), as 2009-03-06 was in the first batch.
- **Robustness again separated nothing.** The 159 dates whose class survives 7 or 8 of the 8 robustness variants hit 77 times (48%); the
  50 fragile ones (45 of them FAIR) hit 39 (78%).
- **Scenario landing:** RICH dates landed in BULL on 92 of 93; CHEAP dates in BASE on all 48; FAIR in BASE on 53 and BULL on 15. Never near
  BEAR ($4.95-11.14) or XBULL.

## 2008-2013: the EPS basis, tested on later dates

The 2008-2009 findings proposed that the company's operating EPS (which removes realized gains and losses) would have served an insurer
better than GAAP. The 2010-2013 dates were not scored when that was written, so they test it. Each of the 314 dates was rebuilt on the
operating basis (every year at the company's figure, every operating range as the guide: the README's sensitivity variant) and scored
by the same call check against the same outcomes (hindsight, this file only):

| | dates | GAAP hits | operating hits | classes moved | mean 2-yr excess of the moved dates |
|---|---|---|---|---|---|
| 2008 | 53 | 43 | 42 | 5 | +1.6pp |
| 2009 | 52 | 2 | 49 | 47 | +7.9pp |
| 2010 | 52 | 40 | 38 | 15 | +14.3pp |
| 2011 | 52 | 37 | 0 | 48 | +10.4pp |
| 2012 | 52 | 4 | 0 | 4 | -1.0pp |
| 2013 | 53 | 35 | 34 | 12 | -3.8pp |
| all | 314 | 161 | 163 | 131 | |

- **The operating basis wins 2009 by 47 calls and loses 2011 by 37: over six years the two tie (161 against 163).** In 2011 the operating
  guides ($5.40-6.75) sat well under GAAP FY10's $9.11 (a year with $451M of realized gains), so the operating basis read RICH on 48
  dates that then beat SPY by 10.4pp. In 2012, the year after the catastrophe year, both bases read RICH.
- **Both bases order the relative returns in 2010-2013** (GAAP: CHEAP +16.8pp, FAIR +8.0pp, RICH -1.0pp; operating: CHEAP +22.7pp on 29
  dates, FAIR +15.0pp on 21, RICH +1.8pp on 159). Over 2008-2013 GAAP gives +8.8, +7.4 and +2.0pp, operating +8.3, +13.3 and +1.8pp.

## Hypotheses (for other tickers and periods, never for this archive)

1. **A GAAP trough year built on realized investment losses makes an insurer look expensive exactly when it is cheap.** The rule that
   rejects the company's operating figure (it removes recurring items) is sound for recurring amortization, but for an insurer in a market
   crash the realized losses are recurring in kind yet reversing in fact: 2009's RICH calls on GAAP were wrong 48 times in 48. JPM's 2009
   (GAAP FY08 after the markdowns) is the same pattern on a bank; a test across financials, on dates not yet scored, would say whether this
   is a rule worth a new method version (it would need one, and a full re-run, with the reason recorded).
   **2010-2013 weakens it** (above): the operating basis would have fixed 2009 and broken 2011, and the two tie over 314 dates. What
   the misses share is narrower: the multiple is set on the single year after a trough (FY08 in 2009 and January 2010, FY11 in 2012),
   whichever basis is used. A hypothesis to test elsewhere: an insurer's anchor needs more than one year (an average of several years'
   EPS, or book value) rather than a different one-year figure.
2. **On a financial, book value may be the better anchor in a crisis.** ACE's book value per share fell 11.4% in 2008 while its GAAP EPS fell 54%; a
   price-to-book cross-check was not part of method r2 and was not computed here.
3. **A rebounding benchmark punishes the cheapest dates.** The late-2008 CHEAP dates lagged SPY by 13pp despite a positive absolute return;
   the relative call check penalises defensive names bought at the market's trough.
4. **In a rising market the RICH call check is unwinnable.** 2012's 48 RICH dates matched SPY exactly (+44.8%) and still scored 0 of 48,
   because the stock cleared the 15%/yr hurdle. The relative ordering (CHEAP > FAIR > RICH against SPY, and BUY > ACCUMULATE >
   WATCHLIST > AVOID in 2010-2013) is the better test of the classes than the hit count.
5. **Robustness agreement did not predict hits in either batch** (2008-2009: 35 of 95 robust, 10 of 10 fragile; 2010-2013: 77 of 159
   robust, 39 of 50 fragile). On this series the fragile dates are mostly FAIR, and FAIR's ±15pp band is the easiest to hit.
