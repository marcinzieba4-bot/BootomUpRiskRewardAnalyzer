# RCL retrospective findings (hindsight)

Patterns seen in `outcome.json` for the RCL weekly dates: 522 from 2008-01-04 to 2017-12-29. They are **labels and hypotheses**: never feed
them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed and pushed (2008-2009:
ea16eb8; 2010-2013: fa305ce; 2014-2017: 6b78a85). Outcomes were computed on 2026-11-08 from the closes posted to 2026-11-06; every date has its 6-month, 1-, 2-
and 3-year horizons.
Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP (every date) | 53 | +5.2% | -34.0% to +536.9% | 15 | 42 | -5.9% | 42 |
| legacy tier BUY | 49 | +5.9% | -34.0% to +536.9% | 15 | 39 | -1.9% | 39 |
| legacy tier ACCUMULATE | 4 | -0.7% | -32.3% to +1.7% | 0 | 3 | -8.8% | 3 |
| FY07 EPS $2.825 (to 2008-01-25) | 4 | -23.2% | -32.3% to -19.4% | 0 | 0 | -52.9% | 0 |
| FY08 EPS $3.30 (2008-01-31 to 2008-04-18) | 12 | -8.8% | -34.0% to +5.7% | 0 | 5 | -42.4% | 5 |
| FY08 EPS $2.925 (2008-04-25 to 2008-07-18) | 13 | +7.1% | -3.2% to +24.7% | 0 | 13 | -11.7% | 13 |
| FY08 EPS $2.60 (2008-07-23 to 2008-10-24) | 14 | +14.9% | -11.5% to +142.9% | 5 | 14 | +3.7% | 14 |
| FY08 EPS $2.755 (from 2008-10-29) | 10 | +295.8% | +145.0% to +536.9% | 10 | 10 | +181.9% | 10 |
| price under the EPP floor | 20 | +145.0% | -2.4% to +536.9% | 15 | 20 | +98.4% | 20 |
| price at or over the EPP floor | 33 | -1.4% | -34.0% to +16.1% | 0 | 22 | -29.2% | 22 |

- **CHEAP held on 42 of 53 dates, but the early dates lost a third.** The 11 failures are the dates from 2008-01-04 to 2008-03-20 but
  2008-03-14 (two-year returns -9% to -34%, 0.6-16.5pp behind SPY). From 2008-03-28 every date beat SPY, whose two-year return ran from -19% to +57%. Only the 15
  dates from 2008-09-26 cleared the hurdle; the 14 of October-December returned +67% to +537%. One-year returns had a median of -41.9%
  (ahead of SPY on 16), three-year returns +30.6% (-17% to +293%, ahead of SPY on 44). Every date sat through a 64-87% drawdown to the
  2009-03-02 close of $5.50.
- **The floor was not a floor.** CHEAP came from the EPP floor (the median of the calendar-year P/E lows, 9-11x) times the guided EPS,
  $23-31 a share in 2008, while the price fell to $5.50 within months. The guide the floor rested on was cut three times in 2008 ($3.30 to
  $2.60) and the next year's first guide was $1.40, so the floor moved down with the earnings rather than holding the price. Under the floor
  the call worked (20 dates, median +145%); at or over it, it did not (33 dates, median -1.4%, none cleared the hurdle). Hypothesis, not a
  rule: for a business whose earnings fall with demand, a floor anchored on the current year's guide moves with the cycle; test a floor on
  normalized or trailing-cycle earnings on other cyclical tickers before any method change.
- **January 2008 was the worst entry, and its BASE was the most inflated.** The four January dates returned -19% to -32%; their BASE growth,
  +19.7%/yr, came from the Q4 2007 guide including Pullmantur (net revenue +23.8%), which the sensitivity run already flagged as moving two of
  them to FAIR on the comparable basis. Seen afterwards, an acquisition-inflated guide lifted BASE at the top; hypothesis only.
- **The signals read the last good quarter.** The proxy composite peaked at 3.00 on the Q1 2008 print (every signal at BULL or better)
  and those dates returned -3% to +25%; it was 2.20 through the trough of Q4 2008. Across the 53 dates it ranks the return to the m12-24
  average price at Spearman -0.27 (the wrong way); the entry price ranks it at -0.99, the EPP gap at -0.84 and Ratio B at -0.71, and the
  adjusted gap at +0.43. One stock through one crash mostly tests "buy lower".
- **The two-year price landed nearest BEAR on 30 dates, BASE on 21 and BULL on 2,** at 1.5-3.6 times the BEAR price ($13-17) and 0.3-0.9
  times BULL: by 2010 the stock had recovered to $23-47 from the $5.50 low, which no scenario priced (BEAR was the 2001 fall, -28.6%/yr,
  at the 10th-percentile P/E). The outcomes record prices, not EPS.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 19 | +407.2% | +142.1% to +693.9% | 19 | 19 | +257.6% | 19 |
| class FAIR | 7 | +166.7% | +146.8% to +188.2% | 7 | 7 | +155.6% | 0 |
| class RICH | 26 | +16.9% | -7.7% to +141.9% | 8 | 12 | +67.2% | 14 |
| legacy tier BUY | 16 | +432.4% | +203.6% to +693.9% | 16 | 16 | +351.7% | 16 |
| legacy tier ACCUMULATE | 9 | +169.1% | +142.1% to +194.5% | 9 | 9 | +166.2% | 3 |
| legacy tier WATCHLIST | 2 | +153.4% | +141.9% to +153.4% | 2 | 2 | +145.4% | 0 |
| legacy tier AVOID | 25 | +16.7% | -7.7% to +138.1% | 7 | 11 | +65.8% | 14 |
| FY09 EPS $1.40 (2009-01-30 to 2009-04-17) | 12 | +518.0% | +218.1% to +693.9% | 12 | 12 | +380.1% | 12 |
| FY09 EPS $1.35 (2009-04-24 to 2009-07-24) | 14 | +166.7% | +119.4% to +203.6% | 14 | 14 | +158.9% | 4 |
| FY09 EPS $0.75 and $0.70 (from 2009-07-30, Ratio B infinite) | 23 | +11.2% | -7.7% to +108.9% | 5 | 9 | +64.2% | 14 |

- **CHEAP to mid-April was the trade of the series.** The 19 CHEAP dates (2009-01-09 to 2009-04-17, and four in June-July) all cleared the
  hurdle, at +142% to +694%; the 14 under the floor returned a median +490%. Every 2009 date beat SPY over one year (median +92.6%).
- **The trough-year anchor read the recovery as RICH.** From 2009-07-30 the current-FY EPS was the FY09 guide of $0.75, then $0.70, a
  trough year: the stock's 19.5-37.7x on it ranked at the 86th-100th percentile of its own window, BULL (the decade EPS CAGR of 2.5% on that
  EPS, at the 75th-percentile P/E) priced it at $12-13 against $15-26, and Ratio B went infinite. The stock then rose to $49.96 on
  2011-01-14; the m12-24 average price was 32-163% above the entry on every one of those 23 dates, and the two-year price landed at 1.7-2.4
  times BULL. The two-year endpoints (July-December 2011) caught a fall back to $22-31, so the RICH call "held" on 14 of 23 by the endpoint
  test, but by the endpoint-robust measure it was wrong on all of them. Every 2009 date landed nearest BULL (28) or XBULL (24). This is the
  same lesson as SHW 2008 (a guided trough year read RICH), here on the EPS anchor of every scenario and the floor at once. Hypothesis for
  the method, not a rule: test a mid-cycle or multi-year EPS anchor for the scenarios and the floor on other cyclical tickers and periods;
  never fit it to RCL's outcomes.
- **FAIR failed by being too cautious.** The 7 FAIR dates (April-July 2009) returned +147% to +188%, 104-132pp ahead of SPY, outside the
  ±15pp band the class expects; so did the three RICH dates before July (+119% to +142%).
- **Within the year the adjusted gap ranked the outcome.** Across the 52 dates the adjusted gap ranks the m12-24 return at Spearman +0.94,
  the EPP gap at -0.97, Ratio B at -0.91 and the entry price at -1.00; the proxy composite at +0.31. The gap's ranking is the anchor
  change again: it fell from +1.55 to -2.27 as the EPS guide fell and the price rose.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 17 | -3.0% | -18.1% to +16.3% | 0 | 0 | +0.3% | 0 |
| class FAIR | 12 | -3.4% | -16.6% to +22.1% | 0 | 0 | -6.3% | 3 |
| class RICH | 23 | -15.6% | -27.9% to +11.1% | 0 | 0 | -18.3% | 23 |
| legacy tier ACCUMULATE | 9 | +2.0% | -13.5% to +16.3% | 0 | 0 | +4.1% | 0 |
| legacy tier WATCHLIST | 14 | -11.0% | -18.1% to +1.6% | 0 | 0 | -6.7% | 0 |
| legacy tier AVOID | 29 | -12.1% | -27.9% to +22.1% | 0 | 0 | -13.8% | 26 |
| FY09 EPS $0.70 (to 2010-01-22) | 3 | +6.7% | -0.8% to +11.1% | 0 | 0 | +30.5% | 3 |
| FY10 EPS $2.10 (2010-01-29 to 2010-04-23) | 13 | -6.7% | -27.3% to +22.1% | 0 | 0 | +0.2% | 12 |
| FY10 EPS $2.20 (2010-04-29 to 2010-07-16) | 12 | -12.9% | -24.2% to +16.3% | 0 | 0 | +0.3% | 1 |
| FY10 EPS $2.30 (2010-07-23 to 2010-10-22) | 14 | -3.2% | -13.5% to +4.7% | 0 | 0 | -9.8% | 0 |
| FY10 EPS $2.45 (from 2010-10-27) | 10 | -16.2% | -27.9% to -13.8% | 0 | 0 | -34.3% | 10 |

- **Nothing cleared the hurdle or beat SPY over two years.** The 52 dates returned -28% to +22%, 7-45pp behind SPY, and every one sat
  through the fall from $49.96 (2011-01-14) to $20.01 (2011-10-03), -59.9%. RICH held on all 23; the 17 CHEAP dates (2010-05-21 to
  2010-09-17) returned -18% to +16%, 22-43pp behind SPY, so the call failed on every one (over three years they returned +21% to +57%).
  The two-year price landed nearest BASE on 46 dates.
- **The signals peaked at the top again.** The proxy composite read 3.05-3.20 on the Q1-Q3 2010 prints (yields up, costs down, revenue
  +17-19%, margins +422-489bp), the series' highest, a year before the fall; it ranks the return to the m12-24 average price at Spearman
  -0.66 within 2010 (-0.87 within 2011). The entry price ranks it at -0.93. As in 2008, the signals read the last good quarter.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 24 | +63.2% | +5.6% to +95.8% | 22 | 20 | +39.2% | 22 |
| class FAIR | 20 | -11.4% | -22.0% to +3.5% | 0 | 0 | -20.9% | 0 |
| class RICH | 8 | -22.1% | -26.7% to -3.3% | 0 | 0 | -37.1% | 8 |
| legacy tier BUY | 9 | +77.2% | +56.0% to +95.8% | 9 | 9 | +52.5% | 9 |
| legacy tier ACCUMULATE | 13 | +60.9% | +44.0% to +87.8% | 13 | 11 | +33.4% | 13 |
| legacy tier WATCHLIST | 16 | -7.4% | -21.6% to +22.7% | 0 | 0 | -14.1% | 0 |
| legacy tier AVOID | 14 | -20.3% | -26.7% to -3.3% | 0 | 0 | -32.6% | 8 |
| FY10 EPS $2.45 (to 2011-01-21) | 3 | -24.5% | -26.7% to -22.1% | 0 | 0 | -40.0% | 3 |
| FY11 EPS $3.35 (2011-01-28 to 2011-04-21) | 13 | -18.2% | -23.0% to -11.4% | 0 | 0 | -29.3% | 2 |
| FY11 EPS $3.20 (2011-04-29 to 2011-07-22) | 13 | -3.3% | -10.7% to +5.6% | 0 | 0 | -14.1% | 3 |
| FY11 EPS $2.90 (2011-07-29 to 2011-10-21) | 13 | +60.7% | +22.7% to +81.7% | 12 | 10 | +43.8% | 12 |
| FY11 EPS $2.75 (from 2011-10-28) | 10 | +70.2% | +46.2% to +95.8% | 10 | 10 | +39.2% | 10 |

- **CHEAP after the fall was the trade of these four years.** The 23 CHEAP dates from 2011-07-29 to 2011-12-30 returned +23% to +96% (median
  +63%), and the call held on 22 of the 24 CHEAP dates; the four under the EPP floor (2011-08-19 to 2011-10-07) returned +72% to +82%. The
  same shape as late 2008 and early 2009: CHEAP after the price had fallen 40-60% worked, CHEAP before the fall (mid-2010) did not.
- **FAIR in February-July 2011 should have been RICH.** The 20 FAIR dates returned -22% to +3.5%, 28-44pp behind SPY, outside the ±15pp
  band the class expects; they priced the FY11 guide of $3.35 and $3.20, a record the company was guiding to, at 10.8-13.6x. The 8 RICH dates
  held. One-year returns had a median of -26.4%.
- **Within the year every price measure ranked the outcome.** The entry price ranks the m12-24 return at Spearman -0.99, the P/E on guided
  EPS -0.98, Ratio B -0.95, the EPP gap -0.94, the adjusted gap +0.86. One stock through one fall again mostly tests "buy lower".

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 4 | +81.0% | +73.7% to +85.6% | 4 | 4 | +38.2% | 4 |
| class FAIR | 2 | +152.0% | +127.5% to +152.0% | 2 | 2 | +96.2% | 0 |
| class RICH | 46 | +115.9% | +60.8% to +162.1% | 46 | 46 | +67.0% | 0 |
| legacy tier ACCUMULATE | 4 | +81.0% | +73.7% to +85.6% | 4 | 4 | +38.2% | 4 |
| legacy tier WATCHLIST | 2 | +152.0% | +127.5% to +152.0% | 2 | 2 | +96.2% | 0 |
| legacy tier AVOID | 46 | +115.9% | +60.8% to +162.1% | 46 | 46 | +67.0% | 0 |
| FY11 EPS $2.75 (to 2012-01-27) | 4 | +81.0% | +73.7% to +85.6% | 4 | 4 | +38.2% | 4 |
| FY12 EPS $2.10 (2012-02-03 to 2012-04-13) | 11 | +89.4% | +60.8% to +100.3% | 11 | 11 | +38.9% | 0 |
| FY12 EPS $1.95 (2012-04-20 to 2012-07-20) | 14 | +128.1% | +88.2% to +152.0% | 14 | 14 | +82.2% | 0 |
| FY12 EPS $1.75 (2012-07-27 to 2012-10-19) | 13 | +131.5% | +85.5% to +162.1% | 13 | 13 | +73.8% | 0 |
| FY12 EPS $1.90 (from 2012-10-26) | 10 | +115.3% | +97.1% to +153.1% | 10 | 10 | +62.8% | 0 |

- **RICH on 46 dates, wrong on every one.** From 2012-02-03 the stock at $24.11-35.25 returned +61% to +162% over two years, 27-115pp ahead
  of SPY (+34% to +55%), and the two-year price ($48-82) landed at 1.2-2.2 times BULL ($33-42). The four CHEAP dates of January 2012 held
  (+74% to +86%); the two FAIR dates (2012-05-18, 2012-06-01) were too cautious (+128%, +152%).
- **The class followed BASE, and BASE followed capacity.** With the BEAR case at 2009's -72%/yr, the downside to BEAR was 91-97% on every
  date, so Ratio B was decided by the upside to BULL alone, and BULL was BASE or a decade CAGR of 3.7-5.4%/yr. BASE came from the net
  revenue guide, Net Yields times capacity, and capacity growth fell from 6-15% a year in 2010-2011 to 0-2.5% from 2012: BASE fell from
  +19-20%/yr to -1.8% to +3.9%/yr and the class went RICH. Across 2010-2013 BASE ranks the m12-24 return at Spearman -0.76: the 116
  dates with BASE at 7%/yr or more returned a median -3.0% over two years (37 cleared the hurdle), the 93 under it +130.4% (90 cleared).
  Hypothesis, not a rule: for a capacity business, low capacity growth may be supply discipline, and the earnings growth that followed
  came through the margin, which method r2's BASE cannot see without a margin guide (the margin step is 0), while a single collapse year
  as BEAR leaves Ratio B blind to the downside. Test a BASE with a margin path, and a BEAR that a single year cannot set, on other
  cyclical tickers and periods; never fit either to RCL's outcomes.

## 2013 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH (every date) | 53 | +136.0% | +89.1% to +161.7% | 53 | 53 | +92.9% | 0 |
| legacy tier AVOID | 53 | +136.0% | +89.1% to +161.7% | 53 | 53 | +92.9% | 0 |
| FY12 EPS $1.90 (to 2013-02-01) | 5 | +129.9% | +110.4% to +141.6% | 5 | 5 | +66.2% | 0 |
| FY13 EPS $2.40 (2013-02-05 to 2013-07-19) | 24 | +136.4% | +89.1% to +161.7% | 24 | 24 | +99.6% | 0 |
| FY13 EPS $2.25 (2013-07-26 to 2013-10-18) | 13 | +142.6% | +127.4% to +154.2% | 13 | 13 | +98.6% | 0 |
| FY13 EPS $2.325 (from 2013-10-25) | 11 | +121.8% | +109.4% to +137.1% | 11 | 11 | +88.2% | 0 |

- **RICH on all 53, wrong on all 53.** Two-year returns +89% to +162%, 54-131pp ahead of SPY; one-year returns +25% to +83%, ahead of SPY
  on every date; the two-year price ($68-103) landed at 1.5-2.5 times BULL ($37-45) and 0.35-0.58 times XBULL. The 12 dates with the price
  already above BULL (Ratio B infinite: 2013-01-25 and every date from 2013-10-25) returned +109% to +137%. The worst drawdown within two
  years was 20-22%.
- **Within the year the adjusted gap ranked the outcome** (Spearman +0.65; BASE +0.50, the EPP gap -0.59), but no measure of the method
  reached a class other than RICH: the 83 consecutive RICH dates from 2012-06-08 are the series' longest wrong run.

## 2010-2013 together

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 45 | +47.2% | -18.1% to +95.8% | 26 | 24 | +29.8% | 26 |
| class FAIR | 34 | -7.4% | -22.0% to +152.0% | 2 | 2 | -16.7% | 3 |
| class RICH | 130 | +117.2% | -27.9% to +162.1% | 99 | 99 | +72.4% | 31 |
| BASE 7%/yr or more | 116 | -3.0% | -27.9% to +100.3% | 37 | 35 | -2.6% | 57 |
| BASE under 7%/yr | 93 | +130.4% | -0.8% to +162.1% | 90 | 90 | +85.7% | 3 |
| RICH, BASE 7%/yr or more | 39 | -12.1% | -27.9% to +100.3% | 11 | 11 | -18.3% | 28 |
| RICH, BASE under 7%/yr | 91 | +130.4% | -0.8% to +162.1% | 88 | 88 | +85.2% | 3 |

- **RICH held when it came with high guided growth and failed when it came with low.** The 31 RICH calls that held are the 23 of 2010
  (three of them January's, on FY09's trough EPS) and the 8 of 2011; the 99 that failed are 2012-2013. CHEAP held on 26 of 45, every one
  of them from 2011-08-05 to 2012-01-27, after the 2011 fall. The proxy composite ranks the m12-24 return at -0.70 across the four years (the wrong way, as in 2008).
- **Six years of one stock, read together** (2008-2013, labels only): CHEAP worked after a fall (October 2008 to April 2009, August 2011 to
  January 2012) and failed before one (January-March 2008, mid-2010); RICH mostly worked when the guided anchor or growth was high
  (2010-2011) and failed when a trough or a low-growth guide set it (late 2009, 2012-2013). The method's EPS anchor and BASE move with the cycle,
  and the series' wrong calls cluster where the cycle turned.

## 2014 (51 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH (every date) | 51 | +32.5% | -0.5% to +92.0% | 26 | 42 | +50.4% | 9 |
| FY13 EPS $2.325 (to 2014-01-24) | 3 | +87.2% | +72.3% to +92.0% | 3 | 3 | +73.0% | 0 |
| FY14 EPS $3.30 (2014-01-28 to 2014-04-17) | 12 | +48.6% | +35.8% to +62.9% | 12 | 12 | +63.1% | 0 |
| FY14 EPS $3.35 (2014-04-25 to 2014-07-18) | 13 | +40.0% | +23.0% to +53.4% | 10 | 13 | +53.6% | 0 |
| FY14 EPS $3.45 (from 2014-07-25) | 23 | +14.1% | -0.5% to +32.5% | 1 | 14 | +20.5% | 9 |

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH (every date) | 53 | +34.5% | +2.6% to +64.3% | 29 | 43 | +6.7% | 9 |
| FY14 EPS $3.45 (to 2015-01-23) | 4 | +4.4% | +2.6% to +6.2% | 0 | 0 | -8.9% | 4 |
| FY15 EPS $4.75 (2015-01-30 to 2015-04-17) | 12 | +28.6% | +22.9% to +31.4% | 0 | 12 | +0.8% | 0 |
| FY15 EPS $4.55 (2015-04-21 to 2015-07-24) | 14 | +46.3% | +36.1% to +64.3% | 14 | 14 | +9.0% | 0 |
| FY15 EPS $4.70 (2015-07-31 to 2015-10-16) | 12 | +36.9% | +27.6% to +44.2% | 9 | 10 | +7.5% | 2 |
| FY15 EPS $4.80 (from 2015-10-23) | 11 | +34.2% | +21.7% to +40.5% | 6 | 7 | +9.9% | 3 |

- **RICH for two years while the stock doubled.** The 108 RICH dates from 2014-01-10 to 2016-01-29 returned -0.5% to +92% over two years
  (median +34.7%), ahead of SPY on 88; the call held on 18 (late 2014, January 2015 and five dates of late 2015). One-year returns from 2014 dates were +20% to
  +82%, ahead of SPY on all 51; the stock rose from $47 to its $102.73 high of 2015-12-30. The two-year price landed nearest BULL on every
  date, at 1.1-2.2 times it. The 35 dates already priced above BULL (Ratio B infinite) returned -0.5% to +92%.
- **The class came from the BEAR case, not from the price.** On guided EPS the stock was at 15-24x (59th-96th percentile of its own window),
  but the RICH reading would have held at any P/E: the BEAR case, 2009's -73.5%/yr fall, put the downside at 94-98% on every date, so
  Ratio B was the upside to BULL, and BULL (BASE or a decade CAGR of 1.4-11.7%/yr) could not match a business whose Adjusted EPS went from
  $2.40 (2013) to $6.08 (2016). Hypothesis, not a rule: a single collapse year in the decade window sets BEAR for ten years (2009 stays in
  the window until 2019) and makes every date RICH unless guided growth is high; test a BEAR that no single year can set on other
  cyclical tickers and periods, as the 2010-2013 findings already suggested; never fit it to RCL's outcomes.
- **2015's endpoint flatters it.** By the endpoint-robust measure the 2015 dates did little (m12-24 average price +6.7%, one-year median
  -8.5%, through the fall to $65.48 on 2016-09-19); the two-year endpoints (late 2017) caught the next rise. RICH "held" on 9 by the
  endpoint test.

## 2016 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 3 | +95.0% | +59.5% to +101.5% | 3 | 3 | +78.9% | 3 |
| class FAIR | 35 | +66.0% | +40.8% to +93.6% | 35 | 35 | +61.4% | 6 |
| class RICH | 14 | +38.3% | +15.5% to +69.2% | 11 | 13 | +41.1% | 0 |
| legacy tier WATCHLIST | 29 | +69.8% | +44.9% to +101.5% | 29 | 29 | +65.2% | 6 |
| legacy tier AVOID | 23 | +46.0% | +15.5% to +79.4% | 20 | 22 | +44.4% | 3 |

- **The low of the window was the trade, and the model leaned only to FAIR.** With the price down to $66-80 and the P/E on guided EPS at
  10.9-13.4x (13th-33rd percentile), the class eased to FAIR on 35 dates and CHEAP on 3 (the only dates under the EPP floor, 2016-07-08,
  2016-09-09, 2016-09-16): FAIR returned +41% to +94% (4-50pp ahead of SPY, outside its ±15pp band on 29) and CHEAP +60% to +102%. Within
  the year the entry price, the P/E and the EPP gap rank the m12-24 return at Spearman -0.98 each; the adjusted gap at +0.59.

## 2017 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class RICH (every date) | 52 | +12.9% | -11.9% to +34.5% | 2 | 13 | +2.9% | 39 |
| FY16 EPS $6.05 (to 2017-01-20) | 3 | +30.7% | +22.8% to +34.2% | 1 | 3 | +35.1% | 0 |
| FY17 EPS $7.00 (2017-01-27 to 2017-04-21) | 13 | +25.5% | +21.9% to +34.5% | 1 | 10 | +17.7% | 3 |
| FY17 EPS $7.10 (2017-04-28 to 2017-07-28) | 14 | +15.6% | +0.4% to +25.1% | 0 | 0 | +4.6% | 14 |
| FY17 EPS $7.40 (2017-08-02 to 2017-11-03) | 14 | -5.2% | -11.9% to +1.5% | 0 | 0 | -4.1% | 14 |
| FY17 EPS $7.375 (from 2017-11-08) | 8 | +1.8% | -7.0% to +16.4% | 0 | 0 | -8.9% | 8 |

- **RICH was right in 2017.** The call held on 39 of 52 (every date from 2017-04-28): two-year returns -12% to +35%, 2 cleared the hurdle,
  13 beat SPY; the stock peaked at $134.98 on 2018-01-26 and fell to $84.55 by 2018-12-24. The three-year horizon (2020) caught the
  pandemic: median -40.7%, -64% to +68%. The signals read their best since 2010 (proxy composite 2.90-3.20) at the top, as in 2008 and
  2010.

## 2014-2017 together

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 3 | +95.0% | +59.5% to +101.5% | 3 | 3 | +78.9% | 3 |
| class FAIR | 35 | +66.0% | +40.8% to +93.6% | 35 | 35 | +61.4% | 6 |
| class RICH | 170 | +28.6% | -11.9% to +92.0% | 68 | 111 | +10.4% | 57 |
| P/E on guided EPS under its 10-yr median | 64 | +47.8% | +15.5% to +101.5% | 47 | 61 | +54.5% | 12 |
| P/E on guided EPS at or over its 10-yr median | 144 | +28.0% | -11.9% to +92.0% | 59 | 88 | +8.0% | 54 |

- **Across 2012-2017 the model was RICH on 269 of 309 dates** (from 2012-02-03), while the price went from $30.59 to $119.28. The P/E
  against its own window ranked better than the class did: under the window's median the 64 dates returned a median +47.8% (61 beat SPY),
  at or over it +28.0%. Within each year the entry price ranks the m12-24 return at Spearman -1.00, +0.11, -0.98 and -0.99; across the
  four years -0.75. The proxy composite ranks it the wrong way again (-0.22; -0.63 in 2015).

## The encoding calls, seen afterwards

- The calls listed in retro/README.md ("RCL") move classes only where the class already changes week to week. GAAP EPS instead of the
  company's comparable figures would have moved six dates from CHEAP to FAIR (three of August-September 2008, which returned -12% to +2%
  and beat SPY by 2-11pp, and three of June-July 2009, which returned +142% to +195%); the comparable Q4 2007 guide would have moved two January 2008
  dates to FAIR, which then lost 30-32%. These are hindsight comparisons of alternatives decided before scoring; the calls stay, and
  changing a rule means a new method version tested elsewhere.
- Today's live profile of RCL (`data/business_profiles.json`, a 2026 judgement, recorded in `outcome.json` as profile drift) files it
  CYCLICAL; the retrospective filed it DURABLE on its 10-Ks' wording by the SHW and WMT precedent. The kind changes only the class label, and
  the outcomes above come from the price state, which the EPS anchor set.
- 2010-2013 (retro/README.md, "RCL 2010-2013"), hindsight comparisons of alternatives decided before scoring; the calls stay:
  - FY2012 at GAAP ($0.08) would have moved five 2013 dates from RICH to FAIR; they returned +146% to +162%, 110-124pp ahead of SPY, so
    FAIR would have been less wrong, not right.
  - FY2010 without the $0.39 legal gain (a figure no filing publishes) would have moved seven dates of April-June 2011 toward CHEAP or
    FAIR (they returned -13% to +1%, 32-35pp behind SPY) and eight of March-July 2012 from RICH to FAIR (+93% to +140%).
  - The guides as reported instead of at constant currency would have moved 17 dates of July-October 2010 and April-July 2011 (-13% to
    +4%, 29-42pp behind SPY), in both directions.
  - Forward growth on Net Yields alone, capacity left out, would have moved 42 dates of 2010-2011 toward FAIR or RICH; they returned -22%
    to +46% and beat SPY on one. Capacity in BASE is the encoding that read 2010-2011 as cheaper; with capacity growth near zero in
    2012-2013 it moves nothing there. It was decided from the company's own definition of Net Revenues before scoring, and changing it
    means a new method version tested elsewhere.
  - Operating margins excluding the Q4 2012 impairment and the Q3 2013 restructuring, and the Interest Expense Revision ignored, move no
    class.
- 2014-2017 (retro/README.md, "RCL 2014-2017"), hindsight comparisons of alternatives decided before scoring; the calls stay:
  - GAAP EPS for 2012-2016 instead of the company's Adjusted EPS would have moved 45 dates of 2016 toward CHEAP or FAIR (they returned
    +16% to +94%, all ahead of SPY: closer to right) and all 52 of 2017 from RICH to FAIR or CHEAP (-12% to +35%, 13 ahead of SPY: wrong
    where RICH held). It works through the P/E window (GAAP 2015 and 2012 raise it), not through the anchor, and it cuts both ways.
  - Net Yields and Net Cruise Costs from the statements instead of the company's definition, the FY2013 restatement ignored, and operating
    margins before the impairments move no class.

