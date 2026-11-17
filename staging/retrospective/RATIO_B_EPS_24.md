# The Ratio B long / falling-EPS short on all twenty-four series: the out-of-sample test (hindsight)

Thirteen tickers were built after the Ratio B and EPS studies of the first eleven: **BKR, BMY, CAT, CMCSA, CTVA, F, KMI,
LMT, MAR, NVDA, PFE, RCL, SO**. The strategy and every setting were fixed before they existed in the repo, so they are an
out-of-sample test of it.

**The strategy** (`RATIO_B_EPS_LS.md`, `EPS_PIT_CHECK.md`): long the three lowest point-in-time Ratio B stocks, and short
50% in stocks with falling **reported** EPS.
- **RB, the falling-EPS filter:** the latest quarter's EPS below the same quarter a year earlier, *and* the last full
  year's EPS below the year before.
- **Shorts:** each monthly cohort is held 6 months.

Everything here is a **label or a hypothesis**. Never feed it back into a model, a fact sheet, a builder or a method rule
(retro/README.md, "The one rule").

Every number is printed by `python3 staging/retrospective/ratio_b_eps_24.py`.
- **Data:** it sets `RETRO_UNIVERSE=all`, a new opt-in switch in `cross_ticker_oos.py`. Without it, the earlier
  eleven-ticker scripts are unchanged.
- **Monthly:** next-day entry, dividends reinvested; no costs, borrow fees or cash interest. Prices to 2026-11-17, so
  the original eleven's figures are a few tenths different from the earlier files.
- **Fixed before the first run:** the strategies, universes and patterns, in the script's docstring. The "posthoc"
  section was added after reading the NEW results, and is labelled so.

**Point-in-time checks on the thirteen:**
- `eps_pit_check.py audit` with `RETRO_UNIVERSE=all`: on all 22,503 dates the EPS data was public by the as-of date.
  Every one of the 8,803 guide-based dates is matched by a guide published by then, and none is matched only by a
  later one.
- The audit was widened for two guide forms the thirteen use: a guide quoted with its date in the model's comment (F,
  SO), and a net-income guide divided by shares (KMI).
- The repo's point-in-time lint, on the thirteen's first-of-month signal dates: passed on all 2,701 dates: 0 errors, and every as-of price matched Yahoo's close within 0.5%.
  Its 583 warnings are the tool's "a later calendar year appears" check. A sample of 541 dates found only:
  - numbers read as years: share counts (BMY 2,078 and 2,027 million), segment revenue (BKR Digital Solutions $2,057
    million), a margin in basis points (PFE 2,079);
  - patent expiries quoted from a 10-K (PFE 2009: Lipitor's U.S. patent "expires in March 2010").
  None is a later fact.

## 1. The result: the strategy failed on the new stocks

Annual return / Sharpe / worst drawdown, 2008-2026 (monthly data):

| Strategy | ORIGINAL eleven | **NEW thirteen** | ALL twenty-four | ALL without tech (19) |
|---|---|---|---|---|
| SPY | +11.1% / 0.69 / -51% | +11.1% / 0.69 / -51% | +11.1% / 0.69 / -51% | +11.1% / 0.69 / -51% |
| EQUAL (all the universe's stocks) | +17.9% / 1.08 / -36% | +15.8% / 0.76 / -54% | **+17.1% / 0.94 / -46%** | +13.8% / 0.78 / -46% |
| A: long 3 lowest Ratio B | +30.6% / 1.45 / -33% | **+9.9% / 0.48 / -57%** | +19.7% / 0.80 / -44% | +15.3% / 0.67 / -47% |
| **B: A + 50% RB short** | +24.1% / 1.38 / -20% | **-1.6% / 0.05 / -73%** | +9.2% / 0.52 / -33% | +7.0% / 0.43 / -45% |
| C: A + 50% E3 short (uses guidance) | +26.0% / 1.60 / -19% | +2.5% / 0.22 / -49% | +13.9% / 0.72 / -35% | +11.4% / 0.64 / -34% |
| D: A - 50% SPY | +24.0% / 1.46 / -17% | +4.8% / 0.32 / -46% | +14.0% / 0.69 / -37% | +9.7% / 0.53 / -41% |
| E: long 6 lowest Ratio B + 50% RB short | +14.2% / 1.03 / -17% | +3.1% / 0.26 / -61% | +9.0% / 0.59 / -37% | +6.1% / 0.45 / -46% |

- **On the thirteen new stocks the strategy lost money:** -1.6% a year with a -73% worst drawdown. It failed in both
  halves:

  | NEW thirteen | 2008-2016 | 2017-2026 |
  |---|---|---|
  | B | -8.8% | +5.5% |
  | A, unhedged | +5.5% | +14.1% |

  It made money in only 11 of 19 calendar years, and lost 52.5% in 2009.
- **It doesn't hang on one stock.** With each new ticker left out, B on the thirteen ran from -3.9% a year (no CMCSA) to
  +4.7% (no F).
- **On all twenty-four, plain equal weight had the best Sharpe (0.94).** No strategy here beat it on a risk-adjusted
  basis. A made 2.6 points more a year with a lower Sharpe; B made 7.9 points less.
- **The original eleven's numbers came from the list.** Within them the strategy beat every one of 200 random-pick runs
  (section 2); outside them, it did not.

## 2. Both legs failed, for different reasons

Each leg against EQUAL (mean monthly difference, annualised):

| Universe | Long: 3 lowest Ratio B | Shorted names: RB (negative = a good short) | E3 names | Above-BULL names |
|---|---|---|---|---|
| ORIGINAL eleven | **+11.0%/yr** | +1.4%/yr | -0.7%/yr | -1.5%/yr |
| NEW thirteen | **-4.0%/yr** | **+7.6%/yr** | +6.0%/yr | +4.6%/yr |
| ALL twenty-four | +4.0%/yr | +1.7%/yr | +1.4%/yr | -0.2%/yr |
| ALL without tech | +2.9%/yr | +5.1%/yr | +1.5%/yr | -1.8%/yr |

| Three random longs a month (200 runs) | Random median | Ratio B long (A) | Random runs at or above A | Random + RB sleeve | B | Runs at or above B |
|---|---|---|---|---|---|---|
| ORIGINAL eleven | +17.3% | +30.6% | 0 | +11.4% | +24.1% | 0 |
| **NEW thirteen** | +14.3% | **+9.9%** | **175 of 200** | +2.6% | **-1.6%** | **179 of 200** |
| ALL twenty-four | +16.8% | +19.7% | 33 of 200 | +6.1% | +9.2% | 26 of 200 |

- **The long side:**
  - Among the eleven compounders, a low Ratio B marked a quality company on sale.
  - Among the new thirteen, it marked value traps. The long book sat most often in CMCSA (58% of months), KMI (43%),
    BKR (40%), LMT (30%) and F (27%), and as a leg it lagged EQUAL by 4.0% a year.
  - Picking the three lowest Ratio B did worse than 175 of 200 random picks.
- **The short side:**
  - The RB short was most often F (26% of months), then PFE (18%) and MAR, CAT and KMI (16% each); on all twenty-four,
    XOM (29%) and F (26%) led.
  - In a cyclical such as F, MAR, CAT, KMI or XOM, falling reported EPS mostly marks the bottom of the earnings cycle.
  - The shorted names then beat the average by 7.6% a year. 2009 is the extreme: shorting cyclicals at their earnings
    low cost the new-thirteen book 52.5%.
  - Even on the original eleven the RB names were not losers (+1.4% a year against EQUAL). The short worked there as a
    cheap hedge against a long side that was itself strong, not as a source of return.

## 3. Other patterns (fixed in advance; nothing chosen on the new thirteen)

Each is a long side plus a 50% short sleeve, held 6 months. Annual return / Sharpe:

| Pattern | ORIGINAL eleven | NEW thirteen | ALL twenty-four | ALL without tech |
|---|---|---|---|---|
| B: long 3 lowest Ratio B; short RB | +24.1% / 1.38 | -1.6% / 0.05 | +9.2% / 0.52 | +7.0% / 0.43 |
| O1: long 3 lowest Ratio B; short above-BULL | +23.0% / 1.22 | +3.1% / 0.25 | +10.7% / 0.52 | +8.4% / 0.44 |
| O2: long 3 lowest Ratio B; short expensive & running | +20.4% / 1.15 | +0.9% / 0.17 | +8.4% / 0.44 | +9.6% / 0.49 |
| O3: long 3 lowest Ratio B; short RQ (quarter only) | +21.5% / 1.37 | +1.1% / 0.16 | +10.4% / 0.59 | +8.4% / 0.51 |
| O4: long 3 lowest Ratio B, RB stocks barred; short RB | +22.2% / 1.23 | -0.6% / 0.09 | +9.5% / 0.53 | +7.1% / 0.43 |
| **O5: long 3 deepest below the 52-week high (price only); short RB** | +20.6% / 1.10 | **+12.8% / 0.56** | **+15.7% / 0.62** | **+11.5% / 0.51** |
| O6: long 3 lowest Ratio B, RQ stocks barred; short RB | +18.1% / 0.99 | -0.2% / 0.11 | +8.9% / 0.55 | +6.7% / 0.45 |

**Only O5 held up on the new stocks.** It swaps the Ratio B long for a price-only one: the three stocks furthest below
their 52-week high. This is the "deep fall" signal of `CROSS_TICKER_OUT_OF_SAMPLE.md` and `LONG_TERM_FINDINGS.md`. Even
so, its falling-EPS short held it back, and no pattern beat EQUAL's Sharpe on all twenty-four (0.94).

## 4. Post-hoc leads (chosen after reading section 1; not findings)

| Pattern | ORIGINAL eleven | NEW thirteen | ALL twenty-four | ALL without tech | Beta (ALL) |
|---|---|---|---|---|---|
| EQUAL (reference) | +17.9% / 1.08 / -36% | +15.8% / 0.76 / -54% | +17.1% / 0.94 / -46% | +13.8% / 0.78 / -46% | 1.00 |
| H1: long 3 deepest below the 52-week high, no short | +26.3% / 1.09 / -36% | +22.8% / 0.70 / -60% | +24.7% / 0.74 / -60% | +18.0% / 0.61 / -69% | 1.58 |
| H2: long every BUY-tier stock (Ratio B < 0.75) | +22.2% / 1.00 / -44% | +10.8% / 0.54 / -54% | +15.8% / 0.78 / -46% | +11.5% / 0.60 / -46% | 1.00 |
| H3: long the falling-EPS stocks (RB), 6 months | +15.3% / 0.73 / -49% | +21.8% / 0.69 / -57% | +20.4% / 0.78 / -52% | +17.1% / 0.69 / -52% | 1.16 |
| H4: H1 minus a static 50% SPY | +20.3% / 1.08 / -30% | +18.0% / 0.64 / -47% | +19.7% / 0.68 / -47% | +13.3% / 0.53 / -54% | 1.08 |

- **Buying the deepest fallers (H1) earned the most everywhere,** 4-8 points a year above EQUAL. But it carries a beta
  of about 1.6 and drawdowns of -60% to -69%, and its Sharpe was no better than EQUAL's. That looks like extra risk
  rather than skill.
- **Buying falling-EPS stocks (H3)** beat EQUAL on the new thirteen (+6.0 points) but lagged it on the original eleven
  (-2.6). It is inconsistent.

## 5. Summary

1. **The Ratio B long / falling-EPS short did not survive the out-of-sample test.** On thirteen stocks it had never
   seen, it lost 1.6% a year. Its success on the first eleven came from the list: compounders picked in 2026.
2. **A low Ratio B is not a buy signal on its own,** and falling EPS is not a short signal on its own. In a broader list
   they flag value traps and cyclical troughs.
3. **On twenty-four stocks, equal weight had the best Sharpe.** The deep-fall long earned the most return, at much
   higher risk.

## The newest month (October 2026), for the record

| Universe | Long (3 lowest Ratio B) | RB short |
|---|---|---|
| ALL twenty-four | ACN, CMCSA, BKR | NKE, PFE |
| NEW thirteen | CMCSA, BKR, NVDA | PFE |
| ALL without tech | CMCSA, BKR, LOW | NKE, PFE |

The strategy failed its out-of-sample test. This is not advice.
