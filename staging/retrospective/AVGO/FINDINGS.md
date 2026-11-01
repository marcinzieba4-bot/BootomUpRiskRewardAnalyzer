# AVGO retrospective findings (hindsight)

Patterns seen in `outcome.json` for the AVGO weekly dates: 22 from 2009-08-07 to 2009-12-31, the first weeks after the
2009-08-06 listing (no AVGO price exists before it; retro/README.md, "AVGO"), and 157 from 2010-01-08 to 2012-12-31. They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. Each batch was scored only after its
point-in-time build was committed and pushed (2009: b3106d7; 2010-2012: 04c4511). Prices run to 2026-10-30; the 2009 batch's
two-year horizons end by 2011-12-30 (three-year: 2012-12-28), the 2010-2012 batch's by 2014-12-30 (2015-12-30). Medians of an even
count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

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

## 2010-2012 (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 61 | +78% | +29% to +230% | 60 | 61 | +61% | 61 |
| class FAIR | 74 | +28% | -3% to +172% | 34 | 27 | +14% | 25 |
| class RICH | 22 | +94% | +0% to +118% | 21 | 21 | +52% | 1 |
| legacy tier BUY | 155 | +65% | -3% to +230% | 114 | 107 | +38% | 86 |
| legacy tier ACCUMULATE | 1 | +29% | +29% | 0 | 1 | +26% | 1 |
| legacy tier WATCHLIST | 1 | +50% | +50% | 1 | 1 | +69% | 0 |
| 2010 to the Q4 FY10 print (FY08's $0.26) | 47 | +67% | +29% to +107% | 46 | 47 | +63% | 41 |
| Q4 FY10 to Q4 FY11 print (FY10's $1.69) | 52 | +17% | -3% to +58% | 11 | 5 | +8% | 27 |
| Q4 FY11 to Q4 FY12 print (FY11's $2.19) | 52 | +108% | +49% to +185% | 52 | 51 | +50% | 14 |
| from the Q4 FY12 print (FY12's $2.25) | 6 | +225% | +172% to +230% | 6 | 6 | +130% | 5 |

- **CHEAP held on all 61 dates; RICH failed on 21 of 22.** The CHEAP dates returned a median +78% over two years, cleared the
  hurdle on 60 and beat SPY on all 61. The RICH dates were six in January and February 2010 and fifteen in 2012:
  - In January and February 2010 the adjusted gap read OVERVALUED (-0.50 to -1.35). BULL's EPS was held to BASE's +14.6%/yr
    guide, and the 15%/yr hurdle price sat above the BULL price on four dates and between BASE and BULL on two. These dates
    returned +50% to +104%.
  - In 2012 the conservative case fell below -15% on a negative BASE (-1.5% to -5.8%/yr). These dates returned +61% to +118%.
  - Only 2011-07-01 held: +0.5% over two years, 24.5pp behind SPY.
- **FAIR was the weak class, and the weak year was the one after the FY10 print.** From December 2010 to November 2011, with the
  price 74-154% above the EPP floor and the class FAIR on 49 of the 52 dates, the two-year return was a median +17% (+6% at one
  year), and the stock lagged SPY on 47 of the 52 (median -14pp). FAIR's call (within 15pp of SPY) held on 25 of its 74 dates.
  It failed on 25 from December 2010 to November 2011 by lagging by more than that. It failed on 24 from December 2011 by
  beating SPY by 22-121pp (median 72pp).
- **The floor distance ranked the outcomes; the signal composite ranked them backwards.** Across the 157 dates:
  - the EPP gap ranks the two-year returns at Spearman -0.77 (-0.89 on the m12-24 average), and the conservative case at +0.49
    (+0.78);
  - the adjusted gap ranks them at -0.29, Ratio B at about 0 (-0.07), and the entry price at -0.03 (but -0.81 on the 47 dates
    before the Q4 FY10 print);
  - the proxy composite ranks them at -0.47:
    - It read 3.2-3.7 on the four FY10 prints (dates from 2010-02-26 to 2011-02-18). Across them the median two-year return
      fell from +86% to +18%.
    - It read 2.55-2.9 on the next three prints (dates from 2011-02-25 to 2011-11-25), whose dates returned medians of +5% and
      +24%.
    - It read 2.0-2.3 on the FY12 prints (from 2012-02-24), whose dates returned medians of +73% and +138%.
  That is the pattern NKE's 2008 batch recorded as a hypothesis (last-quarter operating signals lean pro-cyclical). Here it is
  again a hypothesis: test it on other tickers and years before any method change, never fit it to AVGO's outcomes.
- **Every date beat SPY over three years** (+57% to +383%, by 10-328pp). At one year 72 of the 157 lagged it.
- **BASE was the nearest anchor at two years** on 136 dates (BULL 14, XBULL 7, BEAR none).
  - Before the Q4 FY10 print the history had no growth run to measure, so BULL took BASE's rate (+14.6% to +57.1%/yr). The
    seven January-February 2010 dates landed nearest XBULL, at 1.29-1.53 times the BULL price.
  - From that print on, BULL compounded FY2008's $0.26 across the excluded FY2009: +155%/yr, then +103.5% and +71.5%.
    - To November 2012 the two-year price reached only 0.18-0.64 times that BULL price.
    - The fourteen BULL landings came from September 2012: eight at 0.60-0.64 times the +103.5% case, and six from the Q4 FY12
      print at 0.92-1.02 times the +71.5% case.
  - Ratio B read 0.05-0.16 on all 110 dates from that print, and the tier was BUY on every one, so neither separated them.
- **The FY2008 call, seen afterwards.** Restarting the history after FY2009 (FY2008 out) would have turned 57 dates RICH
  (retro/README.md, "AVGO 2010-2012"): 49 from 2010-12-17 to 2011-11-25 and 8 in 2012. A RICH call would have held on 37 of the 57
  (37 of the 49 in 2011, none of the 8 in 2012), against 25 for the classes as built. That is a fact about one stock in one year,
  not a reason to change the encoding: the call was decided before scoring and stays, and changing a rule means a new method
  version tested elsewhere.
- **The other calls, seen afterwards.** FY2010 at $1.58 instead of GAAP $1.69 would have moved 14 classes; BASE on the latest
  quarter instead of the guides 10; the engine revision and the dollar-level guide none. None of those comparisons is a reason to
  change an encoding.
