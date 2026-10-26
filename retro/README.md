# Retrospective (point-in-time) analyses

Build a history of what the house model *would have said* on a past date, using only
what was public on that date, then score it against what actually happened.

```
retro/
  facts/<TICKER>.json    dated fact sheet: every value carries a source and its publication date
  templates/             the frozen engine appended to every generated model
  build_acn.py           facts + prices truncated at AS_OF -> archive/.../<AS_OF>/model.py
  build_unp.py           the UNP sibling (railroad signals) -> staging/retrospective/UNP/<AS_OF>/model.py
  retro_tool.py          run / outcome / lint / index / series
  taxonomy_eras.json     era-aware durability themes + anachronism list
archive/retrospective/
  index.json             one row per retrospective (outcome = hindsight, filled separately)
  <TICKER>/SERIES.md     table of one ticker's retrospectives
  <TICKER>/<AS_OF>/
    model.py             generated signal model (house 6-section format, methodology v2, retro method r2)
    report.txt           its printed report
    analysis.json        point-in-time classification, metrics, rules, robustness, sources
    outcome.json         HINDSIGHT: +6m/+1y/+2y/+3y vs SPY, 15%/yr hurdle, average price m12-m24
```

## The one rule

**Nothing in a retrospective may depend on information published after its as-of
date.** That covers facts, and it also covers *parameters, judgement calls and
conclusions*. The builder of the history (a person or a model) already knows what
happened next, so the process is designed so that knowledge has no way in:

1. **Facts enter only through the fact sheet.** Every value in
   `retro/facts/<TICKER>.json` cites a source with a `published` date. The builder
   selects prints and events by date and never sees anything later. Prices and every
   market statistic are computed from data truncated at the as-of date.
2. **No hand-chosen parameter.** Scenario growth, multiples, the EPP floor, the
   structural scores and the conservative case all come from frozen rules applied
   to dated facts (method r2, below). Don't carry a number from a later
   retrospective back to an earlier one. That was the leak in the first ACN
   series: June's Q3-informed growth assumptions reused for January.
3. **Outcomes are labels, never inputs.** `outcome.json` is written by a separate
   command and `run` never reads it. Patterns found in outcomes (for example "CHEAP
   calls with a small gap did worse") are hypotheses for the live model. Test them
   on other tickers or periods; never fold them into the archive that produced them.
4. **Changing a rule means a new method version.** Bump the version, re-run the
   whole archive, and say why. Never tune a rule after looking at how it scores.
5. **Disclose what can't be removed.** A model that writes the fact sheet still
   knows the future. Prefer filings over narrative, mechanical rules over
   judgement, and record the residual risk.

**Exporting as training data.** Inputs are `model.py`, `report.txt` and
`analysis.json` without its `generated` stamp (the build date, which is not
point-in-time) and `_doc`. `outcome.json` is the label and never goes in an input.

`retro_tool.py run` enforces what can be checked mechanically, and refuses to write
anything unless all of these pass:
- every `SOURCES` date is on or before `AS_OF`, and so is `PRICE_DATE`
- no anachronistic term (`taxonomy_eras.json`) and no ISO date after `AS_OF`
- an era-legal durability category
- `CURRENT_PRICE` equals the actual close

## Retro method r2 (frozen 2026-10-23)

| Input | Rule (computed inside every `model.py`) |
|---|---|
| Scenario P/E | Percentiles of the stock's own current-FY P/E over the 10 years to AS_OF: BEAR p10, BASE median, BULL p75, XBULL p90 |
| BEAR EPS growth | The decade's worst normalized EPS year, capped at 0% |
| BASE EPS growth | Latest next-quarter revenue guide midpoint (LC) + guided margin step + historical net buyback |
| BULL EPS growth | Decade EPS CAGR (at least BASE) |
| XBULL EPS growth | Best 2-year EPS run of the decade (at least BULL) |
| EPP floor P/E | Median of the calendar-year P/E lows in the window, rounded down |
| Valuation factor | −0.5 at the 80th percentile of its own P/E or above, 0 at the median, +0.5 at the 20th or below |
| Growth factor | +0.1 per point by which the next-quarter guide exceeds the 10-year median revenue growth (±0.5) |
| Other structural factors | Constant across dates (franchise, balance sheet, the GenAI opportunity/risk pair nets to 0) |
| Conservative case | BASE − 2pp EPS growth, exit at the median P/E rounded down, signals at their BASE floor |
| Signals | Thresholds frozen; values are the latest reported quarter |
| History | The latest annual history vintage published by AS_OF. Prints in scope: those published by AS_OF that guide a fiscal year after that history (a Q4 print guides the next year). Events in scope: those published since the vintage |
| Segment bridge | FY revenue from the FY guide; groups pro rata to the latest actuals; bear flat, bull at the decade revenue CAGR |

Fallbacks for facts a company did not publish (decided before any outcome of the affected dates was computed):

- **No next-quarter guide in local currency:** BASE growth and the growth factor use the full-year LC revenue guide.
  Example: ACN FY08 guided Q2 in dollars only. The test is per print: ACN guided the next quarter in LC from
  Q4 FY15 (2015-09-24), not in Q1 FY16 (2015-12-17, dollars only, so the FY16 guide applies), and again from Q2 FY16.
- **No margin guide:** the guided margin step is 0, and the margin signal uses the latest quarter's year-on-year change.
- **No FX guide:** FY revenue is LC growth only.
- **A distorted year with no published adjusted figure:** it is excluded, and the P/E window starts after it.
  Example: ACN FY02, with a $321M investment loss.

Fiscal-year rollover (added 2026-10-23 for ACN Sep 2008; no earlier output changes, so still r2):

- **A Q4 print extends the history.** Its full-year actuals (EPS, revenue, diluted shares, operating margin, LC
  growth, bookings) join the annual history on its release date, and its guide becomes the current fiscal year.
  The next 10-K vintage replaces them. Example: ACN Q4 FY08 (2008-09-25) moves the base to FY09.
- **Between year-end and the Q4 print** no EPS exists for the new year, so days past the last guided year keep
  that year's EPS in the P/E series. Example: ACN on 2008-09-05 to 2008-09-19.
- **Dividend:** the latest declared rate, from the latest print that states one, else the vintage.
- **A new 10-K before the next quarter's print** (ACN: the FY08 10-K on 2008-10-20, before Q1 FY09 on 2008-12-18).
  The Q4 print stays the latest print, because it is the one guiding the new year. The 10-K replaces its full-year
  actuals. The disruption-theme wording (competitor quote, pricing warning, delivery-network size and whether it grew)
  comes from the latest 10-K event in the fact sheet, so it changes when the 10-K's wording changes.

How recurring cases are encoded (each was decided the first time it came up, then applied the same way):

- **A guide restated only in words** ("toward the upper end", "at the lower end", "flat to slightly positive"):
  the last numeric range stands, and the words go in the print's note. First seen in ACN Q3 FY08 (2008-06-26);
  ACN Q3 FY09 (2009-06-25) keeps the 0-4% FY09 revenue range.
- **A guide assumption the company states only later** (ACN's FY09 and FY10 FX assumptions, first disclosed in
  the following quarter's release) is never back-filled into the earlier print.
- **A one-off charge with a company-published figure without it:** EPS and operating margin use that figure,
  and the note keeps the GAAP number. Example: ACN FY09 restructuring charge (EPS $2.68 vs $2.44 GAAP,
  margin 13.4% vs 12.3%). The same holds for a guide given with and without an announced item: ACN's FY15 guide
  excludes the pension settlement charge (from Q2 FY15, before it was booked) and its FY16 guide excludes the
  Navitaire gain; FY15 is $4.82 (GAAP $4.76) and FY16 $5.34 (GAAP $6.45, gains on business sales).
  A guide that includes a change in accounting with no published figure without it stays GAAP
  (ACN FY17: the share-based payment tax benefit of ASU 2016-09).
  Later cases, same rule: FY17 $5.91 (GAAP $5.44, pension settlement), FY18 $6.74 (GAAP $6.34, US tax-law charges).
  The FY23 guide from Q2 FY23 excludes business optimization costs and the Duck Creek investment gain
  ($11.41-11.63 vs $10.84-11.06 GAAP).
- **A figure published to a decimal** is kept as published (ACN FY16 LC revenue growth 10.5%, FY16 guide 9.5-10.5%).
  The exception is the latest quarter's own LC growth (`revenue_lc`, `consulting_lc`, `managed_lc`), which the frozen
  engine prints as a whole percentage: a decimal there is rounded half up, and the note keeps the published figure.
  Example: ACN Q1 FY19 revenue +9.5% LC is stored as 10; the 7-11% signal band is the same either way.
- **No bookings target** for the year: catalyst (3) reads "Bookings run-rate". ACN gave none for FY16 or FY17.
- **A record the company does not call a record** (`bookings_record`) is derived from the dated history and noted:
  ACN FY17 bookings of $37.4B beat every earlier year (previous high $35.9B, FY14), though the release does not say so.
- **A margin guide measured against a restated prior year** (an accounting change) steps from the restated base the
  company states, never from the reported one (`fy_margin_guide_base` on the print). ACN guided FY19 at 14.5-14.7%,
  "an expansion of 10 to 30 basis points from operating margin for fiscal 2018 of 14.4 percent" under the new revenue
  and pension standards (14.8% as reported). Stepping from 14.8% would read that guide as a 20bp cut. Decided before any
  outcome of the affected dates was computed; it lifts BASE growth from about 9.5% to 12.3% on 2018-09-28 to 2018-12-31
  and changes the class on two of those 15 dates (2018-12-21 and 2018-12-28: FAIR instead of RICH).
- **A 10-K that stops giving a headcount** says so in the event's own words (`gdn_clause`, `gdn_factor`). ACN's FY17
  and FY18 10-Ks give "more than 50 delivery centers" and no delivery headcount, so the last count (about 285,000, FY16)
  is quoted as such. Total employees (425,000, 459,000) are a different measure and are not used.
- **A guide that included an item the company strips out only later** keeps the published figure. ACN's Q2 and Q3 FY20
  EPS guides included investment gains that the Q4 FY20 release (2020-09-24) first removed ("$0.27 in gains ... which
  were included in the guidance provided in the company's third-quarter earnings release"); the earlier prints keep
  $7.48-7.70 and $7.57-7.70. FY20 enters the history at the company's $7.46 excluding $0.43 of investment gains, and the
  FY21 guide is used ex-gains from the print that first gives that figure (Q1 FY21, $8.02-8.25).
- **Bookings growth the company states in local currency** is used as stated (ACN from Q3 FY20). A release that gives
  only dollar growth and no FX impact for bookings keeps the dollar figure, with a note (ACN Q1 FY21: +25%; Q2 FY21
  +13%; Q3 FY21 +39%).
- **A one-off without a company-published figure excluding it** stays in. ACN's FY22 guide from Q3 FY22 ($10.61-10.70)
  includes the $0.15 Russia disposition charge, and FY22 enters the history at GAAP $10.71: no adjusted figure was published.
- **A 10-K without five-year selected data** (Item 6 reserved from the FY21 10-K) supplies the years in its income
  statement (FY19-FY21); earlier years keep the latest 10-K that reported them.
- **A change of segment structure** keeps the segment bridge on the lines the company still reports each quarter. ACN
  manages through three geographic markets from 2020-03-01 but still reports its five industry groups, the same lines
  as the old operating groups, so the bridge keeps them. The split is display only; the bridge total does not change.
- **A guidance reaffirmation without numbers** (ACN 8-Ks of 2019-01-11, 2019-07-11 and 2020-01-13) adds nothing: the last
  numeric guide stands.
- **A filing accepted during market hours** is public before that day's close and keeps its filing date (ACN FY19 10-K,
  accepted 2019-10-29 10:53 ET).
- **A filing accepted after the 16:00 ET close** counts from the next trading day, so it never meets a closing price
  that was set before it was public. Example: the FY11 10-K, accepted 2011-10-21 16:06 ET, is dated 2011-10-24.
- **A release made before the open** may meet the same day's close (ACN moved to pre-market releases in 2013).
  The weekly rule still takes the next trading day unless the week has none (Good Friday, 2013-03-29);
  then the date is the release day, and the builder refuses a same-day print not marked `release_time` before the open.
- **A change of company name** (`company_names` in the fact sheet) applies from its filing date. Example:
  Accenture plc replaced Accenture Ltd on 2009-09-01.
- **A renamed reporting line** takes the new name from the first print that uses it (`service_line` on the print;
  otherwise the vintage's). ACN's Q1 FY23 release (2022-12-16) renames outsourcing "managed services (previously
  referred to as outsourcing)"; the FY22 10-K still says outsourcing, so 2022-10-14 to 2022-12-09 keep it.
- **Market and company-action evidence stays in scope once public**; a 10-K's wording is replaced by the next 10-K. An
  event with a `doc` (10-K wording) expires with the next vintage, an event without one (sell-side read, a loser
  repricing, a company investment) does not. Added 2026-10-23 for ACN's FY23 10-K (2023-10-12), which would otherwise
  have dropped the 2022-23 GenAI evidence; no earlier output changes.
- **A non-earnings 8-K that changes no guided number adds nothing**: ACN's 2024-09-30 segment recast (Middle East and
  Africa moved to Europe), the 2025-06-20 growth-model change (Reinvention Services), the 2026-06-23 extra $2B of FY26
  buybacks and the 2026-10-14 investor day (multi-year ambitions, the FY27 guide unchanged), and the debt offerings.
- **A revenue guide given with and without an item** keeps the published range; the other figure goes in the note
  (ACN FY26: 2-5% LC, about 3-6% excluding the US federal business).

Known limitation: the growth factor compares a local-currency guide with dollar revenue history. That penalizes
periods of a weak dollar, such as ACN in 2004–07. Fixing it needs LC history in the fact sheet and a new
method version.

Known limitation (from FY19): ACN's revenues include reimbursements from FY19 (new revenue standard). Until the FY19 10-K
the annual history stays on the net-revenue basis it was reported on, so the FY19 LC growth guide is applied to FY18 net
revenues in the segment bridge. The bridge's dollar base leaves out reimbursements: $2.03B of FY18's $41.60B revenues
(FY18 10-K), about 5%. From the Q4 FY19 print (2019-09-26) FY19 joins the history at $43.2B on the new basis.
The FY19 10-K (2019-10-29) then revises FY15-FY18 to the new basis. Each vintage takes a year from the latest 10-K that
reports it (the same rule as the FY08 and FY11 EPS restatements), so from that date the revenue history is net
revenues to FY14 and revised revenues from FY15. That seam inflates one year-on-year step (FY15 +8.0% instead of
+3.5% on the old basis). It moves the median revenue growth that the growth factor uses by 0.14pp (5.66% instead of
5.52%), a growth score of 0.014 or 0.003 on the composite. The seam leaves the window with the FY25 vintage
(2025-10-10), whose ten years start at FY15.

Display quirk: the frozen engine prints the latest print's next-quarter LC guide as `+lo-hi%`, so a range that starts
below zero reads `+-2-2% LC` (ACN Q2-Q4 FY20 prints: 39 dates, 2020-03-20 to 2020-12-11; Q4 FY23-Q2 FY24 prints:
38 dates, 2023-09-29 to 2024-06-14). The stored values and the
"Growth vs own history" line (`-2% to +2% LC`) are correct. Fixing the string means editing the engine that is copied
into every model, so it is left for an explicit engine revision.

Ratio B is `inf` (printed `infx`) when the price is above the BULL scenario price: there is no upside even in the bull
case. ACN reached that on 14 dates in 2018, 59 in 2019-2020 and 38 in 2021-2022, and on none from 2023 on. `analysis.json` stores it as
`Infinity`, which Python's json reads.

### The 2023 pilot, harmonized (2026-10-23)

The 2023 series was the pilot of method r2. It was first built from its own FY22 history vintage (the Q4 FY22 release
plus XBRL company facts), before the 2008-2022 chain settled the encoding rules above. At the owner's request it was
re-encoded with those rules. The method is still r2, and no outcome was consulted: the rules existed before, the class
comparison below was computed from point-in-time outputs only, and the outcomes were refreshed afterwards.

- **FY22 history vintage** from the FY22 10-K (S99). It was accepted 2022-10-12 21:04 ET, after the close, so it is
  dated 2022-10-13 (the pilot had 2022-10-12). It now uses company-adjusted EPS (FY13 4.21, FY15 4.82, FY16 5.34,
  FY17 5.91, FY18 6.74, FY20 7.46) instead of means, averages and GAAP, and net/revised revenues instead of XBRL
  totals. BUYBACK is again the decade rate (FY12-FY22 diluted shares, not FY18-FY22), and the P/E window starts
  2002-09-01. The previous quarter is Q3 FY22 (+30% LC), the quarter before the first print in scope.
- **FY22 10-K theme events.** OFFSHORE and CLOUD are recorded, so 2022-10-14 to 2022-11-25 carry the offshore theme
  that the pilot left empty. GENAI takes over from 2022-12-02 as before.
- **Q1-Q3 FY23 prints** re-transcribed from their releases. Groups are year to date, at three decimals, sorted by size.
  EPS and margin from Q2 FY23 exclude business optimization costs and the Duck Creek investment gain, as the company
  published them, with the GAAP figures in the notes. Q2 bookings are $22.09B (the pilot had the rounded $22.1B). The
  prints now carry dividend, buyback-authority, tax and FX notes. The pilot's "business-optimization program defends
  margin" line is dropped: no chain print uses that field. An 8-K/A on 2022-12-16 corrected only a dividend record
  date in the Q1 FY23 release.
- **Q4 FY22** keeps every value; its source text and dividend comment take the chain format. This changes three
  chain dates (2022-09-23 to 2022-10-07) in text only.

Effect on the 38 dates from 2022-10-14, computed from the point-in-time outputs:
- **BASE and XBULL rise.** BASE growth is +0.7pp everywhere (decade buyback). XBULL is 19.8% instead of 16.5%,
  because the best two-year run is now measured on adjusted EPS.
- **Ratio B and gap move together.** Ratio B falls and the adjusted gap rises on every date.
- **Five classes change:** FAIR to CHEAP on 2022-11-25, 2022-12-02, 2023-04-14 and 2023-04-28, and RICH to FAIR on
  2023-06-09.
- **Four legacy tiers change:** ACCUMULATE to BUY on 2023-01-06 and 2023-03-03, WATCHLIST to ACCUMULATE on 2023-05-19,
  and AVOID to WATCHLIST on 2023-06-09.
- **The seam is gone.** BASE is 14.6% on 2022-10-07 and 14.5% on 2022-10-14; the pilot's step to 13.8% no longer
  exists. All 809 dates now follow one set of rules.

Found while checking every quoted fragment of the 10-K events: the FY21 event had kept the FY15-FY20 wording
"may be willing, at times, to price contracts lower than us". The FY2021 10-K adds "take on more risk or". That is
corrected, and 52 dates (2021-10-15 to 2022-10-07) change in text only.

### July 2023 to October 2026: GenAI evidence after the first post-ChatGPT 10-K

The GenAI text of 2022-23 rests on market evidence (ChatGPT, J.P.Morgan, Chegg, IBM, the $3B investment) and says when
to re-file ACN: "when the multiple starts discounting the legacy-services deflation J.P.Morgan describes, or it shows up
in managed-services growth". From the FY23 10-K the builder applies that sentence by rule. The rule was decided on
2026-10-23, before any date from July 2023 on was built or scored, and no earlier output changes.

- **Company evidence.** Each 10-K from FY23 adds a GENAI event with its own words on AI substitution (`kind`
  `genai_company_acknowledged`). The wording hardens year by year:
  - FY23: generative AI is among developments that "have reduced and replaced some of our historical services".
  - FY24: services "will be replaced by automation, including AI-enabled solutions".
  - FY25: services "have been and will continue to be replaced".
  - FY26: AI-enabled automation "has led and may continue to lead to reduced demand for our services".
- **Bookings.** Prints carry the company's AI bookings figure (`genai_note`) while it gives one; the last is Q1 FY26.
- **Re-file test, per date.** The theme is re-filed when the P/E is at or below the 30th percentile of its own
  10-year range, or managed-services growth is below 3% LC. The 30th percentile is the line where the text already
  says "a discount to its own history"; 3% is the managed-services signal's lowest band. A re-filed date is
  `DISRUPTION_EXPOSED` (GENAI) with risk 3, one step above DURABLE's 2. Otherwise it stays DURABLE with GENAI on the
  watch list. The kind changes the class label only (CHEAP reads AI-FEAR BASKET); the price state, the scenarios and
  the tier do not depend on it.
- **Result, point in time:**
  - 2023-07-07 to 2025-06-13: not re-filed.
  - 2025-06-20: re-filed (P/E at the 30th percentile, the day of the Q3 FY25 print).
  - 2025-06-27 and 2025-07-03: back to DURABLE (36th and 41st percentiles).
  - 2025-07-11 to 2026-10-22: re-filed throughout (9th percentile at the end).
- **Not recorded.** OFFSHORE wording from the FY23-FY26 10-Ks is left out: GENAI has priority from 2022-11-30, so
  it would be inert. No press coverage was added after 2023. A fixed-outlet search for earnings-day stories was
  tried and dropped, because the outlet's own stories could not be retrieved reliably. Picking articles by hand
  would select with hindsight.

The last date is 2026-10-22: the series was built on 2026-10-23 before that day's close. A rebuild after the close
moves the week's date to 2026-10-23, so delete 2026-10-22 first. The newest date has no outcome yet.

Judgement calls that could carry hindsight, all made before these dates were scored:
- the 30th-percentile and 3% thresholds, and risk 3 for a re-filed date;
- treating the 10-K wording as the attribution of a discount to AI, when the company never says its multiple reflects AI;
- leaving press coverage out after 2023.

The ⑦ robustness block re-runs the verdict with one input moved at a time; a class
that survives only one set of assumptions is not a call.

## UNP (Union Pacific): the second ticker, in staging

The UNP series is built apart from ACN and shares nothing with it but the machinery. It has its own fact sheet
(`retro/facts/UNP.json`), builder (`retro/build_unp.py`) and engine (`retro/templates/unp_engine.py.tmpl`). The
method is still r2: rules R1-R5, scoring, robustness and the weekly dates are the same code. No ACN fact, parameter,
outcome or finding enters a UNP model. Outputs go to `staging/retrospective/UNP/` with their own `index.json` and
`SERIES.md`. They join the archive later by moving the folder to `archive/retrospective/UNP/` (build with
`--out archive/retrospective/UNP`) and running `retro_tool.py index`.

```bash
python3 retro/build_unp.py --weekly 2008-01-01 2008-03-30                   # 13 dates, 2008-01-04 .. 2008-03-28
python3 retro/build_unp.py --weekly 2008-03-31 2008-12-31                   # 40 dates, 2008-04-04 .. 2008-12-31
python3 retro/build_unp.py --weekly 2009-01-05 2009-12-31                   # 52 dates, 2009-01-09 .. 2009-12-31
python3 retro/build_unp.py --weekly 2010-01-04 2010-12-31                   # 52 dates, 2010-01-08 .. 2010-12-31
python3 retro/build_unp.py --weekly 2011-01-03 2011-12-31                   # 52 dates, 2011-01-07 .. 2011-12-30
python3 retro/build_unp.py --weekly 2012-01-02 2012-12-31                   # 53 dates, 2012-01-06 .. 2012-12-31
python3 retro/build_unp.py --weekly 2013-01-07 2013-12-31                   # 52 dates, 2013-01-11 .. 2013-12-31
python3 retro/build_unp.py --weekly 2014-01-06 2014-12-31                   # 52 dates, 2014-01-10 .. 2014-12-31
python3 retro/build_unp.py --weekly 2015-01-05 2015-12-31                   # 52 dates, 2015-01-09 .. 2015-12-31
python3 retro/build_unp.py --weekly 2016-01-04 2016-12-31                   # 52 dates, 2016-01-08 .. 2016-12-30
python3 retro/build_unp.py --weekly 2017-01-02 2017-12-31                   # 52 dates, 2017-01-06 .. 2017-12-29
python3 retro/build_unp.py --weekly 2018-01-01 2018-12-31                   # 53 dates, 2018-01-05 .. 2018-12-31
python3 retro/build_unp.py --weekly 2019-01-07 2019-12-31                   # 52 dates, 2019-01-11 .. 2019-12-31
python3 retro/build_unp.py --weekly 2020-01-06 2020-12-31                   # 52 dates, 2020-01-10 .. 2020-12-31
python3 retro/build_unp.py --weekly 2021-01-04 2021-12-31                   # 52 dates, 2021-01-08 .. 2021-12-31
python3 retro/build_unp.py --weekly 2022-01-03 2022-12-31                   # 52 dates, 2022-01-07 .. 2022-12-30
python3 retro/build_unp.py --weekly 2023-01-02 2023-12-31                   # 52 dates, 2023-01-06 .. 2023-12-29
python3 retro/build_unp.py --weekly 2024-01-01 2024-12-29                   # 52 dates, 2024-01-05 .. 2024-12-27
python3 retro/build_unp.py --weekly 2024-12-30 2025-12-28                   # 52 dates, 2025-01-03 .. 2025-12-26
python3 retro/build_unp.py --weekly 2025-12-29 2026-10-25                   # 43 dates, 2026-01-02 .. 2026-10-23
for d in staging/retrospective/UNP/2008-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series UNP
python3 retro/tools/firewall.py 2026-10-24 UNP
```

Decided on 2026-10-23, before any UNP outcome was computed:

- **Prices on the as-of share basis.** Yahoo's series is split-adjusted to today's shares. The builder multiplies
  the whole series by the splits after AS_OF (UNP split 2:1 in 2008 and 2014), so the AS_OF close is the price as
  traded. Earlier days in the window are adjusted only for splits already public, so price, 52-week range and P/E
  share one basis with the per-share facts: $120.04 on 2008-01-04, not $30.01. `retro_tool.py` checks the price as
  traded, and outcomes run on the same basis. ACN has no splits, and its 982 models rebuild byte-identical.
- **EPS** is diluted EPS from continuing operations. A company-published figure excluding a one-off replaces GAAP:
  2004 $2.89 (asbestos charge) and 2005 $3.41 (tax reduction), both from the Q4 2005 release. 2000 and 2002 stay
  GAAP ($3.22, $4.78): the company's adjusted $3.61 and $4.30 were on the pre-2003 basis that still included
  trucking. **1998 is excluded** (a $0.41 loss from continuing operations, no adjusted figure), so the history and
  the P/E window start on 1999-01-01 (the ACN FY02 rule).
- **Guides are their own dated list.** UNP gives numeric outlooks in the 10-K and in occasional 8-Ks, not in the
  quarterly releases. The FY2006 10-K (2007-02-26) guides FY07 commodity revenue +6-7%, volume +2-3% and an
  operating ratio "below 80%". The 8-K of 2007-12-19 cuts FY07 EPS to $6.76-6.86. The FY2007 10-K (filed
  2008-02-28 after the close, so dated 2008-02-29) gives FY08 EPS $7.75-8.25 and volume -1% to +1%. Each field
  comes from the latest guide for the current year that states it.
- **No numeric EPS guide** for the current year: the last full year's EPS stands. This extends the rollover rule
  (days past the last guided year keep that year's EPS). It applies from the Q4 2007 print (2008-01-24) to the
  FY2007 10-K: five dates (2008-01-25 to 2008-02-22) use FY07's $6.91, and the Q4 release's "post another record
  year in 2008" goes in the text.
- **No numeric revenue guide:** BASE growth and the growth factor use the latest quarter's commodity revenue growth
  (+6% in Q4 2007). This is the step after ACN's next-quarter, then full-year, fallbacks.
- **No numeric operating-ratio guide.** Words, or a one-sided bound such as "below 80%", give no margin step, and
  the signal uses the latest quarter's change (the ACN "no margin guide" rule).
- **Signals.** Six signals, with ACN's weights:
  - carloads −6 / −1 / 2 / 4 % YoY
  - revenue per car −2 / 2 / 4 / 7 %
  - commodity revenue −8 / 1 / 6 / 11 % (the sum of the first two)
  - GTMs per employee −6 / 0 / 3 / 6 %
  - operating ratio +2.0 / 0.0 / −1.0 / −2.5 pt (lower is better)
  - the theme slot at 2/4

  Values are the latest quarter's published percentages. Thresholds are round numbers around UNP's own dated
  history (1999-2007 carload growth median about +2%) and its FY07 targets.
- **Durability.** DURABLE, risk 2, as for ACN. The "why" is the 10-K's own words: largest railroad in North
  America, 23 western states, BNSF the main rail competitor on parallel routes. No disruption theme in
  `taxonomy_eras.json` is live for a railroad in 2008 (ENERGY_TRANSITION, which would carry coal, is live from
  2015-12-12). So the watch list is empty, and the builder refuses events until a theme encoding is decided.
- **EPS check** in the segment bridge (display only) deducts net interest, since a railroad's interest expense is
  material.

Seen in the first build (method behaviour, not tuned): BEAR growth is the decade's worst EPS year, capped at 0%.
For ACN that year was always positive, so BEAR was flat. For UNP it is 2004 (−29%), applied for two years: a BEAR
EPS about half of today's and Ratio B above 2 on most dates. XBULL is the 2004-2006 recovery (+43%/yr). Both follow
the frozen rule. Whether a cyclical's bear should use the worst 2-year run instead is a question for a new method
version, to be tested on other tickers, never fitted to UNP's outcomes.

Judgement calls that could carry hindsight: the signal thresholds; DURABLE rather than CYCLICAL (this changes the
class label only, not the price state or the tier); dating the FY08 guide from the 10-K, although it may have
been given on the 2008-01-24 conference call (no transcript is in the filings, and the later date can only lag,
never leak).

### UNP April to December 2008: the split, a renamed line, quarter guides

Every 8-K, 10-Q and release of the period was read. Encoding rules decided before any of these 40 dates was built
or scored:

- **A stock split restates per-share facts.** The 2-for-1 split was announced on 2008-05-01 (8-K after the close,
  dated 2008-05-02), paid 2008-05-28, and the stock trades on the new basis from 2008-05-29. From that date every
  per-share fact published before it is divided by 2 and every share count doubled: EPS history and guides,
  print EPS, dividends, diluted shares. Facts published later are already on the new basis. Among them is the
  Q2 2008 release, whose prior-year figures the company restated. The builder checks that the split's effective
  date matches the price data. P/E, the scenarios' multiples and Ratio B do not move across the split; prices,
  EPS and the dividend halve (2008-05-23: $152.16 on $8.00; 2008-05-30: $82.31 on $4.00).
- **The FY08 EPS guide stands all year.** No release or 10-Q of 2008 gives a new full-year number. The 8-K of
  2008-09-23 says full-year targets "will change, but the magnitude is somewhat uncertain". That is a guide in words,
  so the last numeric range ($7.75-8.25, $3.875-4.125 after the split) stands and the words go in the guide line.
- **Quarter EPS guides are notes.** The 8-Ks of 2008-06-17 (Q2 toward the bottom half of $0.90-0.98) and
  2008-09-23 (Q3 $1.28-1.33, up from $1.10-1.20) give next-quarter EPS. Method r2 has no input for a quarter's
  EPS, so each is shown in the guide line until that quarter is reported.
- **Freight revenue replaces commodity revenue** from the Q1 2008 release, with prior periods reclassified. The ACN
  renamed-line rule applies: the signal and the bridge take the new name from the first print that uses it.
- **Adds nothing:** the 8-K/A of 2008-05-06 (dividend record date), the DOJ settlement 8-K of 2008-07-22 (no effect
  on earnings), the 10-Q/A of 2008-07-31 (cover-page share count), the debt and board 8-Ks, and the 10-Qs (no
  outlook). The buyback deadline (March 2011) and announced record and payment dates are not quoted as dates.
  The validator rejects any ISO date after AS_OF, and ACN's fact sheet never quotes scheduled dates either.
- **Text-only change to January-March:** the guide line now takes each field from the latest guide that states it,
  as documented above. On 2008-01-04 to 2008-01-18 it now also quotes the FY2006 10-K's "operating ratio below 80%".
  No number or class changes.

Seen in the build (method behaviour, not tuned): from the Q3 2008 print, BASE growth is that quarter's +16% freight
revenue, which fuel surcharges inflate. The FY08 EPS guide stays at $4.00, while nine-month actual EPS is already
$3.24 (the Q3 release) and the company says the full-year target will change.

### UNP 2009: no numeric guide all year, the FY2008 vintage

Every 8-K, 10-Q and release of 2009 was read. Decided before any 2009 date was built or scored:

- **No numeric 2009 guide anywhere.** The Q4 2008 release ("we expect 2009 will be a difficult year"), the FY2008
  10-K's 2009 Outlook (pricing, network and productivity in words) and the Q1-Q3 releases give words only. The rule
  from 2008-01-25 applies all year: FY08's $4.54 stands as the current-year EPS, and BASE growth and the growth
  factor take the latest quarter's freight revenue growth. That was +2% from the Q4 2008 print, then -20%, -28% and
  -25% from the Q1, Q2 and Q3 2009 prints.
- **The FY2008 10-K vintage** (filed 2009-02-06 after the close, dated 2009-02-09) restates 2004-2008 per share for
  the split. Each year comes from the latest filing that reports it. 1999-2003 come from 10-Ks published before the
  split, and the company-adjusted 2004 and 2005 from the Q4 2005 release, so those years are halved and 2006-2008
  are used as the FY2008 10-K restated them (2007: $3.46, not $3.455). `eps_published` and `shares_published` carry
  each year's own date. The 2008 dates rebuild unchanged.
- **Q2 2009 EPS** is the company's $0.78 excluding the RTD land sale gain ($0.92 GAAP, in the note). This is display
  only: no rule reads a quarter's EPS.
- **Adds nothing:**
  - the 8-K of 2009-10-23: the CEO's media remark that 2010 volume would be close to flat, which the filing says
    "should not be viewed as the Company's guidance";
  - the officer, bylaw, board and debt 8-Ks;
  - the 10-Qs (no outlook).

Seen in the build (method behaviour, not tuned):
- **The fallback extrapolates the trough.** From the Q1 2009 print, the latest quarter's -20% to -28% freight
  revenue becomes BASE growth for two years. The BASE price falls below the market, the adjusted gap drops under
  -0.5, and the class reads RICH while Ratio B (BULL still on the decade CAGR) keeps the legacy tier at BUY or
  ACCUMULATE.
- **The floor stays on FY08's EPS.** The P/E and the EPP floor use FY08's $4.54 all year, while 2009's quarters
  ran below 2008's.
- **A harmless warning.** The year check flags the Q3 2009 carload count (2,035 thousand) as a calendar year (likewise 2,052 and
  2,082 in 2010).

### UNP 2010: still no numeric guide, an accounting recast, two dividend increases

Every 8-K, 10-Q and release of 2010 was read, the 10-Qs searched in full for forward-looking statements. Decided
before any 2010 date was built or scored:

- **No numeric 2010 guide anywhere.** The Q4 2009 release, the FY2009 10-K's 2010 Outlook ("expect volume to increase
  from 2009 levels") and the Q1-Q3 releases give words only. FY09's EPS stands as the current-year EPS, and BASE
  growth and the growth factor follow the latest quarter's freight revenue: -13%, then +16%, +27% and +21%.
- **A filing that re-presents the 10-K is a vintage of its own.** The 8-K of 2010-10-25 (after the close, dated
  2010-10-26) re-presents the FY2009 10-K's financial statements for a change in accounting for rail grinding, which
  is now expensed. It is the latest filing that reports 2005-2009, so from that date the history takes 2006-2009 from
  it (EPS 2009 $3.74 instead of $3.75, operating ratio 76.1%, tax 36.4%). 2005 keeps the company's adjusted $3.41
  before the split: no adjusted figure was published on the new basis. ACN's 2024 segment recast added nothing
  because it changed no input; this one changes the EPS history.
- **The ten-year history moves to 2000-2009** with the FY2009 vintage; 2000's diluted shares (269.5M, before the
  split) come from the FY2002 10-K, the latest that reports them.
- **A vintage's dividend is dated by the declaration it reports** (`dividend_published`). Otherwise the October recast,
  which repeats the 10-K's $0.27, would override the $0.33 declared on 2010-05-06. Only the FY2009 vintages carry the
  field, so no earlier date changes.
- **Dividends:** $0.33 from the 8-K of 2010-05-06 (dated 2010-05-07), $0.38 from the 8-K of 2010-11-18 (dated
  2010-11-19).
- **Adds nothing:**
  - the debt exchange offers and notes;
  - the shareholder-vote and officer 8-Ks;
  - the 7.01 of 2010-06-10 (a shareholder demand letter about fuel-surcharge litigation);
  - the capex and positive train control figures (not method inputs);
  - the 10-Qs (no outlook).

Seen in the build (method behaviour, not tuned):
- **The P/E runs on trailing FY09 EPS.** As the stock rose from about $64 to $92, it reached the 99th-100th
  percentile of its own range, so RICH and AVOID most of the year.
- **BASE growth follows the recovery quarters** (+16% to +27%) from the Q1 2010 print.
- **The BEAR price stays near $24** (the 2004 year applied twice).
- **A labelling quirk inherited from the ACN engine.** When BASE exceeds the decade CAGR, BULL takes BASE's value
  but the text still says "CAGR".

### UNP 2011-2012: two 10-K vintages, an after-close release, Energy renamed Coal

Every 8-K, 10-Q and release of 2011 and 2012 was read, the 10-Qs searched in full for forward-looking statements.
Decided before any 2011 or 2012 date was built or scored:

- **No numeric guide in either year.** The FY2010 10-K's 2011 Outlook ("anticipate volume to increase from 2010
  levels", operating ratio improvement), the FY2011 10-K's 2012 Outlook (volume growth "that will exceed 2011
  levels", "earnings that exceed 2011 earnings") and all eight releases give words only. "Exceed 2011 earnings" is a
  one-sided bound, like FY07's "below 80%", not a range. From each Q4 print the year just reported stands as the
  current-year EPS: FY10's $5.53 from 2011-01-21, FY11's $6.72 from 2012-01-20. BASE growth and the growth factor
  follow the latest quarter's freight revenue: +18% (Q4 2010), +13%, +16%, +16%, +16% (Q4 2011), +14%, +7%, +4%.
- **Two 10-K vintages.** The FY2010 10-K (filed 2011-02-04 after the close, dated 2011-02-07) gives 2006-2010. The
  FY2011 10-K (filed 2012-02-03 after the close, dated 2012-02-06) gives 2007-2011, with 2006 from the FY2010 10-K.
  The ten-year history moves to 2001-2010, then 2002-2011. The first year's diluted shares come from the latest
  10-K that reports them, both before the split: 2001's 271.9M from the FY2003 10-K, 2002's 276.8M from the FY2004
  10-K. 2004 and 2005 keep the company-adjusted figures, as before.
- **A release whose 8-K was filed after the close.** The Q1 2011 release is dated April 20, but its 8-K was accepted
  at 17:13 ET and no filing states an earlier release time. By the after-close rule it is dated 2011-04-21. That was
  the week's last trading day (Good Friday followed), so the week's date is 2011-04-21 and the print counts from its
  open (`release_time`). Every other UNP earnings 8-K of 2007-2012 was accepted during market hours.
- **Energy renamed Coal** in the Q2 2012 release ("Formerly titled Energy"). The bridge shows each print's own group
  names; no rule reads a group's name.
- **Carloads published as "-"** (Q2 and Q3 2012, within half a percent) are 0%, as GTMs per employee were in Q4 2009
  and Q3 2011.
- **Dividends:** $0.475 (8-K of 2011-05-05, dated 2011-05-06), $0.60 (2011-11-17, dated 2011-11-18), $0.69
  (2012-11-15, dated 2012-11-16).
- **Adds nothing:**
  - the 8-K of 2011-02-03 (the $0.38 dividend kept, a new 40-million-share repurchase authorization);
  - the debt exchange offers and notes;
  - the fuel-surcharge antitrust complaint (2011-06-07);
  - the shareholder-vote, officer and board 8-Ks, including the CEO's medical leave (2012-03-02) and his
    successor's election to the board;
  - the 10b5-1 trading plans and a webcast notice;
  - the capex and positive train control figures (not method inputs);
  - the 10-Qs (no outlook).
- **ISO week 2013-W01 starts on 2012-12-31,** so that date is built here, and a 2013 batch starts on 2013-01-07 (as
  2009 started on 2009-01-05 after 2008-12-31).

Seen in the build (method behaviour, not tuned):
- **The class follows the price.** FAIR or RICH on most dates. CHEAP on nine: seven from 2011-08-19 to 2011-10-07
  ($82-90), plus 2012-03-09 and 2012-03-30 ($107-108). RICH again from 2012-07-13 ($118-126).
- **The tier stays low.** WATCHLIST or AVOID on most dates, ACCUMULATE on four in August-September 2011 (Ratio B
  0.89-1.05x). On the middle half of the dates Ratio B runs 1.5-2.8x, because the BEAR price applies 2004's -29%
  twice.
- **EPS anchors on the last full year** while the quarters run ahead of it: FY11's $6.72 stands through 2012, against
  2012 quarters of $1.79, $2.10 and $2.19.

### UNP 2013-2014: a quarter guide, the 2014 split, a release before Good Friday

Every 8-K, 10-Q and release of 2013 and 2014 was read, the 10-Qs searched in full for forward-looking statements.
Decided before any 2013 or 2014 date was built or scored:

- **No numeric full-year guide.** The FY2012 10-K's 2013 Outlook says volume "should exceed 2012 levels" if
  industrial production grows about 2%, and earnings will exceed 2012's even with no volume growth. The FY2013
  10-K's 2014 Outlook says the same with 3%. All eight releases give words only. From each Q4 print the year just
  reported stands as the current-year EPS: FY12's $8.27 from 2013-01-25, FY13's $9.42 from 2014-01-24 ($4.71 after
  the split). BASE growth follows the latest quarter's freight revenue: +2% (Q4 2012), +3%, +5%, +5%, +7% (Q4
  2013), +6%, +10%, +11%.
- **A quarter guide.** The 8-K of 2013-10-03 (after the close, dated 2013-10-04) expects Q3 2013 EPS of $2.45-2.48,
  revenue +4-4.5% and an operating ratio about 1.5 points better. By the 2008 rule it is shown in the guide line
  until Q3 is reported (2013-10-04 and 2013-10-11) and feeds no input. When a year's only guide is a reported
  quarter, the guide line now falls back to the release's words; it used to print an empty list. No earlier date
  changes.
- **The 2014 split.** The 2-for-1 split was announced on 2014-05-15 (8-K after the close, dated 2014-05-16) and paid
  2014-06-06, and the stock trades on the new basis from 2014-06-09, as the price data show. As in 2008, from that
  date every per-share fact published before it is halved and every share count doubled. 2004 and 2005, published
  before both splits, are quartered. P/E percentiles do not move (2014-06-06: $201.86 on $9.42; 2014-06-13: $100.90
  on $4.71). The split note now names each split's years on its own; it used one span for all splits. This is text
  only, and no earlier date changes.
- **A release before Good Friday.** Q1 2014 was released on Thursday 2014-04-17. Its 8-K was accepted at 12:10 ET,
  during the session, and no filing states the release time. No trading day followed in its week, so the week's
  date is the release day. The UNP builder accepted a same-day print only "before the open". It now also accepts one
  public "before the close" by its 8-K's acceptance time, and tags the date "released during the session". The
  2014-04-17 model uses a fact that was public about four hours before that close. Leaving the print out instead
  would only lag it. This is a UNP builder rule; ACN's builder is unchanged.
- **First-year diluted shares:** 2003's 268.0M from the FY2005 10-K, 2004's 262.2M from the FY2006 10-K.
- **Dividends:** $0.79 (8-K of 2013-08-01, dated 2013-08-02), $0.91 (2014-02-06, dated 2014-02-07), the split 8-K's
  $0.91 (45.5 cents post-split, dated 2014-05-16), and $0.50 post-split (2014-07-31, dated 2014-08-01).
- **Values published as "-"** (carloads in Q3 2013 and for full-year 2012 and 2013, some groups' growth) are 0%.
- **Adds nothing:**
  - the debt offerings and exchange offers;
  - the 8-K of 2013-11-21 (the $0.79 dividend kept, a 60-million-share repurchase authorization);
  - the vote, officer and board 8-Ks (a new president of the railroad, the CEO elected chairman after the former
    chairman's death);
  - the 10b5-1 trading plans;
  - the capex and positive train control figures, and the dividend payout target of 30-35% (not method inputs);
  - the 10-Qs (no outlook).
- **ISO week 2014-W01 starts on 2013-12-30,** so 2013-12-31 covers it and the 2014 batch starts on 2014-01-06.
  2014-12-31 covers 2015-W01, so a 2015 batch starts on 2015-01-05.

Seen in the build (method behaviour, not tuned):
- **RICH on 96 of the 104 dates,** at 16-26x trailing EPS. The rest are FAIR (2014-02-14 to 2014-03-28 and
  2014-04-11). The tier is WATCHLIST on 20 dates, otherwise AVOID.
- **The BEAR year changes with the window.** From the FY2013 10-K (2014-02-14) the history runs 2004-2013, so 2004
  is the first year and no longer a growth year. The worst year becomes 2009 (-17.4%), not 2004's -29%, and the
  BEAR price moves from $62 to $84 on the pre-split basis.
- **Ratio B reaches 14-37x in November-December 2014,** when the price nears the BULL price (2014-11-21: upside
  1.8%).
- **Print text is not restated for a split.** From 2014-06-13 to 2014-07-18 the latest print's buyback text (Q1 2014,
  3.8M shares) is on the pre-split share count, as in 2008.

### UNP 2015-2016: volume statements in words, a land-sale gain, the energy-transition question

Every 8-K, 10-Q and release of 2015 and 2016 was read, the 10-Qs searched in full for forward-looking statements.
Decided before any 2015 or 2016 date was built or scored:

- **No numeric guide.** The FY2014 10-K's 2015 Outlook ("positive volume growth", "continued margin improvement") and
  the FY2015 10-K's 2016 Outlook ("volumes to be down slightly") give words only, as do all eight releases. FY14's
  $5.75 stands as the current-year EPS from 2015-01-23, FY15's $5.49 from 2016-01-22. BASE growth follows the latest
  quarter's freight revenue: +9% (Q4 2014), -1%, -10%, -10%, -16% (Q4 2015), -14%, -13%, -7%.
- **Two full-year volume statements in words.** The CFO's remarks furnished on 2015-03-03 ("continues to expect
  full-year carload volumes to be positive year-over-year") and 2016-05-17 (full-year volumes "still expected to be
  down in the mid-single digit range") enter as `fy_words`, the field the 2008-09-23 8-K used. They are shown in the
  guide line and feed no input; the method has no volume input. Their quarter statements (Q1 2015 volumes flat to
  slightly down, Q2 2016 down in the low teens) and the quarter-only 8-Ks of 2015-05-20 (coal) and 2016-03-10 (Q1
  coal and volumes) have no field and add nothing.
- **The Q2 2015 land-sale gain stays in.** The Fremont sale added 8 cents to Q2 2015 EPS ($1.38) and to FY15 ($5.49).
  The company published no figure excluding it, so by the normalization rule GAAP stands; the note says so.
- **Two 10-K vintages on the post-split basis.** The FY2014 10-K (filed 2015-02-06 after the close, dated 2015-02-09)
  gives 2010-2014 already restated for the 2014 split (2010: $2.76, not $5.53 / 2 = $2.765). The FY2015 10-K (filed
  2016-02-05 after the close, dated 2016-02-08) gives 2011-2015. Years from filings published before the 2014 split
  (2005-2009) carry their own `eps_published` dates, so the split halves exactly them, as the FY2008 vintage did for
  2008. First-year diluted shares: 2005's 266.5M from the FY2007 10-K, 2006's 543.9M from the FY2008 10-K.
- **Dividends:** $0.55 (8-K of 2015-02-05, dated 2015-02-06) and $0.605 (8-K of 2016-11-17, dated 2016-11-18).
- **ENERGY_TRANSITION is live from 2015-12-12, but not encoded for UNP.** The taxonomy lets a date use a theme only
  with point-in-time evidence that the market was pricing it for that company; the theme's scope is the owners of oil,
  gas and coal reserves and refining. The FY2015 10-K, the first after the theme went live, carries the same
  climate-change risk factor as the FY2014 10-K ("restrictions on emissions could also affect our customers that (a)
  use commodities that we carry to produce energy"). The same 10-K ties the coal decline to low natural-gas prices and
  high inventories. No filing shows the market pricing the theme for UNP. So the builder still has no theme encoding,
  the theme signal stays "none live" and the class DURABLE. A watch-list line in the ACN style (company-acknowledged,
  no market read) would change text only, not numbers; it is left for the owner to decide.
- **Values published as "-"** (Q1 2015 operating revenue, some groups' growth) are 0%. From Q4 2014 the tables name
  the group "Agricultural Products"; group names are display only.
- **Adds nothing:** the debt offerings and exchange offers; the officer, board, bylaw and vote 8-Ks (a new CEO in
  2015, later also chairman); the PTC deadline 8-Ks (embargo plans, then the extension to 2018); the 10b5-1 plan; the
  repurchase authorization of 2016-11-17 (120 million shares); capex figures; the 10-Qs (no outlook).
- **ISO weeks:** 2015 has 53, so the 2015 batch covers weeks 2-53 (2014-12-31 covers week 1) and ends on 2015-12-31;
  the 2016 batch starts on 2016-01-04 and ends on 2016-12-30. A 2017 batch starts on 2017-01-02.

Seen in the build (method behaviour, not tuned):
- **The 2009 pattern, larger.** From the Q1 2015 print the latest quarter's -1% to -16% freight revenue becomes BASE
  growth for two years. The BASE price falls well below the market, so the class reads RICH on 100 of 104 dates, even
  at 12.7x trailing EPS (the 8th percentile, early 2016). Ratio B, with BULL still on the decade CAGR, puts the legacy
  tier at BUY on 32 dates and ACCUMULATE on 23. The class and the tier disagree for most of the two years.
- **A stale guide line.** March 2015's "volumes to be positive" stays in the guide line all year, while the releases
  later say "the volume outlook remains uncertain". Each field comes from the latest guide that states it (the 2008
  rule: the FY08 EPS guide stood all year too).
- **A sign quirk:** a negative BASE growth prints as "EPS +-13.5%/yr" (as in 2009).

### UNP 2017-2018: tax reform, a pension-cost restatement, the Investor Day targets

Every 8-K, 10-Q and release of 2017 and 2018 was read, the 10-Qs searched in full for forward-looking statements.
Decided before any 2017 or 2018 date was built or scored:

- **No numeric guide.** The FY2016 and FY2017 10-Ks' Outlooks both expect volume "to grow in the low single digit range"
  and margin improvement, in words; all eight releases give words only. FY16's $5.07 stands as the current-year EPS
  from 2017-01-20, FY17's $5.79 from 2018-01-26. BASE growth follows the latest quarter's freight revenue: -1% (Q4
  2016), +6%, +11%, +4%, +5% (Q4 2017), +7%, +8%, +10%. As in 2015-2016, the 10-K Outlook words are not entered as a
  guide; only 8-K statements are.
- **Tax reform: the company's adjusted figures.** The Q4 2017 release (2018-01-25) excludes the Tax Cuts and Jobs Act
  items (the $5.9B deferred-tax remeasurement and the $212M equity-method affiliates item). By the normalization rule
  FY17 enters at the adjusted $5.79 (GAAP $13.36) with the adjusted 63.0% operating ratio (GAAP 62.0%), and Q4 2017 at
  $1.53 and 62.6%, +0.6 pt (GAAP $9.25 and 58.7%). The tax rate (display only, in the bridge's EPS check) is 37.5%:
  the release gives adjusted income taxes ($2,782M) and adjusted net income ($4,638M), and the FY2017 10-K publishes
  the same 37.5% as its adjusted effective rate (GAAP (40.4)%). A Q4 print's `fy_actual` may now carry its own
  `tax_note`; no earlier print has one, so no earlier date changes. The 8-K of 2018-01-09 (the preliminary $5.8B)
  adds nothing.
- **Listed items without an adjusted figure stay in** (the Fremont rule). Q3 2017 lists a workforce reduction charge
  ($0.06, 1.55 pts), Hurricane Harvey ($0.04, 0.75 pts), an Illinois tax adjustment ($0.04), a land sale (+$0.04) and a
  litigation resolution (+$0.05); Q1 2018 the debt redemption's 8 cents. No figure excluding them was published, so
  $1.50 / 62.8% and $1.68 / 64.6% stand, with the items in the notes.
- **ASU 2017-07** (pension cost presentation) restates 2017's quarterly operating ratios in the 2018 releases. The signal
  uses each release's published change against the restated quarter (-0.6, +1.1 and 0.0 pt), the ACN rule for a
  restated base. FY17 stays at the 10-K's 63.0%: no filing in range re-presents FY2017.
- **Four commodity groups from 2018** (Agricultural Products, Energy, Industrial, Premium; the 8-K of 2018-02-13 points
  to the reclassification). Group names are display only.
- **The Investor Day 8-K** (2018-05-31, accepted 17:44 ET, dated 2018-06-01) gives "positive annual volume growth over
  the next three years". That covers 2018, so it enters as `fy_words`, as the 2015 and 2016 CFO remarks did. Its numeric
  items are not a 2018 guide: a 60% operating ratio "on a full year basis by 2020" is a later year's target, and the
  method has no input for capex, a buyback plan (about $20B over three years), a payout target (40-45%) or leverage.
  They are in the guide's note. The Unified Plan 2020 8-K (2018-09-17) says it does not change that guidance: nothing.
- **Dividends without an 8-K.** Unlike 2015-2016, no 8-K announced the 2017-2018 increases. Each enters from the first
  filing that states it: $0.665 from the Q4 2017 release (2018-01-25; declared in Q4 2017), $0.73 from the FY2017 10-K
  (2018-02-09; declared 2018-02-08), $0.80 from the Q3 2018 release (2018-10-25; declared in Q3 2018). This can only lag.
- **Two 10-K vintages.** The FY2016 10-K (accepted 2017-02-03 16:13 ET, after the close, dated 2017-02-06) gives
  2012-2016; the FY2017 10-K (accepted 2018-02-09 14:32 ET, during the session, dated that day) gives 2013-2017. The
  history moves to 2007-2016, then 2008-2017. First-year diluted shares, from the latest filing that reports them,
  both after the 2008 split and before the 2014 one: 2007's 536.8M from the 8-K of 2010-10-25 (the re-presented FY2009
  10-K), 2008's 515.0M from the FY2010 10-K.
- **ENERGY_TRANSITION still not encoded.** Both 10-Ks keep the climate risk factor's wording and tie coal to natural-gas
  prices and utility inventories (PRB shipments -24% in 2016, +5% in 2017). No filing shows the market pricing the theme
  for UNP. ECOMMERCE is a retail theme.
- **The franchise text is unchanged.** The "why" (from the 2008 setup) says "largest railroad in North America"; the
  FY2016 and FY2017 10-Ks do not use that phrase (nor did the FY2007, FY2014 or FY2015 10-Ks checked). It is a constant
  of the method, left as it is; rewording it would change text on every date.
- **Adds nothing:** the weather-cost 8-Ks (2017-03-08, 2017-09-06: quarter EPS effects and the capital plan); the
  workforce reduction (2017-08-16) and land sale (2017-08-30) 8-Ks, whose effects are in Q3 2017; the debt offerings;
  the debt redemption 8-K (2018-04-06), whose effect is in Q1 2018; the accelerated share repurchase (2018-06-14); the
  officer, board, vote, incentive-plan and 10b5-1 8-Ks; the capex figures; the 10-Qs (no outlook beyond the capital plan).
- **ISO weeks:** 2017-12-31 is a Sunday, so the 2017 batch ends on 2017-12-29; 2018-12-31 covers 2019-W01, so the 2018
  batch has 53 dates and a 2019 batch starts on 2019-01-07.

Found while dating these filings: the SEC submissions JSON gives `acceptanceDateTime` in UTC, as step 1 below says, but
the `filed` fields of the earlier UNP sources quote that UTC time labelled "ET" (the FY2015 10-K: "18:24 ET"; EDGAR shows
13:24 ET). Sixteen filings accepted before or during the session were therefore dated the next trading day (U3, U9, U12,
U19, U29, U34, U35, U38, U40, U44, U46, U50, U52, U53, U71, U77), and the Q1 2011 and Q1 2014 release-time notes are off
by the same hours. Every error delays a fact by a day; none makes one visible early. ACN's fact sheet has the same
labels, and one date there moves (S65, the FY2015 10-K: 13:09 ET on 2015-10-30, dated 2015-11-02). The 2017-2018
entries use EDGAR's Eastern times. The earlier entries are not changed here: correcting them changes 2008-2016 outputs
and is left for the owner to decide.

Seen in the build (method behaviour, not tuned):
- **RICH and AVOID on all 105 dates.** On trailing EPS the P/E sits at the 90th-100th percentile of its own ten years
  (18.8-28.5x), as the price rose from $102 to $165.
- **The price passes the BULL case.** BULL is the decade EPS CAGR at the 75th-percentile P/E ($111-138). From 2017-10-27
  the price is above it on 60 dates (Ratio B `inf`: 10 in 2017, 50 in 2018).
- **EPS anchors on the last full year again.** Through 2018 the current-year EPS is FY17's $5.79 while the quarters run
  27-43% ahead ($1.68, $1.98, $2.15), mostly the lower tax rate. The bridge's EPS check, on FY17's 37.5% tax rate,
  reads about $6.4.
- **The BEAR price stays at $45-52:** 2009's -17.4% applied twice, the worst year of the window.

### UNP 2019-2020: an operating-ratio bound, a dropped ratio, COVID

Every 8-K, 10-Q and release of 2019 and 2020 was read, the 10-Qs searched in full for forward-looking statements.
Decided before any 2019 or 2020 date was built or scored:

- **No numeric EPS or revenue guide.** The FY2018 10-K expects volume "to grow in the low single digit range", the FY2019
  10-K "slightly positive", both in words; the releases give words only. FY18's $7.91 stands as the current-year EPS from
  2019-01-25, FY19's $8.38 from 2020-01-24. BASE growth follows the latest quarter's freight revenue: +6% (Q4 2018), -2%,
  -2%, -7%, -10% (Q4 2019), -3%, -24%, -11%.
- **An operating-ratio bound, not a range.** The CFO's remarks furnished on 2019-09-04 (before the open) "confirmed the
  Company's expectation of a sub-sixty-one percent operating ratio result for full-year 2019", and the 8-K of 2019-12-04
  confirms it again. No earlier filing states it (the January call and slides were not filed), so it enters on
  2019-09-04; that can only lag. A one-sided bound gives no margin step (the FY07 "below 80%" rule), so it is
  `op_ratio_guide_text`, shown in the guide line. Their half-year and fourth-quarter volume statements have no field.
- **Release outlooks are not guides.** The Q2 2020 release expects full-year carloads "down around 10 percent or so". As
  with the 2017-2018 releases' full-year words, a release's outlook is its `outlook_short`, shown while it is the latest
  print; only 8-K statements become `fy_words` guides, and the 10-K Outlook words are not entered.
- **GTMs per employee, derived from the release.** From Q1 2019 the releases no longer print GTMs per employee, but they
  still print gross ton-miles and average employees for both years. The signal keeps its definition: the change is
  computed from those four published figures and rounded half up (Q1 2019 -3.43% to -3%), with the inputs in
  `gtm_per_employee_note`. The new "workforce productivity (car miles per employee)" is a different measure and is not
  used (the ACN headcount rule). From 2020 the label reads "Total employees (average)", with the prior year on the same
  basis.
- **Q4 2018 against the adjusted base.** The Q4 2018 release compares with Q4 2017 adjusted and restated for ASU
  2017-07: EPS $2.12 against $1.53 (+39%), operating ratio 61.6% against 62.7% (-1.1 pt). The fact sheet entered Q4 2017
  at its adjusted figures, so the signal uses that change, not the +2.8 pt against GAAP 58.8%.
- **One-offs without an adjusted figure stay in:** the 2019 payroll tax refund ($78.5M and $31.3M of interest; Q1 $42M
  and $27M, Q2 $32M and $3M), the Q2 2020 Illinois Tollway land sale ($69M, $0.07), and the debt exchange fees. The Q1 and
  Q2 2020 releases bridge the prior year's operating ratio and EPS by item, but publish no adjusted figure.
- **A release before Good Friday again.** Q1 2019 was released on Thursday 2019-04-18; its 8-K was accepted at 08:06 ET,
  before the open, and the call was at 8:45 a.m. No trading day followed in its week, so the week's date is the release
  day and the print counts from its open (`release_time`), as in 2014.
- **Commodity groups:** four in 2019 (Agricultural Products, Energy, Industrial, Premium), three from 2020 (Bulk,
  Industrial, Premium; the 8-K of 2020-02-18 points to the reclassification). The 2020 releases also list each group's
  components; the bridge takes the three groups. Group names are display only.
- **Dividends, again without an 8-K:** $0.88 from the Q1 2019 release (2019-04-18) and $0.97 from the Q3 2019 release
  (2019-10-17), each the first filing that states it. The rate is unchanged through Q3 2020.
- **Two 10-K vintages,** both accepted during the session and dated that day: the FY2018 10-K (2019-02-08 14:28 ET,
  2014-2018) and the FY2019 10-K (2020-02-07 15:35 ET, 2015-2019). The history moves to 2009-2018, then 2010-2019. 2017
  keeps the company's adjusted $5.79, which the FY2018 10-K still states. The FY2018 10-K restates 2014-2017 operating
  ratios for ASU 2017-07; no rule reads an earlier year's ratio. First-year diluted shares, from the latest filing that
  reports them, before the 2014 split: 2009's 505.8M from the FY2011 10-K, 2010's 502.9M from the FY2012 10-K (dated by
  EDGAR's Eastern acceptance times, 2012-02-03 and 2013-02-08; the earlier entries for the same 10-Ks, U46 and U52, carry
  the one-day lag described above).
- **No theme encoded.** The FY2019 10-K keeps the climate risk factor; the 8-K of 2020-03-10 pledges science-based
  emission targets for the company's own operations. ENERGY_TRANSITION's market pricing (from 2020-08-31) is dated for
  owners of reserves and refining; no filing shows the market pricing it for UNP. EV (live from about 2020) is scoped to
  ICE powertrains, parts and fuel retail. So the class stays DURABLE with no watch list.
- **Adds nothing:**
  - the 8-K of 2019-01-09 (a preliminary FY2018 operating ratio of 62.7%, which the Q4 print reports two weeks later);
  - the payroll-tax-refund 8-K (2019-03-06), whose amounts are in the Q1 and full-year prints;
  - the 8-K of 2020-03-31: the earlier 2020 outlook "does not include the potential impact of COVID-19", a caveat with no
    figure;
  - the CFO 8-Ks of 2020-05-20 and 2020-06-09, which reaffirm guidance given on the Q1 call without stating it, plus
    quarter volume and operating-ratio statements;
  - the conference 8-Ks of 2020-08-11 and 2020-11-17 (a $37M one-time bonus in Q4 2020);
  - the accelerated share repurchases (2019-02-25, 2020-02-18);
  - debt offerings, debt exchange offers, and officer, board, vote and 10b5-1 8-Ks;
  - capex figures and the 10-Qs (no outlook beyond capital spending).
- **ISO weeks:** 2018-12-31 covered 2019-W01, so the 2019 batch starts on 2019-01-07 and ends on 2019-12-31 (2020-W01).
  2020 has 53 ISO weeks; its batch covers weeks 2-53 and ends on 2020-12-31. A 2021 batch starts on 2021-01-04.

Seen in the build (method behaviour, not tuned):
- **RICH on 102 of the 104 dates.** The exceptions are 2020-03-20, CHEAP at $117.84 (14.1x FY19 EPS, the 14th percentile),
  and 2020-05-15, FAIR. The legacy tier, which keeps BULL on the decade CAGR, read BUY or ACCUMULATE from 2020-03-13 to
  2020-04-17 and on 2020-05-15, WATCHLIST on 14 dates, AVOID on 83.
- **The BEAR price moves with the window.** On 2019-02-08 the FY2018 vintage drops 2008, and with it 2009's -17.4% as a
  growth year (2009 becomes the base). The worst year becomes 2016 (-7.7%), and the BEAR price moves from $72 to $90.
- **The fallback carries the COVID quarter.** From the Q2 2020 print, BASE growth is that quarter's -24% freight revenue for
  two years: the BASE price falls to $92 against a $176 market, and the class reads RICH at the 91st-100th percentile.
- **EPS anchors on the last full year again.** FY19's $8.38 stands through 2020 while Q2 2020 EPS fell to $1.67 and Q3
  recovered to $2.01.

### UNP 2021-2023: numeric operating-ratio guides, the first margin step

Every 8-K, 10-Q and release of 2021 to 2023 was read, the 10-Qs searched in full for forward-looking statements.
Decided before any 2021-2023 date was built or scored:

- **A numeric operating-ratio guide gives the margin step.** Method r2 has always had BASE = revenue guide + guided margin
  step + buyback; UNP had never guided a number until 2021, so the builder fixed the step at 0. It now reads a numeric guide
  in either form the company uses: a full-year ratio (`op_ratio_guide`, a range; a point is lo = hi) or an improvement
  in basis points against a base the company states (`op_ratio_guide_bp`, `op_ratio_guide_base`). The guided margin is 100
  minus the midpoint, the step is taken from the previous year's margin (from the stated base when it differs from the
  history: the ACN FY19 rule), and the operating-ratio signal uses the guided step, as in the frozen engine. Words and
  one-sided bounds still give no step. No earlier guide has these fields, so all 679 earlier models rebuild
  byte-identical. Each guide line quotes the company's wording beside the encoding (`op_ratio_guide_quote`).
- **The 2021 guide** is in the transcript of the Q4 2020 call, furnished by 8-K (accepted 2021-01-22 17:21 ET, dated
  2021-01-25): volume +4% to +6%, and "150 to 200 basis points of operating ratio improvement" against "the 58.5%",
  2020's adjusted ratio, which is the history's. The FY2020 10-K repeats the volume range. The 8-K of 2021-12-01 lowers
  both: volume about +4%, the ratio "around 150 basis points" better (the base unrestated, so still 58.5%). The
  reaffirmations without numbers (8-Ks of 2021-03-02, 03-16, 06-08; the Q1 release) add nothing.
- **The 2022 guide** starts at the 2021 Investor Day: "a 55.X% operating ratio on a full-year basis in 2022" (8-Ks of
  2021-05-04 and 2021-05-05), read as the one-decimal values 55.0-55.9; it is a guide for 2022 once 2022 is the current
  year. The Q1 2022 release gives an "Operating ratio beginning with "55", up from ~55.5%", read as 55.6-55.9 (the values
  that begin with 55 and are above ~55.5%; the ~55.5% itself was in no earlier filing). The CFO's remarks of 2022-06-07
  call a "55" ratio "unlikely" but give no new number, so the last numeric range stands until the next one (the FY08 rule,
  "will change, but the magnitude is somewhat uncertain") and the words go in the guide line. The Q2 2022 release guides
  "around 58%" and carloads +4% to +5%, the Q3 2022 release "reported operating ratio around 60%" (including the Q3
  labor-agreement charge) and carloads ~3%.
- **Releases with a guidance list are guides.** From 2022 the releases carry a bulleted "Guidance" or "Outlook" list; its
  numbers enter as guides, its volume words as `fy_words`. A release's outlook quote stays its `outlook_short`, as before
  (the Q2 2020 release's "down around 10 percent or so" was such a sentence). Lists that only maintain the guide (Q1 and Q3
  2023) add nothing.
- **2023: words only.** The Q4 2022 release guides "Full year operating ratio improvement" and carloads to "exceed
  Industrial Production" (its -0.5% forecast is the company's assumption, not a guide); the 8-K of 2023-06-13 says the year's
  ratio likely "exceeds 2022 levels"; the Q2 2023 release expects volume below Industrial Production. No numeric guide, so
  no margin step; FY22's $11.21 stands as the current-year EPS from 2023-01-25.
- **No EPS or revenue guide** in any year (the Investor Day's "low double-digit earnings per share growth CAGR" is a
  2022-2024 rate, not a current-year range). FY20's adjusted $8.19 stands from 2021-01-22, FY21's $9.95 from 2022-01-21. BASE
  growth follows the latest quarter's freight revenue: -1% (Q4 2020), -5%, +29%, +12%, +10% (Q4 2021), +17%, +14%, +18%,
  +9% (Q4 2022), +4%, -5%, -9%. A tax-rate guide (2021: 23-24%, then about 23%) has no input; the tax note says so.
- **Company-adjusted figures:** Q4 and full-year 2020 exclude the $278M Brazos yard impairment ($2.36 and $8.19, operating
  ratios 55.6% and 58.5%; GAAP $2.05, $7.88, 61.0%, 59.9%), as published in the Q4 2020 release and again in the Q4 2021
  release (no 10-K states them). Q3 2022 excludes the $114M labor-agreement charge ($3.19, 58.2%; GAAP $3.05, 59.9%). FY2022
  has no adjusted figure, so it enters at GAAP $11.21 and 60.1%. Items without an adjusted figure stay in: the 2021 real
  estate gain and state tax changes, the 2022 Illinois Tollway land sale, the Q1 2023 real estate gain ($107M), the Q2 2023
  labor expense ($67M) and Nebraska tax benefit ($73M).
- **The signal takes the change the release publishes,** against the base it names: Q4 2021 against adjusted Q4 2020 (+1.8
  pt), Q3 2023 against GAAP Q3 2022 (+3.5 pt), the same rule as Q4 2018.
- **GTMs per employee** stays derived from the published GTMs and "Total employees (average)", as from 2019.
- **Dividends,** each from the first filing that states it: $1.07 (Q2 2021 release), $1.18 (Q4 2021 release; from 2021 the
  board declares the fourth-quarter dividend in December, 8-K of 2021-11-12), $1.30 (Q2 2022 release), unchanged through
  2023.
- **Three 10-K vintages:** FY2020 (accepted 2021-02-05 16:35 ET, after the close, dated 2021-02-08; selected data
  2016-2020), FY2021 (2022-02-04 15:59 ET, during the session, dated that day) and FY2022 (2023-02-10 09:42 ET). From FY2021
  Item 6 is reserved, so each takes its three income-statement years and earlier years from the latest 10-K that reports
  them (the ACN FY21 rule). First-year diluted shares: 2011's 489.8M (FY2013 10-K, before the 2014 split), 2012's 952.9M
  (FY2014 10-K), 2013's 931.5M (FY2015 10-K, dated 2016-02-05 by its acceptance time; the earlier U77 entry carries the
  one-day lag).
- **A typo in a release:** the Q1 2023 bullet says "first quarter 2022"; its cash flow statement's $575M is Q1 2023. The
  print's note records it.
- **No theme encoded.** The 10-Ks keep the climate risk factor; the company's science-based targets (2021-02-10) and net-zero
  plan (2021-12-06) concern its own emissions. GENAI (live 2022-11-30) and GLP1 (2023-08-08) are scoped to other businesses.
- **Adds nothing:** the 8-K of 2021-01-08 (preliminary Q4 2020 results, reported two weeks later); the weather and wildfire
  8-Ks (quarter costs); the accelerated share repurchases; the STB service-recovery filings (2022-06-07, 2022-06-24); the
  CEO succession 8-Ks (2023-02-27, 2023-07-26: Jim Vena chief executive from 2023-08-14) and the CFO, officer, board, vote,
  diversity-report and 10b5-1 8-Ks; debt offerings and exchanges; capex figures; the 10-Qs (no outlook beyond capital
  spending).
- **ISO weeks:** each year's batch runs from its week 1 (2021-01-04, 2022-01-03, 2023-01-02) to its last trading day in
  week 52. A 2024 batch starts on 2024-01-01.

Seen in the build (method behaviour, not tuned):
- **The margin step and the fallback revenue growth together.** BASE growth is the latest quarter's freight revenue plus the
  guided margin step plus the buyback. In 2021 the Q2 rebound quarter (+29%) set BASE at 37%/yr, so the class read CHEAP
  from 2021-09-10 to 2021-10-01 at 24.6-25.4x trailing EPS (the 92nd-94th percentile). In 2022 fuel-surcharge-inflated
  quarters (+14% to +18%) and the guided margin step (+1.75 pt to April, +1.45 pt to July) set BASE at 15-25%/yr: CHEAP
  on 17 dates and FAIR on 13, even at the 74th-92nd percentile from April to July.
- **2023 reads CHEAP on the multiple.** With no margin step and BASE at 8.6-13.6%/yr, the class read CHEAP from 2023-01-25
  to 2023-07-07 (with two FAIR weeks) at 16.8-18.8x, the 18th-47th percentile. It turned RICH on 2023-07-14 as the price rose
  to $211 (the 48th percentile), and stayed RICH after the Q2 print's -5% freight revenue took BASE to -0.4%/yr.

### UNP 2024-2026: guidance in words, adjusted figures, the Norfolk Southern merger

Every 8-K, 10-Q, 10-K and release from 2024 to 2026-10-23 was read, with the 10-Qs searched in full for forward-looking
statements. The 88 merger filings under Rule 425 (from 2025-07-29) were read too. Everything below was decided before
any 2024-2026 date was built or scored:

- **No numeric guide in any year.** The FY2023-FY2025 10-K Outlooks give words only and are not entered, as before. Every
  release's outlook list is in words.
  - Under the 2022 rule each item enters by its field. Volume words go to `fy_words` and operating-ratio words to
    `op_ratio_guide_text`. EPS words go to `eps_guide_text`, a new field that is display only: it is shown in the guide
    line, and no earlier guide has it.
  - An item enters when its wording changes. An item repeated word for word adds nothing: the Q1 2025 list, all of
    2024's later "Affirmed" items, and punctuation-only changes.
  - Some items have no field. These are items that name no measure ("Profitability outlook gaining momentum"),
    half-year or quarter statements ("Second half volume outlook", "Fourth quarter results expected to be consistent
    sequentially"), and pricing, capital, repurchase and dividend items.
- **EPS growth in words is not a range.** The 2025 list says "consistent with attaining the 3-year CAGR target of
  high-single to low-double digit". The 2026 lists say "mid-single digit", later "Reported" (2026-04-23), then "increased
  to high-single digit" (2026-07-23). These are words, not figures (the 2016 rule).
  - So the last full year's EPS stands: FY23's $10.45 from 2024-01-26, FY24's $11.09 from 2025-01-24, and FY25's adjusted
    $11.66 from 2026-01-28.
  - BASE growth follows the latest quarter's freight revenue: +1% (Q4 2023), -1%, +1%, +4%, 0% (Q4 2024), +1%, +4%, +3%,
    -1% (Q4 2025), +4%, +12%, +15%.
  - The operating-ratio words ("Industry-leading operating ratio", then "Operating ratio improvement") are one-sided:
    no margin step.
- **The 2024 Investor Day** (8-K of 2024-09-19, before the open) gives three-year targets. Its volume statement (revenue
  excluding fuel surcharge to grow faster than volume excluding coal, which will outpace the markets served) enters as
  `fy_words` for 2025, its first year, as the 2018 and 2021 ones did. The Q4 2024 list replaces it on the day 2025
  becomes the current year, so it shows only in the guide's document list. The EPS growth CAGR "in the high single to
  low double digit range" is a three-year rate, not a current-year range.
- **Company-adjusted figures from Q2 2025.** The releases exclude the Kansas deferred-tax benefit and crew staffing
  agreements (Q2 2025: $3.03 and 58.1%, GAAP $3.15 and 59.0%), merger costs (Q3 2025: $3.08 and 58.5%; Q1-Q3 2026: $2.93,
  $3.41, $3.53) and industrial park land sales (Q4 2025: $2.86 and 60.0%, GAAP $3.11). FY25 enters at the adjusted $11.66
  and 59.3% (GAAP $11.98 and 59.8%).
  - Its tax rate (23.2%, from the adjusted income taxes and net income) and net interest are on the same basis: the
    adjusted other income of $379M excludes the $250M of land sales. This is the FY17 rule, and both are display only.
- **When an adjusted figure first appears.** The Q4 2024 release names the $40M crew staffing expense but publishes no
  adjusted figure.
  - So Q4 2024 enters at GAAP $2.91 and 58.7%, and FY24 at GAAP $11.09.
  - The adjusted FY24 $11.11 first appears in the Q4 2025 release (2026-01-27). It enters with the FY2025 vintage, the
    Brazos rule.
  - The Q2 2024 intermodal equipment sale and remediation order were published only as operating-ratio effects, so Q2
    2024 stays GAAP.
- **The signal takes the change the release publishes,** against the base it names, as in 2018 and 2021-2023. Q2 2025 is
  measured against adjusted Q2 2024 (60.4%: -2.3 pt) and Q4 2025 against adjusted Q4 2024 (58.1%: +1.9 pt). Q2 and Q3
  2026 are measured against adjusted 2025 (+1.1 pt and +0.3 pt).
- **Dividends,** each from the first filing that states it, none announced by an 8-K:
  - $1.34 (Q3 2024 release);
  - $1.38 (Q3 2025 release; the Q2 2025 release's "dividend increase of 3%" states no rate);
  - $1.42 (Q3 2026 release).
- **Three 10-K vintages,** all filed during the session and dated that day: FY2023 (2024-02-09 13:56 ET), FY2024
  (2025-02-07 12:12 ET) and FY2025 (2026-02-06 10:03 ET). Each year comes from the latest 10-K that reports it.
  First-year diluted shares: 2014's 901.1M (FY2016 10-K), 2015's 869.4M (FY2017 10-K), 2016's 835.4M (FY2018 10-K).
- **The Norfolk Southern merger adds nothing to the inputs.** The timeline:
  - talks confirmed on 2025-07-24;
  - agreement announced on 2025-07-29;
  - shareholders approved on 2025-11-14;
  - the STB application was filed on 2025-12-19;
  - the Q3 2026 10-Q expects completion in the second half of 2027.
  - The 425 filings give post-close synergy and accretion targets, and the proxy supplement (8-K of 2025-11-06) gives
    projections prepared for the boards. Neither is a guide for UNP's current year.
  - No merger shares are issued before close, so the share history and buyback rate are unchanged. The paused
    repurchases show in the cash-return text.
- **Adds nothing:**
  - the Q3 2025 commentary 8-K (2025-09-10: quarter items and about $50M of merger costs);
  - the accelerated share repurchase 8-K (2025-02-18);
  - the President transition (2025-05-09) and CFO retirement (2026-10-16) 8-Ks;
  - board, vote and debt 8-Ks;
  - the 10-Qs (capital plan only).
- **ISO weeks:** each batch runs from week 1 of its ISO year (2024-01-01, 2024-12-30, 2025-12-29) to its last trading day.
  The last date is 2026-10-23, the day after the Q3 2026 print, built on 2026-10-26. Dates from late 2024 on have only
  part of the two-year horizon, and the latest have no outcome.

Seen in the build (method behaviour, not tuned):
- **2024 reads RICH throughout.** All 52 dates were RICH at 21.2-24.6x (the 73rd-98th percentile) with BASE at -4.4% to
  +8.4%/yr.
- **2025 dips with the price.** The class went FAIR on 27 dates and CHEAP on 4 (2025-04-04, 2025-04-25, 2025-09-12,
  2025-10-24), at 19.2-21.6x (the 40th-72nd percentile). It turned RICH again from 2025-11-28.
- **Fuel-inflated freight revenue lifts BASE in 2026.** The Q4 2025 print's -1% set BASE at +2.8%/yr: RICH from
  2026-01-28 at the 43rd percentile. The Q2 and Q3 2026 prints' +12% and +15% (high fuel prices) set it at +15.8% and
  +18.8%/yr. So the class read FAIR on five dates from 2026-09-18 at 23.5-25.1x (the 92nd-98th percentile). This is
  the 2022 pattern again.

## LOW (Lowe's): the third ticker, in staging

The LOW series is built apart from ACN and UNP and shares nothing with them but the machinery: its own fact sheet
(`retro/facts/LOW.json`), builder (`retro/build_low.py`) and engine (`retro/templates/low_engine.py.tmpl`, the UNP engine
with retail signals). The method is still r2. No ACN or UNP fact, parameter, outcome or finding enters a LOW model.
Outputs go to `staging/retrospective/LOW/`, beside UNP, with the same `index.json` and their own `SERIES.md`.

```bash
python3 retro/build_low.py --weekly 2008-01-01 2008-12-31                   # 53 dates, 2008-01-04 .. 2008-12-31
for d in staging/retrospective/LOW/2008-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series LOW
python3 retro/tools/firewall.py 2008-07-01 LOW
```

Every 10-K from FY1997 to FY2007 (with the FY2003 and FY2005 10-K/As), every 8-K, 10-Q and earnings release from
November 2006 to December 2008 was read. Transcription was done by Sonnet 5.5 agents (the cheaper model, per "Which model
to run it on"), which downloaded the filings and checked 1,487 strings word for word with `verbatim.py`; Opus chose the
signals and rules, assembled the fact sheet and checked 18 more strings. Decided on 2026-10-26, before any LOW model was
built or any LOW outcome computed:

- **Fiscal calendar.** Lowe's fiscal year N ends on the Friday nearest January 31 of N+1 (fiscal 2007 ended 2008-02-01).
  The builder maps each day to its fiscal year by that rule and checks it against the year-end dates the filings state.
  Days between the year end and the Q4 print keep the last guided year's EPS (the ACN rollover rule).
- **Prices on the as-of share basis** (the UNP rule). LOW split 2-for-1 effective 1998-06-29, 2001-07-02 and 2006-07-03.
  In the 2008 vintages only the 2006 split restates facts: EPS of 1997-2000 (from 10-Ks published before it) and the first
  year's diluted shares, which also take the 2001 split (370.6M for 1997 from the FY1999 10-K becomes 1,482.5M).
- **History: each year from the latest 10-K that reports it.** FY2006 vintage (2007-04-03): 2002-2006 from the FY2006 10-K,
  2001 from the FY2005 10-K/A (restated for early payment discounts and the split), 2000 from the FY2004 10-K (restated for
  lease accounting), 1999 from the FY2003 10-K/A, 1998 from the FY2002 10-K, 1997 from the FY2001 10-K. The FY2007 10-K
  (accepted 2008-04-01 17:02 ET, dated 2008-04-02) moves the window to 1998-2007. Two seams stay in, as published:
  1997-1998 still include the Contractor Yards, which are discontinued operations from the FY2003 10-K, and 1997 is on the
  Eagle Hardware pooling basis (the FY1997 and FY1998 10-Ks are not).
- **EPS** is diluted EPS from continuing operations where the filing reports the line, else diluted EPS. No year is
  excluded. 1999 keeps the $0.04 Eagle Hardware merger charge: the company's $1.79 excluding it (FY1999 10-K) is on the
  earlier basis that included the Contractor Yards (the UNP trucking rule). FY2004 keeps the $0.16 EPS effect of adopting
  EITF 02-16 (an accounting change with no published EPS excluding it).
- **Guides are a dated list**, one per release ("Lowe's Business Outlook": the next quarter and the fiscal year) plus 8-Ks.
  Method r2 maps them as for ACN: current-FY EPS = the EPS guide midpoint; BASE growth and the growth factor = the
  next-quarter total sales guide (Lowe's is a US retailer, so local currency is dollars); the guided margin step = the
  fiscal-year margin guide in basis points. Each field comes from the latest guide for the current year that states it.
- **The margin definition changes with the FY2008 guide.** To the Q3 FY07 release Lowe's guides "operating margin
  (defined as gross margin less SG&A and depreciation)"; from the Q4 FY07 release (2008-02-25) "EBIT margin", earnings
  before interest and taxes, which also deducts store opening costs. Each guide steps from the previous year's margin on its
  own definition (the ACN rule for a restated base): FY07's -130bp from FY06's 11.29% operating margin, FY08's -180bp
  from FY07's 9.74% EBIT margin. Both previous-year margins are derived from the published percent-of-sales column (EBIT
  margin = pre-tax + interest). A print carries both margins; the report shows the one the current guide uses. In the EPS
  check (display only) store opening costs come off the operating margin but not off EBIT margin.
- **A guide in words keeps the last numeric range.** The 8-K of 2007-09-24 (accepted 17:34 ET, dated 2007-09-25) expects
  fiscal 2007 EPS "at the low end or slightly below its prior guidance of $1.97 to 2.01": the range stands, the words go in
  its note. Its 2008-2010 outlook (sales +8-11% a year, EPS growth averaging 12-15%) is a multi-year rate, not a
  current-year range, and is not entered; on the day fiscal 2008 became the current year the Q4 FY07 release gave a numeric
  guide.
- **Adds nothing:** the analyst-conference 8-K of 2008-09-24 (it repeats the FY2008 guide with the same numbers; its first
  FY2009 outlook matters only from fiscal 2009 and is left for a 2009 batch to decide); the 10-Qs' outlook sections (they
  repeat the release guides); the FY2007 10-K's outlook paragraph (the same); the bylaw, officer, director, credit-facility
  and debt-offering 8-Ks.
- **Dividends,** each from the first filing that states it: $0.08 quarterly from the 8-K of 2007-05-25; $0.085, declared
  2008-05-30 without an 8-K, from the Q1 2008 10-Q (accepted 2008-06-04 16:59 ET, dated 2008-06-05; this can only lag).
- **Signals.** Six, with ACN's weights: comparable store sales (% YoY), gross margin change (bp), net sales growth (%),
  inventory growth less net sales growth (pp, lower is better), the operating-margin change (bp; the guided fiscal-year step,
  else the latest quarter), and the theme slot at 2/4. Values are the latest release's: the margins and the inventory
  growth are derived from the published percent-of-sales column and balance sheets (the UNP GTMs-per-employee rule).
- **Thresholds by rule T,** set because the builder already knows what happened in 2008, so nothing is placed by eye. For
  each signal, its ten annual values for fiscal 1997-2006 (each year from the latest 10-K published by 2008-01-04 that
  reports it; a change from the latest filing that reports both years; the inventory gap within one filing): XBULL = the
  decade's best year, BULL = its median, BASE = its worst year, BEAR = one median-to-worst step below the worst (mirrored
  for the inventory gap). Rounded to whole percent and points, and to 10 bp. A company-published figure excluding an item
  replaces the reported one: FY2004 gross margin "flat compared to 2003" excluding EITF 02-16 (+264bp as reported), FY2006
  sales "approximately 10%" excluding fiscal 2005's extra week (+8.5% as reported).

  | Signal | Decade (FY1997-FY2006) | BEAR / BASE / BULL / XBULL |
  |---|---|---|
  | comparable store sales | 4, 6, 6, 1, 2.5, 5.8, 6.7, 6.6, 6.1, 0.0 % | -6 / 0 / 6 / 7 % |
  | gross margin change | 60, 20, 70, 70, 60, 149, 71, 0, 64, 32 bp | -60 / 0 / 60 / 150 bp |
  | net sales growth | 18.7, 20.0, 19.3, 18.9, 18.2, 20.3, 18.1, 18.2, 18.6, 10 % | 1 / 10 / 19 / 20 % |
  | inventory less sales | -11.1, 2.0, -1.4, -1.2, -7.8, -9.9, -2.6, 12.3, -5.2, -2.3 pp | 27 / 12 / -2 / -11 pp |
  | operating margin change | 20, 40, 90, 20, 50, 132, 27, 4, 62, 20 bp | -30 / 0 / 30 / 130 bp |

- **Durability.** DURABLE, risk 2, as for ACN and UNP. The "why" is the 10-K's own words: "the world's second largest home
  improvement retailer", and "Sales of many of our product categories and services are driven by housing turnover and
  activity level of home improvement projects". The 10-Ks name no competitor. No disruption theme in `taxonomy_eras.json`
  is live for a home-improvement retailer in 2008 (ECOMMERCE from 2015-01-01), so the watch list is empty and the builder
  refuses events until a theme encoding is decided.
- **Segment bridge** (display only): the latest 10-K's product categories, 20 in the FY2006 10-K and 19 (recast) in the
  FY2007 10-K, with each category's growth from the same table.

Seen in the build (method behaviour, not tuned):
- **The multiple sits at the bottom of its own range.** Over the ten-year window the P/E on each year's EPS ran from
  about 14x (5th percentile) to 43.5x. On guided EPS the stock traded at 11-17x in 2008 (the 0th-27th percentile), so the
  valuation score is +0.38 to +0.5, and the EPP floor (17x, then 16x) sits above the price on all 53 dates.
- **BASE growth is the guided margin step.** Method r2 carries the guided step as EPS growth for two years: FY07's -130bp
  on an 11.3% margin and FY08's -180bp on 9.7% give BASE -10.6%/yr in January and -21% to -25%/yr from the Q4 FY07 print. The BASE
  price ($17-32) sits at or below the BEAR price ($20-29, flat EPS then FY07's -6.5% at the 10th-percentile P/E).
- **Ratio B at most 0.20 on every date** (negative when the price is under the BEAR price), so the legacy tier reads BUY on all
  53. The proxy composite is 1.30 throughout: comparable sales, gross margin, sales growth and the margin step all fall
  below the decade's worst year.
- **The class follows the price:** CHEAP on 30 dates (January to March, late June to early August, October to November,
  late December), FAIR on 15, RICH on 8 (late April, mid-August to September, at 16-17x).
- **A display quirk inherited from the UNP engine:** the conservative case says the multiple is "already near its median"
  whenever it is not above it by 10%, even at 11x against a 21x median.

Judgement calls that could carry hindsight: rule T itself (mechanical, but chosen by a builder who knows 2008); the choice
of the inventory signal; applying the two published "excluding" figures to the threshold histories; DURABLE rather than
CYCLICAL (the class label only); EBIT margin taken as pre-tax plus interest.

### LOW 2009-2010: two more vintages, a level-form margin guide, the first margin increase

```bash
python3 retro/build_low.py --weekly 2009-01-05 2009-12-31                   # 52 dates, 2009-01-09 .. 2009-12-31
python3 retro/build_low.py --weekly 2010-01-04 2010-12-31                   # 52 dates, 2010-01-08 .. 2010-12-31
```

Every 8-K, 10-Q, 10-K, 10-K/A and earnings release of 2009 and 2010 was read by Sonnet 5.5 agents (758 strings checked
with `verbatim.py`). Thresholds (rule T) and signals are unchanged. Decided before any 2009 or 2010 date was built or scored:

- **Two 10-K vintages.** The FY2008 10-K (accepted 2009-03-31 16:34 ET, dated 2009-04-01) gives 2004-2008, the FY2009 10-K
  (2010-03-30 17:28 ET, dated 2010-03-31) gives 2005-2009; the history moves to 1999-2008, then 2000-2009, each earlier
  year from the latest 10-K that reports it. First-year diluted shares: 1999's 767.7M from the FY2001 10-K, 2000's 769M from
  the FY2002 10-K, both before the 2006 split. The FY2009 10-K adopts two-class EPS retrospectively and prints FY2006
  diluted EPS as $1.98 ($1.99 in every earlier filing, unexplained); by the vintage rule the FY2009 vintage uses $1.98.
  Its two 10-K/As add nothing: the first only furnishes the XBRL exhibit, the second corrects exhibit references in Item 15.
- **A release on a Friday.** The Q4 FY08 release came out on Friday 2009-02-20 (8-K accepted 08:02 ET, "For 7:00 am EST
  Release", call at 9:00 a.m.). No trading day followed in its week, so the week's date is the release day and the print
  counts from its open (the ACN rule for Good Friday 2013).
- **The analyst-conference outlooks are guides for the next year.** The 8-K of 2008-09-24 gives the first fiscal 2009
  outlook, with EBIT margin as a level, "in the range of 7.2 to 8.1 percent" of sales; the 8-K of 2009-09-22 the first fiscal
  2010 outlook (EBIT margin "increase approximately 30 basis points"). Each enters as a guide for its year (the UNP Investor
  Day rule). A level-form margin guide gives the guided margin as its midpoint (the UNP `op_ratio_guide` rule;
  `op_margin_guide_pct`). Both are replaced field by field on the day their year becomes current, so they show only in the
  guide's document list and in the next EPS note ("lowered from $1.40-1.65"). Their repetition of the current year's guide
  adds nothing; so do the 2009 8-K's "not expected to exceed $100 million" of possible impairments (no field) and the
  2007-09-24 8-K's multi-year rates (unchanged).
- **Every guide from 2009 is in EBIT margin.** From Q1 FY10 the releases fold store opening costs into SG&A and reclassify
  the prior year; EBIT margin (pre-tax plus interest) is unaffected, and the derived operating margin then equals it.
- **One-offs without an adjusted figure stay in** (the Fremont rule): Q2 FY09's $48M charge for store projects no longer
  pursued, Q3 FY09's $57M charge ("approximately two cents per share") and its one-cent state tax benefit, Q3 FY10's $50M
  long-lived asset charge ("two cents"). No release or 10-K prints EPS excluding them.
- **Dividends,** none announced by an 8-K, each from the first filing that states it: $0.09 declared 2009-05-29 (Q1 2009
  10-Q, accepted 2009-06-01 15:35 ET), $0.11 declared 2010-05-28 (Q1 2010 10-Q, accepted 2010-06-01 18:03 ET, dated
  2010-06-02).
- **Adds nothing:** the 10-Qs' outlook sections (they repeat the release guides; from 2010 they add that the outlook does
  not include share repurchases), the $5 billion repurchase authorization of 2010-01-29 (a cash-return fact shown in the
  vintage text, no method input), depreciation guides and capex forecasts, the debt offerings, bylaw, director, officer
  and 401(k) blackout 8-Ks.
- **Text-only change to 2008:** a store-count guide given as a range now prints as a range. The Q3 FY08 release's "115 to
  120 stores" printed as "115 stores" on the seven dates from 2008-11-18; the 2007 guides change the same way but no 2008
  date shows them. Two source descriptions (the FY2001 and FY2002 10-Ks) now also cite the 1999 and 2000 share counts the
  new vintages use, so every 2008 model's SOURCES text changes. No number, class or tier changes.

Seen in the build (method behaviour, not tuned):
- **2009 reads RICH on 40 of 52 dates.** From the Q4 FY08 print the guided margin step (-170bp, then -130bp) plus negative
  guided sales put BASE at -19% to -28%/yr, and the BEAR case applies FY2008's -19.9% EPS year twice. Both prices sit near
  $11-15 against a market of $13-24, so the adjusted gap reads overvalued. CHEAP only before the Q4 print (to 2009-02-13),
  on 2009-03-06 and on three dates from 2009-06-19 to 2009-07-10 (10 dates). The multiple climbs from the 1st to the 61st percentile of its
  own range as guided EPS falls to $1.12-1.18. Ratio B, with BULL still on the decade CAGR, keeps the tier at BUY or
  ACCUMULATE all year.
- **2010 turns with the FY2010 guide.** From the Q4 FY09 print (2010-02-23) the guided step is an increase (+40 to +70bp), so
  BASE is +9% to +15%/yr. The margin step scores BULL, as does gross margin on the Q4 FY09 (+122bp) and Q3 FY10 (+85bp)
  prints, and the proxy composite rises from 1.50 to 1.80-2.20. The class reads CHEAP on 30 dates (2010-02-23, 2010-03-05
  and late May to November, at 13.8-17.7x), FAIR on 11, RICH on 11 (January to mid-February on the FY2009 guide, and April to
  mid-May). The tier spreads out: BUY 29, ACCUMULATE 12, WATCHLIST 10, AVOID 1 (2010-04-23, $28.22 at 20.7x).
- **The EPP floor drops to 15x, then 14x** (from 2010-07-02) as the window takes in 2008-2010's low multiples.

Judgement calls that could carry hindsight: entering the analyst-conference outlooks as guides (they change only the
document list and one EPS note); treating the 2009 impairment ceiling and the repurchase authorization as adding nothing.

### LOW 2011-2012: a 53-week year, store closings, no more quarter guides

```bash
python3 retro/build_low.py --weekly 2011-01-03 2011-12-31                   # 52 dates, 2011-01-07 .. 2011-12-30
python3 retro/build_low.py --weekly 2012-01-02 2012-12-31                   # 53 dates, 2012-01-06 .. 2012-12-31
```

Every 8-K, 8-K/A, 10-Q, 10-K, 10-K/A and earnings release of 2011 and 2012 was read by Sonnet 5.5 agents (818 strings
checked with `verbatim.py`). Thresholds and signals are unchanged. Decided before any 2011 or 2012 date was built or scored:

- **Two 10-K vintages.** FY2010 (accepted 2011-03-29 08:26 ET, before the open, dated that day; 2006-2010) and FY2011
  (2012-04-02 16:59 ET, dated 2012-04-03; 2007-2011). The history moves to 2001-2010, then 2002-2011. First-year diluted
  shares: 2001's 795M from the FY2003 10-K/A, 2002's 810M from the FY2004 10-K, both before the 2006 split. From the FY2010
  10-K store opening costs sit inside SG&A with prior years reclassified; EBIT margin is unchanged by it. The FY2011 10-K/A
  only corrects one XBRL tag: nothing.
- **A 53-week year.** Fiscal 2011 ended 2012-02-03 (the Friday-nearest rule gives it). Its sales guides read "including the
  53rd week", with the week's share in a second bullet: the published range stands and the week goes in the note (the ACN
  "with and without an item" rule). The Q3 FY11 release guides Q4 sales "+8%, including the 14th week" (about 7 points of
  it); that is the next-quarter guide, so BASE growth uses 8% on 2011-11-15 to 2012-02-24, as published.
- **The store-closing 8-K of 2011-10-17** (items 2.05, 2.06, 8.01, accepted 09:13 ET, during the session) closes 20 stores
  and says the $0.17 to $0.20 per share of charges "was not contemplated in the business outlook for fiscal 2011". It gives
  no new range, so the August range ($1.48-1.54) stands with the 8-K's words in its note (the 2007-09-24 rule); the Q3 FY11
  release's range, which includes the charges, replaces it on 2011-11-14. No hand adjustment is made.
- **One-offs without an adjusted figure stay in** (the Fremont rule): Q2 FY11 $83M ($0.04), Q3 FY11 $336M ($0.17), $0.26 for
  fiscal 2011, the 2012 headquarters charges ($0.01 a quarter), Q3 FY12 $85M ($0.05). No release or 10-K prints EPS
  excluding them; the 2011 guides say they include them.
- **No next-quarter outlook from the Q4 FY11 release (2012-02-27).** By the ACN FY08 fallback, BASE growth and the growth
  factor use the fiscal-year sales guide. The 2012 guide gives sales as reported (+1-2%, then "approximately flat") and "on a
  52 versus 52 week basis" (about +3%, +1%, +2%): the reported range stands, the 52-week figure goes in the note.
- **A tax-rate guide** (2012: about 38.1%, then 37.9%, 37.8%, 37.7%) replaces the last year's rate in the EPS check, display
  only (the ACN rule: the latest tax-rate guide). The guide line prints a point EPS guide ("approximately $1.64") as one
  figure.
- **A full-year comp in words.** The Q4 FY11 release says fiscal 2011 comparable sales "were essentially flat": 0.0, the
  words in the note, as "flat" guides are encoded; the FY2011 10-K later prints 0.0%.
- **Dividends,** each from the first filing that states it: $0.14 declared 2011-05-27 (Q1 2011 10-Q, accepted 2011-05-31
  17:19 ET, dated 2011-06-01), $0.16 declared 2012-06-01 (Q1 2012 10-Q, accepted 2012-06-05 19:09 ET, dated 2012-06-06).
- **Adds nothing:** the RONA proposal and its withdrawal (8-Ks of 2012-07-31 and 2012-09-17, after the close; no guided number
  changed, guidance would be updated "if Lowe's moves forward"); the $5 billion repurchase authorization of 2011-08-19 (first
  stated in a 10-Q) and the repurchase amounts the guides assume (no method input); depreciation and capex guides; the
  credit facility, debt offering, officer, director and bylaw 8-Ks; the 10-Qs' outlook sections (they repeat the releases).
- **Text-only change to 2008-2010:** two source descriptions (the FY2003 10-K/A and the FY2004 10-K) now also cite the 2001
  and 2002 share counts the new vintages use. No number, class or tier changes.
- **A harmless warning** on 13 dates (2012-05-22 to 2012-08-17): the year check reads `SHARES_DIL_B = 1.2080` as the year 2080.

Seen in the build (method behaviour, not tuned):
- **2011: CHEAP until the margin guide turned down.** The FY2011 guide's +30bp step put BASE at +7%/yr, gross margin and the
  inventory gap scored BULL, and the proxy composite reached 2.35: CHEAP on 24 dates from 2011-02-24 to 2011-08-12 (FAIR on
  2011-04-15). From the Q2 FY11 print the step turned to -30bp, then -80 to -90bp with the store closings: BASE -1% to -4%/yr,
  RICH on 17 dates (CHEAP again on 2011-09-02, 09-09 and 09-30 at 12.5-12.8x). FAIR on the 7 January-February dates.
- **2012: the +100bp guide.** From the Q4 FY11 print the FY2012 step (+100bp, then +90bp on a 6.53% base) and buybacks put
  BASE at +16% to +17.5%/yr: CHEAP on 19 dates to 2012-08-17 (FAIR from 2012-03-30 to 2012-05-04). The Q2 FY12 guide cut the
  step to +45bp and BASE to +9%/yr. As the price rose from $26 to $36 (16-22x, up to the 95th percentile) the class read RICH
  on every date from 2012-08-21 and the tier AVOID from 2012-09-14, Ratio B climbing from 1.9x to 43x and `inf` on 2012-11-30
  (the price above the BULL case). The eight January-February dates, still on the FY2011 guide, read RICH and AVOID as well.
- **The EPP floor drops to 13x** from 2011-06-10.

Judgement calls that could carry hindsight: reading "essentially flat" as 0.0; keeping the 14th-week quarter guide as
published in BASE; treating the RONA proposal as adding nothing.

### LOW 2013-2014: a renamed comp, the Orchard acquisition, an evening 10-K

```bash
python3 retro/build_low.py --weekly 2013-01-07 2013-12-31                   # 52 dates, 2013-01-11 .. 2013-12-31
python3 retro/build_low.py --weekly 2014-01-06 2014-12-31                   # 52 dates, 2014-01-10 .. 2014-12-31
```

Every 8-K, 10-Q, 10-K and earnings release of 2013 and 2014 was read, this time by Opus directly (the eight releases are
short). 153 strings were checked with `verbatim.py`, and 259 structured checks read each print's numbers back from its
release's table rows and each source's date from EDGAR's acceptance time. Thresholds and signals are unchanged. Decided
before any 2013 or 2014 date was built or scored:

- **Two 10-K vintages.** FY2012 (2008-2012) was accepted 2013-04-01 at 18:19 ET, so it is dated 2013-04-02. EDGAR's
  filing date is also 2013-04-02, because it came in after 17:30; the acceptance time decides, as always. FY2013
  (2009-2013) was accepted 2014-03-31 at 17:21 ET, dated 2014-04-01. The history moves to 2003-2012, then 2004-2013, each
  earlier year from the latest 10-K that reports it. First-year diluted shares: 2003's 1,631M from the FY2005 10-K/A and
  2004's 1,617M from the FY2006 10-K, both already on the post-2006-split basis.
- **No next-quarter outlook in any release of the period.** BASE growth and the growth factor use the fiscal-year sales
  guide (the 2012 rule). Fiscal 2013 guides: sales +4%, +5%, +6%; EBIT margin +60, +65, +75bp; EPS $2.05, $2.10, $2.15.
  Fiscal 2014: sales +5%, +4.5%, +4.5-5%; EBIT margin +65bp, then +70-75bp; EPS $2.60, $2.63, $2.68. A margin guide
  given as a range steps at its midpoint.
- **"Comparable store sales" renamed "comparable sales"** (the FY2012 10-K, then every release from Q1 FY13). The
  definition now reads "location" where it read "store", and the 10-K repeats the earlier years unchanged (2012 +1.4%,
  2011 0.0%, 2010 +1.3%), so the series continues. The signal's label is part of the frozen engine and stays
  "Comparable store sales" (the ACN display-quirk rule: no engine edit without an engine revision).
- **Orchard Supply.** Lowe's acquired most of Orchard Supply Hardware's assets on 2013-08-30: 72 stores, no 8-K. The Q2
  2013 10-Q calls it "not material" and "not included in our fiscal 2013 outlook". From the Q3 FY13 print, store counts
  include these "hardware stores", and the fiscal 2014 store guides name both kinds; they print as given ("15 home
  improvement and 5 hardware stores"). No sales figure is adjusted.
- **Product categories regrouped twice:** 14 plus Other in the FY2012 10-K, 12 plus Other in the FY2013 10-K, prior years
  reclassified each time. The bridge (display only) takes each vintage's own categories, with growth from the same table.
- **One-offs without an adjusted figure stay in** (the Fremont rule): Q4 FY13 impairments ($0.02), Q1 FY14 impairments
  ($0.01) and the Q1 FY14 tax settlement (+$0.04). The settlement is why the fiscal 2014 EPS guide rose to $2.63.
- **Dividends:**
  - $0.18, declared 2013-05-31, from the Q1 2013 10-Q (accepted 2013-06-04 16:50 ET, dated 2013-06-05);
  - $0.23, declared 2014-05-30, from the Q1 2014 10-Q (accepted 2014-06-03 17:16 ET, dated 2014-06-04).
- **Adds nothing:**
  - the 10-Ks' and 10-Qs' outlook sections (they repeat the release guides; the repurchase amounts the guides assume go
    in the cash-return text, as in 2012);
  - the $5 billion repurchase authorizations of 2013-02-01 and 2014-01-31 (cash-return text);
  - the officer and director 8-Ks: 2013-01-24, 2014-03-04, and 2013-11-15, which keeps the $0.18 dividend;
  - the debt-offering and credit-facility 8-Ks;
  - the SEC comment-letter correspondence. It is released only after the review ends, so its filing date is not its
    publication date.
- **Text-only change to 2008-2012:** two source descriptions (the FY2005 10-K/A and the FY2006 10-K) now also cite the
  2003 and 2004 share counts the new vintages use. No number, class or tier changes.

Controls: altering one value of each new print, guide, vintage and dividend changes no date before its publication and
changes the first weekly date after it (20 of 20).

Seen in the build (method behaviour, not tuned):
- **RICH on 86 of 104 dates, AVOID on 68.** The multiple sat high in its own range: 17.3x to 25.7x guided EPS, the 56th to
  100th percentile of a ten-year window that still holds the 11-15x lows of 2007-2012.
- **BASE equals BULL.** From the Q4 FY12 print, BASE growth is +15.3% to +19.6%/yr. It adds three parts: the
  fiscal-year sales guide (+4% to +6%), the guided margin step (+60 to +75bp on a 7.05%, then 7.77%, base) and the
  decade's buybacks (3.9%, then 4.8%/yr). That beats the decade EPS CAGR, so BULL takes BASE's growth (the UNP labelling
  quirk) at the 75th-percentile P/E (18.5-18.9x). The price was above the BULL price on 6 dates (Ratio B `inf`) and near
  it on many more (Ratio B 224x on 2014-12-31).
- **FAIR on 18 dates:** 2013-02-26, the day after the fiscal 2013 guide, and 2014-04-11 to 2014-08-01 ($45-48,
  17.3-18.3x). The tier reads ACCUMULATE on 7 of them (Ratio B 0.95-1.09x), WATCHLIST on 29 dates in all.
- **January-February 2013 still runs on the FY2012 guide** ($1.64): RICH and AVOID at 21.8-23.9x, BASE +8.5%/yr, as in
  late 2012.
- **The BEAR case applies FY2008's -19.9% twice** in both windows, and the EPP floor stays at 13x.

Judgement calls that could carry hindsight: continuing the comp series across the rename; treating the Orchard
acquisition as adding nothing beyond the store counts; dating no fact from the SEC correspondence.

### LOW 2015-2016: adjusted EPS, a guide on two margin bases, RONA, e-commerce on the watch list

```bash
python3 retro/build_low.py --weekly 2015-01-05 2015-12-31                   # 52 dates, 2015-01-09 .. 2015-12-31
python3 retro/build_low.py --weekly 2016-01-04 2016-12-30                   # 52 dates, 2016-01-08 .. 2016-12-30
```

Every 8-K, 8-K/A, 10-Q, 10-K and earnings release of 2015 and 2016 was read by Opus directly. 121 strings were checked
with `verbatim.py`, and 251 structured checks read each print's numbers back from its release's tables and each source's
date from EDGAR's acceptance time. Thresholds and signals are unchanged. Decided before any 2015 or 2016 date was built
or scored:

- **Two 10-K vintages.** FY2014 (2010-2014) was accepted 2015-03-31 at 15:10 ET, during the session, so it is dated that
  day. FY2015 (2011-2015) was accepted 2016-03-28 at 19:07 ET, dated 2016-03-29. The history moves to 2005-2014, then
  2006-2015. First-year diluted shares, both after the 2006 split: 2005's 1,607M from the FY2007 annual report, 2006's
  1,566M from the FY2008 annual report (the 10-K's exhibit 13).
- **The first company-adjusted year.** The Q4 FY15 release (2016-02-24) reports EPS of $2.73. That includes a $530M
  non-cash impairment on leaving the Australian joint venture with Woolworths; the adjusted figure is $3.29. The FY2015
  10-K also states an adjusted EBIT margin of 9.31% (8.41% GAAP; the charge was 90bp of sales and carried no tax
  benefit). By the ACN rule (a company-published figure excluding a one-off replaces GAAP for EPS and margin), FY15 enters
  the history at $3.29 and 9.31%, with the GAAP figures in the notes. Two quarters have a published adjusted EPS: Q4 FY15
  ($0.59, GAAP $0.01) and Q3 FY16 ($0.88, GAAP $0.43). Their prints show it, and their margins add back the charge at the
  share of sales the reconciliation states (4.01%, 2.94%). This is display only, like UNP's Q2 2009.
- **A margin guide on two bases.** The fiscal 2016 guides of the Q4 FY15, Q1 FY16 and Q2 FY16 releases say "Operating
  margin growth excludes the impact of the non-cash impairment charge", so they step from the adjusted 9.31%. The Q3 FY16
  guide (+65bp) "Includes ... the impact of non-cash charges associated with the joint venture with Woolworths in
  Australia (4Q2015 and 3Q2016)", so it steps from the GAAP 8.41%. This is the ACN FY19 restated-base rule. A guide now
  carries it as `fy_margin_guide_base`, and the model's margin comment gives both figures. The fiscal 2016 margin reads
  10.16%, then 9.81%, then 9.06%.
- **Items without an adjusted figure stay in** (the Fremont rule). The RONA foreign-currency hedge (+$0.11 in Q1 FY16,
  -$0.06 in Q2 FY16) was published only as an effect, so those prints are GAAP. The guides keep whatever the company did
  not strip out: the Q1 FY16 guide ($4.11) includes the hedge gain, and the Q3 FY16 guide ($3.52) is GAAP, including the
  hedge gain and the $462M of third-quarter charges. The Q3 FY16 release's adjusted nine-month figures are not
  back-filled into the earlier prints.
- **The impairment 8-K of 2016-01-22** (items 2.06 and 9.01, accepted 11:54 ET during the session) expects a
  fourth-quarter charge but says "the Company is unable to estimate in good faith the amount or range of amounts of the
  impairment charge". The $3.29 guide stands, with the 8-K's words in its note (the 2011-10-17 rule). The 8-K/A of
  2016-02-24, filed after the Q4 release, repeats the release's $530M.
- **RONA.** The acquisition was announced 2016-02-03 (8-K items 1.01 and 7.01, accepted 2016-02-05 at 17:19 ET, dated
  2016-02-08) and closed 2016-05-20 (8-K of 2016-05-24). No 8-K changes a guided number. The Q1 FY16 outlook "excludes
  the impact of the pending RONA acquisition"; the Q2 FY16 release adds it (sales +10%, margin +50bp, EPS $4.06). From
  the Q2 FY16 print, sales, inventory and store counts include RONA, as published.
- **A 53-week year.** Fiscal 2016 ends 2017-02-03. Every fiscal 2016 sales guide includes the 53rd week ("approximately
  1.5 percent"); the published figure stands and the week goes in the note (the 2011 rule).
- **Dividends from the Q2 releases.** From 2015 the Q1 10-Qs no longer report the May declaration, and no 8-K announces
  it. The first filing that states each increase is the Q2 release's cash dividends per share: $0.28 from 2015-08-19 and
  $0.35 from 2016-08-17. This can only lag.
- **ECOMMERCE on the watch list from the FY2015 10-K.** The theme is live from 2015-01-01, its scope (physical retail)
  covers Lowe's, and its market pricing is dated only from 2017-06-16. The FY2013 and FY2014 10-Ks list online retailers
  among many competitors in Item 1. The FY2015 10-K's competition risk factor adds "We face growing competition from
  online and multi-channel retailers who have a similar product or service offering." By the ACN CLOUD rule
  (company-acknowledged, no market read), the theme joins the watch list from that 10-K (2016-03-29) until the next
  10-K's wording replaces it.
  - The class stays DURABLE.
  - The theme signal stays at 2/4.
  - Its factor pair (omni-channel +0.2, online competition -0.2, 10% each) nets to zero.
  - Rebuilding the 40 affected dates without the event changes no number, tier or class.

  The builder encodes this one event kind and still refuses any other.
- **Adds nothing:**
  - the 10-Ks' and 10-Qs' outlook sections (they repeat the release guides; the repurchase assumptions go in the
    cash-return text);
  - the RONA approval 8-K (2016-05-16);
  - the officer, director, bylaw and blackout 8-Ks;
  - the debt offerings;
  - the 401(k) plan amendments filed with the 10-Ks.
- **Text-only change to 2008-2014:** two source descriptions (the FY2007 and FY2008 annual reports) now also cite the
  2005 and 2006 share counts. No number, class or tier changes.
- **ISO weeks:** 2015 has 53, so the 2015 batch covers weeks 2-53 (2014-12-31 covers week 1) and ends on 2015-12-31. The
  2016 batch ends on 2016-12-30, and a 2017 batch starts on 2017-01-02.

Controls: altering one value of each new print, guide, vintage, dividend and the theme event changes no date before its
publication and changes the first weekly date after it (22 of 22).

Seen in the build (method behaviour, not tuned):
- **2015 reads RICH on all 52 dates** (AVOID on 50) at 20.3-27.4x guided EPS, the 85th to 100th percentile of its own
  range. BASE grows +18% to +20%/yr: the sales guide (+4.5-5%), the margin step (8.5-9.5% of EPS) and
  buybacks (4.8%, then 5.5%/yr). The seven January-February dates are still on FY14's guide; four of them have Ratio B
  `inf`.
- **2016 turns with the fiscal 2016 guide and the adjusted base.** From the Q4 FY15 print, EPS of $4.00 and a lower
  price put the multiple at 16.3-21.2x (31st to 81st percentile):
  - FAIR on 33 dates;
  - CHEAP on 11: 2016-02-25, and 2016-09-09 to 2016-11-11 at $66-72;
  - RICH on 8: the seven January-February dates, still on the fiscal 2015 guide, and 2016-12-09.

  The tier reads WATCHLIST 27, ACCUMULATE 16, BUY 5 (October-November) and AVOID 4. BASE grows +19.8% to +22.6%/yr, with
  the sales guide at +6% to +10% (the 53rd week and RONA) and buybacks at 6.0%/yr.
- **The BEAR case still applies FY2008's -19.9% twice**, and the EPP floor moves from 13x to 14x on 2016-09-09.

Judgement calls that could carry hindsight:
- the risk factor as the line for the watch list (Item 1 had listed online retailers among competitors for years);
- taking the company's adjusted FY15, and the two bases of the fiscal 2016 margin guide;
- dating the dividend increases from the Q2 releases.

## Categories change with the era

The five base kinds (DURABLE, CYCLICAL, STRUCTURAL, TURNAROUND, SPECIAL) are
timeless. `AI_EXPOSED` is not: it is the current instance of a recurring
pattern, a franchise that is cheap because the market prices a substitution
story. A retrospective uses the kind `DISRUPTION_EXPOSED` plus the theme live
on its date, and the class names follow the theme:

| theme (label) | live from | first market pricing | class family |
|---|---|---|---|
| GENAI (AI) = today's `AI_EXPOSED` | 2022-11-30 | 2023-05-02 (Chegg) | AI-FEAR BASKET / AI-EXPOSED, … |
| CLOUD | 2012-10-30 (earliest verified 10-K) | 2015-04-23 (AWS disclosed) | CLOUD-FEAR BASKET / … |
| ECOMMERCE (AMAZON) | ~2015 | 2017-06-16 (Whole Foods) | AMAZON-FEAR BASKET / … |
| STREAMING | 2015-08-04 | 2015-08-04 (ESPN subs) | STREAMING-FEAR BASKET / … |
| ENERGY_TRANSITION | 2015-12-12 | 2020-08-31 | TRANSITION-FEAR BASKET / … |
| EV | ~2020 | 2020-12-21 (TSLA in S&P) | EV-FEAR BASKET / … |
| CRYPTO | 2020-10-21 | 2021-04-14 | CRYPTO-FEAR BASKET / … |
| GLP1 (GLP-1) | 2023-08-08 | 2023-08-08 (SELECT) | GLP-1-FEAR BASKET / … |
| OFFSHORE | 2004-11-05 (earliest verified 10-K) | not established | OFFSHORE-FEAR BASKET / … |

What the gates enforce:

- **Before `live_from`.** The theme cannot be assigned, and it cannot even sit on
  the `theme_watch` list. A 2016 analysis that mentions GenAI fails.
- **On or after `live_from`.** The theme still needs dated evidence that the
  market was pricing it *for this company* (`PIT_PROFILE.evidence`). A theme that
  is live but where the stock is priced as a beneficiary stays on `theme_watch`.
  That was ACN in 2023: AI was live, but ACN traded near or above its own median
  multiple, not at an AI discount.
- **Themes that fizzled stay in the registry** (CRYPTO, ENERGY_TRANSITION). A
  registry of only the themes that later mattered would itself be hindsight.
- **What this means by depth.** For shallow dates (late 2025 on), the categories
  are today's, but each ticker's kind must still be re-earned from evidence dated
  by then. For mid-depth dates (2023 to 2024), AI is live but mostly a watch item.
  For deep dates (2016 and earlier), the disruption slot belongs to cloud,
  Amazon, streaming or the energy transition, and `AI_EXPOSED` is illegal.
  IT services in 2008 had their own live theme: offshore delivery. ACN's FY2007 10-K
  names Indian providers "often at highly competitive prices". ACN in January 2008
  carries it on the watch list, not AI.
  From its FY2012 10-K (2012-10-30), ACN also carries CLOUD on the watch list: company-acknowledged,
  no market read. Its earlier 10-Ks mention cloud only as an offering. Its FY2016 10-K (2016-10-31) goes
  further: cloud-based services, artificial intelligence and automation "have reduced and replaced some of our
  historical services and solutions". That changes the quoted wording, not the status: it is still the company's
  own statement, and no dated evidence shows the market pricing it for ACN.
  LOW carries ECOMMERCE on the watch list the same way from its FY2015 10-K (2016-03-29), the first whose risk factors
  name "growing competition from online and multi-channel retailers" ("LOW 2015-2016").

## Workflow

```bash
# 1. add newly published facts to retro/facts/ACN.json (each with source + published date)
python3 retro/build_acn.py --weekly 2023-01-01 2023-06-30        # dates chosen by rule, models generated
python3 retro/build_acn.py --weekly 2008-01-01 2008-01-31        # any era with a history vintage in the fact sheet
python3 retro/build_acn.py --weekly 2008-05-05 2008-09-30        # start a range on a Monday when the prior week is built
python3 retro/build_acn.py --weekly 2008-10-06 2008-12-31
python3 retro/build_acn.py --weekly 2009-01-05 2009-12-31
python3 retro/build_acn.py --weekly 2010-01-04 2010-12-31
python3 retro/build_acn.py --weekly 2011-01-03 2011-12-31
python3 retro/build_acn.py --weekly 2012-01-02 2012-12-31
python3 retro/build_acn.py --weekly 2013-01-07 2014-12-31
python3 retro/build_acn.py --weekly 2015-01-05 2016-12-31
python3 retro/build_acn.py --weekly 2017-01-02 2018-12-31
python3 retro/build_acn.py --weekly 2019-01-07 2020-12-31
python3 retro/build_acn.py --weekly 2021-01-04 2022-12-31        # the 2023 range continues it ("The 2023 pilot, harmonized")
python3 retro/build_acn.py --weekly 2023-07-03 2026-10-23        # last date 2026-10-22 (see "July 2023 to October 2026")
python3 retro/build_acn.py 2008-02-08 2008-02-15 2008-02-22 2008-02-29 2008-03-07 2008-03-14 2008-03-20 \
                           2008-03-28 2008-04-04 2008-04-11 2008-04-18 2008-04-25 2008-04-30   # built by date; include in regressions
for d in archive/retrospective/ACN/2023-*/; do
  python3 retro/retro_tool.py run "$d" && python3 retro/retro_tool.py outcome "$d"
done
python3 retro/retro_tool.py series ACN                           # -> archive/retrospective/ACN/SERIES.md
```

**Picking the weekly dates.** The builder uses one date per ISO week: the last
trading day, except in an earnings week, where it takes the first trading day
*after* the release. The release and the market's reaction are then both in the
information set.

**Scoring a single stock.** One stock's 2-year point return depends on where the
price happened to be that day. ACN entries from January–February 2023 land on the
February 2025 peak; those from April 2023 land after the drop. Judge a series by
`return_to_avg_price_m12_m24_pct` and treat `call_check_2y` as a rough tick. One
stock over a few months mostly tests "buy lower". Testing stock selection needs
many tickers on the same dates.

### Adding dates (the per-year procedure)

Each step exists because skipping it once let something through. Tools are in `retro/tools/`; downloaded
filings go in the session scratchpad, not the repo (every source's URL is in the fact sheet).

1. **List the filings** from `data.sec.gov/submissions/CIK##########.json` (older years are in the paginated
   `filings.files`). Keep `acceptanceDateTime`: it is UTC, and a filing accepted after 16:00 ET counts from the
   next trading day. Read every 8-K in the period (items 2.02, 7.01, 8.01) for guidance changes, not only earnings.
2. **Download** with a generic `User-Agent` (never the owner's email), convert with
   `python3 -I retro/tools/html2rows.py <file.htm>`.
3. **Note the release time** (the conference-call time in the release): before the open or after the close.
4. **Transcribe** prints, the history vintage and 10-K theme events into `retro/facts/ACN.json`. Rules that
   recur: numbers only (a guide restated in words keeps the last numeric range), company figures excluding
   one-offs when published, bookings growth in local currency derived from the FX impact the release states,
   group dollar weights year to date with the latest quarter's LC growth, the ten fiscal years to the latest one.
5. **Check every value word for word** with `python3 -I retro/tools/verbatim.py checklist.json`, each string
   against its own filing.
6. **Regression:** rebuild every earlier range; `git status archive` must show nothing.
7. **Build** the new range (`build_acn.py --weekly START END`; start on the Monday after the last built week),
   then `retro_tool.py run` and `retro_tool.py outcome` on each new date, `retro_tool.py index` and `series ACN`.
8. **Firewall:** commit, then `python3 retro/tools/firewall.py <first day after the range>` must report 0 changes.
   Controls: alter one value of each new print or vintage and check that exactly the dates after its release change.
9. **Scan** the new outputs for years after the as-of date (other than FY labels, SEC accession numbers and the
   `generated` stamp), anachronistic vocabulary, and facts from the next print appearing early.
10. **Commit and push**; report the judgement calls plainly.

**A new ticker** needs its own fact sheet. The engine is generic except for its
signal names and thresholds, so give it a sibling template if the business needs
different signals.

Data sources that worked from the cloud session:

- **Prices and dividends:** the Yahoo chart API (cached in `retro/.cache/`).
- **EPS, revenue and share history with filing dates:** SEC XBRL company facts
  (`data.sec.gov/api/xbrl/companyfacts/CIK##########.json`). SEC asks for a
  `User-Agent` with a contact. Use a project or role address, not a personal one.
- **Quarterly detail:** the 8-K earnings exhibits listed in
  `data.sec.gov/submissions/CIK##########.json`.

## Which model to run it on

Pricing per million tokens, input / output (cached 2026-10-06): Haiku 5.5
$0.10 / $0.50, Sonnet 5.5 $2 / $10, Opus 5.5 $4 / $20, Fable 5.1 $10 / $50.

With the builder, the model's job is to **extend fact sheets**: read a filing,
transcribe dated numbers, cite them. Dates, statistics, scenarios and
classification are code.

- **Sonnet 5.5** (`claude-sonnet-5-5`) at effort `high` is the cheapest model
  that does this reliably.
- **Opus 5.5:** use it to set up a new ticker (choosing signals, era themes and
  evidence) and to review fact sheets.
- **Haiku 5.5:** can do raw extraction if every number is checked against the
  filing.

No model is blind: every current model knows what happened after 2023. The
protection is the dated fact sheet, the frozen rules and the validator, not the
choice of model.
