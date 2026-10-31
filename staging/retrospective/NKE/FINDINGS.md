# NKE retrospective findings (hindsight)

Patterns seen in `outcome.json` for the NKE weekly dates: 53 from 2008-01-04 to 2008-12-31, 156 from 2009-01-09 to 2011-12-30,
157 from 2012-01-06 to 2014-12-31, 156 from 2015-01-09 to 2017-12-29, 157 from 2018-01-05 to 2020-12-31, 156 from 2021-01-08
to 2023-12-29 and 148 from 2024-01-05 to 2026-10-30. They are **labels and hypotheses**: never feed them back into the method
or the fact sheet. Each batch was scored only after its point-in-time build was committed and pushed (2008: 70934e9;
2009-2011: 056235e; 2012-2014: 6a53de0; 2015-2017: faa87f2; 2018-2020: 8d1b0e8; 2021-2023: 76a6b51; 2024-2026: 97cf27a).
Prices run to 2026-10-30; the 2008 batch's two-year horizons end by 2010-12-30 (three-year: 2011-12-30), the 2009-2011 batch's
by 2013-12-30 (2014-12-30), the 2012-2014 batch's by 2016-12-30 (2017-12-29), the 2015-2017 batch's by 2019-12-27
(2020-12-29), the 2018-2020 batch's by 2022-12-30 (2023-12-29), the 2021-2023 batch's by 2025-12-29 (three-year horizons only
to 2023-10-27, the last date with three years of prices); the 2024-2026 batch has two-year horizons only to 2024-10-25, one-year
to 2025-10-31 and six-month to 2026-04-24. Medians of an even count take the upper middle value (`statistics.median_high`).
The 15%/yr hurdle is +32.2% over two years.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 41 | +22% | +4% to +84% | 13 | 41 | +10% | 41 |
| class FAIR | 12 | +14% | +7% to +16% | 0 | 12 | -8% | 0 |
| legacy tier BUY | 39 | +22% | +4% to +84% | 13 | 39 | +11% | 39 |
| legacy tier ACCUMULATE | 12 | +13% | +7% to +16% | 0 | 12 | -7% | 2 |
| legacy tier WATCHLIST | 2 | +16% | +8% to +16% | 0 | 2 | -7% | 0 |
| January to the Q4 FY08 print (FY07 EPS anchor) | 25 | +12% | +4% to +21% | 0 | 25 | -7% | 13 |
| from the Q4 FY08 print (FY08 EPS anchor) | 28 | +30% | +17% to +84% | 13 | 28 | +16% | 28 |
| CHEAP, January to June | 13 | +12% | +4% to +21% | 0 | 13 | -4% | 13 |
| October-December | 14 | +74% | +30% to +84% | 13 | 14 | +44% | 14 |

- **Every date beat SPY; few cleared the hurdle.** All 53 beat SPY over two years, by 15pp to 39pp, while SPY itself returned
  -19% to +57%. Only 13 cleared the hurdle: the October-December entries ($47-58) other than 2008-10-03 (+30%). Every date lived
  through the 2009-03-09 low ($38.57): drawdowns of 28-45% within two years, and a median one-year return of -12% (CHEAP -7%,
  FAIR -19%).
- **The class ranked the outcomes, through the EPS anchor.** CHEAP did better than FAIR on the two-year return (median +22%
  against +14%), on the m12-24 average price (+10% against -8%) and over three years (+54% against +22%). Most of that gap is the
  28 dates after the Q4 FY08 print, all CHEAP, when FY08's $3.74 replaced FY07's $2.93 as the anchor. On the 25 dates anchored on
  FY07 the 13 CHEAP dates (median +12%, m12-24 -4%) and the 12 FAIR dates (+14%, -8%) were close. There were no RICH dates.
- **The FAIR call failed by beating the benchmark**, as for AAPL in 2008. FAIR expects a return within 15pp of SPY's; all 12 FAIR
  dates beat SPY by 21-29pp, so the call held on none. The CHEAP call held on all 41, but 28 of them only by beating SPY (which
  returned -18% to +8% over those windows), not by clearing the hurdle.
- **The floor distance ranked the outcomes; the signal composite ranked them backwards.** Across the 53 dates the EPP gap ranks the
  two-year returns at Spearman -0.90 (-0.95 on the m12-24 average), Ratio B at -0.89, the adjusted gap at +0.82 and the entry price
  alone at -0.77. The proxy composite, built from the latest quarter's signals, ranks them at -0.65. It read 3.05 from January to
  mid-March (11 dates, median two-year return +10%), 3.00 from the Q3 FY08 print to June (14, +13%), 2.70 from the Q4 FY08 print to
  mid-December (25, +29%) and 2.00 after the Q2 FY09 print (3, +77%). The trailing signals were highest near the top of the cycle
  and lowest near its bottom.
  Hypothesis for the method: last-quarter operating signals lag the price, so as composite inputs they lean pro-cyclical. A later
  version could test them against their own trend, or give valuation more weight. Test it on other tickers and years before any
  method change; never fit it to NKE's outcomes. AAPL's 2008 batch found the entry price ranking its returns too (Spearman -0.91):
  one stock through one crash mostly tests "buy lower".
- **BASE was the nearest anchor; BULL and BEAR were not reached at two years.** The two-year price ($61-90) landed nearest the BASE
  price on 51 dates and the BEAR price on 2; it was 0.82-1.20 times BASE, 0.61-0.87 times BULL and 1.19-1.73 times BEAR. On the path
  every date saw a close ($38.57) below its BEAR price ($45-57): flat EPS at the 10th-percentile multiple was a floor for the
  two-year point, not for the drawdown.
- **The FY07 call, seen afterwards.** FY07 at the company's $3.10 instead of GAAP $2.93 would have turned 11 of the 12 FAIR dates
  CHEAP (retro/README.md, "NKE"). Those dates beat SPY by 21-29pp, so the CHEAP call would have held on them too, while their
  m12-24 average was -3% to -12%. That is a fact about one stock in one year, not a reason to change the encoding: the call was
  decided before scoring and stays, and changing a rule means a new method version tested elsewhere.
- **Revenue growth excluding currency moved nothing** (retro/README.md, "NKE"): BASE on reported growth gives the same 53 classes
  and tiers, so the choice of basis did not shape these outcomes.

## 2009-2011 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 73 | +55% | +31% to +130% | 72 | 66 | +42% | 73 |
| class FAIR | 22 | +50% | +15% to +74% | 16 | 16 | +26% | 7 |
| class RICH | 61 | +52% | +12% to +79% | 43 | 53 | +26% | 8 |
| legacy tier BUY | 76 | +56% | +31% to +130% | 75 | 69 | +42% | 65 |
| legacy tier ACCUMULATE | 22 | +51% | +30% to +74% | 21 | 21 | +31% | 10 |
| legacy tier WATCHLIST | 29 | +51% | +15% to +79% | 23 | 23 | +26% | 6 |
| legacy tier AVOID | 29 | +30% | +12% to +67% | 12 | 22 | +20% | 7 |
| January to the Q4 FY09 print (FY08 $3.74 anchor), all CHEAP | 24 | +73% | +42% to +130% | 24 | 18 | +57% | 24 |
| FY09 $3.81 anchor (2009-06-26 to 2010-06-18) | 52 | +54% | +39% to +86% | 52 | 52 | +34% | 33 |
| - of which CHEAP / FAIR / RICH | 32 / 15 / 5 | +57% / +50% / +60% | | 32 / 15 / 5 | 32 / 15 / 5 | +42% / +29% / +32% | 32 / 1 / 0 |
| FY10 $3.86 anchor (2010-06-25 to 2011-06-24) | 53 | +33% | +12% to +62% | 28 | 38 | +25% | 26 |
| - of which CHEAP / FAIR / RICH | 12 / 6 / 35 | +38% / +22% / +31% | | 11 / 0 / 17 | 11 / 0 / 27 | +40% / +25% / +22% | 12 / 6 / 8 |
| FY11 $4.39 anchor (2011-06-29 to 2011-12-30) | 27 | +63% | +40% to +79% | 27 | 27 | +30% | 5 |
| - of which CHEAP / FAIR / RICH | 5 / 1 / 21 | +62% / +74% / +64% | | 5 / 1 / 21 | 5 / 1 / 21 | +34% / +35% / +28% | 5 / 0 / 0 |

- **A rising tide.** The two-year total return ran from +12% to +130% (median +53%) while SPY returned +10% to +99%; 131 of 156
  dates cleared the hurdle and 135 beat SPY. Within two years every date saw a drawdown of 14-23%. The median one-year return was
  +36% for the 2009 dates, +17% for 2010 and +19% for 2011; over three years every date beat SPY.
- **The class ranked the m12-24 average more than the two-year endpoint.** On the endpoint CHEAP (median +55%), FAIR (+50%) and
  RICH (+52%) were close; on the m12-24 average CHEAP led (+42% against +26% and +26%), and at one year too (+33% against +15% and
  +18%). Within the FY10 anchor CHEAP led on both (+38% and +40%, against +31% and +22% for RICH and +22% and +25% for FAIR);
  within the FY09 and FY11 anchors RICH beat CHEAP on the endpoint (+60% against +57%, +64% against +62%).
- **The CHEAP call held on all 73;** 72 cleared the hurdle (2010-07-23, +31%, did not) and 7 lagged SPY (April-June 2009 and
  2010-07-02), when SPY returned +39% to +63%.
- **The RICH call held only in late 2010:** on 8 of 61 dates, 2010-10-08 and 2010-11-05 to 2010-12-17 ($82-90), with two-year
  returns of +12% to +19%, 3.5-10.5pp behind SPY. The 46 RICH dates of 2011 all beat SPY (by 4-37pp) and 38 cleared the hurdle.
  The FAIR call held on 7 of 22 (2010-06-18 and 2010-09-17 to 2010-10-29, within -9pp to +14pp of SPY); the other 15 beat SPY by
  more than 15pp, as in 2008.
- **BULL, not BASE, was the nearest anchor.** The two-year price landed nearest the BULL price on 92 dates, XBULL on 36 (all in
  2011) and BASE on 28 (all in 2009). It was 1.08-1.77 times the BASE price on every date; on every 2011 date it was 1.08-1.44
  times BULL (0.80-1.09 times XBULL). The path went below the BEAR price on all 24 dates of January to June 2009 (lows of
  $38.57 on 2009-03-09 to $50.84 on 2009-06-26) and on 34 of the 52 dates of 2009, on none after.
- **The floor distance ranked the m12-24 average; the endpoint less.** The EPP gap ranks the two-year returns at Spearman -0.49
  (-0.80 within 2009 and within 2010, -0.31 within 2011) and the m12-24 averages at -0.90; Ratio B at -0.50 and -0.90, the
  conservative return at +0.54 and +0.84, the entry price alone at -0.35 and -0.83. As in 2008, much of this is "buy lower".
- **The proxy composite ranked the outcomes backwards again,** at -0.53 on the two-year return and -0.58 on the m12-24 average,
  but not step by step: the lowest medians followed 2.85 (after the Q1 FY11 print, +16%) and 2.70 (after Q2 FY11 and Q2 FY12,
  +30%); the 3.20 and 3.35 of March-September 2010 were followed by +51% and +35%, and the 1.85-2.15 of 2009 and early 2010 by
  +52% to +61%. Within each year it ranks them weakly (+0.12, -0.20, -0.27). This is a second, weaker reading on the same stock
  of the 2008 hypothesis (trailing signals lean pro-cyclical); it still needs other tickers before any method change.
- **The FY09 call, seen afterwards.** FY09 at GAAP $3.03 instead of the company's $3.81 would have turned 47 CHEAP or FAIR dates
  RICH, 10 CHEAP dates FAIR and 1 RICH date FAIR (retro/README.md, "NKE 2009-2011"). The stock beat SPY on 53 of those 58 dates,
  so the call held on 43 of them as built and would have held on 14: 59 of 156 overall against 88. BASE on reported revenue
  growth would have held on 94 (+6), FY08 at GAAP on 87 (-1). These are facts about one stock in three years, not reasons to
  change an encoding: the calls were decided before scoring and stay, and a rule change means a new method version tested
  elsewhere.

## 2012-2014 (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 5 | +103% | +76% to +110% | 5 | 5 | +70% | 5 |
| class FAIR | 2 | +100% | +88% to +100% | 2 | 2 | +65% | 0 |
| class RICH | 150 | +64% | +5% to +107% | 135 | 132 | +46% | 8 |
| legacy tier BUY | 2 | +103% | +81% to +103% | 2 | 2 | +70% | 2 |
| legacy tier ACCUMULATE | 12 | +88% | +66% to +110% | 12 | 12 | +61% | 3 |
| legacy tier WATCHLIST | 11 | +73% | +64% to +107% | 11 | 11 | +57% | 0 |
| legacy tier AVOID | 132 | +60% | +5% to +94% | 117 | 114 | +45% | 8 |
| FY11 $4.39 anchor (2012-01-06 to 2012-06-22), all RICH | 25 | +44% | +34% to +61% | 25 | 15 | +29% | 0 |
| FY12 anchor, Q4 FY12 print to the split 8-K (2012-06-29 to 2012-11-16) | 21 | +73% | +64% to +110% | 21 | 21 | +58% | 5 |
| - of which CHEAP / FAIR / RICH | 5 / 2 / 14 | +103% / +100% / +69% | | 5 / 2 / 14 | 5 / 2 / 14 | +70% / +65% / +57% | 5 / 0 / 0 |
| FY12 anchor after the split 8-K (2012-11-23 to 2013-06-21), all RICH | 31 | +75% | +59% to +107% | 31 | 31 | +52% | 0 |
| FY13 $2.69 anchor (2013-06-28 to 2014-06-20), all RICH | 52 | +69% | +46% to +84% | 52 | 52 | +49% | 0 |
| FY14 $2.97 anchor (2014-06-27 to 2014-09-26), all RICH | 14 | +48% | +24% to +52% | 13 | 14 | +54% | 0 |
| FY15E $3.56 from the EPS guide (2014-10-03 to 2014-12-31), all RICH | 14 | +10% | +5% to +22% | 0 | 6 | +21% | 8 |

- **The stock kept compounding through a RICH call.** The model called NKE RICH on 150 of 157 dates, at 19.7-30.1x a
  last-full-year anchor (the 87th-100th percentile of its own ten-year range). The two-year total return then ran from +5% to
  +110% (median +65%) while SPY returned +6% to +56%; 142 dates cleared the hurdle and 139 beat SPY, and over three years 144
  beat SPY (median +81%). Within two years every date saw a drawdown of 11-26%.
- **The RICH call held on 8 of 150 dates,** the last ones, 2014-11-14 to 2014-12-31 ($94.84-99.33), where the two-year
  return was +5% to +10%, 2.6-7.1pp behind SPY. On the other 142 the stock beat the hurdle or SPY. Even the 69 dates priced
  above the BULL price returned a median +63% (65 cleared the hurdle). The two-year price was 0.99-2.0 times the BULL price
  and 1.1-2.4 times BASE; it landed nearest XBULL on 145 dates and BULL on 12.
- **Where the class varied, it ranked the outcomes.** In 2012, the only year with CHEAP and FAIR dates (all between the Q4
  FY12 print and the split 8-K), CHEAP (median +103%) and FAIR (+100%) beat RICH (+55%), and the EPP gap ranks 2012's two-year
  returns at Spearman -0.92 (-0.95 on the m12-24 average); at one year the batch's CHEAP, FAIR and RICH medians were +68%,
  +63% and +28%. The FAIR call failed on both FAIR dates by beating SPY by 50-53pp. Across the batch the EPP gap ranks the
  two-year returns at -0.51 (-0.67 within 2013, +0.25 within 2014), the entry price alone at -0.49.
- **The EPS-guide dates fared worst** (2014-10-03 to 2014-12-31: median +10%, none cleared the hurdle, 6 of 14 beat SPY), but
  they were also the batch's highest prices ($87.18-99.33), and within 2014 the entry price ranks the two-year returns at
  -0.87. The guide moved the anchor, not the class (retro/README.md, "NKE 2012-2014"): one quarter of one stock says nothing
  about reading growth guides as EPS.
- **The proxy composite ranked the outcomes backwards again within 2012** (Spearman -0.87: 2.70 on the 25 dates to June
  2012, median +44%; 2.35 from the Q4 FY12 print, +81% over its 38 dates to March 2013), and weakly across the batch (-0.34 on
  the two-year return, -0.56 on the m12-24 average). A third reading on the same stock of the 2008 hypothesis (trailing
  signals lean pro-cyclical); it still needs other tickers before any method change.
- **The calls, seen afterwards.** BASE on reported revenue growth would have turned the 4 CHEAP and 2 FAIR dates of July to
  November 2012 RICH; they returned +76% to +110%, so the call held on 4 of them as built and would have held on none. FY08 at
  GAAP would have turned the 2 FAIR dates RICH (+88%, +100%), failing either way. These are facts about one stock in three
  years, not reasons to change an encoding: the calls were decided before scoring and stay.
- **What the three batches suggest together (hypotheses only).** On NKE the class worked where it marked cheap entries (CHEAP
  held on 41 of 41 in 2008, 73 of 73 in 2009-2011 and 5 of 5 here) and failed where it marked RICH on a business that kept
  growing (RICH held on 8 of 61 in 2009-2011 and 8 of 150 here). The anchor is the last full year's EPS, which trails a growing
  company by up to a year (retro/README.md, "NKE 2012-2014": each spring nine-month EPS was already over four-fifths of the
  anchor), and the method has no trend term for a multiple that rerates. Both are hypotheses to test on other tickers and
  years, under a new method version, never fitted to NKE's outcomes.

## 2015-2017 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR | 1 | +73% | +73% | 1 | 1 | +56% | 0 |
| class RICH | 155 | +38% | -19% to +87% | 82 | 89 | +15% | 66 |
| legacy tier BUY | 9 | +73% | +52% to +87% | 9 | 9 | +55% | 0 |
| legacy tier ACCUMULATE | 8 | +63% | +49% to +66% | 8 | 8 | +48% | 0 |
| legacy tier WATCHLIST | 35 | +53% | +38% to +66% | 35 | 35 | +40% | 0 |
| legacy tier AVOID | 104 | +15% | -19% to +65% | 31 | 38 | +6% | 66 |
| FY15E $3.56 from the EPS guide (2015-01-09 to 2015-06-19), all RICH | 24 | +14% | +0% to +25% | 0 | 7 | +10% | 17 |
| FY15 $3.70 anchor (2015-06-26 to 2015-12-18), all RICH | 26 | -2% | -19% to +10% | 0 | 0 | -6% | 26 |
| FY15 anchor after the split, $1.85 (2015-12-24 to 2016-06-24), all RICH | 27 | +15% | +2% to +44% | 4 | 4 | -1% | 23 |
| FY16 $2.16 anchor (2016-06-30 to 2017-06-23), all RICH | 52 | +52% | +36% to +66% | 52 | 52 | +38% | 0 |
| FY17 $2.51 anchor (2017-06-30 to 2017-12-29) | 27 | +61% | +38% to +87% | 27 | 27 | +42% | 0 |
| - of which FAIR / RICH | 1 / 26 | +73% / +61% | | 1 / 26 | 1 / 26 | +56% / +42% | 0 / 0 |

- **A RICH call that held, then failed.** The model called NKE RICH on 155 of 156 dates and CHEAP on none. The two-year total
  return ran from -19% to +87% (median +39%) while SPY returned +11% to +53%; 83 dates cleared the hurdle and 90 beat SPY. The
  RICH call held on 66: every date from 2015-01-09 to 2016-05-27 except 2015-02-06 to 2015-03-20, where the stock returned +18%
  to +25%, 0.9-9.4pp ahead of SPY but short of the hurdle. It failed on all 82 RICH dates from 2016-06-03, every one of which
  cleared the hurdle and beat SPY. Within two years every date saw a drawdown of 16-26%. The median one-year return was +6% for
  the 2015 dates, -2% for 2016 and +30% for 2017; over three years 116 of 156 beat SPY (median +54%).
- **Within RICH, the multiple's own percentile ranked the outcomes.** At the 95th-100th percentile of its ten-year range (69
  dates, 2015-01-09 to 2016-04-29) the median two-year return was +8.5% (-19% to +25%) and the call held on 62; at the 85th-94th
  (23 dates) +42%, held on 4; at the 67th-84th (54) +55%, and below the 67th (9, August to October 2017) +66%, held on none.
  Ratio B ranks the two-year returns at Spearman -0.89 (-0.94 on the m12-24 average), the EPP gap at -0.91 (-0.95), the multiple
  on the anchor at -0.86 (-0.96), the conservative return at +0.74 (+0.88) and the entry price alone at -0.81 (-0.79). The tiers
  sorted cleanly: AVOID median +15%, WATCHLIST +53%, ACCUMULATE +63%, BUY +73%.
- **Above the BULL case meant something this time.** The 61 dates priced above the BULL price (Ratio B infinite, 2015-03-20 to
  2016-05-13) returned a median +6.7%; none cleared the hurdle and one beat SPY. In 2012-2014 the 69 such dates returned a median
  +63%.
- **The FY15 anchor dates fared worst:** on FY15's $3.70, at 28.9-36.3x (2015-06-26 to 2015-12-18), the stock returned -19% to
  +10% and none beat SPY; on the FY15E guide, at 25.8-29.9x, +0% to +25%.
- **The FAIR date failed by beating the benchmark,** as in 2008: 2017-09-08 returned +73%, 48pp ahead of SPY. The nine BUY
  dates (2017-08-25 to 2017-10-20) returned +52% to +87%, 31-67pp ahead.
- **XBULL, not BASE, was the nearest anchor.** The two-year price landed nearest the XBULL price on 109 dates and BULL on 47; it
  was 1.13-1.84 times the BASE price and 0.96-1.35 times BULL. No path went below its BEAR price (the two-year price was 1.9-2.8
  times BEAR).
- **The proxy composite ranked the outcomes backwards again,** at -0.67 on the two-year return and -0.69 on the m12-24 average:
  its 2.70 on 23 dates of 2015 preceded a median +0.3%, 2.50-2.55 +12% to +15%, and 2.15 on the Q4 FY15 dates +4%, while 2.00-2.35
  from 2016-06-30 preceded +44% to +61%. A fourth reading on the same stock of the 2008 hypothesis (trailing signals lean
  pro-cyclical); it still needs other tickers before any method change.
- **The calls, seen afterwards.** BASE on reported revenue growth, or FY17 at a derived $2.40 without the one-time tax benefit,
  would have turned the one FAIR date RICH; it returned +73%, so the call fails either way. The derived FY17 would also have moved
  6 of the 9 BUY dates to ACCUMULATE and 6 other dates a tier lower, and FY08 at GAAP 20 dates a tier lower, 8 of them BUY dates
  that returned +52% to +84%. The futures encodings and the ECOMMERCE watch moved nothing; the 24 watch-list dates from
  2017-07-21 returned +38% to +87%, which says nothing about the theme, since the watch list changes text only. These are facts
  about one stock in three years, not reasons to change an encoding: the calls were decided before scoring and stay.
- **What the four batches suggest together (hypotheses only).** The CHEAP call held on every CHEAP date of 2008-2014 (41, 73
  and 5); there was none here. The RICH call held on 8 of 61 (2009-2011), 8 of 150 (2012-2014) and 66 of 155 here, and here
  almost only at the 95th-100th percentile of the stock's own range (62 of 69), where the multiple then fell back, and on none of
  the 63 RICH dates below the 85th. Within this batch the multiple's percentile and Ratio B ranked the outcomes better than the
  class did. Hypotheses to test on other tickers and years, under a new method version and never fitted to NKE's outcomes: that a
  RICH label carries information only near the top of the stock's own range, and, as in every NKE batch so far, that the
  trailing operating signals in the proxy composite lean pro-cyclical.

## 2018-2020 (157 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class FAIR | 1 | +98% | +98% | 1 | 0 | +124% | 1 |
| class RICH | 156 | +51% | -32% to +117% | 107 | 115 | +38% | 34 |
| legacy tier ACCUMULATE | 1 | +98% | +98% | 1 | 0 | +124% | 1 |
| legacy tier AVOID | 156 | +51% | -32% to +117% | 107 | 115 | +38% | 34 |
| FY17 $2.51 for FY18E, the rollover rule (2018-01-05 to 2018-06-22), all RICH | 25 | +36% | -0.1% to +62% | 15 | 25 | +32% | 0 |
| FY17 $2.51 for FY19E, FY18 excluded (2018-06-29 to 2019-06-21), all RICH | 52 | +63% | +23% to +102% | 47 | 52 | +34% | 0 |
| FY19 $2.49 anchor (2019-06-28 to 2020-06-19), 51 RICH and 1 FAIR | 52 | +65% | +14% to +117% | 46 | 38 | +58% | 7 |
| FY20 $1.60 anchor (2020-06-26 to 2020-12-31), all RICH | 28 | -16% | -32% to +23% | 0 | 0 | +7% | 28 |

- **A RICH call that failed until the COVID-19 rally, then held.** The model called NKE RICH on 156 of 157 dates and CHEAP on
  none. The two-year total return ran from -32% to +117% (median +51%) while SPY returned -9% to +99%; 107 RICH dates cleared the
  hurdle and 115 beat SPY. The RICH call ("should miss the hurdle and lag the benchmark") failed on all 122 RICH dates from
  2018-01-05 to 2020-05-15, except 2020-05-08: the seven that lagged SPY (2020-03-26 to 2020-05-15) still returned +32% to +72%.
  It held on 34, 2020-05-08 and every date from 2020-05-22 on, which returned -32% to +29%, 8-43pp behind SPY. Within two years
  every date saw a drawdown of 21-53% (the 2018 and 2019 dates through the March 2020 low, the 2020 dates from the November 2021
  high into 2022). The median one-year return was +21% for 2018, +25% for 2019 and +43% for 2020; over three years 68 of 157
  beat SPY (median +44%): all 52 of 2018, 9 of 2019 and 7 of 2020.
- **The multiple's percentile no longer ranked the outcomes.** At the 95th-100th percentile of its own range (118 RICH dates) the
  median two-year return was +48.5% (-32% to +101%) and the call held on 34, all from May 2020; at the 85th-94th (35) +58%, held on
  none; at the 67th-84th (3) +62%. Across all dates Ratio B ranks the two-year returns at Spearman -0.26 (+0.04 on the m12-24
  average), the EPP gap at -0.36, the multiple on the anchor at -0.38, the entry price at -0.38 and the conservative return at
  +0.66 (+0.30); in 2015-2017 the first four were -0.81 to -0.91. Within 2020 alone the multiple ranks them at -0.90 and Ratio B
  at -0.55: the rally lifted the price far faster than the anchor.
- **Above the BULL case did not mean a poor outcome:** the 85 dates with Ratio B infinite (from 2018-06-29) returned a median
  +44.7%; 50 cleared the hurdle and 48 beat SPY. The 72 others returned a median +61%. (2015-2017: +6.7%; 2012-2014: +63%.)
- **The FY18 exclusion, afterwards.** The 52 dates anchored on FY17's $2.51 for FY19E traded at 25.5-35.5x and returned +23% to
  +102% (median +63%), every one ahead of SPY; FY19's reported EPS was $2.49. At GAAP $1.17 the same dates would have been RICH at
  61-76x, so the call failed either way; the exclusion moved the numbers, not the class. It was decided by the r2 rule before
  scoring and is not evaluated by this outcome.
- **COVID-19.** The FAIR date, 2020-03-20 ($67.45, the low week), returned +98% against SPY's +99%, within the FAIR band, so the
  call held. From the Q4 FY20 print the anchor fell to FY20's $1.60 (58.5-89.0x) while the price rose to $94-142: those 28 dates
  returned -32% to +23%, none cleared the hurdle or beat SPY, and the RICH call held on all of them.
- **XBULL, not BASE, was the nearest anchor again:** the two-year price landed nearest XBULL on 146 dates, BULL on 9 and BASE on 2;
  it was 0.82-2.28 times the BULL price and 1.6-9.8 times BEAR. No path went below its BEAR price.
- **The proxy composite ranked the outcomes forward this time,** at +0.51 on the two-year return but -0.03 on the m12-24 average,
  and only across years (within 2018 +0.10, 2019 -0.25, 2020 +0.15): its lowest readings, 1.35 on the Q4 FY20 dates and 2.15 on
  Q1 FY21, preceded medians of +11% and -20%, because the COVID-19 quarters coincided with high prices on a depressed anchor; 2.60-2.65
  preceded +68% to +74%. The pro-cyclical-lean hypothesis of the earlier batches is not confirmed here, and not refuted.
- **The calls, seen afterwards.** FY18 at GAAP would have moved 2020-03-20 from ACCUMULATE to WATCHLIST, and BASE on reported
  revenue growth would have made it RICH; it returned +98%, level with SPY but over the hurdle, so a RICH call there would have
  failed. The other variants (the exclusion from the FY2018 10-K, FY20 excluded as well, no ECOMMERCE watch, the futures slot
  re-weighted) moved nothing. These are facts about one stock in three years, not reasons to change an encoding: the calls were
  decided before scoring and stay.
- **What the five batches suggest together (hypotheses only).** The RICH call held on 8 of 61 (2009-2011), 8 of 150 (2012-2014),
  66 of 155 (2015-2017) and 34 of 156 here. The 2015-2017 hypothesis that a RICH label carries information only near the top of
  the stock's own range weakens: at the 95th-100th percentile the call held on 62 of 69 there and on 34 of 118 here, and the 34
  came only after the anchor dropped to a depressed year. The anchor's lag is the recurring thread (in 2018-2019 the price ran
  ahead of an anchor that later proved close, in late 2020 the anchor sat below the earnings already in hand). Hypotheses to
  test on other tickers and years, under a new method version and never fitted to NKE's outcomes.

## 2021-2023 (156 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 15 | -32% | -41% to +10% | 0 | 0 | -25% | 0 |
| class FAIR | 65 | -30% | -54% to -8% | 0 | 0 | -29% | 0 |
| class RICH | 76 | -27% | -44% to -2% | 0 | 0 | -22% | 76 |
| legacy tier BUY | 17 | -34% | -40% to +10% | 0 | 0 | -30% | 0 |
| legacy tier ACCUMULATE | 24 | -38% | -43% to -8% | 0 | 0 | -30% | 0 |
| legacy tier WATCHLIST | 41 | -26% | -54% to -9% | 0 | 0 | -16% | 2 |
| legacy tier AVOID | 74 | -26% | -44% to -2% | 0 | 0 | -22% | 74 |
| FY20 $1.60 anchor (2021-01-08 to 2021-06-18), all RICH | 24 | -10% | -20% to -2% | 0 | 0 | -17% | 24 |
| FY21 $3.56 anchor (2021-06-25 to 2022-06-24), 33 RICH and 20 FAIR | 53 | -29% | -40% to -9% | 0 | 0 | -27% | 33 |
| FY22 $3.75 anchor (2022-06-29 to 2023-06-23), 35 FAIR, 15 CHEAP, 2 RICH | 52 | -33% | -54% to +10% | 0 | 0 | -24% | 2 |
| FY23 $3.23 anchor (2023-06-30 to 2023-12-29), 17 RICH and 10 FAIR | 27 | -29% | -44% to -17% | 0 | 0 | -33% | 17 |

- **Every date lost against SPY.** The two-year total return ran from -54% to +10% (median -28.5%) while SPY returned -8% to
  +70%: no date cleared the hurdle and none beat SPY, by 4pp to 99pp. Every date saw a drawdown of 31-58% within two years; the
  median one-year return was -29% for the 2021 dates, -3% for 2022 and -19% for 2023, and over three years none of the 147 dates
  with three years of prices beat SPY (median -46%). The best entry was 2022-09-30 ($83.12, CHEAP, +10%), the worst 2023-04-14
  ($125.95, FAIR, -54%).
- **So the RICH call held on all 76 RICH dates, and the FAIR and CHEAP calls on none.** FAIR "should land within +/-15pp of the
  benchmark"; its 65 dates lagged by 32pp to 97pp. CHEAP "should clear the hurdle or beat the benchmark"; its 15 dates (September
  2022 to June 2023) returned -41% to +10% and lagged by 55pp to 91pp. The tiers ranked backwards: BUY median -34%, ACCUMULATE
  -38%, WATCHLIST -26%, AVOID -26%.
- **Within the batch the multiple ranked the outcomes in a U.** The 22 dates at the 95th-100th percentile of the stock's own range
  (all RICH, the FY20 $1.60 anchor at 80-91x, early 2021) returned a median -9.4%; the 129 between the 34th and 94th percentile
  -29% to -34%; the 5 at or below the 33rd (CHEAP, September-October 2022) -4.0%. Across all dates the rankings are weak (Ratio B
  +0.32, the EPP gap +0.10, the multiple on the anchor +0.10, the conservative return -0.42); within each year the entry price
  ranks best (-0.82, -0.50 and -0.69 on the two-year return; -0.99, -0.88 and -0.55 on the m12-24 average): the lowest prices
  did least badly.
- **The anchors and the window, afterwards.** The 24 dates on FY20's $1.60 (a COVID year) were the least bad (-2% to -20%); the
  window's high percentiles (38-66x on FY20's own days) made 40-50x on FY21's $3.56 read as FAIR and BUY in mid-2021, and those
  13 BUY dates returned -27% to -40%. The FY20-excluded test (32 classes, 55 tiers) would have changed the label on many of the
  2022-2023 dates; it was a test, not the encoding, and outcomes do not decide it.
- **BEAR and BASE were the nearest anchors:** the two-year price landed nearest BEAR on 68 dates, BASE on 64 and XBULL on 24 (0.22-2.22
  times the BULL price). No path went below its BEAR price (BEAR at -35.7%/yr put it far below: the two-year price was 1.7-10.7
  times BEAR).
- **The proxy composite did not rank the outcomes** (-0.01 on the two-year return, -0.30 on the m12-24 average); its highest
  reading, 3.30 on the Q4 FY21 dates (the COVID comparison), preceded a median -35.6%, and its lowest, 1.85 on Q4 FY22 and Q1 FY23
  (inventories +23% and +44%), -24.3%. Within 2021 it ranked them backwards (-0.70), as in 2008-2017: the pro-cyclical lean shows
  again.
- **The calls, seen afterwards.** None of the encodings moved the outcome's direction: every class lost against SPY. FY18 at
  GAAP, BASE on reported growth and the futures re-weighting would have shifted 13, 13 and 3 classes among RICH, FAIR and CHEAP,
  none of which held except RICH. These are facts about one stock in three years, not reasons to change an encoding: the calls
  were decided before scoring and stay.
- **What the six batches suggest together (hypotheses only).** The CHEAP call held on every CHEAP date of 2008-2014 (119) and on
  none of the 15 here; the RICH call held on 8 of 61 (2009-2011), 8 of 150 (2012-2014), 66 of 155 (2015-2017), 34 of 156
  (2018-2020) and 76 of 76 here. In the falling market for this stock every label lost to SPY, and the lowest entry prices did
  least badly. A class built on the stock's own multiple and a trailing anchor does not see a de-rating driven by the next years'
  earnings; whether a forward measure (consensus or guidance, which NIKE stopped filing) would, is a question for other tickers
  and a new method version, never fitted to NKE's outcomes.

## 2024-2026 (148 dates)

Prices end on 2026-10-30, so only the 43 dates to 2024-10-25 have two years, the 96 to 2025-10-31 one year and the 121 to
2026-04-24 six months; 2026-10-30 has no outcome. No RICH date has two years of prices yet.

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 18 | -48% | -56% to -35% | 0 | 0 | -32% | 0 |
| class FAIR | 25 | -43% | -52% to -34% | 0 | 0 | -33% | 0 |
| legacy tier BUY | 18 | -48% | -56% to -35% | 0 | 0 | -32% | 0 |
| legacy tier ACCUMULATE | 1 | -47% | -47% to -47% | 0 | 0 | -27% | 0 |
| legacy tier WATCHLIST | 19 | -48% | -52% to -34% | 0 | 0 | -33% | 0 |
| legacy tier AVOID | 5 | -36% | -37% to -34% | 0 | 0 | -35% | 0 |
| FY23 $3.23 anchor (2024-01-05 to 2024-06-21), all FAIR | 25 | -43% | -52% to -34% | 0 | 0 | -33% | 0 |
| FY24 $3.95 anchor (2024-06-28 to 2024-10-25), all CHEAP | 18 | -48% | -56% to -35% | 0 | 0 | -32% | 0 |

| Group (one year) | Dates | Median 1-yr total return | Range | Cleared 15% hurdle | Beat SPY | Median price change to 2026-10-30 |
|---|---|---|---|---|---|---|
| class CHEAP | 52 | -15% | -31% to +7% | 0 | 0 | -48% |
| class FAIR | 25 | -31% | -39% to -19% | 0 | 0 | -60% |
| class RICH | 19 | -44% | -52% to -37% | 0 | 0 | -47% |
| FY23 $3.23 anchor (2024-01-05 to 2024-06-21), all FAIR | 25 | -31% | -39% to -19% | 0 | 0 | -60% |
| FY24 $3.95 anchor (2024-06-28 to 2025-06-20), all CHEAP | 52 | -15% | -31% to +7% | 0 | 0 | -48% |
| FY25 $2.16 anchor, RICH dates with a year (2025-06-27 to 2025-10-31) | 19 | -44% | -52% to -37% | 0 | 0 | -47% |

- **Every scored horizon lost against SPY.** Over two years the 43 dates returned -56% to -34% (median -47%) while SPY returned
  +24% to +50%: none cleared the hurdle and none beat SPY, by 66pp to 94pp. Over one year the 96 dates returned -52% to +7%
  (median -22%) and none beat SPY; over six months one of 121 did (2025-02-07, CHEAP, +9.4%, by 3.6pp). The lowest close of the
  period was $33.87 on 2026-10-02, and drawdowns within the windows reached 60%.
- **So the CHEAP and FAIR calls failed on every scored date.** CHEAP "should clear the hurdle or beat the benchmark"; its 18
  two-year dates (the Q4 FY24 print to 2024-10-25, BUY throughout) returned -56% to -35%. FAIR "should land within +/-15pp of
  the benchmark"; its 25 (the FY23 anchor) lagged by 66pp to 94pp. The tiers did not separate them: BUY median -48%,
  WATCHLIST -48%, AVOID -36%.
- **On one year and six months the classes ranked in order:** CHEAP (52, all on FY24's $3.95) median -15%, FAIR (25) -31%, RICH
  (19, from the Q4 FY25 print) -44%; over six months -1.8%, -17.9% and -29.0%. Within the 96 one-year dates the method's own
  measures ranked the outcomes the right way round, unlike 2021-2023: the adjusted gap +0.87, Ratio B -0.73, the multiple on
  the anchor -0.71, the EPP gap -0.69 and the conservative return +0.67. On the 43 two-year dates the signs flip (+0.29 to
  +0.30): the June-October 2024 CHEAP entries ($73-89) ended two years later at 2026's lows ($34-44), the January-June FAIR
  ones ($89-106) at $42-66.
- **The trailing anchor overstated the next years' earnings, beyond BEAR.** The 52 CHEAP dates sat on FY24's $3.95 (the
  company's figure; GAAP $3.73) at 13.8-22.6x. NIKE then reported $2.16 for FY25 and $2.10 for FY26 and guided $1.15-1.35 for
  FY27, below the BEAR case's own path from $3.95 at -35.7%/yr ($2.54 a year out, $1.63 two). The two-year price landed nearest
  BEAR on all 43 dates (0.94-2.26 times BEAR, 0.19-0.45 times BULL), and the path went below the BEAR price ($34-36) on the 35
  dates from 2024-09-20 to 2025-05-16, the first NKE dates since 2009 to do so; the two-year endpoints of 2024-09-20 to
  2024-10-11 ($33.87-35.75) ended below it. What kept the price above BEAR was the multiple: 27-31x on the FY27 range in
  October 2026.
- **The RICH dates of 2025-2026 were RICH by the scenarios, not the multiple.** The 35 on FY25's $2.16 (2025-06-27 to
  2026-02-27) sat at 28-36x, the 29th-67th percentile, with BEAR at -45.3%/yr and BULL near 0%. The 19 with a year of prices
  returned -52% to -37% (lagging SPY by 50pp to 69pp), and all 35 stood 36.5-50.7% lower on 2026-10-30. Their two-year call is not
  scored yet.
- **The latest dates are too recent to read:** the 13 CHEAP dates on FY26's $2.10 (2026-07-02 to 2026-09-25) stood -13% to +9%
  on 2026-10-30 and the five RICH dates on the FY27 range 0% to +14%, weeks rather than horizons. Neither the FY27-range call
  (5 classes) nor the IEEPA test (10 classes, July-September 2026) can be judged.
- **The proxy composite ranked the one-year outcomes positively** (+0.44; +0.61 on the 43 two-year dates): its lowest reading,
  1.50 on Q4 FY25 (the RICH summer of 2025), preceded the worst one-year median (-43%), and 2.80 on Q2 and Q4 FY24 -16%. In this
  batch it moved with the class; in 2021 it had ranked them backwards.
- **The calls, seen afterwards.** FY24 at the company's $3.95 rather than GAAP would have moved no class; FY18 at GAAP 8 (FAIR
  to CHEAP on 2024-04-05, RICH to FAIR on six dates from 2025-11-07 to 2026-02-27 and on 2026-10-02) and FY20 excluded 4. None
  changes the direction of the scored outcomes: every scored date lost against SPY. These are facts about one stock, not
  reasons to change an encoding: the calls were decided before scoring and stay.
- **What the seven batches suggest together (hypotheses only).** The CHEAP call held on every CHEAP date of 2008-2014 (119) and
  on none of 2021-2023 (15) or of the 18 two-year dates here; the RICH call, from 2015 on, on 66 of 155, 34 of 156 and 76 of 76,
  with none here scored yet. In 2021-2023 the multiple fell while earnings held ($3.23-3.75); in 2024-2026 the earnings fell
  too, below a BEAR case built on the decade's worst year. A class built on the stock's own multiple and a trailing anchor
  does not see that; the one forward figure NIKE filed in the period, the FY27 range, moved the class at once (CHEAP to RICH on
  2026-10-02, on a lower price). Whether forward figures should weigh more, or BEAR reach below the decade's worst year, is a
  question for other tickers and a new method version, never fitted to NKE's outcomes.
