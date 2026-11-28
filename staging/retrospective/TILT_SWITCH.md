# The yield-switched growth/value book with a tilt, horizons, 1-3 picks, stops and re-entry (hindsight)

**The idea (post-hoc):** `BASKET_SELECTION.md`'s near-misses, turned into a book.
- **The switch:** each month the 10-year yield's 6-month trend (Y6, `STYLE_SWITCH.md`) names the basket: VALUE when
  the yield is up, GROWTH when down.
- **VALUE picks:** the members whose floor EPS (guide or last year) fell most over 26 weeks.
- **GROWTH picks:** the members trading highest against their own P/E history (ties broken by the EPP gap).

**This is a sweep around one idea chosen after seeing the data.** The numbers carry that hindsight, and the twenty-four
stocks were picked in 2026. Read the grid for a stable region, and against the WHOLE-basket row run in the same engine.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/tilt_switch.py`, from daily total-return data, 2008-01-07 to
2026-11-17.
- **Fixed in advance:** the grid, in its docstring.
- **Added after the first run:** the `short` section, because the 1- and 3-month holds came out best.

**Selections:**
- **1, 2 or 3 picks;**
- **TILT:** half the whole basket plus half the 2 picks;
- **WHOLE:** the whole basket.

**Holding:** monthly cohorts held 1, 3, 6 or 12 months.

**Stops, per position:** traded at the next close, and the proceeds sit in cash.
- a fixed -15% from entry;
- a trailing -15% from the peak;
- trailing -10%, -15% or -20% with re-entry after a close above the 50-day average.

## 1. No stop: shorter holds and 2 picks did best

Annual return / Sharpe / worst drawdown, before costs:

| Selection | 1 month | 3 months | 6 months | 12 months |
|---|---|---|---|---|
| 1 pick | +18.3% / 0.68 / -67% | +27.3% / 1.02 / -54% | +21.9% / 0.89 / -50% | +20.5% / 0.89 / -51% |
| **2 picks** | **+31.2% / 1.14 / -56%** | **+28.7% / 1.16 / -49%** | +22.6% / 0.99 / -50% | +21.3% / 0.98 / -49% |
| 3 picks | +24.3% / 1.01 / -48% | +24.5% / 1.08 / -48% | +21.2% / 0.99 / -49% | +20.3% / 0.97 / -50% |
| TILT | +26.8% / 1.14 / -47% | +25.0% / 1.14 / -43% | +20.8% / 1.00 / -48% | +19.6% / 0.97 / -49% |
| WHOLE (baseline) | +22.0% / 1.04 / -37% | +21.1% / 1.04 / -38% | +18.7% / 0.95 / -46% | +17.8% / 0.91 / -49% |

SPY: +11.1% / 0.63 / -51%.

- **Shorter holds were better,** for every selection. 1-3 months beat 6-12.
- **Two picks beat one and three.** One pick was erratic (+18% at one month, +27% at three).
- **The tilt led WHOLE in both halves at 1-3 months:**

  | | 2008-2016 | 2017-2026 |
  |---|---|---|
  | 2 picks, 1 month | +23.7% | +38.3% |
  | WHOLE, 1 month | +20.0% | +23.8% |

  But the picked books fell deeper (-49% to -56% against -37%).

## 2. Stops: they help at short holds and hurt at long ones

Full period, before costs:

| Book | No stop | Fixed -15% | Trailing -15% | Trailing -15% + re-entry | Trailing -20% + re-entry |
|---|---|---|---|---|---|
| 2 picks, 1 month | +31.2% / 1.14 / -56% | +32.0% / 1.20 / -39% | **+32.5% / 1.24 / -36%** | +32.7% / 1.24 / -37% | +32.4% / 1.20 / -42% |
| 2 picks, 3 months | +28.7% / 1.16 / -49% | +25.0% / 1.17 / -32% | +24.0% / 1.19 / -28% | **+26.4% / 1.22 / -31%** | +27.4% / 1.21 / -37% |
| 2 picks, 6 months | +22.6% / 0.99 / -50% | +18.0% / 0.98 / -28% | +14.9% / 0.96 / -23% | +19.1% / 1.02 / -36% | +20.0% / 1.01 / -42% |
| 2 picks, 12 months | +21.3% / 0.98 / -49% | +15.3% / 0.94 / -27% | +8.7% / 0.78 / -18% | +17.3% / 1.01 / -37% | +17.9% / 0.99 / -40% |
| TILT, 1 month | +26.8% / 1.14 / -47% | +26.9% / 1.20 / -35% | +26.9% / 1.22 / -35% | +26.9% / 1.22 / -37% | +27.2% / 1.19 / -39% |
| WHOLE, 1 month | +22.0% / 1.04 / -37% | +21.4% / 1.07 / -33% | +20.9% / 1.08 / -36% | +20.8% / 1.07 / -37% | +21.5% / 1.06 / -35% |

- **At a 1-month hold, a 15% trailing stop cut the worst drawdown by a third** (-56% to -36% for 2 picks). It cost
  nothing in return. It rarely fires: about once a year, with 2% of position-time in cash.
- **At 6-12 months, stops cut returns sharply** (cash drag and whipsaws). With no re-entry the 12-month book spent
  43% of position-time in cash.
- **Re-entry (a close back above the 50-day average) mattered at longer holds,** where stopped positions otherwise sat
  out for months.
- **The -10% stop with re-entry traded far too often:** up to 60-220 exits a year counted across the overlapping
  cohorts.

## 3. After costs, with and without the half hedge

0.10% on each dollar traded, from the added `short` section: annual return / Sharpe / worst drawdown.

| Book | After costs | 2008-2016 | 2017-2026 |
|---|---|---|---|
| **2 picks, 1 month, trailing -15%** | **+29.3% / 1.14 / -37%** | +25.0% / 0.97 / -37% | +33.3% / 1.31 / -35% |
| 2 picks, 3 months, trailing -15% + re-entry | +25.2% / 1.18 / -31% | +21.2% / 1.00 / -31% | +28.9% / 1.35 / -29% |
| 2 picks, 1 month, trailing -15%, half hedge | +26.0% / 1.13 / -34% | +21.7% / 0.97 / -26% | +30.0% / 1.27 / -34% |
| TILT, 3 months, no stop, half hedge | +21.1% / 1.19 / -22% | +18.8% / 1.06 / -22% | +23.2% / 1.32 / -22% |
| TILT, 3 months, trailing -15% + re-entry | +21.6% / 1.18 / -32% | +19.3% / 1.03 / -32% | +23.7% / 1.33 / -24% |
| WHOLE, 1 month (baseline) | +19.1% / 0.93 / -38% | +17.1% / 0.81 / -38% | +20.8% / 1.06 / -34% |
| WHOLE, 3 months, half hedge | +17.3% / 1.09 / -25% | +16.7% / 1.04 / -16% | +17.9% / 1.14 / -25% |

**Calendar years after costs, 2 picks, 1 month, trailing -15%:**

| | Years |
|---|---|
| Best | 2020 +101%, 2021 +71%, 2024 +65%, 2009 +61% |
| Weakest | 2018 -24%, 2025 +7% |
| 2022 | +23% (SPY -18%), with the switch in value |
| Positive | 18 of 19 |

**Costs matter at a 1-month hold** (about 3 points a year here) and little at three months (about 1 point).

**The growth picks carried the book.** For the 2-pick, 1-month book (113 months in each style), NVDA, AVGO, MSFT and
AAPL were 30% of the weight but supplied 56% of the summed monthly returns (NVDA alone 22%). These figures were
computed after the run, outside the script. It is the same reliance on the tech winners as in `PE_PCTL_HEDGE.md` and
`RATIO_B_HEDGE.md`.

## Summary

1. **On this data, the best region is 2 picks, a 1-3 month hold and a 15% trailing stop.**
   - After costs: +25% to +29% a year, Sharpe about 1.15, worst drawdowns -31% to -37%.
   - Against the whole-basket switch's +19% / 0.93 / -38%, and in both halves.
2. **For a smoother ride, use TILT (half the basket, half the picks) held 3 months, with the half hedge:** +21% a year,
   Sharpe 1.19, worst drawdown -22%.
3. **Hold these with caution.** The tilt was found after seeing the data and then swept over about 150 settings. It
   rests on two names at a time, and the gains lean on the tech winners of 2020-2024. Expect much less going forward.
   The whole-basket switch (+19-22%) is the honest baseline.

## The newest month (October 2026): Y6 names VALUE

- **Basket:** CMCSA, NKE, LOW, PEP, LMT, PFE, BMY.
- **Picks by the largest 26-week fall in the floor's EPS:** NKE (-42%), then LOW (-2%). The third pick, BMY, is a tie
  at 0%. Only two members have a real EPS cut.
- **Fills:** 1 pick NKE; 2 picks NKE, LOW; 3 picks NKE, LOW, BMY.

These are hindsight hypotheses applied to point-in-time data, not advice.
