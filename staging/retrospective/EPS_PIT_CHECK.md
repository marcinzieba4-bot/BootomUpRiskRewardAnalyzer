# Was the falling-EPS short point-in-time? And without company guidance? (hindsight)

`RATIO_B_EPS_LS.md` shorted stocks with falling EPS. This file checks two questions:
1. Did the short use any EPS information that was not public before it was placed (look-ahead)?
2. How much did it rely on company guidance (a forecast, even if public), and does it work on reported EPS alone?

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/eps_pit_check.py`. The checks were fixed in its docstring
before the first run. The audit's matching was widened after the first run, as noted below and in the docstring.

## 1. No look-ahead: every EPS input was public before the trade

**The timing.** A signal is read on an as-of date and the trade is placed at the next trading day's close.
- retro/facts dates every source by publication. An after-close release is already dated the next day: for example,
  ACN's FY22 10-K, accepted 2022-10-12 at 21:04 ET, is dated 2022-10-13.
- So everything a signal uses was public before the trade.

**E1 (last fiscal year's EPS below the year before)** reads the as-of date's own EPS history.
- **On all 10,728 dates, the latest year in that history had been reported by the as-of date,** in an annual history
  vintage or a Q4 release from retro/facts.
- The first pass flagged 122 dates: ACN and UNP in the days just after their Q4 releases. Those two fact sheets label
  their Q4 prints only by name ("Q4 FY08", "Q4 2007"), with no quarter number, which the check had not read. Each
  flagged date came after its Q4 release (for example, UNP's Q4 2007 on 2008-01-24, ACN's Q4 FY08 on 2008-09-25).

**E2 (the floor's EPS lower than 26 weeks earlier)** reads EPP_TODAY_EPS.
- **On 6,859 dates it is the last reported full year.**
- **On 3,869 dates it comes from a company EPS guide: the midpoint of a range, or a growth guide applied to the last
  year.** Every one of those 3,869 dates matches a guide for the same fiscal year published on or before the as-of date.
  **None is matched only by a guide published later.**
- The first pass left 78 NKE and WMT dates unmatched. They use growth guides, such as "FY22's $6.46 -1%, the Q1 FY23
  release's guide", published 2022-05-17 for a 2022-05-18 date. The value check had not read growth guides.

| Ticker | Dates | Last reported year | From a guide (all published by the as-of date) |
|---|---|---|---|
| AAPL, AVGO, PEP, XOM | 3,848 | all | none (no numeric EPS guide) |
| SHW, ACN | 1,966 | none | all |
| LOW | 982 | 81 | 901 |
| WMT | 984 | 130 | 854 |
| MSFT, UNP, NKE | 2,948 | 2,800 | 148 |

**So the short used company guidance, a public forecast, not future data.** 23% of the 1,224 dates on which E3 fired
had a guide-based EPS.

## 2. With reported EPS only (no guidance)

Two filters built from reported results alone (retro/facts prints published by the as-of date):
- **RQ:** the latest quarter's EPS is below the same quarter a year earlier, both as printed in that release.
- **RB:** RQ and E1 (reported annual EPS down). It is the reported-only twin of E3.
- ACN's prints carry no quarterly EPS, so RQ and RB never fire on it.

RB fires about as often as E3 (1,221 dates against 1,224), but on a different mix of stocks: more LOW, WMT and MSFT;
fewer UNP and AVGO.

**The frozen pick from `RATIO_B_EPS_LS.md`** (long the 3 lowest Ratio B; short at 50%, each short held 6 months).
Annual return / Sharpe / worst drawdown, monthly data, 2008-2026:

| Universe | Short filter | Empty cohort | Full period | 2008-2016 | 2017-2026 | Beta |
|---|---|---|---|---|---|---|
| with tech | **E3 (uses guides)** | SPY | **+26.2% / 1.61 / -19%** | +19.7% / 1.33 / -19% | +32.5% / 1.85 / -12% | 0.30 |
| with tech | **RB (reported only)** | cash | **+24.4% / 1.39 / -20%** | +17.5% / 1.10 / -20% | +31.0% / 1.66 / -14% | 0.39 |
| with tech | RB | SPY | +22.7% / 1.38 / -20% | +16.3% / 1.12 / -20% | +28.9% / 1.61 / -14% | 0.31 |
| with tech | RQ | cash | +21.9% / 1.39 / -19% | +17.6% / 1.21 / -19% | +25.9% / 1.55 / -11% | 0.37 |
| with tech | *no short* | | *+31.0% / 1.46 / -33%* | | | |
| without tech | **E3 (uses guides)** | cash | **+15.5% / 1.06 / -15%** | +10.0% / 0.85 / -15% | +20.8% / 1.24 / -15% | 0.39 |
| without tech | **RB (reported only)** | cash | **+12.9% / 0.90 / -19%** | +8.7% / 0.78 / -16% | +17.0% / 1.01 / -19% | 0.31 |
| without tech | RQ | cash | +11.4% / 0.89 / -20% | +7.3% / 0.79 / -12% | +15.2% / 0.99 / -20% | 0.27 |
| without tech | *no short* | | *+16.9% / 0.95 / -25%* | | | |

- **Without guidance, the short sleeve still cut the worst drawdown by about a third** (-33% to -20% with tech, -25% to
  -19% without).
- **It no longer raised the Sharpe ratio.** RB with tech made 1.39, against 1.46 for the long book alone; without tech
  0.90 against 0.95.
- **So guidance carried part of the edge,** about 2-3 points a year and 0.15-0.2 of Sharpe. It is information that was
  public, and a company's own forecast is often the first public sign of falling EPS.

**The full procedure again, with reported-only filters** (216 settings, chosen on one half, judged on the other):

| Universe | Chosen on | Setting | On the other years (untouched) | Rank there |
|---|---|---|---|---|
| with tech | 2008-2016 | N=2, short RQ, hold 1m, 50%, cash | +24.5% / 1.08 / -19% | 98 of 216 |
| with tech | 2017-2026 | N=3, short E1, hold 3m, 50%, cash | +14.0% / 0.94 / -25% | 46 |
| without tech | 2008-2016 | N=2, short RB, hold 3m, 50%, cash | +15.3% / 0.78 / -25% | 49 |
| without tech | 2017-2026 | N=3, short E1, hold 3m, 50%, cash | +6.0% / 0.56 / -19% | 54 |

- **Less stable than with E3.** The two halves chose different filters and holds, and the settings' rank correlation
  between halves is +0.68 with tech and +0.70 without, against +0.88 and +0.72 with E3.
- **What held:** a short size of 50% and an unfiltered long side. RB had the best average Sharpe of the three
  reported-only filters (0.90 with tech, 0.47 without).

## 3. Summary

1. **No look-ahead.** Every EPS figure the short used was published on or before the signal date, and the trade
   happened the next day: 10,728 dates for E1, 3,869 guide-based dates for E2, no leaks.
2. **The E3 short partly used company guidance.** It was public, but it is a forecast: 23% of the short signals. If
   only reported numbers are allowed, use RB.
3. **Reported only, the strategy keeps the drawdown protection** (worst drawdown about -20% instead of -33% with tech,
   about -19% instead of -25% without), **but not the Sharpe improvement.**
   - With tech: about +24% a year, Sharpe 1.39.
   - Without tech: about +13% a year, Sharpe 0.90.

## The newest month (October 2026)

| Universe | Long | Short |
|---|---|---|
| With tech | ACN, LOW, AVGO | NKE |
| Without tech | LOW, SHW, UNP | NKE |

- RB shorts NKE, as E3 does: NKE's last quarter is below a year earlier, and so is its last full year.
- RQ alone would also short WMT.
