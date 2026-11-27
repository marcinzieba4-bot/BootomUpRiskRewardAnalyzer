# NEM retrospective findings (hindsight)

Patterns seen in `outcome.json` for the NEM weekly dates: 105 from 2008-01-04 to 2009-12-31, all Newmont Mining Corporation (NYSE: NEM).
They are **labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time
build, validation outputs, README section and firewall result were committed and pushed (24fcadece, 1e9dff356, c4a387d70), on 2026-11-27.
The one-line 2026 profile that `retro_tool outcome` copies into each `outcome.json` (`profile_drift`: today CYCLICAL, "gold miner; gold
price, rising AISC") was first seen there, after every model had been built, validated and committed. Every date has its 6-month, 1-, 2- and
3-year horizons. Total returns include the $0.10 quarterly dividends. The 15%/yr hurdle is +32.2% over two years. "Call held" is
`call_check_2y`: CHEAP should clear the hurdle or beat the benchmark (SPY).

## 2008 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2008-01-04 to 2008-12-26) | 52 | +21.6% | -15.6% to +157.5% | 21 | 51 | +2.1% | 51 |
| FY07E $1.18 (FY06's) (2008-01-04 to 2008-02-15) | 7 | -8.5% | -15.6% to -1.2% | 0 | 6 | -17.0% | 6 |
| FY08E $1.25 (FY06's) (2008-02-22 to 2008-12-26) | 45 | +26.8% | -5.2% to +157.5% | 21 | 45 | +4.4% | 45 |
| latest print Q3 2007 (2008-01-04 to 2008-02-15) | 7 | -8.5% | -15.6% to -1.2% | 0 | 6 | -17.0% | 6 |
| latest print Q4 2007 (2008-02-22 to 2008-04-18) | 9 | +7.8% | -5.2% to +19.7% | 0 | 9 | -2.9% | 9 |
| latest print Q1 2008 (2008-04-25 to 2008-07-18) | 13 | +19.6% | +9.0% to +27.8% | 0 | 13 | -1.9% | 13 |
| latest print Q2 2008 (2008-07-25 to 2008-10-24) | 14 | +53.4% | +19.9% to +152.8% | 12 | 14 | +28.7% | 14 |
| latest print Q3 2008 (2008-10-30 to 2008-12-26) | 9 | +112.5% | +57.0% to +157.5% | 9 | 9 | +87.1% | 9 |
3y (52 dates with one): 17 of 52 cleared, 48 beat SPY; range +0.1% to +193.6%

## 2009 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY (2009-01-02 to 2009-12-31) | 53 | +39.0% | +17.0% to +60.5% | 35 | 26 | +36.3% | 41 |
| FY08E $1.25 (FY06's) (2009-01-02 to 2009-02-13) | 7 | +40.5% | +27.7% to +56.0% | 6 | 2 | +39.3% | 6 |
| FY09E $1.82 (FY08's) (2009-02-20 to 2009-09-11) | 30 | +37.0% | +17.0% to +53.9% | 19 | 8 | +38.7% | 19 |
| FY09E $1.80 (FY08's) (2009-09-18 to 2009-12-31) | 16 | +40.7% | +21.9% to +60.5% | 10 | 16 | +24.2% | 16 |
| latest print Q3 2008 (2009-01-02 to 2009-02-13) | 7 | +40.5% | +27.7% to +56.0% | 6 | 2 | +39.3% | 6 |
| latest print Q4 2008 (2009-02-20 to 2009-04-24) | 10 | +37.7% | +17.3% to +53.9% | 7 | 0 | +38.8% | 7 |
| latest print Q1 2009 (2009-05-01 to 2009-07-17) | 12 | +25.7% | +17.0% to +53.8% | 4 | 0 | +36.6% | 4 |
| latest print Q2 2009 (2009-07-24 to 2009-10-23) | 14 | +44.0% | +33.5% to +52.6% | 14 | 14 | +37.4% | 14 |
| latest print Q3 2009 (2009-10-30 to 2009-12-31) | 10 | +32.1% | +21.9% to +60.5% | 4 | 10 | +18.8% | 10 |
3y (53 dates with one): 5 of 53 cleared, 3 beat SPY; range -7.8% to +72.6%

## What the labels suggest (hypotheses only)

- **Every date was CHEAP and BUY, and the call held on 92 of 105** (51 of 52 in 2008, 41 of 53 in 2009). The 2-year median was +21.6% for
  the 2008 entries and +39.0% for 2009's; 56 of 105 cleared the 15%/yr hurdle.
- **The 2008 calls held mostly by beating a falling market** (51 of 52 beat SPY, 21 cleared the hurdle): the January-February 2008
  entries on FY06's $1.18 lost 1-16% over two years, and only the entries from the Q2 2008 print on (late July to December 2008, the price
  mostly under the EPP floor) cleared the hurdle: 21 of those 23 dates, medians +53.4% and +112.5%. The m12-24 average price was +2.1% (median) for 2008 entries: a stock that went nowhere for a
  year and a half after entry, then rose.
- **The 2009 calls cleared the hurdle more often (35 of 53) but lagged a rebounding market** (26 of 53 beat SPY; none of the 22 dates from
  the Q4 2008 print to mid-July 2009 did). 11 of the 12 misses are there.
- **The class did not discriminate:** with one class on every date, the series tests only "buy Newmont on its own 2002-2009 multiple".
  The window's median (42-47x on the low 2002-2006 earnings) made every anchor read cheap; whether that is information or an artefact of a
  loss-heavy decade cannot be told from one stock. Worth testing on other miners and other loss-heavy windows before any rule changes.
- **The kind drifted:** DURABLE then (no 10-K said "cyclical"), CYCLICAL in today's profile. Label only; it changes no price state.
- The worst within-2-year drawdowns (-62% from the January 2008 entries) came with CHEAP calls: CHEAP here never meant safe.
