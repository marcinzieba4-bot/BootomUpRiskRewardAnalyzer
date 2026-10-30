# NKE retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 53 weekly dates from 2008-01-04 to 2008-12-31. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time build was committed
and pushed (70934e9). Prices run to 2026-10-30; every two-year horizon used here ends by 2010-12-30 (three-year: 2011-12-30).
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 41 | +22% | +4% to +84% | 13 | 41 | +10% | 41 |
| class FAIR | 12 | +14% | +7% to +16% | 0 | 12 | -8% | 0 |
| legacy tier BUY | 39 | +22% | +4% to +84% | 13 | 39 | +11% | 39 |
| legacy tier ACCUMULATE | 12 | +13% | +7% to +16% | 0 | 12 | -7% | 2 |
| legacy tier WATCHLIST | 2 | +16% | +8% to +16% | 0 | 2 | -7% | 0 |
| January to the Q4 FY08 print (FY07 EPS anchor) | 25 | +12% | +4% to +21% | 0 | 25 | -7% | 13 |
| from the Q4 FY08 print (FY08 EPS anchor) | 28 | +30% | +17% to +84% | 13 | 28 | +16% | 28 |
| CHEAP, January to June | 13 | +12% | +4% to +21% | 0 | 13 | -4% | 13 |
| October-December | 14 | +74% | +30% to +84% | 13 | 14 | +44% | 14 |

- **Every date beat SPY; few cleared the hurdle.** All 53 beat SPY over two years, by 15pp to 39pp, while SPY itself returned
  -19% to +57%. Only 13 cleared the hurdle: the October-December entries ($47-58) other than 2008-10-03 (+30%). Every date lived
  through the 2009-03-09 low ($38.57): drawdowns of 28-45% within two years, and a median one-year return of -12% (CHEAP -7%,
  FAIR -19%).
- **The class ranked the outcomes, through the EPS anchor.** CHEAP did better than FAIR on the two-year return (median +22%
  against +14%), on the m12-24 average price (+10% against -8%) and over three years (+54% against +22%). Most of that gap is the
  28 dates after the Q4 FY08 print, all CHEAP, when FY08's $3.74 replaced FY07's $2.93 as the anchor. On the 25 dates anchored on
  FY07 the 13 CHEAP dates (median +12%, m12-24 -4%) and the 12 FAIR dates (+14%, -8%) were close. There were no RICH dates.
- **The FAIR call failed by beating the benchmark**, as for AAPL in 2008. FAIR expects a return within 15pp of SPY's; all 12 FAIR
  dates beat SPY by 21-29pp, so the call held on none. The CHEAP call held on all 41, but 28 of them only by beating SPY (which
  returned -18% to +8% over those windows), not by clearing the hurdle.
- **The floor distance ranked the outcomes; the signal composite ranked them backwards.** Across the 53 dates the EPP gap ranks the
  two-year returns at Spearman -0.90 (-0.95 on the m12-24 average), Ratio B at -0.89, the adjusted gap at +0.82 and the entry price
  alone at -0.77. The proxy composite, built from the latest quarter's signals, ranks them at -0.65. It read 3.05 from January to
  mid-March (11 dates, median two-year return +10%), 3.00 from the Q3 FY08 print to June (14, +13%), 2.70 from the Q4 FY08 print to
  mid-December (25, +29%) and 2.00 after the Q2 FY09 print (3, +77%). The trailing signals were highest near the top of the cycle
  and lowest near its bottom.
  Hypothesis for the method: last-quarter operating signals lag the price, so as composite inputs they lean pro-cyclical. A later
  version could test them against their own trend, or give valuation more weight. Test it on other tickers and years before any
  method change; never fit it to NKE's outcomes. AAPL's 2008 batch found the entry price ranking its returns too (Spearman -0.91):
  one stock through one crash mostly tests "buy lower".
- **BASE was the nearest anchor; BULL and BEAR were not reached at two years.** The two-year price ($61-90) landed nearest the BASE
  price on 51 dates and the BEAR price on 2; it was 0.82-1.20 times BASE, 0.61-0.87 times BULL and 1.19-1.73 times BEAR. On the path
  every date saw a close ($38.57) below its BEAR price ($45-57): flat EPS at the 10th-percentile multiple was a floor for the
  two-year point, not for the drawdown.
- **The FY07 call, seen afterwards.** FY07 at the company's $3.10 instead of GAAP $2.93 would have turned 11 of the 12 FAIR dates
  CHEAP (retro/README.md, "NKE"). Those dates beat SPY by 21-29pp, so the CHEAP call would have held on them too, while their
  m12-24 average was -3% to -12%. That is a fact about one stock in one year, not a reason to change the encoding: the call was
  decided before scoring and stays, and changing a rule means a new method version tested elsewhere.
- **Revenue growth excluding currency moved nothing** (retro/README.md, "NKE"): BASE on reported growth gives the same 53 classes
  and tiers, so the choice of basis did not shape these outcomes.
