# Growth and value baskets, switched on bond yields and the ISM (hindsight)

**The idea:** split the twenty-four series into a growth basket and a value basket, then test whether interest rates
and the ISM manufacturing index tell when to hold which. The same rules are also run on the Russell 1000 Growth and
Value ETFs (IWF and IWD) from 2000: a broad market, chosen without hindsight, with eight years (2000-2007) that come
before every retrospective date.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/style_switch.py`.
- **Fixed in advance:** the baskets, signals and rules, in the script's docstring.
- **Added after the first run:** the `contrib` section, labelled so.

**Data:**
- **Yields:** ^TNX (10-year) and ^IRX (13-week), Yahoo daily closes.
- **ISM:** the ISM manufacturing PMI, as 50 + half the OECD's US manufacturing composite confidence balance
  (`data/us_mfg_confidence_oecd.csv`, from DBnomics' mirror of OECD). That series equals 2 x (PMI - 50) exactly:
  December 2008 -35.2 (PMI 32.4), April 2020 -17.0 (41.5), March 2021 +27.9 (64.0).
- **When a PMI month is usable:** from the 5th of the following month (ISM publishes on the first business day). The
  file ends at May 2026, and its last value carries forward.
- **Revisions:** it is the current vintage, with seasonal factors revised since. The ISM rules therefore carry a small
  revision look-ahead; the yield rules do not.

## 1. The baskets (point-in-time, each month)

Each month every ticker gets a value score: the average of its ranks on earnings yield (EPS / price, high), dividend
yield (high) and 5-year EPS growth (low). The most value-like third is the VALUE basket, the least value-like third the
GROWTH basket. Each basket holds about 7 names, in equal weight.

| Basket | Most frequent members (share of months) |
|---|---|
| GROWTH | NVDA 88%, MAR 81%, NKE 78%, AAPL 70%, SHW 68%, AVGO 60%, MSFT 49%, CMCSA 45% |
| VALUE | SO 88%, XOM 85%, PFE 81%, LMT 68%, F 64%, BMY 60%, KMI 50%, CAT 47%, WMT 45% |

| Annual return / Sharpe / worst drawdown | 2008-2026 | 2008-2016 | 2017-2026 |
|---|---|---|---|
| GROWTH basket | +19.8% / 0.90 / -57% | +16.0% / 0.72 / -57% | +23.4% / 1.10 / -31% |
| VALUE basket | +15.5% / 0.83 / -39% | +17.2% / 0.92 / -39% | +14.0% / 0.75 / -32% |
| SPY | +11.1% / 0.69 / -51% | +7.6% / 0.48 / -51% | +14.4% / 0.94 / -22% |

IWF and IWD over 2000-2026: +7.7% / 0.49 / -63% and +8.5% / 0.58 / -58%.

## 2. The rules

Each rule holds VALUE when its condition is true, GROWTH when false. The direction is the textbook one, set before
looking: rising rates and a strengthening economy favour value.

| Rule | Condition for VALUE |
|---|---|
| Y3 / Y6 | the 10-year yield is higher than 3 / 6 months ago |
| C3 | the curve (10-year minus 13-week) is steeper than 3 months ago |
| I50 | the PMI is 50 or above |
| I3 | the PMI is higher than 3 months ago |
| COMBO A | Y6 and I3 agree (otherwise half and half) |
| COMBO B | I50 and Y6 agree (otherwise half and half) |

## 3. Does the signal sort next month's value-minus-growth return?

Mean monthly spread when the rule says VALUE minus when it says GROWTH (Welch t):

| Rule | ETFs 2000-2026 | **ETFs 2000-2007** | ETFs 2008-2016 | ETFs 2017-2026 | Baskets 2008-2026 | Baskets 2008-2016 | Baskets 2017-2026 |
|---|---|---|---|---|---|---|---|
| Y3 | +0.7% (1.88) | +0.2% (0.26) | +0.3% (0.76) | +1.7% (2.55) | +1.0% (1.30) | +0.6% (0.62) | +1.7% (1.36) |
| Y6 | +0.6% (1.60) | +0.0% (0.01) | +0.4% (1.10) | +1.6% (2.39) | +1.1% (1.41) | +1.0% (0.99) | +1.5% (1.21) |
| C3 | +0.7% (2.00) | +0.2% (0.27) | +0.3% (0.93) | +1.7% (2.49) | +0.9% (1.19) | +0.0% (0.05) | +1.9% (1.61) |
| I50 | +0.3% (0.68) | **-1.4%** (-1.08) | +0.4% (0.79) | +1.2% (1.66) | +1.0% (1.03) | **-0.7%** (-0.44) | +2.1% (1.61) |
| I3 | +0.4% (1.19) | **-0.9%** (-1.16) | +0.6% (1.62) | +1.5% (2.07) | +0.4% (0.57) | **-0.1%** (-0.06) | +0.8% (0.68) |
| COMBO A | +0.9% (1.69) | **-0.4%** (-0.42) | +0.7% (1.73) | +2.4% (2.76) | +1.3% (1.13) | +0.8% (0.57) | +2.1% (1.17) |
| COMBO B | +0.7% (1.09) | **-1.1%** (-0.77) | +0.8% (1.15) | +2.6% (2.45) | +1.8% (1.38) | +0.6% (0.31) | +2.6% (1.40) |

- **The yield rules (Y3, Y6, C3) never pointed the wrong way,** in any period or universe. They were strong in
  2017-2026 (t of about 2.4-2.6 on the ETFs) and weak to nil before.
- **The ISM rules pointed the wrong way in 2000-2007 and on the baskets in 2008-2016.** Below-50 or falling PMI did not
  mean growth would lead. The ISM adds little beyond rates.

## 4. Switching books (hold what the rule says; monthly)

| Annual return / Sharpe / worst drawdown | ETFs 2000-2026 | ETFs 2000-2007 | ETFs 2017-2026 | Baskets 2008-2026 | Baskets 2017-2026 |
|---|---|---|---|---|---|
| always GROWTH | +7.7% / 0.49 / -63% | -4.0% / -0.13 / -61% | +17.2% / 0.93 / -30% | +19.8% / 0.90 / -57% | +23.4% / 1.10 / -31% |
| always VALUE | +8.5% / 0.58 / -58% | **+7.4% / 0.70 / -26%** | +11.1% / 0.74 / -30% | +15.5% / 0.83 / -39% | +14.0% / 0.75 / -32% |
| half and half | +8.2% / 0.56 / -53% | +1.8% / 0.20 / -44% | +14.4% / 0.91 / -25% | +18.2% / 0.98 / -46% | +19.3% / 1.12 / -23% |
| SPY | +8.3% / 0.57 / -53% | +1.4% / 0.18 / -43% | +14.8% / 0.94 / -24% | +11.1% / 0.69 / -51% | +14.4% / 0.94 / -22% |
| **switch on Y6** | +9.9% / 0.62 / -54% | +0.1% / 0.10 / -54% | **+19.4% / 1.16 / -21%** | **+22.0% / 1.11 / -37%** | **+23.8% / 1.31 / -16%** |
| **switch on C3** | **+10.6% / 0.67 / -55%** | +1.7% / 0.19 / -42% | **+20.1% / 1.17 / -22%** | +20.7% / 0.95 / -45% | +24.7% / 1.11 / -27% |
| switch on Y3 | +10.3% / 0.63 / -52% | +1.4% / 0.17 / -49% | +19.6% / 1.16 / -22% | +21.2% / 1.02 / -49% | +23.7% / 1.20 / -18% |
| switch on COMBO B | +9.5% / 0.61 / -53% | +0.2% / 0.10 / -53% | +18.4% / 1.11 / -24% | +21.0% / 1.09 / -43% | +24.3% / 1.38 / -22% |

The script also prints the 2008-2016 periods.
- **ETFs, 2008-2016:** Y6 +8.6% against half and half's +7.3%.
- **Baskets, 2008-2016:** Y6 +20.0% (Sharpe 0.94, worst drawdown -37%) against half and half's +17.0%.
- **Switching trades:** about 2-3 switches a year.

- **The best rule was the 10-year yield's 6-month trend (Y6),** for its consistency.
  - Value when the yield is above where it was 6 months ago, growth when below.
  - It beat half-and-half on the ETFs over 2000-2026 (+1.7 points a year) and on the baskets in both halves.
  - The ETFs' worst drawdown stayed about the same (-54%).
  - On the baskets it had the best risk profile: Sharpe 1.11 and a -37% drawdown, against always-growth's 0.90 and -57%.
- **It failed in 2000-2007.** Value won throughout the dot-com bust whatever rates did. Always-value made +7.4% a year;
  every switching rule made 0-2%.
- **The gains came from a few rate-regime years.** Switching on Y6 minus half and half, on the ETFs:

  | Year | Y6 against half and half |
  |---|---|
  | 2009 | +8.9% |
  | 2020 | +25.1% (falling yields: growth) |
  | 2022 | +11.7% (the rate shock: value) |
  | 2024 | +12.4% |
  | 2000 | -18.0% |

  The baskets show the same years (2008 +20.5%, 2020 +23.3%, 2022 +15.8%, 2024 +25.4%; 2017 -13.5%). In ordinary
  years the rule adds little. C3 spreads its gains more evenly (2001, 2002, 2009, 2023, 2025).

## Summary

1. **Rates beat the ISM as a growth/value switch.** The yield-trend and curve rules never pointed the wrong way. The ISM
   rules did, in two of the four periods, and added nothing on top of rates.
2. **The rule that held up best:** hold value when the 10-year yield is above its level 6 months ago, growth when below.
   From 2008 it added about 1.3-5 points a year over a fixed 50/50 split (ETFs 2008-2016 +1.3, baskets 2017-2026 +4.5,
   ETFs 2017-2026 +5.0), with lower drawdowns on the baskets.
3. **But it is a rates-regime bet:** most of the gain came in 2009, 2020, 2022 and 2024. It did nothing in the 2000-2007
   value run, and the signal-to-return link is statistically strong only since 2017.
4. **A 50/50 growth/value split is the baseline to beat,** and it is already decent. It beat always-growth on Sharpe in
   most periods tested here. The exceptions are the ETFs in 2008-2016 (0.47 against 0.51) and 2017-2026 (0.91 against
   0.93).

## Now (2026-11-17)

- **The 10-year yield is 5.10%,** above its level 3 and 6 months ago.
- **The curve (10-year minus 13-week) is +0.96 points** and steepening.
- **The PMI is 54.0** (May 2026, the last value in the file; it is stale) and rising.
- **Every rule says VALUE.**
- **The newest baskets (October 2026):**
  - VALUE: CMCSA, NKE, LOW, PEP, LMT, PFE, BMY;
  - GROWTH: NVDA, AVGO, AAPL, CAT, MAR, MSFT, WMT.

This is the rule applied to point-in-time data, not advice.

## Limits

- **Few regime changes:** about 2-3 switches a year, and the result rests on a handful of rate-regime years.
- **The ISM series is a revised vintage, and stale after May 2026.**
- **The baskets come from survivors picked in 2026.** The ETF test has no such bias.
- **Not modelled:** costs and taxes.
- **Hindsight in the reading:** the rules came from textbook direction, but which ones this file highlights (Y6, C3) was
  chosen after seeing the results.
