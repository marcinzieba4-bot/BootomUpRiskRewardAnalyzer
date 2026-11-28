# Ratio B long/short baskets (hindsight): eleven retrospective series, 2008-2026

Each month, the eleven tickers (ACN, UNP, LOW, AAPL, AVGO, MSFT, NKE, PEP, SHW, WMT, XOM) are sorted by the engine's
point-in-time **Ratio B** (downside to BEAR / upside to BULL), and a long/short basket is formed. This file reports how
those baskets did, rebalanced monthly and held for two to four years.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/ratio_b_basket.py` (one section: `... ratio_b_basket.py summary`).

**The rules were fixed in the script's docstring before the first run**:
- **Baskets:**
  - **TIER**: long the engine's BUY tier (Ratio B < 0.75), short AVOID (>= 1.75).
  - **BULL**: long the BUY tier, short only the tickers above their BULL price (Ratio B inf).
  - **RANK3**: long the three lowest Ratio B, short the three highest. Tickers above BULL are ordered by how far above.
- **Signal and entry:** Ratio B on each ticker's first as-of date of the month. Entry is at the next trading day's close.
- **Weights and returns:** equal weight; dividends reinvested; no costs, borrow fees or financing. The spread is long
  minus short.
- **Holding:** rebalanced monthly (1m), or overlapping monthly cohorts held 24, 36 or 48 months.

**Changed or added after the first run, and labelled where printed:**
- an empty leg's own return is now the equal-weight basket's, not 0% (the spread is unchanged);
- the newest basket now uses each ticker's latest date;
- turnover, "long minus SPY", the 2- and 4-name check and the cohort-age table were added as checks.

## 1. The spread

226 monthly formations, 2008-01 to 2026-10, with the last return to 2026-11-06.

| Basket | Hold | Annual return | Volatility | Sharpe | Worst drawdown | Positive months | t-stat (NW, 12 lags) | Beta to SPY |
|---|---|---|---|---|---|---|---|---|
| **RANK3** | **1m** | **+10.4%** | 18.8% | **+0.62** | -40% | 54% | **+2.96** | -0.06 |
| RANK3 | 24m | +2.9% | 14.5% | +0.27 | -33% | 52% | +1.49 | -0.05 |
| RANK3 | 36m | +3.5% | 13.8% | +0.32 | -33% | 52% | +1.76 | -0.03 |
| RANK3 | 48m | +3.2% | 13.0% | +0.31 | -31% | 52% | +1.64 | -0.03 |
| TIER | 1m | +3.5% | 20.9% | +0.27 | -52% | 47% | +1.20 | +0.03 |
| TIER | 24m / 36m / 48m | +0.0% / -0.4% / -0.4% | 15.0-12.7% | +0.08 to +0.03 | -42% to -46% | 49-50% | +0.42 to +0.17 | -0.07 |
| BULL | 1m | +4.1% | 21.3% | +0.29 | -66% | 34% | +1.14 | -0.05 |
| BULL | 24m / 36m / 48m | +0.3% / +0.8% / +0.7% | 12.0-9.3% | +0.08 to +0.13 | -41% to -33% | 41-42% | +0.38 to +0.62 | -0.05 |

For reference: SPY +11.2% a year (Sharpe 0.69, worst drawdown -51%); an equal-weight basket of all eleven +17.9% (1.07,
-35%).

- **Only the ranked basket rebalanced monthly cleared the noise.** RANK3 1m:
  - positive in 15 of 19 calendar years and in all four sub-periods (2008-2012 +5.6%, 2013-2017 +9.0%, 2018-2022 +16.7%,
    2023-2026 +10.8%);
  - positive with each ticker left out in turn (11 of 11; lowest +5.9% without AVGO, +6.6% without XOM);
  - about the same with two or four names a side (+10.3% and +8.7%, t +2.61 and +2.77);
  - market-neutral in practice (beta -0.06).
- **The engine's own tiers do not make a long/short basket.** TIER and BULL earned 3.5-4.1% a year monthly (t near 1.2,
  drawdowns of -52% and -66%) and about nothing over 2-4 years. BULL had no short leg in 80 of the 226 months.
- **Held two to four years, the edge is small and not reliable:** +2.9% to +3.5% a year (t 1.5-1.8), positive in 10-12
  of 19 years, and negative over 2023-2026 (-1.4% to -3.2%).

Worst calendar years for RANK3 1m: 2012 -21.8%, 2015 -14.1%, 2013 -6.3%. Best: 2022 +48.8%, 2008 +41.3%, 2017 +30.7%.

## 2. The edge is in the long leg

Each leg against the equal-weight basket of all eleven (EQUAL), annual return / Sharpe:

| Basket | Long leg | Short leg | Long minus EQUAL | EQUAL minus short | Long minus SPY |
|---|---|---|---|---|---|
| RANK3 1m | +31.0% / 1.46 | +17.1% / 0.94 | **+11.2% / 0.96** (drawdown -23%) | -0.2% / 0.03 | +17.1% / 1.09 (drawdown -27%) |
| RANK3 24m | +23.1% / 1.18 | +18.6% / 1.04 | +4.5% / 0.55 | -1.1% / -0.11 | +10.2% / 0.82 |
| TIER 1m | +22.6% / 1.02 | +16.9% / 0.94 | +4.1% / 0.34 | +0.0% / 0.05 | +9.7% / 0.61 |
| TIER 24m | +19.8% / 1.02 | +18.5% / 1.01 | +1.7% / 0.22 | -1.2% / -0.10 | +7.2% / 0.57 |

- **Buying the lowest Ratio B beat the basket. Shorting the highest earned nothing:** the high-Ratio-B names matched
  the basket. The short leg was mostly the compounders SHW, NKE, UNP, WMT and MSFT (each in it 35-40% of the months), so
  it worked as a hedge, not a source of return.
- **"Long minus SPY" carries the sample's hindsight.** EQUAL beat SPY by 6.7 points a year because the eleven were picked
  in 2026. Read "long minus EQUAL" as the signal's own contribution.

## 3. When the edge is earned: the first months after formation

Mean monthly spread of a cohort by its age, annualised (share of months positive):

| Basket | Month 1 | Months 2-3 | Months 4-6 | Months 7-12 | Months 13-24 | Months 25-36 | Months 37-48 |
|---|---|---|---|---|---|---|---|
| RANK3 | **+11.7%** (54%) | +7.3% (56%) | +3.9% (52%) | +3.4% (53%) | +1.4% (50%) | +4.4% (54%) | +1.8% (51%) |
| TIER | +6.2% (52%) | +8.4% (53%) | +5.3% (52%) | +2.5% (50%) | -0.6% (48%) | -0.1% (49%) | +1.8% (50%) |
| BULL | +9.7% (53%) | +7.5% (52%) | +3.2% (49%) | +2.9% (50%) | -1.3% (48%) | +3.8% (51%) | +1.3% (50%) |

Ratio B's information is spent within about six months. A plausible reason: the scenario prices move only at each
earnings print, so between prints Ratio B moves with the price. A low reading then partly means "fell since the last
print", and that rebound comes soon. **For a 2-4 year holder, re-reading Ratio B every month is worth more than holding
one month's ranking for years.**

## 4. Each monthly basket held to its end

Long and short legs compounded on their own; spread = long minus short, per $1 long and $1 short:

| Basket | Held | Cohorts | Median long | Median short | Median spread | Long beat short | Worst / best spread | Long beat SPY |
|---|---|---|---|---|---|---|---|---|
| RANK3 | 2y | 202 | +55% | +46% | +11.5% | 63% | -58% / +85% | 88% |
| RANK3 | 3y | 190 | +88% | +66% | +16.1% | 61% | -139% / +158% | 96% |
| RANK3 | 4y | 178 | +128% | +98% | +12.5% | 58% | -220% / +207% | 93% |
| TIER | 2y / 3y / 4y | 181 / 169 / 157 | | | +3.2% / +3.5% / -2.4% | 55% / 54% / 50% | | 87-92% |
| BULL | 2y / 3y / 4y | 122 / 112 / 108 | | | +0.2% / +15.2% / +15.7% | 50% / 68% / 56% | | 86-89% |

A worst spread below -100% means the short leg more than doubled. With three names a side, one runaway short decides
the cohort.

## 5. The newest basket

Readings dated 2026-10-22 to 2026-11-06, lowest Ratio B first: ACN -0.06, AVGO 0.36, LOW 0.46, MSFT 0.50, SHW 0.97,
UNP 1.64, PEP 2.16, NKE 4.05, XOM 5.52, AAPL inf, WMT inf.

| Basket | Long | Short |
|---|---|---|
| RANK3 | ACN, AVGO, LOW | XOM, AAPL, WMT |
| TIER | ACN, LOW, AVGO, MSFT | AAPL, NKE, PEP, WMT, XOM |
| BULL | ACN, LOW, AVGO, MSFT | AAPL, WMT |

ACN tops the long side under its live `DISRUPTION_EXPOSED` theme. Its below-BEAR dates since 2025-08 have lost money at
one year (`RATIO_EPP_FINDINGS.md` section 4). These are hindsight hypotheses applied to point-in-time readings, not a
model output or advice.

## Limits

- **Survivorship.** The universe is eleven companies chosen in 2026. Buying whichever has fallen toward its BEAR price
  pays more reliably among companies known to have survived and compounded.
- **Concentration.** Three names a side, from a pool of 10-11. A broader universe is needed before the RANK3 numbers mean
  much.
- **Costs.** About 17% of each leg's names change each month. At 0.05% a trade that costs about 0.4 points a year
  before borrow fees: small against RANK3 1m, not against the 2-4 year versions.
- **The t-stats overstate independence:** 226 months, one shared market, 12 Newey-West lags.
- Judgement calls made after the outcomes were visible: the checks listed at the top, and the mechanism offered in
  section 3.
