# AAPL retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 53 weekly dates from 2008-01-04 to 2008-12-31. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time build was committed
and pushed (e0b1ff4). Prices run to 2026-10-29; every horizon used here ends by 2010-12-30. Medians of an even count take the
upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 33 | +79% | +28% to +279% | 32 | 33 | +51% | 33 |
| class FAIR | 20 | +44% | +19% to +60% | 17 | 20 | +16% | 0 |
| legacy tier BUY (all dates) | 53 | +61% | +19% to +279% | 49 | 53 | +28% | 33 |
| January-September | 39 | +54% | +19% to +128% | 35 | 39 | +22% | 19 |
| October-December | 14 | +238% | +180% to +279% | 14 | 14 | +167% | 14 |
| CHEAP, January-September | 19 | +64% | +28% to +128% | 18 | 19 | +29% | 19 |
| CHEAP, October-December | 14 | +238% | +180% to +279% | 14 | 14 | +167% | 14 |

- **In absolute terms the year paid, whatever the class.** Every date beat SPY over two years, by 35pp to 235pp, and 49 of 53
  cleared the hurdle. The four that missed are the three January dates at $161-180 and 2008-05-09 ($183). But every date lived
  through the 2009-01-20 low ($78.20): drawdowns of 19-59% within two years, and a median one-year return of -18% (FAIR -20%,
  CHEAP +16%).
- **The class ranked the outcomes in order.** CHEAP did better than FAIR on the two-year return (median +79% against +44%) and on
  the m12-24 average price (+51% against +16%). There were no RICH dates.
- **The FAIR call failed by beating the benchmark.** FAIR expects a return within 15pp of SPY's. All 20 FAIR dates beat SPY by
  35-69pp, so the call held on none of them, while the CHEAP call held on all 33. On this stock in this year the class worked as a
  ranking, not as a level.
- **The class was the entry price.** The adjusted gap read UNDERVALUED and the tier BUY on every date, so the only split was the
  distance above the EPP floor: FAIR above +100% (the $165-189 entries), CHEAP below. Across the 53 dates the entry price alone
  ranks the two-year returns almost perfectly (Spearman -0.91). The 14 October-December entries ($83-108) returned +180% to
  +279%; the 20 FAIR entries +19% to +60%. One stock through one crash mostly tests "buy lower". Testing selection needs many
  tickers on the same dates.
- **BULL and XBULL were never in play.** Built on FY2003's $0.08 of EPS (a year of operating losses that interest income carried
  into profit), the BULL case (+165%/yr, then +132%/yr, at the 75th-percentile P/E) priced the stock at $1,086-1,278 in two years
  and XBULL at $7,043-9,606. The two-year prices were $194-324: nearest the BASE price on all 53 dates, and at most 30% of the
  BULL price. Ratio B (0.10 or less) and the market composite (1.00-1.22, the bottom of its grid) carried no information, so the
  BUY tier was right in direction for a scenario that never came close.
  Hypothesis for the method: when the first kept year of the window has near-zero EPS, the decade CAGR and the best two-year run
  are not growth anchors, and they swamp the probability-weighted price. A later version could measure them from a normalized
  base or cap them. Test it on other tickers whose window starts in a trough before any method change; never fit it to AAPL's
  outcomes. LOW's 2008 hypothesis is the mirror image: there a growth decade's multiple and CAGR were stale anchors for a year
  guided at 0-3% sales growth.
- **The BASE case was too low on every date.** The two-year price was 1.01 to 2.19 times the BASE price. BASE carried one
  quarter's revenue guide, less dilution, for two years, and anchored EPS on the last full year (FY07's $3.93 until October). From
  the Q4 FY08 print BASE was -5.4%/yr on the Q1 FY09 range, and those eleven dates, priced below the BEAR case, returned +180% to
  +279%.
- **The FY2002 call, seen afterwards.** Keeping FY2002 in the history would have turned all 20 FAIR dates CHEAP (retro/README.md,
  "AAPL"). Those dates beat SPY by 35-69pp, so the CHEAP call would have held on them too. That is a fact about one stock in one
  year, not a reason to change the encoding: the call was decided before scoring and stays, and changing a rule means a new
  method version tested elsewhere.
