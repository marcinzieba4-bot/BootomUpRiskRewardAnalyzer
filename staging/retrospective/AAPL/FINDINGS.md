# AAPL retrospective findings (hindsight)

Patterns seen in `outcome.json` for the 418 weekly dates from 2008-01-04 to 2015-12-31. They are **labels and hypotheses**:
never feed them back into the method or the fact sheet. Each batch was scored only after its point-in-time build was committed
and pushed: 2008 in e0b1ff4, 2009-2011 in 72db502, 2012-2015 in 2b6d96e. Prices run to 2026-10-29; every horizon used here ends by
2017-12-30. Medians of an even count take the upper middle value (`statistics.median_high`). The 15%/yr hurdle is +32.2% over two
years. Prices are as traded on each date, so entries before 2014-06-09 are on the pre-split basis (seven times the later one);
rank correlations across the split use split-adjusted entry prices.

## 2008 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 33 | +79% | +28% to +279% | 32 | 33 | +51% | 33 |
| class FAIR | 20 | +44% | +19% to +60% | 17 | 20 | +16% | 0 |
| legacy tier BUY (all dates) | 53 | +61% | +19% to +279% | 49 | 53 | +28% | 33 |
| January-September | 39 | +54% | +19% to +128% | 35 | 39 | +22% | 19 |
| October-December | 14 | +238% | +180% to +279% | 14 | 14 | +167% | 14 |
| CHEAP, January-September | 19 | +64% | +28% to +128% | 18 | 19 | +29% | 19 |
| CHEAP, October-December | 14 | +238% | +180% to +279% | 14 | 14 | +167% | 14 |

- **In absolute terms the year paid, whatever the class.** Every date beat SPY over two years, by 35pp to 235pp, and 49 of 53
  cleared the hurdle. The four that missed are the three January dates at $161-180 and 2008-05-09 ($183). But every date lived
  through the 2009-01-20 low ($78.20): drawdowns of 19-59% within two years, and a median one-year return of -18% (FAIR -20%,
  CHEAP +16%).
- **The class ranked the outcomes in order.** CHEAP did better than FAIR on the two-year return (median +79% against +44%) and on
  the m12-24 average price (+51% against +16%). There were no RICH dates.
- **The FAIR call failed by beating the benchmark.** FAIR expects a return within 15pp of SPY's. All 20 FAIR dates beat SPY by
  35-69pp, so the call held on none of them, while the CHEAP call held on all 33. On this stock in this year the class worked as a
  ranking, not as a level.
- **The class was the entry price.** The adjusted gap read UNDERVALUED and the tier BUY on every date, so the only split was the
  distance above the EPP floor: FAIR above +100% (the $165-189 entries), CHEAP below. Across the 53 dates the entry price alone
  ranks the two-year returns almost perfectly (Spearman -0.91). The 14 October-December entries ($83-108) returned +180% to
  +279%; the 20 FAIR entries +19% to +60%. One stock through one crash mostly tests "buy lower". Testing selection needs many
  tickers on the same dates.
- **BULL and XBULL were never in play.** Built on FY2003's $0.08 of EPS (a year of operating losses that interest income carried
  into profit), the BULL case (+165%/yr, then +132%/yr, at the 75th-percentile P/E) priced the stock at $1,086-1,278 in two years
  and XBULL at $7,043-9,606. The two-year prices were $194-324: nearest the BASE price on all 53 dates, and at most 30% of the
  BULL price. Ratio B (0.10 or less) and the market composite (1.00-1.22, the bottom of its grid) carried no information, so the
  BUY tier was right in direction for a scenario that never came close.
  Hypothesis for the method: when the first kept year of the window has near-zero EPS, the decade CAGR and the best two-year run
  are not growth anchors, and they swamp the probability-weighted price. A later version could measure them from a normalized
  base or cap them. Test it on other tickers whose window starts in a trough before any method change; never fit it to AAPL's
  outcomes. LOW's 2008 hypothesis is the mirror image: there a growth decade's multiple and CAGR were stale anchors for a year
  guided at 0-3% sales growth.
- **The BASE case was too low on every date.** The two-year price was 1.01 to 2.19 times the BASE price. BASE carried one
  quarter's revenue guide, less dilution, for two years, and anchored EPS on the last full year (FY07's $3.93 until October). From
  the Q4 FY08 print BASE was -5.4%/yr on the Q1 FY09 range, and those eleven dates, priced below the BEAR case, returned +180% to
  +279%.
- **The FY2002 call, seen afterwards.** Keeping FY2002 in the history would have turned all 20 FAIR dates CHEAP (retro/README.md,
  "AAPL"). Those dates beat SPY by 35-69pp, so the CHEAP call would have held on them too. That is a fact about one stock in one
  year, not a reason to change the encoding: the call was decided before scoring and stays, and changing a rule means a new
  method version tested elsewhere.

## 2009 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 50 | +140% | +81% to +323% | 50 | 50 | +123% | 50 |
| class FAIR | 2 | +124% | +94% to +124% | 2 | 2 | +85% | 0 |
| legacy tier BUY (all dates) | 52 | +139% | +81% to +323% | 52 | 52 | +119% | 50 |
| January-June | 25 | +197% | +129% to +323% | 25 | 25 | +153% | 25 |
| July-December | 27 | +115% | +81% to +160% | 27 | 27 | +86% | 25 |

- **Every date cleared the hurdle and beat SPY,** by 68pp to 266pp. Every two-year price landed nearest the BASE case, at 1.6 to
  2.4 times its price and at most 43% of the BULL price. Drawdowns within two years were 13-19%, and the median one-year return
  was +77%.
- **The entry price ranks the outcomes almost perfectly** (Spearman -0.98). The January-June entries ($82-145) returned +129% to
  +323%, the July-December ones ($139-211) +81% to +160%. The 11 dates priced under the BEAR case, to 2009-03-20 ($82-102), returned
  +226% to +323%.
- **FAIR failed again by beating the benchmark.** The two FAIR dates (2009-10-09 and 2009-10-16, $188-190) returned +94% and +124%,
  82pp and 108pp above SPY, so their call held on neither; the CHEAP call held on all 50.

## 2010 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 52 | +132% | +60% to +181% | 52 | 52 | +79% | 52 |
| legacy tier BUY (all dates) | 52 | +132% | +60% to +181% | 52 | 52 | +79% | 52 |
| January-June | 25 | +132% | +99% to +170% | 25 | 25 | +74% | 25 |
| July-December | 27 | +131% | +60% to +181% | 27 | 27 | +82% | 27 |

- **Every date cleared the hurdle and beat SPY again,** by 44pp to 145pp, from entries at $195-324. Drawdowns were 14-27%. The
  entry price ranks the outcomes less well (Spearman -0.62).
- **BASE turned from too low to too high at the Q4 FY10 print.** To 2010-10-15 the two-year price was 1.18 to 1.89 times the BASE
  price. From 2010-10-20 BASE carried the Q1 FY11 guide's +46.7% (+43.3%/yr after dilution) for two years on FY10's $15.15, and the
  two-year price was 0.65 to 0.77 times it. Every two-year price still landed nearest BASE.
- **The restatement call, seen afterwards.** Without the 10-K/A vintage the 19 dates from 2010-04-22 to 2010-10-15 would have read
  FAIR (retro/README.md, "AAPL 2009-2011"). They returned +103% to +158%, 76pp to 126pp above SPY, so FAIR's call would have failed
  on them and CHEAP's held. That is a fact about one stock in one year, not a reason to change the encoding.

## 2011 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 52 | +34% | +13% to +57% | 31 | 22 | +54% | 38 |
| legacy tier BUY (all dates) | 52 | +34% | +13% to +57% | 31 | 22 | +54% | 38 |
| January-June | 25 | +34% | +14% to +57% | 15 | 22 | +65% | 22 |
| July-December | 27 | +34% | +13% to +51% | 16 | 0 | +27% | 16 |

- **The first year the calls were mostly wrong in level.** CHEAP and BUY on all 52 dates, but the median two-year return was +34%:
  21 dates missed the hurdle and 30 lagged SPY. The CHEAP call held on 38, most of them only by clearing the hurdle.
- **The two halves split on the benchmark's path.** The January-June entries ($320-360) returned +14% to +57% against SPY's +17% to
  +34%, and beat it on 22 of 25. The July-December entries ($343-422) returned +13% to +51% against SPY's +25% to +61%, and lagged
  it on all 27. Their two years held a fall of 44% from the 2012-09-19 high ($702.10).
- **The two-year price landed nearest the BEAR case on 37 dates,** at 0.42 to 0.96 times the BASE price and at most 23% of the BULL
  price. BASE carried quarter guides of +23% to +63% for two more years on top of an anchor that had grown 67% (FY10 on FY09)
  and then 83% (FY11).
- **The cheapest reading was not the best entry.** From the Q4 FY11 print the stock traded at 13-15x FY11's $27.68, below the EPP
  floor, the deepest-value reading of the four years. Those 11 dates returned +32% to +51%, just clearing the hurdle, against SPY's
  +42% to +61%. The entry price no longer ranks the outcomes (Spearman -0.12).

## 2012 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 52 | +13% | -13% to +61% | 11 | 5 | -9% | 11 |
| legacy tier BUY (all dates) | 52 | +13% | -13% to +61% | 11 | 5 | -9% | 11 |
| January-June | 26 | +12% | -13% to +33% | 2 | 0 | -9% | 2 |
| July-December | 26 | +16% | +4% to +61% | 9 | 5 | -6% | 9 |

- **The weakest year for the calls.** CHEAP and BUY on all 52 dates, but the median two-year return was +13%: 41 dates missed
  the hurdle and 47 lagged SPY, by up to 51pp. The CHEAP call held on 11. Every two-year window held the 2013-04-19 low
  ($390.53), 44% under the 2012-09-19 high ($702.10); drawdowns were 29-44% and the median one-year return -20%.
- **Only the entries after the fall paid.** The 43 entries to the end of October ($420-700) returned -13% to +33% and none beat
  SPY. The 9 November-December entries ($510-585, on FY12's $44.15, 4 of them below the EPP floor) returned +35% to +61%, and 5 beat
  SPY. The entry price ranks the outcomes only loosely (Spearman -0.49).
- **BASE was too high on every date.** The two-year price was 0.45 to 0.82 times the BASE price and landed nearest the BEAR case
  on 29 dates. BASE carried the next quarter's guided growth (+12% to +38%, less dilution) for two years on an anchor that had
  just grown 83% (FY11) and then 60% (FY12); FY13's EPS fell 10%.

## 2013 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 52 | +86% | +40% to +130% | 52 | 52 | +66% | 52 |
| legacy tier BUY (all dates) | 52 | +86% | +40% to +130% | 52 | 52 | +66% | 52 |
| January-June | 26 | +108% | +50% to +130% | 26 | 26 | +67% | 26 |
| July-December | 26 | +66% | +40% to +120% | 26 | 26 | +66% | 26 |

- **The deepest-value readings were the best entries.** Every date cleared the hurdle and beat SPY, by 5pp to 95pp, and the CHEAP
  call held on all 52. The 19 dates below the EPP floor (2012-11-16 to 2013-07-25) returned +55% to +130% (median +113%) and the 20
  below the BEAR price +85% to +130%, all above SPY. The entry price ranks the outcomes almost perfectly (Spearman -0.96). In 2011
  the same reading (below the floor, at 13-15x) had returned +32% to +51% and lagged SPY.
- **BASE was too low again from the Q2 FY13 print.** The two-year price stood above the BASE price on 35 of the 52 dates (0.65 to
  1.20 times it) and landed nearest BASE on 49. BASE was +9.3%/yr on the Q1 FY13 guide, then +4.2% to -4.4% on the Q2-Q4 FY13
  ranges and +1.6% on Q1 FY14's.

## 2014 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 39 | +16% | -4% to +52% | 14 | 24 | +31% | 24 |
| class FAIR | 13 | +14% | +6% to +19% | 0 | 6 | +5% | 13 |
| legacy tier BUY (all dates) | 52 | +16% | -4% to +52% | 14 | 30 | +18% | 37 |
| January-June | 26 | +33% | +4% to +52% | 14 | 22 | +52% | 22 |
| July-December | 26 | +9% | -4% to +25% | 0 | 8 | +4% | 15 |

- **FAIR's call held for the first time on this stock,** on all 13 FAIR dates (2014-07-11 to 2014-10-10): +6% to +19% over two
  years, within 8pp of SPY. The CHEAP call held on 24 of 39. CHEAP beat FAIR on the median two-year return only narrowly (+16%
  against +14%), more clearly on the m12-24 average price (+31% against +5%).
- **The year divides around the split.** The 17 entries to 2014-04-25 ($501-572 before the split, $72-82 on its basis) returned +26%
  to +52%, 17pp to 36pp above SPY; the 9 of May and June +5% to +16%, within 2pp of it. The 26 of July-December ($94-119) returned
  -4% to +25%, none cleared the hurdle and 18 lagged SPY; their windows held the fall to the 2016-05-12 low ($90.34). On
  split-adjusted prices the entry price ranks the outcomes well (Spearman -0.81).
- **Every two-year price landed nearest BASE,** at 0.85 to 1.29 times it.

## 2015 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP | 48 | +24% | +6% to +71% | 22 | 29 | +2% | 29 |
| class FAIR | 5 | +19% | +8% to +21% | 0 | 2 | -10% | 5 |
| legacy tier BUY (all dates) | 53 | +23% | +6% to +71% | 22 | 31 | -1% | 34 |
| January-June | 26 | +16% | +6% to +24% | 0 | 6 | -9% | 8 |
| July-December | 27 | +45% | +17% to +71% | 22 | 25 | +19% | 26 |

- **FAIR held again,** on all 5 dates (+8% to +21%, within 7.3pp of SPY). Their trigger was the same as 2008's FAIR dates: the
  price just over 100% above the EPP floor. The 2008 FAIR dates beat SPY by 35pp to 69pp, so the same reading gave opposite calls in
  the two years. The CHEAP call held on 29 of 48.
- **The halves split on the 2016 low.** Every two-year window held the 2016-05-12 low ($90.34). The January-June entries ($106-133)
  returned +6% to +24%: none cleared the hurdle and 6 beat SPY. The July-December entries ($105-130) returned +17% to +71%: 22
  cleared it and 25 beat SPY. The entry price ranks the outcomes loosely (Spearman -0.52).
- **Every two-year price landed nearest BASE,** at 0.90 to 1.31 times it, and at most 54% of the BULL price.

## 2008-2015 together (418 dates)

- **The model never read RICH and always read BUY.** CHEAP on 378 dates, FAIR on 40. The median two-year return was +50%; 283
  of 418 dates cleared the hurdle and 297 beat SPY. The CHEAP call held on 289 of 378 (median +54%). The FAIR call held on 18 of
  40 (median +29%): on none of the 22 FAIR dates of 2008-2009, which beat SPY by more than 15pp, and on all 18 of 2014-2015.
- **2012-2015 was a weaker stretch.** 209 dates: CHEAP 191, FAIR 18, a median two-year return of +26%; 99 cleared the hurdle and
  118 beat SPY; the CHEAP call held on 116 of 191. The two-year price landed nearest BASE on 177 dates and BEAR on 32, never BULL.
- **The verdict carried little information within the stock.** On every date to the FY2013 vintage Ratio B was 0.15 or less and
  the market composite sat at 1.00-1.22, because BULL and XBULL were built on FY2003's $0.08 of EPS. With that year out of the
  window (from 2013-10-30) BULL fell from +102% to +70%/yr, and to +45% from the FY2014 vintage, and XBULL from +340% to +158%,
  then +75%/yr. Ratio B rose to 0.41 and the market composite to 1.26-2.03 in 2014-2015, but the two-year price never reached
  more than 54% of the BULL price. What separated the outcomes was
  the entry price in 2008-2009 and 2013 and the year of entry otherwise.
- **The two-year price beat the BASE price on every date to 2010-10-15 (146 dates), fell short of it on every date from
  2010-10-20 to 2013-04-19 (131 dates), and from 2013-04-25 beat it on 106 of 141.** Quarter-only guidance plus the last-full-year
  anchor kept BASE too low while growth accelerated, too high once BASE carried a single quarter's +23-63% (2010-2011) and then
  +12-38% (2012) for two years, and closer once the guides fell to a few percent.
- Hypotheses for the method, to test on other tickers and never to fit to AAPL's outcomes:
  - when the window's first kept year has near-zero EPS, the decade CAGR and the best two-year run swamp the probability-weighted
    price and pin Ratio B and the market composite (the 2008 hypothesis; once FY2003 left the window, both loosened);
  - for a company that guides one quarter at a time, the last full year's EPS is a stale anchor. A later version could anchor on the
    trailing four quarters, or on the reported quarters plus the next quarter's guide, and should not carry one quarter's guided
    growth for two years;
  - a FAIR reading from the EPP distance alone (more than 100% above the floor) said nothing about the outcome on this stock: it
    beat SPY by 35-69pp in 2008 and tracked it within 8pp in 2015.
