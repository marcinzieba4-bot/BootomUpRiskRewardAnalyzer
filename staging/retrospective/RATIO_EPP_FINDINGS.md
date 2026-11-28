# Ratio B and the EPP cushion against the 2-4 year outcome (hindsight): eleven retrospective series

Do the engine's two risk readings, **Ratio B** and the **EPP gap** (the price's distance above the EPP floor), point to
better entries over two to four years? Pooled over all eleven series (ACN, UNP, LOW, AAPL, AVGO, MSFT, NKE, PEP, SHW, WMT,
XOM), and split into the discovery set (ACN, UNP, LOW) and the eight newer tickers.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/ratio_epp.py` (one section: `... ratio_epp.py cushion`).
Outcomes use retro_tool's `total_return` on its Yahoo source, the outcome.json convention (cash dividends, not
reinvested). The script recomputes all 18,583 stored 2y and 3y outcomes with no difference above 0.15pp and adds 4y.
Sample: 9,586 dates with a 2y outcome, 9,014 with 3y, 8,442 with 4y (start dates 2008-01 to 2022-11).

**The readings and their cuts are the engine's own,** identical in all eleven templates:
- **Ratio B** = downside to BEAR / upside to BULL. It is negative when the price is below the BEAR price and `inf` at or
  above BULL. Tier cuts: BUY < 0.75, ACCUMULATE < 1.10, WATCHLIST < 1.75, else AVOID.
- **EPP gap** = price / (EPS x the median yearly-minimum P/E) - 1. Bands: at or below the floor, 0-40%, 40-100%,
  100-200%, above 200%.

No cut was chosen here, so the grid itself carries no hindsight; reading a pattern out of it does. "vs own base" is a
date's return minus the median return of all that ticker's dates at the same horizon: did the reading pick a better entry
into *the same stock*? "Beat SPY" mostly measures which stocks are in the sample (all chosen in 2026).

## 1. The grid: 2-year return minus the stock's own base (dates)

| Ratio B \ EPP gap | below floor (<= 0%) | 0-40% | 40-100% | 100-200% | > 200% |
|---|---|---|---|---|---|
| below BEAR (< 0) | **+17pp (304)** | -5pp (38) | | | |
| BUY (< 0.75) | -6pp (861) | **+6pp (1,511)** | +3pp (488) | -38pp (147) | |
| ACCUMULATE (< 1.10) | +38pp (23) | +9pp (495) | -8pp (265) | +44pp (22) | +9pp (22) |
| WATCHLIST (< 1.75) | | +6pp (311) | +2pp (527) | +8pp (29) | -11pp (21) |
| AVOID (>= 1.75) | | -1pp (536) | +1pp (1,874) | -3pp (247) | -44pp (68) |
| above BULL (inf) | | +19pp (36) | +5pp (726) | **-10pp (677)** | **-15pp (352)** |

The script prints the same grid at 3y and 4y, and for the loss rate and beating SPY. Three cells hold their sign at every
horizon and in both ticker sets: the two **bold** corners and the 0-40% BUY cell.

## 2. The three patterns

| Cell | Horizon | Dates | Episodes | Tickers | vs own base | Beat own base | Beat SPY | Lost money |
|---|---|---|---|---|---|---|---|---|
| **Cushion: price below the BEAR price** (Ratio B < 0) | 2y | 342 | 32 | 7 | **+16pp** | 64% | 61% | **1%** (4 dates) |
| | 3y | 342 | 32 | 7 | +5pp | 58% | 59% | **0%** |
| | 4y | 334 | 29 | 7 | +5pp | 59% | 50% | **0%** |
| **Sweet spot: Ratio B 0-0.75, EPP gap 0-40%** | 2y | 1,511 | 135 | 11 | **+6pp** | 58% | 67% | 8% |
| | 3y | 1,460 | 127 | 11 | +6pp | 56% | 73% | 7% |
| | 4y | 1,360 | 116 | 11 | +4pp | 54% | 76% | 1% |
| **Warning: above the BULL price, EPP gap > 100%** | 2y | 1,029 | 52 | 11 | **-12pp** | 34% | 62% | **21%** |
| | 3y | 978 | 49 | 11 | -22pp | 32% | 62% | 16% |
| | 4y | 978 | 49 | 11 | -30pp | 35% | 67% | 19% |
| every date | 2y / 3y / 4y | 9,586 / 9,014 / 8,442 | | 11 | 0 | 50% | 60% / 63% / 66% | 13% / 8% / 5% |

By ticker set (2y / 3y / 4y vs own base):
- **Cushion:** discovery -1 / -9 / -8pp, lost 3% / 0% / 0%. Out of sample +19 / +6 / +6pp, lost 0% / 0% / 0%. It held
  as protection in both sets. It added return only in the newer set.
- **Sweet spot:** discovery +3 / +10 / +17pp, out of sample +8 / +3 / -2pp. Modest, and it fades by four years in the
  newer set.
- **Warning:** discovery -37 / -42 / -62pp, out of sample -11 / -19 / -28pp. Per ticker at 2y, negative in **9 of 11**
  (ACN -40pp, NKE -45, UNP -32, WMT -26, LOW -25 on 4 dates, AAPL -16, XOM -11, AVGO -10, SHW -10). The exceptions are
  MSFT (+31pp, 322 dates in 2015-2024) and PEP (+7pp).

## 3. What the readings do not do

- **The EPP floor alone is protection, not return.** Below the floor (1,192 dates), the 2y median matched the stock's own
  base (-1pp) and beat SPY only 36% of the time (45% at 4y). Yet **only 4 of its 1,077 dates with a 4y outcome lost money**
  (135 of 1,192 at 2y). Most of those dates are MSFT 2008-2012, WMT, PEP and XOM: low multiples that stayed low. It is the value-trap
  read of `CROSS_TICKER_OUT_OF_SAMPLE.md`.
- **Do not use the EPP gap to choose between stocks.** In the same week across tickers, a *higher* EPP gap went with the
  better return. The weekly rank correlation is -0.23 at 2y and -0.31 at 4y, with lower doing better in only 20-27% of
  weeks. The compounders (AVGO, AAPL, MSFT) always sit far above their floor. Ratio B is near neutral across stocks
  (+0.03 to +0.07).
- **Within one stock, both are weaker timing signals than the price fall.** A lower reading did better in 8-9 of 11
  series for the EPP gap and 7-8 for Ratio B, against 9-10 for the distance below the 52-week high. Both run the wrong way
  for MSFT and WMT, the re-rating stocks (MSFT -0.41 to -0.56).
- **The deep-fall filter is one episode.** Among dates 30%+ below the 52-week high, Ratio B < 0.75 with EPP gap <= 40%
  lost money over two years 6% of the time, against 24% otherwise. But 33 of the 35 losing dates outside that cell are NKE
  2022, and NKE 2024 lost inside it (17 dates). Do not read it as a rule.

## 4. The cushion's evidence is old, and it is failing live

The 342 below-BEAR dates with a 2y outcome come mostly from **2008-2009** (195 of them). The rest are WMT 2010-2012, AAPL
2013 and LOW 2020-2023.

The test running now is **ACN**. It has sat below its BEAR price on 59 dates from 2025-08-01 to 2026-10-22, all filed
`DISRUPTION_EXPOSED` (GenAI). The 10 with a one-year outcome all lost money, a median -23%; the first two-year outcomes
arrive in August 2027. This is the same exception as the cheap & falling zone (`CROSS_TICKER_FINDINGS.md` section 3): the
cushion assumes the BEAR case is a floor for the business, and a live disruption theme questions exactly that.

## 5. Where the newest dates sit

Point-in-time readings; the cells are hindsight hypotheses, not a model output (`ratio_epp.py latest`).

| Ticker | As of | Ratio B | EPP gap | Cell |
|---|---|---|---|---|
| ACN | 2026-10-22 | -0.06x | -7% | cushion (below BEAR and the floor), under the live disruption theme |
| LOW | 2026-10-23 | 0.46x | +8% | sweet spot |
| MSFT | 2026-10-30 | 0.50x | +38% | sweet spot |
| AVGO | 2026-10-30 | 0.36x | +107% | BUY tier far above the floor (-38pp cell at 2y, 147 dates) |
| AAPL | 2026-10-23 | inf | +133% | warning |
| WMT | 2026-11-06 | inf | +133% | warning |
| XOM | 2026-10-30 | 5.52x | +106% | AVOID tier, 100-200% band (-3pp) |
| UNP, SHW, NKE, PEP | | 1.64x / 0.97x / 4.05x / 2.16x | +48% / +43% / +29% / +9% | none of the three |

## Hypotheses for a new method version

Test each on tickers not yet built; never fit one to these eleven.
1. **Report "above BULL with EPP gap > 100%" as a warning beside the tier.** It was the most consistent cell: below the
   stock's own base in 9 of 11 tickers and both sets, at every horizon.
2. **Read "below BEAR" as capital protection over 3-4 years, not as a return call,** and only for a business whose BEAR
   case is still a floor (ACN 2025-2026 is the open test).
3. **Read the EPP floor as a 4-year capital floor,** not as an entry. It lagged SPY on most dates.
4. **Do not rank stocks against each other by the EPP gap.** Across stocks it pointed the wrong way.

## Limits and judgement calls

- **Survivorship:** all eleven exist and were picked in 2026.
- **Overlap:** weekly dates with 2-4 year windows. The cushion rests on 32 episodes, most of them the 2008-2009 market.
- The cut points are the engine's. Choosing the three cells to report, the cushion and deep sections (added after the
  first run to split the cells that stood out), and reading ACN's case through its disruption theme were all done after
  the outcomes were visible.
