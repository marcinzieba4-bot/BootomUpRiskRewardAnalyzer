# CB retrospective findings (hindsight)

**Everything below is hindsight.** It is computed from `outcome.json` (prices and dividends after each as-of date, Yahoo's CB series and
SPY), which no model reads. These are hypotheses for the live model, to be tested on other tickers and periods; none may be folded into
the CB archive or any other ticker's models (retro/README.md, "The one rule"). The point-in-time build, its decisions and its judgement
calls are in retro/README.md, "CB"; they were committed and fire-walled before any outcome was computed.

The series is ACE Limited (NYSE: ACE), the company behind today's CB, on 105 weekly dates from 2008-01-04 to 2009-12-31. The call check
is the tool's: CHEAP should clear the 15%/yr hurdle or beat SPY over two years, FAIR should land within ±15pp of SPY, RICH should miss the
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

## Hypotheses (for other tickers and periods, never for this archive)

1. **A GAAP trough year built on realized investment losses makes an insurer look expensive exactly when it is cheap.** The rule that
   rejects the company's operating figure (it removes recurring items) is sound for recurring amortization, but for an insurer in a market
   crash the realized losses are recurring in kind yet reversing in fact: 2009's RICH calls on GAAP were wrong 48 times in 48. JPM's 2009
   (GAAP FY08 after the markdowns) is the same pattern on a bank; a test across financials, on dates not yet scored, would say whether this
   is a rule worth a new method version (it would need one, and a full re-run, with the reason recorded).
2. **On a financial, book value may be the better anchor in a crisis.** ACE's book value per share fell 11.4% in 2008 while its GAAP EPS fell 54%; a
   price-to-book cross-check was not part of method r2 and was not computed here.
3. **A rebounding benchmark punishes the cheapest dates.** The late-2008 CHEAP dates lagged SPY by 13pp despite a positive absolute return;
   the relative call check penalises defensive names bought at the market's trough.
