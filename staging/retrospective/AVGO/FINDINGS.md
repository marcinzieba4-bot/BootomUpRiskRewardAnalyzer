# AVGO retrospective findings (hindsight)

Patterns seen in `outcome.json` for the AVGO weekly dates: 22 from 2009-08-07 to 2009-12-31, the first weeks after the
2009-08-06 listing (no AVGO price exists before it; retro/README.md, "AVGO"). They are **labels and hypotheses**: never feed them
back into the method or the fact sheet. The batch was scored only after its point-in-time build was committed and pushed
(b3106d7). Prices run to 2026-10-30; the two-year horizons end by 2011-12-30 (three-year: 2012-12-28). Medians of an even count
take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

## 2009 (22 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH (every date) | 22 | +93% | +60% to +127% | 22 | 22 | +91% | 0 |
| legacy tier AVOID | 15 | +96% | +60% to +127% | 15 | 15 | +87% | 0 |
| legacy tier BUY | 6 | +91% | +78% to +127% | 6 | 6 | +98% | 0 |
| legacy tier ACCUMULATE | 1 | +60% | +60% | 1 | 1 | +77% | 0 |
| to the Q3 FY09 print (no guide; BASE -20.9%/yr) | 4 | +80% | +60% to +88% | 4 | 4 | +76% | 0 |
| Q4 FY09 guide of the Q3 release (BASE -11.9%/yr) | 6 | +105% | +77% to +127% | 6 | 6 | +87% | 0 |
| Q4 FY09 guide update (BASE -6.6%/yr) | 7 | +119% | +82% to +127% | 7 | 7 | +106% | 0 |
| from the Q4 FY09 print (BASE +14.6%/yr) | 5 | +79% | +60% to +91% | 5 | 5 | +95% | 0 |

- **The RICH call failed on every date.** RICH expects the stock to miss the hurdle and lag SPY. All 22 dates cleared the hurdle
  and beat SPY over two years, by 43pp to 109pp, while SPY returned +10% to +29%. The stock also beat SPY at one year (by 2-60pp)
  and at three (by 43-96pp; three-year returns +76% to +137%). The two-year window held a 25-30% drawdown (the July-August 2011
  fall from $39.08 to $27.19) but no close below $14.49 (2009-11-03), 12% under the first date's price.
- **The two-year price was above every scenario price on every date:** 1.31-3.05 times the XBULL price and 1.77-2.26 times the
  BEAR price. The nearest scenario was BEAR on 13 dates (from August to October BEAR was the highest scenario price, the bounds rule
  putting BULL and XBULL on BASE's negative rate) and XBULL on 9. Neither the bounds rule's scenarios nor the window's multiples
  contained the outcome.
- **Nothing in the model ranked the outcomes except the price.** Across the 22 dates the entry price ranks the two-year returns at
  Spearman -0.74 (-0.86 on the m12-24 average) and the EPP gap at -0.70 (-0.23); the adjusted gap at +0.35 (-0.38), the proxy
  composite at +0.46 (+0.63) and Ratio B at about 0 (-0.49). The best entries were the cheapest: the late-October and November dates
  ($15.00-15.86) returned +82% to +127%. The tiers did not separate the outcomes (AVOID median +96%, BUY +91%). One stock over five
  months mostly tests "buy lower", as AAPL's and NKE's 2008 batches found.
- **What drove the verdict, seen afterwards.** Every input the model used was public and every rule mechanical, yet the verdict
  rested on three things a longer history would have supplied:
  - a one-year history (FY08 alone, after three loss years), so the bounds rule left no bull case beyond the guided growth;
  - a P/E window of a few weeks, so the multiple was measured against itself (the class did not depend on the EPS level: the
    company's non-GAAP EPS would have changed no class, retro/README.md "AVGO");
  - BASE growth from one quarter's revenue guide, which was negative to November because the year-ago quarters were the last ones
    before the 2008-09 downturn.
  The model also had no input for what the prospectus and releases said about the capital structure: the IPO proceeds and cash
  went to a debt tender offer (completed in October) and to redeeming the remaining senior and floating rate notes (called in
  October, paid on December 1), and long-term debt on the balance sheet fell from $700M (August) to $230M (November); interest
  ($86M in FY08, $77M in FY09) and the $54M sponsor fee weighed on GAAP EPS. Those lines are display only in method r2 (a quarter's outlook components; no figure is derived from another).
  Hypothesis for the method: for a newly listed or recently recapitalized company, a trailing GAAP anchor with a one-year history
  and a weeks-long multiple window carries little information, and the bounds rule turns that into a systematic RICH read. A later
  version could wait for a minimum history or window before classifying, or encode announced deleveraging. Test it on other new
  listings and years before any method change; never fit it to AVGO's outcomes.
- **The knife-edge dates were not a signal.** On 2009-10-30 and 2009-11-06 the tier read BUY only because the price fell to or below
  the BEAR price while every scenario sat below the hurdle price (retro/README.md, "AVGO", "A flat expected-price curve"). Those two
  dates returned +126% and +127%, as did their AVOID neighbours (+113% on 2009-10-23, +122% on 2009-11-13): the outcome followed the
  price, not the tier.
- **The encoding calls, seen afterwards.** No class moves under any alternative tried before scoring (FY08 net EPS moves the one
  knife-edge class; non-GAAP EPS, the guide reading and a BEAR bounded by BASE move none). The RICH verdict on these dates is the
  method's, not one encoding's. That is a fact about one stock in one five-month window, not a reason to change an encoding: the
  calls were decided before scoring and stay, and changing a rule means a new method version tested elsewhere.
