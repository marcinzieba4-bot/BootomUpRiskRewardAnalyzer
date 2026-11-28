# Does a small EPP gap mean little room to fall? And selling puts on it, with a martingale (hindsight)

**Hypothesis tested:** when the price is near or below the EPP floor (a small EPP gap), there is little room left to fall,
so selling puts is safe, even with martingale sizing (doubling the stake after each losing month). Also tested with the
Ratio B filters.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/epp_downside.py`.
- **Data:** 10,725 weekly dates across the eleven series, with Yahoo daily closes to 2026-11-06. Entry is the close after
  each as-of date.
- **Fixed before the first run:** the tests and the put rules, in the script's docstring.
- **Added after the first run:** the "single" section.
- **Not real option prices:** no option-price history is in the repo, so the put P&L uses Black-Scholes premiums from
  each stock's own recent volatility.

## 1. The EPP gap does not predict a smaller fall

Downside after entry, all eleven. "Worst" is the deepest close below the entry price within the window.

| EPP gap | Dates | Volatility | 1m: fell > 10% | 3m: worst 5% | 3m: fell > 20% | 12m: worst 5% | 12m: fell > 30% |
|---|---|---|---|---|---|---|---|
| **below the floor (<= 0%)** | 1,328 | 31% | 6% | **-26%** | 9% | **-41%** | **11%** |
| 0-40% | 3,289 | 26% | 5% | -23% | 7% | -38% | 11% |
| 40-100% | 4,184 | 25% | 5% | -20% | 5% | -33% | 7% |
| 100-200% | 1,316 | 28% | 6% | -28% | 10% | -39% | 11% |
| > 200% | 480 | 33% | 5% | -19% | 4% | -40% | 9% |
| every date | 10,597 | 26% | 5% | -22% | 7% | -36% | 9% |

- **Near or below the floor, the downside was as large as anywhere, or larger.** The worst 5% of 12-month falls from
  below the floor reached -41%, against -36% for every date.
- **Volatility is higher there** (31% against 26%). Measured in units of each stock's own volatility, falls below the
  floor were slightly smaller: a fall of more than one standard deviation in 3 months happened 6% of the time, against 8%
  overall. That is the only hint in the hypothesis's favour, and it is small.

**The floor did not hold:**

| Starting point | Broke below it within 3 months | within 12 months | Depth below it when it broke: median / worst 5% |
|---|---|---|---|
| 0-40% above the EPP floor | 18% | **31%** | -12% / **-49%** |
| 40-100% above the EPP floor | 0% | 3% | -8% / -35% |
| above the BEAR price, Ratio B 0-0.75 | 9% | 16% | -11% / -36% |

**Already below the floor, the stock still fell further:** 12-month median worst -9% and worst 5% -41%, against -9% and
-36% for every date. 21% of those dates saw a fall of more than 20%. The worst cases:

| Stock | From | EPP gap | Ratio B | Worst fall within 12 months |
|---|---|---|---|---|
| LOW | 2008-09 | 0% | 0.20 | -51% |
| ACN | 2025-10 | -5% | -0.12 | -50% |
| MSFT | 2008-04 | -46% | 0.15 | -50% |
| NKE | 2024-09 | -2% | 0.62 | -40% |
| NKE | 2025-02 | -16% | 0.43 | -34% |

## 2. With the Ratio B filter: only "below the BEAR price" shows a thinner tail

| Cell | Dates | 1m: fell > 10% | 3m: worst 5% | 12m: worst 5% | 12m: fell > 30% |
|---|---|---|---|---|---|
| Ratio B < 0.75 and EPP gap <= 40% (all eleven) | 2,879 | 5% | -25% | -37% | 11% |
| below BEAR (all eleven) | 390 | 7% | -27% | **-31%** | **6%** |
| below BEAR and below the floor (all eleven) | 345 | 6% | -26% | -31% | 5% |
| below BEAR, without tech | 247 | **2%** | **-18%** | **-29%** | **4%** |
| below BEAR and below the floor, without tech | 234 | 2% | -16% | -27% | 3% |
| every date (all eleven / without tech) | 10,597 / 6,797 | 5% / 5% | -22% / -21% | -36% / -36% | 9% / 9% |

- **The combined filter (Ratio B < 0.75, EPP gap <= 40%) is no safer than any date.**
- **Price below the BEAR price is the one reading with a thinner tail, mainly without tech:** a monthly fall over 10% on
  2% of dates against 5%, and a 12-month fall over 30% on 3-4% against 9%.
- **That evidence is narrow.** It comes from about 25 episodes, mostly the 2008-2009 lows, WMT 2010-2012 and LOW
  2022-2023. With tech it includes ACN from late 2025: below both its BEAR price and its floor, it then fell 50% within
  a year.

## 3. Selling 1-month puts: the result depends on the premium assumption

Each month, a 1-month put sold on every stock that passes the filter, equal size, cash-secured. Return on the capital
committed, 2008-01 to 2026-10, premium at 1.1x volatility.

| Universe | Filter | Strike | Months | Losing months | Worst month | Fixed size: annual / worst drawdown |
|---|---|---|---|---|---|---|
| all eleven | every stock | 5% below | 226 | 30 | -12% | +13% / -12% |
| all eleven | EPP gap <= 40% | 5% below | 219 | 37 | -10% | +12% / -10% |
| all eleven | Ratio B < 0.75 and EPP gap <= 40% | 5% below | 193 | 32 | **-24%** | +11% / **-26%** |
| all eleven | below BEAR | 5% below | 65 | 7 | -12% | +6% / -18% |
| without tech | below BEAR | 5% below | 44 | **1** | -0% | +5% / -0% |
| without tech | below BEAR | 10% below | 44 | **0** | +0% | +3% / 0% |

- **The profit is set by an assumption the data cannot check.** With premiums priced at 0.9x, 1.1x and 1.3x recent
  volatility, the same trades return +2%, +6% and +11% a year (all eleven, Ratio B < 0.75 and EPP gap <= 40%, 10%
  below).
  - Real premiums also carry the extra price of downside protection (put skew), bid-ask spreads and early assignment.
  - Settling this needs real option prices, which are not in the repo.
- **The worst month came from the EPP + Ratio B filter:** March 2025, -21% of committed capital at 10% below. The filter
  had loaded the low-Ratio-B names (ACN, NKE) just before the April 2025 sell-off.
- **Below BEAR without tech was the cleanest:** 0-1 losing months out of 44. But that is only 44 months, and it does not
  contain a case like ACN 2025-2026.

## 4. The martingale

- **Rule:** start at 10% of equity, double the stake after every losing month, return to 10% after a winning one.
  Variants: capped at 100% (cash-secured), or uncapped (on margin).
- **Results:**
  - **It never ruined the account in this sample.** The longest run of losing months was 1-3, even one stock at a time
    (AAPL had a run of 3). The largest stake reached was 20-80% of equity.
  - **It also barely earned anything:** +1% to +3% a year. With a 10% starting stake, most capital sits idle (cash
    interest is not modelled). The same puts at a fixed 100% stake earned +4% to +23% a year per stock, with worst
    drawdowns of -8% to -41%.
- **Why the sample hides the danger:** a martingale fails on a long losing streak.
  - A stock that falls month after month needs the stake doubled each time: five losing months turn 10% into 320%.
  - All eleven stocks here are survivors picked in 2026. The months-long declines of failing companies are missing.
  - Single months already lost up to -37% of committed capital (AAPL). Doubled into such a month, the loss is doubled
    too.

## Summary

1. **The hypothesis does not hold for the EPP gap.** A small or negative gap did not mean little room to fall: the floor
   broke within a year from 31% of dates 0-40% above it, and the tail was as deep as anywhere.
2. **The only Ratio B reading with a thinner tail is "price below BEAR", mainly without tech.** Its evidence is about 25
   episodes, mostly crisis lows, and ACN in 2025-2026 is a live counter-example.
3. **Selling puts on these signals has no proven edge.** The result depends on the premium assumed, and real option
   prices are needed to settle it.
4. **Do not use a martingale.** It added almost nothing here, and its risk lies in losing streaks that this survivor-only
   sample does not contain.

## Where the newest dates sit

| Ticker | EPP gap | Fall to the EPP floor | Ratio B | Fall to BEAR | Volatility | One-standard-deviation 1-month move |
|---|---|---|---|---|---|---|
| ACN | -7% | floor above the price (+6%) | -0.06 | BEAR above the price (+4%) | 66% | -19% |
| LOW | +8% | -18% | 0.46 | -33% | 30% | -9% |
| PEP | +9% | -11% | 2.16 | -70% | 25% | -7% |
| NKE | +29% | -22% | 4.05 | -77% | 36% | -11% |
| MSFT | +38% | -29% | 0.50 | -29% | 32% | -9% |
| SHW | +34% | -30% | 0.60 | -28% | 28% | -8% |

ACN is the only stock below both levels, and its volatility (66%) is the highest of the eleven. This is point-in-time data
read through hindsight labels, not advice.
