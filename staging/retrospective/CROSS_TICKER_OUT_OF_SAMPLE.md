# Cross-ticker patterns, out of sample (hindsight): the ACN/UNP/LOW zones tested on eight newer tickers

`CROSS_TICKER_FINDINGS.md` found its patterns on ACN, UNP and LOW and asked for them to be tested on other tickers.
Eight have been built since, under the same method (r2) and over the same years (AVGO from its 2009 listing):
**AAPL, AVGO, MSFT, NKE, PEP, SHW, WMT and XOM**. None of their FINDINGS files tested the zones. This file is that test.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule"). Nothing from one ticker's outcomes enters another ticker's models.

Every count and return below is printed by `python3 staging/retrospective/cross_ticker_oos.py` (one section:
`... cross_ticker_oos.py zones`). The script reads the repo and writes nothing. Medians of an even count take the upper
middle value (`statistics.median_high`).

**What was frozen and what was not.** The three zones are copied unchanged from `cross_ticker.py`. They were fixed on
ACN, UNP and LOW before any of the eight existed, so for them the eight are a true out-of-sample test. They are:
- **cheap & falling:** own 10-year P/E percentile under 40 and a 12-month price change of -10% or worse;
- **expensive & running:** own P/E percentile 80 or above and a 12-month change above +25%;
- **crash:** 40% or more below the 52-week high, or a 12-month change of -25% or worse.

The script reproduces the discovery-set figures exactly (cheap & falling 157 dates, +74%, none lost money). Every other
cut here was chosen while looking at all eleven: the 52-week buckets, the market-wide split and the same-week ranks.
Those are in-sample.

**Sample.** 10,728 weekly dates, 9,578 with a two-year outcome (2008-01-04 to 2024-11-01); 6,946 of them in the eight
test tickers. A ticker's **base** is the median two-year total return over all its scored dates. SPY's median over the
same dates is +29%.

| Ticker | Base 2y | Beat SPY (2y) | Lost money (2y) |
|---|---|---|---|
| ACN / UNP / LOW (discovery) | +38% / +33% / +33% | 68% / 56% / 62% | 12% / 13% / 7% |
| AAPL | +51% | 76% | 2% |
| AVGO | +85% | 91% | 1% |
| MSFT | +46% | 73% | 6% |
| NKE | +39% | 61% | 27% |
| PEP | +21% | 32% | 14% |
| SHW | +47% | 74% | 9% |
| WMT | +27% | 51% | 14% |
| XOM | +8% | 23% | 34% |

**Two yardsticks, kept apart.** "vs own base" asks whether a signal picked a better entry date into *the same stock*
than an average date. "vs SPY" asks whether it beat the market. The eleven were chosen in 2026, and most of them beat
SPY on most dates whatever the signal said. So "vs own base" is the honest test of a timing signal, and "vs SPY" mostly
measures which stocks were picked.

## 1. Scorecard: what replicated

| Hypothesis from ACN/UNP/LOW | Discovery | Out of sample (8 tickers) | Verdict |
|---|---|---|---|
| **Crash entries pay** | +52pp vs own base, 89% beat it, 0% lost money, +42pp vs SPY | **+38pp, 76% beat it, 16% lost, +27pp vs SPY** (62% beat SPY); without NKE +46pp, 90%, 0% lost, +43pp vs SPY | **Holds**, except NKE |
| **Cheap & falling is the best zone** | +39pp vs own base, 77%, 0% lost, +33pp vs SPY | **+16pp, 71%, 10% lost, -2pp vs SPY** (48% beat SPY); without NKE +19pp, 76%, 2% lost | **Weaker**: a better entry into the same stock, not a market-beater. "Never lost money" fails |
| **Expensive & running is a worse entry** | -12pp vs own base, 37% beat it | **-6pp, 43% beat it** (still +17pp vs SPY) | **Holds weakly**: negative in AAPL, AVGO, NKE and SHW, positive in MSFT and WMT |
| **Expensive & running carries the loss risk** | 25% lost money, against 6% elsewhere; drawdown -33% | **11% lost, against 13% elsewhere**; drawdown -28% against -22% | **Fails** for losses; the drawdown is still deeper |
| **The house class / BASE price is a loss filter** | below BASE 3% lost, above 20% | **below BASE 16% lost, above 11%** | **Fails**; holds only in SHW and XOM |
| **The own P/E percentile is a slow signal** | under 40th pctl about 7 points a year better | **0-19th pctl: -0pp vs own base, 50% beat it**; under 40 placed below the middle stock in the same week | **Fails** as a stand-alone signal |

Per ticker, out of sample: the two-year median minus the ticker's base (dates; share that lost money over two years).

| Ticker | Cheap & falling | Crash | Expensive & running | Price below BASE | Price at or above BASE |
|---|---|---|---|---|---|
| AAPL | +55pp (95, 0%) | +122pp (60, 0%) | -9pp (225, 2%) | +2pp (430, 3%) | -2pp (448, 1%) |
| AVGO | +243pp (8, 0%) | +145pp (1, 0%) | -15pp (352, 1%) | +19pp (283, 0%) | -6pp (512, 1%) |
| MSFT | -13pp (51, 0%) | +2pp (41, 0%) | +10pp (315, 5%) | -10pp (407, 8%) | +20pp (472, 4%) |
| NKE | **-43pp (65, 52%)** | **-64pp (49, 80%)** | -16pp (267, 29%) | -19pp (326, 40%) | +4pp (552, 19%) |
| PEP | +10pp (46, 11%) | +15pp (19, 0%) | -15pp (9, 0%) | -2pp (502, 23%) | +1pp (377, 3%) |
| SHW | +44pp (4, 0%) | +19pp (14, 0%) | -5pp (309, 23%) | +4pp (373, 3%) | -6pp (506, 13%) |
| WMT | -8pp (47, 0%) | +41pp (12, 0%) | +8pp (82, 2%) | -11pp (446, 20%) | +10pp (433, 7%) |
| XOM | +20pp (86, 1%) | +133pp (55, 0%) | +38pp (3, 0%) | +8pp (451, 29%) | -4pp (428, 39%) |

- **Crash entries beat the ticker's base in seven of eight**: MSFT barely (+2pp), AVGO on a single date, and NKE is
  the exception.
- **Cheap & falling beat the base in five of eight**, two of them on few dates (AVGO 8, SHW 4). MSFT (2009-2011)
  and WMT (2009) are dead-money cases: no losses, but a slower path than an average date. NKE is the loss case.
- **One date per quarter** (thins the overlap): crash entries 23 dates, +14pp vs own base, 74% beat it, 17% lost money.
  Cheap & falling 44 dates, +12pp, 68%, 14% lost. Expensive & running 127 dates, -8pp, 39%, 13% lost. Every other date
  342 dates, +2pp, 52%, 13% lost.

## 2. The pattern that generalises: buy the same durable stock after a deep fall

Read on its own, the depth of the fall ranks entry dates in order, out of sample. Below, the distance under the 52-week
high on the eight test tickers. The buckets were chosen after looking; the 40% edge is the frozen crash rule.

| Distance below the 52-week high | Dates | Median 2y | 2y vs SPY | 2y vs own base | Beat own base | Lost money (2y) |
|---|---|---|---|---|---|---|
| 40% or more | 124 | +119% | +82pp | **+106pp** | 77% | 14% |
| 30-40% | 234 | +59% | +19pp | **+23pp** | 71% | 17% |
| 20-30% | 567 | +46% | +14pp | +6pp | 57% | 13% |
| 10-20% | 1,677 | +40% | +10pp | +2pp | 52% | 14% |
| 5-10% | 1,592 | +32% | +6pp | -3pp | 46% | 15% |
| within 5% | 2,752 | +33% | +9pp | -3pp | 46% | 11% |

The trailing 12-month change shows the same shape: -25% or worse returned +34pp vs own base (77% beat it), -25% to -10%
returned +8pp, and every bucket above that sat between -6pp and +4pp.

**Within each ticker's own series** the rank correlation with the forward return (+ = a lower reading did better)
is the most consistent result in the repo:

| Measure | Positive at 1y | Positive at 2y | Positive at 3y |
|---|---|---|---|
| 12-month price change (lower = better) | 9 of 11 | 10 of 11 | **11 of 11** |
| distance below the 52-week high (deeper = better) | 9 of 11 | 9 of 11 | 10 of 11 |
| own 10-year P/E percentile (lower = better) | 8 of 11 | 8 of 11 | 9 of 11 |

The own-P/E correlation runs the wrong way for MSFT (-0.40 at two years), WMT (-0.18) and NKE (-0.18). Two of these are
the re-rating case of `CROSS_TICKER_FINDINGS.md` section 2: the 10-year window held another regime. MSFT's cloud
re-rating and WMT's e-commerce re-rating made the stock look rich for years as it compounded. NKE's derating made it
look cheap as it fell. The price-change measures have no such window, which may be why they travel better.

## 3. Market-wide against stock-specific falls

"Market-wide" means at least half the tickers listed that week were down 10% or more over 12 months, a point-in-time
breadth read. Out of sample:

| Group | Dates | Episodes | Median 2y | 2y vs SPY | Beat SPY | 2y vs own base | Lost money (2y) |
|---|---|---|---|---|---|---|---|
| crash, market-wide | 107 | 13 | +52% | -8pp | 47% | +21pp | 11% |
| crash, stock-specific | 144 | 15 | +101% | **+63pp** | 73% | +57pp | 19% |
| cheap & falling, market-wide | 204 | 13 | +36% | -10pp | 33% | +13pp | 2% |
| cheap & falling, stock-specific | 198 | 22 | +63% | **+29pp** | 63% | +21pp | 18% |

- **Buying a market-wide fall** gave a better entry into the stock than an average date (+13pp to +21pp). It did
  **not** beat SPY bought on the same day (-8pp to -10pp), because the index rebounded too. That beats your own average
  entry, not the market.
- **Buying a fall specific to one durable company** is where the market-beating returns were (+29pp to +63pp vs SPY).
  It is also where the losses were: 18-19% of these dates lost money over two years, mostly NKE.
- In the discovery set both kinds paid, and neither lost money. The stock-specific risk shows up only out of sample.

## 4. Picking between stocks in the same week: cheapness lost, strength won (but read the bias)

Each week, the tickers scored that week are ranked by their two-year return (0 worst, 1 best, 0.5 the middle).
Out of sample, over 878 weeks:

| Group | Stock-weeks | Mean place | In the top half |
|---|---|---|---|
| own P/E pctl < 40 | 1,626 | **0.42** | 35% |
| own P/E pctl >= 80 | 3,527 | 0.54 | 56% |
| 12m change > +25% | 2,223 | 0.56 | 56% |
| expensive & running | 1,560 | 0.58 | 60% |
| crash entries | 251 | **0.62** | 60% |
| house class CHEAP / RICH | 2,219 / 4,064 | 0.49 / 0.51 | 44% / 52% |

The mean weekly rank correlation of the own P/E percentile with the two-year return is -0.18 (positive in only 29% of
weeks). For the 12-month change it is also -0.18 (33%): across stocks the expensive and the strong did better, the
opposite of the within-stock result.

**Do not read this as "buy expensive stocks".** The eight were chosen in 2026, after AVGO, AAPL and MSFT had already run.
Stocks that sat expensive and rising for years are in the sample *because* they kept rising. The within-stock result
(sections 1-2) does not depend on which stocks were picked; this one does. Crash entries are the one group that ranks
well on both views.

## 5. The exception: NKE, a durable label on a franchise in decline

NKE accounts for most of the out-of-sample losses in every falling zone. Its crash entries in 2022 (29 dates, median -24%
over two years) and 2024 (11 with an outcome, -40%) and its cheap & falling dates in 2024 (28 with an outcome, -48%) all
lost money. Its 2009 entries paid (+100%, +68%). The house kind read `DURABLE` throughout. Nothing in the price inputs
separates NKE 2022-2024 from AAPL 2013 or 2016, which paid +101% to +113%. Like ACN's GenAI dates
(`CROSS_TICKER_FINDINGS.md` section 3), it is a judgement about the business, not a price signal: whether the fall is the
market marking down a franchise that is still intact or one that is impaired.

## 6. Where the newest dates sit

These zones are hindsight hypotheses applied to point-in-time values, not a model output (`cross_ticker_oos.py latest`).

| Ticker | As of | Own P/E pctl | 12m change | Below 52w high | Zone | House class / tier |
|---|---|---|---|---|---|---|
| NKE | 2026-10-30 | 37 | -40% | -44% | cheap & falling, crash | RICH / AVOID |
| LOW | 2026-10-23 | 25 | -18% | -32% | cheap & falling | CHEAP / BUY |
| AVGO | 2026-10-30 | 87 | -12% | -34% | none (30-40% below its high) | FAIR / BUY |
| PEP | 2026-10-30 | 17 | -6% | -20% | none | RICH / AVOID |
| ACN | 2026-10-22 | 9 | +4% | -11% | none | CHEAP / BUY (`DISRUPTION_EXPOSED`) |
| MSFT | 2026-10-30 | 65 | +1% | -5% | none | CHEAP / BUY |
| SHW | 2026-11-06 | 66 | +1% | -9% | none | RICH / ACCUMULATE |
| WMT | 2026-11-06 | 97 | +22% | -7% | none | RICH / AVOID |
| UNP | 2026-10-23 | 98 | +35% | -7% | expensive & running | FAIR / WATCHLIST |
| AAPL | 2026-10-23 | 100 | +32% | -1% | expensive & running | RICH / AVOID |
| XOM | 2026-10-30 | 87 | +64% | -1% | expensive & running | RICH / AVOID (`DISRUPTION_EXPOSED`) |

- **NKE** is in the strongest zone again, on the one ticker where that zone failed out of sample. It is the live test of
  section 5.
- **LOW** is in cheap & falling, as `CROSS_TICKER_FINDINGS.md` already noted. LOW was the weakest discovery ticker in
  that zone (+8pp vs its base).

## Hypotheses for a new method version

Test each on tickers not yet built; never fit one to these eleven.
1. **Report the depth of the fall (52-week distance, 12-month change) beside the class.** It is the one input that
   ranked entry dates the same way in all eleven series at three years. Treat it as timing within a business already
   judged durable, never as a way to choose the business.
2. **Separate market-wide from stock-specific falls.** The first improved the entry but not the result against SPY. The
   second beat SPY and carried the losses.
3. **Drop "price below BASE = protected" as a loss filter.** It did not replicate.
4. **Do not use the own-history P/E percentile alone.** Out of sample it was flat against the stock's own base and
   negative across stocks. It inverts when the 10-year window holds a different regime (MSFT, WMT, NKE).
5. **Before reading a stock-specific fall as an entry, ask whether the franchise is impaired** (NKE 2022-2024, ACN
   2025-2026). No price rule tried here separates the cases.
6. **Test on companies that did not survive or did not stay durable.** All eleven were chosen in 2026. A buy-the-fall
   rule on a failing company (the case NKE only hints at) is untested here.

## What these 9,578 dates can and cannot show

- **Survivorship.** All eleven are large companies picked in 2026, most of them winners. "Buy the fall" looks safer
  here than it would on a sample that includes companies which kept falling.
- **Overlap.** Weekly dates with two-year windows overlap heavily. Out of sample, crash entries rest on 23 episodes and
  cheap & falling on 30, many of them shared market events (2008-2009, 2020, 2022). The one-per-quarter table thins this.
- **Endpoints.** Two-year point returns depend on where the endpoint falls; each FINDINGS file gives the m12-24 averages.

Judgement calls that could carry hindsight, all made after the outcomes were visible:
- the 52-week drawdown buckets other than the frozen 40% edge, and the -25%/-10% 12-month buckets;
- the market-wide breadth definition (half the listed tickers down 10% or more over 12 months);
- the same-week ranking and its six-ticker minimum;
- reading NKE as "franchise impairment", an explanation chosen after its 2024 outcomes.
