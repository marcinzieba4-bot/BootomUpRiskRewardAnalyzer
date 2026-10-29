# Cross-ticker retrospective findings (hindsight): ACN, UNP, LOW

Patterns seen when the three retrospective series are pooled. They are **labels and hypotheses**: never feed them back
into a model, a fact sheet, a builder or a method rule (retro/README.md, "The one rule"). Each ticker's own FINDINGS file
stays the record for that ticker; nothing here enters another ticker's models. The patterns were found on the same three
tickers they describe, so they are in-sample. Testing one means a fourth ticker (ideally several on the same dates),
then a new method version and a full re-run.

Every count and return below is printed by `python3 staging/retrospective/cross_ticker.py` (one section:
`... cross_ticker.py zones`). The script reads the repo and writes nothing. Medians of an even count take the upper
middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

**Sample.** 2,632 weekly dates with a two-year outcome (ACN 877, UNP 877, LOW 878; 2008-01-04 to 2024-10-25), 2,476
with three years. A ticker's **base** is the median two-year total return over all its scored dates: ACN +38%, UNP +33%,
LOW +33%. The weekly dates overlap: each stock has about eight non-overlapping two-year windows, and the three stocks
share their market episodes (2008-09, 2020, 2022). "Episodes" below count runs of consecutive weekly dates.

**Point-in-time inputs used**, all printed by each date's own model or report: the class, tier and scenario prices
(analysis.json); the stock's own 10-year P/E percentile (`PE_NOW_PCTL`: on guided current-year EPS for ACN and LOW, on
the last full year for UNP on 932 of its 982 dates and for LOW on 52); the 52-week high (report.txt); and the trailing 12-month price
change, computed from the weekly series itself (prices public by the as-of date, UNP's 2008 and 2014 splits restated).

## 1. The house calls: the same median, a different left tail

Pooled, the class and the tier barely separate the median outcome:

| Group | Dates | Median 2y | Median 3y | Cleared hurdle | Beat SPY |
|---|---|---|---|---|---|
| class CHEAP | 698 | +36% | +59% | 55% | 61% |
| class FAIR | 265 | +40% | +68% | 57% | 67% |
| class RICH | 1,669 | +35% | +60% | 54% | 62% |
| tier BUY | 831 | +37% | +66% | 57% | 60% |
| tier AVOID | 1,109 | +34% | +55% | 53% | 63% |

But they separate the **risk of losing money over two years**, the same way in all three tickers:

| Share of dates that lost money over two years | ACN | UNP | LOW |
|---|---|---|---|
| class CHEAP | 3% of 278 | 0% of 89 | 2% of 331 |
| class RICH | 18% of 560 | 16% of 692 | 12% of 417 |
| price below the BASE scenario price | 3% of 521 | 3% of 264 | 3% of 668 |
| price above the BASE scenario price | 25% of 356 | 18% of 613 | 17% of 210 |

- Below the BASE price, 3% of dates lost money in each ticker; above it, 17-25%. This is the most consistent pattern in
  the pooled data.
- The losing dates cluster after long runs: ACN 2021 and 2023-2024, UNP 2014-2015 and 2021-2022, LOW 2021 and 2024, plus
  all three in 2008 and LOW in 2009.
- So the class reads best as a downside filter, not a return ranker. Its RICH dates often compounded anyway (ACN
  2015-2020, LOW 2011-2013, UNP 2010-2012), but 259 of the 283 two-year losses in the sample started from a RICH date,
  and 236 from a price above BASE.

## 2. The stock's own multiple is a slow signal

| Own 10-yr P/E percentile | Dates | Median 1y | Median 2y | Median 3y | Lost money (2y) | ACN / UNP / LOW 2y |
|---|---|---|---|---|---|---|
| 0-19 | 333 | +18% | +39% | +77% | 4% | +57% / +103% / +28% |
| 20-39 | 247 | +23% | +46% | +83% | 4% | +53% / +44% / +36% |
| 40-59 | 276 | +17% | +41% | +75% | 4% | +41% / +39% / +40% |
| 60-79 | 539 | +17% | +39% | +61% | 9% | +30% / +54% / +44% |
| 80-89 | 334 | +15% | +30% | +53% | 14% | +27% / +29% / +38% |
| 90-100 | 903 | +14% | +31% | +51% | 17% | +37% / +22% / +23% |

- **About seven points a year, at one year and at three.** Below the 40th percentile the median compounded at
  +21.7%/yr over one year and +21.8%/yr over three; at the 80th or above, +14.3% and +14.9%. Against SPY the lead builds
  with time: the low-percentile dates led by +8pp after one year and +38pp after three, the high-percentile ones by +3pp
  and +12pp.
- **Within each ticker's series** the rank correlation of the P/E against its own median with the forward return rises
  with the horizon for ACN (+0.03 at six months, +0.34 at three years) and UNP (+0.21 to +0.47). For LOW it is near zero
  beyond six months.
- **It fails when the 10-year window holds another regime:** LOW in 2008 (a growth decade's 14-43x made 11-17x look
  cheap), LOW 2013-2014 (the crisis years made a recovery look rich), ACN 2015-2020 (a seven-year re-rating). Each
  ticker's FINDINGS records its case (LOW "The P/E window lags a regime change", ACN item 1, UNP "2010 against 2014").

## 3. The strongest pattern: the multiple read together with the last 12 months

The own-history percentile alone is a weak signal. Read beside the trailing 12-month price change it splits cleanly
(dates from 2009, when the weekly series first has a 12-month history):

| Own P/E percentile, 12-month price change | Dates | Episodes | Median 2y | Median 3y | Cleared hurdle | Lost money (2y) | Median drawdown | ACN / UNP / LOW 2y |
|---|---|---|---|---|---|---|---|---|
| **< 40, -10% or worse ("cheap & falling")** | 157 | 16 | **+74%** | **+105%** | 78% | 0% | -18% | +84% / +82% / +40% |
| < 40, -10% to +10% | 196 | 34 | +41% | +85% | 58% | 1% | -25% | +58% / +21% / +34% |
| < 40, +10% to +25% | 71 | 22 | +55% | +90% | 72% | 1% | -25% | +57% / +66% / +40% |
| < 40, above +25% | 42 | 13 | +53% | +86% | 76% | 0% | -25% | +48% / +64% / +32% |
| 40-79, -10% or worse | 99 | 14 | +33% | +22% | 51% | 6% | -27% | +33% / +39% / -2% |
| 40-79, -10% to +10% | 275 | 51 | +40% | +71% | 57% | 11% | -24% | +41% / +24% / +44% |
| 40-79, +10% to +25% | 233 | 53 | +43% | +72% | 64% | 8% | -23% | +33% / +74% / +43% |
| 40-79, above +25% | 178 | 31 | +47% | +66% | 72% | 0% | -25% | +39% / +61% / +41% |
| >= 80, -10% or worse | 2 | 2 | +16% | +11% | 0% | 0% | -16% | +16% / +16% / - |
| >= 80, -10% to +10% | 168 | 39 | +38% | +56% | 62% | 5% | -23% | +47% / +26% / +45% |
| >= 80, +10% to +25% | 445 | 66 | +36% | +56% | 57% | 7% | -23% | +40% / +23% / +37% |
| **>= 80, above +25% ("expensive & running")** | 610 | 48 | **+22%** | **+48%** | 40% | 25% | -33% | +20% / +27% / +23% |

**Cheap & falling** (own percentile under 40, the price down at least 10% over 12 months):
- 0 of 157 dates lost money over two years or three. All 13 ticker-years in the zone had a positive median, and 11
  beat their ticker's base. The two that did not are the 2022-2023 entries (LOW 2023 +28%, UNP 2023 +21%), when all
  three stocks lagged SPY (section 5).
- It rests on about six market episodes: 2008-2009 (all three), August 2010 and August-October 2011 (LOW), late
  2015 to early 2016 (UNP), March-April 2020 (LOW, UNP), and late 2022 to mid-2023 (LOW, UNP).
- Without the crash dates of section 4 it still returned +45% over two years and +77% over three, with no losses.
- **The house class read RICH on 47 of the 157 dates**: all 19 of UNP's 2015-2016 dates and parts of UNP 2009, LOW
  2009 and LOW 2011. Those 47 returned +71% over two years. Their BASE growth was a median -21%/yr: the trough quarter's
  revenue or a guided margin cut, carried for two years (the fallback and margin-step findings in each FINDINGS file).
  The legacy tier read BUY on 149 of the 157.

**Expensive & running** (own percentile 80 or above, the price up more than 25% over 12 months):
- A median +22% over two years, against +40% for every other date from 2009. A quarter of its dates (151 of 610) lost
  money over two years, against 6% elsewhere. The median drawdown inside the two years was -33%, against -25%.
- **It does not time the top.** Only 15 of its 37 ticker-years beat their ticker's base, and those 15 are re-rating
  runs: ACN 2016-2017 and 2019-2020, LOW 2012-2013 and 2017-2020, UNP 2010-2012 and 2016-2017. What it changes is the
  odds of a two-year loss and the size of the drawdown.
- **The business mostly caught up by year three:** only 9 of 584 dates lost money over three years, at a median +48%.
  For these three companies, buying in this zone cost time more often than capital.

**One date per quarter** (the first scored date of each quarter, to thin the overlap): cheap & falling 13 dates, median
+98%, none lost money; expensive & running 47 dates, +20%, 26% lost money; every other date 135, +38%, 4% lost money.

**The thresholds were chosen after looking** (40th and 80th percentiles, -10% and +25%), so the script prints a grid
of nearby cuts:
- Percentile under 30, 40 or 50 with a 12-month change at or below 0%, -10% or -20%: medians +49% to +97% over two
  years, 0-3% of dates losing money. All three tickers sit above their base in every cell, LOW by the least (+3pp to
  +26pp).
- Percentile at or above 70, 80 or 90 with a change above +15%, +25% or +35%: medians +16% to +30%, with 17-31% losing.
  ACN and LOW sit below their base in every cell; UNP is mixed (-11pp to +8pp).

**The exception in sight: a live disruption theme.** ACN reads cheap & falling on 67 dates from 2025-04-04 to
2026-10-09, and 14 of the 16 with a one-year outcome are filed `DISRUPTION_EXPOSED` (GenAI). One year on, those 16 had
lost a median 26% (-48% to -2%) and all lagged SPY (median -46pp). No cheap & falling date with an outcome carried a
live disruption theme before. ACN's FINDINGS (item 8) asks the same question. Its first two-year outcomes come in
April 2027. Until then, cheap & falling under a live disruption theme is untested.

## 4. Crash entries paid in all three

Dates at least 40% below the 52-week high, or down at least 25% over 12 months: 87 dates, 14 episodes, 12 ticker-years.
A median +85% over two years and +118% over three; 92% cleared the hurdle and none lost money over two years (one did
over three). The median drawdown after entry was -16%: most of the fall was already behind these dates.

- The best were the market-wide lows: UNP 2008-2009 (+100%, +112%), ACN April-May 2009 (+109%), LOW and UNP in March
  2020 (+263%, +129%), and UNP's 2015-2016 freight recession (+72%, +74%).
- The weakest were entries before the market bottom (LOW January-October 2008, +18%) and ACN's late-2022 low (+39% over
  two years, +7% over three, into the GenAI derating).
- On UNP's 2015-2016 dates the house class read RICH throughout.

## 5. Beating SPY was a market regime, not a stock call

| Start year | SPY 2y median | ACN beat SPY | UNP beat SPY | LOW beat SPY | All three beat | All three lag |
|---|---|---|---|---|---|---|
| 2017 | +23% | 100% | 100% | 100% | 52/52 | 0/52 |
| 2018 | +20% | 100% | 94% | 87% | 43/53 | 0/53 |
| 2021 | +3% | 27% | 19% | 71% | 0/52 | 15/52 |
| 2022 | +39% | 4% | 0% | 8% | 0/52 | 46/52 |
| 2023 | +49% | 0% | 0% | 0% | 0/52 | 52/52 |
| 2024 | +39% | 0% | 0% | 0% | 0/42 | 42/42 |

Over the 877 weeks scored for all three, the stocks' two-year excess returns over SPY are correlated at +0.44 (ACN-UNP),
+0.45 (ACN-LOW) and +0.16 (UNP-LOW). From 2022 start dates the three lagged SPY together, whatever the class said. The
CHEAP call's "beat SPY" test then passed or failed on the benchmark's path, as LOW's FINDINGS showed for 2008 and
2022-2023 and ACN's item 3 for 2022-2023. Read CHEAP as an absolute-return call.

## 6. The scenario band trailed the regime in all three

| Ticker | 2018-2020 starts: nearest BULL or XBULL | 2021-2024 starts: nearest BEAR or BASE |
|---|---|---|
| ACN | 99% (XBULL 94%) | 70% |
| UNP | 99% | 64% |
| LOW | 79% (XBULL 55%) | 100% |

The bands are built from the stock's own P/E percentiles and its decade EPS CAGR, so they lag a re-rating on the way
up and a derating on the way down. This is the same root cause as section 2, and each FINDINGS file reports it for
its own ticker.

## Tried, no consistent sign across the three

Each was read against the same valuation buckets (`cross_ticker.py tried`):
- **The business dashboard** (each ticker's thirds of its proxy composite): at a given percentile, weak and strong
  numbers ordered the outcomes differently in each ticker. Over each series it ranked contrarian for ACN and UNP and,
  up to two years, slightly the other way for LOW (`cross_ticker.py rank`).
- **The EPS cycle** (last year down / up but below the old peak / a record): the clean results rest on LOW's 2011-2014
  dates alone, the recovery after the 2009 low. A record year at the 80th percentile or above returned +36% for ACN
  against +19% for UNP and LOW.
- **The price against the scenario band:** above the BULL price returned +22% over two years, with a 21% loss rate,
  but LOW's 11 such dates returned +81%.

## Hypotheses for a new method version

Test each on other tickers first; never fit one to these three.
1. **Read the own-history multiple with the trailing 12-month price change**, not with the business dashboard. Report
   the two zones beside the class.
2. **Use the class as a loss filter as well as a call:** in all three tickers, dates above the BASE price lost money
   over two years 17-25% of the time, against 3% below it.
3. **At a trough, do not let one quarter set two years of BASE growth.** Each FINDINGS file proposes its own variant.
   The 47 RICH reads inside cheap & falling are what it cost.
4. **Before reading cheap & falling as an entry, check for a live disruption theme** (ACN 2025-2026). Untested until
   2027.
5. **Score the class on absolute return, and against an equal-weight or sector benchmark as well as SPY.** The three
   lagged a cap-weighted SPY together from 2022.
6. **Value against the market's multiple as well as the stock's own** (ACN item 1). Untested: no market multiple is in
   the repo.

## Where the newest dates sit

These zones are hindsight hypotheses applied to point-in-time values, not a model output (`cross_ticker.py latest`).

- **LOW: cheap & falling** on all 9 dates from 2026-08-28 to 2026-10-23 (12th-33rd percentile, down 18-28% over 12
  months), DURABLE, BUY on all nine and CHEAP on eight.
  - The zone has the cleanest record of any pattern here, but LOW was its weakest ticker (+40%). LOW's 2022-2023 entries
    returned +28% to +36% while lagging SPY.
  - The house CHEAP reads lean on BASE growth that includes the FBM acquisition and the decade buyback rate (LOW
    FINDINGS, hypothesis 9).
- **UNP: expensive & running** on 13 dates between 2026-04-24 and 2026-10-23, the last two among them (93rd-100th
  percentile, up 26-38% over 12 months).
  - By history: a median +22% over two years, a one-in-four chance of a two-year loss and a -33% median drawdown.
    In 15 of 37 such ticker-years, though, the run kept going.
  - UNP's FINDINGS flags the same dates' BASE growth from fuel-inflated freight revenue. The Norfolk Southern merger
    is outside anything this sample tested.
- **ACN: the open exception.** Cheap & falling through 2026-10-09 under `DISRUPTION_EXPOSED`. After a 30% rise in
  October the last two dates fall out of the zone (12-month change -4%, then +4%), still CHEAP and BUY at the 7th-9th
  percentile.

## What 2,632 dates can and cannot show

- **Independent evidence is thin.** About eight two-year windows per stock, shared across the three. Cheap & falling
  rests on about six market episodes and crash entries on about four. Expensive & running covers more ground (37
  ticker-years), but its losses cluster in three periods (UNP 2013-2015, all three in 2021-2022, ACN and LOW in
  2023-2024).
- **The tickers survived.** All three are large, durable companies chosen in 2026, and "none lost money" would not
  survive a company that failed. The zones are a timing read on a business already judged durable, not a way to choose
  businesses.
- **Endpoints matter.** A two-year point return depends on where the endpoint falls (the March 2020 crash, the February
  2025 peak). Each FINDINGS file gives the m12-24 average price beside it.

Judgement calls that could carry hindsight, all made after the outcomes were visible:
- the zone thresholds, with the grid shown for that reason;
- the crash definition (40% below the 52-week high or down 25% over 12 months);
- pairing valuation with the 12-month price change rather than with the dashboard or the EPS cycle, which were tried
  and are shown above;
- treating `DISRUPTION_EXPOSED` as the exception's marker, an explanation chosen after ACN's 2025 one-year outcomes.
