# RCL retrospective findings (hindsight)

Patterns seen in `outcome.json` for the RCL weekly dates: 105 from 2008-01-04 to 2009-12-31. They are **labels and hypotheses**: never feed
them back into the method or the fact sheet. The batch was scored only after its point-in-time build was committed and pushed (ea16eb8).
Outcomes were computed on 2026-11-08 from the closes posted to 2026-11-06; every date has its 6-month, 1-, 2- and 3-year horizons.
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

## The encoding calls, seen afterwards

- The calls listed in retro/README.md ("RCL") move classes only where the class already changes week to week. GAAP EPS instead of the
  company's comparable figures would have moved six dates from CHEAP to FAIR (three of August-September 2008, which returned -12% to +2%
  and beat SPY by 2-11pp, and three of June-July 2009, which returned +142% to +195%); the comparable Q4 2007 guide would have moved two January 2008
  dates to FAIR, which then lost 30-32%. These are hindsight comparisons of alternatives decided before scoring; the calls stay, and
  changing a rule means a new method version tested elsewhere.
- Today's live profile of RCL (`data/business_profiles.json`, a 2026 judgement, recorded in `outcome.json` as profile drift) files it
  CYCLICAL; the retrospective filed it DURABLE on its 10-Ks' wording by the SHW and WMT precedent. The kind changes only the class label, and
  the outcomes above come from the price state, which the EPS anchor set.
