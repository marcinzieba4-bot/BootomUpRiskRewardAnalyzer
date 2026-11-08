# The Ratio B book hedged with sector ETFs (hindsight), with and without tech, 2008-2026

Each month the long book buys the three lowest point-in-time Ratio B stocks in the universe, equal weight. Each position
is hedged with its own sector's Select Sector SPDR:

| ETF | Sector | Stocks |
|---|---|---|
| XLK | Technology | AAPL, MSFT, AVGO, ACN |
| XLE | Energy | XOM |
| XLP | Consumer Staples | PEP, WMT |
| XLY | Consumer Discretionary | LOW, NKE |
| XLI | Industrials | UNP |
| XLB | Materials | SHW |

Two universes: all eleven (with tech), and the seven without tech.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/ratio_b_sector.py`, from daily total-return data, 2008-01-07 to
2026-11-06. The modes and tests were fixed in its docstring before the first run. The "overlap" section was added after.
The reference mode reproduces `ratio_b_hedge.py` (27.0%) and `ratio_b_nontech.py` (13.1%) exactly.

**Hedge modes.** Each short is sized to the position's value every day, and trades at the next day's close.
- **TACTICAL** (main): short the position's sector ETF while that ETF closes below its own 100-day average.
- **TACTICAL 50%**: the same at half size.
- **SPX TIMING**: sector ETFs as the hedge, but on while the S&P 500 is below its 100-day average.
- **ALWAYS**: short the sector ETF every day, a pure "stock against its sector" bet.
- **SPY hedge** (reference): the whole book hedged with SPY on the S&P 500 timing, from the earlier files.

## 1. The result

| Mode | With tech: return / Sharpe / worst drawdown | Without tech: return / Sharpe / worst drawdown |
|---|---|---|
| SPY bought and held | +11.2% / 0.64 / -51% | +11.2% / 0.64 / -51% |
| Equal weight of the universe | +17.9% / 0.96 / -37% | +13.6% / 0.78 / -35% |
| Unhedged | +31.1% / 1.29 / -35% | +16.9% / 0.84 / -35% |
| **TACTICAL sector hedge** | **+22.6% / 1.28 / -27%** | **+9.4% / 0.68 / -34%** |
| TACTICAL 50% | +27.2% / 1.38 / **-25%** | +13.4% / 0.84 / -31% |
| SPX TIMING, sector instruments | +24.7% / 1.35 / -30% | +11.7% / 0.79 / -30% |
| ALWAYS (stock against sector) | +11.5% / 0.84 / -44% | +2.4% / 0.25 / -38% |
| SPY hedge (reference) | +27.0% / **1.41** / -28% | +13.1% / 0.83 / **-28%** |

- **Sector hedges did worse than one market hedge.**
  - With tech: the full tactical sector hedge earned 4.4 points a year less than the SPY hedge, for about the same worst
    drawdown.
  - Without tech it was worse than not hedging at all: +9.4% a year with a -34% worst drawdown, against +16.9% and -35%
    unhedged, and +13.1% and -28% with the SPY hedge.
- **The half-size sector hedge roughly matched the SPY hedge.** With tech: +27.2% with the lowest worst drawdown (-25%).
  Without tech: +13.4% against +13.1%.
- **After a 0.10% charge on every dollar traded:**

  | Universe | Tactical | Tactical 50% | SPY hedge |
  |---|---|---|---|
  | With tech | +20.2% | +25.6% | +25.0% |
  | Without tech | +7.4% | +12.2% | +11.5% |

## 2. Why the sector hedge disappointed

1. **Sector ETFs below their 100-day average tended to rebound.** At each monthly entry where a pick's sector ETF was
   below its average, that ETF returned +2.3% over the next month (with tech; +1.9% without), against +1.2% (+0.9%)
   when it was above. Shorting on that signal shorted the rebound.
   - The first guess, that Ratio B picks stocks whose sector had just broken down, was wrong. Picks had the hedge on at
     entry 31-32% of the time, the same rate as every stock in the universe (30-32%).
2. **Defensive sectors fall less in a market crash, so their hedge pays less.** For example:

   | Crash, without tech | Sector hedge | SPY hedge |
   |---|---|---|
   | 2008-2009 | +28.8% | +59.9% |
   | 2011 | -10.1% | -0.8% |

   In the fast crashes (2018, 2020, 2025) the sector hedge did as well as SPY, or better.
3. **More signals, more whipsaw.** The sector hedge was on for 30-31% of the book's value on average, against 26% for
   the SPY hedge, and each sector switched on its own.

## 3. What the always-hedged mode reveals: Ratio B's stock picking against the sector

Shorting the sector every day leaves only "did the pick beat its own sector?" (beta to SPY -0.08). Against 200 runs of
three random stocks a month from the same universe with the same hedge:

| Universe | Random median | Random 95th percentile | **Ratio B book** | Random runs at or above |
|---|---|---|---|---|
| With tech | +3.7% | +7.1% | **+11.5%** | 0 of 200 |
| Without tech | +2.6% | +5.2% | **+2.4%** | 109 of 200 |

- **With tech, Ratio B beat its picks' sectors by 11.5 points a year,** far above any random run. But that list holds
  AVGO and AAPL, which were picked in 2026 as winners; this is the hindsight of `RATIO_B_HEDGE.md`, "Is the 27% real?".
- **Without tech, Ratio B's picking added nothing beyond sector exposure:** +2.4% against a random median of +2.6%.
  Even random picks beat their sectors by about 3 points a year, which is the survivors' premium.
- This suggests the non-tech book's edge over random picks seen before (`RATIO_B_NONTECH.md`, section 3) came from
  which sectors and when, not from picking stocks within a sector.
- Unhedged, the non-tech Ratio B book beat 188 of 200 random runs. With the tactical sector hedge, 61 random runs matched or beat it.

## 4. Crashes and years (full tactical sector hedge)

| SPY peak - trough | SPY | With tech: unhedged / sector / SPY hedge | Without tech: unhedged / sector / SPY hedge |
|---|---|---|---|
| 2008-05 - 2009-03 | -51.5% | -22.2% / +18.8% / +45.8% | -14.5% / +28.8% / +59.9% |
| 2011-04 - 2011-10 | -18.6% | -2.6% / +4.4% / +13.7% | -14.4% / -10.1% / -0.8% |
| 2018-09 - 2018-12 | -19.3% | -19.7% / -3.3% / -7.2% | -23.6% / -6.1% / -11.9% |
| 2020-02 - 2020-03 | -33.7% | -34.2% / -6.2% / -8.0% | -34.2% / -6.2% / -8.0% |
| 2022-01 - 2022-10 | -24.5% | +3.9% / +5.9% / +11.9% | -0.8% / +2.3% / +6.2% |
| 2025-02 - 2025-04 | -18.8% | -17.2% / -4.9% / -2.5% | -15.5% / -4.7% / -0.7% |

Positive calendar years:
- **with tech:** unhedged 19 of 19, sector tactical 17, SPY hedge 18;
- **without tech:** 16, 16 and 14.

The sector-hedged non-tech book's weak years: 2015 (-21.1%), 2023 (+0.6%), 2024 (+2.0%), 2025 (+2.0%), 2026 to date
(-14.1%).

## 5. Where it sits now (2026-11-06)

| Universe | Held since 2026-10-05 | Sector hedges on now |
|---|---|---|
| With tech | ACN, LOW, AVGO | XLK for ACN and AVGO (XLK is 11.2% below its 100-day average); LOW's XLY is above (+2.5%) |
| Without tech | LOW, SHW, UNP | XLI for UNP (-7.4%); XLY (+2.5%) and XLB (+1.2%) are above |

The other sector ETFs: XLE +0.1%, XLP +6.1%, against their 100-day averages. This is the rule applied to
point-in-time data, not advice.

## Hypotheses (test before use)

1. **Hedge with the broad market, not with sectors, or hedge sectors at half size.** In this sample, sector 100-day
   signals pointed the wrong way more often than the market's did.
2. **Read Ratio B as a sector and timing signal, not a stock-within-sector signal,** at least outside tech. Testing this
   needs more stocks per sector than this sample has (at most four).
3. **Before trusting the with-tech stock-picking edge, test it on a tech list chosen without hindsight.**

## Limits

- **Survivorship:** the stocks are survivors picked in 2026, and the with-tech results carry most of that hindsight.
- **Few stocks per sector:** one or two per sector except tech, so "stock against sector" rests on few names.
- **Not modelled:** interest on the short proceeds, borrow fees and taxes.
