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
  A distorted latest year (added 2026-10-31 for NKE FY2018; no earlier output changes, so still r2): starting the history and
  the window after it would leave neither, so only the year itself leaves them. Its own days leave the P/E window (labelled
  "10-yr ex-FY18"); EPS growth is measured only between years in the history (BEAR over one-year changes between consecutive
  years, XBULL over two-year runs whose ends are both in it, BULL from the first year to the last); and the rollover rule's last
  full year is the last year in the history. Example: NKE FY2018, whose Tax Act charges ($1,875M and $158M) exceeded the year's
  $1,933M net income.
  A loss even on the company's figure (added 2026-11-05 for XOM FY2020; no earlier output changes, so still r2): a year whose
  company-published EPS without its one-offs is itself a loss has no P/E either, so it is excluded like a loss with no adjusted
  figure (as the latest year, in the way above). Example: XOM FY2020, $(5.25) GAAP and $(0.33) excluding identified items.
- **A listing inside the window** (added 2026-11-01 for AVGO; no earlier output changes, so still r2): a stock's own P/E exists
  only from its first trading day, so the window runs from the listing, up to ten years, and its label counts trading days below
  a year ("22-trading-day"). Example: AVGO, listed 2009-08-06.
- **A history too short to measure a rule** (added 2026-11-01 for AVGO; no earlier output changes, so still r2): the rule's own
  bound stands. No EPS change between two years in the history: BEAR is the 0% cap. No EPS CAGR: BULL is BASE's rate (its "at
  least BASE" floor). No two-year run: XBULL is BULL's rate. One diluted share count: no net buyback. No revenue change: the
  growth factor is 0 and the segment bridge's bull is flat. Rule T takes the annual values the filings report, however few
  (at least two). Example: AVGO in 2009, whose history is FY08 alone (FY06, FY07 and FY09 were losses).
- **A year distorted by one-off benefits** (added 2026-11-01 for AVGO FY2018; no earlier output changes, so still r2): the
  AAPL FY2002 test (listed one-off items larger than the year's net income, so reported EPS is under half the year's EPS
  without them) is written for items that depress a year, and a benefit can never meet it. Its mirror: listed one-off benefits
  larger than the year's income without them (reported EPS more than double the year's EPS without them). Such a year with no
  published figure excluding only them is excluded like a depressed one. Checked before any affected date was built: no year of
  any ticker kept at GAAP has listed one-off benefits over half its net income (UNP 2017 and ACN FY13 use company-adjusted
  figures; the benefits of NKE FY08, FY17, FY22 and FY25, AAPL FY05, UNP 2008 and 2023 and AVGO FY10 are small fractions).
  Example: AVGO FY2018, whose Tax Act and redomiciliation benefits ($8,273M in its 10-K) exceed its $12,629M income from
  continuing operations without them ($4,356M).

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

### LOW 2017-2018: tax reform, the Orchard exit, a guide with and without charges

```bash
python3 retro/build_low.py --weekly 2017-01-02 2017-12-31                   # 52 dates, 2017-01-06 .. 2017-12-29
python3 retro/build_low.py --weekly 2018-01-01 2018-12-31                   # 53 dates, 2018-01-05 .. 2018-12-31
```

Every 8-K, 8-K/A, 10-Q, 10-K and earnings release of 2017 and 2018 was read by Opus directly. 115 strings were checked
with `verbatim.py`, and 278 structured checks read each print's numbers back from its release's tables and each source's
date from EDGAR's acceptance time. Thresholds and signals are unchanged. Decided before any 2017 or 2018 date was built
or scored:

- **Two 10-K vintages.** FY2016 (2007-2016) was accepted 2017-04-04 at 09:27 ET, before the open, so it is dated that
  day. FY2017 (2008-2017) was accepted 2018-04-02 at 16:36 ET, dated 2018-04-03. First-year diluted shares: 2007's
  1,507M from the FY2009 annual report (two-class method) and 2008's 1,468M from the FY2010 annual report (exhibit 13 of
  each 10-K).
- **Adjusted EPS, GAAP margins.** The 10-Ks publish adjusted diluted EPS: $3.99 for FY16 (GAAP $3.47) and $4.39 for FY17
  (GAAP $4.09, excluding the debt loss, the joint venture gain, the Tax Cuts and Jobs Act charge and an hourly bonus). By
  the ACN rule these replace GAAP in the history. Neither 10-K publishes an adjusted margin, so the margins stay GAAP
  (the Fremont rule): FY16 8.99% on both definitions; FY17 9.60% operating margin and 8.92% EBIT margin, which carries
  the 0.68% loss on extinguishment of debt. Each print shows the quarter's adjusted EPS where the release published one,
  with GAAP in the note.
- **The margin guide moves back to operating income.** The Q4 FY16 release guides fiscal 2017 "Earnings before interest
  and taxes as a percentage of sales (operating margin)" (+120bp). From the Q1 FY17 release the guide is "Operating
  income as a percentage of sales (operating margin)", which leaves out the debt loss below operating income. Each guide
  steps from FY16's margin on its own definition; both are 8.99%. The fiscal 2018 guides step from FY17's operating
  margin, 9.60%.
- **The fiscal 2017 guides are GAAP:** EPS $4.64, then $4.30 (lowered "reflective of the loss on extinguishment of debt
  and resulting lower interest expense"), then $4.20-4.30 (adding the gain on the Australian joint venture interest); the
  margin step +120bp, then +80-100bp; sales +5% (52 weeks against fiscal 2016's 53). No adjusted guide was published, so
  the guide keeps both items (the Fremont rule), against FY16's adjusted $3.99.
- **Fiscal 2018: tax reform, the revenue standard, Orchard Supply, store closings.**
  - The Q4 FY17 release (2018-02-28) guides EPS $5.40-5.50 at a 25.5% tax rate, sales +4% and operating margin -30bp.
  - The Q1 FY18 release reflects the new revenue recognition standard: sales +5%, "approximately 1 percent" of it from
    the reclassification, and margin -40bp, "approximately 10 basis points" of it from the same; EPS reaffirmed. Fiscal
    2017 was not restated, so the published figures stand, with the effect in the note (the 2011 rule).
  - The Q2 FY18 release (2018-08-22, items 2.02, 2.05 and 2.06) announces the exit from Orchard Supply Hardware and lowers
    the guide to EPS $4.50-4.60 and margin -180bp. It publishes an adjusted quarter ($2.07, GAAP $1.86). The outlook
    names the Orchard charges in dollars ($230 million recorded, $390 to $475 million to come) but gives no margin or
    EPS figure without them, so the guide includes them (the Fremont rule: no figure is derived from a published
    amount).
  - The 8-K of 2018-11-05 (items 2.05, 2.06 and 7.01, accepted 09:01 ET) closes 20 U.S. stores and 31 Canadian locations:
    "The expected financial impact of today's announcement of $0.28 to $0.34 per diluted share was not contemplated in
    the business outlook for fiscal 2018". It gives no new range, so $4.50-4.60 stands with the words in its note (the
    2011-10-17 rule).
  - The Q3 FY18 release (2018-11-20) gives the guide with and without the charges: GAAP EPS $4.08-4.24, adjusted
    $5.08-5.13; operating margin -240 to -255bp "including 135 to 150 basis points from charges", so -105bp without them.
    By the ACN with-and-without rule the guide takes the adjusted figures from this release on.
- **Dividends from the Q2 releases** (the 2015 rule): $0.41 from 2017-08-23, $0.48 from 2018-08-22.
- **ECOMMERCE stays on the watch list.** The FY2016 10-K repeats the risk factor and puts online sales at "approximately
  3.5% of our total sales". The FY2017 10-K reads "online and omni-channel retailers" and describes Lowes.com orders
  picked up in store, delivered from a store or shipped. Each 10-K's event replaces the previous one. The theme's market
  pricing is dated from 2017-06-16, but that evidence is the sell-off of grocers and food retailers on the Whole Foods
  deal. No filing shows the market pricing the theme for Lowe's, and press coverage is not entered, so the status stays
  "company-acknowledged; no market read" (the ACN CLOUD rule). Rebuilding the 105 dates without the events changes no
  number, tier or class.
- **Adds nothing:**
  - the 10-Qs, which no longer restate the outlook, and the 10-Ks, which have no outlook section (the cash-return text
    takes the repurchases and the remaining authorization);
  - the investor-day 8-K of 2018-12-12, which reiterates the fiscal 2018 ranges. Its first fiscal 2019 guide matters only
    from fiscal 2019 and is left for a 2019 batch (the 2008 rule);
  - the management and director 8-Ks (among them a new chief executive, named 2018-05-22), the bylaw changes and the
    proxy materials;
  - the debt tender offer and debt 8-Ks of April-May 2017 and the credit agreement of 2018-09-12. They reach the facts only
    through the published debt loss.
- **Text-only change to 2008-2016:** two source descriptions (the FY2009 and FY2010 annual reports) now also cite the 2007
  and 2008 share counts. 353 dates change only in that text.
- **ISO weeks:** 2018-12-31 covers week 1 of 2019, so a 2019 batch starts on 2019-01-07.

Controls: altering one value of each new print, guide, vintage, dividend and theme event changes no date before its
publication and changes the first weekly date after it (23 of 23).

Seen in the build (method behaviour, not tuned):
- **2017 turns CHEAP on the fiscal 2017 guide.**
  - January-February, still on the fiscal 2016 guide ($3.52, GAAP), reads FAIR on 5 dates and RICH on 3 at 20.2-21.8x (the
    72nd-86th percentile).
  - From the Q4 FY16 print, $4.64 and a +120bp margin step (11.8% of EPS) give BASE +22.7%/yr at 17.3-18.5x (46th-65th
    percentile): CHEAP on all 12 dates to 2017-05-19. After the cut to $4.30, CHEAP on 12 of 13.
  - From the Q2 FY17 print BASE is +20.2%/yr. As the price rose from $73 to $93 the class went FAIR (from 2017-09-08), then
    RICH (2017-10-13, and December at 19.8-21.9x).

  In all: CHEAP 26, FAIR 17, RICH 9; BUY 15, ACCUMULATE 25, WATCHLIST 11, AVOID 1.
- **2018 reads RICH on 47 of 53 dates.**
  - January-February, still on the fiscal 2017 guide: 22.3-25.3x (the 92nd-100th percentile), RICH and AVOID on all 8.
  - The fiscal 2018 guide's tax rate lifts EPS to $5.45 and puts the stock at 15.3-16.2x (the 13th-22nd percentile). But
    its -30bp step takes 3.2% off EPS growth, so BASE is +6.8-7.2%/yr. The tier reads BUY on 8 of 12 dates (Ratio B
    0.55-0.73) and ACCUMULATE on 4 (0.88-0.92). The class reads CHEAP on 5, FAIR on 1 and RICH on 6, because the adjusted gap stays negative (-0.33 to
    -0.62).
  - From the Q1 FY18 print ($96-101, 17.5-18.5x): RICH on all 13.
  - **The Orchard charges, carried twice.** The Q2 FY18 guide's -180bp step on a 7.8% margin is -23.1% of EPS. Method r2
    carries it as growth for two years: BASE -12.2%/yr, a BASE price of $64-65 against a stock at $93-117, Ratio B 1.83x
    to 61x. All 13 dates read RICH and AVOID. The adjusted Q3 FY18 guide (-105bp) brings BASE to -1.9%/yr: RICH on all
    7, ACCUMULATE 5, WATCHLIST 2.
  - The 8-K of 2018-11-05 changes no number, only the guide's note.
- **BULL separates from BASE** for the first time since 2012-02-24. From the Q4 FY17 print BASE sits below the decade
  EPS CAGR, so BULL takes the CAGR: +9.0%/yr, then +12.8%/yr from the FY2017 vintage.
- **The BEAR case** applies FY2008's -19.9% until the FY2017 vintage, then FY2009's -18.8% (FY2008's fall needs FY2007,
  which leaves the window). The EPP floor moves from 14x to 15x on 2018-01-05.

Judgement calls that could carry hindsight:
- keeping the GAAP guides (fiscal 2017 with the debt loss, the Q2 FY18 guide with the Orchard charges) against adjusted
  history years, and taking the adjusted guide from the Q3 FY18 release;
- not converting the Q2 FY18 outlook's dollar charges into a margin step without them;
- keeping the theme on the watch list after its 2017-06-16 market-pricing date;
- leaving the fiscal 2019 outlook of 2018-12-12 to the 2019 batch.

### LOW 2019-2020: adjusted guides, Q4 releases without a full-year EPS, a withdrawn guide

```bash
python3 retro/build_low.py --weekly 2019-01-07 2019-12-31                   # 52 dates, 2019-01-11 .. 2019-12-31
python3 retro/build_low.py --weekly 2020-01-06 2020-12-31                   # 52 dates, 2020-01-10 .. 2020-12-31
```

Every 8-K, 8-K/A, 10-Q, 10-K and earnings release from 2018-12-06 to the end of 2020 was read directly, with the 10-Qs
searched in full for forward-looking statements. That includes the analyst-conference 8-K of 2018-12-12, which the
2017-2018 batch left for this one. 166 strings were checked with `verbatim.py`, and 299 structured checks read each
print's numbers back from its release's tables, each vintage's from its 10-K and each source's date from EDGAR's
acceptance time. Thresholds and signals are unchanged. Decided before any 2019 or 2020 date was built or scored:

- **Two 10-K vintages.** FY2018 (2014-2018) was accepted 2019-04-01 at 19:26 ET, dated 2019-04-02; FY2019 (2015-2019)
  2020-03-23 at 17:05 ET, dated 2020-03-24. The history moves to 2009-2018, then 2010-2019. First-year diluted shares:
  2009's 1,464M from the FY2011 10-K and 2010's 1,403M from the FY2012 10-K. The 10-Ks publish adjusted diluted EPS of
  $5.11 for FY18 (GAAP $2.84) and $5.74 for FY19 (GAAP $5.49); by the ACN rule these replace GAAP. 2015-2017 keep the
  adjusted figures of the earlier 10-Ks.
- **Q4 releases without a full-year adjusted EPS.** The Q4 FY18 (2019-02-27) and Q4 FY19 (2020-02-26) releases publish
  adjusted EPS for the quarter and an adjusted operating margin for the year (8.56%, 9.13%), but no adjusted EPS and no
  comparable sales for the year. By the Fremont rule (UNP's "when an adjusted figure first appears"), FY18 enters the
  history at GAAP $2.84 from its Q4 print until the 10-K, and FY19 at $5.49; nothing is summed from the quarters. The
  year's adjusted operating margin is published, so the history takes it. The franchise line says the release gives no
  full-year comp until the 10-K supplies it (a builder change, text only: every earlier Q4 release gave one).
- **Guides with and without items** (the Q3 FY18 rule). From the Q4 FY18 release every outlook gives the operating
  margin step on both bases, and from Q1 FY19 both EPS figures. The guide takes the adjusted ones, stepped from the
  adjusted margin the company states. Fiscal 2019: +85 to +95bp, then +20 to +50bp, then +40 to +60bp from 8.56%; EPS
  $6.00-6.10 (no adjustment was then expected), $5.45-5.65 (excluding the Mexico tax benefit), $5.63-5.70. Fiscal 2020:
  +50 to +70bp from 9.13%, EPS $6.45-6.65. The GAAP figures are in the notes.
- **The conference outlook of 2018-12-12** (accepted 11:35 ET, during the session) is fiscal 2019's first guide (the
  2009 rule). Its margin step, +235 to +250bp against the fiscal 2018 outlook including 135 to 150bp from the absent 2018
  charges, is +100bp without them, as in the Q3 FY18 encoding. The Q4 FY18 release replaces every field on the day fiscal
  2019 becomes current, so the 8-K shows only in the guide's document list.
- **A withdrawn guide.** The Q1 FY20 release (2020-05-20): "The Company is withdrawing its financial guidance for fiscal
  year 2020." That is not a guide restated in words, which keeps the last numeric range (the ACN Q3 FY08 rule): it says
  no range stands. So a guide marked withdrawn voids every earlier guide for its year, and the no-guide rules apply
  (a builder change; no earlier guide is a withdrawal, so no earlier date changes):
  - FY19's adjusted $5.74 stands as the current-year EPS;
  - BASE growth and the growth factor take the latest quarter's sales growth (+10.9%, then +30.1% and +28.3%);
  - there is no margin step, and the margin signal takes the latest quarter's change.

  The Q2 FY20 release repeats the withdrawal. The Q3 FY20 release (2020-11-18) gives a fourth-quarter outlook only: sales
  +15 to +20% (BASE growth uses it, the next-quarter rule), comps, EPS $1.10-1.20 (shown in the guide line), and an
  adjusted margin "essentially flat" (a quarter's margin, no field). The investor-update 8-K of 2020-12-09 (before the
  open) restores a fiscal 2020 guide: adjusted EPS $8.62-8.72 (GAAP $7.53-7.63), sales about +22%, comps about +23%,
  adjusted margin +170bp from 9.13%.
- **Published adjusted quarter margins replace GAAP in the prints.** This is LOW's setup rule (a company-published figure
  excluding an item replaces the reported one), as in the Q4 FY15 and Q3 FY16 prints. Only the Q4 infographics (exhibit
  99.2) publish them:
  - Q4 FY18: adjusted operating margin 6.44% against 7.50% (-106bp; GAAP -1,071bp);
  - Q4 FY19: adjusted gross margin 31.89% against 31.49% (+40bp; GAAP -22bp) and operating margin 7.15% against 6.45%.

  So the gross-margin signal reads +40bp for Q4 FY19. Every other quarter, and every annual gross margin, comes from the
  percent-of-sales columns.
- **Shipping and handling costs move into cost of sales** from the Q4 FY18 release, prior periods recast; operating income
  is unchanged. Each print's gross margin change is measured against the recast prior-year quarter its release prints
  (the ACN restated-base rule).
- **One-offs without an adjusted figure stay in the GAAP lines** (the Fremont rule), and each print shows the quarter's
  adjusted EPS the release publishes: the Canadian goodwill impairment and the strategic-reassessment charges (Q4 FY18),
  the Mexico exit (2019), the Canadian restructuring (Q3 FY19 into 2020), and the $1.06B loss on extinguishment of debt
  (Q3 FY20, which the EBIT margin carries and the operating margin the guides use does not).
- **Dividends,** each from the first filing that states it: $0.55 from the Q2 2019 release (2019-08-21) and $0.60 from the
  Q3 2020 release (2020-11-18). The 2020 increase was declared in the third quarter; the Q2 2020 release still shows $0.55.
- **ECOMMERCE stays on the watch list.** The FY2018 and FY2019 10-Ks keep the risk factor and add a sentence on online and
  omni-channel retailers' delivery services; the quote now carries the risk factor's three sentences on online rivals.
  Lowes.com sales growth in 2020 (+80%, +135%, +106% by quarter) is the company's own channel, not evidence that the market
  prices substitution of its stores. No filing shows that, so the status stays company-acknowledged (the ACN CLOUD rule).
- **COVID enters only through the prints and the withdrawal.** The FY2019 10-K names it as a risk factor and a subsequent
  event, with no estimate: a caveat without a figure adds nothing (the UNP 2020 rule). The registry has no COVID theme.
- **The franchise text is unchanged.** From the FY2018 10-K the sentence reads "driven by the activity level of home
  improvement projects"; housing turnover moves to the indicators the 10-K says it monitors. The "why" keeps its wording,
  a constant of the method (the UNP rule), with each vintage's store count, footprint and countries.
- **Adds nothing:**
  - the 8-K/A of 2019-11-20 (a column date in the reconciliation);
  - the 10-Qs (no outlook beyond repurchase plans);
  - the repurchase authorizations ($10 billion on 2018-12-12, $15 billion on 2020-12-09), the suspension in the first
    quarter of 2020 and the restart 8-K of 2020-09-29 (cash-return text);
  - the guides' operating-income growth, leverage-ratio, repurchase and capital-expenditure items (no field);
  - the long-term targets and 2021 scenarios of the 2020-12-09 webcast (not in the filing);
  - the officer, director, bylaw and vote 8-Ks, the credit facilities, the debt offerings and the tender offer.
- **Text-only change to 2008-2018:** two source descriptions (the FY2011 and FY2012 10-Ks) now also cite the 2009 and 2010
  share counts. 353 dates change only in that text.
- **ISO weeks:** 2019-12-31 covers week 1 of 2020, so the 2020 batch starts on 2020-01-06; 2020 has 53 ISO weeks and its
  batch ends on 2020-12-31. A 2021 batch starts on 2021-01-04.

Controls: altering one value of each new print, guide, vintage, dividend and theme event changes no date before its
publication and changes the first weekly date after it (23 of 23). The conference guide of 2018-12-12 first shows on
2019-02-28, the first date with fiscal 2019 current.

Seen in the build (method behaviour, not tuned):
- **2019: the margin guide and FY18's GAAP weeks.**
  - January-February, still on the adjusted fiscal 2018 guide ($5.105, BASE -1.9%/yr): RICH on all 7 dates, WATCHLIST
    then AVOID.
  - From the Q4 FY18 print the +90bp adjusted step and buybacks put BASE at +17.6%/yr. On the five dates to 2019-03-29
    FY18 sits in the history at GAAP $2.84, so BEAR applies -35.3% twice: FAIR 3, CHEAP 2, all ACCUMULATE.
  - From the FY2018 vintage the worst year of 2009-2018 is +0.7% (2011), so BEAR is flat EPS on every later date and
    Ratio B runs 0.08-0.77x: BUY on 37 of the 40 dates from 2019-04-05, ACCUMULATE on the last three (0.75-0.77x).
    CHEAP on the 7 dates to the Q1 print (17.6-19.2x).
  - After the Q1 FY19 cut ($5.55, +35bp, BASE +12.7%/yr): CHEAP on 11 of 13 dates to mid-August at 16.8-19.4x. The Q2
    print (gross margin -85bp, sales +0.5%) lowers the proxy composite from 1.80 to 1.65: RICH from 2019-08-22 to
    2019-11-15 at 19.4-20.8x (the 66th-80th percentile). The Q3 print (gross margin +156bp) lifts it to 2.40: CHEAP on 3
    dates, FAIR on 1, then RICH at 21.1-21.2x.

  In all: CHEAP 23, FAIR 5, RICH 24; BUY 37, ACCUMULATE 8, WATCHLIST 5, AVOID 2.
- **2020: the crash on the February guide, then the fallback.**
  - January-February, on the raised fiscal 2019 guide ($5.67, BASE +14.3%/yr): RICH on 6 of 7 dates at 21.2-22.1x,
    CHEAP on 2020-01-31 at 20.5x.
  - On the fiscal 2020 guide ($6.55, BASE +15.4%, then +15.7%/yr) CHEAP and BUY on all 12 dates from 2020-02-27 to
    2020-05-15, at 10.1-17.4x; on 2020-03-20 the price ($66.36) is under the BEAR price.
  - From the withdrawal, FY19's $5.74 and the latest quarter's sales growth set BASE at +17.7%, then +36.9%/yr, while the
    multiple on that EPS climbs to 21-31x (the 81st-100th percentile). CHEAP on 2020-05-21, then FAIR or RICH on most
    dates; CHEAP on 7 between 2020-08-20 and 2020-11-13, where the proxy composite (3.70: comps, sales, inventory and both
    margins at XBULL) and BASE outweigh the multiple.
  - The fourth-quarter guide (+17.5% sales) brings BASE to +24.3%/yr: FAIR, RICH, FAIR.
  - The 2020-12-09 guide ($8.67, +170bp) puts the multiple at 18.2-18.8x and BASE at +40.0%/yr, the margin step carried as
    growth for two years (the 2018 Orchard pattern in reverse): CHEAP and BUY on the last four dates.

  In all: CHEAP 25, FAIR 13, RICH 14; BUY 18, ACCUMULATE 13, WATCHLIST 14, AVOID 7.
- **How far each call moves the classes** (the affected dates rebuilt with one encoding changed; no outcome consulted):
  - keeping the withdrawn February guide would change 26 of the 29 classes from 2020-05-21 to 2020-12-04;
  - taking the 10-K's adjusted EPS from the Q4 prints would change the class on 3 and the tier on 4 of the 5 dates of
    early 2019, and nothing in 2020;
  - a GAAP gross margin for Q4 FY19 would change none.
- **The EPP floor stays at 15-16x,** and the P/E median of the window at 18.3-18.8x.

Judgement calls that could carry hindsight:
- treating the withdrawal as voiding the earlier guides (the call that moves the most classes);
- keeping FY18 and FY19 at GAAP between the Q4 print and the 10-K;
- the published adjusted quarter margins in the prints (no class changes in 2019-2020);
- extending the online-competition quote to the new delivery sentence (text only).

### LOW 2021-2023: sales guides in dollars, a year without an EPS guide, the Canadian sale

```bash
python3 retro/build_low.py --weekly 2021-01-04 2021-12-31                   # 52 dates, 2021-01-08 .. 2021-12-31
python3 retro/build_low.py --weekly 2022-01-03 2022-12-31                   # 52 dates, 2022-01-07 .. 2022-12-30
python3 retro/build_low.py --weekly 2023-01-02 2023-12-31                   # 52 dates, 2023-01-06 .. 2023-12-29
```

Every 8-K, 10-Q, 10-K and earnings release from 2020-12-10 to the end of 2023 was read directly, with the 10-Qs searched
in full for forward-looking statements. 253 strings were checked with `verbatim.py`, and 645 structured checks read each
print's numbers back from its release's tables, each vintage's from its 10-K and each source's date from EDGAR's
acceptance time. Thresholds and signals are unchanged. Decided before any 2021-2023 date was built or scored:

- **Three 10-K vintages.** FY2020 (accepted 2021-03-22 at 17:06 ET, dated 2021-03-23; five-year selected data 2016-2020),
  FY2021 (2022-03-21 at 16:47 ET, dated 2022-03-22) and FY2022 (2023-03-27 at 16:46 ET, dated 2023-03-28). From the FY2021
  10-K Item 6 is reserved, so each vintage takes its three income-statement years and every earlier year from the latest
  10-K that reports it (the ACN FY21 rule). The history moves to 2011-2020, 2012-2021, then 2013-2022.
  - First-year diluted shares: 2011's 1,273M (FY2013 10-K), 2012's 1,152M (FY2014 10-K), 2013's 1,061M (FY2015 10-K).
  - FY20 is the company's adjusted $8.86 (GAAP $7.75, excluding the $1.1 billion loss on extinguishment of debt and the
    Canada restructuring). FY21 has no adjustment ($12.04). FY22 is the adjusted $13.81 (GAAP $10.17, excluding the
    Canadian retail business impairment and transaction costs).
  - The FY2020 10-K recasts comparable sales to a transacted basis (2018 2.2%, 2019 2.6%). Only the latest year's comp is
    shown, so nothing else moves.
- **What each Q4 release publishes for its year.**
  - Q4 FY20: the adjusted EPS ($8.86), so FY20 enters the history at it from the print. No adjusted operating margin for
    the year, so the margin stays GAAP (10.77%, the Fremont rule), and no full-year comp (the 10-K's 26.1% follows).
  - Q4 FY21: no adjustments, and the year's comp in the chief executive's quote (6.9%).
  - Q4 FY22: the adjusted EPS ($13.81) and adjusted operating margin (13.04%) in the 8-K's reconciliation (exhibit 99.2),
    so FY22 enters at them from the print. No full-year comp and no store count. The franchise line now says when a Q4
    release gives no store count (a builder change, text only; every earlier Q4 release gave one).
- **Fiscal 2021: guided in levels, never in EPS.**
  - The Q4 FY20 release gives words only. It reiterates the 2021 "scenarios" of the December 2020 Investor Update, which
    no filing states (the 2019-2020 rule), and expects further market share gains and operating margin improvement. So
    FY20's $8.86 stands as the current-year EPS, BASE growth and the growth factor take the latest quarter's sales growth
    (+26.7%), and there is no margin step. The guide line shows the release's words; it is the first LOW date to show them.
  - The Q1 FY21 release expects "the achievement of a 12% operating margin" for the fiscal year. That is a numeric level,
    so a guide (the 2009 level-form rule; UNP read "a 55.X% operating ratio" the same way). Its sales statement, "tracking
    ahead of" the Robust Market scenario's $86 billion, is a one-sided bound and gives no sales field, so BASE growth
    takes the Q1 quarter's +24.1%.
  - The Q2 and Q3 FY21 releases guide "Revenue of approximately $92 billion", then $95 billion, and an operating margin of
    12.2%, then 12.4%. No EPS figure all year: FY20's $8.86 stands to the Q4 FY21 print.
- **A sales guide in dollars** (a builder change). From fiscal 2021 every sales guide is a dollar level (`rev_guide_usd_b`).
  It is read as growth against the previous fiscal year's net sales in the history, the year the guide compares with,
  rounded to 0.1: $92 billion is +2.7% on FY20's $89.60B. The guide line shows both. No earlier guide has the field, so
  no earlier date changes. Catalyst (3) now says when a year is guided in numbers but never in EPS (text only).
- **Fiscal 2022: a 53-week year and the Canadian sale.**
  - The first fiscal 2022 outlook is in the 8-K of 2021-12-15 (before the open): sales $94-97 billion, operating margin
    12.5-12.8%, EPS $12.25-13.00. By the 2009 rule it is a guide for fiscal 2022. The Q4 FY21 release replaces every field
    on the day fiscal 2022 becomes current, so the 8-K shows only in the guide's document list and the EPS note ("raised
    from $12.25-13.00"). Its restatement of the fiscal 2021 outlook adds nothing.
  - The Q4 FY21 release guides sales of $97-99 billion including the 53rd week (about $1.0-1.5 billion, in the note: the
    2011 rule), comps -1% to +1%, an operating margin of 12.8-13.0%, tax about 25% and EPS $13.10-13.60. The Q1 FY22
    release affirms it. The Q2 FY22 release keeps the ranges with words ("toward the bottom end" for sales, "toward the top
    end" for operating income and EPS): the ranges stand and the words go in the notes (the ACN Q3 FY08 rule).
  - The 8-K of 2022-11-03 (after the close, dated 2022-11-04) announces the sale of the Canadian retail business and a
    pre-tax impairment of about $2.0 billion. It reaffirms the outlook "exclusive of the asset impairment" with no new
    figure, so the range stands with its words in the note (the 2011-10-17 rule).
  - The Q3 FY22 release guides on adjusted measures only, excluding the impairment and transaction costs: sales about
    $97-98 billion, an adjusted operating margin of 13.0%, adjusted EPS $13.65-13.80. No GAAP figure is published, so the
    guide takes them (the Q3 FY18 rule). The conference 8-K of 2022-12-07 repeats these ranges and adds nothing; its 2023
    scenarios are not in the filing.
- **Fiscal 2023.**
  - The Q4 FY22 release guides on GAAP: sales about $88-90 billion, comps flat to -2%, an operating margin of 13.6-13.8%,
    EPS $13.60-14.00.
  - From Q1 FY23 the guides are adjusted, excluding the gain on the Canadian sale: $87-89 billion, 13.4-13.6%,
    $13.20-13.60 (affirmed in Q2), then about $86 billion, about 13.3% and about $13.00 (Q3).
  - The sales levels compare with fiscal 2022 as reported: a 53-week year that still included the Canadian business. So
    BASE growth reads -7.3% to -11.4% while the comps guides read flat to -5%. The published range stands (the 2011
    rule); no comparable-basis sales figure was published.
- **Level-form margin guides step from the history's margin**, as in 2009: fiscal 2021 from FY20's GAAP 10.77% (+123bp to
  +163bp), fiscal 2022 from FY21's 12.56%, fiscal 2023 from FY22's adjusted 13.04% (the GAAP level of the Q4 FY22 guide
  included).
- **Published adjusted quarter margins replace GAAP in the prints** (the LOW setup rule). EBIT margin stays GAAP.
  - Q4 FY20: gross margin 31.80% (-9bp; GAAP +70bp) and operating margin 7.56% (+41bp; GAAP +152bp).
  - Q3 FY22: operating margin 12.71% (+54bp; GAAP -824bp).
  - Q4 FY22: 9.55% (+88bp; GAAP -108bp).
  - Q1 FY23: 14.43% (+47bp; GAAP +75bp).
  - Q3 FY23 has no adjustment of its own. Its change is measured against the prior year's adjusted 12.71% (+46bp, as
    published; GAAP +924bp): the UNP rule for the base a release names.
- **Dividends,** each from its Q2 release (the 2015 rule; the Q1 10-Qs report only the old rate): $0.80 (2021-08-18), $1.05
  (2022-08-17), $1.10 (2023-08-22).
- **ECOMMERCE stays on the watch list.** The FY2020-FY2022 10-Ks keep the risk factor; from FY2021 it reads "online and
  omnichannel retailers" and its third sentence adds same-day and next-day delivery and pick-up options. No filing shows the
  market pricing online substitution of Lowe's stores, so the status stays company-acknowledged (the ACN CLOUD rule).
  GENAI's registry scope does not cover a home-improvement retailer, and these 10-Ks do not mention artificial intelligence.
- **Adds nothing:**
  - the CFO-appointment 8-K of 2022-04-08 (after the close), which reaffirms the outlook without numbers (its 35% dividend
    payout target has no field);
  - the 10-Qs (capital expenditure and repurchase plans only);
  - the repurchase authorizations ($13 billion on 2021-12-15, $15 billion on 2022-12-07) and repurchase plans (cash-return
    text);
  - the guides' interest-expense, depreciation, ROIC, repurchase and capital-expenditure items, the gross-margin words and
    the two-year comp stacks (no field);
  - the debt offerings and credit agreements; the bylaw, officer, director, vote and blackout 8-Ks; the proxy materials;
  - the SEC comment-letter correspondence (released after the review ends).
- **Text-only change to 2008-2020:** three source descriptions (the FY2013, FY2014 and FY2015 10-Ks) now also cite the
  2011-2013 share counts. 353 dates change only in that text.
- **ISO weeks:** each year's batch runs from its week 1 (2021-01-04, 2022-01-03, 2023-01-02) to its last trading day in
  week 52. A 2024 batch starts on 2024-01-01.

Controls: altering one value of each new print, guide, vintage, dividend and theme event changes no date before its
publication and changes the first weekly date after it (34 of 34). The fiscal 2022 outlook of 2021-12-15 first shows on
2022-02-24, the first date with fiscal 2022 current.

Seen in the build (method behaviour, not tuned):
- **2021: the fallback, then the EPS anchor.**
  - January-February, on the restored fiscal 2020 guide ($8.67) and the Q4 FY20 sales guide (+15-20%): CHEAP and BUY on
    all 7 dates at 19.0-20.5x.
  - From the Q4 FY20 print FY20's $8.86 stands. The latest quarter's +26.7%, then Q1 FY21's +24.1% with the 12% margin
    step, put BASE at 32.8%, then 40.4%/yr. CHEAP and BUY on all 25 dates to 2021-08-13, while the price rose from $158.52
    to $208.40 and the multiple on $8.86 reached the 98th percentile of its own range.
  - The dollar guides bring BASE to 20.5%, then 25.2%/yr, while the price keeps rising on the same $8.86 (22.9-29.5x, the
    95th-100th percentile): RICH on all 20 dates from 2021-08-19.

  In all: CHEAP 32, RICH 20; BUY 32, ACCUMULATE 8, WATCHLIST 2, AVOID 10.
- **2022: CHEAP on the fiscal 2022 guide.**
  - The seven January-February dates are still on the fiscal 2021 guides and $8.86 (25.1-28.3x): RICH.
  - From the Q4 FY21 print the guided $13.35 puts the stock at 12.9-17.7x (the 2nd-31st percentile) and BASE at about
    10%/yr: CHEAP and BUY on all 45 dates.
  - The BEAR case is flat EPS at the 10th-percentile multiple (no year of the decade's history fell), so the BEAR price
    ($200-215) sits near the price, and Ratio B runs from -0.15 to 0.11.

  In all: CHEAP 45, RICH 7; BUY 45, WATCHLIST 4, AVOID 2, ACCUMULATE 1.
- **2023: a sales base with the Canadian business.** The fiscal 2023 sales guides read -8.3%, -9.4% and -11.4% at their
  midpoints, so BASE runs from +2.7% to -3.5%/yr (a negative BASE prints as "EPS +-3.5%/yr", the old sign quirk). The
  multiple (13.7-17.5x, the 5th-39th percentile) still keeps the class CHEAP on 46 dates. It reads FAIR on 2023-07-14 and
  RICH on 2023-07-21, 2023-07-28 and the last three December dates, at 17.1-17.5x. Ratio B stays between -0.06 and 0.22, so
  the tier reads BUY on all 52.

  In all: CHEAP 46, FAIR 1, RICH 5; BUY 52.
- **How far each call moves the classes** (the 156 dates rebuilt with one encoding changed; no outcome consulted):
  - reading the $86 billion scenario as the Q1 FY21 sales guide would change 1 class and 1 tier (2021-07-23: CHEAP to
    FAIR, BUY to ACCUMULATE);
  - not reading dollar levels as sales guides (the latest quarter's sales growth instead) would change 2 classes (2023-07-14
    and 2023-07-21) and 2 tiers (2022-01-28 and 2022-02-18);
  - not reading the 12% as a guide, stepping the GAAP fiscal 2023 guide from FY22's GAAP margin, keeping FY22 at GAAP from
    the Q4 print, using GAAP quarter margins, or reading "bottom end" and "top end" as numbers would change none.
- **The EPP floor is 16x, then 15x.** BULL is the decade EPS CAGR (22.5% to 24.4%/yr), or BASE where that is higher.
  XBULL is the best two-year run, or BULL where that is higher: 2018-2020 (31.7%/yr), then 2019-2021 (44.8%/yr) from the
  Q4 FY21 print.

Judgement calls that could carry hindsight:
- reading "the achievement of a 12% operating margin" as a guide, and "tracking ahead of" the $86 billion scenario as no
  sales figure;
- reading dollar sales levels as growth against the previous year's reported sales, including fiscal 2023's comparison
  with a 53-week year that included the Canadian business;
- taking FY22's adjusted EPS and margin from the reconciliation exhibit of the Q4 FY22 8-K;
- showing the chief executive's "Looking ahead to 2021" sentence as the Q4 FY20 release's words (text only).

### LOW 2024-2026: guides on both bases, the ADG and FBM acquisitions, a year guided in growth

```bash
python3 retro/build_low.py --weekly 2024-01-01 2024-12-29                   # 52 dates, 2024-01-05 .. 2024-12-27
python3 retro/build_low.py --weekly 2024-12-30 2025-12-28                   # 52 dates, 2025-01-03 .. 2025-12-26
python3 retro/build_low.py --weekly 2025-12-29 2026-10-23                   # 43 dates, 2026-01-02 .. 2026-10-23
```

Every 8-K, 8-K/A, 10-Q, 10-K and earnings release from 2023-11-22 to 2026-10-23 was read directly, with the 10-Qs
searched in full for forward-looking statements. Independent reader agents read the same filings again in four groups,
and a checker agent re-read each group's filings against its reader. Every number matched. The two groups finished
before the build commit (the FY2023 close to the FY2024 10-K) changed two wordings (the buybacks as paid, the published
FY24 adjusted margin changes). The rest changed text only, committed separately before any date was scored: the fiscal
2026 guide notes name what their adjusted figures exclude (the acquisitions' intangible amortization, not all their
costs), the Q2 FY24 note calls the guide it lowered GAAP, and the bonuses read as announced. 48 dates (13 in 2024, 35 in
2026) change only in that text. Two checker claims did not hold: that the FY2023 10-K has no product-category table (it
has one, the source of the FY23 groups), and that the 10-Ks from FY2023 no longer tie sales to housing turnover (each
still lists decreasing housing turnover among the factors that may hurt results, as the FY2020-FY2022 10-Ks did, so the
profile's wording stays). 314 strings were checked with `verbatim.py`, and 799 structured checks read each print's
numbers back from its release's tables, each vintage's from its 10-K and each source's date from EDGAR's acceptance
time. Thresholds and signals are unchanged. The encodings below were decided before any 2024-2026 date was built; no
outcome was computed until the build and these corrections were committed.

- **Three 10-K vintages.** FY2023 (accepted 2024-03-25 at 16:18 ET, dated 2024-03-26), FY2024 (2025-03-24 at 16:33 ET,
  dated 2025-03-25) and FY2025 (2026-03-23 at 16:52 ET, dated 2026-03-24). Each takes its three income-statement years and
  every earlier year from the latest 10-K that reports it. The history moves to 2014-2023, 2015-2024, then 2016-2025.
  - First-year diluted shares: 2014's 990M (FY2016 10-K), 2015's 929M (FY2017 10-K), 2016's 881M (FY2018 10-K).
  - FY23 is the company's adjusted $13.09 (GAAP $13.20, excluding the $63 million gain on the Canadian sale), FY24 the
    adjusted $11.99 (GAAP $12.23, excluding $177 million of such gains) and FY25 the adjusted $12.28 (GAAP $11.85, excluding
    $321 million of ADG and FBM acquisition costs). FY22 keeps its adjusted $13.81, which the FY2024 10-K no longer
    reconciles: an adjusted year keeps its figure (the 2019-2020 rule for 2015-2017).
- **What each Q4 8-K publishes for its year.** The reconciliation in exhibit 99.2 gives the year's adjusted EPS and adjusted
  operating margin (13.31%, 12.30%, 12.11%), so each year enters the history at them from the print (FY22's rule). The
  infographic prints the year's comparable sales (-4.7%, -2.7%, +0.2%, the 10-Ks' figures), so they show from the print too
  (text only; FY22's infographic gave only a U.S. comp, so FY22 waited for the 10-K). Q4 FY25 also publishes the year's
  adjusted gross margin, 33.54% (display only).
- **Fiscal 2024 and fiscal 2025: GAAP guides, then adjusted ones.**
  - The Q4 FY23 release guides fiscal 2024 on GAAP: sales $84-85 billion, comps -2% to -3%, operating margin 12.6-12.7%,
    EPS $12.00-12.30. The Q1 FY24 release affirms it.
  - From the Q2 FY24 release the guide excludes the gains on the Canadian sale and gives no GAAP figure, so it takes the
    adjusted figures (the Q3 FY18 rule): $82.7-83.2 billion, 12.4-12.5%, EPS $11.70-11.90; then $83.0-83.5 billion,
    12.3-12.4% and $11.80-11.90 (Q3).
  - The investor-conference 8-K of 2024-12-11 (before the open) affirms the fiscal 2024 ranges. Its fiscal 2025 scenarios
    and long-term targets are in the presentation, not the filing (the 2020-12-09 and 2022-12-07 rule): it adds nothing.
  - The Q4 FY24 release guides fiscal 2025 on GAAP: $83.5-84.5 billion, flat to +1%, 12.3-12.4%, $12.15-12.40. The Q1 FY25
    release affirms it.
- **Guides on both bases** (the Q3 FY18 with-and-without rule: the guide takes the adjusted figures, GAAP in the notes).
  - The Q2 FY25 release adds ADG and gives both: EPS $12.20-12.45 adjusted ($12.10-12.35 GAAP), operating margin 12.2-12.3%
    adjusted (12.1-12.2%).
  - The Q3 FY25 release, now including FBM, gives adjusted figures only: $86.0 billion, flat comps, 12.1%, $12.25.
  - The fiscal 2026 guides give both again: $12.25-12.75 and 11.6-11.8% adjusted ($11.75-12.25 and 11.2-11.4% GAAP),
    affirmed in Q1. The Q2 FY26 release lowers them to $12.25 and 11.6% ($11.75 and 11.2%). Its outlook "includes tariff
    refunds recognized during the second quarter", and the quarter's EPS includes $0.11 of them on both bases.
  - The fiscal 2026 adjusted figures exclude only the acquisitions' intangible asset amortization ("an expected 40 basis
    point and $0.50 after tax impact"); FY25's adjusted figures also excluded the transaction costs. The margin step from
    FY25's 12.11% is taken as published (the level-form rule below).
- **A sales guide stated in growth.** The fiscal 2026 releases say "Total sales of $92.0 to $94.0 billion or an increase of
  approximately 7% to 9% compared to prior year". A guide that states its growth keeps it: the percent form (`rev_guide`)
  is LOW's original field, the builder already prefers it to a dollar level, and the dollar range goes in the note. The Q2
  FY26 release states only $92.0 billion: +6.6% on FY25's $86.29 billion. No builder change.
- **The acquisitions enter only through the guides and prints.** The Q2 FY25 guide includes ADG (closed in June 2025,
  $1.3 billion), the Q3 FY25 guide FBM (signed 2025-08-19, announced 2025-08-20, closed 2025-10-09, $8.8 billion), and
  the fiscal 2026 growth both. Sales growth in the prints and guides includes the acquired businesses, as published. The
  FBM 8-K expects the deal to be "accretive to adjusted diluted earnings per share in the first full year, post-closing,
  excluding synergies": not a current-year figure (the UNP merger rule). The financing 8-Ks (2025-09-19, 2025-09-30)
  reach the facts only through interest. No shares are issued, so the share history and buyback rate are unchanged; the
  paused repurchases show in the cash-return text.
- **Level-form margin guides step from the history's margin**, as since 2009: fiscal 2024 from FY23's adjusted 13.31%,
  fiscal 2025 from FY24's adjusted 12.30%, fiscal 2026 from FY25's adjusted 12.11%.
- **Published adjusted quarter margins replace GAAP in the prints** (the LOW setup rule), each change against the base the
  release names (the UNP rule):
  - Q4 FY23 and Q1 FY24 have no adjustment of their own. Their operating margins (9.07%, 12.42%) change by -48bp and
    -201bp against the prior year's adjusted 9.55% and 14.43%, as the infographics print them (GAAP +148bp and -229bp).
  - Q2-Q4 FY24 exclude the Canadian-sale gains: 14.43% (-114bp), 12.31% (-86bp), 9.43% (+36bp).
  - Q1 FY25 has no adjustment (11.92%, -50bp). Q2 FY25 to Q2 FY26 exclude the acquisition costs: 14.66% (+23bp), 12.41%
    (+10bp), 9.02% (-41bp), 11.49% (-43bp), 14.04% (-62bp).
  - Adjusted gross margins: Q2 FY25 33.84% (+37bp) and Q4 FY25 32.68% (-18bp). Q2 FY26's 33.04%, with no adjustment of
    its own, changes by -80bp against the prior year's adjusted 33.84%, as printed (GAAP -77bp).
  - The Q3 FY25 infographic is a set of images whose text layer is glyph-encoded. Its 12.41% (+10bp) was read from the
    images (exhibit992-10312025001.jpg and 003.jpg); the reconciliation page there, $2,481M plus $101M of acquisition costs
    on $20,813M of sales, agrees with it. A reader and a checker each decoded the text layer's glyphs independently and
    got the same figures.
- **Dividends,** each from the first filing that states it:
  - $1.15 from the Q2 2024 release (2024-08-20);
  - $1.20 from the Q2 2025 10-Q (accepted 2025-08-28 at 16:35 ET, dated 2025-08-29: "Cash dividends declared, $1.20 per
    share"). The Q2 2025 release's per-share row still reads 1.15 (and 3.40 for six months), beside $673 million declared;
  - $1.25 from the Q2 2026 release (2026-08-19).
- **ECOMMERCE stays on the watch list.** The FY2023-FY2025 10-Ks keep the risk factor. A new third sentence says Lowe's is
  at a disadvantage if competitors use rapidly evolving technologies, "including artificial intelligence and machine
  learning technologies" ("AI" from FY2024), more effectively; the delivery sentence drops its list of pick-up options. The
  quote carries the four sentences (text only). No filing shows the market pricing online substitution of Lowe's stores.
- **GENAI is not a LOW theme.** From the FY2023 10-K the filings describe Lowe's own use of predictive and generative AI
  (pilots, an "AI framework" in the 2024-12-11 8-K, an AI governance committee). The registry's GENAI scope, AI that
  substitutes the core product, does not cover a home-improvement retailer, so no event is entered.
- **Two segments from fiscal 2025.** The FY2025 10-K reports FBM and ADG as "Other" ($2.208 billion of fiscal 2025 sales,
  no prior year). The segment bridge (display only) takes the fifteen Retail Home Improvement categories (97.4% of sales)
  and says so; the history and the guides use total net sales.
- **Adds nothing:**
  - the 8-K/A of 2025-05-21 (one balance-sheet line of the Q1 FY25 release);
  - the 10-Qs (capital-expenditure guidance and repurchase status only), and the Retail Home Improvement segment's sales
    and margins in the 10-Qs and the FY2025 10-K: the history and the prints keep the consolidated figures the releases
    publish;
  - the guides' interest, depreciation, capital-expenditure and repurchase items (no field);
  - one-offs the company does not adjust: the discretionary bonuses the Q4 FY23, FY24 and FY25 releases announce ($140
    million, $80 million, $125 million), the storm effects of late 2024 and the IEEPA tariff refunds in Q2 FY26;
  - the vote 8-Ks (2024-06-05, 2025-06-05, 2026-06-02) and the officer 8-K of 2026-09-02.
- **Text-only change to 2017-2023:** three source descriptions (the FY2016, FY2017 and FY2018 10-Ks) now also cite the
  2014-2016 share counts. 352 dates change only in that text.
- **ISO weeks:** 2024-01-01 starts the 2024 batch, 2024-12-30 the 2025 batch and 2025-12-29 the 2026 batch. The last date
  is 2026-10-23, the last full week before the build (2026-10-29); the Q3 FY26 print is not out yet. Dates from late 2024
  on have only part of the two-year horizon, and the latest have no outcome.

Controls: altering one value of each new print, guide, vintage, dividend and theme event changes no date before its
publication and changes the first weekly date after it (31 of 31).

Seen in the build (method behaviour, not tuned):
- **2024: RICH on the fiscal 2024 guides.**
  - January-February, still on the fiscal 2023 guide ($13.00 adjusted, sales -11.4% against FY22's 53 weeks with Canada,
    so BASE -3.5%/yr) and with no down year in FY13-FY22 (BEAR flat): BUY on all 8 dates at 16.3-17.9x (the 24th-50th
    percentile), CHEAP on 2 and RICH on 6.
  - The Q4 FY23 print puts FY23 at $13.09, below FY22's $13.81: the window's first down year, so BEAR applies -5.2%/yr.
    The fiscal 2024 guide ($12.15, sales -1.6% to -2.8%, margin 12.65% against 13.31%) puts BASE at -1.3%/yr, and the
    stock traded at 17.6-21.3x (the 42nd-89th percentile): RICH on all 25 dates to 2024-08-16; BUY 15, ACCUMULATE 8,
    WATCHLIST 2.
  - The Q2 and Q3 FY24 guides ($11.80, then $11.85, sales -3.3% to -4.3%) put BASE at -4.9%, then -5.3%/yr, while the
    price rose to $282 (23.9x, the 98th percentile): RICH on all 19 dates to the year end; WATCHLIST 10, AVOID 5,
    ACCUMULATE 4.

  In all: RICH 50, CHEAP 2; BUY 23, ACCUMULATE 12, WATCHLIST 12, AVOID 5.
- **2025: a second down year, a guide for growth, and still RICH.**
  - January-February, on the fiscal 2024 guide: RICH on all 8; WATCHLIST 5, ACCUMULATE 3.
  - From the Q4 FY24 print FY24's adjusted $11.99 is a second down year (-8.4%), so BEAR applies -8.4%/yr. The fiscal
    2025 guide ($12.275, sales -0.2% to +1.0%, margin +5bp) and buybacks put BASE at +6.4%/yr. At 17.3-20.5x (the
    38th-85th percentile) the class reads RICH on 21 of the 25 dates to 2025-08-15, FAIR on 3 and CHEAP on 2025-04-17
    (17.8x): the proxy composite (1.65-1.85) sits below the market composite (2.29-2.84) even at the median multiple.
  - The guides with ADG and FBM (sales +1.0% to +2.2%, then +2.8%) lift BASE to +6.8%/yr while the price rises to $272
    (22.1x, the 94th percentile): RICH on all 19 dates from 2025-08-21, AVOID on 3 in September.

  In all: RICH 48, FAIR 3, CHEAP 1; ACCUMULATE 21, WATCHLIST 19, BUY 9, AVOID 3.
- **2026: the growth guide, then CHEAP as the price fell.**
  - January-February, still on the fiscal 2025 guide, at 20.2-23.5x (the 84th-99th percentile): RICH on all 8, AVOID on
    7 (Ratio B up to 4.49).
  - The fiscal 2026 guide ($12.50 adjusted, sales "an increase of approximately 7% to 9%" with FBM) puts BASE at
    +9.7%/yr. As the price fell from $264 to $208 (21.2x to 16.6x, the 92nd to the 28th percentile) the class moved from
    RICH to FAIR and CHEAP: of the 25 dates to 2026-08-14, RICH 5 (to mid-April), FAIR 6 and CHEAP 14.
  - The Q2 FY26 guide ($12.25, sales +6.6%, adjusted margin 11.6%) lowers BASE to +7.4%/yr and the proxy composite to
    1.50: RICH on 2026-08-20 and 2026-08-28 at 17.0-17.7x (the 33rd-44th percentile), then CHEAP on all 8 dates to
    2026-10-23 as the price fell to $181-205 (14.8-16.7x, the 12th-28th percentile).

  In all (43 dates): CHEAP 22, RICH 15, FAIR 6; BUY 19, ACCUMULATE 11, AVOID 8, WATCHLIST 5.
- **How far each call moves the classes** (the 147 dates rebuilt with one encoding changed; no outcome consulted):
  - the GAAP figures of the guides that give both bases (Q2 FY25 and fiscal 2026) would change 18 classes, all from
    2026-03-13, and 17 tiers from 2025-08-29. GAAP EPS sits $0.10-0.50 below adjusted: 15 of the 28 CHEAP and FAIR dates
    of 2026 would read RICH and 3 CHEAP dates FAIR;
  - FY23-FY25 at GAAP from the Q4 print until the 10-K would change 2 tiers (2025-02-27, 2025-03-21) and no class;
  - reading the fiscal 2026 sales guides as dollar levels, the Q3 FY25 margin at GAAP, GAAP quarter margins throughout,
    the $1.20 dividend from the Q3 FY25 release, or no full-year comps from the infographics would change none.
- **The EPP floor is 15x, 16x from 2026-02-13 to 2026-09-11.** BULL is the decade EPS CAGR: 23.0%, then 19.1-19.9%
  (FY14-FY23), 15.5-16.0% (FY15-FY24) and 13.3-14.1%/yr (FY16-FY25). XBULL stays the 2019-2021 run (44.8%/yr).

Judgement calls that could carry hindsight:
- taking the adjusted figures where a guide gives both bases (the call that moves the most classes: 18 of 147);
- keeping the growth the fiscal 2026 releases state (7-9%) rather than reading their dollar range against FY25's sales;
- reading the Q3 FY25 adjusted operating margin from the infographic's images;
- dating the $1.20 dividend from the Q2 FY25 10-Q, because the Q2 FY25 release's per-share row reads 1.15;
- taking each year's comparable sales from the Q4 infographics (text only), and leaving the acquired segment out of the
  segment bridge (display only).

## AAPL (Apple): the fourth ticker, in staging

The AAPL series is built apart from ACN, UNP and LOW and shares nothing with them but the machinery: its own fact sheet
(`retro/facts/AAPL.json`), builder (`retro/build_aapl.py`) and engine (`retro/templates/aapl_engine.py.tmpl`, the LOW engine
with personal-computer and consumer-electronics signals). The method is still r2. No ACN, UNP or LOW fact, parameter, outcome
or finding enters an AAPL model. Outputs go to `staging/retrospective/AAPL/`, beside UNP and LOW, with the same `index.json`
and their own `SERIES.md`.

```bash
python3 retro/build_aapl.py --weekly 2008-01-01 2008-12-31                  # 53 dates, 2008-01-04 .. 2008-12-31
for d in staging/retrospective/AAPL/2008-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series AAPL
python3 retro/tools/firewall.py 2008-07-01 AAPL
```

The 10-Ks from FY1999 to FY2008 (FY2001 a 10-K405) were read for the history and the decade's signal values, and every 8-K of
2007 and 2008 and the fiscal 2008 10-Qs were read in full, by Opus directly; the 10-Qs and the FY2007 and FY2008 10-Ks were
searched for forward-looking statements. 246 strings were checked with `verbatim.py` against their own filings (179 for the
prints, guides and vintages, 67 for the rule T decade), and each source's date comes from EDGAR's acceptance time. Decided on
2026-10-29, before any AAPL model was built or any AAPL outcome computed:

- **Fiscal calendar.** Apple's fiscal year is "the 52 or 53-week period that ends on the last Saturday of September" (FY2007
  10-K); fiscal 2006 had 53 weeks. The builder maps each day to its fiscal year by that rule and checks it against the year-ends
  the filings state.
- **Prices on the as-of share basis** (the UNP rule). Yahoo's series is adjusted for the 2014 (7-for-1) and 2020 (4-for-1)
  splits, so 2008 prices are Yahoo's times 28: $180.05 on 2008-01-04. The 2000 and 2005 2-for-1 splits precede every per-share
  fact in the fact sheet, so they restate nothing; the 2005 split is listed (8-K of 2005-02-11).
- **Every release came after the close.** Each earnings 8-K was accepted at 16:28-16:40 ET (the webcast at 2:00 p.m. Pacific),
  so a print is dated the next trading day and the week's date is the trading day after that: 2008-01-24, 2008-04-25,
  2008-07-23 and 2008-10-23. ACN's releases before 2013 were dated on the release day; the acceptance-time rule of "Adding
  dates" is stricter, and can only lag.
- **History: the FY2007 10-K** (accepted 2007-11-15 16:49 ET, dated 2007-11-16) gives FY2003-FY2007, already restated for
  stock-based compensation by the FY2006 10-K (the option-dating review). The FY2008 10-K (accepted 2008-11-05 06:16 ET, before
  the open) gives FY2004-FY2008; FY2003 comes from the FY2007 10-K, the latest that reports it.
- **Two years excluded** (the ACN FY02 rule). FY2001 was a net loss ($(0.04) per diluted share). FY2002's GAAP EPS of $0.06 (as
  restated; $0.09 first reported) was depressed by items the 10-K lists for the year, a $42 million net loss on non-current
  investments and $30 million of restructuring charges, together more than the year's $42 million net income, and no adjusted
  figure was published. So the history and the P/E window start with FY2003 (2002-09-29): a 5.3-year window on 2008-01-04,
  6.3 years on 2008-12-31. FY2003 is kept: its listed items ($26 million of restructuring against $10 million of investment
  gains and a $6 million forward-contract gain) are a fraction of its $57 million net income, although it had a $17 million
  operating loss (interest income made the year profitable).
- **EPS** is diluted EPS as reported. No year has a company-published figure excluding a one-off; FY2005's $81 million tax
  benefit is a dollar amount, not an EPS without it, so GAAP stands (no figure is derived from a published amount).
- **The Q4 FY08 non-GAAP measures stay out.** The 2008-10-21 release adds "Adjusted Sales" ($11.68 billion) and "Adjusted Net
  Income" ($2.44 billion, $2.69 per share) that remove subscription accounting for iPhone and Apple TV. That is a different
  revenue-recognition basis, not a one-off, and it is given for the quarter only ("not presented with comparable non-GAAP
  financial measures for prior periods"). FY08 enters the history at GAAP $5.36; the adjusted quarter is shown in a note.
- **Apple guides one quarter at a time.** Each release gives the next quarter's revenue (a dollar level, "about $9.2 billion";
  from the Q4 FY08 release a range, $9.0-10.0 billion) and diluted EPS. No release or filing of the period gives a full-year
  revenue, EPS or operating-margin guide. Method r2 maps this as for UNP and LOW:
  - current-FY EPS: no fiscal-year EPS guide, so the last full year's EPS stands: FY07's $3.93 to the Q4 FY08 print, FY08's
    $5.36 from it. A quarter's EPS guide is shown in the guide line and feeds no input (the UNP 2008 rule);
  - BASE growth and the growth factor: the next-quarter revenue guide, read as growth against the same quarter a year earlier
    (the LOW dollar-level rule, applied to a quarter), each year-ago revenue from that quarter's own release, rounded to 0.1:
    +29.3% (Q1 FY08 on Q1 FY07's $7.115B), +29.2%, +33.1%, +25.5%, then -6.3% to +4.1% (Q1 FY09 on Q1 FY08's $9.608B);
  - no operating-margin guide, so no margin step, and the margin signal takes the latest quarter's change (the ACN rule).
- **Gross-margin expectations are display only.** The Q3 FY08 10-Q (accepted 2008-07-23 17:27 ET, dated 2008-07-24) "anticipates
  gross margin levels of about 31.5% in the fourth quarter of 2008 and about 30% in 2009"; the FY2008 10-K repeats "about 30% in
  2009". The method's margin is the operating margin, and no figure is derived from another, so each is shown in the guide line
  (the quarter's while Q4 FY08 is unreported, fiscal 2009's once it is the current year). The words-only statements of the FY2007
  10-K and the Q1 and Q2 FY08 10-Qs (gross margin to "decline sequentially", to "continue to decrease") add nothing. The quoted
  "2009" draws the year-check warning on the 23 dates from 2008-08-01; it is the company's forecast, public before each date.
- **No dividend** ("did not declare or pay cash dividends in either fiscal 2007 or 2006"), so the conservative case carries none.
  Repurchases were $3 million in FY07 and nil in FY08.
- **Signals.** Six, with ACN's weights, mirroring LOW's: Mac unit growth (0.20, the release's headline unit), gross margin change
  (0.20), net sales growth (0.15), growth of net sales other than Macs (0.15: iPod, music, iPhone, peripherals, software; total net
  sales less the Mac line, 57% of FY07 sales), the operating-margin change (0.15; the guided step, else the latest quarter) and the
  theme slot at 2/4. Values are the latest release's, derived from its income statement and data sheet. iPod and iPhone units have
  no ten-year history, so they are shown, not scored.
- **Thresholds by rule T** (the LOW rule), over the ten years of the FY2007 10-K, the vintage public on 2008-01-04: FY1998-FY2007,
  each change from the latest 10-K that reports both years. Where a filing publishes "operating income before special charges"
  for both years of a change (the FY2000 and FY2001 10-Ks, FY1999-FY2001), it replaces the reported figure; FY1998 against FY1997
  stays as reported (no filing gives FY1997 before its special charges). The values are in the fact sheet (`rule_t`).

  | Signal | Decade (FY1998-FY2007) | BEAR / BASE / BULL / XBULL |
  |---|---|---|
  | Mac unit growth | -3.9, 24.8, 32.2, -32.3, 0.5, -2.9, 9.2, 37.8, 17, 33 % | -78 / -32 / 13 / 38 % |
  | gross margin change | 557.5, 275.4, -51.7, -410.5, 488.9, -36.4, -23.9, 175.3, -3.2, 498.4 bp | -910 / -410 / 90 / 560 bp |
  | net sales growth | -16.1, 3.2, 30.1, -32.8, 7.1, 8.1, 33.4, 68.3, 38.6, 24.3 % | -82 / -33 / 16 / 68 % |
  | net sales other than Macs | -23.5, -2.5, 4.4, -12.6, 25.8, 42.1, 95.6, 128.1, 56, 14.7 % | -67 / -23 / 20 / 128 % |
  | operating margin change | 1950.4, 178.2, 147.4, -1397.6, 671, -6.5, 405.5, 801.3, 90.6, 566.6 bp | -3090 / -1400 / 290 / 1950 bp |

- **Durability.** DURABLE, risk 2, as for ACN, UNP and LOW. The "why" is the 10-K's own words: Apple "designs and develops
  virtually the entire solution" (FY2008: "nearly"), is the "only maker of hardware using the Mac OS", which "has a minority
  market share in the personal computer market", and its markets are "highly competitive and characterized by aggressive price
  cutting, with its resulting downward pressure on gross margins". No disruption theme in `taxonomy_eras.json` is live for a
  personal-computer and consumer-electronics maker in 2008 (CLOUD from 2012-10-30; OFFSHORE is scoped to IT services), so the
  watch list is empty and the builder refuses events until a theme encoding is decided.
- **Segment bridge and EPS check** (display only): the latest 10-K's product lines with each line's growth (iPhone shown as new
  in FY07); the EPS check adds other income and expense (mostly interest on $15-25 billion of cash) instead of deducting interest.
- **Adds nothing:**
  - the 2008 8-Ks: a director and a principal accounting officer (2008-01-08); Macworld's 4 million iPhones and 5 million Leopard
    copies to date (2008-01-15, items 2.02 and 8.01); WWDC's 6 million iPhones, the iPhone 3G in 22 countries and its carrier
    terms (2008-06-09); the bylaws (2008-08-26);
  - the 2007 8-Ks other than the releases: the name change to Apple Inc. (2007-01-10, before the FY2007 vintage), bylaws, an
    officer, and the SEC's charges against two former officers (2007-04-24; no action against Apple);
  - the proxy (2008-01-23) and the 10-Qs beyond the Q3 FY08 gross-margin sentence.
- **Anachronism list:** Apple-era product names (MacBook Air, App Store, MobileMe, Snow Leopard, iPhone 3GS, iPad, iCloud) join
  `taxonomy_eras.json` beside "iPhone 3G". No existing model of any ticker contains them, so no output changes.

Controls: altering one value of each print, guide, vintage and the split changes no date before its publication and changes the
first weekly date after it (17 of 17); a guide for fiscal 2009 first shows on 2008-10-23, the first date with fiscal 2009 current,
and the split, which restates no fact, changes nothing. Rebuilding the 2008 dates of ACN, UNP and LOW changes nothing.

Seen in the build (method behaviour, not tuned):
- **BULL and XBULL start from near-zero EPS.** BULL is the FY03-FY07 EPS CAGR, +164.7%/yr ($0.08 to $3.93; FY03-FY08's +131.9%
  from the Q4 print), at the 75th-percentile P/E: a BULL price of $1,086-1,278 against a stock at $83-189. XBULL is FY03-FY05's
  +340%/yr ($7,043-9,606). Ratio B runs from -0.03 to 0.10, so the legacy tier reads BUY on all 53 dates.
- **The market composite sits at the bottom of its grid** (1.00-1.22): even a small XBULL weight lifts the expected price above
  the hurdle price. The adjusted composite is 2.42-3.05, so the adjusted gap is +1.21 to +2.00 (UNDERVALUED) on every date.
- **The class follows the EPP floor:** FAIR on the 20 dates where the price stood more than 100% above it ($165-189, 2008-01-04,
  2008-01-11, 2008-04-25 to 2008-07-23 and 2008-08-08 to 2008-08-29), CHEAP on the other 33. The floor is the median of the
  calendar-year P/E lows (on 2008-01-04: 2002 85x, 2003 29x, 2004 12x, 2005 20x, 2006 19x, 2007 21x, 2008 46x), 21x times FY07's
  $3.93 ($83), then 20x times FY08's $5.36 ($107) from the Q4 print.
- **The P/E window holds FY2003 at 82-144x** (EPS $0.08), so its 90th percentile is 92-95x and its median 31-33x. On FY07 EPS the
  stock traded at 30-48x (the 43rd-79th percentile) to September and 24.6-24.8x in October (the 20th-21st); on FY08 EPS, from the
  Q4 print, at 15.4-20.1x (the 1st-5th).
- **EPS anchors on the last full year:** FY07's $3.93 stands until 2008-10-22, when nine-month FY08 EPS was already $4.10.
- **BASE growth is the quarter guide less dilution:** diluted shares grew 5.0%/yr over FY03-FY07, so BASE is +24.3%, +24.2%,
  +28.1% and +20.5%/yr on the four FY08 guides, and -5.4%/yr on the Q1 FY09 range. The growth factor reads -0.5 on 40 dates and
  -0.29 on the 13 of the Q3 FY08 guide (+33.1% against the FY04-FY07 median of +36.0%).
- **From the Q4 FY08 print the price sits below the BEAR price:** BEAR is flat FY08 EPS at the 10th-percentile P/E, $112-117,
  against a stock at $83-108, so Ratio B turns negative and the EPP gap reads -23% to 0%.
- **A display quirk inherited from the LOW engine:** with no fiscal-year EPS guide the EPS check prints the label and the figure
  twice ("FY07's $3.93 stands $3.93").

How far each call moves the classes (the 53 dates rebuilt with one encoding changed; no outcome consulted):
- keeping FY2002 (excluding only the FY2001 loss) would change 20 classes, every FAIR date to CHEAP: the window then starts on
  2001-09-30 and adds 2001-2002's P/E lows of about 125x, which lifts the EPP floor from 21x to 25x. No tier changes;
- excluding FY2003 as well would change 3 classes (2008-01-18, 2008-04-18, 2008-09-05: CHEAP to FAIR) and no tier.

Judgement calls that could carry hindsight:
- excluding FY2002 as distorted (the call that moves the most classes: 20 of 53) and keeping FY2003;
- the signals, chosen by a builder who knows what Apple became: Mac units and net sales other than Macs (rule T then sets their
  thresholds mechanically);
- reading each dollar revenue guide as growth on the year-ago quarter;
- keeping GAAP over the Q4 FY08 non-GAAP measures, and the gross-margin expectations out of the inputs;
- DURABLE rather than CYCLICAL (the class label only).

### AAPL 2009-2011: non-GAAP quarters, the 2010 restatement, the iPad

```bash
python3 retro/build_aapl.py --weekly 2009-01-05 2011-12-31                  # 156 dates, 2009-01-09 .. 2011-12-30
```

Every 8-K, 10-Q, 10-Q/A, 10-K, 10-K/A and proxy from 2008-11-06 to the end of 2011 was read by Opus directly, with the 10-Qs and
10-Ks searched for forward-looking statements. 361 strings were checked with `verbatim.py` against their own filings, and each
source's date comes from EDGAR's acceptance time. Thresholds and signals are unchanged. Decided before any 2009-2011 date was built
or scored:

- **Four vintages.**
  - The FY2009 10-K (accepted 2009-10-27 16:18 ET, dated 2009-10-28) gives FY2005-FY2009; FY2004 comes from the FY2008 10-K and
    FY2003 from the FY2007 10-K.
  - The FY2009 10-K/A (accepted 2010-01-25 16:25 ET, dated 2010-01-26) is a vintage of its own (the UNP rule for a filing that
    re-presents the 10-K). Apple adopted the amended revenue-recognition standards (ASU 2009-13 and 2009-14) retrospectively in Q1
    FY10: iPhone and Apple TV revenue is now recognized at sale instead of over 24 months, and every quarter of FY2007-FY2009 is
    revised. FY09 EPS goes from $6.29 to $9.08 and FY08 from $5.36 to $6.78; FY07 stays at $3.93. The 10-K/A amends Items 6-8
    only, so the business wording stays the FY2009 10-K's.
  - The FY2010 10-K (accepted 2010-10-27 16:36 ET, dated 2010-10-28) and the FY2011 10-K (2011-10-26 16:35 ET, dated 2011-10-27).
    Each year comes from the latest 10-K that reports it: FY2005 from the 10-K/A, FY2006 from the FY2010 10-K.
  - The history runs FY2003-FY2009, then to FY2010 and FY2011. FY2001 and FY2002 stay excluded (from the FY2011 10-K only FY2002
    is in the decade), and the P/E window starts on 2002-09-29 throughout: 6.3 years on 2009-01-09, 9.2 on 2011-12-30.
- **FY2009 prints stay GAAP.** Each FY2009 release adds quarterly non-GAAP "Adjusted Sales" and "Adjusted Net Income" that remove
  subscription accounting; the Q4 FY09 release gives them for the quarter only. By the 2008 rule GAAP stands, and the adjusted
  figures go in a note. FY09 enters the history at $6.29 from the Q4 print until the 10-K/A revises it.
- **Year-ago quarters on the guide's own basis.** A dollar revenue guide is read against the same quarter a year earlier on the
  guide's accounting basis, from the latest filing published by the guide's date. The Q2-Q4 FY10 guides are read against the
  revised FY2009 quarters in exhibit 99.3 of the Q1 FY10 8-K ($9.084B, $9.734B, $12.207B); every other guide against the year-ago
  quarter's own release. This states the 2008 rule ("from that quarter's own release") for a restatement, and no 2008 value
  changes. The Q1 FY10 guide, given in October 2009 before the restatement, is on the old basis, against Q1 FY09's $10.167B.
- **The guides, as growth on the year-ago quarter:** Q2 FY09 +1.2% to +6.5%, Q3 +3.2% to +5.8%, Q4 +10.2% to +12.7%; Q1 FY10
  +11.1% to +14.1%, Q2 +21.1% to +25.5%, Q3 +33.6% to +37.7%; from the Q4 FY10 guide the company gives points ("about $18
  billion"): Q4 FY10 +47.5%, Q1 FY11 +46.7%, Q2 +63.0%, Q3 +46.5%, Q4 +22.9%, Q1 FY12 +38.4%. That last quarter "will span 14
  weeks rather than 13": the published figure stands and the week goes in the note (the LOW 53rd-week rule).
- **No fiscal-year guide in any year,** so the last full year's EPS stands: FY08's $5.36 to 2009-10-20, FY09's $6.29 to
  2010-01-26, FY09's revised $9.08 to 2010-10-19, FY10's $15.15 to 2011-10-19 and FY11's $27.68 after.
- **Gross-margin expectations stay display only.** The 10-Qs and the FY2009 and FY2010 10-Ks give the next quarter's gross margin
  ("about 32.5% in the second quarter of 2009" to "about 36% in the first quarter of 2011"), each shown while its quarter is
  unreported. A statement about a later quarter or a half-year ("about 30% in the second half of 2009") has no field. The 10-K/A
  drops the sentence, and the FY2011 10-Qs and 10-K give it in words only. The quoted years draw the year-check warning on 20
  dates; each is the company's forecast, public before the date.
- **Good Friday 2011.** The Q2 FY11 release came after the close on Wednesday 2011-04-20, so it is dated Thursday 2011-04-21, and
  no trading day followed in that week. The week's date is 2011-04-21, and the print, public before that day's open, counts (the
  ACN rule for Good Friday 2013).
- **Display-only additions,** shown only where the data exists, so every 2008 model rebuilds byte-identical: long-term marketable
  securities beside cash (from FY2009, when Apple first splits its securities), the absence of an iPhone and Apple TV deferral
  (from Q1 FY10), and iPad units in catalyst (4) (from Q3 FY10). iPad sales fall inside net sales other than Macs.
- **No dividend, no repurchases and no debt outstanding** in any year (each 10-K).
- **Adds nothing:** Steve Jobs's medical leaves (8-Ks of 2009-01-16 and 2011-01-18), his resignation as chief executive and Tim
  Cook's appointment (2011-08-26), his death (2011-10-06), the auditor change (2009-02-27), the director and officer 8-Ks
  (2009-08-04, 2010-03-12, 2010-11-17, 2011-06-15, 2011-11-16), bylaws (2009-06-02), vote results (2010-03-01, 2011-02-24), the
  10-Q/A of 2009-04-27 (vote percentages), the proxies, and the 10-Qs beyond their gross-margin sentence. None changes a guided
  number (the UNP and LOW rule for officer and board 8-Ks).
- **Durability is unchanged:** DURABLE, risk 2, with each 10-K's own words ("nearly the entire solution", the "only authorized
  maker of hardware using the Mac OS", "aggressive price cutting, with resulting downward pressure on gross margins"). No theme is
  live for Apple before CLOUD (2012-10-30).
- **Anachronism list:** iPhone 4, FaceTime, Retina display, iPad 2, iOS 5, Siri, iPhone 4S, iPhone 5 and iPad mini join it; no
  existing model contains them.

Controls: altering one value of each new print, Q4 full-year figure, guide and vintage changes no date before its publication and
changes the first weekly date on or after it (39 of 39). Several 10-Qs were accepted after the close on the eve of a weekly date,
so they first show on that date; a guide for the next fiscal year first shows on the first date with that year current. The 53
dates of 2008 rebuild byte-identical.

Seen in the build (method behaviour, not tuned):
- **CHEAP on 154 of 156 dates, BUY on all.** The two FAIR dates, 2009-10-09 and 2009-10-16 ($188-190), are where the conservative
  case fell to -6.7% and -5.5%.
- **2009 opens below the BEAR price.** On the anchor EPS the stock traded at 15.4-35.5x in 2009 (the 1st-76th percentile). To
  2009-03-20 the price sat below the BEAR price (flat EPS at the 10th-percentile multiple), so Ratio B was negative on 11 dates.
  BASE growth followed the quarter guides less dilution (4.3%/yr, 3.7% from the FY2009 10-K): -5.4%/yr on the Q1 FY09 range in
  January, then -0.5%, +0.2% and +7.1%/yr, and +8.9%/yr on the Q1 FY10 guide.
- **The restatement lowered the multiple in a week:** 31.4x FY09's $6.29 on 2010-01-22 (the 58th percentile), 22.9x the revised
  $9.08 on 2010-01-27 (the 32nd).
- **The guides carry BASE to +44% and +60%/yr.** BASE growth reached +43.8%/yr on the Q4 FY10 guide and +59.6%/yr on the Q2 FY11
  guide (+63%), so the BASE price ran to $796 in 2010 and $1,215 in late 2011. The growth factor read +0.5 from 2010-07-22 to
  2011-07-15, -0.04 on the Q3 FY10 guide and -0.5 on the other dates.
- **BULL and XBULL still start from FY2003's $0.08:** BULL +107% to +132%/yr ($941-3,832), XBULL +340%/yr ($9,450-47,248). Ratio B
  ran from -0.03 to 0.15, and the market composite stayed at 1.00-1.22.
- **The EPP floor stayed at 18-20x until the Q4 FY11 print, then fell to 15x** as the window took in 2009-2011's lower multiples.
  From that print, at 13.1-14.6x FY11's $27.68 (the 18th-26th percentile), the price sat below the floor (-12% to -3%).
- **EPS anchors on the last full year:** FY10's $15.15 stood until 2011-10-19, when nine-month FY11 EPS was already $20.63.

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- keeping the FY2009 10-K's old basis until the FY2010 10-K (no 10-K/A vintage) would change 19 classes, CHEAP to FAIR, from
  2010-04-22 to 2010-10-15, and no tier;
- reading the Q2-Q4 FY10 guides against the year-ago quarters as first reported would change none;
- keeping FY2002 would change 2 (the October 2009 FAIR dates to CHEAP), and excluding FY2003 3 (2009-09-18 to 2009-10-02, CHEAP
  to FAIR); no tier.

Judgement calls that could carry hindsight:
- treating the 10-K/A as a vintage from its filing date (the call that moves the most classes: 19 of 156);
- reading the fiscal 2010 guides against the revised year-ago quarters (no class moves);
- keeping the FY2009 prints, and FY09's first $6.29, on GAAP rather than the non-GAAP measures;
- treating the chief executive's medical leaves, resignation and death as adding nothing (the method has no input for them);
- DURABLE rather than CYCLICAL (the class label only).

### AAPL 2012-2015: the dividend, guidance lists without EPS, the 7-for-1 split, no iPod units

```bash
python3 retro/build_aapl.py --weekly 2012-01-02 2015-12-31                  # 209 dates, 2012-01-06 .. 2015-12-31
```

Every 8-K, 10-Q, 10-K and proxy filed on Apple's CIK from 2012-01-01 to 2015-12-31 was read directly, with the
third-party solicitations (PX14A6G, DFAN14A) and the 10-Qs and 10-Ks searched for forward-looking statements. 558 strings were
checked with `verbatim.py` against their own filings. 187 structured checks read each print's statements and each Q4 print's
full-year figures back from the XBRL of the 10-Q or 10-K filed with it, 45 read the unit sales back from each 10-Q's own table,
and the four quarters of units and net sales sum to each 10-K's year. Every source's date comes from EDGAR's acceptance time.
Thresholds and signals are unchanged. Decided before any 2012-2015 date was built or scored:

- **Four vintages, ten years each.** The FY2012 10-K (accepted 2012-10-31 17:07 ET, dated 2012-11-01) gives FY2008-FY2012, the
  FY2013 10-K (2013-10-29 20:38 ET, dated 2013-10-30) FY2009-FY2013, the FY2014 10-K (2014-10-27 17:11 ET, dated 2014-10-28)
  FY2010-FY2014 and the FY2015 10-K (2015-10-28 16:31 ET, dated 2015-10-29) FY2011-FY2015. Each earlier year comes from the
  latest 10-K that reports it. The history moves to FY2003-FY2012, FY2004-FY2013, FY2005-FY2014, then FY2006-FY2015.
  - First-year diluted shares: FY2003's 723,352K (FY2007 10-K), FY2004's 774,776K (FY2008 10-K), FY2005's 856,878K (FY2009
    10-K/A), FY2006's 877,526K (FY2010 10-K).
  - From the FY2012 vintage the decade no longer reaches FY2001-FY2002 (still excluded), and from 2012-09-29 the ten-year P/E
    window starts after 2002-09-29, so that start stops binding; the vintages from FY2013 carry none.
  - FY2012 spanned 53 weeks (a 14th week in Q1 FY12). Every year is GAAP: Apple published no figure excluding a one-off.
- **Two re-presentations add nothing.** The 8-Ks of 2013-04-24 (accepted 17:05 ET) and 2015-01-28 (16:48 ET) re-present the
  FY2012 and FY2014 10-Ks for new segments and product categories: "There is no change to the Company's previously reported
  Consolidated Statements of Operations". They change no input, so they add nothing (the ACN 2024 segment recast); the UNP
  vintage rule is for a re-presentation that changes the history. The bridge (display only) keeps the latest 10-K's lines.
- **Prints.** Every release came after the close, so each print is dated the next trading day. The Q4 FY12 release came on
  Thursday 2012-10-25, so its print is dated Friday 2012-10-26 and no trading day follows in the week: the week's date is the
  print's day and the print, public before that day's open, counts (the Good Friday 2011 rule). Q1 FY12 spanned 14 weeks against
  13, and Q1 FY13 13 against 14: growth as published, the weeks in the notes (the LOW 53rd-week rule).
- **Guides, one quarter at a time.** Through the Q4 FY12 release each gives the next quarter's revenue and EPS as points, as
  before. From the Q1 FY13 release a bulleted list gives revenue and gross margin as ranges, operating expenses,
  other income/(expense) and a tax rate, and no EPS. Revenue is read against the year-ago quarter's own release, as before (net
  sales were never restated): Q2 FY12 +31.8%, Q3 +19.0%, Q4 +20.3%, Q1 FY13 +12.2% (against the 14-week quarter), Q2 +4.6% to
  +9.7%, Q3 -4.3% to +1.4%, Q4 -5.5% to +2.9%, Q1 FY14 +0.9% to +6.4%, Q2 -3.7% to +0.9%, Q3 +1.9% to +7.6%, Q4 -1.3% to +6.7%,
  Q1 FY15 +10.3% to +15.5%, Q2 +13.9% to +20.5%, Q3 +22.9% to +28.2%, Q4 +16.3% to +21.1%, Q1 FY16 +1.2% to +3.9%.
  - The operating-expense, other-income and tax-rate items (`opex_usd_b`, `oie_usd_b`, `tax_pct`) are shown in the guide line
    and feed no input. An operating margin derived from the revenue, gross-margin and expense ranges would be a figure derived
    from others (the 2008 rule), and a quarter's tax rate is not the year's, so the EPS check keeps the last year's rate (a
    quarter's EPS guide fed nothing either).
  - Still no fiscal-year guide, so the last full year's EPS stands: FY11's $27.68 to 2012-10-25, FY12's $44.15 to
    2013-10-28, FY13's $39.75 ($5.68 after the split) to 2014-10-20, FY14's $6.45 to 2015-10-27, FY15's $9.22 after.
- **Gross-margin expectations.** The FY2012 10-Qs give words only. The FY2012 10-K's "about 36% during the first quarter of
  2013" is a quarter's expectation, shown in the guide line until Q1 FY13 is reported. From the Q1 FY13 release the 10-Qs and
  10-Ks repeat the release's range: nothing.
- **A guide restated in words.** The 8-K of 2013-09-23 (08:45 ET, before the open) expects Q4 FY13 revenue and gross margin
  "near the high end of the previously provided range": the ranges stand and the words go in the note (the ACN Q3 FY08 rule).
- **Dividends: the latest declared rate.** The March 2012 policy had no 8-K. Its first filing is the Q2 FY12 10-Q (accepted
  2012-04-25 17:01 ET, dated 2012-04-26): Apple "plans to make, subject to subsequent declaration, quarterly dividends of $2.65
  per share". A plan subject to declaration is not a declared rate, so the conservative case carries no dividend until the first
  declaration. That can only lag. The rates, each from the first filing that states it:
  - $2.65, Q3 FY12 release (2012-07-25);
  - $3.05, the 7.01 8-K of 2013-04-23 (dated 2013-04-24);
  - $3.29, the 7.01 8-K of 2014-04-23 (dated 2014-04-24), divided by 7 from the split;
  - $.47, Q3 FY14 release (2014-07-23), the first declaration after the split;
  - $.52, the 7.01 8-K of 2015-04-27 (dated 2015-04-28).
- **The capital return program, display only.** Catalyst (5) now shows the latest statement of the program (`capital_return`):
  the Q2 FY12 10-Q's policy and $10 billion repurchase program from 2012-04-26, then the 7.01 8-Ks' $100 billion (2013-04-24),
  over $130 billion (2014-04-24) and $200 billion (2015-04-28). The 10-Qs' and 10-Ks' restatements of an unchanged program add
  nothing. Each print's cash-return text gives the dividends and repurchases paid year to date (cash flow statement) and, from Q3
  FY13, the debt on its balance sheet.
- **The 7-for-1 split.** Announced in the 7.01 8-K of 2014-04-23 (dated 2014-04-24); "trading will begin on a split-adjusted
  basis on June 9, 2014", the price data's split date. From that date every per-share fact published before it is divided by 7
  and every share count multiplied by 7 (the UNP rule). The FY2014 and FY2015 10-Ks restate FY2010-FY2015 for it, so those years
  enter as restated ($2.16 for FY10, not $15.15 / 7), and the years from earlier 10-Ks are divided. P/E percentiles do not move
  (2014-06-06: $645.57 on $39.75; 2014-06-13: $91.28 on $5.68). Print and program text is not restated (the UNP 2014 rule).
- **No iPod units from Q1 FY15.** The data sheets and 10-Qs report units for iPhone, iPad and Mac only; iPod sales fall in Other
  Products. Mac units and net sales other than Macs are unaffected.
- **An engine revision, text only.** Two lines of `aapl_engine.py.tmpl` assumed facts that 2012-2015 changes. Catalyst (5) said
  "none so far (no dividend, no buyback)"; it now prints `CAPITAL_RETURN`, which keeps those words until the first program
  statement. The bridge printed iPod units unconditionally; it now says "iPod units not reported" when there are none. No rule
  changes. The 209 models of 2008-2011 rebuild with the new engine text and one new constant, and every one of their reports
  rebuilds byte-identical.
- **No theme.** CLOUD is live from 2012-10-30 but its scope is on-premise enterprise IT. STREAMING (from 2015-08-04) covers
  linear TV and ECOMMERCE (from 2015-01-01) physical retail. The FY2012-FY2015 10-Ks mention cloud and streaming only as Apple's
  own services (iCloud, iTunes Radio, Beats Music, Apple Music). So there are no events, the watch list stays empty, and the class
  is DURABLE, risk 2, with each 10-K's own words ("nearly the entire solution", the "only authorized maker of hardware using OS
  X", "aggressive price cutting and resulting downward pressure on gross margins") and store count (390, 416, 437, 463).
- **Adds nothing:**
  - the officer, director, vote, compensation, bylaw and articles 8-Ks, among them the CFO transition (2014-03-05, 2014-05-30),
    the chief operating officer (2015-12-17), the split's articles amendment (2014-06-06) and proxy access (2015-12-22);
  - the debt offerings (8-Ks of 2013-05-03, 2014-05-06, 2014-11-10, 2015-02-09, 2015-05-13, 2015-06-10, 2015-07-31 and
    2015-09-17) and the description of common stock (2014-07-23); they reach the facts only through the balance sheet;
  - the 8-K of 2013-09-23's nine million iPhones (units, as Macworld's in 2008);
  - the proxies and the shareholder solicitations (CalPERS; Greenlight's preferred-stock proposal, 2013; Icahn's repurchase
    proposal, 2013-2014; the New York City Comptroller), and Apple's own DEFA14A statements, which restate the $45 billion plan
    with no new figure;
  - the 10-Qs' and 10-Ks' capital-expenditure, store-opening, debt-plan and Beats statements (no field).
- **Text-only change to 2008-2011:** besides the engine text, three source descriptions (the FY2008 10-K, the FY2009 10-K/A and
  the FY2010 10-K) now also cite the FY2004-FY2006 share counts the new vintages use. 165 analyses change only in that text.
- **Anachronism list:** Apple product and software names from 2012 to 2016 join it (from OS X Mountain Lion and iOS 6 to the
  iPhone 7 and AirPods). Of all existing models, only "Apple Watch" appears, in the FY2015 vintage's product list from 2015-10-29.
- **Year-check warnings:** "2013" on the 36 dates from 2012-04-26 to 2012-12-28 (the 10-Q's repurchase program "beginning in
  2013" and, from 2012-11-02, the 10-K's "first quarter of 2013"): the company's plans, public before each date.

Controls: altering one value of each new print, Q4 full-year figure, guide, vintage, dividend, program statement and the split
changes no date before its publication and changes the first weekly date on or after it (50 of 52). The other two are the
Q4 FY13 and Q4 FY15 full-year figures. Their 10-K came out on the next trading day, which is also the first weekly date, so the
vintage replaces them on every weekly date. Built by date on the print's own day (2013-10-29, 2015-10-28), each changes that
model. A guide for the next fiscal year first shows on the first date with that year current, and the split from its effective
date. The 209 dates of 2008-2011 rebuild with byte-identical reports.

Seen in the build (method behaviour, not tuned):
- **CHEAP on 191 of 209 dates, BUY on all.** 2012 and 2013 read CHEAP on all 104. FAIR on 13 dates from 2014-07-11 to
  2014-10-10 (except 2014-07-18), where the conservative case fell to -5% to -13%: BASE was +2.7%, then +0.7%/yr on the Q3 and Q4
  FY14 guides, and the stock stood at 16.7-18.1x FY13's $5.68 against a 15.8-15.9x median. FAIR on 5 dates in 2015 (2015-02-20, 04-24, 05-22, 05-29,
  07-17), where the price stood just over 100% above the EPP floor.
- **The EPS anchor and the multiple.** On the last full year's EPS the stock traded at 11.5-25.3x in 2012 (the 11th-58th
  percentile; 25.3x on 2012-09-21 at $700.09), 8.8-14.1x in 2013 (the 1st-39th; 8.8x on 2013-04-19 at $390.53), 12.6-18.4x in
  2014 and 11.4-20.5x in 2015.
- **Below the floor and the BEAR price in 2013.** The price sat below the EPP floor on 19 dates from 2012-11-16 to 2013-07-25
  (as far as -11.5%) and below the BEAR price (Ratio B negative) on 20 dates from 2013-01-25 to 2013-07-19: FY12's $44.15 at the
  10th-percentile multiple, while BASE fell to +4.2%, then -4.4% and -4.2%/yr on the Q2-Q4 FY13 ranges.
- **BASE follows the quarter guides less dilution:** +35.2%/yr on the Q1 FY12 guide, then +28.6%, +15.8% and +17.1%; +9.3% (Q1
  FY13), +4.2%, -4.4% and -4.2%; +1.6% (Q1 FY14), -3.4%, +2.7% and +0.7%; +11.7% (Q1 FY15; +12.7% from the FY2014 vintage),
  +17.0%, +25.3% and +18.5%; +3.2% on the Q1 FY16 range. The decade's share count turns from dilution (-3.2%/yr FY03-FY11) to a buyback (+0.65%/yr FY06-FY15) only with the
  FY2015 vintage.
- **BULL, XBULL and BEAR move with the window.** BULL is the decade EPS CAGR: +107.7% and +101.7%/yr from FY2003's $0.08, +69.7%
  from FY2004 (the FY2013 vintage; +63.0% with FY14 from the Q4 print), +45.4% from FY2005 and +45.1% from FY2006. XBULL, FY03-FY05's +340%/yr, becomes FY04-FY06's +158% and from the
  FY2014 vintage FY09-FY11's +74.5%. BEAR, flat while every year grew, applies FY13's -10.0% twice from the FY2013 vintage. Ratio B
  ran from -0.02 to 0.41.
- **The EPP floor falls from 14x to 9x** (12x from the Q4 FY12 print, 11x on 2013-01-04 and 2013-01-11, 10x from 2013-01-25, 9x on
  2015-12-31) as the window takes in 2008-2013's low multiples.
- **Display quirks:** after the split the EPS check prints FY13's EPS to three decimals ("$5.679", the shared `money` format
  for a split that leaves a fraction of a cent), and catalyst (5) quotes the program as announced ($3.29 before the split).

How far each call moves the classes (the affected dates rebuilt with one encoding changed; no outcome consulted):
- an operating-margin step derived from each guide list (revenue and gross-margin midpoints less operating expenses, against the
  year-ago quarter's margin) would change 2 of the 154 classes from 2013-01-25 (2014-07-03 and 2014-07-18, CHEAP to FAIR) and no
  tier;
- carrying the March 2012 policy's $2.65 as a dividend from the Q2 FY12 10-Q would change none of the 13 dates to 2012-07-20;
- not counting the Q4 FY12 print on its own day (2012-10-26) would change neither class nor tier;
- the re-presentations as vintages would change only the bridge (display only).

Judgement calls that could carry hindsight:
- keeping the guide lists' operating-expense and tax items out of the inputs (the call that moves the most classes: 2 of 209);
- dating the first dividend from its declaration, not from the policy stated in the Q2 FY12 10-Q (no class moves);
- treating the two segment re-presentations as adding nothing;
- reading the Q1 FY13 guide against the 14-week Q1 FY12 as published;
- DURABLE rather than CYCLICAL (the class label only), and CLOUD and STREAMING as outside Apple's scope.

### AAPL 2016-2019: unit sales end, a guidance letter, tax reform, a 53-week year

```bash
python3 retro/build_aapl.py --weekly 2016-01-04 2019-12-31                  # 209 dates, 2016-01-08 .. 2019-12-31
```

Every 8-K, 8-K/A, 10-Q, 10-K and proxy filed on Apple's CIK from 2016-01-01 to 2019-12-31 was read directly (74 filings with
the shelf registrations and note listings), with the third-party solicitations (PX14A6G) and the 10-Qs and 10-Ks searched for
forward-looking statements. 655 strings were checked with `verbatim.py` against their own filings. 232 structured checks read
each print's statements and each Q4 print's full-year figures back from the XBRL of the 10-Q or 10-K filed with it: 226 match,
and the other six are dividends paid, which the XBRL tags without dividend equivalents (each 10-Q's own cash flow statement
prints the release's figure). 141 more read the units and the product or category net sales back from each 10-Q's own table
and the four quarters' units back to each 10-K's year; the four quarters' net sales and Mac net sales also sum to each 10-K's.
Every source's date comes from EDGAR's acceptance time. Thresholds and signals are unchanged. Decided before any 2016-2019 date
was built or scored:

- **Four vintages, ten years each.** The FY2016 10-K (accepted 2016-10-26 16:42 ET, dated 2016-10-27) gives FY2012-FY2016, the
  FY2017 10-K (2017-11-03 08:01 ET, before the open, dated that day) FY2013-FY2017, the FY2018 10-K (2018-11-05 08:01 ET, dated
  that day) FY2014-FY2018 and the FY2019 10-K (2019-10-30 18:12 ET, dated 2019-10-31) FY2015-FY2019. Each earlier year comes
  from the latest 10-K that reports it. The history moves to FY2007-FY2016, FY2008-FY2017, FY2009-FY2018, then FY2010-FY2019.
  - First-year diluted shares: FY2007's 889,292K (FY2011 10-K), FY2008's 902,139K (FY2012 10-K) and FY2009's 907,005K (FY2013
    10-K), all before the split, and FY2010's 6,472,983K (FY2014 10-K).
  - Every year is GAAP: Apple published no figure excluding a one-off. The FY2018 10-K gives the Tax Cuts and Jobs Act's effect
    as a dollar amount ("increased the Company's provision for income taxes by $1.5 billion during 2018"), not as an EPS without
    it, so FY18 stays at $11.91 (the FY2005 rule: no figure is derived from a published amount).
- **The new revenue standard restates nothing.** Apple adopted it in Q1 FY19, full retrospective, but "did not restate total net
  sales in the prior periods presented". It moved the amortization of Maps, Siri and free iCloud services from Products to
  Services and recast the Q1 FY18 split (Mac $6,824M; $6,895M in the Q1 FY18 data sheet). No new vintage; each print's growth is
  against its own release's year-ago column (the restated-base rule).
- **Prints.** Every release came after the close, so each print is dated the next trading day. Q4 FY17, Q1 FY18 and Q4 FY18 came
  on Thursdays: the print is dated Friday, no trading day follows in its week, and it counts on its own day (the Q4 FY12 rule).
  The FY2017 10-K came out before the open on that Friday, so on 2017-11-03 it replaces the Q4 print's full-year figures, and
  the FY2019 10-K was filed on the evening of the Q4 FY19 release, so both are dated 2019-10-31.
- **Guides, one quarter at a time, as lists.** Each release gives the next quarter's revenue and gross-margin ranges, operating
  expenses, other income/(expense) and a tax rate. Revenue is read against the year-ago quarter's own release: Q2 FY16 -13.8% to
  -8.6%, Q3 -17.3% to -13.3%, Q4 -11.7% to -7.8%, Q1 FY17 +0.2% to +2.8%, Q2 +1.9% to +5.8%, Q3 +2.7% to +7.4%, Q4 +4.6% to
  +11.0%, Q1 FY18 +7.2% to +11.0%, Q2 +13.4% to +17.2%, Q3 +13.4% to +17.8%, Q4 +14.1% to +17.9%, Q1 FY19 +0.8% to +5.3% (then
  -4.9%, below), Q2 -10.0% to -3.5%, Q3 -1.4% to +2.3%, Q4 -3.0% to +1.7%, Q1 FY20 +1.4% to +6.2%.
  - Still no fiscal-year guide, so the last full year's EPS stands: FY15's $9.22 to 2016-10-25, FY16's $8.31 to 2017-11-02,
    FY17's $9.21 to 2018-11-01, FY18's $11.91 to 2019-10-30, FY19's $11.89 after.
  - The tax-rate items ("approximately 15 percent", from 2018 "before discrete items") stay display only, as does the Q1 FY18
    10-Q's rate "for the remainder of 2018" (a part of the year, the 2009 half-year rule).
- **The letter of 2019-01-02.** An 8-K (item 2.02, accepted 16:30 ET, dated 2019-01-03) revised the Q1 FY19 guide after the
  quarter had ended and before it was reported: revenue "approximately $84 billion" (from $89-93 billion), gross margin about
  38%, operating expenses about $8.7 billion, other income about $550 million, tax rate about 16.5% before discrete items. New
  numbers, not words, so it is a guide of its own and each field it states replaces the release's (the 8-K of 2013-09-23 restated
  its ranges in words, which kept them): -4.9% on Q1 FY18's $88.293B from 2019-01-04 to 2019-01-25. Its share count
  ("approximately 4.77 billion"), net cash and EPS words have no field.
- **The 53-week year.** Fiscal 2017 had 53 weeks, a 14th in Q1 FY17. Growth is as published, and the week is noted only where a
  filing public by that date states it (the LOW 53rd-week rule): the Q1 FY18 guide (the FY2017 10-K) and the Q1 FY18 print (its
  10-Q, before the open on the print's day). The Q4 FY16 release, the FY2016 10-K and the Q1 FY17 release do not mention it; the
  Q1 FY17 10-Q, the first that does, is dated the next trading day. Nothing is back-filled.
- **One-time items stay in** (no figure excluding them was published): Q1 FY16 Services include $548 million received from Samsung
  (the supplemental material gives Services "excluding" it); Q4 FY17 Services a favorable one-time adjustment of $640 million and
  Q3 FY18 Services a one-time item of $236 million (each quarter's own data sheet); Q1 FY18 the tax act's $2.6 billion provisional
  charge (the 10-Q). From Q1 FY16 a release may carry a supplemental exhibit (non-GAAP constant-currency growth, installed-base
  purchases): display material, no input.
- **No unit sales from Q1 FY19.** From that release Apple reports net sales by category only, with no data sheet.
  - Mac units cannot be derived from what is published, and Mac net sales is a different measure (the ACN headcount and UNP GTM
    rules). So the Mac unit signal keeps its name, thresholds and weight and, with no value, scores BASE (2/4), the engine's value
    for a slot without information (the theme slot with no live theme). It shows "n/r".
  - The text shows Mac and iPhone net sales growth from the category table instead (`mac_sales_pct`, `iphone_sales_pct`, display
    only); catalyst (4) has no units, and the FY2019 vintage has no full-year Mac units.
- **Dividends and the capital return program come from the Q2 releases** (no separate 8-K in these years): $.57 (2016-04-27),
  $0.63 (2017-05-03), $0.73 (2018-05-02), $0.77 (2019-05-01), each from the first filing that states the rate. Catalyst (5) shows
  the $250 billion and $300 billion programs (2016, 2017), then a new $100 billion repurchase authorization (2018) and an
  additional $75 billion (2019). The programs' end dates are left out, as before.
- **No theme.** CLOUD (on-premise enterprise IT), STREAMING (linear TV), ECOMMERCE (physical retail) and ENERGY_TRANSITION are
  outside Apple's scope; the 10-Ks name iCloud, Apple Music and, in FY2019, Apple TV+ as Apple's own services. The watch list stays
  empty, DURABLE, risk 2.
- **The franchise text follows each 10-K.** From FY2016 "macOS" replaces "OS X", from FY2017 "aggressive price competition"
  replaces "price cutting", and from FY2018 the "only authorized maker of hardware" sentence is gone: the 10-K's "minority market
  share in the global smartphone, tablet and personal computer markets" takes its place. From the FY2016 10-K no store count is
  given, so the text quotes the last one (463, FY2015 10-K) as such (the ACN headcount rule).
- **Adds nothing:**
  - the debt offerings and note listings (among them the euro notes moved from NYSE to Nasdaq, 2019-03-14) and the shelf
    registrations;
  - the vote, officer and director 8-Ks (a new general counsel, 2017-10-12; the head of retail, 2019-02-06; a director,
    2019-09-13), the bylaw amendments (proxy access, 2016-12-15) and the e-book derivative settlement notice (8-K and 8-K/A of
    2018-05-07);
  - the proxies, whose executive cash-incentive goals are for years already finished, and the shareholder solicitations (a
    greenhouse-gas report, board diversity, proxy access);
  - the 10-Qs' and 10-Ks' gross-margin sentences (they repeat the release ranges) and their capital-expenditure, lease,
    deferred-tax and manufacturing-commitment estimates (no field);
  - the EU State Aid decision (2016-08-30) and the escrow funded from 2018 (a contingency on the balance sheet, no field);
  - the Q4 FY18 release's Services growth excluding the $640 million (the signals use total net sales).
- **An engine revision for the missing units, text only for earlier dates.** `score_signal` scores a value of `None` as BASE, and
  every line that prints Mac, iPhone or iPad units has a branch for a print without them (dashboard, bear anatomy, conservative
  case, key trigger, volatility text, catalysts (1) and (4), summary). The builder adds the two category growth rates to `LATEST`
  only where a print has them. All 418 reports of 2008-2015 rebuild byte-identical.
- **Text-only change to 2008-2015:** besides the engine text, four source descriptions (the FY2011-FY2014 10-Ks) now also cite the
  FY2007-FY2010 share counts the new vintages use. 219 analyses change only in that text.
- **Anachronism list:** Apple product and software names from 2016 to 2020 join it (from macOS and iOS 10 to the iPhone 12 and the
  M1 chip), and "Tax Cuts and Jobs Act" (2017-11-02). Of the 3,364 existing models of all tickers only that name appears, in UNP
  models from 2018-01-26 and LOW models from 2018-03-01, after it.
- **ISO weeks:** the batch runs from 2016-W01 to 2020-W01; 2019-12-31 covers 2020-W01, so a 2020 batch starts on 2020-01-06.

Controls: altering one value of each new print, Q4 full-year figure, guide, vintage, dividend and program statement changes no
date before its publication (49 of 49) and changes the first weekly date on or after it (46 of 49). The other three are Q4
full-year figures that the 10-K replaces by then: Q4 FY16's 10-K came out on the next trading day, the first weekly date (built by
date on the print's own day, the figure changes that model), and the FY2017 and FY2019 10-Ks are dated the same day as their Q4
print, so those figures never show. The letter of 2019-01-02 first shows on 2019-01-04, a guide for the next fiscal year on the
first date with that year current. The 418 dates of 2008-2015 rebuild with byte-identical reports, and the 2008 dates of ACN, UNP
and LOW rebuild unchanged. A scan of all 627 AAPL models for 79 values of the new prints, guides and vintages finds none before
its publication, and the firewall at 2020-01-01, 2018-11-03 and 2017-02-01 changes none of the 627, 566 and 474 earlier models.

Seen in the build (method behaviour, not tuned):
- **AAPL reads RICH for the first time.** CHEAP on 56 of the 209 dates, FAIR on 25, RICH on 128 (2008-2015 had no RICH date). The
  tier reads BUY 85, ACCUMULATE 43, WATCHLIST 38, AVOID 43.
  - 2016: CHEAP on 48 dates, FAIR on 4 (2016-10-14, 10-21, 12-23, 12-30), BUY on all. On FY15's $9.22 the stock traded at
    9.8-12.8x (the 5th-46th percentile of its own range).
  - 2017: FAIR from 2017-01-06 to 2017-03-24 (12 dates), RICH from 2017-03-31 (40), as the price rose from $118 to $175 at
    14.2-19.7x (the 66th-93rd percentile).
  - 2018: RICH on 43 dates, AVOID on 29. From the Q4 FY17 print to 2018-11-01 the anchor is FY17's $9.21 while the FY18 quarters
    run ahead (Q1 FY18 $3.89 against $3.36): 17.0-24.7x, the 85th-100th percentile. FAIR on 2018-02-02, 02-09 and from 2018-11-16
    to 12-07; CHEAP from 2018-12-14 to 12-28 at 12.7-13.9x FY18's $11.91.
  - 2019: CHEAP on the 5 dates from 2019-01-04 to 2019-01-31 (12.4-14.0x), FAIR on 2019-02-08, 02-15 and 05-31, RICH on 45 as the
    price rose from $148 to $294; at the 100th percentile of its own range from 2019-10-04.
- **BASE follows the quarter guides plus the buyback:** -10.5%, -14.6% and -9.1%/yr on the Q2-Q4 FY16 guides; +2.9% (Q1 FY17),
  +5.2%, +6.4% and +9.2%; +11.2% (Q1 FY18), +17.4%, +17.7% and +18.1%; +5.4% (Q1 FY19; +5.7% from the FY2018 vintage), -2.2% on
  the letter, then -4.1%, +3.1% and +2.0%; +7.5% on the Q1 FY20 guide. The decade's buyback rises from 0.65%/yr (FY06-FY15) to
  1.38%, 2.07%, 2.69% and 3.75%/yr (FY10-FY19).
- **BULL, XBULL and BEAR move with the window.** BULL is the decade EPS CAGR: +45.1%/yr (FY06-FY15), then +34.9% (FY07-FY16),
  +28.4% (FY08-FY17), +27.9% (FY09-FY18) and +20.9% (FY10-FY19). XBULL is FY09-FY11's +74.5%/yr, then FY10-FY12's +70.9% from the
  FY2019 vintage. BEAR applies FY13's -10.0% twice throughout.
- **The price passes the BULL case in late 2019.** Ratio B reaches 33.6x on 2018-08-31 and 657x on 2019-11-15, and is `inf` on
  the 6 dates from 2019-11-29. No date sits below the EPP floor (9-10x) or the BEAR price; the closest is 2016-05-06, 0.6% above
  the floor.
- **The proxy composite sits at 2.00 on most dates:** against the FY1998-FY2007 thresholds every signal reads BASE. It is 2.50 on
  the three January 2016 dates (Q4 FY15's +189bp gross margin) and 2.30 from the Q3 FY18 print to the Q1 FY19 print (net sales
  and net sales other than Macs at BULL). The unreported Mac slot changes none of it.
- **Display quirks:** a negative BASE growth prints as "EPS +-4.1%/yr" (as in 2009); Q3 FY19's net sales other than Macs prints as
  -0.0% (a 0.04% decline, kept with its sign).

How far each call moves the classes (the affected dates rebuilt with one encoding changed; no outcome consulted):
- re-weighting the other five signals instead of scoring the unreported Mac slot BASE would change none of the 49 classes or tiers
  from 2019-01-31 (every other signal also reads BASE);
- carrying Q4 FY18's -1.6% Mac unit growth instead would change none (it also scores BASE);
- not treating the letter of 2019-01-02 as a guide (the $89-93 billion range standing to the Q1 FY19 print) would change none of
  the 4 dates;
- reading the Q1 FY18 guide against Q1 FY17 scaled to 13 weeks (a figure derived from others) would change none of the 13 dates.

Judgement calls that could carry hindsight:
- scoring a measure the company stopped publishing at BASE, with no substitute and no re-weighting (no class moves);
- treating the letter as a guide (no class moves);
- keeping GAAP through the tax act and the one-time Services items;
- noting the 14th week only from the first filing that states it, and leaving growth as published (no class moves);
- DURABLE rather than CYCLICAL (the class label only), and CLOUD, STREAMING and ECOMMERCE as outside Apple's scope.

### AAPL 2020-2023: no guidance, a withdrawn revenue range, the 4-for-1 split, a second 53-week year

```bash
python3 retro/build_aapl.py --weekly 2020-01-06 2023-12-31                  # 208 dates, 2020-01-10 .. 2023-12-29
```

Every 8-K, 10-Q, 10-K and proxy filed on Apple's CIK from 2020-01-01 to 2023-12-31 was read directly (74 filings with the
third-party solicitations, the IRANNOTICEs and the 2021 shelf), and the 10-Qs and 10-Ks were searched for forward-looking
statements. 557 strings were checked with `verbatim.py` against their own filings. 229 structured checks read each print's
statements and each Q4 print's full-year figures back from the XBRL of the 10-Q or 10-K filed with it, and all match. Two of them
are Q2 and Q3 FY20's "commercial paper and repurchase agreement(s)", tagged as other short-term borrowings. Six are Q4 FY21-FY23
net sales and gross margin: the FY2021-FY2023 10-Ks give no quarterly figures, so each is the year less the Q3 10-Q's nine
months. Those three Q4 EPS figures have no XBRL counterpart and rest on the verbatim check. 144 more read each quarter's net sales
by category back from its 10-Q, and sum the four quarters (total and each category) to each 10-K's year. Every source's date comes
from EDGAR's acceptance time. Thresholds and signals are unchanged. Decided before any 2020-2023 date was built or scored:

- **Four vintages, ten years each.** The FY2020 10-K (accepted 2020-10-29 18:06 ET, dated 2020-10-30) gives FY2016-FY2020 in its
  selected financial data, restated for the split. The FY2021 (2021-10-28 18:04 ET, dated 2021-10-29), FY2022 (2022-10-27 18:01
  ET, dated 2022-10-28) and FY2023 (2023-11-02 18:08 ET, dated 2023-11-03) 10-Ks reserve Item 6, so each supplies the three years
  of its income statement (the ACN FY21 rule), and the earlier years keep the latest 10-K that reported them. The history moves to
  FY2011-FY2020, FY2012-FY2021, FY2013-FY2022, then FY2014-FY2023. Each 10-K came the evening of its Q4 release and is dated the
  same day as the Q4 print, so the release's full-year figures never show (as in FY2017 and FY2019).
  - First-year diluted shares: FY2011's 6,556,514K (FY2015 10-K), FY2012's 6,617,483K (FY2016 10-K), FY2013's 6,521,634K (FY2017
    10-K) and FY2014's 6,122,663K (FY2018 10-K), all on the 7-for-1 basis.
  - Every year is GAAP. FY20 includes "a one-time adjustment of U.S. foreign tax credits" that lowered its tax rate (the Q1 FY20
    10-Q, the FY2020 10-K); Apple published no figure without it (the Fremont rule).
- **The 4-for-1 split.** Approved in the Q3 FY20 release (accepted 2020-07-30 18:55 ET, dated 2020-07-31): "trading will begin
  on a split-adjusted basis on August 31, 2020", the price data's split date. From that date every per-share fact published before
  it is divided by 4 and every share count multiplied by 4 (the UNP rule): FY19's $11.89 stands as $2.9725 from 2020-08-31 to
  2020-10-29. The FY2020 10-K restates FY2016-FY2019, so those years enter as restated ($2.08, $2.30, $2.98, $2.97; not $8.31 / 4
  and so on), and FY2011-FY2015 from the earlier 10-Ks are divided. Print and program text is not restated (the UNP 2014 rule). The
  8-K of 2020-08-07 (the articles amended for the split) adds nothing.
- **Dividends,** each from the first filing that states the rate: $0.82 (Q2 FY20 release, 2020-05-01, "an increase of 6
  percent"), divided by 4 from the split; $0.205 (Q4 FY20 release, 2020-10-30, the first declaration after it, as in 2014); $0.22,
  $0.23 and $0.24 (the Q2 FY21-FY23 releases). A builder change, text only: a rate declared before a split was announced says
  "divided by 4 for the 4-for-1 split effective 2020-08-31" from that date on. A note written into the fact would have shown the
  split, announced on 2020-07-30, on the dates from 2020-05-01; the 2014 rate came in the same 8-K as its split, so no earlier note
  changes. Catalyst (5) shows the programs: $50 billion more (2020), $90 billion more (2021, 2022), then a new $90 billion program
  (2023).
- **One guide, then none.** The Q1 FY20 release (accepted 2020-01-28 16:30 ET, dated 2020-01-29) gives Q2 FY20 as before: revenue
  $63.0-67.0 billion (+8.6% to +15.5% on Q2 FY19's $58.015B), gross margin 38-39%, operating expenses $9.6-9.7 billion, other
  income $250 million, a 16.5% tax rate. From the Q2 FY20 release (2020-04-30) to the end of 2023 no release, 10-Q or 10-K gives any
  guidance or outlook, in numbers or in words (the conference calls are not filings). The builder's no-guide rule applies (UNP
  2009, LOW 2020): the last full year's EPS stands, BASE growth and the growth factor take the latest quarter's net sales growth,
  and there is no margin step. A builder change, text only: a print without outlook words says its release "gives none", with no
  quote (no earlier print lacks them).
- **The update of 2020-02-17.** An 8-K (item 7.01, accepted 2020-02-18 06:24 ET, before the open; 2020-02-17 was a market
  holiday): "we do not expect to meet the revenue guidance we provided for the March quarter", with no new number. That is not a
  guide restated in words, which keeps the last range (the 8-K of 2013-09-23 put revenue "near the high end of the previously
  provided range"): it says the range will not hold. As with LOW's withdrawn guide, the field it names is void and the no-guide
  rule applies to it. From 2020-02-21, BASE takes Q1 FY20's +8.9% instead of the range's +12.1% midpoint. The other fields (gross
  margin, operating expenses, other income, tax rate) are display only and not mentioned, so they stand. A builder change
  (`q_guide.withdrawn`): a guide may withdraw named fields of its quarter, which voids them in every earlier guide for that
  quarter. No earlier guide withdraws anything, so no earlier date changes.
- **Prints.** Every release came after the close, so each print is dated the next trading day. Twelve came on Thursdays (Q2-Q4
  FY20, Q4 FY21, Q1-Q4 FY22, Q1-Q4 FY23): the print is dated Friday and counts on its own day (the Q4 FY12 rule). No unit sales, as
  from Q1 FY19: the Mac unit slot scores BASE, and Mac and iPhone net sales growth are display only. Q2 and Q3 FY20's balance sheets
  name the line "commercial paper and repurchase agreement(s)", and the cash-return text uses that name.
- **The second 53-week year.** Fiscal 2023 had 53 weeks, a 14th in Q1 FY23. Growth is as published (-5.5% against the 13 weeks of
  Q1 FY22), and the week is noted where a filing public by then states it (the LOW 53rd-week rule): the FY2022 10-K ("which will
  occur in the first quarter of the Company's fiscal year ending September 30, 2023"), the Q1 FY23 10-Q (dated the print's day) and
  the FY2023 vintage.
- **No theme.** GENAI (live from 2022-11-30) is scoped to software seats, IT services and BPO hours, professional information,
  search, education content and mobility; EV to combustion powertrains, parts and fuel; CRYPTO to payments networks, banks and
  exchanges; GLP1 to snacks, beverages and medical devices; CLOUD, STREAMING, ECOMMERCE and ENERGY_TRANSITION as before. None
  names Apple's products. The watch list stays empty, DURABLE, risk 2.
- **The franchise text follows each 10-K.** The FY2020-FY2023 10-Ks keep the three quoted phrases word for word ("designs and
  develops nearly the entire solution", "a minority market share in the global smartphone, personal computer and tablet markets",
  "highly competitive global markets characterized by aggressive price competition"), and give no store count.
- **Adds nothing:**
  - the update of 2022-11-06 (8-K of 2022-11-07, before the open), which expects lower shipments of two iPhone models "than we
    previously anticipated": words, and no guide in force (the ACN non-earnings 8-K rule);
  - the debt offerings (item 8.01) and the 2021 shelf registration;
  - the officer, director, bylaw and vote 8-Ks, among them the articles amendment of 2020-08-07;
  - the proxies, the shareholder solicitations and the IRANNOTICEs;
  - the 10-Qs' and 10-Ks' expectations without a field (deferred revenue realization, unrecognized tax benefits, hedges, the EU
    State Aid escrow and the timing of the ECJ's decision);
  - COVID-19 beyond the prints and the update (the UNP 2020 rule: a caveat without a figure adds nothing).
- **Text-only change to 2015-2019:** four source descriptions (the FY2015-FY2018 10-Ks) now also cite the FY2011-FY2014 share
  counts the new vintages use. 219 models and analyses change only in that text, and every report rebuilds byte-identical.
- **Anachronism list:** Apple product and software names first seen from 2021 to 2025 join it (from AirTag and iOS 15 to the
  iPhone 17 and the M5 chip, with M2, M3, Vision Pro and Apple Intelligence), and "Omicron" (2021-11-26). None of the 3,573
  existing models of any ticker contains one.
- **ISO weeks:** the batch runs from 2020-W02 to 2023-W52; a 2024 batch starts on 2024-01-01.

Controls: altering one value of each new print, Q4 full-year figure, guide, the withdrawal, the split, each vintage, dividend and
program statement changes no date before its publication (36 of 36) and changes the first weekly date on or after it (32 of 36).
The other four are the Q4 full-year figures, which the 10-K replaces on the same day. The withdrawal first shows on 2020-02-21, and
the split on 2020-09-04, the first weekly date after its effective date. The 627 dates of 2008-2019 rebuild with byte-identical
reports, and the 2008 dates of ACN, UNP and LOW rebuild unchanged. A scan of all 835 AAPL models for 76 values of the new prints,
guide, withdrawal, vintages, split, dividends and programs finds none before its publication. The firewall, which now also plants
a later withdrawal of every guided field, changes none of the 835, 722 and 635 models before 2024-01-01, 2021-11-01 and
2020-03-01.

Seen in the build (method behaviour, not tuned):
- **RICH on every date.** All 208 dates read RICH; the tier reads AVOID on 202 and WATCHLIST on 6 (2022-12-16 to 2023-01-20, Ratio
  B 1.27-1.63x). The multiple stands at the 95th-100th percentile of its own decade in 2020-2021 and at the 72nd-98th in
  2022-2023: 19.3-42.0x in 2020 (the lowest 19.3x on 2020-03-20, at $229.24), 26.7-47.0x in 2021, 21.3-31.1x in 2022 and
  21.2-32.2x in 2023.
- **The last full year's EPS is the anchor all along:** FY19's $11.89 ($2.973 after the split) to 2020-10-29, FY20's $3.28 to
  2021-10-28, FY21's $5.61 to 2022-10-27, FY22's $6.11 to 2023-11-02, FY23's $6.13 after. Through 2021 the stock trades at
  26.7-47.0x FY20's $3.28 while the FY21 quarters run ahead (Q1 FY21 $1.68 against $1.25).
- **BASE follows each quarter's net sales growth plus the buyback:** +7.5%/yr on the Q1 FY20 guide and +15.8% on Q2 FY20's, +12.6%
  after the update withdrew its revenue range, then +4.2% (Q2 FY20's +0.5%), +14.6%, +5.6%, +26.0% (Q1 FY21's +21.4%), +58.2% (Q2
  FY21's +53.6%), +41.0%, +33.9%, +16.3%, +13.7%, +7.0%, +13.4%, -0.2% (Q1 FY23's -5.5%), +2.8%, +3.9% and +4.3%. The decade's
  buyback rises from 3.75%/yr (FY10-FY19) to 4.58%, 5.14%, 5.35%, then 4.98%/yr. As with UNP in 2009 and LOW in 2020, the
  fallback carries one quarter's growth for two years. BASE lifts BULL to its own rate (the rule's floor) on the 65 dates from
  2021-01-29 to 2022-04-22, and XBULL too on the 26 from 2021-04-30 to 2021-10-22.
- **BULL, XBULL and BEAR move with the window.** BULL is the decade EPS CAGR: +20.9%/yr (FY10-FY19), +14.3% (FY11-FY20), +15.1%
  (FY12-FY21), +17.6% (FY13-FY22), +16.0% (FY14-FY23). XBULL is FY10-FY12's +70.9%/yr, then FY13-FY15's +27.4% (FY2020 vintage) and
  FY19-FY21's +37.4% (from the FY2021 vintage). BEAR applies FY13's -10.0% twice through the FY2021 vintage, then FY16's -9.8%.
- **Ratio B is `inf` on 106 dates,** the last on 2022-09-09: the price stands above the BULL case.
- **The proxy composite leaves 2.00 from the Q1 FY21 print.** Against the FY1998-FY2007 thresholds the gross-margin change reads
  BULL from Q1 FY21 to Q2 FY22 and from Q3 FY23, net sales and other net sales from Q1 FY21 to Q4 FY21, and the operating-margin
  change from Q2 FY21 to Q1 FY22: 2.50 on 13 dates, 2.65 on 39, 2.35 on 13, 2.20 on 35, and 2.00 on the other 108. The unreported
  Mac slot changes none of it.

How far each call moves the classes (the affected dates rebuilt with one encoding changed; no outcome consulted):
- reading the update of 2020-02-17 as words only (the $63.0-67.0 billion range standing to the Q2 FY20 print) would change none of
  the 10 dates;
- re-weighting the other five signals instead of scoring the unreported Mac slot BASE would change none of the 208 classes or
  tiers;
- Q1 FY23's net sales growth on 13 weeks (-12.2%, a figure derived from others) would change none of the 13 dates.

Judgement calls that could carry hindsight:
- treating the update of 2020-02-17 as withdrawing the revenue range (no class moves);
- scoring the unreported Mac slot at BASE, as from Q1 FY19 (no class moves);
- leaving the 14-week Q1 FY23 as published (no class moves);
- keeping GAAP through the one-time adjustment of U.S. foreign tax credits (no figure without it was published; not rebuilt);
- DURABLE rather than CYCLICAL (the class label only), and GENAI, EV and CRYPTO as outside Apple's scope.

### AAPL 2024-2026: still no guidance, the State Aid tax charge, tariff refunds, a 13-week first quarter

```bash
python3 retro/build_aapl.py --weekly 2024-01-01 2026-10-25                  # 147 dates, 2024-01-05 .. 2026-10-23
```

Every 8-K, 8-K/A, 10-Q, 10-K and proxy filed on Apple's CIK from 2024-01-01 to 2026-10-29 was read directly (55 filings with
the third-party solicitations and the 2024 shelf), and the 10-Qs and 10-Ks were searched for forward-looking statements. 368
strings were checked with `verbatim.py` against their own filings. 149 structured checks read each print's statements back from
the XBRL of the 10-Q or 10-K filed with it, and all match. The FY2024 and FY2025 10-Ks give no quarterly figures, so four more
checks take Q4 FY24 and Q4 FY25 net sales and gross margin as the year less the Q3 10-Q's nine months; both Q4 EPS figures rest
on the verbatim check. 102 more read each quarter's net sales by category back from its 10-Q, and sum the four quarters (total
and each category) to each 10-K's year. Every source's date comes from EDGAR's acceptance time. Thresholds and signals are
unchanged, and no code changed. Decided before any 2024-2026 date was built or scored:

- **Two vintages, ten years each.** The FY2024 10-K (accepted 2024-11-01 06:01 ET, before the open; dated 2024-11-01) and the
  FY2025 10-K (2025-10-31 06:01 ET; dated 2025-10-31) reserve Item 6, so each supplies the three years of its income statement
  and the earlier years keep the latest 10-K that reported them. The history moves to FY2015-FY2024, then FY2016-FY2025.
  - First-year diluted shares: FY2015's 5,793,069K (FY2019 10-K, on the 7-for-1 basis) and FY2016's 22,001,126K (FY2020 10-K).
  - Each 10-K came before the open the morning after its Q4 release and is dated the same day as the Q4 print, so the
    release's full-year figures never show (as in 2020-2023).
- **FY24 excludes the State Aid tax charge** (the ACN rule: a company-published figure excluding a one-off replaces GAAP).
  - The Q4 FY24 release (accepted 2024-10-31 16:30 ET, dated 2024-11-01) reconciles the quarter and the year "when excluding
    the one-time charge recognized during the fourth quarter of 2024 related to the impact of the reversal of the European
    General Court's State Aid decision": diluted EPS $1.64 for the quarter (GAAP $0.97) and $6.75 for the twelve months (GAAP
    $6.08). The FY2024 10-K calls it "a one-time income tax charge of $10.2 billion, net". FY24 enters at $6.75, with the
    tax rate excluding the charge, 15.79% ($19,503M on $123,485M; GAAP 24.09% in the note).
  - The FY2025 vintage keeps FY24 at $6.75 (an adjusted year keeps its figure, the LOW rule); the Q4 FY25 release reconciles it
    again. Q4 FY24's print shows $1.64, and Q4 FY25's $1.85 compares with it, as the release does ("up 13 percent year over
    year on an adjusted basis"; display only). Every other year is GAAP.
  - The 8-K of 2024-09-10 (item 7.01, accepted 09:06 ET, before the open) expects a one-time charge "of up to approximately $10
    billion": a dollar amount with no guide in force, so it adds nothing, and FY23's $6.13 stands to the Q4 FY24 print.
- **Tariff refunds in Q3 FY26.** The Q3 FY26 release gives gross margin 50.1% "including a favorable impact of approximately 2
  percentage points from tariff refunds", and EPS $2.02 that "included a favorable impact of $0.11 from tariff refunds". These
  are impacts, not figures excluding the refunds, so GAAP stands and nothing is derived (the Fremont rule; LOW's Q2 FY26
  refunds the same).
- **Still no guidance.** No release, 10-Q or 10-K from 2024-01-01 to 2026-10-23 gives any guidance or outlook, in numbers or in
  words. The no-guide rule applies on every date: the last full year's EPS stands, BASE growth and the growth factor take the
  latest quarter's net sales growth, and there is no margin step.
- **Prints.** All eleven releases (Q1 FY24 to Q3 FY26) came on Thursdays after the close (8-Ks accepted at 16:30 ET): each print
  is dated Friday and counts on its own day (the Q4 FY12 rule). The 10-Qs followed the same evening through Q3 FY24 (18:03-18:04
  ET) and before the next open from Q1 FY25 (06:00-06:01 ET); each is dated the print's day. No unit sales: the Mac unit slot
  scores BASE, and Mac and iPhone net sales growth are display only.
- **A 13-week first quarter.** Q1 FY24 had 13 weeks against Q1 FY23's 14. Growth is as published (+2.1%). The Q1 FY24 10-Q,
  dated the print's day, states it ("The Company's fiscal years 2024 and 2023 span 52 and 53 weeks, respectively."), and its
  source text carries it (the LOW 53rd-week rule).
- **Dividends,** each "an increase of 4 percent" from the Q2 release that declares it: $0.25 (2024-05-03), $0.26 (2025-05-02)
  and $0.27 (2026-05-01). Catalyst (5) shows the programs, each "an additional program to repurchase up to": $110 billion
  (2024), then $100 billion (2025 and 2026).
- **No theme.** The FY2024 and FY2025 10-Ks name artificial intelligence as features Apple introduces (safety and privacy
  risks), as an area of regulation, and from FY2025 as a source of intellectual-property claims. They name the revenue from
  the search licensing arrangements with Google as exposed to litigation against Google. GENAI's scope, AI that
  substitutes the core product, names none of Apple's products. The watch list stays empty: DURABLE, risk 2.
- **The franchise text follows each 10-K.** The FY2024 10-K keeps the three quoted phrases word for word. From the FY2025
  10-K (2025-10-31) the profile quotes "a minority market share in the global smartphone, personal computer, tablet and
  wearables markets" and markets that "are highly competitive and are characterized by aggressive price competition, downward
  pressure on gross margins".
- **Adds nothing:**
  - the chief executive transition: Tim Cook to executive chair and John Ternus chief executive from 2026-09-01 (8-K of
    2026-04-20; the 8-K/A of 2026-09-01 gives their pay), as Steve Jobs's resignation and Tim Cook's appointment in 2011;
  - the other officer 8-Ks (chief financial officer 2024-08-26 and 2025-01-03, chief operating officer 2025-07-08 and
    2025-07-25, general counsel 2025-12-05, principal accounting officer 2026-01-02), the bylaw 8-K of 2024-08-23 and the vote
    8-Ks;
  - the derivative-settlement notice (8-K of 2024-05-03, item 7.01), the debt offering (8-K of 2025-05-12) and the 2024 shelf
    registration;
  - the proxies and the shareholder solicitations;
  - the 10-Qs' tariff wording without a figure, and their expectations without a field.
- **Text-only change to 2019-2023:** two source descriptions (the FY2019 and FY2020 10-Ks) now also cite the FY2015 and FY2016
  share counts the new vintages use. 218 models and analyses (2019-11-01 to 2023-12-29) change only in that text, and every
  report rebuilds byte-identical.
- **Anachronism list:** Apple names first seen in 2026 filings join it, each dated by its filing (approx): iPhone 17e, MacBook
  Neo and AirPods Max 2 (the Q2 FY26 10-Q, 2026-05-01) and Siri AI (the Q3 FY26 release, 2026-07-31). None of the 3,928 models
  of any ticker contains one.
- **ISO weeks:** the batch runs from 2024-W01 to 2026-W43. The last date is 2026-10-23, the last full week before the build
  (2026-10-30; prices to 2026-10-29), and no Q4 FY26 print or FY2026 10-K is in the facts. A later batch starts on 2026-10-26.
  Dates from late 2024 on have only part of the two-year horizon, and the latest have no outcome.

Controls: altering one value of each new print, Q4 full-year figure, vintage, dividend and program statement changes no date
before its publication (21 of 21) and changes the first weekly date on or after it (19 of 21). The other two are the Q4 FY24 and
Q4 FY25 full-year figures, which the 10-K replaces on the same day. The 835 dates of 2008-2023 rebuild with byte-identical
reports. A scan of all 982 AAPL models for 57 values and notes of the new sources, prints, vintages, dividends and programs finds
none before its publication. The firewall changes none of the 982, 930 and 878 models before 2026-10-24, 2025-10-31 and
2024-11-01.

Seen in the build (method behaviour, not tuned):
- **RICH and AVOID on every date.** All 147 dates read RICH, and the tier reads AVOID on all of them. The multiple stands at the
  81st-100th percentile of its own decade: 26.9-38.3x in 2024 (the lowest 26.9x on 2024-04-19, at $165.00), 27.9-38.9x in 2025
  (27.9x on 2025-04-04, at $188.38) and 33.2-46.6x in 2026 (46.6x on 2026-10-23, at $347.73).
- **The last full year's EPS is the anchor all along:** FY23's $6.13 to 2024-10-25, FY24's $6.75 to 2025-10-24, FY25's $7.46
  after. In 2026 the stock trades at 33.2-46.6x FY25's $7.46 while the FY26 quarters run ahead ($6.87 for Q1-Q3 FY26 against
  $5.62).
- **BASE follows each quarter's net sales growth plus the buyback:** +4.3%/yr (Q4 FY23's -0.7%), +7.1%, +0.7% (Q2 FY24's -4.3%),
  +9.9%, +10.7%, +8.6%, +9.7%, +14.2% (Q3 FY25's +9.6%), +12.2%, +20.0% (Q1 FY26's +15.7%), +20.9% and +20.7%. The decade's
  buyback falls from 4.98%/yr (FY14-FY23) to 4.64%, then 4.34%. BASE lifts BULL to its own rate on 52 dates: 2025-08-01 to
  2025-10-24, and from 2026-01-30.
- **BULL, XBULL and BEAR move with the window.** BULL is the decade EPS CAGR: +16.0%/yr (FY14-FY23), +12.7% (FY15-FY24),
  +15.2% (FY16-FY25). XBULL stays FY19-FY21's +37.4%/yr. BEAR applies FY16's -9.8% through the FY2024 vintage, then FY19's
  -0.3% (FY2025 vintage: $2.97 against $2.98).
- **The EPP floor rises as the cheap years leave the window.** It is the median of the calendar-year P/E lows: 12x through 2024
  (six lows of 10.9-12.6x in 2014-2019), 17x from 2025-01-03 (2014 out: 2020's 17.1x) and 20x from 2026-01-02 (2015 out:
  2023's 20.4x). The price stands 124-220% above it in 2024, 64-129% in 2025 and 66-133% in 2026.
- **Ratio B is `inf` on 61 dates** (29 in 2024, 18 in 2025, 14 in 2026; from 2024-06-14): the price stands above the BULL case.
  The lowest finite reading is 2.71x (2024-04-19), far above WATCHLIST's 1.75x.
- **The proxy composite reads 2.20 on 82 dates, 2.35 on 39 and 2.00 on 26.** Against the FY1998-FY2007 thresholds the
  gross-margin change reads BULL (+90bp or more) on every print but Q2 and Q3 FY25 (+47bp, +23bp). The operating-margin change
  also reads BULL in Q1 FY24 (+302bp), and net sales from Q2 FY26 (+16.6%, +16.4%). The unreported Mac slot changes none of it.

How far each call moves the classes (the affected dates rebuilt with one encoding changed; no outcome consulted):
- FY24 at GAAP ($6.08, the 24.09% tax rate, Q4 FY24's $0.97) instead of the company's figures excluding the State Aid charge
  would change none of the 104 dates from 2024-11-01. Ratio B and the gaps move (on 2025-06-06 Ratio B 23.18x instead of 4.95x,
  the EPP gap +97% instead of +78%), all toward AVOID;
- re-weighting the other five signals instead of scoring the unreported Mac slot BASE would change none of the 147 classes or
  tiers;
- Q1 FY24's net sales growth against 13 weeks of Q1 FY23 (+9.9%, a figure derived from others) would change none of the 13
  dates;
- Q3 FY26 without the tariff refunds (gross margin about 2 points and EPS $0.11 lower, figures derived from the stated impacts)
  would change none of the 13 dates.

Judgement calls that could carry hindsight:
- taking FY24 at the company's $6.75 excluding the State Aid charge, with its adjusted tax rate (no class moves at GAAP);
- keeping GAAP through Q3 FY26's tariff refunds (no figure without them was published; no class moves when derived);
- leaving the 13-week Q1 FY24 as published (no class moves);
- scoring the unreported Mac slot at BASE, as from Q1 FY19 (no class moves);
- reading the State Aid 8-K of 2024-09-10 as adding nothing (a charge expected before the year closed, with no guide in force);
- treating the chief executive transition as adding nothing (the method has no input for it);
- DURABLE rather than CYCLICAL (the class label only), and GENAI as outside Apple's scope (AI named only as Apple's own features
  and their risks).

## NKE (NIKE): the fifth ticker, in staging

The NKE series is built apart from ACN, UNP, LOW and AAPL and shares nothing with them but the machinery: its own fact sheet
(`retro/facts/NKE.json`), builder (`retro/build_nke.py`) and engine (`retro/templates/nke_engine.py.tmpl`, the AAPL engine with
athletic footwear and apparel signals). The method is still r2. No ACN, UNP, LOW or AAPL fact, parameter, outcome or finding enters
an NKE model, and neither does the repository's live `nke_signal_model.py` (a 2026 analysis). Outputs go to
`staging/retrospective/NKE/`, beside the others, with the same `index.json` and their own `SERIES.md`.

```bash
python3 retro/build_nke.py --weekly 2008-01-01 2008-12-31                   # 53 dates, 2008-01-04 .. 2008-12-31
for d in staging/retrospective/NKE/2008-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series NKE
python3 retro/tools/firewall.py 2008-07-01 NKE
```

The 10-Ks from FY1997 to FY2008 (FY1998 and FY2000 10-K405s) were read for the history and the decade's signal values, and every
8-K and 10-Q from June 2006 to December 2008 (46 filings) was read in full, with no delegated transcription, including the seven
call transcripts NIKE furnished by 8-K a few days after each release. 242 strings were checked with `verbatim.py` against their own filings, and
each source's date comes from EDGAR's acceptance time. Decided on 2026-10-30, before any NKE model was built or any NKE outcome
computed:

- **Fiscal calendar.** NIKE's fiscal year ends on May 31 (fiscal 2008 runs from 2007-06-01 to 2008-05-31). The builder maps each
  day to its fiscal year by that rule and checks it against the year-ends the vintages state. Days between May 31 and the Q4 print
  keep the last year's EPS (the ACN rollover rule): 2008-06-06 to 2008-06-20.
- **Prices on the as-of share basis** (the UNP rule). Yahoo's series is adjusted for the 2012 and 2015 2-for-1 splits, so 2008
  prices are Yahoo's times 4: $61.74 on 2008-01-04. The 2007 2-for-1 split (8-K accepted 2007-02-16 18:04 ET, dated 2007-02-20
  after the Presidents' Day holiday; split-adjusted trading from 2007-04-03, Yahoo's date) restates the per-share facts published
  before it: EPS of FY1998-FY2002 (from the 10-Ks of 2002-2006) and the first year's diluted shares. The 1995 and 1996 splits
  precede every per-share fact in the fact sheet.
- **Every release came after the close.** Each earnings 8-K was accepted at 16:16-16:37 ET, so a print is dated the next trading
  day and the week's date is the trading day after that: 2008-06-27, 2008-09-26 and 2008-12-19. The Q3 FY08 release (accepted
  2008-03-19 16:16 ET) is dated Thursday 2008-03-20 and Good Friday followed, so that day is the week's date and the print meets
  its close, public before the open (the AAPL 2011 rule). Each call transcript is dated by its own 8-K, two to six days after the
  call, which can only lag.
- **History: each year from the latest 10-K that reports it.** The FY2007 10-K (accepted 2007-07-27 16:16 ET, dated 2007-07-30)
  gives FY2003-FY2007; FY2002 comes from the FY2006 10-K, FY2001 from FY2005, FY2000 from FY2004, FY1999 from FY2003 and FY1998
  from the FY2002 10-K's eleven-year history. The Q4 FY08 release extends it with FY08 from 2008-06-26, and the FY2008 10-K
  (accepted 2008-07-28 16:08 ET, dated 2008-07-29) moves the window to FY1999-FY2008.
- **EPS** is diluted EPS before the cumulative effect of accounting changes, the line the 10-Ks report for FY2002 ($2.46, net
  $2.44) and FY2003 ($1.38 after the split, net $0.89). A company-published figure excluding a one-off replaces it: FY2006 enters at
  $2.70 excluding the Converse arbitration charge (FY2007 10-K and Q4 FY07 release; GAAP $2.64).
  - **FY2007 stays GAAP $2.93.** The company's $3.10 excludes the Converse settlement and stock-based compensation, expensed from
    fiscal 2007 under FAS 123R. That expense recurs, so a figure without it is not a figure excluding a one-off (the AAPL Q4 FY08
    non-GAAP rule), and no figure excluding the settlement alone was published.
  - **Per-share effects stay in** when no EPS excluding them was published (no figure is derived): the FY1998 restructuring charge
    ($0.27 per diluted share), FY1999's ($0.10), and FY2008's one-time tax benefit ($0.21) and Starter and Bauer sale gains ($29
    million and $32 million). FY08 enters at GAAP $3.74.
  - **No year is excluded.** FY1998's charge ($79.5 million after tax) is a fraction of the year's $399.6 million net income (the
    AAPL FY2003 test).
- **No guide in numbers.** No release, call transcript, 10-Q or 10-K of the period gives a revenue, EPS or margin guide in numbers.
  The CFO's outlook on each call is in words ("high single- to low double-digit revenue growth", "moderate growth in gross margins";
  for fiscal 2009 "high single digit revenue growth"), and words are not figures (the UNP 2016 rule). So:
  - current-FY EPS: the last full year's EPS stands: FY07's $2.93 to the Q4 FY08 print, FY08's $3.74 from it;
  - BASE growth and the growth factor: the latest quarter's revenue growth excluding currency changes, method r2's local-currency
    basis. The releases state the currency effect, so it is the release's growth less those points (the ACN bookings derivation):
    +10% (Q2 FY08: 14 less 4), +10% (Q3 FY08), +9% (Q4 FY08), +10% (Q1 FY09), +5% (Q2 FY09: 6 less 1);
  - no margin step: the margin signal takes the latest quarter's change.
  - Each call's outlook for the rest of the current fiscal year (its revenue and gross-margin words) is shown in the guide line and
    feeds no input. The latest call's words replace the earlier ones, and a statement for the next fiscal year shows once that year is
    current (the Q3 FY08 call's fiscal 2009 words from 2008-06-27). Tax-rate estimates and the SG&A, interest and other-income
    statements have no field. The multi-year targets (the long-term model of "high-single-digit revenue growth, mid-teens earnings per
    share growth"; "$23 billion in revenue by fiscal year 2011") are not current-year ranges and are not entered (the LOW rule).
- **Dividends:** the latest declared rate: $0.185 a quarter (FY2007 10-K), $0.23 from the Q2 FY08 release (2007-12-20; declared in
  November 2007 without an 8-K), $0.25 from the Q2 FY09 release (2008-12-18).
- **Signals.** Six, with ACN's weights, mirroring LOW's: futures orders growth (0.20, the release's headline: worldwide orders for
  delivery over the next five to six months, as reported), gross margin change (0.20), revenue growth (0.15, as reported), inventory
  growth less revenue growth (0.15, lower is better), the pre-tax margin change (0.15; NIKE "evaluates performance of individual
  operating segments based on pre-tax income") and the theme slot at 2/4. Values are the latest release's, derived from its income
  statement and balance sheet; futures as published.
- **Thresholds by rule T** (the LOW rule), over the ten years of the FY2007 10-K, the vintage public on 2008-01-04: FY1998-FY2007, each
  change from the latest 10-K published by 2008-01-04 that reports both years (the FY2002 10-K's eleven-year history covers
  FY1997-FY1999); year-end futures growth from each year's own 10-K, the only filing that reports it. The reported figures stand: no
  filing publishes gross margin or pre-tax income excluding the FY1998-FY1999 restructuring charges. The values are in the fact sheet
  (`rule_t`); the builder recomputes the thresholds from them and refuses to build if the engine's differ.

  | Signal | Decade (FY1998-FY2007) | BEAR / BASE / BULL / XBULL |
  |---|---|---|
  | futures orders growth | -13, 4, 3, 3, 6.3, 5, 11.3, 9.5, 5, 12 % | -31 / -13 / 5 / 12 % |
  | gross margin change | -358.9, 90.2, 251.6, -89.1, 26.9, 167.4, 188.2, 164.9, -46.3, -18.6 bp | -780 / -360 / 60 / 250 bp |
  | revenue growth | 4, -8.1, 2.5, 5.5, 4.3, 8.1, 14.5, 12.1, 8.8, 9.2 % | -23 / -8 / 7 / 15 % |
  | inventory less revenue | 0.3, -8.1, 21, -7, -7.8, 2.1, -5.6, -2.4, 5.8, -7 pp | 46 / 21 / -4 / -8 pp |
  | pre-tax margin change | -726.3, 166.5, 171.8, -50.9, 57.3, 21.5, 133.5, 170.2, 78.4, -84.5 bp | -1520 / -730 / 70 / 170 bp |

- **Durability.** DURABLE, risk 2, as for the other four. The "why" is the 10-K's own words: "NIKE is the largest seller of athletic
  footwear and athletic apparel in the world", "Virtually all of our products are manufactured by independent contractors", the
  industry "is keenly competitive", "including Adidas, Puma, and others", and demand follows "the relative popularity of various
  sports and fitness activities and changing design trends". No disruption theme in `taxonomy_eras.json` is live for an athletic
  footwear and apparel brand in 2008 (ECOMMERCE from 2015-01-01, scoped to physical retail; OFFSHORE to IT services), so the watch
  list is empty and the builder refuses events until a theme encoding is decided.
- **Segment bridge and EPS check** (display only): the 10-K's operating segments (the U.S., EMEA, Asia Pacific and Americas regions
  and Other) with each one's growth; the EPS check runs on the pre-tax margin, which already carries net interest income.
- **Adds nothing:** the officer, director and employment-agreement 8-Ks, the annual meeting results (2007-09-19 and 2008-09-25), the
  Umbro offer 8-K and its call ("You're seeking guidance we're not prepared to give"), the Umbro share purchase 8-K, and the 10-Qs
  (SG&A words and tax-rate estimates).
- **Anachronism list:** NIKE names from after 2008 (FuelBand, Flyknit, Consumer Direct Offense, Consumer Direct Acceleration) join
  `taxonomy_eras.json`. No existing model of any ticker contains them, so no output changes.

Controls: altering one value of each print, vintage, guide, dividend and the split changes no date before its publication and changes
the first weekly date after it (20 of 20; the Q4 FY07 print and the fiscal 2008 words of the Q4 FY07 and Q1 FY08 calls show on no 2008
date and change nothing). The Q3 FY08 call's fiscal 2009 words, public on 2008-03-25, first show on 2008-06-27, the first date with
fiscal 2009 current. Rebuilding the 2008 dates of ACN, UNP, LOW and AAPL changes nothing.

Seen in the build (method behaviour, not tuned):
- **BEAR is flat on every date.** EPS rose in every year of the history (FY1999-FY2008); FY1998's fall from FY1997 is not a change
  within the ten years. BEAR is flat EPS at the 10th-percentile P/E (15.0-15.3x): $45 on FY07's $2.93, $56-57 on FY08's $3.74.
- **BULL and XBULL** are the FY98-FY07 EPS CAGR (+17.7%/yr; +18.7% FY98-FY08 from the Q4 print, +18.9% FY99-FY08 from the FY2008
  10-K) and the FY03-FY05 run (+27.4%/yr), at the 75th and 90th percentile P/E: BULL prices of $90-91 to June and $107-112 after.
- **BASE is the quarter's revenue growth excluding currency plus the buyback** (diluted shares fell 1.6%/yr over FY98-FY07, 1.5% over
  FY99-FY08): +11.6%/yr to June, +10.6% from the Q4 FY08 print (+10.5% once the FY2008 10-K moves the history to FY99-FY08),
  +11.5% on Q1 FY09, +6.5% on Q2 FY09. The growth factor reads +0.19, +0.05, +0.02, +0.12 and -0.38 against the history's median
  revenue growth of 8.1-8.8%.
- **The class follows the EPS anchor.** On FY07's $2.93 the stock traded at 19.1-21.3x (the 51st-69th percentile) to 2008-03-14:
  CHEAP and BUY on all 11 dates, with Ratio B 0.31-0.61 and the proxy composite at 3.05 (futures +13% and the inventory gap
  -10.9pp at XBULL). From the Q3 FY08 print the stock stood at $65-69, 22.1-23.5x the same $2.93 (75th-82nd percentile): FAIR on 12
  of the 14 dates to 2008-06-20 (CHEAP on 2008-05-09 and 2008-05-23), tier ACCUMULATE (WATCHLIST on 2008-04-25 and 2008-06-13). From
  the Q4 FY08 print FY08's $3.74 is the anchor: 12.4-18.1x (0th-51st percentile), CHEAP and BUY on all 28 dates.
- **EPS anchors on the last full year:** FY07's $2.93 stands until 2008-06-25, when nine-month FY08 EPS was already $2.76 (the Q3 FY08
  release), so the March-June multiple of 22-23.5x is on a year already passed (the AAPL 2008 pattern).
- **From October the price sits below the BEAR price** on 11 of the 14 dates (Ratio B -0.15 to -0.03; also 2008-07-11 at -0.01), and
  below the EPP floor (14x FY08's $3.74, $52) on 8.
- **The Q2 FY09 print turns every signal to BASE** (futures -1%, revenue +5.8%, gross margin +39bp, the inventory gap +3.0pp, pre-tax
  margin -54bp): the proxy composite falls from 2.70 to 2.00 and BASE growth to +6.5%/yr; the class stays CHEAP, below the floor.
- **Robustness:** all eight variants agree on every date from the Q4 FY08 print; on the FAIR dates three to six of eight.

How far each call moves the classes (the 53 dates rebuilt with one encoding changed; no outcome consulted):
- FY07 at the company's $3.10 instead of GAAP $2.93 would change 11 classes (FAIR to CHEAP on 11 of the 12 FAIR dates, 2008-03-20 to
  2008-06-20) and 8 tiers;
- BASE and the growth factor on reported revenue growth instead of growth excluding currency would change no class and no tier;
- FY06 at GAAP $2.64 instead of $2.70 would change nothing;
- excluding FY1998 (the history and the P/E window from FY1999) would change no class and one tier (2008-04-04, ACCUMULATE to
  WATCHLIST).

Judgement calls that could carry hindsight:
- FY07 at GAAP $2.93 rather than the company's $3.10 (the call that moves the most classes: 11 of 53);
- the signals, chosen by a builder who knows what 2008 and 2009 brought: futures orders and the inventory gap (rule T then sets their
  thresholds mechanically);
- revenue growth excluding currency changes for BASE (it moves nothing on these dates), and keeping FY1998;
- DURABLE rather than CYCLICAL (the class label only);
- dating each call's words from its transcript's 8-K (can only lag).

### NKE 2009-2011: adjusted EPS, currency-neutral growth as stated, six geographies

```bash
python3 retro/build_nke.py --weekly 2009-01-05 2011-12-31                   # 156 dates, 2009-01-09 .. 2011-12-30
for c in 2009-07-01 2010-07-01 2011-07-01 2012-01-01; do python3 retro/tools/firewall.py $c NKE; done
```

All 48 filings from 2009-01-08 to 2012-01-06 (34 8-Ks, an 8-K/A, 10 10-Qs and the FY2009-FY2011 10-Ks) were read in full, with no
delegated transcription: twelve releases, eleven call transcripts (none was filed for Q4 FY11, when an investor meeting took the
call's place), the segment recast, and the officer, meeting and credit 8-Ks. 316 strings were checked with `verbatim.py` against
their own filings (the call words read from the fact sheet itself), and every print's raw figures were cross-checked against its
own release. Each source's date comes from EDGAR's acceptance time. Thresholds, signals and the engine are unchanged. Decided
before any 2009-2011 date was built or scored:

- **Three vintages.** The FY2009 10-K (accepted 2009-07-27 17:27 ET, dated 2009-07-28) gives FY2005-FY2009; FY2004 comes from the
  FY2008 10-K, FY2003 and FY2006's $2.70 from the FY2007 10-K, FY2002 from FY2006, FY2001 from FY2005 and FY2000 from FY2004
  (the last three restated by the 2007 split). The FY2010 10-K (2010-07-20 17:18 ET, dated 2010-07-21) and the FY2011 10-K
  (Friday 2011-07-22 16:16 ET, dated Monday 2011-07-25) report their selected data in whole millions, which the revenue history
  takes; the prior year's margins and tax rate come from each 10-K's income statement. The history runs FY2000-FY2009, then
  FY2001-FY2010 and FY2002-FY2011.
- **EPS excluding non-comparable items** (the ACN rule, as for FY06 in 2008). FY09 enters at the company's $3.81 from the Q4 FY09
  print (2009-06-25; GAAP $3.03, after the Umbro impairment, $0.49, and restructuring charges, $0.29). That release first
  published FY08 at $3.45 (GAAP $3.74, with the one-time tax benefit of $0.21 and the Starter and Bauer sale gains of $0.04 each);
  it enters with the FY2009 10-K, which states it too (the UNP Brazos rule), and later vintages keep both (the LOW rule). FY10's
  $3.86 and FY11's $4.39 have no such items. A print shows the release's EPS excluding non-comparable items where it publishes one
  (Q3 FY09 $0.99 against $0.88, Q4 FY09 $0.99 against $0.94, Q3 FY10 $1.01 against $0.99, Q4 FY10 $1.06 against $0.99), GAAP in
  the note.
- **Margins stay GAAP** (adjusted EPS, GAAP margins: the LOW 2016-2017 call). No filing publishes gross margin or pre-tax income
  excluding the items, and no figure is derived. The pre-tax margin signal reads -941bp in Q3 FY09 (the $401.3 million
  impairment) and -242bp in Q4 FY09 (the $195.0 million restructuring charge), and +868bp and +313bp a year later against those
  quarters.
- **Growth excluding currency as each release states it.** From Q3 FY09 the releases state revenue and futures growth excluding
  currency changes (from Q1 FY10 also for the total in the divisional tables) instead of the currency points, so `lc_pct` takes
  the stated figure: +2, 0 ("flat with the prior year excluding currency changes"), -7, -4, +2, +4, +10, +11, +8, +11, +11 and +16%.
  Where currency had "a minimal impact" (Q2 FY10 revenue, Q2 FY11 futures) or "did not have a significant impact" (Q2 FY12
  futures), the table's figure stands; it equals the reported one. The futures signal stays as reported, with the
  currency-neutral figure in the note.
- **Year-end futures in the franchise line** (display only): each 10-K's reported figure, FY09 "declined 12%", FY10 7% ("increased
  7% when translated at forecasted exchange rates", the release's reported figure; the 10-K states "10% higher" at prior-year
  rates first) and FY11 "15% higher". Rule T's futures measure is the reported figure.
- **Still no guide in numbers.** Revenue outlooks are in words ("flat to slightly down on a currency neutral basis",
  "high-single-digit", "low to mid teens", "mid-teens"), and from fiscal 2010 the gross-margin outlooks are in basis points ("about
  1 point below FY '09", "at least 160 basis points"). They are display only: words are not figures, gross-margin expectations
  have no field (the AAPL rule), and NIKE gave no pre-tax margin guide. Tax-rate estimates have no field. With no Q4 FY11
  transcript filed, the Q3 FY11 call's first fiscal 2012 words show from the Q4 FY11 print to the Q1 FY12 call. The May 2010 and
  June 2011 investor meetings were not furnished by 8-K, so their long-term targets are not in the fact sheet (nor would they be
  entered: the LOW rule).
- **Six geographies from the FY2010 vintage.** NIKE reorganized from fiscal 2010 into North America, Western Europe, Central and
  Eastern Europe, Greater China, Japan and Emerging Markets, plus Global Brand Divisions and Other Businesses; the bridge takes
  those eight lines and leaves out Corporate (-$24 million in FY10, +$11 million in FY11). The FY2009 vintage keeps the four
  regions and Other, with FY08 as restated in that 10-K. From fiscal 2010 NIKE evaluates its segments on EBIT; the margin signal
  keeps the pre-tax margin its thresholds were set on.
- **Dividends:** $0.27 a quarter from the Q2 FY10 release (2009-12-18), $0.31 from Q2 FY11 (2010-12-22) and $0.36 from Q2 FY12
  (2011-12-21); the vintages carry $0.25, $0.27 and $0.31.
- **Calendar.** Every release came after the close (8-Ks accepted at 16:17-16:22 ET). Four were dated on a Friday, the week's last
  trading day (2009-12-18, 2010-09-24, 2011-03-18 and 2011-09-23), so the print meets that day's close, public before the open
  (the 2008 Good Friday rule). The Q4 FY09 call's 8-K (2009-07-01 19:07 ET) is dated Thursday 2009-07-02, the week's last trading
  day before Independence Day. From Q1 FY11 the releases are in whole millions, and Q2 FY12 renames gross margin "Gross profit".
- **Durability is unchanged:** DURABLE, risk 2, with each 10-K's own words. No theme in the registry is live for NIKE in
  2009-2011 (ECOMMERCE from 2015, scoped to physical retail).
- **Adds nothing:** the officer and director 8-Ks (2009-03-05, 2009-06-22, 2009-11-24, 2010-07-21, 2011-04-25, 2011-06-17), the
  annual meetings (2009-09-29, 2010-09-24, 2011-09-26 and the 8-K/A of 2011-11-22), the segment recast of 2009-09-28 (the bridge
  keeps the FY2009 10-K's regions until the FY2010 10-K), the credit agreement of 2011-11-02, and the 10-Qs (tax-rate estimates, gross-margin words, the Japan earthquake). The Q3 FY09 release's
  expected $175-225 million restructuring charge goes in that print's note.

Controls: altering one value of each print, vintage, guide, dividend and the split changes no date before it can be shown and
changes the first weekly date on or after it (52 of 52; a guide for the next fiscal year first shows on the first date with that
year current: the Q3 FY09 call's fiscal 2010 words on 2009-06-26, the Q3 FY10 call's fiscal 2011 words on 2010-06-25, the Q3
FY11 call's fiscal 2012 words on 2011-06-29). No string of any print, vintage, guide or dividend appears in a model dated before
it (19,747 checks over the 209 NKE models). The firewall at 2009-07-01, 2010-07-01, 2011-07-01 and 2012-01-01 changes no model
before its cutoff. The 53 dates of 2008 rebuild byte-identical, and no file shared with another ticker changed.

Seen in the build (method behaviour, not tuned):
- **CHEAP on 73 of 156 dates, FAIR on 22, RICH on 61;** BUY on 76, ACCUMULATE on 22, WATCHLIST on 29, AVOID on 29. By year: 44,
  6 and 2 in 2009 (BUY on all 52); 24, 15 and 13 in 2010; 5, 1 and 46 in 2011.
- **2009 opened below the BEAR price.** On FY08's $3.74 the stock traded at 10.7-15.6x (the 0th-22nd percentile) to 2009-06-19:
  CHEAP and BUY on all 24 dates, below the BEAR price ($54-56) on 17 and below the EPP floor ($52) on 14, Ratio B -0.23 to 0.10.
- **BEAR is flat on every date:** with FY08 at $3.45 and FY09 at $3.81, EPS rose in every year of each window. BULL is the
  window's EPS CAGR (18.9%/yr on FY99-FY08, 17.1% from the Q4 FY09 print, 15.6% on FY00-FY09, 14.1% from the Q4 FY10 print,
  15.2% on FY01-FY10, 15.1% from the Q4 FY11 print and 15.2% on FY02-FY11) and XBULL the FY03-FY05 run (+27.4%/yr) throughout.
  The EPP floor P/E stays at 14x: $52-54 on FY08-FY10's EPS, $61 on FY11's.
- **BASE followed the quarter's currency-neutral revenue growth plus the buyback** (1.1-1.6%/yr): +6.5%/yr on Q2 FY09, +3.5% on
  Q3 FY09, +1.6% and +1.5% on Q4 FY09 (before and after the FY2009 10-K), -5.5% on Q1 FY10 (revenue -7%), -2.5% on Q2 FY10, +3.5%
  on Q3 FY10, +5.2% and +5.1% on Q4 FY10, +11.1%, +12.1% and +9.1% on Q1-Q3 FY11, +12.2-12.3% on Q4 FY11 and Q1 FY12, and +17.3%
  on Q2 FY12 (+16%), where it also lifts BULL. The growth factor read -0.38 to -0.5 to 2010-09-17 and -0.08 to +0.5 after.
- **The proxy composite trailed the quarter:** 2.00 on Q2 FY09, 1.85 on Q3 FY09 (futures -10%, the impairment quarter), 2.00 on Q4
  FY09 and Q1 FY10, 2.15 on Q2 FY10, 3.20 and 3.35 on Q3 and Q4 FY10 (gross margin +299bp and +403bp, the inventory gap -19pp
  and -21pp, the pre-tax margin against the charge quarters), then 2.85, 2.70 and 2.35 on Q1-Q3 FY11, 2.55 on Q4 FY11 and Q1
  FY12 (gross margin -310bp and -275bp, inventories +33% and +41%), and 2.70 on Q2 FY12.
- **The class followed the price against a lagging anchor.** On FY09's $3.81, from the FY2009 10-K to 2010-06-18, the stock traded
  at 14.2-20.4x (the 10th-88th percentile): CHEAP on 27 of 47 dates, FAIR on 15 and RICH on 5 (the RICH dates at the 47th-65th
  percentile, in October-November 2009 and February-March 2010, on BASE growth of -5.5% and -2.5%). On FY10's $3.86, from the
  Q4 FY10 print to 2011-06-24, it traded at 17.6-23.3x (54th-97th): CHEAP on 12 of 53 dates, FAIR on 6 and RICH on 35, AVOID on 20.
  On FY11's $4.39 it traded at 17.9-22.3x (60th-96th): RICH on 21 of 27 dates, CHEAP on 5 (2011-08-05 to 2011-09-09, $78.58-84.24)
  and FAIR on 1.
- **EPS anchors on the last full year:** FY09's $3.81 stood until 2010-06-24, when nine-month FY10 EPS was $2.81 (the Q3 FY10
  release), and FY10's $3.86 until 2011-06-28, when nine-month FY11 EPS was already $3.16.
- **Robustness:** all eight variants agree on 39 of the 73 CHEAP dates and six or seven on the rest; on the RICH dates three to
  eight agree, on the FAIR dates one to eight.

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- FY09 at GAAP $3.03 instead of the company's $3.81 would change 58 classes (CHEAP to RICH on 27, FAIR to RICH on 20, CHEAP to
  FAIR on 10, RICH to FAIR on 1; 2009-07-17 to 2011-09-09) and 96 tiers or classes;
- BASE and the growth factor on reported revenue growth instead of growth excluding currency would change 20 classes (9 FAIR to
  RICH, 5 FAIR to CHEAP, 5 RICH to FAIR, 1 CHEAP to FAIR) and 28 dates' class or tier;
- FY08 at GAAP $3.74 in every vintage (its $3.45 never entering) would change 11 classes (7 CHEAP to FAIR, 4 FAIR to RICH);
- FY08's $3.45 from the Q4 FY09 print rather than the FY2009 10-K (five dates) would change none;
- the pre-tax margin signal with the FY09 impairment and restructuring added back (a derived figure, as a test only) would change
  none.

Judgement calls that could carry hindsight:
- FY09 at the company's $3.81 rather than GAAP $3.03 (the call that moves the most classes: 58 of 156), and FY08 at $3.45 with it
  (11): both follow the 2008 rule for a company figure excluding one-offs, applied once the figures were published;
- revenue growth excluding currency changes for BASE (20 classes), as in 2008;
- GAAP margins beside adjusted EPS (no class moves);
- the signals and the reported basis for futures, chosen by a builder who knows how 2009-2011 went;
- DURABLE rather than CYCLICAL (the class label only); dating each call's words from its transcript's 8-K (can only lag).

### NKE 2012-2014: continuing operations, the 2012 split, the first EPS guide in numbers

```bash
python3 retro/build_nke.py --weekly 2012-01-02 2014-12-31                   # 157 dates, 2012-01-06 .. 2014-12-31
for c in 2012-12-26 2013-07-01 2014-07-01 2015-01-01; do python3 retro/tools/firewall.py $c NKE; done
```

All 44 filings published from 2012-01-07 to 2014-12-31 (33 8-Ks, 8 10-Qs and the FY2012-FY2014 10-Ks) were read in full, with
no delegated transcription: twelve releases, twelve call transcripts, the split and dividend 8-K, the April 2013 notes offering,
and the officer, director, bylaw and meeting 8-Ks. 324 strings were checked with `verbatim.py` against their own filings (the
call words read from the fact sheet itself), and every print's raw figures were cross-checked against its own release. Each
source's date comes from EDGAR's acceptance time. Thresholds, signals and the engine are unchanged; the builder gains two
fact fields (below). Decided before any 2012-2014 date was built or scored:

- **Continuing operations.** NIKE announced on 2012-05-31 its intention to divest Cole Haan and Umbro; from the Q2 FY13
  release (2012-12-21) they are discontinued operations (Umbro sold on 2012-11-30, Cole Haan on 2013-02-01). EPS is diluted
  EPS from continuing operations where the filing reports the line, else diluted EPS (the LOW and UNP rule). The Q1 FY13
  release is still consolidated: GAAP $1.23 stands, and its pro forma $1.27 "excluding the results of the Businesses to be
  Divested" removes ongoing operations rather than a one-off (the AAPL 2008 non-GAAP rule), so it goes in the note.
- **Three vintages.**
  - The FY2012 10-K (accepted 2012-07-24 16:16 ET, dated 2012-07-25) gives FY2008-FY2012 on the old basis; FY08's $3.45
    and FY09's $3.81 (company figures from the FY2009 and FY2010 10-Ks) stay (the LOW rule). Window FY2003-FY2012.
  - The FY2013 10-K (2013-07-23 16:32 ET, dated 2013-07-24) restates FY2009-FY2013 for continuing operations, after the
    split: $1.79, $1.95, $2.24, $2.42, $2.69. FY09's $3.81 was on the basis that included Umbro and Cole Haan, so the
    restated $1.79 stands (the UNP trucking rule); it already leaves out the Umbro impairment, now in discontinued
    operations, and keeps the restructuring charge. No later 10-K restates FY2004-FY2008, so they stay as published, a seam
    (the LOW Contractor Yards rule): FY08's $3.45 ($1.725 after the split) beside FY09's continuing $1.79, revenues of
    $18.627 billion beside $18.528 billion. Window FY2004-FY2013.
  - The FY2014 10-K (Friday 2014-07-25 16:22 ET, dated Monday 2014-07-28) gives FY2010-FY2014, revised to expense internally
    developed patent and trademark costs ($1.94, $2.23, $2.40, $2.68, $2.97); FY09 comes from the FY2013 10-K. Window
    FY2005-FY2014.
- **Q4 prints and restated years.** The Q4 prints extend the history with FY12's $4.73 (2012-06-29), FY13's continuing $2.69
  (2013-06-28) and FY14's $2.97 (2014-06-27). A prior year first restated in a later Q4 release (FY12's continuing $2.42,
  FY13's revised $2.68) enters with the next 10-K (the UNP Brazos rule).
- **The 2012 split.** 2-for-1, announced in the 8-K accepted 2012-11-15 16:19 ET (dated 2012-11-16); NIKE "expects its common
  stock to begin trading at the split-adjusted price on December 26, 2012", the price data's date. From that date per-share
  facts published before it are divided by 2 and share counts multiplied by 2 (the UNP rule): $105.10 on 2012-12-21, $50.99
  on 2012-12-28, and FY12's $4.73 becomes $2.365. Later 10-Ks enter as restated; print text is not restated.
- **A dividend declared on the post-split basis.** The split 8-K declares "$0.21 per share, on a post-split basis", a 17
  percent increase over the "split-adjusted quarterly rate of $0.18". It enters on the 8-K's date with its basis recorded
  (`basis` = 2012-12-26): $0.42 a share until the split, $0.21 from it; the Q2 FY13 release, published before the split,
  confirms 0.42. The builder converts such a dividend itself, since `on_basis` assumes a fact is on the share basis of its
  publication date. Later rates first appear in the Q2 releases: $0.24 (2013-12-20) and $0.28 (2014-12-19).
- **The first EPS guide in numbers.** On the Q1 FY15 call (furnished on 2014-09-30 during market hours) the CFO expects
  "earnings per share to grow at a high-teens rate for Q2 and about 20% for the full year". Method r2 takes the current-FY EPS
  from the EPS guide; a guide stated as growth keeps its growth (the LOW growth-form rule) and applies it to the year it is
  stated on: FY15E = FY14's $2.97 x 1.20 = $3.56 from 2014-10-03 (`eps_growth`, a new guide field). The Q2 FY15 call's
  words ("full year results largely in line with the expectations we shared 90 days ago") keep it (the LOW rule: a guide in
  words keeps the last numeric one). Everything else on the calls stays display only: revenue in words ("low double digits"),
  gross margin in basis points (the AAPL rule; NIKE gave no pre-tax margin guide), quarter EPS words, tax-rate estimates. The
  multi-year targets ("$28 billion to $30 billion in revenue by FY '15"; the October 2013 investor meeting, not furnished by
  8-K) are not entered (the LOW rule).
- **Futures and growth excluding currency** as each release states them. Four releases give no dollar amount for futures (Q4
  FY12, Q1 FY14, Q1 FY15, Q2 FY15), so the note omits it; Q3 FY12 states the currency effect in points ("reduced reported
  futures orders by 3 percentage points"); where currency "did not have a significant impact" (Q4 FY13 futures, Q1 FY14
  revenue) the table's figure stands.
- **Restated prior-year columns** (patent and trademark costs, inventories held at third parties) in the FY14 and FY15
  releases: each print's change comes from its own release's two columns, as published.
- **Segments** (display): six geographies, Global Brand Divisions and Other Businesses in the FY2012 and FY2013 10-Ks; from
  the FY2014 10-K Converse is its own segment and NIKE Golf and Hurley sit in the geographies. Corporate stays out of the
  split.
- **Durability:** DURABLE, risk 2, each vintage quoting its own 10-K. The FY2013 and FY2014 10-Ks rewrote the competition
  sentences ("is highly competitive in the United States and on a worldwide basis", then "is highly competitive on a worldwide
  basis"; "including adidas, V.F. Corp., Puma, Li Ning and Under Armour, among others"). No theme in the registry is live for
  NIKE in 2012-2014 (ECOMMERCE from 2015, scoped to physical retail).
- **Calendar.** Every release came after Thursday's close (16:18-16:27 ET), so each print is dated a Friday, the week's last
  trading day, and meets that close, public before the open (the 2008 Good Friday rule). 2014-12-31 covers ISO week
  2015-W01, so a 2015 batch starts on 2015-01-05.
- **Builder changes, data-driven only:** the two fields above, and catalyst (3) naming the EPS guide while one is in force.
  No earlier fact carries either field, and the 209 models of 2008-2011 rebuild byte-identical.
- **Adds nothing:** the officer and director 8-Ks (2012-05-23, 2013-06-21, 2014-04-21, 2014-06-23), the annual meetings
  (2012-09-27, 2013-09-24, 2014-09-23), the bylaw amendments, the $1 billion notes offering (2013-04-29; long-term debt
  enters through the FY2013 10-K), and the 10-Qs (tax-rate estimates, China words, gross-margin words).

Controls: altering one value of each print, vintage, guide, dividend and split changes no date before it can be shown and
changes the first weekly date on or after it (86 of 86). A guide for the next fiscal year first shows on the first date with
that year current (2012-06-29, 2013-06-28, 2014-06-27); altering the 2012 split's ratio changes the dates from its
announcement (2012-11-16), through the dividend declared on its basis. No string of any print, vintage, guide or dividend
appears in a model dated before it (62,093 checks over the 366 NKE models; the scan skips a string an earlier item already
carries, alone or inside a longer string). The firewall at 2012-12-26, 2013-07-01, 2014-07-01 and 2015-01-01 changes no model
before its cutoff. The 209 dates of 2008-2011 rebuild byte-identical, and no file shared with another ticker changed.

Seen in the build (method behaviour, not tuned):
- **RICH on 150 of 157 dates** (45 of 52 in 2012, all 52 in 2013, all 53 in 2014); tier AVOID on 132. On the RICH dates the
  stock traded at 19.7-30.1x its anchor EPS, the 87th-100th percentile of its own ten-year P/E range, and from 2013-04-12
  above the BULL price on 69 dates (Ratio B infinite). The exceptions: CHEAP on 5 dates and FAIR on 2, from the Q4 FY12 print
  to the split announcement (2012-06-29 to 2012-11-16), when FY12's $4.73 became the anchor and the price was $87.78-94.54
  (18.6-20.0x, the 70th-87th percentile).
- **The anchor lags a growing company:** FY11's $4.39 stood until 2012-06-28, when nine-month FY12 EPS was $3.56; FY12's
  $2.365 (after the split) until 2013-06-27, nine-month FY13 EPS from continuing operations $1.93; FY13's $2.69 until
  2014-06-26, nine-month FY14 EPS $2.20.
- **The EPS guide moved the anchor, not the class:** on 2014-10-03 FY15E's $3.56 replaced FY14's $2.97, and the multiple fell
  from 30.1x (2014-09-26) to 25.4x, the 97th percentile; the class stayed RICH and the tier AVOID.
- **BEAR is flat on every date.** BASE is the quarter's currency-neutral growth plus the buyback (1.3-2.0%/yr): +17.3%/yr on
  Q2-Q3 FY12, +15.5% on Q4 FY12, +16.5% on Q1 FY13, +11.5% on Q2-Q3 FY13, +10.6-10.8% on Q4 FY13, +9.8% on Q1 FY14, +10.8% on
  Q2 FY14, +15.8% on Q3 FY14, +14.8-15.0% on Q4 FY14, +17.0% on Q1 FY15 and +20.0% on Q2 FY15. BASE above the window's EPS
  CAGR lifts BULL to it on 92 dates (to 2012-12-14 and from 2014-03-21); between them BULL is that CAGR, 13.3-14.7%/yr. From
  the FY2014 10-K XBULL is lifted too: the best two-year run of FY05-FY14 is 14.4%/yr.
- **The EPP floor P/E moved from 14x to 15x on 2012-10-12** as the window's calendar-year lows rose.
- **The proxy composite stayed at 2.35-2.85,** with futures +6% to +15% and revenue growth at BULL or above on every print
  (+7.4% to +18.4%).
- **Robustness:** all eight variants agree on 125 of the 150 RICH dates, four to seven on the rest; on the seven CHEAP and
  FAIR dates four to seven of eight.

How far each call moves the classes (the 157 dates rebuilt with one encoding changed; no outcome consulted):
- BASE and the growth factor on reported revenue growth instead of growth excluding currency would change 6 classes (CHEAP to
  RICH on 4, FAIR to RICH on 2, all from 2012-07-06 to 2012-11-16) and 13 dates' class or tier;
- FY08 at GAAP $3.74 in the 2012-2014 vintages would change 2 classes (FAIR to RICH on 2012-10-12 and 2012-11-02);
- the Q1 FY15 call's "about 20%" kept as words (FY14's $2.97 standing), FY09 at the earlier-basis $3.81 instead of the
  restated $1.79, and the split dividend entering with the Q2 FY13 release instead of the 8-K would change none.

Judgement calls that could carry hindsight:
- BASE on growth excluding currency changes (the call that moves the most classes: 6 of 157), as in 2008-2011;
- FY08 at the company's $3.45 (2 classes), and the seam between FY08 on the old basis and FY09-FY14 from continuing
  operations;
- the Q1 FY15 call's "about 20%" read as an EPS guide in numbers (no class moves);
- the post-split dividend put on the pre-split basis for six weeks (no class moves);
- the signals, chosen by a builder who knows how 2012-2014 went; DURABLE rather than CYCLICAL (the class label only).

### NKE 2015-2017: the 2015 split, futures off the release and then discontinued, e-commerce on the watch list

```bash
python3 retro/build_nke.py --weekly 2015-01-05 2017-12-31                   # 156 dates, 2015-01-09 .. 2017-12-29
for c in 2015-07-01 2015-12-24 2016-07-01 2016-12-23 2017-03-24 2017-07-21 2017-09-26 2018-01-01; do python3 retro/tools/firewall.py $c NKE; done
```

All 54 filings published from 2015-01-01 to 2017-12-31 (40 8-Ks, 2 8-K/As, 9 10-Qs and the FY2015-FY2017 10-Ks) were read,
with no delegated transcription: the twelve releases and the split and segment-recast 8-Ks with their exhibits in full, and the
items of the officer, director, credit, notes, bylaw and meeting 8-Ks (not their legal exhibits: the credit agreement,
indentures, bylaws and plans); the twelve call transcripts' prepared remarks in full, with each Q&A searched for figures (none
gives an EPS, revenue or margin number); the 10-Ks' business, risk-factor, selected-data, futures, segment and cash-flow sections; and the
10-Qs searched for outlook statements (tax-rate estimates only). 374 strings were checked with `verbatim.py` against their own
filings, among them every print's income-statement, balance-sheet and futures rows, every call's words and every vintage's
rows. Each source's date comes from EDGAR's acceptance time. Thresholds and signals are unchanged. Decided before any 2015-2017
date was built or scored:

- **Three vintages.**
  - The FY2015 10-K (accepted 2015-07-23 17:26 ET, dated 2015-07-24) gives FY2011-FY2015 from continuing operations. Window
    FY2006-FY2015; FY2006's diluted shares (527.6M) from the FY2010 10-K, the latest that reports them.
  - The FY2016 10-K (2016-07-21 16:11 ET, dated 2016-07-22) gives FY2012-FY2016 after the 2012 and 2015 splits. Window
    FY2007-FY2016; FY2007's shares (509.9M) from the FY2011 10-K.
  - The FY2017 10-K (2017-07-20 16:18 ET, dated 2017-07-21) gives FY2013-FY2017. Window FY2008-FY2017; FY2008's shares
    (504.1M) from the FY2012 10-K.
  - Every earlier year comes from the latest 10-K that reports it, and FY08's $3.45 on the old basis stays until it leaves the
    window (the seam of "NKE 2012-2014"). A first year's share count is recorded by `shares_published`; no older source text
    changes.
- **EPS as released.** FY15 $3.70, FY16 $2.16 and FY17 $2.51 have no company figure excluding an item. FY17 includes the Q1 FY17
  one-time tax benefit ("a one-time benefit related to the resolution with the U.S. Internal Revenue Service of a foreign tax
  credit matter", a 2.5 percent Q1 rate): no figure without it was published, so GAAP stands (the ACN Russia rule; FY08's tax
  benefit stayed in until the company published $3.45). The same holds for the ASU 2016-09 tax benefit in Q1 FY18.
- **The 2015 split.** 2-for-1, announced in the 8-K accepted 2015-11-19 16:19 ET (dated 2015-11-20); NIKE "expects its common
  stock to begin trading at the split-adjusted price on December 24, 2015", the price data's date. From that date per-share
  facts published before it are divided by 2 (the UNP rule): $128.71 on 2015-12-23, $63.18 on 2015-12-24, and FY15's $3.70
  becomes $1.85. The Q2 FY16 release, dated 2015-12-23, is "presented on a pre-split basis"; its weekly date is 2015-12-24, the
  split's first day, so its EPS shows halved. Unlike 2012 the split 8-K declares the dividend on the pre-split basis ("$0.32 per
  share, on a pre-split basis", up 14 percent), so it needs no `basis`: $0.16 from the split. The same 8-K approves a new
  four-year $12 billion repurchase program.
- **Still one EPS guide in numbers.** The Q1 FY15 call's "about 20%" keeps FY15E at $3.56 to the Q4 FY15 print: the Q3 FY15
  call gives fiscal 2015 revenue and gross-margin words and no EPS statement (the LOW words rule). Every later EPS statement is
  in words: fiscal 2016 "EPS growth in the high-single to low-double digit range" (Q3 FY15 call), fiscal 2017 "EPS to grow at a
  low teens rate" (Q3 FY16 call), fiscal 2018 "earnings growth consistent with our long-term financial model" (Q3 FY17 call).
  So the last full year stands: FY15's $3.70 ($1.85 after the split) for FY16, FY16's $2.16 for FY17 and FY17's $2.51 for FY18.
  Revenue outlooks are in words and gross-margin outlooks in basis points, display only (the AAPL rule); a Q3 call that gives
  only fourth-quarter words for the current year is shown with them (as the Q3 FY09 and Q3 FY11 calls were). The CEO's
  restricted stock units in the 8-K of 2015-06-30 vest on 9% revenue and 13% EPS compound growth over FY16-FY20 at the maximum:
  a compensation target, not a guide (the LOW multi-year rule). The October 2015 and October 2017 investor days were not
  furnished by 8-K.
- **Futures orders leave the release, then end.**
  - From Q2 FY17 the releases no longer state futures orders ("Worldwide futures orders for the NIKE Brand will be referenced on
    our earnings conference calls as deemed appropriate"; the Q4 FY17 release does not mention them). A print's futures enter
    from the first filing that states them, on that filing's own date, as any fact does (the UNP 2019 rule; that can only lag):
    Q2 FY17 "flat versus prior year on a reported basis", +2% currency-neutral (the call's 8-K, 2016-12-23); Q3 FY17 down 4%
    reported, down 1% currency-neutral (2017-03-24); Q4 FY17 $14.7 billion, "2% lower", 0% excluding currency (the FY2017 10-K,
    2017-07-21). The investor-relations website posts are not filings, and the 10-Qs repeat the calls' figures later. New print
    field `futures_later`.
  - Until then the slot has no value, and from Q1 FY18 NIKE no longer reports futures (8-K accepted 2017-09-25 16:41 ET, dated
    2017-09-26: NIKE "will discontinue reporting Futures Orders in its financial disclosures"). The AAPL Mac-unit rule applies:
    the signal keeps its name, thresholds and weight, scores BASE with no value (shown "n/r"), and no other measure replaces it.
    The Q4 FY17 release gives no year-end futures, so the franchise line says so until the FY2017 10-K.
  - The Q3 FY16 release first states that reported futures include internal orders from NIKE's own in-line stores and
    e-commerce; its 10-Q says "Consistent with prior periods", so the measure did not change.
- **ECOMMERCE on the watch list from the FY2017 10-K.** ECOMMERCE is live from 2015-01-01 and scoped to e-commerce displacing
  physical retail. The FY2015 and FY2016 10-Ks name e-commerce only as NIKE's own channel (its systems, and "diversion of sales
  from our and our retailers' brick and mortar stores" by its own e-commerce): no theme, as for Apple's own services (the AAPL
  rule). The FY2017 10-K is the first whose risk factors name the shift as a risk to NIKE's own business: "the competitive nature
  of retail including shifts in the ways in which consumers are shopping, and the rising trend of digital commerce, constitutes
  a risk factor implicating our DTC and wholesale operations", with "a shift in consumer behavior away from brick-and-mortar
  retail" for its stores. So the LOW and ACN CLOUD rule: from 2017-07-21 ECOMMERCE is on the watch list, company-acknowledged,
  no market read; DURABLE, risk 2. The factor pair (NIKE's own digital commerce, $2.2 billion in fiscal 2017, against the shift)
  nets to zero and the theme signal stays at 2/4, so only text changes. Re-filing needs dated evidence that the market priced it
  for NIKE; no press coverage is added. The Q4 FY17 call's Amazon pilot is NIKE selling through another channel and adds nothing.
- **Calendar.** Every release came after the close (16:16-16:26 ET). Q2 FY16 to Q3 FY17 and Q1 FY18 came on a Tuesday, so the
  print is dated Wednesday and the week's date is Thursday. Q3 FY15, Q4 FY15, Q1 FY16, Q4 FY17 and Q2 FY18 came on a Thursday,
  so the print is dated Friday, the week's last trading day, and meets that close, public before the open (the 2008 Good Friday
  rule). The Q3 FY16 call's 8-K was accepted on Good Friday 2016-03-25 (15:34 ET, market closed) and is dated 2016-03-28; the
  Q4 FY17 call's at 16:00:17 ET, after the close, and is dated 2017-07-06. 2017-12-29 closes 2017-W52, so a 2018 batch starts on
  2018-01-01.
- **Segments** (display): six geographies, Global Brand Divisions and Converse in all three vintages. NIKE reports four NIKE
  Brand geographies from fiscal 2018 (the recast 8-K and the Q1 FY18 release); the bridge keeps the FY2017 10-K's lines until
  the FY2018 10-K (the 2009 recast rule).
- **Dividends:** $0.32 on the pre-split basis from the split 8-K ($0.16 after the split), $0.18 from the Q2 FY17 release
  (2016-12-21) and $0.20 from the Q2 FY18 release (2017-12-22); the vintages carry $0.28, $0.16 and $0.18.
- **An engine revision, text only for earlier dates.** A signal with no value scores BASE, and every line that prints futures
  has a branch for a print without them (dashboard, bear anatomy, conservative case, key trigger, volatility text, catalyst (1)
  and summary), as in the AAPL 2016-2019 revision. The builder gains `futures_later`, the ECOMMERCE encoding (LOW's, with
  NIKE's wording) and a franchise line without year-end futures. The 366 reports of 2008-2014 rebuild byte-identical; their
  models change only in the engine text. The firewall also plants, for NKE, futures that a filing after the cutoff first states
  on the last print before it.
- **Adds nothing:** the officer and director 8-Ks (the CFO succession of 2015-02-12, 2015-06-18, 2015-06-30, 2015-07-06,
  2016-04-21, and Philip Knight's retirement as chairman on 2016-07-01), the annual meetings (2015-09-23, 2016-09-30 and its 8-K/A
  of 2016-10-13, 2017-09-22 and the 8-K/A of 2017-11-22), the credit agreement (2015-09-02), the notes offerings (2015-10-29,
  2016-10-21; long-term debt enters through the 10-Ks), the bylaw amendments (2017-04-21, 2017-11-17), and the 10-Qs (tax-rate
  estimates; the Q1 FY18 10-Q's retail-landscape words are 10-Q wording, not a 10-K event).

Controls: altering one value of each new print, later-stated futures, Q4 full-year figure, vintage, guide, dividend, the split
and the event changes no date before it can be shown and changes the first weekly date on or after it (41 of 41). A guide for
the next fiscal year first shows on the first date with that year current and only until the next call: the Q3 FY15 call's
fiscal 2016 words on 2015-06-26, the Q3 FY16 call's fiscal 2017 words on 2016-06-30 and the Q3 FY17 call's fiscal 2018 words on
2017-06-30. The split changes the 106 dates from its effective date. No string of any print, vintage, guide, dividend, split,
event or source appears in a model dated before it (132,612 checks over the 522 NKE models). The firewall at the eight cutoffs
above changes no model before its cutoff. The 366 dates of 2008-2014 rebuild with byte-identical reports, and the 2008 dates
of ACN, UNP, LOW and AAPL rebuild unchanged.

Seen in the build (method behaviour, not tuned):
- **RICH on 155 of 156 dates** (all 52 in 2015, all 52 in 2016, 51 of 52 in 2017), FAIR on 2017-09-08 (20.8x FY17's $2.51,
  the 56th percentile), no CHEAP date. Tiers: AVOID 104 (all 52 of 2015), WATCHLIST 35, ACCUMULATE 8, BUY 9.
- **2015 traded at the top of its own range.** On FY15E's $3.56 (the "about 20%" guide) to 2015-06-19 the stock stood at
  25.8-29.9x, the 95th-100th percentile; on FY15's $3.70 from the Q4 FY15 print to 2015-12-18 at 28.9-36.3x (98th-100th); after
  the split, on $1.85, at 28.4-34.2x (90th-98th) to 2016-06-24. The price was above the BULL case on 61 dates, 2015-03-20 to
  2016-05-13 (Ratio B infinite).
- **From the Q4 FY16 print the anchor rose and the price fell.** On FY16's $2.16 (2016-06-30 to 2017-06-23) the stock traded at
  23.1-27.3x (67th-94th): RICH throughout, tier AVOID on 24 dates, WATCHLIST on 24, ACCUMULATE on 4. On FY17's $2.51 from
  2017-06-30 it traded at 20.3-25.8x (50th-85th): RICH on 26 of 27, BUY on 9 (2017-08-25 to 2017-10-20).
- **The anchor lags:** FY15's $3.70 ($1.85) stood until 2016-06-28, when nine-month FY16 EPS was $1.67; FY16's $2.16 until
  2017-06-29, nine-month FY17 EPS $1.91.
- **BEAR is flat on every date:** EPS rose in every year of each window. BASE is the quarter's currency-neutral growth plus the
  buyback (1.8-2.0%/yr): +20.0%/yr on Q2 FY15, +15.0% on Q3 and Q4 FY15, +16.0% on Q1 FY16, +14.0% on Q2 FY16, +16.0% on Q3
  FY16, +10.8-10.9% on Q4 FY16, +11.8% on Q1 FY17, +9.8% on Q2 FY17, +8.8% on Q3 FY17, +8.9-9.0% on Q4 FY17, +2.0% on Q1 FY18
  (flat revenue) and +5.0% on Q2 FY18. BASE lifts BULL to it to 2016-06-24; from the Q4 FY16 print BULL is the window's EPS
  CAGR, 12.3-13.1%/yr. XBULL is lifted to BASE to 2015-06-19, then FY13-FY15's +17.5%/yr, then FY14-FY16's +20.4-20.6%/yr.
- **The growth factor turned negative:** +0.22 to +0.5 to 2016-06-24 against the window's median revenue growth of 9.2-9.8%,
  -0.08 to +0.02 on Q4 FY16 and Q1 FY17, -0.15 to -0.5 from Q2 FY17.
- **The EPP floor P/E rose from 15x to 16x (from 2016-01-08), 17x (2017-09-28) and 18x (2017-10-13)** as low-multiple years
  left the window; no date sat below the floor (the closest, 12.8% above it).
- **The proxy composite drifted down:** 2.70 on Q2 FY15 and Q1 FY16, 2.50 on Q3 FY15, 2.15 on Q4 FY15, 2.55 on Q2-Q3 FY16, 2.20
  on Q4 FY16, 2.35 on Q1 FY17, 2.15 on Q2-Q3 FY17 and 2.00 from Q4 FY17 (every signal at BASE).
- **Robustness:** all eight variants agree on 122 of the 155 RICH dates and three to seven on the rest; on the FAIR date two of
  eight.

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- BASE and the growth factor on reported revenue growth instead of growth excluding currency would change 1 class (FAIR to RICH
  on 2017-09-08) and no tier;
- FY17 at a derived $2.40 excluding the Q1 FY17 tax benefit (Q1 taxed at the rest of the year's rate; no such figure was
  published, so a test only) would change 1 class (the same date) and 12 tiers;
- FY08 at GAAP $3.74 in the 2015-2017 vintages would change no class and 20 tiers (FY09's step becomes a fall, so BEAR is no
  longer flat);
- futures from the releases only (no value for Q2-Q4 FY17), the unreported futures slot re-weighted across the other signals
  instead of scored BASE, no ECOMMERCE watch, and the Q1 FY15 call's "about 20%" kept as words would change none.

Judgement calls that could carry hindsight:
- FY17 at GAAP $2.51 with the one-time tax benefit (a derived figure without it moves 1 class and 12 tiers);
- BASE on growth excluding currency changes (1 class), as in 2008-2014;
- FY08 at the company's $3.45 (20 tiers), and the seam between FY08 on the old basis and FY09-FY17 from continuing operations;
- ECOMMERCE on the watch list from the FY2017 10-K, on its own risk-factor words, for a brand rather than a physical retailer
  (text only);
- futures from the first filing that states them, and BASE with no value from Q1 FY18 (no class moves either way);
- the signals, chosen by a builder who knows how 2015-2017 went; DURABLE rather than CYCLICAL (the class label only).

### NKE 2018-2020: the Tax Act year excluded, no more call transcripts, COVID

```bash
python3 retro/build_nke.py --weekly 2018-01-01 2020-12-31                   # 157 dates, 2018-01-05 .. 2020-12-31
for c in 2018-03-23 2018-06-29 2018-07-25 2019-06-28 2019-07-24 2020-03-25 2020-06-26 2020-07-27 2021-01-01; do python3 retro/tools/firewall.py $c NKE; done
```

All 45 filings published from 2018-01-01 to 2020-12-31 (33 8-Ks, 9 10-Qs and the FY2018-FY2020 10-Ks) were read, with no
delegated transcription: the twelve releases in full; the two call transcripts' prepared remarks in full, with each Q&A searched
for figures (none gives an EPS, revenue or margin number); the items of every other 8-K and the exhibits of its Item 7.01 and 8.01
releases (the COVID-19 updates of 2020-02-04 and 2020-05-14, the South America transition of 2020-02-06, the CEO succession
and leadership changes, and the 2020-03-25 reprint of the Q3 FY20 results for the notes offering), not their legal exhibits;
the 10-Ks' business, risk-factor, selected-data, tax, segment and cash-flow sections; and the 10-Qs searched for outlook
statements (none in numbers). 316 strings were checked with `verbatim.py` against their own filings, among them every print's
income-statement and balance-sheet rows, every call's words and every vintage's rows; the FY2013 and FY2014 10-Ks were fetched
again for two first-year share counts. Each source's date comes from EDGAR's acceptance time. Thresholds and signals are
unchanged. Decided before any 2018-2020 date was built or scored:

- **Three vintages.** The FY2018 10-K (accepted 2018-07-24 18:22 ET, dated 2018-07-25) gives FY2014-FY2018, the FY2019 10-K
  (2019-07-23 16:13 ET, dated 2019-07-24) FY2015-FY2019 and the FY2020 10-K (Friday 2020-07-24 16:07 ET, dated Monday
  2020-07-27) FY2016-FY2020. Windows FY2009-FY2018, FY2010-FY2019 and FY2011-FY2020; every earlier year from the latest 10-K
  that reports it, and the first year's diluted shares from the same 10-K: FY2009's 981.4M (FY2013 10-K), FY2010's 987.8M (FY2014
  10-K) and FY2011's 971.3M (FY2015 10-K), all before the 2015 split. FY08's $3.45 on the old basis leaves the window with the
  FY2018 10-K, and with it the seam of "NKE 2012-2014".
- **FY18 is excluded (a distorted year, the r2 rule).** The Q3 FY18 release (dated 2018-03-23) reports a diluted net loss of
  $0.57 after "additional income tax expense of $2.0 billion" from the Tax Cuts and Jobs Act, whose "one-time provisional charges
  ... reduced diluted earnings per share by $1.25". FY18's diluted EPS is $1.17 (Q4 FY18 release, 2018-06-29), with net income
  of $1,933M; the FY2018 10-K lists the charges as "provisional expense of $1,875 million for the one-time transition tax ... and
  $158 million resulting from the remeasurement of deferred tax assets and liabilities", and the FY2019 10-K made no adjustment
  to them. The items exceed the year's net income (the AAPL FY2002 test), and no EPS excluding them was published: the "$1.25"
  is a per-share effect, not an EPS without it, and no figure is derived from it (the NKE 2008 rule). Both facts of the test are
  public with the Q4 FY18 print, so the exclusion starts there. The rule's "the P/E window starts after it" assumes a first
  year: for the latest year it would leave no history and no window, so the method gains a note for a distorted latest year
  (see "Retro method r2"; no earlier output changes, so still r2):
  - FY18 leaves the EPS history (vintages: `eps_excluded`; the Q4 print: a `fy_actual` with no EPS). Its revenue, shares and
    margins stay; its 55.3% tax rate stays as the fact, so the display-only EPS check reads $1.27 until the FY2019 10-K.
  - FY18's own days leave the P/E window ("10-yr ex-FY18", about nine years of days).
  - BEAR takes one-year changes between consecutive years only, so FY17-FY19 is not a BEAR year; XBULL takes two-year runs whose
    ends are both in the history, so FY17-FY19 counts; BULL runs from the first year to the last ("FY09-FY19 ex-FY18").
  - The rollover rule's last full year is the last year in the history: FY17's $2.51 stands for FY19E from 2018-06-29 to the
    Q4 FY19 print, and the EPS label says why ("FY18 is excluded: GAAP $1.17 after the Tax Act's one-time charges ...").
  The builder works around the shared split helper for a year with no EPS (it refuses a split after an excluded year until
  that is decided). FY17 keeps its one-time tax benefit and FY20 its South America charge: each is a fraction of the year's net
  income, so neither year is excluded (the AAPL FY2003 test).
- **No guide in numbers, and from FY20 no words.** The Q3 FY18 call's fiscal 2018 words ("excluding the one-time impact of
  U.S. Tax Reforms", Q4 revenue "in the high single- digit range", as transcribed) replace the Q2 FY18 call's; its fiscal 2019
  words ("mid-to high-single-digit") show from 2018-06-29, the first date with fiscal 2019 current, and the Q4 FY18 call's
  ("entering the high-single-digit range", gross margin "roughly 50-basis points or slightly greater") from 2018-07-06. The Q4
  FY18 call is the last transcript NIKE furnished by 8-K; no release, 10-Q, 10-K or 8-K of 2018-2020 states an outlook in
  numbers (the 2020-02-04 update says COVID-19 "was not contemplated at the time we provided Q3 guidance during our Q2 fiscal
  year 2020 earnings call", a call not filed), so FY20 and FY21 show no outlook and the last full year stands: FY17's $2.51
  for FY19, FY19's $2.49 for FY20, FY20's $1.60 for FY21.
- **One-offs and COVID as reported.** Q3 FY20 and FY20 include the South America distributor-transition charge ("a $0.25
  non-recurring, non-cash charge"; $400 million in Q3) and Q2 FY21 restructuring costs in gross margin: no figure without them
  was published, so GAAP stands, and margins are GAAP throughout (the 2009 rule). The COVID-19 quarters enter as released: Q4
  FY20 revenue -38% (-36% excluding currency), gross margin -822bp, a pre-tax loss (-2,494bp) and inventories +31% (a +69pp gap),
  with no new field. The loss quarters' diluted share counts are the basic ones, as published (Q3 FY18, Q4 FY20).
- **Accounting changes:** the revenue standard (Topic 606, fiscal 2019, modified retrospective; "did not have a material effect"
  on the income statement) and the lease standard (Topic 842, fiscal 2020, balance sheet only) restate nothing.
- **ECOMMERCE stays on the watch list.** Each 10-K replaces the last (the 2015-2017 encoding): the FY2018 and FY2019 10-Ks name
  "the rising trend of digital commerce" as "a risk factor implicating our NIKE Direct and wholesale operations" (the FY2017 10-K
  said "DTC"), and the FY2020 10-K "the continued proliferation of digital commerce"; NIKE's own digital commerce was $2.8 billion
  in fiscal 2018, $3.8 billion in 2019 and $5.5 billion in 2020. Company-acknowledged, no market read; text only. No other theme
  is live for NIKE (EV and CRYPTO from 2020 are scoped to other industries).
- **Calendar.** Every release came after the close (16:16-17:09 ET). Q1 FY19, Q1 FY20, Q3 FY20 and Q1 FY21 came on a Tuesday, so
  the week's date is Thursday; the others on a Thursday, dated Friday and meeting that close, except Q2 FY21 (Friday
  2020-12-18, dated Monday 2020-12-21, the week's date 2020-12-22). The Q4 FY18 call's 8-K was accepted 2018-07-03 at 14:31 ET,
  after that day's 13:00 early close before Independence Day, so it is dated 2018-07-05 (the first early close in a fact
  sheet; it moves no weekly date). 2020-12-31 closes 2020-W53.
- **Segments** (display): from the FY2018 vintage the four NIKE Brand geographies (North America; Europe, Middle East & Africa;
  Greater China; Asia Pacific & Latin America), Global Brand Divisions and Converse; Corporate left out. Hurley, sold on
  December 6, 2019, leaves the FY2020 vintage's business line.
- **Dividends:** $0.22 a quarter from the Q2 FY19 release (2018-12-21), $0.245 from Q2 FY20 (2019-12-20) and $0.275 from Q2 FY21
  (2020-12-21); the vintages carry $0.20, $0.22 and $0.245. Repurchases: the $12 billion program completed in Q3 FY19 and the
  $15 billion program of June 2018 began; NIKE suspended repurchases in March 2020.
- **An engine revision, text only for earlier dates:** EPS growth over a gap in the history (above) and the span label. The 522
  reports of 2008-2017 rebuild byte-identical; their models change only in the engine text.
- **Adds nothing:** the officer and director 8-Ks (2018-02-21, 2018-03-15 with Trevor Edwards' resignation, 2018-07-12,
  2018-11-19, 2019-04-23, the CEO succession of 2019-10-22, 2019-11-14, 2020-02-18, 2020-05-27), the annual meetings
  (2018-09-21, 2019-09-23, 2020-09-18), the credit agreement (2019-08-20), the $6 billion notes (2020-03-27; long-term debt enters
  through the 10-Ks), the bylaw and plan amendments (2020-06-19), the COVID-19 updates and the South America announcement
  (words and an expected charge, no outlook), and the 10-Qs (tax estimates, accounting notes and the Q1 FY21 10-Q's expected
  restructuring charge of about $315 million).

Controls: altering one value of each new print, Q4 full-year figure, vintage, guide, dividend and event, and putting FY18 back at
GAAP in the Q4 FY18 print and in each vintage, changes no date before it can be shown and changes the first weekly date on or
after it (31 of 31). The Q3 FY18 call's fiscal 2019 words first show on 2018-06-29 and only that week. No string
of any new print, vintage, guide, dividend, event or source appears in a model dated before it (108,236 checks over the 679 NKE
models). The firewall at the nine cutoffs above changes no model before its cutoff. The 522 dates of 2008-2017 rebuild with
byte-identical reports.

Seen in the build (method behaviour, not tuned):
- **RICH on 156 of 157 dates** (all 52 in 2018, all 52 in 2019, 52 of 53 in 2020), FAIR on 2020-03-20 (the COVID-19 low: $67.45,
  27.1x FY19's $2.49, the 72nd percentile; tier ACCUMULATE). Tier AVOID on the other 156. No CHEAP date.
- **The anchors:** FY17's $2.51 to 2019-06-21 (77 dates; for FY18E by the rollover rule to 2018-06-22, then for FY19E with FY18
  excluded) at 25.5-35.5x, the 83rd-100th percentile; FY19's $2.49 to 2020-06-19 at 27.1-42.0x (72nd-100th); FY20's $1.60 from
  2020-06-26 at 58.5-89.0x (96th-100th). The price was above the BULL case on 85 dates (Ratio B infinite), from 2018-06-29.
- **The anchor lags:** FY17's $2.51 stood until 2019-06-27, when nine-month FY19 EPS was already $1.87; FY19's $2.49 until
  2020-06-25 (nine-month FY20 $2.09); FY20's $1.60, a year with a COVID-19 fourth quarter, stands through 2020 while Q1 FY21
  alone earned $0.95 and the first half $1.73 (2020-12-21).
- **BEAR is flat to 2020-06-19** (with FY18 out, EPS rose in every pair of consecutive years), then -35.7%/yr from the Q4 FY20 print
  (FY19 to FY20). **BASE** is the quarter's currency-neutral growth plus the buyback (1.9-2.2%/yr): +5.0%/yr on Q2 and Q3 FY18,
  +9.9-10.0% on Q4 FY18, +10.9% on Q1 FY19, +15.9% on Q2 FY19, +12.9% on Q3 FY19, +11.9-12.2% on Q4 FY19 and Q1 FY20, +15.2% on
  Q2 FY20, +9.2% on Q3 FY20, -33.8% on Q4 FY20, +2.2% on Q1 FY21 and +9.2% on Q2 FY21. BULL is the window's EPS CAGR (12.6-13.8%/yr
  to the Q4 FY19 print, 10.8-11.0% to the Q4 FY20 print, 4.1-5.1% after it) or BASE where higher; XBULL is FY14-FY16's +20.4%/yr
  throughout.
- **The window's multiples rose:** the median P/E from 20.5x to 24.8x and the 90th percentile from 26.5x to 33.7x before the Q4
  FY20 print, then 52.1-58.3x once FY20's and FY21's days sit on $1.60. The EPP floor P/E is 19x to 2019-12-27 and 20x from
  2020-01-03; no date came within 34% of it, and none sat below the BEAR price.
- **The growth factor** against the window's median revenue growth (7.3-8.5%): -0.5 on Q2-Q3 FY18 (+3%), about 0 on Q4 FY18 and
  Q1 FY19, +0.5 on Q2 FY19 (+14%), +0.15 to +0.45 to Q2 FY20, -0.15 on Q3 FY20, -0.5 on Q4 FY20 and Q1 FY21, -0.05 on Q2 FY21.
- **The proxy composite:** 2.00 on Q2-Q3 FY18, 2.50-2.65 from Q4 FY18 to Q3 FY19, 2.20 on Q4 FY19, 2.65 on Q1 FY20, 2.30 on Q2
  FY20, 2.00 on Q3 FY20, 1.35 on Q4 FY20 (revenue, gross margin, pre-tax margin and the inventory gap all at BEAR), 2.15 on Q1 FY21
  and 2.60 on Q2 FY21.
- **Robustness:** all eight variants agree on 150 of the 156 RICH dates and seven on the rest; on the FAIR date five of eight.

How far each call moves the classes (the 157 dates rebuilt with one encoding changed; no outcome consulted):
- FY18 at GAAP $1.17 instead of excluded would change no class and 1 tier (2020-03-20, ACCUMULATE to WATCHLIST): the stock is RICH
  either way, but the numbers differ: FY19E $1.17 at 61-76x from 2018-06-29 to the Q4 FY19 print, BEAR -53.4%/yr on every date
  from 2018-06-29, and the window's 90th percentile 45-62x instead of 27-30x to the Q4 FY19 print and 36-42x instead of 30-34x to
  the Q4 FY20 print;
- BASE and the growth factor on reported revenue growth instead of growth excluding currency would change 1 class (FAIR to RICH
  on 2020-03-20) and 1 tier;
- the exclusion from the FY2018 10-K instead of the Q4 FY18 print, FY20 excluded as well (a test: it is not a distorted year), no
  ECOMMERCE watch, and the unreported futures slot re-weighted instead of scored BASE would change none.

Judgement calls that could carry hindsight:
- FY18 excluded rather than at GAAP, and the mechanics of a distorted latest year (FY17's $2.51 as the FY19 anchor, the window
  without FY18's days, growth over the gap): no class moves either way, but the scenario numbers do;
- FY20 kept at GAAP $1.60 although COVID-19 hit its fourth quarter (the test is listed items against net income, and a
  pandemic is not an item); it drives BEAR (-35.7%/yr) and the 52-58x upper percentiles of late 2020;
- BASE on growth excluding currency (1 class), as in 2008-2017;
- dating the Q4 FY18 call after the 2018-07-03 early close (moves no weekly date);
- the signals, chosen by a builder who knows how 2018-2020 went; DURABLE rather than CYCLICAL (the class label only).

### NKE 2021-2023: three-year 10-Ks, the post-COVID anchors, an inventory cycle

```bash
python3 retro/build_nke.py --weekly 2021-01-01 2023-12-31                   # 156 dates, 2021-01-08 .. 2023-12-29
for c in 2021-03-19 2021-06-25 2021-07-21 2022-06-28 2022-07-22 2022-09-30 2023-06-30 2023-07-21 2023-12-22 2024-01-01; do python3 retro/tools/firewall.py $c NKE; done
```

All 36 filings published from 2021-01-01 to 2023-12-31 (24 8-Ks, 9 10-Qs and the FY2021-FY2023 10-Ks) were read, with no
delegated transcription: the twelve releases in full; the items of every other 8-K (officer, director, meeting and credit
8-Ks, and the Q2 FY24 restructuring under Item 2.05) with their press-release exhibits, not their legal exhibits; the 10-Ks'
business, risk-factor, income-statement, tax, segment, cash-flow and equity sections; and the 10-Qs searched for outlook
statements (words only). 295 strings were checked with `verbatim.py` against their own filings, among them every print's
income-statement and balance-sheet rows and every vintage's rows. Each source's date comes from EDGAR's acceptance time.
Thresholds, signals and the engine are unchanged; the builder gains only its usage line. Decided before any 2021-2023
date was built or scored:

- **Three vintages from 10-Ks without selected financial data.** The FY2021 10-K (accepted 2021-07-20 16:11 ET, dated
  2021-07-21) and the FY2022 10-K (2022-07-21 16:05 ET, dated 2022-07-22) answer Item 6 "Not applicable", and the FY2023 10-K
  (2023-07-20 16:20 ET, dated 2023-07-21) "[RESERVED]": each reports three years, in its income statement. Each year still comes
  from the latest 10-K that reports it: in the FY2021 vintage FY19-FY21 from the FY2021 10-K, FY16-FY18 from the FY2020 10-K,
  FY15 from FY2019's, FY14 from FY2018's, FY13 from FY2017's and FY12 from FY2016's. Windows FY2012-FY2021, FY2013-FY2022 and
  FY2014-FY2023; the first year's diluted shares FY2012's 1,879.2M (FY2016 10-K), FY2013's 1,832.9M (FY2017 10-K) and FY2014's
  1,811.6M (FY2018 10-K).
- **No year excluded, and FY18 stays out.** FY21's restructuring charges ($294 million pre-tax), and FY22's Russia
  deconsolidation charge ($96 million), fourth-quarter charges ("approximately $150 million") and one-time onshoring tax benefit
  (4.7 points of the rate), are each a fraction of the year's net income ($5,727M, $6,046M), and no figure without them was
  published: GAAP stands, $3.56, $3.75 and $3.23 for FY21-FY23. FY18 stays excluded in every vintage (all three windows hold it),
  and FY20 stays at $1.60.
- **Still no guide.** No call transcript was furnished, and no release, 10-Q, 10-K or 8-K states an outlook in numbers. The FY2021
  10-K's long-term targets (high-single to low-double-digit revenue growth, a gross margin in the high 40s and an EBIT margin in
  the high teens by fiscal 2025, mid-to-high-teens EPS growth) are multi-year and not entered (the LOW rule). Executives' quotes
  in the releases are not guides, as in 2008-2020: the Q2 FY24 release's "softer second-half revenue outlook" and "Revised
  guidance will be provided on the conference call" are noted here, not entered. So the last full year stands: FY20's $1.60 for
  FY21 to the Q4 FY21 print, then FY21's $3.56, FY22's $3.75 and FY23's $3.23.
- **Dividends from the releases.** $0.305 a quarter from the Q2 FY22 release (2021-12-21), $0.34 from Q2 FY23 (2022-12-21) and
  $0.37 from Q2 FY24 (2023-12-22). The 10-Ks now give only the year's total ($1.070, $1.190 and $1.325 a share), so each vintage
  carries the latest release's quarterly rate with that release's date (`dividend_published`); no figure is derived.
- **ECOMMERCE stays on the watch list,** each 10-K replacing the last with the same sentence ("the continued proliferation of
  digital commerce") and its own digital figure: digital commerce sales of $9.1 billion in fiscal 2021, NIKE Brand Digital $10.7
  billion in 2022 and $12.6 billion in 2023. Text only. No other theme is live for NIKE (GENAI from 2022-11-30 and CRYPTO are
  scoped to other industries).
- **Calendar.** Every release came after the close (16:12-16:18 ET). Q3-Q4 FY21, Q1 FY22, Q1 FY23, Q4 FY23 and Q1-Q2 FY24 came on
  a Thursday, dated Friday and meeting that close; Q2-Q4 FY22 on a Monday (dated Tuesday, the week's date Wednesday); Q2 and Q3
  FY23 on a Tuesday (the week's date Thursday). No filing came on an early-close day.
- **Q4 FY21 is compared with the COVID-19 quarter:** revenue +96%, gross margin +854bp, pre-tax margin +2,776bp and an
  inventory gap of -102pp, all past their XBULL thresholds, and BASE +89.9%/yr (the quarter's +88% excluding currency plus the
  buyback): as released, with no new field.
- **Segments** (display): the four NIKE Brand geographies, Global Brand Divisions and Converse in all three vintages; the
  business line names "the NIKE and Jordan brands".
- **Adds nothing:** the officer and director 8-Ks (the performance-award form of 2021-06-17, 2021-11-01, 2022-05-05, 2022-06-10,
  2022-09-20, 2023-05-09, the leadership changes of 2023-05-24), the annual meetings (2021-10-08, 2022-09-14, 2023-09-15), the
  credit agreements (2021-03-18, 2022-03-14, 2023-03-13), and the 10-Qs (supply-chain, promotion and gross-margin words, no
  numbers).

Controls: altering one value of each new print, Q4 full-year figure, vintage, dividend and event, and putting FY18 back at GAAP
in each vintage, changes no date before it can be shown and changes the first weekly date on or after it (27 of 27). No string
of any new print, vintage, dividend, event or source appears in a model dated before it (119,837 checks over the 835 NKE
models). The firewall at the ten cutoffs above changes no model before its cutoff. The 679 dates of 2008-2020 rebuild
byte-identical.

Seen in the build (method behaviour, not tuned):
- **The classes spread out:** RICH on 76 of 156 dates, FAIR on 65 and CHEAP on 15, the first CHEAP NKE dates since 2014 (2021: 39
  RICH and 13 FAIR; 2022: 20, 24 and 8; 2023: 17, 28 and 7). Tiers: AVOID 74, WATCHLIST 41, ACCUMULATE 24, BUY 17.
- **The anchors:** FY20's $1.60 to 2021-06-18 (24 dates) at 80.3-91.5x, the 93rd-100th percentile, RICH and AVOID throughout;
  FY21's $3.56 from the Q4 FY21 print to 2022-06-24 (53) at 30.2-49.9x (59th-90th), FAIR and BUY on the 13 dates to 2021-09-17,
  then mostly RICH; FY22's $3.75 from 2022-06-29 to 2023-06-23 (52) at 22.2-34.4x (20th-71st), FAIR on 35, CHEAP on 15 and RICH
  on 2; FY23's $3.23 from 2023-06-30 (27) at 28.1-37.6x (39th-75th), RICH on 17 and FAIR on 10. The price was above the BULL case
  on 35 dates, all in 2021 (Ratio B infinite).
- **The window carries FY20.** FY20's own days, on its $1.60, sit at about 38-66x, so the window's 90th percentile is 58.5-61.4x to
  the Q4 FY21 print (FY21's days were on $1.60 too) and 50.8x after it, and its median rose from 24.9x to 31.6x. So 40-50x on
  FY21's $3.56 read as the 59th-90th percentile, and the EPP floor P/E (the median of calendar-year lows) rose from 20x to 26x.
  No date sat below the floor or the BEAR price; the closest, 2022-09-30, 0.8% above the floor ($83.12, 22.2x).
- **BEAR is -35.7%/yr on every date** (FY19 to FY20). **BASE** is the quarter's currency-neutral growth plus the buyback
  (1.45-2.24%/yr): +9.2%/yr on Q2 FY21, +1.2% on Q3 FY21, +89.9% on Q4 FY21, +13.7% on Q1 FY22, +1.7% on Q2 FY22, +9.7% on Q3
  FY22, +4.4-4.6% on Q4 FY22, +11.4% on Q1 FY23, +28.4% on Q2 FY23, +20.4% on Q3 FY23, +9.6% on Q4 FY23, +3.6% on Q1 FY24 and
  +0.6% on Q2 FY24. BULL is the window's EPS CAGR (4.1%/yr to the Q4 FY21 print, 12.1-12.8% to the Q4 FY23 print, 9.0-9.2% after)
  or BASE where higher; XBULL is FY14-FY16's +20.4%/yr, lifted to BASE on Q4 FY21, and FY20-FY22's +53.1%/yr from the Q4 FY22 print.
- **The growth factor,** against the window's median revenue growth (6.1-8.0%): -0.5 on Q3 FY21, Q2 FY22 and Q2 FY24; +0.5 on Q4
  FY21 and Q2-Q3 FY23; +0.45 on Q1 FY22, +0.39 on Q1 FY23, -0.31 to -0.38 on Q4 FY22, -0.41 on Q1 FY24, and -0.05 to +0.19 on the rest.
- **The proxy composite:** 2.60 on Q2 FY21, 2.50 on Q3 FY21, 3.30 on Q4 FY21, 2.95 on Q1 FY22, 2.40 on Q2 FY22, 2.20 on Q3 FY22,
  1.85 on Q4 FY22 and Q1 FY23 (inventories +23% and +44%), 2.15 on Q2-Q4 FY23, 2.30 on Q1 FY24 and 2.80 on Q2 FY24.
- **Robustness:** all eight variants agree on 50 of the 76 RICH dates (four to eight on the rest), on 6 of the 65 FAIR dates
  (four to eight), and on none of the CHEAP dates (six or seven of eight).

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- FY20 excluded as well (a test: by the test of listed items against net income it is not a distorted year) would change 32
  classes and 55 tiers, the largest of the batch;
- FY18 at GAAP $1.17 instead of excluded would change 13 classes and 21 tiers;
- BASE and the growth factor on reported revenue growth instead of growth excluding currency would change 13 classes and 15 tiers;
- the unreported futures slot re-weighted instead of scored BASE would change 3 classes and no tier, and no ECOMMERCE watch none.

Judgement calls that could carry hindsight:
- FY20 kept at GAAP $1.60, a year with a COVID-19 fourth quarter (the test is listed items against net income): it sets BEAR at
  -35.7%/yr on every date, the FY21E anchor to the Q4 FY21 print (80-91x) and the window's high percentiles, against which 40-50x
  reads as average (32 classes and 55 tiers as a test);
- FY18 excluded (13 classes, 21 tiers);
- BASE on growth excluding currency (13 classes), as in 2008-2020;
- the releases' outlook quotes kept out of the guide line (display only), and dividends from the releases (no class moves);
- the signals, chosen by a builder who knows how 2021-2023 went; DURABLE rather than CYCLICAL (the class label only).

### NKE 2024-2026: an adjusted FY24, two GAAP years with one-off items, the first EPS range

```bash
python3 retro/build_nke.py --weekly 2024-01-01 2026-10-30                   # 148 dates, 2024-01-05 .. 2026-10-30
for c in 2024-03-22 2024-06-28 2024-07-26 2025-06-27 2025-07-18 2026-04-01 2026-07-01 2026-07-16 2026-10-02 2026-10-31; do python3 retro/tools/firewall.py $c NKE; done
```

All 42 filings published from 2024-01-01 to 2026-10-30 (30 8-Ks, 9 10-Qs and the FY2024-FY2026 10-Ks) were read, with no
delegated transcription: the eleven releases in full; the items of every other 8-K (officer, director, meeting, bylaw and credit
8-Ks, the cost realignment under Item 2.05 dated 2026-03-06, and the purchase-obligation correction of 2025-07-28) with their
press-release exhibits, not their legal exhibits; the 10-Ks' business, risk-factor, income-statement, tax, segment, cash-flow
and equity sections; and the 10-Qs searched for outlook statements (words only). 282 strings were checked with `verbatim.py`
against their own filings, among them every print's income-statement and balance-sheet rows and every vintage's rows. Each
source's date comes from EDGAR's acceptance time. Thresholds, signals and the engine are unchanged. Decided on 2026-10-31,
before any 2024-2026 date was built or scored:

- **FY24 at the company's $3.95.** The Q4 FY24 release (dated 2024-06-28) gives diluted EPS excluding restructuring charges, $3.95
  for fiscal 2024 against GAAP $3.73, and $1.01 for the quarter against $0.99; the Q3 FY24 release gives "Excluding these charges,
  Diluted earnings per share would have been $0.98" (GAAP $0.77). The charges were announced with the Q2 FY24 release (Item 2.05,
  dated 2023-12-22), so the ACN rule applies, as for FY09 ("NKE 2009-2011"): the prints show the company's figures with GAAP in
  the note, FY24 enters the history at $3.95 from the Q4 FY24 print, and every later vintage keeps it although the 10-Ks state
  GAAP only (an adjusted year keeps its figure, the LOW rule). Q3 and Q4 FY25 compare with $0.98 and $1.01, as their releases
  reconcile them again. Margins stay GAAP.
- **FY25 and FY26 at GAAP, $2.16 and $2.10.** FY25 includes "a one-time, non-cash deferred tax benefit" (Q3 FY25); FY26
  includes "a $0.52 benefit related to the expected recovery of the IEEPA tariffs" (Q4 FY26, $986 million, about 900 basis
  points of the quarter's gross margin) and employee severance costs (about $300 million for the nine months, the Item 2.05
  8-K dated 2026-03-06). Each is an
  impact with no figure excluding it, so GAAP stands (the Fremont rule, as for AAPL's and LOW's tariff items), and each is a
  fraction of the year's net income, so no year is excluded. FY18 stays excluded: all three windows hold it.
- **The first EPS range: FY27E is its midpoint.** The Q1 FY27 release (dated 2026-10-02) has an Outlook section: "Revenues are
  expected to decline high-single digits in fiscal 2027", a tax rate "in the mid-20 percent range", and adjusted diluted EPS
  "expected to be in the range of $1.15 to $1.35, which excludes approximately $0.15 of restructuring expenses related to Pace
  for fiscal 2027". The range is a guide in numbers, given excluding an announced item (Pace, under Item 2.05 of the same
  8-K), so FY27E is its midpoint, $1.25, on the company's basis (the ACN rule; nothing is derived). The revenue and tax words
  are display only: BASE stays on the quarter's growth excluding currency. The builder gains two guide fields for it,
  `eps_guide` and `eps_guide_note` (no earlier guide has them), and its usage line.
- **Three vintages, three-year 10-Ks.** The FY2024 10-K (accepted 2024-07-25 16:16 ET, dated 2024-07-26), the FY2025 10-K
  (2025-07-17 16:25 ET, dated 2025-07-18) and the FY2026 10-K (2026-07-15 16:43 ET, dated 2026-07-16) each report three years.
  Each year comes from the latest 10-K that reports it. Windows FY2015-FY2024, FY2016-FY2025 and FY2017-FY2026; the first year's
  diluted shares FY2015's 1,768.8M (FY2019 10-K), FY2016's 1,742.5M and FY2017's 1,692.0M (FY2020 10-K).
- **No other guide.** The Q1 FY25 release says NIKE "will address its approach to guidance on the conference call" and
  postpones its Investor Day; the Q4 FY24 release's "update our Fiscal '25 outlook" and the June 2026 8-K's words on tariff
  refunds "not contemplated in the company's previously provided guidance" give no number. Executives' quotes stay out of the
  guide line, as in 2008-2023. So the last full year stands until the range: FY23's $3.23 for FY24, FY24's $3.95 for FY25,
  FY25's $2.16 for FY26 and FY26's $2.10 for FY27 until 2026-10-02.
- **Dividends from the releases:** $0.40 a quarter from the Q2 FY25 release (2024-12-20) and $0.41 from Q2 FY26 (2025-12-19);
  the 10-Ks give only the year's total ($1.450, $1.570 and $1.63 a share), so each vintage carries the latest release's rate
  with its date.
- **ECOMMERCE stays on the watch list,** a judgement call. The FY2024-FY2026 10-Ks drop "the continued proliferation of
  digital commerce" but say NIKE Direct competes "with digital commerce platforms", and keep "shifts in the ways in which
  consumers shop" as a risk factor for the NIKE Direct and wholesale operations. Text only, with each 10-K's digital figure:
  NIKE Brand Digital $12.1 billion in fiscal 2024, $9.6 billion in 2025 and $8.6 billion in 2026. The FY2025 and FY2026 10-Ks
  name artificial intelligence among the changes in technology and competition; GENAI's scope, AI that substitutes the core
  product, names nothing NIKE sells, so no theme.
- **Calendar.** Every release came after the close (16:15-16:18 ET). Q3-Q4 FY24, Q2-Q4 FY25, Q2 FY26 and Q1 FY27 came on a
  Thursday, dated Friday and meeting that close; Q1 FY25, Q1 FY26, Q3 FY26 and Q4 FY26 on a Tuesday, dated Wednesday, the
  week's date Thursday (for Q3 FY26 2026-04-02, before Good Friday; for Q4 FY26 2026-07-02, before the Independence Day holiday
  of 2026-07-03). No filing came on an early-close day. The last date is 2026-10-30, the last full week before the build
  (prices to 2026-10-30); a later batch starts on 2026-11-02.
- **Segments** (display): the four NIKE Brand geographies, Global Brand Divisions and Converse in all three vintages. The move
  to three geographies announced with Pace is not yet reported.
- **Adds nothing:** the officer and director 8-Ks (2024-06-05, 2024-09-19, 2025-05-05, 2025-06-18, 2025-06-25, 2025-12-02,
  2026-06-18, 2026-08-10, 2026-09-16), the bylaw amendment (2024-09-20), the annual meetings (2024-09-13, 2025-09-11,
  2026-09-10), the credit agreements (2024-03-11, 2025-03-10, 2026-03-09), the purchase-obligation correction (2025-07-28), the
  June 2026 8-K's words ("generally in line with previously provided guidance", excluding the tariff refunds), and the 10-Qs
  (outlook words only).

Controls: altering one value of each new print, Q4 full-year figure, vintage, dividend, event and the FY27 range, and putting
FY18 back at GAAP in each vintage, changes no date before it can be shown and changes the first weekly date on or after it (27
of 27). No string of any new print, vintage, guide, dividend, event or source appears in a model dated before it, nor do 20
distinctive figures and words ($3.95, IEEPA, Pace, $1.15-1.35 and others) (157,237 checks over the 983 NKE models). The firewall
at the ten cutoffs above changes no model before its cutoff. The 835 dates of 2008-2023 rebuild byte-identical.

Seen in the build (method behaviour, not tuned):
- **CHEAP returns:** CHEAP on 80 of 148 dates, RICH on 40 and FAIR on 28 (2024: 27 CHEAP and 25 FAIR; 2025: 25 CHEAP, 26 RICH
  and 1 FAIR; 2026: 28 CHEAP, 14 RICH and 2 FAIR). Tiers: BUY 63, AVOID 45, WATCHLIST 23, ACCUMULATE 17.
- **The anchors:** FY23's $3.23 to 2024-06-21 (25 dates) at 27.5-32.7x, the 30th-54th percentile, FAIR throughout (WATCHLIST 19,
  AVOID 5, ACCUMULATE 1); FY24's $3.95 from the Q4 FY24 print to 2025-06-20 (52) at 13.8-22.6x (0th-12th), CHEAP and BUY
  throughout; FY25's $2.16 from 2025-06-27 to 2026-06-26 (53) at 18.9-36.3x (0th-67th), RICH and AVOID on 35 of the 36 dates to
  2026-02-27 (FAIR on 2025-12-19), then CHEAP on 15 of the last 17; FY26's $2.10 from 2026-07-02 to 2026-09-25 (13) at 16.9-21.1x
  (0th-6th), CHEAP throughout (BUY 7, ACCUMULATE 6); the FY27 range's $1.25 from 2026-10-02 (5) at 27.1-30.9x (19th-37th), RICH
  and AVOID.
- **RICH at an average multiple.** The RICH dates sit at 27.1-36.3x, the 19th-67th percentile: what makes them RICH is the
  scenarios, not the multiple. From the Q4 FY25 print BEAR is FY24-FY25's -45.3%/yr (to $15 on FY25's $2.16, $9 on the
  range's $1.25), while BULL, the window's EPS CAGR or BASE where higher, is 0.0-1.8%/yr and then -2.0% (FY16's $2.16 to
  FY25's $2.16 is 0.0%; FY17-FY26 is -2.0%). Ratio B is 1.83-13.72 on the 35 RICH dates to 2026-02-27 and 2.05-4.05 on the
  five of October 2026.
- **The floor.** 79 dates sat below the EPP floor: all 52 on FY24's $3.95 (the deepest 2025-04-11, 40.1% below it at $54.39,
  13.8x), and all 27 from 2026-03-27 to 2026-09-25 (2026-03-13 sat at it). The floor P/E (the median of calendar-year lows) was
  23-26x. No date sat below the BEAR price or above the BULL price.
- **BEAR** is -35.7%/yr (FY19 to FY20) to 2025-06-20 and -45.3%/yr (FY24 to FY25) after. **BASE** is the quarter's growth
  excluding currency plus the buyback: +0.6%/yr on Q2 FY24, +1.6-1.7% on Q3-Q4 FY24, -7.4% on Q1-Q2 FY25, -5.4% on Q3 FY25,
  -9.2 to -9.3% on Q4 FY25, +0.8% on Q1 FY26, +1.8% on Q2 FY26, -1.2% on Q3 FY26, -2.4 to -2.5% on Q4 FY26 and -3.5% on Q1 FY27.
  BULL is 9.0%/yr to the Q4 FY24 print and 8.8-10.2% to the Q4 FY25 print, then 1.6%, 0.0% (BASE's +0.8% and +1.8% where
  higher), -0.3% from the Q4 FY26 print and -2.0% from the FY2026 10-K. XBULL is FY20-FY22's +53.1%/yr throughout.
- **The growth factor is -0.5 on every date:** no quarter's growth excluding currency (-11% to 0%) came near the window's
  median (4.9-6.1%).
- **The proxy composite:** 2.80 on Q2 and Q4 FY24, 2.50 on Q3 FY24, 2.05 on Q1 FY25, 2.00 on Q2 FY25, 1.85 on Q3 FY25, 1.50 on
  Q4 FY25, 2.00 on Q1-Q3 FY26, 2.70 on Q4 FY26 (the tariff recovery's gross margin) and 2.20 on Q1 FY27.
- **Robustness:** all eight variants agree on 79 of the 80 CHEAP dates (seven on the other), on 14 of the 40 RICH dates (six or
  seven on the rest), and on none of the 28 FAIR dates (two to six).

How far each call moves the classes (the 148 dates rebuilt with one encoding changed; no outcome consulted):
- FY26 without the IEEPA recovery ($1.58, a derived figure, so a test only) would change 10 classes and 13 tiers, all from
  2026-07-02 to 2026-09-25 (CHEAP to RICH or FAIR);
- FY18 at GAAP $1.17 instead of excluded would change 8 classes and 21 tiers;
- the FY27 range not used (FY26's $2.10 standing) would change 5 classes and 5 tiers: the five dates from 2026-10-02, RICH and
  AVOID to CHEAP and BUY;
- FY20 excluded as well (a test) would change 4 classes and 23 tiers;
- BASE and the growth factor on reported revenue growth would change 1 class and 10 tiers;
- the unreported futures slot re-weighted instead of scored BASE would change 6 classes (spring 2024, FAIR to CHEAP) and no tier;
- FY24 at GAAP $3.73 would change no class and 4 tiers; the range less the Pace charges ($1.10, a test) and no ECOMMERCE watch
  none.

Judgement calls that could carry hindsight:
- the FY27 range taken at its midpoint on the company's adjusted basis, through new guide fields encoded by a builder who knows
  the year (5 classes): the guide rule NKE has used since its first EPS guide in numbers, but the only range in the fact sheet;
- FY26 kept at GAAP with the IEEPA recovery inside it (the Fremont rule; 10 classes as a test), and FY25 with its tax benefit;
- FY24 at the company's $3.95 rather than GAAP (no class, 4 tiers);
- FY18 excluded (8 classes, 21 tiers) and FY20 kept (4 classes, 23 tiers as a test);
- BASE on growth excluding currency (1 class, 10 tiers);
- ECOMMERCE kept on the watch list on the FY2024-FY2026 wording (no class moves);
- the signals, chosen by a builder who knows how 2024-2026 went; DURABLE rather than CYCLICAL (the class label only).

## AVGO (Avago Technologies): the sixth ticker, in staging, from its 2009 listing

The AVGO series is built apart from ACN, UNP, LOW, AAPL and NKE and shares nothing with them but the machinery: its own fact sheet
(`retro/facts/AVGO.json`), builder (`retro/build_avgo.py`) and engine (`retro/templates/avgo_engine.py.tmpl`, the NKE engine with
analog semiconductor signals and the two rules below for a new listing). The method is still r2. No ACN, UNP, LOW, AAPL or NKE fact,
parameter, outcome or finding enters an AVGO model, and neither do the repository's live `avgo_signal_model.py`,
`avgo_proxy_model.py` and `avgo_tracker.py` (2026 analyses). Outputs go to `staging/retrospective/AVGO/`, beside the others, with the
same `index.json` and their own `SERIES.md`.

```bash
python3 retro/build_avgo.py --weekly 2009-08-03 2009-12-31                  # 22 dates, 2009-08-07 .. 2009-12-31
for d in staging/retrospective/AVGO/2009-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series AVGO
python3 retro/tools/firewall.py 2009-10-01 AVGO
```

**Why it starts in August 2009.** The owner asked for 2008, as for the other tickers. AVGO did not trade in 2008: Avago
Technologies was owned by its sponsors (KKR and Silver Lake) from its purchase of Agilent's Semiconductor Products Group on
2005-12-01 until its IPO, and filed with the SEC only as the issuer of notes (Avago Technologies Finance Pte. Ltd., a foreign
private issuer: 20-F and 6-K). It first filed to register its shares on 2008-08-21 (S-1), and the shares first traded on the
Nasdaq Global Select Market on 2009-08-06, the first day of Yahoo's AVGO series. Method r2 needs a closing price and the stock's own
P/E on every date, so no 2008 date can be built. Broadcom Corporation (BRCM), which traded in 2008, is another company; choosing it
because Avago took its name in 2016 would itself use hindsight, and Yahoo no longer serves its prices. On 2026-11-01 the owner chose
to start at the listing, with rules for a short history fixed before any outcome was computed.

Every 8-K of Avago Technologies Limited to the end of 2009 was read in full, and its prospectus, 10-Q and 10-K for the history,
the prints and forward-looking statements; for the time before the listing, the finance subsidiary's results 6-Ks from Q3 FY08 to
Q2 FY09, its other 2009 6-Ks, its FY2007 and FY2008 20-Fs (with the 20-F/As) and its January 2007 exchange-offer prospectus. All
were read directly, with no delegated transcription. 121 strings were checked with `verbatim.py` against their own filings, and each source's date comes from
EDGAR's acceptance time. Decided on 2026-11-01, before any AVGO model was built or any AVGO outcome computed:

- **Fiscal calendar.** Avago's fiscal year ended on October 31 to FY2007 and "commencing with the 2008 fiscal year, is the Sunday that
  is the closest to October 31" (prospectus): FY2008 ended 2008-11-02, FY2009 2009-11-01. The builder maps each day by that rule and
  checks it against the year-ends the vintages state.
- **Prices on the as-of share basis** (the UNP rule). Yahoo's series is adjusted for the 2024 10-for-1 split, so 2009 prices are
  Yahoo's times 10: $16.43 on 2009-08-07 (the IPO priced at $15.00). No split restates a 2009 fact.
- **Every release came after the close.** The Q3 FY09 release (8-K accepted 2009-09-03 16:12 ET) and the Q4 FY09 release (2009-12-03
  16:07 ET) are dated the next trading day, a Friday each time, the week's last trading day: 2009-09-04 and 2009-12-04 carry the print,
  public before the open (the AAPL 2011 and NKE Good Friday rule). The guidance update 8-K (2009-10-14 17:30 ET) is dated 2009-10-15.
  The Q2 FY09 release came from the finance subsidiary (6-K, 2009-06-04 16:06 ET, dated 2009-06-05); the prospectus was accepted on
  2009-08-06 at 06:42 ET, before the open of the first trading day.
- **History: two vintages.** The prospectus (2009-08-06) gives FY2004-FY2008, FY2004-FY2005 being the Predecessor (Agilent's
  Semiconductor Products Group, a segment with no per-share figures), and the FY2009 10-K (accepted 2009-12-15 17:28 ET, dated
  2009-12-16) gives FY2005-FY2009. Each year comes from the latest filing that reports it. The Q4 FY09 print extends the prospectus
  history with FY2009 from 2009-12-04 to the 10-K.
- **EPS** is diluted EPS from continuing operations (the UNP and LOW rule): FY08 $0.26 (net $0.38 with the discontinued operations'
  earn-outs).
  - **Three loss years are excluded** (the ACN FY02 and AAPL FY2001 rule: a loss with no published adjusted figure). FY2006 lost
    $(1.07) per diluted share (eleven months after the acquisition), FY2007 $(1.03) (the $158M asset impairment and $51M of
    restructuring) and FY2009 $(0.20) (the $54M advisory agreement termination fee paid to the sponsors on the IPO). The first two
    are the first years, so the history starts with FY2008. FY2009 is the latest year: it leaves the EPS history, its revenue and
    shares stay, and its own days leave the P/E window (the NKE FY2018 rule). The history is FY2008 alone all year.
  - **The company's non-GAAP EPS stays out.** From the Q3 FY09 release Avago publishes non-GAAP EPS (FY2008 $0.81 and FY2009
    $0.66, first in the Q4 FY09 release). It removes amortization of acquisition-related intangibles and share-based compensation,
    which recur, as well as restructuring and the sponsor fee, so it is not a figure excluding a one-off (the NKE FY2007 and AAPL
    rule), and GAAP stands. No figure excluding only the sponsor fee was published.
  - **FY2008 is kept.** Its listed items, $12M of restructuring and a $10M loss on extinguishing debt, are under its $57M income
    from continuing operations (the AAPL FY2003 test).
- **The listing rule** (method r2, "A listing inside the window"): the P/E window runs from 2009-08-06, from 2 trading days on the
  first date to 80 on 2009-11-27; from the Q4 FY09 print FY2009's own days leave it, so it restarts on 2009-11-02 (24 to 42 trading
  days, labelled "ex-FY09").
- **The bounds rule** (method r2, "A history too short to measure a rule"): with FY2008 alone there is no EPS change, CAGR or
  two-year run, so BEAR is flat EPS (the 0% cap), BULL and XBULL take BASE's rate, the net buyback is 0 (FY2008 and FY2009 both had
  219M diluted shares), and the growth factor is 0 until FY2009's revenue makes a revenue change (from 2009-12-04).
- **Current-FY EPS:** no release, 10-Q or 10-K of the period gives a fiscal-year EPS guide, so FY08's $0.26 stands all year (the
  rollover rule; with FY2009 excluded, FY2008 is the last full year in the history).
- **Avago guides one quarter at a time, in revenue only.** Each release from the Q3 FY09 release guides the next quarter's revenue
  as growth on the quarter just reported. Method r2's input is the next-quarter revenue guide as growth on the same quarter a year
  earlier, so the guide is read as a dollar level on the reported quarter and then against the year-ago quarter from its own release
  (the AAPL dollar-level rule), rounded to 0.1:
  - Q4 FY09: "Projected revenue growth of 7 percent to 10 percent above the third quarter" on Q3's $363M, i.e. $388.4M-$399.3M
    against Q4 FY08's $447M (its own 6-K): -13.1% to -10.7%;
  - the 8-K of 2009-10-14, "now expects fourth fiscal quarter revenue to be up 15% from the third quarter": $417.4M, -6.6%;
  - Q1 FY10: "Flat to Down 3%" on Q4's $428M against Q1 FY09's $368M (its own 6-K): +12.8% to +16.3%.
  - Before the first guide (2009-08-07 to 2009-08-28) no revenue guide is in scope (the finance subsidiary's releases gave no
    outlook), so BASE takes the latest quarter's revenue growth, Q2 FY09's -20.9% (the UNP rule).
  - The outlook tables' other lines (GAAP gross margin, operating expenses, interest, taxes, diluted share count) are display only
    (the UNP 2008 rule for a quarter's figures; the AAPL rule for gross margin).
- **No fiscal-year margin guide**, so no margin step; the margin signal takes the latest quarter's operating-margin change.
- **No dividend:** "We currently do not plan to declare dividends on our ordinary shares in the foreseeable future" (prospectus).
- **Signals.** Six, with ACN's weights: net revenue growth (0.20, the release's headline), GAAP gross margin change (0.20), growth of
  R&D and SG&A less net revenue growth (0.15, lower is better: the "highly variable, low-cost operating model" the prospectus
  describes), inventory growth less net revenue growth (0.15, lower is better: the distributor and inventory cycle of 2008-2009), the
  operating-margin change (0.15; the guided step, else the latest quarter) and the theme slot at 2/4. Values are the latest release's,
  derived from its income statement and balance sheets, which carry the year-ago quarter; the fact sheet keeps the raw figures and the
  builder re-derives each value.
- **Thresholds by rule T over the years the filings report** (method r2, the bounds rule): FY2005-FY2008 for four signals and
  FY2006-FY2008 for the inventory gap, not ten years. Each change comes from the latest filing published by 2009-08-07 that reports
  both years: the prospectus for the statement of operations (FY2004-FY2005 the Predecessor; FY2006 the company's published combined
  year, one Predecessor month and eleven Company months, $1,513M), and for year-end inventories the prospectus (FY2008), the FY2007 20-F
  (FY2007) and the exchange-offer prospectus of 2007-01-09 (FY2006, with revenue on that filing's basis). GAAP as reported: no filing
  publishes gross or operating margin excluding only the FY2007 impairment, and FY2004-FY2005 keep the Camera Module Business sold in
  2005. The values are in the fact sheet (`rule_t`); the builder recomputes the thresholds from them and refuses to build if the
  engine's differ.

  | Signal | Annual values | BEAR / BASE / BULL / XBULL |
  |---|---|---|
  | net revenue growth | FY05-FY08: -17.7, 7.3, 0.9, 11.3 % | -39 / -18 / 4 / 11 % |
  | gross margin change | 353.3, -412.5, -557.3, 1484.5 bp | -1080 / -560 / -30 / 1480 bp |
  | opex growth less revenue | 16.4, -0.4, -17.8, 4.6 pp | 31 / 16 / 2 / -18 pp |
  | inventory less revenue | FY06-FY08: -7.9, -18.1, 23.0 pp | 54 / 23 / -8 / -18 pp |
  | operating margin change | -288.7, -822.9, 85.7, 1629.4 bp | -1540 / -820 / -100 / 1630 bp |

- **Durability.** DURABLE, risk 2, as for the other five. The "why" is the prospectus's own words (the FY2009 10-K's from 2009-12-16):
  "a leading designer, developer and global supplier of a broad range of analog semiconductor devices with a focus on III-V based
  products", about 6,500 products (7,000) "in four primary target markets", "a primarily outsourced manufacturing business model",
  "The global semiconductor market is highly competitive", and "We operate in the highly cyclical semiconductor industry, which is
  subject to significant downturns". No disruption theme in `taxonomy_eras.json` is live for an analog semiconductor maker in 2009
  (CLOUD from 2012-10-30, scoped to on-premise IT; OFFSHORE to IT services; GENAI from 2022-11-30), so the watch list is empty and the
  builder refuses events until a theme encoding is decided.
- **Segment bridge and EPS check** (display only): the vintage's four target markets (FY2008, then FY2009) with each one's growth;
  the EPS check runs on the pre-tax margin, which carries the interest on the notes (material for this company: $86M in FY2008).
- **Volatility and beta** come from the daily returns since the listing; with fewer than two (2009-08-07) they read n/a.
- **Adds nothing:** the 8-Ks of 2009-08-14 (the IPO's closing: 21,500,000 new shares at $15.00, the articles), 2009-09-18, 2009-10-02
  and 2009-10-28 (the debt tender offer and the redemption of the remaining senior and floating rate notes), 2009-09-24 and 2009-12-07
  (an officer, the board, bonuses, the code of ethics); the finance subsidiary's 6-Ks on officers and directors (2009-01-07, 2009-01-21,
  2009-04-10) and workforce reductions (2009-01-09, 2009-05-15); the 10-Q and 10-K beyond their financial statements (restructuring
  cost estimates only); the 20-F/As of 2008-02-27 and 2009-06-16 (directors, shareholders and exhibits). None changes a guided
  number.
- **Anachronism list:** "Broadcom Limited" (2015-05-28, the name announced for the company combined with Broadcom Corporation) and
  "Broadcom Inc." (2017-11-09) join `taxonomy_eras.json`. No existing model of any ticker contains them, so no output changes.

Controls: altering one value of each print, guide and vintage, the Q4 print's FY2009 revenue and the listing changes no date before
its publication and changes the first weekly date on or after it (10 of 10). Rebuilding the 2008 dates of ACN and the 2008-2009
dates of UNP, LOW, AAPL and NKE changes nothing.

Seen in the build (method behaviour, not tuned):
- **RICH on all 22 dates; tier AVOID on 15, BUY on 6, ACCUMULATE on 1.** Robustness agrees on every date except four in December
  (six or seven of eight variants RICH).
- **The multiple is measured against itself.** On FY08's $0.26 the stock traded at 57.7-71.0x. With one EPS anchor for every day of a
  window shorter than a fiscal year, every P/E in it scales together: the scenario prices, the EPP gap and the class do not depend on
  the EPS level (the company's non-GAAP $0.81 would change no class on the December dates). What moves them is the window's own range
  and the growth inputs.
- **To 2009-11-27 BASE growth is negative** (-20.9%, -11.9%, -6.6%/yr) and the bounds rule sets BULL and XBULL to it while BEAR stays
  flat, so the BEAR price sits above the BULL price (as LOW's did in 2008). Ratio B is infinite (no upside even in the bull case) on
  15 dates, and the class is RICH.
- **A flat expected-price curve.** With every scenario price below the hurdle price, the market composite is the one with the highest
  expected price, and BEAR and XBULL are within a few cents: it reads 1.24 to 2009-10-23 and 3.68-3.93 after, so the adjusted gap turns
  from +1.18 to +1.36 into -1.17 to -1.33 on a price move from $16.05 to $15.00. Ratio B is negative (-2.00) on 2009-10-30, when the
  price fell below the BEAR price, and 0.00 on 2009-11-06: BUY on both, RICH on both.
- **From the Q4 FY09 print the guide turns positive:** the Q1 FY10 range is +12.8% to +16.3% on the year-ago quarter, so BASE, BULL
  and XBULL are +14.6%/yr and Ratio B falls to 0.24-0.84 (BUY, then ACCUMULATE on 2009-12-31). The 15% hurdle still asks for more than
  BASE's rate at the window's multiples, so the adjusted gap is -1.21 to -1.48 and the class stays RICH.
- **The proxy composite** is 1.45 on the Q2 FY09 print (revenue -20.9%, gross margin -853bp and operating margin -1,336bp all at
  BEAR) and 2.35 from the Q3 FY09 print (gross margin and the opex gap at BULL). The Q4 FY09 operating-margin change, -845bp, scores
  BEAR because the $54M sponsor fee sits in operating expenses; the inventory gap moves to BULL.
- **The EPP floor** follows the lowest P/E since the listing (62x, then 60x, 57x and 55x) and the price stays 1-28% above it.

How far each call moves the classes (the 22 dates rebuilt with one encoding changed; no outcome consulted):
- FY08 at net EPS $0.38 instead of $0.26 from continuing operations would change 1 class (2009-10-30, RICH to CHEAP) and 1 tier
  (2009-11-06, BUY to AVOID), through rounding at the two knife-edge dates;
- the company's non-GAAP FY08 EPS of $0.81 (on the 5 dates after its first publication) would change nothing;
- BASE on the latest quarter's revenue growth instead of the sequential guide read against the year-ago quarter would change no
  class and 7 tiers (BUY or ACCUMULATE to AVOID from 2009-10-30);
- BEAR bounded by BASE where no EPS change is measurable would change no class and 2 tiers (2009-10-30 and 2009-11-06, BUY to AVOID).

Judgement calls that could carry hindsight:
- starting at the listing, and the listing and bounds rules themselves (mechanical, but decided by a builder who knows what AVGO
  became; no class moves under the alternatives tried above);
- the signals, chosen by a builder who knows the 2009 recovery: the opex and inventory gaps (rule T then sets the thresholds
  mechanically, from four and three annual values);
- reading the sequential guide against the year-ago quarter (7 tiers, no class);
- GAAP over the company's non-GAAP EPS, and excluding the three loss years (no class moves on the dates where both were public);
- DURABLE rather than CYCLICAL, although the company calls its industry "highly cyclical" (the class label only).

### AVGO 2010-2012: FY2008 across the FY2009 gap, guides off the trough, the first dividends

```bash
python3 retro/build_avgo.py --weekly 2010-01-04 2012-12-31                  # 157 dates, 2010-01-08 .. 2012-12-31
```

Every 8-K of 2010-2012 was read in full: the earnings releases, two mid-quarter guide updates, the dividend and buyback
announcements, the sponsors' secondary offerings (with the "recent developments" of their prospectus supplements), the
redemption of the last notes, the credit agreements, officers, board and votes. The 10-Qs and the FY2010-FY2012 10-Ks were read
for the history, the dividend declarations and forward-looking statements, with the 10-K/A of 2010-01-15 and the proxies. 307 more
strings were checked with `verbatim.py` (428 in all), each source dated by EDGAR's acceptance time. Thresholds and signals are
unchanged. Decided on 2026-11-01, before any 2010-2012 date was built or scored:

- **Three vintages:** the FY2010 10-K (accepted 2010-12-15 17:01 ET, dated 2010-12-16), the FY2011 10-K (2011-12-15 18:03 ET,
  dated 2011-12-16) and the FY2012 10-K (2012-12-17 16:31 ET, dated 2012-12-18). Each Q4 print extends the history with its year
  until the 10-K. The 10-K/A of 2010-01-15 adds Part III and Item 9B only.
- **FY2008 stays in the history across the FY2009 gap.** FY2009 stays excluded. Once FY2010 is in, FY2009 is a year inside the
  history: its own days leave the P/E window, and EPS growth is measured only between years in the history (the NKE FY2018 rule,
  which kept NIKE's earlier years when FY2019 followed its excluded FY2018). The history is FY2008 and FY2010 from the Q4 FY10 print,
  then FY2011 and FY2012. BEAR stays flat (the one-year changes, FY10 to FY11 +29.6% and FY11 to FY12 +2.7%, are positive). BULL
  runs from FY2008's $0.26: +155.0%/yr to FY2010's $1.69, +103.5%/yr to FY2011's $2.19, +71.5%/yr to FY2012's $2.25.
- **An engine revision, text only for earlier dates.** XBULL takes every two-year run "whose ends are both in" the history (the r2
  wording of the NKE FY2018 rule). The engine copied from NKE looked only at runs ending in the history's third year or later,
  which skips FY2008 to FY2010 across the gap. XBULL is +155.0%/yr from the Q4 FY11 print. The 22 reports of 2009 rebuild
  byte-identical; their models change only in that line.
- **EPS: GAAP.** FY2010's $1.69 includes the fourth quarter's $28.7M discrete tax benefit from the notes redemption; the release
  gives its per-share effect ($0.11) but no EPS excluding it, so GAAP stands (the NKE FY2008 rule). FY2011 $2.19, FY2012 $2.25.
- **Guides.** Each release guides the next quarter's revenue as sequential growth, read against the same quarter a year earlier
  (the 2009 rule): Q2 FY10 up 6% to 9% (+48.7% to +52.9%), Q3 FY10 up 4% to 7% (+47.5% to +51.8%), Q4 FY10 up 3% to 6% (+32.4% to
  +36.2%), Q1 FY11 down 3% to 6% (+17.9% to +21.7%), Q2 FY11 down 1% to up 2% (+5.7% to +8.9%), Q3 FY11 up 5% to 8% (+6.9% to
  +10.0%), Q4 FY11 up 2% to 5% (+7.5% to +10.7%), Q1 FY12 down 10% to 14% (-2.6% to +1.9%), Q2 FY12 up 1% to 4% (+1.5% to +4.6%),
  Q3 FY12 up 3% to 6% (-1.4% to +1.4%), Q4 FY12 up 0% to 3% (-2.7% to +0.2%), Q1 FY13 down 5% to 9% (-0.1% to +4.3%).
  - **Two 8-Ks update a quarter's guide**, and the latest guide for a quarter wins. The 8-K of 2010-04-19 (dated 2010-04-20) has
    Q2 FY10 "up 11% to 13% sequentially" (+55.7% to +58.5%). The 8-K of 2010-08-10 (dated 2010-08-11) has Q3 FY10 "approximately
    $550 million", on preliminary results for the quarter just ended.
  - **A guide stated as a dollar level** is read against the year-ago quarter directly (the AAPL rule): +51.5% on Q3 FY09's $363M.
- **Year-ago inventory.** From FY2010 the releases' balance sheets carry only the quarter end and the last fiscal year end, so a
  print's year-ago inventory comes from that quarter's own release (an extra source of the print).
- **Dividends,** the latest declared rate from the first filing that states it:
  - $0.07 a quarter, the first, with the Q4 FY10 results (2010-12-03);
  - $0.08 (Q1 FY11 10-Q, accepted before the open on 2011-03-10), $0.09 (2011-06-10), $0.11 (2011-09-09);
  - $0.12 (8-K of 2011-12-09, accepted in market hours), $0.13 (2012-03-09), $0.15 (2012-06-11), $0.16 (2012-08-31);
  - $0.17 (the secondary-offering prospectus supplement of 2012-12-07, accepted the evening before).
- **Release timing.** Every release came after the close, and each print is dated by its 8-K's acceptance. The Q3 FY11 release
  went out after the close on 2011-08-23 and its 8-K was accepted at 06:12 ET the next morning: dated 2011-08-24, with the week's
  date 2011-08-25. Four prints fall on a Friday, the week's last trading day (2010-12-03, 2011-12-02, 2012-08-17, 2012-11-30), and
  meet that day's close, public before the open.
- **Adds nothing:**
  - the sponsors' secondary offerings and their prospectus supplements (the "recent developments" repeat released results) and
    the offering withdrawn on 2010-08-11;
  - the analyst day (8-K of 2010-09-16; the presentations were not filed);
  - the redemption of the remaining notes (8-K of 2010-10-25) and the credit agreements (2010-07-02, 2011-04-01, 2012-08-10);
  - the buyback programs (2011-06-09, 2012-04-05; diluted share counts carry their effect);
  - officers, board, bonuses, AGM votes, 10b5-1 plans and the proxies.
- **Durability unchanged:** DURABLE, risk 2, in each 10-K's words (the FY2012 10-K: "We serve three primary target markets"). The
  FY2012 10-K comes after CLOUD's live_from (2012-10-30), but it names cloud only for Avago's own "cloud-based" IT service
  providers (a security risk), not as a substitute for its products. The watch list stays empty (the AAPL rule).

Controls: altering one value of each print, Q4 full-year figure, guide, vintage and dividend changes no date before its publication
and changes the first weekly date on or after it (41 of 41). No fact appears in a model dated before its publication, and no later
year appears in any model's text. The 2008 dates of ACN and the 2008-2009 dates of UNP, LOW, AAPL and NKE rebuild unchanged.

Seen in the build (method behaviour, not tuned):
- **Classes:** CHEAP on 61 dates, FAIR on 74, RICH on 22. The tier is BUY on 155 (WATCHLIST on 2010-01-08, ACCUMULATE on
  2010-11-26). All eight robustness variants agree on 126 dates, three to seven on 31.
- **2010, on FY08's $0.26 (47 dates to the Q4 FY10 print).** The stock traded at 66-104x. With FY2008 alone in the history, the
  bounds rule sets BULL to BASE, the guide's growth on the year-ago quarter:
  - +14.6%/yr in January and February, so the 15% hurdle asks for more than BASE at the window's multiples: RICH on 6 of the 7
    dates to 2010-02-19 (adjusted gap -0.50 to -1.35; CHEAP on 2010-02-05 at -0.39), Ratio B 1.38 (WATCHLIST) on 2010-01-08;
  - +49.6% to +57.1%/yr from the Q1 FY10 print to August, and +34.3%/yr on the Q4 FY10 guide. The comparisons are 2009's trough
    quarters (the UNP 2009 extrapolation, in reverse).
  - CHEAP on 41 dates (Ratio B 0.13 to 0.83, the EPP floor at 60-64x).
- **From the Q4 FY10 print** the anchor is FY10's $1.69 (15.6-22.9x). The window's P/Es are recomputed on it (FY2010's days now on
  its actual EPS), and the stock stays at the 59th-100th percentile of its own range.
  - BULL at +155%/yr puts Ratio B at 0.06-0.15 (BUY).
  - The EPP floor at 9x (the calendar-year lows of 2009-2011) puts the price 74-154% above it: FAIR on 49 of the 52 dates,
    CHEAP on 2010-12-03 and 2010-12-10, RICH on 2011-07-01 (the conservative case at -40%).
- **From the Q4 FY11 print** the anchor is FY11's $2.19 (12.9-17.8x). The guides turn flat, and the net buyback is negative
  (diluted shares 219M in FY08, 252M in FY11: -4.6%/yr), so BASE is -5.8% to -1.5%/yr. When the multiple sits above its median, the
  conservative case loses 16-24%: RICH on 15 dates (2012-02-24 to 2012-04-13, 2012-06-29, 2012-07-20 to 2012-08-24), CHEAP on 13,
  FAIR on 24.
- **From the Q4 FY12 print** the anchor is FY12's $2.25 (13.8-15.6x), with BULL at +71.5%/yr: CHEAP on 5 of 6 dates.
- **The proxy composite** is 3.2-3.7 on the FY10 prints, 2.55-2.9 on FY11's and 2.0-2.3 on FY12's.

How far each call moves the classes (the 157 dates rebuilt with one encoding changed; no outcome consulted):
- restarting the history after FY2009 from the FY2010 10-K (FY2008 out) would change 57 classes and 57 tiers: FAIR to RICH and
  BUY to AVOID on most dates from 2010-12-17 to 2011-11-25, and some in 2012;
- FY2010 at $1.58 (GAAP less the published $0.11 per-share tax benefit, a derived figure, as a test) would change 14 classes and
  no tier;
- BASE on the latest quarter's revenue growth instead of the guides would change 10 classes and 2 tiers;
- the engine revision (XBULL across the gap) and leaving out the dollar-level guide of 2010-08-11 would change none.

Judgement calls that could carry hindsight:
- keeping FY2008 across the FY2009 gap (the NKE precedent; 57 classes): BULL then starts from an LBO-era $0.26;
- FY2010 at GAAP with the discrete tax benefit (14 classes);
- reading each sequential guide against the year-ago quarter (10 classes against the latest quarter's growth);
- the signals, unchanged from 2009, chosen by a builder who knows these years; DURABLE rather than CYCLICAL (the class label only).

### AVGO 2013-2016: LSI and Broadcom, two more excluded years, the first theme

```bash
python3 retro/build_avgo.py --weekly 2013-01-07 2016-12-31                  # 208 dates, 2013-01-11 .. 2016-12-30
```

Every 8-K and 8-K/A of 2013-2016 was checked for a guided number: Avago's, and from 2016-02-02 those of Broadcom Limited, its
successor issuer (CIK 1649338, with the 8-K12B and 8-K12B/A). The items of each 8-K were skimmed and the headline of every exhibit
99 listed; the earnings releases and the two guidance updates were read in full, and the deal releases, presentations and call
scripts (CyOptics, LSI, PLX, Emulex, Broadcom Corporation, Brocade) were searched for outlooks: they state accretion only. The 10-Qs
were searched for dividend declarations and revenue expectations, the joint proxy statement/prospectus for projections, and the
FY2013-FY2016 10-Ks read for the history, the business wording and the risk factors. A first pass over the 8-K bodies missed one
guidance update (2016-11-02); a sweep of every exhibit's headline found it before any 2013-2016 outcome was computed. 430 more
strings were checked with `verbatim.py` (858 in all), each source dated by EDGAR's acceptance time. Thresholds and signals are
unchanged. Decided on 2026-11-01, before any 2013-2016 date was built or scored:

- **Four vintages:** the FY2013 10-K (accepted 2013-12-20 16:56 ET, dated 2013-12-23), FY2014 (2014-12-29 17:23 ET, dated
  2014-12-30), FY2015 (2015-12-17 16:25 ET, dated 2015-12-18) and Broadcom Limited's FY2016 10-K (2016-12-23 08:20 ET, before the
  open). Each year comes from the latest 10-K that reports it (FY2008 still from the FY2012 10-K).
- **EPS: GAAP diluted EPS from continuing operations,** as since 2009: FY13 $2.19, FY14 $1.16 (net $0.99; LSI's Flash and Axxia
  businesses are discontinued operations), FY15 $4.95 (net $4.85), FY16 $(4.57) (net $(4.86)).
- **FY2014 excluded, a distorted year (the AAPL FY2002 test).** The items the 10-K lists for the year ($210M of inventory step-up
  charges, $162M of restructuring and $74M of acquisition-related costs, for LSI, PLX and CyOptics: $446M) exceed its $309M income
  from continuing operations. No EPS excluding only them was published (the non-GAAP $4.90 also removes amortization and share-based
  compensation, which recur: the 2009 rule). Both facts are in the Q4 FY14 release, so the exclusion starts with that print
  (2014-12-04). The NKE FY2018 rule then applies: FY2014's own days leave the P/E window ("ex-FY14"), growth is measured only
  between years in the history, and FY13's $2.19 stands for FY15E until the Q4 FY15 print. FY2013 ($26M of such items against $552M)
  and FY2015 ($248M against $1,391M) are kept (the AAPL FY2003 test).
- **FY2016 excluded, a loss** (the FY2009 rule): $(4.57) per diluted share from continuing operations in the year Broadcom
  Corporation was acquired. From the Q4 FY16 print (2016-12-09) its days leave the window and FY15's $4.95 stands for FY17E. The
  display-only EPS check then runs on FY16's pre-tax loss margin (-8.4%) and reads a loss, as NKE's did after FY18.
- **The anchors:** FY12's $2.25 to the Q4 FY13 print (2013-12-05), FY13's $2.19 for FY14E and then FY15E, FY15's $4.95 from the Q4
  FY15 print (2015-12-03) for FY16E and then FY17E.
- **Guides,** the GAAP column, read against the same quarter a year earlier from its own release (the 2009 rule):
  - sequential: Q2 FY13 down 2% to 5% (-5.2% to -2.2%), Q3 FY13 up 6% to 9% (-1.7% to +1.1%), Q4 FY13 up 12% to 15% (+16.7% to
    +19.8%), Q1 FY14 down 3% to 6% (+20.4% to +24.3%), Q2 FY14 down 3% to 6% (+18.6% to +22.4%), Q4 FY14 up 18% to 22% (+102.9%
    to +109.8%), Q1 FY15 flat to up 4% (+124.3% to +133.2%), Q2 FY15 down 4% to flat (+123.9% to +133.2%);
  - dollar levels, read directly (the AAPL rule), as ranges: Q3 FY14 $1.3B-$1.4B (+101.9% to +117.4%), Q3 FY15 $1,729M plus/minus
    $25M (+34.3% to +38.2%), Q4 FY15 $1,838M (+14.0% to +17.2%), Q1 FY16 $1,768M (+6.6% to +9.7%), Q2 FY16 $3,533M plus/minus $75M
    (+114.3% to +123.5%), Q3 FY16 $3,740M (+111.2% to +119.9%), Q4 FY16 $4,090M (+118.2% to +126.4%), Q1 FY17 $4,065M (+125.3% to
    +133.8%).
  - **The 8-K of 2016-11-02** (before the open, filed with the Brocade merger agreement) tightens the Q4 FY16 GAAP guide to
    $4,090M-$4,165M "based on current business trends and conditions" and affirms the rest: the latest guide for a quarter wins
    (the 2010 rule), +122.3% to +126.4% from 2016-11-04 to the Q4 FY16 print.
  - **The acquisitions enter only through the guides and prints, as published** (the LOW 2025 rule): LSI from the Q3 FY14 guide,
    PLX from Q4 FY14, Emulex from Q3 FY15, Broadcom Corporation from Q2 FY16. No deal filing changes a guided number:
    "immediately accretive to non-GAAP EPS" is not a current-year figure (the UNP merger rule), and the joint proxy statement's
    management projections were "not prepared with a view toward public disclosure".
  - **The CyOptics 8-K of 2013-07-15** (before the open) affirms the Q3 FY13 guide and adds a non-GAAP outlook for CyOptics alone
    from June 29 ($18M plus/minus 10%), "in addition to" the standalone guide. It is not a guide for the quarter's net revenue and
    no total is derived from two published figures (the NKE 2008 rule): the affirmed guide stands, as a record with the same
    numbers, and the CyOptics outlook is display only.
  - **Q2 FY15:** the 8-K accepted 2015-05-28 at 07:24 ET (before the open, with the Broadcom announcement) carried the release
    without its financial statements; the 8-K/A accepted at 19:20 ET carried the full release, with the GAAP gross margin guide
    corrected from 52.75% to 49.5%. The print and the Q3 FY15 guide are dated by the 8-K/A (2015-05-29, the week's date either way).
- **Dividends,** the latest declared rate from the first filing that states it: $0.19 (Q1 FY13 10-Q, 2013-03-15), $0.21
  (2013-06-10), $0.23 (an 8-K before the open, 2013-09-05), $0.25 (2013-12-13), $0.27 (2014-03-06), $0.29 (Q2 FY14 10-Q,
  2014-06-11), $0.32 (2014-09-04), $0.35 (2014-12-11), $0.38 (2015-03-05), $0.40 (2015-06-05), $0.42 (2015-09-04), $0.44
  (2015-12-09), then with each release of 2016: $0.49, $0.50, $0.51 and $1.02 (2016-12-09).
- **Broadcom Limited from 2016-02-02** (`company_names`, the 8-K12B accepted 08:26 ET, before the open): Pavonia Limited, renamed,
  is the successor issuer, and the AVGO ticker continues. Diluted shares are taken as reported: FY2016's 383M includes 17M
  restricted exchangeable partnership units (if-converted), so the net buyback over FY2008-FY2016 is -6.8%/yr.
- **The first theme: CLOUD on the watch list from the FY2016 10-K.** Its risk factors are the first to name cloud as a risk to the
  company's own products: "the shift to cloud-based IT solutions and services, such as hyperscale computing, may adversely affect
  both our wired infrastructure and enterprise storage segments" (the FY2013-FY2015 10-Ks name cloud only for their own IT service
  providers). CLOUD is live from 2012-10-30 and scoped to on-premise hardware and storage, so the ACN rule applies, as for LOW and
  NKE: company-acknowledged, no market read. The factor pair nets to zero and the theme signal stays at 2/4, so only text changes
  (2016-12-23 and 2016-12-30). The builder now accepts this one event kind.
- **Business line, segments and wording** follow each 10-K: three target markets in FY2013, four segments from FY2014 (enterprise
  storage, new with LSI, shows as "new in FY14" in the segment bridge); DURABLE, risk 2 throughout ("highly competitive", "highly
  cyclical"). FY2016's tax rate is FY15's (a pre-tax loss: the FY09 rule).
- **An engine revision, text only for earlier dates.** The segment bridge printed every segment's growth as a number; a segment
  with no prior-year revenue now reads "new in FYxx, no prior-year revenue". The 179 reports and analyses of 2009-2012 rebuild
  byte-identical; their models change only in that line. The builder prints guide and quarter dollars with thousands separators,
  and a guide range without "about"; no earlier output changes.
- **Adds nothing:**
  - the deal filings (CyOptics, LSI, PLX, Emulex, Broadcom Corporation, Brocade), their 425s, DEFA14As, tender-offer filings and
    the joint proxy statement/prospectus;
  - Broadcom Corporation's own Q4 2015 results in the 8-K12B (item 2.02: the acquired company's, not a print of this company), and
    the pro forma statements (8-K/A of 2014-07-08, 8-K12B/A of 2016-03-02);
  - credit agreements and amendments, the convertible notes and their conversion, the restructuring (item 2.05) estimates, and the
    Axxia, Flash, Endace, fiber optics and wireless IoT sales;
  - the investor presentations of 2016-03-10 (it repeats the Q2 FY16 guide and gives a long-term non-GAAP model) and 2016-11-02
    (Brocade; it repeats the tightened Q4 FY16 range);
  - shelves, 13Ds, officers, board, bonuses, AGM and court-meeting votes, the code of ethics and the proxies.

Controls: altering one value of each print, Q4 full-year figure, excluded-year note, guide, vintage, dividend, the event and the
company name changes no date before its publication and changes the first weekly date on or after it (62 of 62). No fact appears
in a model dated before its publication, and no later year appears in any model's text. The 2008 dates of ACN and the 2008-2009
dates of UNP, LOW, AAPL and NKE rebuild unchanged. The firewall (a planted later print, vintage, guides, dividend, event and company
name, and 10x prices after the cutoff) changes no earlier model at 13 cutoffs from 2013-01-07 to 2017-01-01.

Seen in the build (method behaviour, not tuned):
- **Classes:** CHEAP on 20 dates, FAIR on 102, RICH on 86. Tiers: BUY on 109, ACCUMULATE on 34, WATCHLIST on 21, AVOID on 44. All
  eight robustness variants agree on 119 dates, two classes split the other 89.
- **2013, on FY12's $2.25 (47 dates to the Q4 FY13 print).** The stock traded at 13.9-20.5x. The guides read flat to down against
  2012 and the net buyback is -3.3%/yr (219M diluted shares in FY08, 250M in FY12), so BASE is -7.0% to -1.2%/yr until the Q4 FY13
  guide (+15.0%). BULL runs from FY08 at +71.5%/yr. CHEAP on 20 dates, FAIR on 27, BUY throughout (Ratio B 0.08-0.35).
- **From the Q4 FY13 print, on FY13's $2.19.** BEAR takes FY12 to FY13 (-2.7%) and BULL falls to +53.1%/yr. To 2014-05-23 the
  price rose to 20.8-32.2x (97th-100th percentile), 74-168% above the EPP floor (12x): RICH on 20 of 25 dates.
- **The LSI guide** (from 2014-05-30): Q3 FY14 revenue of $1.3-1.4 billion against Q3 FY13's $644M puts BASE at +106.9%/yr (BULL
  takes BASE's rate), then +103.6% on the Q4 FY14 guide with PLX. FAIR on 20 of 27 dates to the Q4 FY14 print, the conservative
  case +46% to +101%.
- **From the Q4 FY14 print, with FY2014 excluded,** FY13's $2.19 anchors FY15E at 45-68x, 278-463% above the floor: RICH on all 52
  dates to 2015-11-27. BASE is +125.5% and +125.3% on the Q1 and Q2 FY15 guides. From 2015-05-29 the Emulex-era guides (+34% to
  +38%, then +14% to +17%) bring BASE down to +33.0% and +12.4%, under BULL's +53.1%, and the price stands above the BULL price:
  Ratio B is infinite and the tier AVOID on 27 dates.
- **From the Q4 FY15 print, on FY15's $4.95** (24-30x): BASE +4.7% on the Q1 FY16 guide; RICH on 7 and FAIR on 6 of 13 dates. The
  floor is 13x from 2016-01-08.
- **From the Q1 FY16 print,** the guides for the combined Avago and BRCM businesses (+111% to +134% on Avago's year-ago quarters) put
  BASE at +112.1% to +122.8%/yr: FAIR and BUY on all 44 dates to 2016-12-30 (118-183% above the floor, the conservative case +87%
  to +144%).
- **The proxy composite** reads 2.05-2.3 in 2013, 2.2-3.05 in 2014, 3.05-3.7 in 2015 and 1.75-3.05 in 2016 (1.75-1.95 on the BRCM
  quarters from June 2016, whose inventory step-up and operating expenses weigh on the margin, opex and inventory signals).

How far each call moves the classes (the 208 dates rebuilt with one encoding changed; no outcome consulted):
- keeping FY2014 at GAAP $1.16 instead of excluding it would change 9 classes and 35 tiers: FY14's $1.16 becomes the FY15E anchor
  and BEAR takes FY13 to FY14 (-47.0%); RICH turns FAIR on 2015-05-08, 2015-05-15 and seven dates from 2015-12-04 to 2016-02-26,
  and the tier moves on most dates from 2014-12-05 to 2016-02-26;
- BASE on the latest quarter's revenue growth instead of the guides would change 46 classes and 52 tiers, mostly to RICH in
  September-November 2013, May-November 2014 and March-May 2016, when the guides ran ahead of the quarter just reported (the Q4
  FY13 ramp, then LSI and BRCM);
- adding the CyOptics outlook to the affirmed Q3 FY13 guide (a derived total, +1.0% to +4.4% YoY instead of -1.7% to +1.1%) and
  leaving out the FY2016 10-K's cloud wording would change none.

Judgement calls that could carry hindsight:
- excluding FY2014 as a distorted year (the AAPL FY2002 test on the listed acquisition items; 9 classes and 35 tiers): the
  anchor then stays on FY13 through FY2015;
- the GAAP basis through the acquisitions (FY14, FY16), where the company's non-GAAP EPS removes the acquisition accounting as well
  as recurring costs;
- reading the acquisition-swollen guides against the year-ago quarter as published (the LOW rule), which puts BASE above +100%/yr
  on most dates from mid-2014 and from March 2016;
- the CyOptics outlook left out of the Q3 FY13 guide (no class or tier moves either way);
- the signals, unchanged since 2009, and DURABLE rather than CYCLICAL (the class label only); CLOUD on the watch list from the
  FY2016 10-K (text only).

### AVGO 2017-2020: tax reform and the redomiciliation, fiscal-year guides with a GAAP margin, a withdrawn guide

```bash
python3 retro/build_avgo.py --weekly 2017-01-02 2020-12-31                  # 209 dates, 2017-01-06 .. 2020-12-31
for c in 2017-01-01 2017-03-01 2017-11-01 2017-12-20 2018-01-30 2018-04-04 2018-12-01 2019-06-01 2019-08-08 2019-12-10 \
         2020-03-10 2020-09-01 2021-01-01; do python3 retro/tools/firewall.py $c AVGO; done
```

Every 8-K of Broadcom Limited (CIK 1649338) to its redomiciliation and of Broadcom Inc. (CIK 1730168, from 2018-04-04) to the end of
2020 was checked for a guided number: the items of each, the headline of every exhibit 99, and a sweep of every non-earnings exhibit
for "affirm", "guidance" and "outlook"; the three guidance-update 8-Ks were read in full, and the sixteen releases' headlines,
statements, outlooks and dividend and repurchase statements. The Qualcomm bid's 425s, DFAN14As and proxy materials, the
redomiciliation S-4 and the deal releases and presentations (Brocade, CA, Symantec's enterprise security business) were searched for
Broadcom's own outlook: they use the guides already published, state accretion, run-rate and long-term models, and, once, reaffirm a
guide (below). The FY2017-FY2020 10-Ks were read for the history, the tax items, the fiscal calendar, the business wording and the
risk factors, and the Q1-Q3 FY18 10-Qs for the tax benefits. 291 more strings were checked with `verbatim.py` (1,149 in all), 299
structured checks read every print's income-statement and balance-sheet figures back from its own release (and each year-ago
inventory from that quarter's release), and each of the 26 new sources' dates comes from EDGAR's acceptance time. Thresholds and
signals are unchanged. Decided on 2026-11-01, before any 2017-2020 date was built or scored:

- **Four vintages:** the FY2017 10-K (accepted 2017-12-21 17:10 ET, dated 2017-12-22), FY2018 (Broadcom Inc.'s, 2018-12-21 17:17 ET,
  dated 2018-12-24), FY2019 (2019-12-20 16:10 ET, dated 2019-12-23) and FY2020 (2020-12-18 17:07 ET, dated 2020-12-21). Each holds
  the ten fiscal years to its latest one (the ACN and NKE rule): FY2008-FY2017, then FY2009-FY2018, where FY2009 is the first year
  and a loss, so the history and the P/E window start with FY2010 (the ACN FY02 rule), then FY2010-FY2019 and FY2011-FY2020. Each
  year comes from the latest 10-K that reports it.
- **EPS: GAAP diluted EPS from continuing operations,** as since 2009, attributable to common stock after the preferred dividends
  from FY2019. FY17 is $4.28 in the Q4 FY17 release and $4.03 in the FY2017 10-K, which records a $110M fourth-quarter litigation
  settlement the release did not include: the print carries $4.28 until the 10-K replaces it (the rollover rule). FY19 $6.46, FY20
  $6.33. FY2017, FY2019 and FY2020 are kept: their listed items are fractions of their income (FY17 $1,790M, FY19 $2,736M, FY20
  $2,961M; the FY19 and FY20 tax benefits, $510M and $518M, included).
- **FY2018 excluded, a year distorted by one-off benefits** (the mirror of the AAPL FY2002 test; see "Retro method r2"). GAAP EPS
  from continuing operations was $28.48 (net $28.44). The Q3 FY18 10-Q (dated 2018-09-14) lists the 2017 Tax Reform Act's
  provisional benefit of $7,303M and the redomiciliation's tax benefits of $1,162M less an $84M provision, and the Q4 FY18 release
  gives the year's $12,629M income from continuing operations: the items exceed the income without them. Both facts are public
  with the Q4 FY18 print (2018-12-07), so the exclusion starts there; the FY2018 10-K's figures ($7,278M, $1,162M less $167M) say
  the same. No EPS excluding only them was published (non-GAAP also removes amortization and stock-based compensation: the 2009
  rule). The NKE FY2018 rule then applies: FY2018's own days leave the P/E window ("ex-FY18"), growth is measured only between
  years in the history, and FY17's $4.03 stands for FY19E until the Q4 FY19 print. Its revenue, shares and margins stay; its
  effective tax rate (-177.9%, a benefit) stays as the fact in the display-only EPS check, as NKE's 55.3% did.
- **The fiscal calendar.** The FY2017 10-K states the year end as "the Sunday closest to October 31 in a 52-week year and the first
  Sunday in November in a 53-week year"; the Q4 FY17 release (2017-12-07) first says fiscal 2018 has the extra week (its first
  quarter "ending February 4, 2018"). So FY2018 ends on 2018-11-04, not on the closest Sunday (2018-10-28). The builder's calendar
  takes 53-week years from the fact sheet (`fiscal_calendar`) and refuses one published after the first day it moves.
- **Guides.**
  - Quarter guides, FY2017-FY2018: the GAAP column, as ranges read against the year-ago quarter from its own release (the 2009
    rule): Q2 FY17 $4,090M plus/minus $75M (+13.4% to +17.6%), Q3 FY17 $4,445M (+15.2% to +19.2%), Q4 FY17 $4,796M (+14.1% to
    +17.8%), Q1 FY18 $5,296M (+26.1% to +29.8%: a 14-week quarter with the Brocade FC SAN business, as published, the 2011
    rule), Q2 FY18 $4,997M (+17.5% to +21.1%), Q3 FY18 $5,047M (+11.4% to +14.8%), Q4 FY18 $5,397M (+9.9% to +13.0%).
  - **Two 8-Ks narrow a quarter on a non-GAAP basis only:** Q1 FY18 to $5,300-5,350M (2018-01-31, before the open) and Q2 FY18 to
    $5,000M plus/minus $25M (2018-04-30, after the close, dated 2018-05-01). The published range is the latest guide for its
    quarter (the LOW Q3 FY18 rule: only the adjusted figure is published, so the guide takes it); the difference is the de minimis
    licensing revenue the release reconciles ($3-4M). Each 8-K also gives a preliminary guide for the quarter after next; the next
    release guides that quarter the day it becomes the next one, so neither preliminary range ever applies.
  - **A guide restated in words:** the 8-K of 2017-11-02 (before the open) expects Q4 FY17 revenue "at the higher end" of the
    outlook: the range stands, as a record with the same numbers and the words (the ACN Q3 FY08 rule, the CyOptics record).
  - **Fiscal-year guides from the Q4 FY18 release** (CA closed on 2018-11-05): Broadcom guided the fiscal year, not the quarter.
    With no next-quarter guide in scope, method r2 takes the fiscal-year revenue guide; it is a dollar level, read against the
    previous year's net revenue in the history (the LOW 2021 rule): FY2019 $24,500M on FY18's 53-week $20,848M (+17.5%, as published),
    cut to $22,500M (+7.9%) on 2019-06-14; FY2020 $25 billion plus or minus $500 million on FY19's $22,597M (+8.4% to +12.8%).
  - **The FY2019 GAAP operating margin guide** is a level (20%, then 17.6%, 14.75% and 14.75%), so it gives the guided margin
    step from FY18's 24.63% (the LOW level-form rule): -463bp, -703bp, -988bp. The non-GAAP margin, interest, taxes and capital
    expenditures are display only, and so is the FY2020 and 2020 quarters' Adjusted EBITDA, a non-GAAP figure (the 2009 rule).
  - **A reaffirmation in numbers:** the Symantec enterprise security release (8-K accepted 2019-08-09 06:10 ET, before the open)
    "reaffirmed its fiscal year 2019 revenue guidance of $22.5 billion": a record with the same numbers (the CyOptics rule);
    the Q2 FY19 release's margin stands.
  - **The withdrawal.** The Q1 FY20 release (2020-03-13) is "withdrawing its prior annual guidance for fiscal year 2020, and
    providing guidance for its second fiscal quarter": the withdrawal voids the FY2020 guide (the LOW 2020 rule), and the
    next-quarter guide, r2's primary input, applies: Q2 FY20 $5.7 billion plus or minus $150 million (+0.6% to +6.0%), Q3 FY20
    $5.75 billion (+1.5% to +7.0%), Q4 FY20 $6.4 billion (+8.2% to +13.4%), Q1 FY21 "approximately $6.6 billion" (+12.7%).
  - The acquisitions enter only through the guides and prints, as published (the LOW 2025 rule): Brocade from Q1 FY18, CA from
    FY2019, the Symantec enterprise security business from FY2020.
- **Dividends,** the latest declared rate from the first filing that states it: $1.75 (2017-12-07), $2.65 (2018-12-07), $3.25
  (2019-12-13), $3.60 (2020-12-11); the $20.00 dividend on the mandatory convertible preferred stock (from 2019-12-13) is not a
  common dividend and shows only in the cash-return text.
- **Broadcom Inc. from 2018-04-05** (`company_names`, the 8-K12B accepted 2018-04-04 16:34 ET, after the close): the redomiciliation
  to Delaware, completed after the close of trading on April 4, the shares exchanged one-for-one; the AVGO ticker continues.
- **Durability unchanged:** DURABLE, risk 2, in each 10-K's words ("highly competitive", "highly cyclical"; the FY2019 and FY2020
  10-Ks: "The markets in which we participate are highly competitive"). CLOUD stays on the watch list in each 10-K's own wording:
  the FY2017 10-K repeats FY2016's sentence ("may adversely affect both our wired infrastructure and enterprise storage
  segments"), the FY2018-FY2020 10-Ks name "the shift to cloud-based IT solutions and services, such as hyperscale computing" as
  affecting sales "for use in traditional enterprise data centers". Company-acknowledged, no market read; text only. No other
  theme is live for the company (EV from 2020 is scoped to powertrains and fuel, CRYPTO from 2020-10-21 to payments and banks).
- **Segments and wording** follow each 10-K: four segments in FY2017 and FY2018, three in FY2019 (semiconductor solutions,
  infrastructure software, IP licensing), two in FY2020. The tax rate is each year's published effective rate, negative from
  FY2018 (benefits); the FY09 rule takes the prior year's rate only for a pre-tax loss. The text constant "An analog
  semiconductor maker" in the engine's volatility section stays (the UNP franchise-text rule).
- **A builder change, no earlier output changes.** The fiscal-year guide (`period`), its margin level (`op_margin_guide_pct`), the
  withdrawal (`withdrawn`), the 53-week calendar and a risk quote without a final period are new encodings; the 387 dates of
  2009-2016 rebuild byte-identical. The firewall now also plants absurd later margins and a later withdrawal of every fiscal year
  guided before its cutoff.
- **Adds nothing:**
  - the Regulation FD reconciliation of 2017-01-09; the 2018-09-07 company overview (it repeats the Q4 FY18 guide); the long-term
    target model in the Q4 FY17 release ("should not be interpreted as guidance") and the CA presentation's long-term models;
  - the Qualcomm bid (2017-11-06 to its withdrawal on 2018-03-14): its 8-Ks, 425s, DFAN14As and proxy materials use the Q4 FY17
    guide already published;
  - the redomiciliation's filings (S-4, scheme, court and vote 8-Ks), the deal filings (Brocade, CA, Symantec's enterprise security
    business: accretion, run-rate revenue and synergy estimates are not current-year figures) and the pro forma statements;
  - the 8-K of 2020-06-26, which recasts the FY2019 10-K for the new segments (no EPS, revenue or share count changes);
  - the Apple supply agreements (2019-06-10, 2020-01-23: multi-year estimates), the European Commission proceedings
    (2019-06-26), the preferred stock offering (2019-09-30), the $12 billion buyback authorization (2018-04-12; diluted share counts
    carry the repurchases), the debt offerings, tender and exchange offers and credit agreements;
  - officers, board, bonuses, votes, the 10b5-1 plan of 2020-01-09 and the proxies.

Controls: altering one value of each print, Q4 full-year figure, excluded-year note, guide, vintage, dividend, event and the company
name changes no date before its publication and changes the first weekly date on or after it (55 of 57). The two exceptions are the
preliminary guides for the quarter after next (2018-01-31 for Q2 FY18, 2018-04-30 for Q3 FY18), which change no date at all: each is
superseded the day its quarter becomes the next one. No new fact appears in a model dated before its earliest publication (82,809
checks over the 596 AVGO models), and no later calendar year appears in any report or analysis. The 2008 dates of ACN and the
2008-2009 dates of UNP, LOW, AAPL and NKE rebuild unchanged. The firewall (a planted later print, vintage, guides with absurd margins,
withdrawals, dividend, event and company name, and 10x prices after the cutoff) changes no earlier model at the 13 cutoffs above.

Seen in the build (method behaviour, not tuned):
- **Classes:** RICH on 203 dates, FAIR on 6 (2017-01-06 to 2017-02-10), no CHEAP. Tiers: AVOID on 177, WATCHLIST on 21, BUY on 9,
  ACCUMULATE on 2. All eight robustness variants agree on 169 dates, seven on 38, five on 2. Ratio B is infinite (the price above
  the BULL price) on 92 dates.
- **January-February 2017, on FY15's $4.95 for FY17E** (FY2016 excluded): 35.7-42.5x, the 98th-100th percentile. The Q1 FY17 guide
  reads +125.3% to +133.8% against Q1 FY16, Avago's last quarter before BRCM, so BASE is +122.8%/yr and BULL takes BASE's rate:
  FAIR on 6 dates and RICH on 2, BUY on all 8 (Ratio B 0.46-0.61).
- **From the Q1 FY17 print** the year-ago quarters include BRCM: the Q2-Q4 FY17 guides put BASE at +8.8% to +10.5%/yr (net
  buyback -6.7%/yr: 219M diluted shares in FY08, 383M in FY16). On FY15's $4.95 the stock traded at 42.7-57.0x (95th-100th
  percentile), 205-308% above the EPP floor (14x): RICH and AVOID on all 40 dates to 2017-12-01.
- **From the Q4 FY17 print** the anchor is FY17's $4.28, then the 10-K's $4.03 (for FY18E): 56.8-67.4x to June 2018. The Q1 FY18
  guides (the 14-week quarter with Brocade) put BASE at +20.9% and +21.7%/yr, the Q2-Q4 FY18 guides at +12.3%, +6.1% and +4.4%.
  After the CA announcement (2018-07-12) the price fell to $202-248 and Ratio B to 1.0-2.5: WATCHLIST on 14 dates, ACCUMULATE on
  2018-10-26. RICH on all 52 dates of 2018 at 50.2-67.4x (the 77th-100th percentile).
- **From the Q4 FY18 print, FY2018 excluded,** FY17's $4.03 stands for FY19E at 56.7-79.1x (the 91st-100th percentile). The FY2019
  margin guides cut BASE to -12.2% and -12.4%/yr (revenue +17.5%, margin -463bp: -23.1% of EPS), -29.2%/yr (-703bp: -39.9%)
  and -65.9%/yr (revenue +7.9%, -988bp: -67.0%): the CA amortization in the GAAP margin, carried as growth for two years (the
  LOW Orchard pattern). BEAR stays at -2.7%/yr (FY12 to FY13), so the BEAR price sits above the BASE price. RICH and AVOID on
  all 53 dates to 2019-12-06, every variant agreeing; the conservative case -62% to -73%.
- **The FY2018 vintage drops FY2008:** BULL falls from +35.6%/yr (FY08's $0.26 to FY17's $4.03) to +13.2%/yr (FY10's $1.69 to
  FY17) and XBULL from +155.0%/yr (FY08 to FY10) to +50.3%/yr (FY13 to FY15, across the excluded FY14).
- **From the Q4 FY19 print,** FY19's $6.46 at 41.7-50.2x (the 72nd-89th percentile) and BASE +4.9%/yr on the FY2020 guide. From the
  withdrawal the Q2-Q4 FY20 guides put BASE at -2.4%, -1.5% and +5.1%/yr. At the COVID-19 low (2020-03-20, $192.22) the stock
  traded at 29.8x (the 66th percentile), 57% above the floor (19x): Ratio B 0.63 (BUY), still RICH (adjusted gap -0.14,
  conservative case -29%). From late November it traded at 61-69x (the 97th-100th percentile), on FY19's $6.46 and from the Q4
  FY20 print on FY20's $6.33. RICH on all 53 dates of 2020.
- **The window's multiples rose** as the FY17 days on $4.03 filled it: the median from 15.5x to 25.6x, the 90th percentile from
  25.7x to 57.5x. The EPP floor was 14x in 2017, 15x in 2018, 17x in 2019, 19x in 2020 and 22x on 2020-12-31.
- **The proxy composite:** 1.95 on the Q1 FY17 print (operating margin -1,460bp and the opex and inventory gaps at BEAR against
  Avago's Q1 FY16), 3.55 and 3.35 on Q2-Q3 FY17, 2.85 on Q4 FY17, 3.20 on Q1-Q2 FY18, 3.05 on Q3 FY18, 2.90 on Q4 FY18, 2.55 on Q1
  FY19, 2.40 on Q2-Q4 FY19 (the opex gap and the guided margin step at BEAR), 2.35 on Q1-Q2 FY20, 2.70 on Q3 FY20 and 2.90 on Q4
  FY20.

How far each call moves the classes (the 209 dates rebuilt with one encoding changed; no outcome consulted):
- FY2018 at GAAP $28.48 (the literal AAPL FY2002 test, which a benefit cannot meet) would change 53 classes and 62 tiers: every date
  from 2018-12-07 to 2019-12-06 turns CHEAP and BUY (FY19E at 8.0-11.1x, the 3rd-28th percentile, below the 12x floor), and from the
  Q4 FY19 print BEAR becomes FY18 to FY19's -77.3%/yr, which moves nine tiers of March-May 2020 toward AVOID;
- BASE on the latest quarter's revenue growth instead of the guides would change no class and 13 tiers (2017-03-03 to 2017-05-26,
  AVOID to BUY on Q1 FY17's +133.7%);
- the FY2019 margin guides as display only, the two non-GAAP quarter updates left out, and FY2018 ending on 2018-10-28 would change
  none.

Judgement calls that could carry hindsight:
- excluding FY2018 by the mirrored test (53 classes and 62 tiers): FY17's $4.03 then anchors FY19E at 57-79x where GAAP $28.48
  would have put it at 8-11x; the test was added for this case, by a builder who knows what followed;
- the FY2019 GAAP operating margin level as a guided margin step, carried for two years (no class moves; it drives BASE to -66%/yr);
- the GAAP basis through CA and Symantec's enterprise security business, whose amortization the non-GAAP figures remove (the 2009
  rule, as for LSI and BRCM);
- reading the fiscal-year guide against FY2018's 53-week revenue as published, and the non-GAAP 8-K ranges as the latest quarter
  guides (no class moves);
- the signals, unchanged since 2009, for a company with a software segment from FY2019 (28% of FY2020 revenue); DURABLE rather than
  CYCLICAL (the class label only); CLOUD on the watch list (text only).

### AVGO 2021-2023: quarter guides in dollars, the preferred stock converted, VMware and a fiscal-year guide

```bash
python3 retro/build_avgo.py --weekly 2021-01-04 2023-12-31                  # 156 dates, 2021-01-08 .. 2023-12-29
for c in 2021-01-01 2021-03-01 2021-06-01 2021-09-01 2021-12-15 2022-01-01 2022-05-26 2022-09-01 2022-12-15 2023-03-01 \
         2023-09-01 2023-12-10 2024-01-01; do python3 retro/tools/firewall.py $c AVGO; done
```

Every 8-K of Broadcom Inc. (CIK 1730168) from the Q4 FY20 release to the end of 2023 was checked for a guided number: the items of
each, the headline of every exhibit 99 and a sweep of every exhibit for "guidance", "outlook", "affirm" and revenue expectations. The
twelve releases were read in full (headlines, statements, outlooks, dividend and repurchase statements), and so were the FY2021-FY2023
10-Ks for the history, the tax items, the fiscal calendar, the business wording and the risk factors. The nine 10-Qs were searched for
dividend declarations and revenue expectations, the 56 425s and six DEFA14As (the VMware merger, the equity-plan vote) for Broadcom's
own outlook, and the VMware proxy statement/prospectus (S-4, S-4/As, 424B3) for projections. 177 more strings were checked with
`verbatim.py` (1,326 in all), 263 structured checks read every print's income-statement and balance-sheet figures back from its own
release (each year-ago inventory and each guide's year-ago revenue from that quarter's own release) and every vintage's from its 10-K,
and each of the 15 new sources' dates comes from EDGAR's acceptance time. Thresholds and signals are unchanged. Decided on 2026-11-02,
before any 2021-2023 date was built or scored:

- **Three vintages:** the FY2021 10-K (accepted 2021-12-17 16:42 ET, dated 2021-12-20), FY2022 (2022-12-16 16:21 ET, dated
  2022-12-19) and FY2023 (2023-12-14 16:54 ET, dated 2023-12-15). Item 6 is reserved from the FY2021 10-K, so each 10-K supplies the
  three years of its statements of operations and earlier years keep the latest 10-K that reported them (the ACN FY21 rule): FY2019
  from the FY2021 10-K, FY2020 from the FY2022 10-K, FY2016-FY2018 still from the FY2020 10-K. Each vintage holds the ten fiscal years
  to its latest one: FY2012-FY2021, FY2013-FY2022 and FY2014-FY2023. In the last, FY2014 is the first year and excluded (a distorted
  year), so the history and the P/E window start with FY2015 (the ACN FY02 rule, as for FY2009 in the FY2018 vintage).
- **EPS: GAAP diluted EPS,** as since 2009, attributable to common stock after the preferred dividends: FY21 $15.00 from continuing
  operations ($299M of preferred dividends), FY22 $26.53 ($272M; the mandatory convertible preferred stock converted into common
  stock in the fourth quarter), FY23 $32.98. The statements carry no discontinued operations from FY2021. All three years are kept:
  their listed items (restructuring, acquisition-related costs, a loss on debt extinguishment, gains and losses on investments) are
  fractions of their income, and FY21's $29M tax provision (0.4% of pre-tax income) comes from recurring items: excess tax benefits
  from stock awards, foreign derived intangible income and lapsed statutes (the AAPL FY2003 test and its mirror). FY2014, FY2016 and
  FY2018 stay excluded while they are among the ten years.
- **Guides.** Each release from Q4 FY20 to Q3 FY23 guides the next quarter's revenue as a dollar level ("approximately $6.5
  billion"), read against the same quarter a year earlier from its own release (the 2009 and AAPL rules): Q2 FY21 $6.5B (+13.2%),
  Q3 FY21 $6.75B (+16.0%), Q4 FY21 $7.35B (+13.7%), Q1 FY22 $7.6B (+14.2%), Q2 FY22 $7.9B (+19.5%), Q3 FY22 $8.4B (+23.9%), Q4
  FY22 $8.9B (+20.2%), Q1 FY23 $8.9B (+15.5%), Q2 FY23 $8.7B (+7.4%), Q3 FY23 $8.85B (+4.6%), Q4 FY23 $9.27B (+3.8%). The Adjusted
  EBITDA percentage beside each is non-GAAP and display only (the 2009 rule). No release gives a GAAP margin guide, so there is no
  margin step.
  - **The fiscal-year guide again.** The Q4 FY23 release guides fiscal year 2024 only, "including contributions from VMware"
    (acquired on 2023-11-22, after the year end): revenue of approximately $50.0 billion against FY23's $35,819M, +39.6% (method r2's
    fallback with no next-quarter guide, the LOW 2021 rule, as for FY2019 and FY2020). The acquisition enters only through the guide,
    as published (the LOW 2025 rule).
  - No 8-K between releases changes a guided number.
- **The Q2 FY22 release came before the open,** with the VMware announcement (8-K accepted 2022-05-26 07:28 ET; conference call at
  8:00 a.m. Eastern Time): dated 2022-05-26, the week's date 2022-05-27, the first trading day after it. Every other release came
  after the close and is dated the next trading day, a Friday each time and the week's last trading day: those prints meet that
  day's close, public before the open.
- **Dividends,** the latest declared rate from the first filing that states it: $4.10 (2021-12-10), $4.60 (2022-12-09) and $5.25
  (2023-12-08), each with the Q4 release. The $20.00 dividend on the preferred stock (to its conversion) shows only in the
  cash-return text.
- **The fiscal calendar.** FY2021-FY2023 are 52-week years ending on the Sunday closest to October 31, as each 10-K states. FY2024
  has 53 weeks and ends on 2024-11-03 (the Q4 FY23 release), which is also the Sunday closest to October 31, so it needs no
  `fiscal_calendar` entry.
- **Durability unchanged:** DURABLE, risk 2, in each 10-K's words. CLOUD stays on the watch list: the FY2021-FY2023 10-Ks repeat the
  FY2018-FY2020 sentence naming "the shift to cloud-based IT solutions and services, such as hyperscale computing" as affecting sales
  "for use in traditional enterprise data centers" (the FY2023 10-K's data-center Ethernet sentence changes and is quoted as
  written). GENAI is live from 2022-11-30 but stays off the watch list. Its scope (generative AI substituting software seats, IT
  services and BPO hours, professional information, search, education content, mobility) names none of Broadcom's products. The
  FY2022 and FY2023 10-Ks name AI only as features of Broadcom's own products and, once, in a regulatory risk ("particularly in cloud
  computing, artificial intelligence and our own data management practices"), never as a substitute for them (the AAPL rule).
- **Adds nothing:**
  - the VMware merger's filings: the 425s, the merger and voting agreements, the S-4, S-4/As and the 424B3 (its "VMware-Approved
    Broadcom Financial Projections" rest on analyst consensus and "were not prepared with a view toward public disclosure"), the
    expected-closing and regulatory updates (2023-08-21, 2023-10-18, 2023-10-30) and the completion (2023-11-22); the announcement's
    "$8.5 billion of pro forma EBITDA" within three years of closing (a run-rate, not a current-year figure); the VMware restructuring
    estimate in the Q4 FY23 8-K (item 2.05);
  - the share repurchase programs (2021-12-09, 2022-05-26; diluted share counts carry them), the debt offerings, exchange and tender
    offers, and the credit and term loan agreements;
  - the Apple statements of work (2023-05-23: multi-year), the investor presentation of 2021-01-06 (the equity-plan vote), officers,
    board, AGM votes and the proxies.
- **A display quirk, left as it is** so no earlier output changes: the builder's catalyst text reads "Avago guides one quarter at a
  time, in revenue only" on every quarter-guided date (491 dates to 2020-12-31 and 152 of 2021-2023), though the company has been
  Broadcom since 2016. Like the engine's "An analog semiconductor maker", it is fixed text.

Controls: altering one value of each print, Q4 full-year figure, guide, vintage, dividend and event changes no date before its
publication and changes the first weekly date on or after it (36 of 36). No new fact appears in a model dated before its publication
(89,955 checks over the 752 AVGO models), and no later calendar year appears in any model, report or analysis of 2021-2023. The 596
dates of 2009-2020 rebuild byte-identical, and so do the 2008 dates of ACN and the 2008-2009 dates of UNP, LOW, AAPL and NKE. The
firewall (a planted later print, vintage, guides with absurd values, withdrawals, dividend, event and company name, and 10x prices
after the cutoff) changes no earlier model at the 13 cutoffs above.

Seen in the build (method behaviour, not tuned):
- **Classes:** CHEAP on 96 dates, FAIR on 10, RICH on 50. Tiers: BUY on 87, AVOID on 48, ACCUMULATE on 17, WATCHLIST on 4. All
  eight robustness variants agree on 117 dates, seven on 30 and six on 5; four or fewer on 2022-01-14 and 2022-03-18 to 2022-04-01.
  Ratio B is infinite (the price above the BULL price) on 48 dates.
- **2021, on FY20's $6.33 (48 dates to the Q4 FY21 print).** The stock traded at 69.8-89.8x, the 95th-100th percentile of its own
  range, 168-246% above the EPP floor (26x): RICH and AVOID on all 48 dates, every variant agreeing, Ratio B infinite. The guides'
  +12.7% to +16.0% less the net buyback (-5.5%/yr: 252M diluted shares in FY11, 421M in FY20) put BASE at +7.2% to +10.5%/yr; BULL
  is +12.5%/yr (FY11 to FY20) and XBULL +50.3%/yr (FY13 to FY15). The window's median rose from 25.7x to 42.2x as the FY21 days, on
  FY20's EPS, filled it.
- **From the Q4 FY21 print, on FY21's $15.00** (28.5-44.4x). FAIR and WATCHLIST on 2021-12-10 and 2021-12-17 (Ratio B 1.13-1.15),
  then RICH on 2021-12-23 and 2021-12-31 under the FY2021 vintage (the 72nd percentile; BULL +23.5%/yr from FY12's $2.25). In 2022
  the price fell to $427-629 (the 31st-64th percentile): CHEAP on 43 of 48 dates, FAIR on 5; BUY on 31, ACCUMULATE on 17. The Q1-Q4
  FY22 guides put BASE at +8.4% to +18.1%/yr, and the EPP floor was 28x.
- **From the Q4 FY22 print, on FY22's $26.53** (20.5-36.9x, the 22nd-60th percentile): CHEAP on 49 of 52 dates and BUY on all (Ratio
  B 0.07-0.41), FAIR on 2023-11-10 to 2023-11-24. The FY2023 guides read +7.4%, +4.6% and +3.8% against FY2022's quarters, so BASE
  falls to +1.8%, -1.0% and -1.8%/yr; the class rests on BULL (+28.0%, then +31.9%/yr from FY13) and XBULL (+104.7%/yr, FY20 to
  FY22) at the window's multiples. The floor fell to 19x as FY2022's days were recomputed on its actual EPS, then rose to 20x and 22x.
- **From the Q4 FY23 print, on FY23's $32.98** (28.6-34.3x) with the FY2024 guide (+39.6%; BASE and BULL +34.5%/yr): CHEAP and BUY
  on all 4 dates.
- **The proxy composite:** 2.9 on Q4 FY20, 3.2 on Q1 FY21, 3.35 on Q2 FY21, 3.2 on Q3 FY21, 2.9 on Q4 FY21, 2.75 on Q1 FY22, 2.9 on
  Q2 FY22 to Q1 FY23 (the inventory gap at BEAR on the four FY22 prints, +28 to +44pp), 2.7 on Q2 FY23 and 2.55 on Q3-Q4 FY23
  (revenue growth at +4-5% and the opex gap turned positive).

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- FY2018 at GAAP $28.48 (the literal AAPL FY2002 test, which a benefit cannot meet; the exclusion was decided in 2017-2020) would
  change 37 classes and 62 tiers, all toward a richer reading: FAIR to RICH on 7 dates (2021-12-10 to 2022-04-01), CHEAP to RICH on
  12 (2022-02-04 to 2022-05-27), CHEAP to FAIR on 18 (2022-01-28 to 2023-12-01). FY2018's own days return to the window at 7-9x,
  which lowers the 10th percentile (15.7x to 9.2x on 2022-03-04) and the EPP floor (28x to 19x), and BEAR becomes FY18 to FY19's
  -77.3%/yr;
- BASE on the latest quarter's revenue growth instead of the guides would change 2 classes (CHEAP to FAIR on 2023-12-15 and
  2023-12-22, where the FY2024 guide with VMware reads +39.6% against Q4 FY23's +4.1%) and no tier;
- FY2014 as an interior gap in the FY2023 vintage (its revenue and shares kept, the window from its first day) would change none.

Judgement calls that could carry hindsight:
- the FY2018 exclusion, carried from 2017-2020, which moves 37 classes and 62 tiers here: FY17's $4.03 stays a BULL and window anchor
  where GAAP $28.48 would put FY2018's days in the window at 7-9x;
- reading the FY2024 guide, swollen by VMware, against FY23 as published (2 classes against the quarter's growth);
- GENAI kept off the watch list (text only: the factor pair nets to zero and no class depends on it), a reading of the scope and the
  10-K wording by a builder who knows how AI demand later moved this stock;
- the FY2014 first-year exclusion in the FY2023 vintage (no class moves);
- the signals, unchanged since 2009, for a company whose software segment was 21-26% of revenue; DURABLE rather than CYCLICAL (the
  class label only); CLOUD on the watch list (text only);
- the builder had read the 2017-2020 hindsight summary (the commit message of its outcomes) before this range was built. Every
  2021-2023 encoding above applies a rule that existed before, and none was tuned on an outcome.

### AVGO 2024-2026: VMware, the 10-for-1 split, FY2024 excluded, quarter guides again

```bash
python3 retro/build_avgo.py --weekly 2024-01-01 2026-10-31                  # 148 dates, 2024-01-05 .. 2026-10-30
for c in 2024-01-01 2024-03-01 2024-06-13 2024-07-15 2024-09-01 2024-12-15 2025-03-01 2025-06-01 2025-09-01 2025-12-15 \
         2026-03-01 2026-06-01 2026-09-01 2026-11-01; do python3 retro/tools/firewall.py $c AVGO; done
```

Every 8-K and 8-K/A of Broadcom Inc. from the Q4 FY23 release to 2026-11-02 was checked for a guided number: the items of each
and the headline of every exhibit 99. The eleven releases were read in full (headlines, statements, outlooks, dividend, split and
repurchase statements), and so were the FY2024 and FY2025 10-Ks for the history, the tax items, the fiscal calendar, the business
wording and the risk factors. The nine 10-Qs were searched for dividend declarations, revenue expectations and recent developments;
the DEFA14As, the exchange-offer S-4s and 424B3s and the debt prospectuses (424B5, 424B2, FWP) for Broadcom's own outlook. 149 more
strings were checked with `verbatim.py` (1,475 in all). 245 structured checks read every print's income-statement and balance-sheet
figures back from its own release (each year-ago inventory and each guide's year-ago revenue from that quarter's own release, the
previous quarter's per-share column across the split) and every vintage's from its 10-K. Each of the 13 new sources' dates comes from
EDGAR's acceptance time. Thresholds and signals are unchanged. Decided on 2026-11-02, before any 2024-2026 date was built or scored:

- **Two vintages:** the FY2024 10-K (accepted 2024-12-20 17:26 ET, dated 2024-12-23) and FY2025 (2025-12-18 16:04 ET, dated
  2025-12-19). Each holds the ten fiscal years to its latest one, every year from the latest 10-K that reports it: FY2015-FY2024 and
  FY2016-FY2025. In the second, FY2016 (a loss) is the first year, so the history and the P/E window start with FY2017 (the ACN FY02
  rule, as for FY2009 and FY2014). No FY2026 10-K is out yet.
- **The 10-for-1 split** (`splits`): announced in the Q2 FY24 release (dated 2024-06-13), trading split-adjusted from 2024-07-15,
  Yahoo's split date. From that day every per-share fact published before it is divided by 10 and every share count multiplied (the
  shared `on_basis`, the UNP and AAPL rule), and prices are on the as-of share basis throughout ($1,700.67 on 2024-07-12, $157.35 on
  2024-07-19). The FY2024 and FY2025 10-Ks report FY2022 onward after the split; the earlier years of those vintages keep the
  publication date of the 10-K they come from (`eps_published`, `shares_published`), so on_basis divides them. FY22's $2.65 and FY23's
  $3.30 in the FY2024 10-K replace $26.53 and $32.98 divided by 10 (rounding only).
- **Builder changes for the split, no earlier output changes.** The check that refused a split after an excluded year now applies
  to the prints in scope (no excluded year's figure is shown on another share basis). As in the AAPL builder, the EPS history's
  comment carries on_basis's split note and a dividend declared before the split says "divided by 10 from the 10-for-1 split". The
  latest print's per-share words (EPS, shares, the cash return), when published before the split, say "(per share before the 10-for-1
  split effective 2024-07-15)": seven dates, 2024-07-19 to 2024-08-30. The 752 dates of 2009-2023 rebuild byte-identical.
- **EPS: GAAP diluted EPS from continuing operations,** as since 2009: FY24 $1.29 (net $1.23, after the split, with the discontinued
  operations VMware brought), FY25 $4.77. From FY2026 the statements carry no discontinued operations.
- **FY2024 excluded, a distorted year (the AAPL FY2002 test, as for FY2014).** Its listed one-off items exceed its $6,168M income
  from continuing operations: the Q3 FY24 release's "one-time discrete non-cash tax provision of $4.5 billion" from an intra-group
  transfer of IP rights, plus the Q4 FY24 release's $1,787M of restructuring and other charges, $549M of acquisition-related costs and
  $157M loss on debt extinguishment (VMware): $6,993M. The FY2024 10-K puts the transfer at 39.6 points of the year's 37.8% effective
  tax rate (about $3.9B on $9,916M of pre-tax income), and with that figure the items (about $6.4B) still exceed the income. No EPS
  excluding only them was published (the non-GAAP $4.87 also removes amortization and stock-based compensation: the 2009 rule).
  Both facts are public with the Q4 FY24 print (2024-12-13), so the exclusion starts there. The NKE FY2018 rule then applies:
  FY2024's own days leave the P/E window ("ex-FY24"), growth is measured only between years in the history, and FY23's EPS stands for
  FY25E until the Q4 FY25 print. FY2025 is kept: its listed items, including a one-time discrete non-cash tax benefit of $2.1 billion
  from lapses of statutes of limitations, are fractions of its $23,126M income (the AAPL FY2003 test and its mirror).
- **Guides.**
  - Fiscal 2024: the Q4 FY23 release's $50.0 billion (+39.6% on FY23) is reiterated in the Q1 FY24 release (a record with the same
    numbers, the CyOptics rule) and raised to $51.0 billion (+42.4%) in the Q2 FY24 release. With no quarter guide in scope, r2's
    fiscal-year fallback applies until the Q3 FY24 release.
  - From the Q3 FY24 release each release guides the next quarter's revenue as a dollar level, read against the same quarter a year
    earlier from its own release: Q4 FY24 $14.0B (+50.6%), Q1 FY25 $14.6B (+22.1%, against the 14-week Q1 FY24, as published: the
    2011 rule), Q2 FY25 $14.9B (+19.3%), Q3 FY25 $15.8B (+20.9%), Q4 FY25 $17.4B (+23.8%), Q1 FY26 $19.1B (+28.1%), Q2 FY26 $22.0B
    (+46.6%), Q3 FY26 $29.4B (+84.3%), Q4 FY26 $34.8B (+93.2%).
  - The Adjusted EBITDA percentages and, from the Q2 FY26 release, a non-GAAP operating income margin are display only (the 2009
    rule). No release gives a GAAP margin guide, so there is no margin step.
- **Dividends,** the latest declared rate from the first filing that states it: $5.25 (2023-12-08), divided by 10 from 2024-07-15;
  $0.53 (2024-09-06, the first rate declared after the split), $0.59 (2024-12-13) and $0.65 (2025-12-12).
- **Release timing.** Every release came after the close. Through FY2025 each was a Thursday, dated the Friday, the week's last
  trading day: those prints meet that day's close, public before the open. The Q2 FY24 release and the three FY2026 releases came on
  a Wednesday: dated the Thursday, with the week's date the Friday after.
- **The fiscal calendar.** FY2024 has 53 weeks (its first quarter 14) and ends on 2024-11-03, which is also the Sunday closest to
  October 31, so it needs no `fiscal_calendar` entry. FY2025 ends on 2025-11-02. The 10-Ks now state the rule as "the Sunday closest
  to October 31".
- **Durability unchanged:** DURABLE, risk 2, in each 10-K's words; the FY2025 10-K: "We operate in a highly cyclical semiconductor
  industry that is undergoing profound change due to AI". CLOUD stays on the watch list in each 10-K's wording: sales "of our
  semiconductor products for use in traditional enterprise data centers" (FY2024), "for use in enterprise data centers" (FY2025);
  the data-center Ethernet sentence now reads "AI data center" (FY2024) and "enterprise and AI data center" (FY2025). GENAI stays
  off the list. The FY2024 and FY2025 10-Ks name AI as Broadcom's own market and products (AI networking, custom accelerators,
  VMware's Private AI), as an upturn "which may not be sustainable", as a source of cyber attacks and as a reason for new business
  models (AI racks), never as a substitute for its products. The FY2024 10-K mentions "software seat licenses" among what it sells;
  no filing ties them to AI substitution.
- **Adds nothing:**
  - the VMware pro formas (8-K/A of 2024-02-08, 8-Ks of 2024-07-08 and 2025-09-10) and the split's charter amendment (2024-07-12);
  - the debt offerings (424B5, 424B2, FWP), the exchange offers (S-4, 424B3), the tender offers (2026-06-11, 2026-06-18), the credit
    agreements and repayments, and the share repurchase programs (diluted share counts carry them);
  - the Google TPU and Anthropic capacity agreement (2026-04-06) and the Apple custom ASIC agreements (2026-07-06), multi-year;
  - the AI XPV platform and its backstop (8-K of 2026-10-27; the Q3 FY26 10-Q's recent developments: a contingent liability of up to
    about $29 billion, no guided number);
  - officers, board, AGM votes, the CEO's performance award (2025-09-09) and the proxies.
- **The last date is 2026-10-30,** a complete week: the series was built on 2026-11-02 before the open. The newest dates have no
  two-year outcome yet.

Controls: altering one value of each print, Q4 full-year figure (the excluded FY2024's revenue), guide, vintage, dividend and event
changes no date before its publication and changes the first weekly date on or after it, and the split changes none before its
effective date (32 of 32). No new fact appears in a model dated before its publication (91,759 checks over the 900 AVGO models), and no
later calendar year appears in any model, report or analysis of 2024-2026. The 752 dates of 2009-2023 rebuild byte-identical, and so do
the 2008 dates of ACN and the 2008-2009 dates of UNP, LOW, AAPL and NKE. The firewall changes no earlier model at the 14 cutoffs above.

Seen in the build (method behaviour, not tuned):
- **Classes:** RICH on 71 dates, FAIR on 47, CHEAP on 30. Tiers: AVOID on 68, BUY on 52, ACCUMULATE on 21, WATCHLIST on 7. All eight
  robustness variants agree on 74 dates, seven on 51, six on 20, five or fewer on 3. Ratio B is infinite on 24 dates.
- **2024 to the Q2 FY24 print** (FY23's $32.98, $3.298 after the split; the FY2024 guide +39.6%, BASE and BULL +34.5%/yr): CHEAP and BUY
  on all 23 dates (31.8-42.7x, the 53rd-70th percentile, Ratio B 0.27-0.64).
- **The raised FY2024 guide and the Q4 FY24 guide** (BASE +37.3%, then +45.5%/yr; 41.5-55.7x, the 64th-92nd percentile): FAIR on 20
  of 26 dates, CHEAP on 3, RICH on 3 (2024-06-14, 2024-07-05 and 2024-07-12); BUY on 9, ACCUMULATE on 17.
- **From the Q4 FY24 print, FY2024 excluded,** FY23's $3.30 stands for FY25E at 44.3-122.1x (the 66th-100th percentile). The EPP floor
  rose from 23x to 34x on 2025-01-03, when 2014 left the ten-year window and 2025 (about 70x) joined its calendar-year lows; with
  FY2024's own days out of the window, 2024's low was already 48.4x. RICH on 46 of 52 dates and AVOID on 48; FAIR on 2025-03-21 to
  2025-04-25 and CHEAP on 2025-04-04, at the April low (44.3x). The guides' +19.3% to +23.8% less the net buyback (-5.7%/yr: 2,810M
  diluted shares in FY15 after the split, 4,778M in FY24) put BASE at +13.6% to +18.1%/yr, and BULL is +26.8%/yr (FY15 to FY23). From
  2025-06-27 the price stood above the BULL price: Ratio B infinite on 24 dates.
- **From the Q4 FY25 print, on FY25's $4.77** (63.0-93.7x, the 87th-100th percentile; the floor 32-33x): RICH and AVOID on all 12
  dates to 2026-02-27 (BASE +22.8%, then +26.3%/yr with the FY2025 vintage's -1.8%/yr buyback). The Q2 FY26 guide (BASE +44.8%):
  RICH on 10 of 13 dates, CHEAP on 2026-03-20 to 2026-04-02. The Q3 and Q4 FY26 guides read +84.3% and +93.2% against FY2025's
  quarters (BASE +82.5% and +91.4%/yr): FAIR on all 22 dates to 2026-10-30, BUY on 20, the conservative case +54% to +125%.
- **The proxy composite:** 2.55 on Q4 FY23, 2.2 on Q1-Q2 FY24 (VMware's operating expenses and the margin change at BEAR), 2.4 on
  Q3-Q4 FY24, 3.5 on Q1 FY25, 3.05 on Q2 FY25, 2.9 on Q3-Q4 FY25, 2.75 on Q1 FY26, 2.9 on Q2 FY26 and 3.2 on Q3 FY26.

How far each call moves the classes (the 148 dates rebuilt with one encoding changed; no outcome consulted):
- FY2024 at GAAP $1.29 instead of excluded would change 6 classes (FAIR to RICH on 5 dates of 2025-03-21 to 2025-04-25, CHEAP to RICH
  on 2025-04-04) and 14 tiers. FY24's $1.29 would anchor FY25E (113x on 2025-04-04, the 90th percentile) and BEAR would become FY23
  to FY24's -60.9%/yr; most dates of 2025 read RICH either way;
- FY2018 at GAAP $28.48 (the exclusion decided in 2017-2020) would change 55 classes and 66 tiers, all toward a richer reading: CHEAP
  to FAIR on 5 dates, CHEAP to RICH on 18 and FAIR to RICH on 32;
- BASE on the latest quarter's revenue growth instead of the guides would change 33 classes and 29 tiers, both ways: 26 toward a
  richer reading (13 of them from 2026-06-05, where the guides ran far above the quarter just reported) and 7 toward a cheaper one
  (2024-07-05 to 2025-02-28);
- FY2016 as an interior gap in the FY2025 vintage would change none.

Judgement calls that could carry hindsight:
- excluding FY2024 by the AAPL FY2002 test (6 classes, 14 tiers), with the one-time tax provision counted as a listed item, as the
  FY2018 tax benefits were, by a builder who knows what FY2025 and FY2026 earned;
- the FY2018 exclusion, carried from 2017-2020, which moves 55 classes and 66 tiers here;
- BASE on the guides (33 classes against the quarter's growth): the 2026 guides read +84% and +93% against FY2025's quarters;
- GENAI kept off the watch list (text only), and the reading of "software seat licenses";
- the split encoding (`eps_published`: rounding only) and the display marker for pre-split words;
- the signals, unchanged since 2009, for a company whose software segment was 42% of FY2025 revenue; DURABLE rather than CYCLICAL
  (the class label only), though the FY2025 10-K calls the industry "highly cyclical" and "undergoing profound change due to AI";
- the builder had read the 2017-2020 and 2021-2023 hindsight findings before this range was built. Every 2024-2026 encoding above
  applies a rule that existed before (the split encodings follow the AAPL builder), and none was tuned on an outcome.

## PEP (PepsiCo): the seventh ticker, in staging

The PEP series is built apart from ACN, UNP, LOW, AAPL, NKE and AVGO and shares nothing with them but the machinery: its own
fact sheet (`retro/facts/PEP.json`), builder (`retro/build_pep.py`) and engine (`retro/templates/pep_engine.py.tmpl`, the NKE
engine with beverage and convenient-food signals and the AVGO engine's pre-tax EPS check). The method is still r2. No ACN, UNP,
LOW, AAPL, NKE or AVGO fact, parameter, outcome or finding enters a PEP model. Outputs go to `staging/retrospective/PEP/`, beside
the others, with the same `index.json` and their own `SERIES.md`.

```bash
python3 retro/build_pep.py --weekly 2008-01-01 2008-12-31                   # 53 dates, 2008-01-04 .. 2008-12-31
for d in staging/retrospective/PEP/2008-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series PEP
python3 retro/tools/firewall.py 2009-01-01 PEP
```

The 10-Ks from FY1997 to FY2007 (with the FY1999 and FY2002 10-K/As, which carry no figures) were read for the history and the
decade's signal values; Sonnet 5.5 agents transcribed them and checked 2,206 strings word for word with `verbatim.py` against their
own filings. Every 8-K and 10-Q from October 2006 to December 2008 was read by Opus directly, with the Q4 releases of 2001-2006 for
the figures they publish excluding one-offs; 90 more strings were checked. Each source's date comes from EDGAR's acceptance time
(converted from UTC; before 2003 EDGAR gives the filing date only). Decided on 2026-11-02, before any PEP model was built or any
PEP outcome computed:

- **Fiscal calendar.** PepsiCo's fiscal year "ends on the last Saturday of each December, resulting in an additional week of
  results every five or six years" (FY2006 10-K); quarters of 12, 12, 12 and 16 weeks (17 in 2005). The builder maps each day to
  its fiscal year by that rule and checks it against the year-ends the vintages state.
- **Prices as traded.** PepsiCo last split in 1996, before every fact in the fact sheet: Yahoo's series is the price as traded,
  no fact is restated, and the builder refuses a split factor other than 1.
- **Every release came during the session.** Each earnings 8-K of 2007-2008 was accepted between 09:39 and 10:34 ET on its
  release day (the conference call at 11 a.m. ET), so a print is dated its release day and the week's date is the next trading
  day: 2008-02-08, 2008-04-25, 2008-07-24 and 2008-10-15. The 10-Qs, accepted after the close, count from the next trading day.
- **History: each year from the latest 10-K that reports it.** The FY2006 10-K (accepted 2007-02-20 16:57 ET, dated 2007-02-21)
  gives 2002-2006; 2001 comes from the FY2005 10-K, 2000 from the FY2004 10-K, 1999 from the FY2003 10-K and 1998 from the FY2002
  10-K. The Q4 2007 print extends it with FY2007 from 2008-02-07, and the FY2007 10-K (accepted 2008-02-15 15:27 ET, during the
  session) moves the window to 1998-2007. Three seams stay in, as published (the LOW rule):
  - the Quaker Oats pooling of 2001 restated 1997-2000 in the FY2001 10-K, but the only filings that report 1998's diluted shares
    are the earlier ones (1,519M, FY2000 10-K), so the buyback runs from a pre-pooling first year to pooled later years: -1.3%/yr
    over 1998-2006, -1.0%/yr over 1998-2007, where the pooled share count fell;
  - the stock-option restatement of 2001-2003 in the FY2003 10-K ("Fiscal years 2000 and 1999 have not been restated"), so 2001
    carries option expense and 2000 does not;
  - the EITF 01-9 reclassifications (net revenue from the FY2002 10-K) and the 2005 move of warehouse and freight costs from cost
    of sales to SG&A (the FY2005 10-K), each year's revenue and margins on the basis of its source 10-K.
- **EPS** is diluted EPS from continuing operations (diluted EPS where none were discontinued). A company figure excluding
  one-offs only replaces it (the ACN rule), from any filing on the same basis: 1999 $1.23 and 2000 $1.46, the FY2001 10-K's
  "comparable" figures (excluding the 1999 bottling gain, the fifty-third week of 2000, impairment and restructuring charges,
  Quaker one-time items and tax items; GAAP $1.38 and $1.42); 2004 $2.32 (Q4 2004 release), 2005 $2.66 (Q4 2005 release; the
  AJCA tax charge, the extra week and restructuring), 2006 $3.00 and 2007 $3.38 (tax items and restructuring). 1998 ($1.23),
  2001 ($1.33) and 2002 ($1.68) stay GAAP: the comparable $1.66 for 2001 and $1.96 for 2002 were published before the
  restatement, on the earlier basis (the UNP trucking rule). 2003 is $2.05 either way.
  - **1997 is excluded.** On the pooled basis of the FY2001 10-K, the latest that reports it, 1997's $0.30 from continuing
    operations is under half of the $1.05 without its listed items (a $1.1 billion after-tax loss on a business divestiture,
    $0.61 a share, and $0.14 of impairment and restructuring), and no adjusted figure was published on that basis (the ACN FY02
    and AAPL FY2002 rule). The history starts with fiscal 1998 and so does the P/E window (`pe_window_start` 1997-12-28; the
    ten-year window of every 2008 date starts later anyway).
- **The 2008 core rule.** From the Q2 2008 release PepsiCo's "core" figures and guides also exclude "the commodity
  mark-to-market net impact included in corporate unallocated expenses". That item recurs in every period ($19 million of gains in
  2007, $346 million of losses in 2008) and its gains and losses "are subsequently reflected in division results when the divisions
  take delivery of the underlying commodity": a timing basis, not a one-off (the AAPL Q4 FY08 subscription-accounting and NKE
  FY2007 rule). So a core figure does not replace GAAP, and a core guide gives no field. Nothing is derived from the per-share
  effects the reconciliations list.
- **No EPS guide gives a field.** Every 2007-2008 EPS guide is a one-sided bound: fiscal 2007 "at least $3.30", then $3.35, then
  "at least $3.39" reported and "at least $3.35" core; fiscal 2008 "EPS of at least $3.72" (the Q4 2007 release, the CAGNY 8-K of
  2008-02-20, the Q1 2008 release, the 8-Ks of 2008-06-10 and 2008-06-16), "excluding the impact of any mark-to-market
  gains/losses" from the Q2 2008 release. A one-sided bound gives no field (the UNP "below 80%" and LOW "tracking ahead of" rule).
  The Q3 2008 release's "core 2008 earnings per share in the range of $3.67 — $3.68 (excluding any commodity mark-to-market
  impact and Productivity for Growth costs)" is a range on the core basis (the rule above). So the last full year's EPS stands
  all year (the rollover rule): FY06's $3.00 to the Q4 2007 print, FY07's $3.38 from it. Each guide is shown in the guide line
  with the reason it gives no field.
- **Revenue and volume guides are words or volume.** "mid-to-high single digit", "high-single-digit" and "low-double-digit net
  revenue growth (including acquisitions and foreign exchange)" are words (the UNP 2016 rule), and the "3% to 5% volume growth"
  is not revenue, so BASE growth and the growth factor take the latest quarter's net revenue growth excluding currency: the growth
  the release states less the currency effect the release or the quarter's 10-Q states (the NKE rule): Q3 2007 +8% (11 less the
  10-Q's "nearly 3"), Q1 2008 +10% (13 less 3), Q2 2008 +10% (14 less 4), Q3 2008 +8% (11 less 3). No filing states the
  currency effect on the fourth quarter of 2007 (the release gives PepsiCo International's "over 7 percentage points" and the
  year's "about 2 points"), so its reported +17% stands.
- **No operating-margin guide**, so no margin step; the margin signal takes the latest quarter's change.
- **Dividends,** each from the first filing that states the rate: $0.30 a quarter (FY2006 10-K), $0.375 from the 8-K of
  2007-05-02 ("a 25% increase in the annual dividend, raising it to $1.50 per share from $1.20 per share"; first entered from the
  Q2 2007 10-Q and corrected in the 2009-2010 batch, a source change only), $0.425 from the Q2 2008 10-Q (accepted 2008-07-23
  16:33 ET, dated 2008-07-24: "a 13% dividend increase from
  $1.50 to $1.70 per share"). The releases state no dividend.
- **Signals.** Six, with ACN's weights: volume (servings) growth (0.20, the releases' headline unit, "Volume (Servings)" in each
  summary table), gross margin change (0.20), net revenue growth (0.15, as reported), inventory growth less net revenue growth
  (0.15, lower is better; the year-ago quarter's inventories from its own release, since a release's balance sheet compares with
  the prior year-end), the operating-margin change (0.15; the guided step, else the latest quarter) and the theme slot at 2/4.
  Values are each release's, derived from its income statement and balance sheet (the fact sheet keeps the raw figures and the
  builder re-derives them). An operating profit on a comparable basis that excludes one-offs only replaces GAAP (Q4 2007:
  $1,832M vs $1,656M excluding restructuring); a core statement that also excludes the mark-to-market item does not (2008).
- **Thresholds by rule T** over the ten years of the FY2006 10-K, the vintage public on 2008-01-04: FY1997-FY2006, each change
  from the latest 10-K published by then that reports both years (income statements for the margins, five-year summaries for net
  revenue), the inventory gap within each year's own 10-K, seams included. Total servings growth was first stated for 2000 (FY2001
  10-K), so that signal has seven values (the AVGO rule: the years the filings report). A company figure excluding one-offs
  replaces the reported one where it was published for both years on the same basis: 1997 and 1998 operating margins on the FY1998
  10-K's ongoing operating profit (excluding unusual items); 2005 and 2006 net revenue excluding the 53rd week of 2005 ($32,144M);
  the 2005 gross margin and the 2006 gross and operating margins on the Q4 2006 release's comparable basis. The values are in the
  fact sheet (`rule_t`); the builder recomputes the thresholds and refuses to build if the engine's differ.

  | Signal | Annual values | BEAR / BASE / BULL / XBULL |
  |---|---|---|
  | volume (servings) growth | 2000-2006: 5, 4, 4, 5, 6, 7, 5.5 % | 3 / 4 / 5 / 7 % |
  | gross margin change | 80.3, -99.2, 149.7, 101.6, 5.9, -6.2, -11.5, 3.3, -23.7, -130.8 bp | -260 / -130 / 0 / 150 bp |
  | net revenue growth | 2.85, 4.85, -9.84, 0.69, 5.26, 6.81, 7.4, 8.49, 9.85, 9.31 % | -26 / -10 / 6 / 10 % |
  | inventory less net revenue | -17.0, 32.0, -2.7, 0.3, 4.2, -4.4, -2.2, 0.6, -1.4, 5.9 pp | 65 / 32 / -1 / -17 pp |
  | operating margin change | 125.0, -126.2, 227.4, 110.5, 0.9, 163.9, 62.3, 24.6, 21.4, 6.8 bp | -300 / -130 / 40 / 230 bp |

- **Durability.** DURABLE, risk 2, as for the other six. The "why" is the 10-K's own words: "We are a leading global snack and
  beverage company", "Our businesses operate in highly competitive markets", The Coca-Cola Company as "our chief beverage
  competitor" (the FY2006 10-K: "a slightly larger share of carbonated soft drink (CSD) consumption in the U.S."; the FY2007 10-K:
  "a similar share of CSD"), and "Our success depends on our ability to respond to consumer trends, such as consumer health
  concerns about obesity, product attributes and ingredients". No disruption theme in `taxonomy_eras.json` is live for a beverage
  and convenient-food company in 2008 (GLP1, whose scope names snacks and beverages, from 2023-08-08; ECOMMERCE is scoped to
  physical retail, OFFSHORE to IT services); no theme covers the obesity risk, so it stays in the "why". The watch list is empty
  and the builder refuses events until a theme encoding is decided.
- **Segment bridge and EPS check** (display only): the vintage's four divisions (FLNA, PBNA, PI, QFNA), each with its growth. The
  2008 reorganization into six segments is recast by the 8-Ks of 2008-03-24 and 2008-04-07, which "do not revise or restate" the
  consolidated statements: a segment recast adds nothing (the ACN 2024-09-30 rule), so the bridge keeps the FY2007 10-K's four
  divisions until the next 10-K. The EPS check runs on the pre-tax margin, which carries bottling equity income and net interest.
- **Adds nothing:** the 8-Ks on officers, directors and compensation, the debt offerings (2007-11-29, 2008-10-24, 2008-05-21), the
  Lebedyansky agreement (2008-03-20, no guided number), the XBRL test filings furnished after each 10-Q and 10-K, the segment
  recasts, and the 10-Qs beyond their currency effects and dividends.
- **Anachronism list:** PepsiCo names first seen after the start of 2008 (Lebedyansky, Productivity for Growth, PureVia, Trop50,
  Pepsi Refresh, Wimm-Bill-Dann) join `taxonomy_eras.json`, dated from the first PepsiCo filing that uses them. No existing model of
  any ticker contains them, so no output changes.

Controls: altering one value of each print, vintage, guide and dividend changes no date before its publication and changes the
first weekly date on or after it (19 of 19; the Q3 2007 release's fiscal 2007 guide is superseded by the 8-K of 2007-11-14 on every
2008 date and changes nothing). Rebuilding the 2008 dates of ACN, UNP, LOW, AAPL and NKE and the 2009 dates of AVGO changes nothing.

Seen in the build (method behaviour, not tuned):
- **CHEAP on all 53 dates; tier BUY on 52** and ACCUMULATE on 2008-01-11 (Ratio B 0.77). Robustness agrees on 6-8 of 8 variants.
- **EPS anchors on the last full year.** FY06's $3.00 stands to 2008-02-07, when nine-month 2007 EPS was already $2.64 ($2.57
  excluding the tax item): the stock traded at 22.9-25.9x it (the 44th-59th percentile). From the Q4 2007 print FY07's $3.38 is
  the anchor: 20.3-21.2x to April (the 17th-30th percentile), 15.2-17.1x from 2008-10-10 (the 0th-2nd).
- **BEAR is the restatement seam.** The worst year in the history is 2001 (-8.9%: 2000's $1.46 before option expensing, 2001's
  $1.33 after it), so BEAR is -8.9%/yr on every date, at the 10th-percentile P/E: $50 on FY06's EPS, $55 on FY07's.
- **BULL and XBULL** are the 1998-2006 EPS CAGR (+11.8%/yr; +11.9% over 1998-2007) and the 2001-2003 run (+24.2%/yr), the latter
  also lifted by the seam.
- **BASE is the quarter's growth excluding currency less the pooling seam:** +6.7%/yr on Q3 2007 (8% less 1.3%), +16.0% on Q4
  2007 (the reported 17%, no currency effect stated), +9.0% on Q1 and Q2 2008, +7.0% on Q3 2008. The growth factor reads +0.09,
  +0.50, +0.26, +0.26 and +0.06 against the history's median revenue growth (7.1%, then 7.4% with FY2007).
- **The proxy composite** is 2.30 on Q3 2007 (net revenue +11.4% at XBULL, the rest at BASE), 2.50 on Q4 2007 and Q2 2008
  (servings +5% at BULL), 2.10 on Q1 2008 (gross margin -132bp, below the decade's worst year) and 1.75 on Q3 2008 (servings +2%,
  gross margin -136bp and operating margin -263bp at BEAR).
- **From the market's fall the price sits at the BEAR price:** $51-57 from 2008-10-15 against BEAR's $55, so Ratio B is -0.05 to
  0.03, and the price is 10-20% below the EPP floor (19x FY07's $3.38, $64; 20x FY06's $3.00 before) from 2008-10-10.

How far each call moves the classes (the 53 dates rebuilt with one encoding changed; no outcome consulted):
- "at least" read as a point (fiscal 2007 core $3.35, fiscal 2008 $3.72) would change no class and 1 tier (2008-01-11, ACCUMULATE
  to BUY);
- the Q3 2008 core range used ($3.675 from 2008-10-14) would change nothing;
- the buyback measured from 1999's pooled 1,817M diluted shares, without the pooling seam, would change nothing;
- Q4 2007 growth excluding the year's 2 points of currency (15% instead of 17%) would change nothing;
- 1999 and 2000 at GAAP ($1.38, $1.42) would change nothing;
- FY1997 kept at the pooled $0.30 would change no class and 1 tier (2008-01-11).

Judgement calls that could carry hindsight:
- the signals, chosen by a builder who knows what 2008 brought: servings and the inventory gap (rule T then sets the thresholds
  mechanically);
- the 2008 core rule (it moves nothing in 2008; it decides FY2008's entry into the history from the Q4 2008 print);
- reading "at least" as a one-sided bound, and the core range as no field (1 tier);
- keeping the three seams, which set BEAR (-8.9%/yr) and the buyback (-1.0% to -1.3%/yr);
- excluding FY1997, and the Q4 2007 print's reported growth for want of a stated currency effect;
- DURABLE (the class label only).

### PEP 2009-2010: two GAAP years under the core rule, a revenue guide in numbers, the bottler acquisitions

```bash
python3 retro/build_pep.py --weekly 2009-01-05 2010-12-31                   # 104 dates, 2009-01-09 .. 2010-12-31
for c in 2010-01-01 2011-01-01; do python3 retro/tools/firewall.py $c PEP; done
```

All 52 8-Ks, the 8-K/A, the six 10-Qs and the FY2008 and FY2009 10-Ks filed from December 2008 to December 2010 were checked:
the eight releases, the four guidance 8-Ks, the dividend 8-Ks and the SFAS 160 re-presentation read in full, and every other 8-K
read for guides, figures and dividend rates. 129 strings from the releases and 8-Ks, and 361 and 409 from the two 10-Ks
(transcribed as the earlier ones were), were checked word for word with `verbatim.py` against their own filings; the builder
re-derives every print's signal values from its raw figures. Each source's date comes from EDGAR's acceptance time. Thresholds,
signals and the engine are unchanged; the builder gained an encoding for a fiscal-year revenue guide (`rev_guide`, below).
Decided before any 2009-2010 outcome was computed:

- **Three vintages.** The FY2008 10-K (accepted 2009-02-19 16:40 ET, dated 2009-02-20) gives 2004-2008, and each earlier year
  comes from the latest 10-K that reports it: the history runs 1999-2008. The 8-K of 2009-08-27 (16:41 ET, dated 2009-08-28)
  re-presents the FY2006-FY2008 statements for SFAS 160 (noncontrolling interests): a re-presentation of the 10-K's financial
  statements is a vintage (the UNP 2010-10-25 rule). It moves FY08 operating profit to $6,959M ($6,935M in the 10-K) and pre-tax
  income to $7,045M, leaves diluted EPS at $3.21, and names the Europe and Asia, Middle East & Africa segments. The FY2009 10-K
  (2010-02-22 16:19 ET, dated 2010-02-23) gives 2005-2009: the history runs 2000-2009.
- **The pooling seam leaves the buyback.** With 1999 as the first year, the first-year diluted shares are the pooled 1,817M (FY2001
  10-K, the latest that reports them), then 2000's 1,791M (FY2002 10-K): the buyback is +1.4%/yr over 1999-2008 (to 1,602M) and
  2000-2009 (to 1,577M), against -1.0% to -1.3%/yr in 2008. On 2009-02-13, between the Q4 2008 print and the 10-K, the history is
  1998-2008 and the seam still runs (-0.5%/yr). The option-restatement seam (2000 before option expense, 2001 after) stays in
  both windows, so BEAR stays -8.9%/yr.
- **FY2008 and FY2009 at GAAP (the 2008 core rule).** FY08 enters at $3.21 from the Q4 2008 print (released Friday 2009-02-13, 08:24
  ET, before the open): the company's core $3.68 also excludes the commodity mark-to-market net impact, and no figure excluding only
  the Productivity for Growth charges and PepsiCo's share of PBG's charges was published. FY09 enters at $3.77 from the Q4 2009
  print (2010-02-11, 09:44 ET, during the session): the core $3.71 also excludes the mark-to-market impact. The prints show GAAP
  quarterly EPS with the core figure in the note, and the margins stay GAAP for the same reason.
- **One revenue guide in numbers.** The 2009 guidance for net revenue and core EPS is in words, "mid- to high-single-digit growth on
  a constant currency" basis (the Q4 2008 release, the 8-K of 2009-02-13 and the Q1-Q3 2009 releases): words are not figures (the
  UNP 2016 rule), and the EPS half is on the core basis. The 8-K of 2009-12-08 (16:53 ET, dated 2009-12-09) expects "constant
  currency net revenue to be up about five percent": a point (the LOW "approximately" rule) and a fiscal-year revenue guide, which
  method r2 prefers to the latest quarter's growth, so it feeds BASE and the growth factor from 2009-12-11 to the Q4 2009 print.
  It equals the Q3 2009 quarter's 5%, so nothing moves. Its "about five to six percent" core EPS growth gives no field.
- **No EPS guide gives a field.** Every 2010 EPS guide is a core growth range: "an 11 to 13 percent growth rate for core constant
  currency EPS off of its fiscal 2009 core EPS of $3.71" (the Q4 2009 release, reiterated by the 8-Ks of 2010-03-01 and
  2010-03-22 and the Q1 2010 release), then core EPS growth "in the 10 to 12 percent range" (Q2 2010) and "in the 10 to 11 percent
  range" (Q3 2010). So the last full year's EPS stands (the rollover rule): FY07's $3.38 to 2009-02-06, FY08's $3.21 from the Q4
  2008 print, FY09's $3.77 from the Q4 2009 print.
- **Growth excluding currency as each release states it** (the NKE rule): Q4 2008 +8.5% (the reported 3% and "Foreign exchange
  adversely impacted net revenue growth in the quarter by 5.5 percentage points"), then the stated constant-currency growth: +6%,
  +5.5%, +5% and +3% in 2009, and the stated core constant-currency growth of +11%, +37% and +41% in 2010.
- **The bottler acquisitions stay in growth (the AVGO rule).** PepsiCo consolidated The Pepsi Bottling Group and PepsiAmericas from
  2010-02-26 (the 8-K of 2010-03-01), and the 2010 releases' growth includes them, as published. BASE takes it, so from Q1 2010
  BASE passes BULL and from Q2 2010 XBULL too: both are floored at BASE. The merger 8-K of 2009-08-04 expects "annual pre-tax
  synergies of $300 million by 2012" and accretion "by about 15 cents per share when synergies are fully realized in 2012":
  later years' targets with no input in the method (the UNP 2018 rule). The 2010 margin and inventory signals carry the
  acquisitions as reported, with the GAAP charges (merger and integration costs and the fair-value step-up of acquired inventory).
- **A dash is zero.** The Q4 2009 and Q1 2010 releases print "—" in the Volume (Servings) row, read as 0% (the UNP carloads rule).
  The FY2009 10-K says total servings "increased slightly" in 2009, with no figure: the franchise line shows the words.
- **Dividends,** from the first filing that states each declared rate: $0.45 a quarter from the 8-K of 2009-05-05 (18:48 ET, dated
  2009-05-06: "a 6 percent increase in the annual dividend, from the current $1.70 to $1.80 per share"), $0.48 from the Q2 2010
  10-Q (17:05 ET, dated 2010-07-21). The 8-K of 2010-03-15 says the board "approved a 7 percent increase in the annual dividend"
  to $1.92, which "will take effect when the Board declares the next quarterly common stock dividend". A rate that still has to be
  declared is not a declared rate (the AAPL 2012 rule), and no filing states the declaration before the Q2 2010 10-Q. This can
  only lag.
- **Calendar.** Every 2009-2010 release came before the open (07:36-08:50 ET) except Q4 2009 (09:44 ET, during the session). The
  Q4 2008 release came on a Friday, the week's last trading day, so the print meets that day's close (the NKE rule). The weeks'
  dates after the other releases are the next trading days: 2009-04-21, 2009-07-23, 2009-10-09, 2010-02-12, 2010-04-23, 2010-07-21
  and 2010-10-08.
- **Durability is unchanged:** DURABLE, risk 2, with each 10-K's own words ("a leading global beverage, snack and food company" in
  FY2008, "food, snack and beverage" in FY2009, which adds "The Coca-Cola Company has a significant CSD share advantage in many
  markets outside the United States"). No theme in the registry is live for PepsiCo in 2009-2010.
- **Adds nothing:** the officer and director 8-Ks, the bylaw amendments (2009-09-18, 2010-02-05, 2010-09-28), the 2010 annual
  meeting (2010-05-11), the XBRL exhibit (2009-02-19), the subsidiary financial statements (2009-02-20), the note offerings, a
  credit agreement's termination and a debt guarantee (2009-02-27, 2010-01-13, 2010-06-17, 2010-10-05, 2010-10-25), the bottler
  proposals, litigation, antitrust and merger filings from 2009-04-20 to the closing 8-Ks of 2010-02-26 and 2010-03-01 (with the
  8-K/A of 2010-04-22 incorporating PBG's and PAS's statements), the second 8-K of 2010-02-11 (a summary of that day's release), the
  segment recast of 2009-03-25 (Turkey and some Central Asian markets moved within PepsiCo International: the ACN 2024-09-30 rule),
  the clarification of 2010-08-24 (R&D spending), the Gatorade distribution release of 2010-09-01, the Wimm-Bill-Dann agreement
  (2010-12-02), and the 10-Qs beyond their dividends.

Corrections to 2008, found while extending the series and applied before any 2009-2010 outcome: the $0.375 dividend's source is the
8-K of 2007-05-02, the first filing that states it (it had been the Q2 2007 10-Q; the rate was public before 2008 either way), and
the servings line's previous quarter is the print published before the latest one (Q3 2007 on the ten dates from 2008-02-15 to
2008-04-18, which had shown the vintage's Q2 2007). Both change text only, on 16 dates: no metric, class, tier or 2008 outcome
moves.

Controls: altering one value of each print, vintage, guide and dividend published from 2008-12-01 changes no date before its
publication and changes the first weekly date on or after it (25 of 25). No string of any print, vintage, guide, dividend or source
appears in a model dated before it (12,766 checks over the 157 PEP models). The firewall at 2010-01-01 and 2011-01-01 changes no
model before its cutoff. The 53 dates of 2008 rebuild identical apart from the two corrections, and no file shared with another
ticker changed.

Seen in the build (method behaviour, not tuned):
- **CHEAP and BUY on all 104 dates.** The tier agrees on 7 or 8 of the 8 robustness variants on every date; the valuation verdict
  on 2 to 8 (2 on 2009-12-04, 4 on five dates from 2009-02-13 to 2009-04-17).
- **EPS anchors on the last full year:** FY07's $3.38 to 2009-02-06 (14.9-15.8x, the 0th-2nd percentile of its own range), FY08's
  $3.21 from 2009-02-13 to 2010-02-05 (14.7-19.9x, the 0th-24th) and FY09's $3.77 from 2010-02-12 (16.1-17.8x, the 9th-20th).
- **The price sat at the floors.** Below the BEAR price on 14 dates from 2009-01-09 to 2009-05-15 (Ratio B -0.07 to -0.01; BEAR
  $51-55). At or below the EPP floor on 91 dates: 19x to the end of 2009 ($64 on FY07's EPS, $61 on FY08's), 18x from 2010-01-08
  ($58, then $68 on FY09's $3.77). Above it on 13 dates from 2009-10-16 to 2010-02-05, by up to 7.8%; the highest Ratio B was 0.41
  on 2009-12-04 ($63.85).
- **BEAR is -8.9%/yr on every date** (the 2001 seam). BULL is the window's EPS CAGR: +11.9%/yr (1998-2007) to 2009-02-06, +10.1% on
  2009-02-13 (1998-2008, with FY08 at GAAP), +11.2% (1999-2008) from the FY2008 10-K, +11.9% (1999-2009) from the Q4 2009 print and
  +11.1% (2000-2009) from the FY2009 10-K. XBULL is the 2001-2003 run (+24.2%/yr) to Q1 2010.
- **BASE followed the quarter's constant-currency growth plus the buyback:** +7.0%/yr on Q3 2008, +8.0% on 2009-02-13 (8.5% less
  the seam's 0.5%), +9.9% from the FY2008 10-K (8.5% plus 1.4%), +7.4%, +6.9% and +6.4% on Q1-Q3 2009 (the about-5% guide kept
  +6.4%), +4.4% on Q4 2009, then +12.4%, +38.4% and +42.4% on the 2010 quarters with the bottlers. The BASE price went from $78-88
  to $101-102 on Q1 2010 and $153-161 from Q2 2010, and the adjusted gap from 0.44-1.21 to 2.25-2.39. From Q2 2010 BASE is
  acquired revenue compounded for two years, not a forecast of the business PepsiCo owned before.
- **The proxy composite** was 1.75 on Q3 2008, 1.45 on Q4 2008 (servings +1%, gross margin -163bp, operating margin -448bp), 2.15
  on Q1 and Q2 2009, 2.45 on Q3 2009 (operating margin +244bp), 2.30 on Q4 2009 (+571bp, servings flat), 1.75 on Q1 2010 (gross
  margin -233bp and operating margin -1,025bp with the acquisition charges, inventories +27%), then 3.05 and 3.10 on Q2 and Q3 2010
  (servings +7% and +8%, net revenue +40%, the inventory gap -20pp and -16pp): the acquired volume and revenue.

How far each call moves the classes (the 104 dates rebuilt with one encoding changed; no outcome consulted):
- the core figures in the history (FY08 $3.68, FY09 $3.71) would change nothing;
- those and the core EPS guides read as points (FY09 $3.88 from 2009-12-09; FY10 $4.16, then $4.12 and $4.10) would change nothing;
- 2010 growth without the acquisitions (3%, the last quarter before them) would change nothing;
- the servings dash read as not reported (scored BASE) would change nothing;
- the SFAS 160 re-presentation not taken as a vintage would change nothing;
- the $0.48 dividend dated from the 8-K of 2010-03-15 would change nothing.

Judgement calls that could carry hindsight:
- the 2008 core rule, which puts FY08 and FY09 in at GAAP (no class moves either way);
- keeping the bottler acquisitions in growth, which makes BASE +38-42%/yr from Q2 2010 (no class moves at 3%);
- reading the SFAS 160 8-K as a vintage, a dash as zero and "increased slightly" as no figure, and the March 2010 dividend
  approval as not yet declared (none moves a class);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2009-2010 went; DURABLE (the class label only).

### PEP 2011-2013: a 53-week year, servings leave the release, the refranchisings, the first RICH dates

```bash
python3 retro/build_pep.py --weekly 2011-01-03 2013-12-31                   # 157 dates, 2011-01-07 .. 2013-12-31
for c in 2012-01-01 2013-01-01 2014-01-01; do python3 retro/tools/firewall.py $c PEP; done
```

The 66 8-Ks, nine 10-Qs and the FY2010-FY2012 10-Ks filed from January 2011 to December 2013 were transcribed by Sonnet 5.5 agents
to a written spec (as for LOW 2011-2012): every figure with the row it comes from, and every guidance, dividend, volume and
53rd-week sentence. 4,648 strings were checked word for word with `verbatim.py` against their own filings (574, 572 and 577 in the
three 10-Ks; 1,222, 639 and 1,064 in each year's releases, 8-Ks and 10-Qs), and 69 more that the fact sheet quotes. The assembler
asserts each print's raw figures against the transcription of its own release and the year-ago quarter's inventories against that
quarter's print, and each vintage against its 10-K; the builder re-derives every signal value. Each source's date comes from EDGAR's
acceptance time. Thresholds, signals and the engine are unchanged; the builder gained one print field (`servings_later`, below).
Decided before any 2011-2013 outcome was computed:

- **Three vintages.** The FY2010 10-K (accepted Friday 2011-02-18 16:57 ET, dated Tuesday 2011-02-22 after Presidents' Day) gives
  2006-2010: the history runs 2001-2010. The FY2011 10-K (2012-02-27 16:50 ET, dated 2012-02-28) gives 2007-2011 and the history
  2002-2011; the FY2012 10-K (2013-02-21 16:46 ET, dated 2013-02-22) gives 2008-2012 and the history 2003-2012. First-year diluted
  shares come from the latest 10-K that reports them: 2001's 1,805M (FY2003), 2002's 1,782M (FY2004), 2003's 1,739M (FY2005). The
  8-Ks of 2011-03-18 and 2011-03-31 recast the 2010 segment data and parts of the FY2010 10-K for the 2011 realignment without
  restating the consolidated statements: a segment recast adds nothing (the ACN 2024-09-30 rule), and the bridge takes the FY2011
  10-K's recast FY10 from that 10-K's date.
- **The option seam leaves the window.** With 2001 as the first year, 2000-2001 (-8.9%, before and after option expensing) is out,
  so from the FY2010 10-K BEAR is 2008's -5.0% ($3.38 to $3.21). XBULL stays the 2001-2003 run (+24.2%/yr) to the FY2011 10-K, then
  2002-2004 (+17.5%/yr), then 2003-2005 (+13.9%/yr) from the FY2012 10-K.
- **FY2010-FY2012 at GAAP (the 2008 core rule):** $3.91, $4.03 and $3.92 from the Q4 prints. Each 10-K's EPS "excluding above items"
  ($4.13, $4.40, $4.10, the releases' core figures) also removes the commodity mark-to-market net impact, so none replaces GAAP.
  GAAP 2010 carries a $0.60 gain on the previously held bottler stakes against $0.61 of merger and inventory charges, GAAP 2011 the
  extra week, GAAP 2012 the productivity-plan charges: all as published.
- **A 53-week year.** Fiscal 2011 ended 2011-12-31 (the last-Saturday rule; the builder's calendar check passes), with a 17-week Q4.
  The extra week stays in the GAAP figures, as published (the LOW and AAPL rule): FY11 EPS $4.03 (the week added $0.04), the Q4 2011
  statements (net revenue +11.0% against 16 weeks) and servings (+7% reported; the release's +4% excluding the week goes in the
  note). The Q4 2011 release's core statement removes the week from net revenue ($19,535M against $20,158M), but a core statement
  does not replace GAAP even where, as for net revenue, the week is its only adjustment (the 2009-2010 margins rule). Growth
  excluding currency is stated only on that basis, so `lc_pct` takes it: 9% ("an extra reporting week increased reported net revenue
  by 3 percentage points"). The Q4 2012 print compares 16 weeks with 17, as published.
- **No guide gives a field.** 2011: "7 to 8 percent on a 52-week, core constant currency basis" from core $4.13, then
  "high-single-digit" core EPS growth from the Q2 2011 release; 2012: a core constant currency EPS decline "of approximately 5
  percent from its fiscal 2011 core EPS of $4.40"; 2013: "7 percent core constant currency EPS growth versus its fiscal 2012 core
  EPS of $4.10". All are on the core basis (the 2008 core rule). The revenue outlooks are words ("mid-single-digit",
  "low-single-digits", organic "mid-single-digits"), so no `rev_guide` this time. Each reiteration 8-K (CAGNY, CAGE, Goldman Sachs,
  Deutsche Bank, Barclays, Bernstein, the July 2013 prepared remarks) shows as the latest guide from its date. The last full year's
  EPS stands (the rollover rule): FY09's $3.77 to 2011-02-04, FY10's $3.91 from the Q4 2010 print, FY11's $4.03 from 2012-02-10,
  FY12's $3.92 from 2013-02-15.
- **Growth excluding currency: the stated figure, else reported less the stated currency effect** (the NKE rule). Core constant
  currency +37% (Q4 2010), +26%, +11% and +10% (2011), +9% (Q4 2011), +5%, +1% and "—" (zero) in Q1-Q3 2012. From Q4 2012 the
  releases state only reported and organic growth, so `lc_pct` is reported growth less the currency effect the release states, as
  for Q4 2008: -0.5% (Q4 2012: -1% and "less than a 1 percent unfavorable impact", 0.5 points in its organic table), +1.5%, +3.5%
  and +2.5% (Q1-Q3 2013). Acquisitions (the bottlers' first two months in Q1 2011, Wimm-Bill-Dann from February 2011), the
  refranchisings in China, Mexico and Vietnam (2012-2013) and the prior year's extra week stay in, as published (the AVGO rule, as
  in 2010). Organic growth, which removes them, is not used.
- **Servings leave the release.** From Q3 2012 the releases give snack and beverage volume but no total servings. A measure that
  leaves the release enters from the first filing that states it, on that filing's own date (the NKE futures rule; it can only lag),
  through a new print field, `servings_later`: Q3 2012 +4% (the 10-Q, accepted 2012-10-17 17:09 ET, dated 2012-10-18), Q1 2013 +3%
  (the 10-Q, 2013-04-19 16:17 ET, dated 2013-04-22), Q2 2013 +4% (the prepared remarks furnished by an 8-K at 10:52 ET on the
  release day, 2013-07-24: "Our overall servings increased 4 percent"), Q3 2013 +1% (the 10-Q, dated 2013-10-17). Until then the
  slot has no value (the AAPL Mac-unit rule): on 2013-04-19 for Q1 2013. No filing states Q4 2012's total servings, so that slot
  stays empty, and the franchise line shows the FY2012 10-K's +3% for the year from its date.
- **Dividends,** the latest declared rate: $0.515 a quarter from the 8-K of 2011-05-09 (17:21 ET, dated 2011-05-10: "declared a
  seven percent increase in the company’s annual dividend, from the current annual rate of $1.92 to $2.06 per share"), $0.5375 from
  the 8-K of 2012-05-04 (dated 2012-05-07; declared May 1), $0.5675 from the 8-K of 2013-05-06 (dated 2013-05-07; declared April
  30). The increases announced with the Q4 2011 and Q4 2012 results (to $2.15 and $2.27, "effective with the dividend payable in
  June") were announcements, not declarations (the AAPL 2012 rule, as for March 2010).
- **Calendar.** Every release came before the open (07:36-08:01 ET), so the weeks' dates are the next trading days: 2011-02-11,
  2011-04-29, 2011-07-22, 2011-10-13, 2012-02-10, 2012-04-27, 2012-07-26, 2012-10-18, 2013-02-15, 2013-04-19, 2013-07-25 and
  2013-10-17. An 8-K at 08:44 ET on 2013-07-24 moved that day's call to 9 a.m.
- **Durability is unchanged:** DURABLE, risk 2, with each 10-K's own words (FY2011: "a leading global food and beverage company with
  hundreds of brands that are respected household names throughout the world"; FY2012: "In many countries in which we do business,
  The Coca-Cola Company is our primary beverage competitor"). No theme in the registry is live for PepsiCo in 2011-2013.
- **Adds nothing:** the Wimm-Bill-Dann 8-Ks (2011-01-27, 2011-02-04, 2011-03-10, 2011-06-06), the 2011 segment recasts, the officer,
  director, by-law and annual-meeting 8-Ks, the note offerings and credit agreements, the Tingyi alliance (2011-11-04, completed
  2012-04-02), the 2012 productivity plan (item 2.05 of 2012-02-09: charges and savings, no guided EPS or revenue figure), the FDA
  clarification (2013-02-14), the call-time 8-K (2013-07-24, 08:44 ET), the redemption notice (2013-07-25), the CEO statement of
  2013-08-19, and the 10-Qs beyond their servings.

Controls: altering one value of each print, vintage, guide, dividend and `servings_later` published from 2010-12-01 changes no date
before its publication and changes the first weekly date on or after it (44 of 44). No string of any print, vintage, guide,
dividend, `servings_later` or source appears in a model dated before it (53,167 checks over the 314 PEP models). The firewall at
2012-01-01, 2013-01-01 and 2014-01-01 changes no model before its cutoff (209, 261 and 314 dates). The 157 dates of 2008-2010
rebuild byte-identical, and no file shared with another ticker changed.

Seen in the build (method behaviour, not tuned):
- **CHEAP on 107 of 157 dates, RICH on 50;** BUY on 111, AVOID on 26, WATCHLIST on 18, ACCUMULATE on 2. By year: CHEAP and BUY on
  all 52 dates of 2011; CHEAP on 49 of 2012 and RICH on 3 (2012-08-03, 2012-08-17 and 2012-08-24, still BUY); in 2013 CHEAP on the 6
  dates to 2013-02-08 and RICH on the 47 from 2013-02-15. The tier agrees on 5 to 8 of the 8 robustness variants (5 or 6 on 34
  dates, all in 2013), the valuation verdict on 3 to 8.
- **EPS anchors on the last full year:** FY09's $3.77 to 2011-02-04 (16.9-17.7x, the 14th-22nd percentile), FY10's $3.91 to
  2012-02-03 (15.3-18.2x, the 7th-29th), FY11's $4.03 to 2013-02-08 (15.5-18.2x, the 9th-42nd) and FY12's $3.92 from 2013-02-15
  (18.8-22.0x, the 45th-87th, at $73.68-86.41): FY12's EPS fell 2.7% while the price rose.
- **The EPP floor fell with the window:** 18x to the end of 2012 ($67.86 on FY09's EPS, $70.38 on FY10's, $72.54 on FY11's), 17x
  from 2013-01-04 ($68.51, then $66.64 on FY12's) and 16x on 2013-12-31 ($62.72), as the 2008-2012 lows (12.2-15.9x) filled the ten
  calendar years. The price was above the floor on 58 dates, every date from 2013-02-15 (by 10.6% to 32.2%).
- **BEAR** is -8.9%/yr to 2011-02-18 and -5.0%/yr from the FY2010 10-K. **BULL** is the window's EPS CAGR: +12.7%/yr (2001-2010),
  +11.7% (2001-2011, from the Q4 2011 print), +10.2% (2002-2011), +8.8% (2002-2012, from the Q4 2012 print) and +7.5% (2003-2012),
  floored at BASE to Q1 2011.
- **BASE followed the quarter's growth plus the buyback** (+1.0% to +1.3%/yr): +42.4% and +38.0-38.3%/yr with the bottlers (Q3 and
  Q4 2010), +27.3% (Q1 2011), +12.3% and +11.3% (Q2, Q3 2011), +10.2% (Q4 2011), then +6.2%, +2.2% and +1.2% (Q1-Q3 2012, the
  refranchisings in them), +0.7% and +0.6% (Q4 2012, before and after the FY2012 10-K), and +2.6%, +4.6% and +3.6% (2013). The
  adjusted gap went from +2.1 to +2.6 (to July 2011) to +0.6 to +1.3 (to April 2012), -0.7 to +0.3 (the rest of 2012) and -1.7 to
  -0.7 (2013).
- **The proxy composite** was 3.10 on Q3 2010, 2.90 on Q4 2010 and 3.55 on Q1 2011 (servings +9%, net revenue +27-37% with the
  acquisitions), 2.30 and 1.95 on Q2 and Q3 2011 (gross margin -175bp and -290bp), 2.50 on Q4 2011 (servings +7% with the extra
  week), 1.60 and 1.80 on Q1 and Q2 2012 (servings +2%), 2.35 on Q3 2012 (servings +4% from the 10-Q, gross margin +103bp), 2.15 on
  Q4 2012 (no servings), 2.35 then 2.15 on Q1 2013 (the 10-Q's +3% scores BEAR: an empty slot scores BASE), 2.65 on Q2 2013
  (operating margin +263bp) and 2.15 on Q3 2013 (servings +1%).

How far each call moves the classes (the 157 dates rebuilt with one encoding changed; no outcome consulted):
- FY11 without the extra week ($3.99, the stated $0.04 taken out: a derived figure, as a test only) would change 3 classes (CHEAP to
  RICH on 2012-08-10, 2012-08-31 and 2012-09-07) and no tier;
- Q4 2011 growth with the extra week in (reported 11% less the 1.5-point currency effect, 12.5%) would change nothing;
- Q4 2011 servings without the extra week (the release's core +4%) would change nothing;
- the stated organic growth from Q2 2012 (the refranchisings out: 5%, 5%, 5%, 4%, 4% and 3%) would change nothing;
- servings from the releases only (no `servings_later`) would change nothing;
- the dividends dated from the announcements (2012-02-09, 2013-02-14) would change nothing;
- the core figures in the history (FY10 $4.13, FY11 $4.40, FY12 $4.10) would change 4 classes (RICH to CHEAP on 2012-08-03,
  2012-08-17, 2012-08-24 and 2013-02-15) and 13 tiers in 2013 (AVOID to WATCHLIST, WATCHLIST to ACCUMULATE);
- those and the core EPS guides read as points (FY11 $4.44, FY12 $4.18, FY13 $4.39) would change 17 classes (RICH to CHEAP or FAIR:
  the three August 2012 dates, 2013-02-15 to 2013-03-15 and 2013-08-16 to 2013-10-11) and 46 tiers (every date from 2013-02-22:
  AVOID to WATCHLIST or ACCUMULATE, WATCHLIST to ACCUMULATE or BUY, ACCUMULATE to BUY).

Judgement calls that could carry hindsight:
- the 2008 core rule, which keeps FY10-FY12 at GAAP (4 classes and 13 tiers, 17 and 46 with the core guides as points: the call that
  moves the most in this range);
- the extra week: in the GAAP figures and servings as published, out of `lc_pct` because the release states it so; FY11 at $4.03 (3
  classes if the week were taken out of FY11);
- keeping the refranchisings in growth, which puts BASE at +0.6% to +2.2%/yr from mid-2012 against organic growth of 4-5% (no class
  moves);
- `servings_later` (a new field, from the NKE rule) and Q4 2012's empty slot (no class moves);
- dating dividends from their declarations (no class moves);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2011-2013 went; DURABLE (the class label only).

### PEP 2014-2016: the Venezuela charges at GAAP, servings only in the 10-Qs, new segments, RICH on 154 of 156 dates

```bash
python3 retro/build_pep.py --weekly 2014-01-06 2016-12-31                   # 156 dates, 2014-01-10 .. 2016-12-30
for c in 2015-01-01 2016-01-01 2016-02-15 2017-01-01; do python3 retro/tools/firewall.py $c PEP; done
```

The 51 8-Ks, nine 10-Qs and the FY2013-FY2015 10-Ks filed from January 2014 to December 2016 were transcribed by agents on the
cheaper model (see "Which model to run it on") to the written spec of 2011-2013: every figure with the row it comes from, and every
guidance, dividend, servings, Venezuela and productivity sentence. 4,762 strings were checked word for word with `verbatim.py`
against their own filings (229, 194 and 282 in the three 10-Ks; 1,378, 1,412 and 1,267 in each year's releases, 8-Ks and 10-Qs),
and 63 more that the fact sheet quotes. The assembler asserts each print's raw figures against the transcription of its own release
and the year-ago quarter's inventories against that quarter's print, and each vintage against its 10-K; the builder re-derives every
signal value. Each source's date comes from EDGAR's acceptance time. Thresholds, signals, the builder and the engine are unchanged;
the firewall's PEP branch also plants a later `servings_later` (below). Decided before any 2014-2016 outcome was computed:

- **Three vintages.** The FY2013 10-K (accepted Friday 2014-02-14 16:26 ET, dated Tuesday 2014-02-18 after Presidents' Day) gives
  2009-2013 and the history 2004-2013; the FY2014 10-K (2015-02-12 17:01 ET, dated 2015-02-13) gives 2010-2014 and the history
  2005-2014; the FY2015 10-K (2016-02-11 16:40 ET, dated 2016-02-12) gives 2011-2015 and the history 2006-2015. First-year diluted
  shares come from the latest 10-K that reports them: 2004's 1,729M (FY2006), 2005's 1,706M (FY2007), 2006's 1,687M (FY2008).
- **FY2013-FY2015 at GAAP (the 2008 core rule):** $4.32, $4.27 and $3.67 from the Q4 prints. Each year's core figure ($4.37, $4.63,
  $4.57: the 10-Ks' EPS "excluding above items") also removes the commodity mark-to-market net impact, so none replaces GAAP. GAAP
  2015 carries the Venezuela impairment charges ($1.4 billion, $0.91 a share, in Q3 2015, when PepsiCo deconsolidated its Venezuelan
  subsidiaries "effective as of the end of the third quarter of 2015"), as published, as GAAP 2014 carries the productivity-plan
  charges, a Venezuela remeasurement ($0.07 a share) and a pension settlement ($0.06). So BEAR, the window's worst year, is 2008's
  -5.0% to 2016-02-05 and 2015's -14.1% ($4.27 to $3.67) from the Q4 2015 print.
- **No guide gives a field.** 2014: "7 percent core constant currency EPS growth in 2014 versus its fiscal 2013 core EPS of $4.37",
  raised to 8 percent (Q2 2014) and 9 percent (Q3 2014); 2015: 7 percent "versus its fiscal 2014 core EPS of $4.63", raised to 8
  and 9 percent; 2016: "core earnings per share of $4.66", then $4.71 (Q2 2016) and $4.78 (Q3 2016). All are on the core basis (the
  2008 core rule). The revenue outlooks for 2014 and 2015 are words (organic "mid-single digits"). 2016's is a figure, "organic
  revenue growth of approximately 4 percent, excluding the impact of the 53rd week", but organic growth removes acquisitions,
  divestitures, currency and the extra week, so it is not the measure the method uses (as for the prints, below): display only. The
  Barclays reiteration 8-Ks (2014-09-02, 2015-09-08, 2016-09-06, each after the close) show as the latest guide from the next day.
  The last full year's EPS stands (the rollover rule): FY12's $3.92 to 2014-02-07, FY13's $4.32 from 2014-02-14, FY14's $4.27 from
  2015-02-12, FY15's $3.67 from 2016-02-12.
- **Growth excluding currency: reported growth less the stated currency effect** (the NKE rule, as from Q4 2012: no release states
  constant currency growth). +4% (Q4 2013: +1% and 3 points), +3%, +3.5% and +3% (Q1-Q3 2014: "even", +0.5% and +2% against 3, 3
  and 1 points), +5% (Q4 2014: -1% and 6), +5%, +4% and +7% (Q1-Q3 2015: -3%, -6% and -5% against 8, 10 and 12 points), +1% (Q4
  2015: -7% and 8), +1.5%, +0.7% and +1.1% (Q1-Q3 2016: -3%, -3.3% and -1.9% against 4.5, 4 and 3 points). The Vietnam
  refranchising (Q4 2013), the structural changes and divestitures of 2014-2015 and the Venezuela deconsolidation (2 to 3 points a
  quarter from Q4 2015) stay in, as published (the AVGO rule, as in 2010-2013). Organic growth (+3% to +7.4%), which removes them,
  is not used.
- **Servings only in the 10-Qs.** No release of 2014-2016 states total servings. Each 10-Q does, on the evening of its release day
  (16:09-16:25 ET), so `servings_later` takes it from the next trading day (the NKE futures rule): +1% for Q1, Q2 and Q3 2014,
  Q1 and Q3 2015, +2% for Q1 and Q2 2016, +3% for Q3 2016 ("increased 3% and 2.5%, respectively": the quarter's figure). The Q2
  2015 10-Q says "total servings increased slightly": words, which are not figures, so that slot stays empty (the AAPL Mac-unit
  rule: an empty slot scores BASE). No filing states a fourth quarter's total servings, so those slots stay empty too, and the
  franchise line shows each 10-K's figure for the year from its date (+2% for 2013, +1% for 2014 and 2015).
- **Dividends,** the latest declared rate: $0.5675 a quarter to 2014-05-12; $0.655 from the 8-K of 2014-05-12 (16:40 ET, dated
  2014-05-13: "On May 6, 2014 the Board of Directors of PepsiCo declared a quarterly dividend of $0.655 per share payable on June
  30, 2014"); $0.7025 from the Q2 2015 release (2015-07-09: "Cash dividends declared per common share | 0.7025 | 0.655") and
  $0.7525 from the Q2 2016 release (2016-07-07), as no 8-K of 2015 or 2016 states a declaration. The increases announced with each
  year's Q4 results ("annualized dividend raised 15 percent to $2.62 per share" on 2014-02-13, then 2015-02-11 and 2016-02-11)
  were announcements, not declarations (the AAPL 2012 rule, as for 2010-2013). The 8-K of 2014-02-07 declares the existing $0.5675.
- **New segments, a reclassified cost of sales.** From Q3 2015 PepsiCo reports North America Beverages, Latin America, Europe
  Sub-Saharan Africa and Asia, Middle East and North Africa in place of PepsiCo Americas Beverages, Latin America Foods, Europe and
  Asia, Middle East & Africa (announced 2015-07-08). The 8-K of 2015-08-06 (recast segment schedules) and the 8-K of 2015-10-07 (the
  FY2014 10-K's business, MD&A and statements re-filed with the segment notes revised; the consolidated statements "as previously
  reported") add nothing (a segment recast, the ACN 2024-09-30 rule); the FY2015 10-K's business line and groups use the new
  segments from its date. From Q1 2016 the releases move "certain functional support costs associated with the manufacturing and
  production of our products" from selling, general and administrative expenses into cost of sales and restate the prior year to
  match, so each print's gross margin change compares the two years as that release states them (FY15's own gross margin stays as
  the Q4 2015 release states it).
- **A 53-week year ahead.** Fiscal 2016 ends on 2016-12-31 with 53 weeks (the last-Saturday rule); its fourth quarter, with the
  extra week, is printed in February 2017, after this range. Here the extra week shows only in the 2016 guide's words.
- **Calendar.** Every release came before the open (06:35-07:31 ET), so the weeks' dates are the next trading days: 2014-02-14,
  2014-07-24, 2014-10-10, 2015-02-12, 2015-04-24, 2015-07-10, 2015-10-07, 2016-02-12, 2016-04-19, 2016-07-08 and 2016-09-30. The
  Q1 2014 release came on Thursday 2014-04-17, before Good Friday, so that week's date is the release day itself (it counts from the
  open), and the 10-Q filed that evening counts from Monday 2014-04-21: its +1% enters on 2014-04-25.
- **Durability is unchanged:** DURABLE, risk 2, with each 10-K's own words (FY2013: "a leading global food and beverage company with
  brands that are respected household names throughout the world"; FY2014 and FY2015: "with a complementary portfolio of enjoyable
  brands, including Frito-Lay, Gatorade, Pepsi-Cola, Quaker and Tropicana"; FY2015: "In 2015, we and The Coca-Cola Company
  represented approximately 24% and 20%, respectively, of the U.S. liquid refreshment beverage category"). No theme in the registry
  is live for PepsiCo in 2014-2016.
- **Adds nothing:** the letter to Trian Partners rejecting a separation of the snacks and beverage businesses (7.01 of 2014-02-27:
  no figure), the 2014 Productivity Plan (2.05 and 2.06 of 2014-02-13: about $990 million of charges, no guided EPS or revenue
  figure), the officer, director, compensation, by-law (proxy access, 2016-01-11) and annual-meeting 8-Ks, the note offerings and
  the 2016 redemption, the credit agreements, the leadership changes and the segment realignment (2015-07-08, 2016-03-30), the
  segment recasts (2015-08-06, 2015-10-07), and the 10-Qs beyond their servings.

Controls: altering one value of each print, vintage, guide, dividend and `servings_later` published from 2013-12-01 changes no date
before its publication and changes the first weekly date on or after it (42 of 42). No string of any print, vintage, guide,
dividend, `servings_later` or source appears in a model dated before it (124,652 checks over the 470 PEP models). The firewall at
2015-01-01, 2016-01-01, 2016-02-15 and 2017-01-01 changes no model before its cutoff (365, 418, 424 and 470 dates); the extra
2016-02-15 cutoff is the one where the new `servings_later` plant fires (the last print before it, Q4 2015, has no total servings;
at the year-end cutoffs a 10-Q had already stated the last print's). The 314 dates of 2008-2013 rebuild byte-identical. Beyond the
156 new entries in the index, the only file shared with another ticker that changed is the firewall (the PEP plant, and
`servings_later` dropped from its planted print, a field no other ticker has).

Seen in the build (method behaviour, not tuned):
- **RICH on 154 of 156 dates, CHEAP on 2;** AVOID on 139, WATCHLIST on 9, ACCUMULATE on 6, BUY on 2. CHEAP and BUY only on
  2014-02-14 and 2014-02-21, the two weeks after FY13's $4.32 replaced FY12's $3.92 (18.1x, the 43rd percentile); ACCUMULATE from
  2014-02-28 to 2014-04-04; WATCHLIST on 2014-01-31, 2014-02-07 and from 2014-04-11 to 2014-05-23; AVOID on the first three dates
  and every date from 2014-05-30. By year: 49 RICH and 2 CHEAP in 2014, RICH on all 53 dates of 2015 and all 52 of 2016. The tier
  agrees on 4 to 8 of the 8 robustness variants (8 on 121 dates), the valuation verdict on 1 to 8 (8 on 147).
- **EPS anchors on the last full year:** FY12's $3.92 to 2014-02-07 (20.5-21.3x, the 63rd-79th percentile), FY13's $4.32 to
  2015-02-06 (18.1-23.2x, the 43rd-99th, at $78.09-100.10), FY14's $4.27 to 2016-02-05 (21.3-24.0x, the 78th-100th) and FY15's
  $3.67 from 2016-02-12 (26.8-29.9x, the 92nd-100th, at $98.36-109.66): GAAP EPS fell 14.1% with the Venezuela charges while the
  price rose.
- **The EPP floor:** 17x on FY12's EPS ($66.64) to 2014-02-07 and 16x from 2014-02-14 ($69.12 on FY13's, $68.32 on FY14's, $58.72
  on FY15's), with 15x on the last date of 2015 and of 2016 ($64.05, $55.05), when the window holds ten full calendar years and the
  median falls between two lows. The price was above the floor on every date, by 13.0% (2014-02-14) to 90.1% (2016-12-30).
- **BULL** is the window's EPS CAGR: +7.5%/yr (2003-2012) to 2014-02-07, +7.7% (2003-2013, from the Q4 2013 print), +7.2%
  (2004-2013, from the FY2013 10-K), +6.3% (2004-2014, from the Q4 2014 print), +5.4% (2005-2014, from the FY2014 10-K) and +2.3%
  (2006-2015, from the FY2015 10-K), floored at BASE on 74 dates (2015-02-12 to 2015-07-02, 2015-10-07 to 2016-07-01, and from
  2016-09-30). **XBULL** is +13.9%/yr (2003-2005) to 2014-02-14, +13.7% (2004-2006) from the FY2013 10-K, +12.7% (2005-2007) from
  the FY2014 10-K and +10.4% (2008-2010) from the FY2015 10-K. The price stood above the BULL value ($82-85) on every date from
  2016-02-12, and on 2015-02-12.
- **BASE followed the quarter's growth plus the buyback** (+1.1 to +1.4 points): +3.6%/yr (Q3 2013) to 2014-02-07, +5.1% (Q4
  2013), +4.1%, +4.6% and +4.1% (Q1-Q3 2014), +6.3% and +6.2% (Q4 2014, before and after the FY2014 10-K), +6.2%, +5.2% and +8.2%
  (Q1-Q3 2015), +2.4% (Q4 2015), and +2.9%, +2.1% and +2.5% (Q1-Q3 2016), the Venezuela deconsolidation in each 2016 figure. The
  adjusted gap was -1.51 to -1.72 to 2014-02-07, -0.29 to -0.85 from 2014-02-14 to 2014-04-11, -1.04 to -2.05 from then to
  2016-02-05, and -1.18 to -1.58 from 2016-02-12.
- **The proxy composite** was 2.15 on Q3 2013, 2.50 on Q4 2013 and the Q1 2014 release (gross margin +84bp, operating margin +83bp
  and +114bp, the servings slot empty), 2.30 from 2014-04-25 (the 10-Q's servings +1%), 2.00 on Q2 and Q3 2014 (servings +1%), 2.20
  on Q4 2014 (operating margin -174bp, no servings), 2.15 on Q1 2015 (servings +1%), 2.35 on Q2 2015 (servings "slightly": an empty
  slot), 2.00 on Q3 2015 (operating margin -786bp with the Venezuela charges), 2.70 on Q4 2015 (gross margin +185bp, operating
  margin +187bp, no servings), 2.35 on Q1 2016 (servings +2%) and 2.30 on Q2 and Q3 2016 (servings +2% and +3%; operating margin
  +104bp and +893bp, the latter against the charges).

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- FY15 without the Venezuela charges ($4.58: $3.67 plus the stated $0.91, a derived figure, as a test only) would change nothing;
- the 2016 organic revenue guide (about 4%) as a fiscal-year revenue guide would change nothing;
- the stated organic growth for every print (+3% to +7.4%: the Venezuela deconsolidation, refranchisings and divestitures out) would
  change nothing;
- servings from the releases only (no `servings_later`) would change nothing;
- the dividends dated from the announcements (2014-02-13, 2015-02-11, 2016-02-11) would change nothing;
- the core figures in the history (FY13 $4.37, FY14 $4.63, FY15 $4.57) would change no class and 8 tiers (AVOID to WATCHLIST,
  WATCHLIST to ACCUMULATE, on 2014-04-11, 2014-05-30 to 2014-06-13, 2014-08-01, 2015-09-04, 2015-09-11 and 2016-01-15);
- those and the core EPS guides read as points (FY14 $4.68-4.76, FY15 $4.95-5.05, FY16 $4.66-4.78) would change 7 classes (RICH to
  CHEAP, 2014-02-28 to 2014-04-11) and 79 tiers, all before 2016-02-12 (AVOID to WATCHLIST or ACCUMULATE, WATCHLIST to ACCUMULATE
  or BUY, ACCUMULATE to BUY); no date from 2016-02-12 moves.

Judgement calls that could carry hindsight:
- the 2008 core rule, which keeps FY13-FY15 at GAAP, the Venezuela charges in FY15 (8 tiers with the core history; 7 classes and 79
  tiers with the core guides as points: the call that moves the most in this range);
- keeping the Venezuela deconsolidation, refranchisings and divestitures in growth, which puts BASE at +2.1% to +2.9%/yr in 2016
  against organic growth of 3.3-4.2% (no class moves), and the 2016 organic revenue guide as display only (no class moves);
- `servings_later` from the 10-Qs, Q2 2015's "slightly" as an empty slot, and the empty fourth quarters (no class moves);
- dating dividends from their declarations (no class moves);
- the segment recasts adding nothing, and each 2016 print's gross margin change on its release's reclassified basis (not tested: the
  release states no other basis for both years);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2014-2016 went; DURABLE (the class label only).

### PEP 2017-2020: the Tax Act years at GAAP, servings from the 10-Qs, Nasdaq, e-commerce on the watch list, a CHEAP year from FY2018's tax benefits

```bash
python3 retro/build_pep.py --weekly 2017-01-02 2020-12-31                   # 209 dates, 2017-01-06 .. 2020-12-31
for c in 2017-02-20 2018-01-01 2018-02-20 2019-01-01 2019-02-20 2020-01-01 2020-02-20 2021-01-01; do python3 retro/tools/firewall.py $c PEP; done
```

The 62 8-Ks (one an 8-K/A), twelve 10-Qs and four 10-Ks filed from October 2016 to December 2020 were listed from EDGAR with their
acceptance times; every 8-K's items were read for guides, figures and dividend rates, and the sixteen releases, the 10-Qs' servings
and dividend notes and the FY2016-FY2019 10-Ks were transcribed by Opus directly, each figure typed and then asserted by script against
the parsed table of its own filing (the print's quarter, the Q4 releases' full year, each 10-K's statements, segments and cash flow).
366 strings were checked word for word with `verbatim.py` against their own filings. Each source's date comes from EDGAR's acceptance
time. Thresholds, signals and the engine are unchanged; the builder gained two encodings that change no earlier output (the e-commerce
watch list and the listing, below), the firewall's PEP branch also plants a later listing, and SodaStream joins the anachronism list
(no model of any ticker names it before 2020-02-14). Decided before any 2017-2020 outcome was computed:

- **Four vintages.** The FY2016 10-K (accepted 2017-02-15 16:35 ET, dated 2017-02-16) gives 2012-2016 and the history 2007-2016; the
  FY2017 10-K (2018-02-13 16:32 ET, dated 2018-02-14) gives 2013-2017 and the history 2008-2017; the FY2018 10-K (Friday 2019-02-15
  16:23 ET, dated Tuesday 2019-02-19 after Presidents' Day) gives 2014-2018 and the history 2009-2018; the FY2019 10-K (2020-02-13 06:09
  ET, before the open and two minutes before the Q4 2019 release) gives 2015-2019 and the history 2010-2019, so the Q4 2019 print's
  full year never extends a history. First-year diluted shares come from the latest 10-K that reports them: 2007's 1,658M (FY2009),
  2008's 1,602M (FY2010), 2009's 1,577M (FY2011), 2010's 1,614M (FY2012). No 10-K restates an earlier year's EPS or net revenue.
- **FY2016-FY2019 at GAAP (the 2008 core rule):** $4.36, $3.38, $8.78 and $5.20 from the Q4 prints. Each 10-K's EPS "excluding above
  items" ($4.85, $5.23, $5.66, $5.53, the releases' core figures) also removes the commodity mark-to-market net impact, so none
  replaces GAAP. GAAP 2016 is a 53-week year as published (the extra week added $0.04, FY2016 10-K). GAAP 2017 carries the provisional
  net tax expense of the TCJ Act ($2,451 million, $1.70 a share; $1.73 on the fourth quarter's shares): the AAPL FY2002 test is not met
  ($2.7 billion of listed charges against $4.9 billion of net income). GAAP 2018 carries "other net tax benefits" of $5,064 million
  ($3.55 a share, the reorganization of the international operations) and the TCJ Act's $28 million: the mirror test of method r2
  (listed one-off benefits larger than the year's income without them) is not met ($5.3 billion of listed benefits, with the
  refranchising and asset-sale gains, against $7.2 billion), so the year stays in, at GAAP. So BEAR, the window's worst year, is 2015's
  -14.1% to 2018-02-09, 2017's -22.5% ($4.36 to $3.38) from the Q4 2017 print and 2019's -40.8% ($8.78 to $5.20) from the Q4 2019
  print, and XBULL is 2016-2018's +41.9%/yr from the Q4 2018 print. The vintages' tax rates are as published (FY17 48.9%, FY18 -36.7%):
  they reach only the display-only EPS check.
- **No guide gives a field.** 2017: "The Company expects 2017 organic revenue growth of at least 3 percent" and "core earnings per
  share of $5.09", then $5.13 (Q2 2017) and $5.23 (Q3 2017, with organic growth "to approximate our year-to-date growth rate"); 2018:
  core EPS of $5.70, then $5.65 (Q3 2018), with organic growth "at least in line with the 2017 growth rate", then "at least 3 percent";
  2019: organic growth "to be 4 percent" and an implied core EPS of $5.50, the Q3 2019 release expecting "to meet or exceed" the 4
  percent; 2020: organic growth of 4 percent and an implied core EPS of $5.88. The EPS figures are on the core basis (the 2008 core
  rule); the revenue figures are organic, which removes acquisitions, divestitures, currency and the extra week, so they are not the
  measure the method uses (as for the prints, and the 2016 guide): display only. The Q4 2018 release's long-term targets (4 to 6
  percent organic revenue growth, core operating margin expansion of 20 to 30 basis points) are later years' targets on those bases,
  with no input (the UNP 2018 rule). The Q1 2020 release: "the Company's previous financial outlook regarding fiscal year 2020 is no
  longer applicable"; the Q2 2020 release repeats it; the Q3 2020 release (dated 2020-10-01) expects organic growth of "approximately 4
  percent" and core EPS of $5.50. A withdrawal of guides that gave no field changes no input. No reiteration 8-K was filed in these
  years. The last full year's EPS stands (the rollover rule): FY15's $3.67 to 2017-02-10, FY16's $4.36 from 2017-02-16, FY17's $3.38
  from 2018-02-14, FY18's $8.78 from 2019-02-15, FY19's $5.20 from 2020-02-14.
- **Growth excluding currency: reported growth less the stated currency effect** (the NKE rule, as from Q4 2012), both from the table
  that opens each release ("Net revenue change/growth/performance" and "Foreign exchange impact on net revenue"); a "—%" or "even" is
  0% (the Q1 2014 rule). +7.0% (Q4 2016: +5.0% and 2 points; the 53rd week's 3.5 points in), +2.6%, +3.5% and +2.3% (Q1-Q3 2017), -1.0%
  (Q4 2017: even, with 1 point of favorable currency; 16 weeks against 17), +2.3%, +1.4% and +3.5% (2018), +4.0% (Q4
  2018: even against 4 points), +5.6%, +5.2% and +5.3% (2019), +5.7% (Q4 2019, no currency effect), +7.7%, +0.9% and +7.3% (Q1-Q3 2020:
  +7.7%, -3.1% against 4 points, +5.3% against 2). The 53rd week, divestitures, SodaStream (from December 2018) and the 2020
  acquisitions stay in, as published (the AVGO rule, as in 2010-2016). Organic growth (-0.3% to +7.9%), which removes them, is not used.
- **Servings from the 10-Qs.** No release of 2017-2020 states total servings; each 10-Q does, so `servings_later` takes it: +0.5% (Q1
  2017), 0% for Q2 and Q3 2017 ("total servings was even with the prior year", read as 0%: the Q1 2014 "even" rule), +1%, +1% and +3%
  (2018), +4%, +3% and +4% (2019), +6%, +1% and +13% (2020: "which reflects the impact of the revised guidelines on our prior-year
  servings", the FDA's 12-ounce serving for most beverages from 2020-01-01 applied to both years; Q3 "primarily reflecting the contributions from
  our recent acquisitions"), all as published. The 10-Qs of 2017-2018 came after the close and count from the next trading day; from
  2019 each 10-Q was accepted minutes before its release (06:03-06:07 ET), so its servings arrive with the print; Q3 2020's came after
  the close with the release. No filing states a fourth quarter's total servings, so those slots stay empty (the AAPL Mac-unit rule),
  and the franchise line shows each 10-K's figure for the year from its date: +3% for 2016 (+2% without the extra week), -1% for 2017,
  +1% for 2018, +4% for 2019 ("primarily reflecting our acquisition of SodaStream").
- **Dividends,** the latest declared rate: $0.7525 a quarter to 2017-07-10; $0.805 from the Q2 2017 release (2017-07-11) and $0.9275
  from the Q2 2018 release (2018-07-10), each "Cash dividends declared per common share"; $0.955 from the Q2 2019 10-Q and $1.0225 from
  the Q2 2020 10-Q ("Cash dividends declared per common share were $0.955 and $0.9275 for the 12 weeks ended June 15, 2019 and June 16,
  2018, respectively"), each accepted minutes before that morning's release: the 2019 and 2020 releases state no dividend per share,
  and no 8-K of 2017-2020 states a declaration. The increases announced with each year's Q4 results (to $3.22, $3.71, $3.82 and $4.09
  annualized, "effective with the dividend expected to be paid in June") were announcements (the AAPL 2012 rule, as for 2010-2016).
- **The non-service pension cost.** From Q1 2018 PepsiCo presents the non-service components of pension cost below operating profit
  (ASU 2017-07) and each 2018 release recasts the prior-year quarter, so each print's operating margin change compares the two years
  as its release states them (the 2016 cost-of-sales rule, which also covers the Q4 2016 release's reclassified 2015 cost of sales).
  The 8-K of 2018-02-27 (the recast quarterly operating profit of 2016 and 2017) "does not revise or restate PepsiCo's previously
  reported consolidated financial statements": it adds nothing (the ACN 2024-09-30 rule, as for the 2008 segment recasts); the FY2017 vintage keeps the 10-K's
  $10,509 million until the FY2018 10-K. Net revenue is never recast.
- **Segments.** Six through the FY2018 10-K (North America Beverages is "PepsiCo Beverages North America" in the 2019 releases); the
  FY2019 10-K realigns Europe Sub-Saharan Africa and Asia, Middle East and North Africa into Europe, Africa, Middle East and South Asia,
  and Asia Pacific, Australia and New Zealand and China region "during the fourth quarter of 2019": each vintage's bridge and business
  line take its own 10-K's segments.
- **E-commerce on the watch list from 2018-02-14.** ECOMMERCE (live from 2015-01-01) is scoped to e-commerce displacing physical
  retail, grocery and distribution. The FY2014-FY2016 10-Ks name e-commerce only among the channels larger retailers might use ("other
  distribution channels such as e-commerce ... the competitive advantages we derive from our go-to-market systems and brand equity may
  be eroded"), under a heading about "changes to the retail landscape". The FY2017 10-K is the first whose risk-factor heading names it:
  "The loss of, or a significant reduction in sales to, any key customer or disruption in the retail landscape, including rapid growth
  in hard discounters and the e-commerce channel, could adversely affect our business, financial condition or results of operations."
  So PEP carries ECOMMERCE on the watch list from that 10-K's date, company-acknowledged, with no market read (the NKE and LOW rule),
  each 10-K's wording replacing the last (FY2018: a heading of its own; FY2019: "can adversely affect"), on 151 dates. The factor pair
  nets to zero and the theme signal stays at 2/4, so only text changes; no dated evidence ties PepsiCo's multiple to e-commerce. Decided
  from the filings' wording before any outcome; the builder gained the NKE encoding (`ecommerce_company_acknowledged`).
- **Nasdaq.** The 8-K of 2017-12-08 (16:35 ET, dated 2017-12-11) transfers the listing from the New York Stock Exchange "effective
  December 19, 2017 after market close"; "PepsiCo shares are expected to begin trading as a Nasdaq-listed security on December 20,
  2017". A new fact-sheet key, `listings`, names the exchange once announced and effective, so the model's header and price line read
  Nasdaq from 2017-12-22 (display only; the NYSE before, so no earlier model changes).
- **Calendar.** Every release came before the open (8-Ks accepted 06:00-06:33 ET; calls at 7:45 or 8 a.m. ET, question-and-answer
  calls at 8:15 a.m. in 2020) except Q3 2020, whose 8-K was accepted at 17:56 ET on 2020-09-30 for a release dated October 1: after the
  close, so it counts from 2020-10-01 (the UNP Q1 2011 rule). The Q4 2018 release came on Friday 2019-02-15 before the open, so the print
  meets that day's close; the Q1 2019 release on 2019-04-17 was followed by Good Friday. The weeks' dates are 2017-02-16, 2017-04-27,
  2017-07-12, 2017-10-05, 2018-02-14, 2018-04-27, 2018-07-11, 2018-10-03, 2019-02-15, 2019-04-18, 2019-07-10, 2019-10-04, 2020-02-14,
  2020-04-29, 2020-07-14 and 2020-10-02. The next print's timing in each print's note is the year-ago quarter's (public), not the
  actual next date (earlier prints mostly took the actual one: display text only).
- **Durability is unchanged:** DURABLE, risk 2, with each 10-K's own words (FY2016 and FY2017: "a complementary portfolio of enjoyable
  brands", from FY2018 "of brands"; the U.S. liquid refreshment beverage shares of PepsiCo and The Coca-Cola Company were 24% and 20%
  in 2016, 23% and 20% in 2017, 22% and 20% in 2018 and 2019). The FY2019 10-K adds to its competitors "smaller companies developing
  and selling micro brands directly to consumers through e-commerce platforms" (not quoted in the "why"; the e-commerce risk is on the
  watch list). EV and CRYPTO, live from 2020, are scoped to other industries; GLP1 is not live until 2023-08-08.
- **Adds nothing:** the officer, director, compensation and annual-meeting 8-Ks; the note offerings, redemptions, and tender and
  exchange offers (2016-10-03 to 2020-10-09); the credit agreements (2017-06-06, 2018-06-05, 2020-06-03); the SodaStream agreement
  (2018-08-20, $3.2 billion, no guided figure) and completion (2018-12-06); the pension recast (2018-02-27); the by-law amendment and
  virtual annual meeting (2020-04-16); and the 10-Qs beyond their servings and dividends.

Corrections to 2013-2016, found while extending the series and applied before any 2017-2020 outcome: the Q4 2012-2015 prints' servings
notes cited the next 10-K's figure for the year ("the FY2012 10-K gives +3% for the year"), which that 10-K published after the print:
on 2013-02-15, 2014-02-14 and 2015-02-12 a model showed it before it was public. The notes now say only that no filing states the
quarter's total servings; the franchise line shows each 10-K's figure from its own date, as intended. Text only, on 38 dates (the
volume line, and the franchise line on those three): no metric, class, tier or outcome moves. A check now finds no model that cites a
10-K or 10-Q dated after it, and no fact whose text cites a later filing apart from the Q3 2007 print, whose currency effect comes from
the 10-Q filed the next day by design ("PEP") and which no model dated before that 10-Q uses.

Controls: altering one value of each print, `servings_later`, vintage, guide, dividend, event and listing published from 2016-12-01
changes no date before its publication (a listing: its effective date) and changes the first weekly date on or after it (56 of 56). No
string of any dated fact appears in a model dated before it (448,581 checks over the 679 PEP models). The firewall at 2017-02-20,
2018-01-01, 2018-02-20, 2019-01-01, 2019-02-20, 2020-01-01, 2020-02-20 and 2021-01-01 changes no model before its cutoff (477, 522,
529, 574, 581, 626, 633 and 679 dates); the cutoffs after each Q4 print are those where the `servings_later` plant fires. The 470 dates
of 2008-2016 rebuild byte-identical apart from the 38 corrected. Beyond the 209 new entries in the index, the files shared with other
tickers that changed are the firewall (the listing plant, a key no other ticker has) and the anachronism list (SodaStream).

Seen in the build (method behaviour, not tuned):
- **RICH and AVOID on 156 of 209 dates, CHEAP and BUY on 52, FAIR and WATCHLIST on 1.** RICH and AVOID from 2017-01-06 to 2019-02-08
  (110 dates), CHEAP and BUY from 2019-02-15 to 2020-02-07 (52), RICH and AVOID from 2020-02-14 (46), except FAIR and WATCHLIST on
  2020-03-20. By year: RICH on all 52 dates of 2017 and all 52 of 2018; CHEAP on 46 of 2019 and RICH on its first 6; RICH on 46 of 2020,
  CHEAP on its first 6 and FAIR on 1. The tier agrees on 6 to 8 of the 8 robustness variants (8 on 161 dates), the valuation verdict on
  2 to 8 (8 on 140).
- **EPS anchors on the last full year:** FY15's $3.67 to 2017-02-10 (27.7-28.9x, the 92nd-97th percentile), FY16's $4.36 to 2018-02-09
  (24.8-27.9x, the 83rd-100th), FY17's $3.38 to 2019-02-08 (28.8-36.1x, the 84th-100th: the Tax Act charge in it), FY18's $8.78 from
  2019-02-15 to 2020-02-07 (13.1-16.6x, the 10th-34th, at $115.23-145.37: the tax benefits in it) and FY19's $5.20 from 2020-02-14
  (20.0-28.5x, the 51st-90th, at $103.93-148.30). The 2019 CHEAP year is FY2018's tax benefits: the price did not fall.
- **The EPP floor:** 16x on FY15's, FY16's and FY17's EPS ($58.72, $69.76, $54.08), 18x from 2019-01-04 ($60.84), 15x on FY18's $8.78
  from 2019-02-15 ($131.70), 18x on FY19's $5.20 from 2020-02-14 ($93.60) and 19x on 2020-12-31 ($98.80). The price was below the
  floor on 22 dates, 2019-02-15 to 2019-08-23 (by 0.4% to 12.5%), and above it on every other date, by up to 125.5% (2018-11-30, on
  FY17's $3.38).
- **BEAR** is -14.1%/yr to 2018-02-09, -22.5% from the Q4 2017 print and -40.8% from the Q4 2019 print. **BULL** is the window's EPS
  CAGR, floored at BASE on most dates: +0.6%/yr (2008-2017) from 2018-02-14 against BASE's +0.2%, +10.6% (2008-2018, FY18 from the Q4
  print) on 2019-02-15, +9.8% (2009-2018) from the FY2018 10-K, +3.2% (2010-2019) against BASE's +2.4% from 2020-07-14. **XBULL** is
  +10.4%/yr (2008-2010) to 2019-02-08 and +41.9% (2016-2018) from 2019-02-15. The price stood above the BULL value on 97 dates, all
  before 2019-02-15 (Ratio B `inf`).
- **BASE followed the quarter's growth plus the buyback** (+1.1 to +1.5 points): +2.5%/yr (Q3 2016) to 2017-02-10, +8.5% (Q4 2016, the
  extra week in), +4.1%, +5.0% and +3.8% (Q1-Q3 2017), +0.2% (Q4 2017), +3.5%, +2.6% and +4.7% (Q1-Q3 2018), +5.2% and +5.1% (Q4 2018,
  before and after the FY2018 10-K), +6.7%, +6.3% and +6.4% (Q1-Q3 2019), +7.2% (Q4 2019), +9.2%, +2.4% and +8.8% (Q1-Q3 2020). On the
  CHEAP dates Ratio B was 0.33 to 0.71 and the BASE price $175-180.
- **The proxy composite** was 2.30 on Q3 2016, 2.15 on Q4 2016 (no servings: an empty slot scores BASE), 2.10 on Q1 2017 (servings
  +0.5% at BEAR, operating margin +239bp at XBULL), 1.80 on Q2 2017 (servings 0%), 2.15 on Q3 and Q4 2017, 1.95 on Q1-Q3 2018 (servings
  +1%, +1% and +3%, each below the decade's worst year of 4%), 2.20 on Q4 2018 (gross margin +73bp), 2.35 on Q1 2019 (servings +4%,
  gross margin +87bp, operating margin +120bp), 1.85 on Q2 2019 (servings +3% and operating margin -223bp at BEAR), 2.20 on Q3 2019,
  2.35 on Q4 2019, 2.55 on Q1 2020 (servings +6% and net revenue +7.7% at BULL, operating margin -172bp at BEAR), 1.85 on Q2 2020
  (servings +1% and operating margin -205bp at BEAR) and 2.40 on Q3 2020 (servings +13% with the acquisitions, at XBULL).

How far each call moves the classes (the 209 dates rebuilt with one encoding changed; no outcome consulted):
- the core figures in the history (FY16 $4.85, FY17 $5.23, FY18 $5.66, FY19 $5.53) would change 52 classes (CHEAP to RICH on every date
  from 2019-02-15 to 2020-02-07) and 59 tiers (those 52 BUY to AVOID; AVOID to WATCHLIST on the six dates from 2018-04-27 to 2018-06-01;
  WATCHLIST to ACCUMULATE on 2020-03-20);
- those and the core EPS guides read as points (FY17 $5.09, $5.13, $5.23; FY18 $5.70, then $5.65; FY19 $5.50; FY20 $5.88 until the
  withdrawal of 2020-04-28, $5.50 from 2020-10-01) would change 59 classes (the 52; RICH to FAIR or CHEAP on five dates from 2018-05-04
  to 2018-06-01; FAIR to CHEAP on 2020-03-20 and RICH to FAIR on 2020-03-27) and 78 tiers;
- FY18 without the stated tax benefits ($5.21: $8.78 less $3.55 and $0.02, a derived figure, as a test only) would change the same 52
  classes and 52 tiers (BUY to AVOID);
- FY17 without the Tax Act charge ($5.08: $3.38 plus the stated $1.70, a derived figure, as a test only) would change 1 class (FAIR to
  RICH on 2020-03-20) and 9 tiers (AVOID to WATCHLIST on the eight dates from 2018-04-20 to 2018-06-08, and 2020-03-20); both derived
  figures together, 52 classes and 60 tiers;
- the stated organic growth for every print (-0.3% to +7.9%: the extra week, structural changes and currency out) would change 1 class
  and 1 tier (FAIR to RICH and WATCHLIST to AVOID on 2020-03-20);
- the organic revenue guides read as fiscal-year revenue guides (4 percent for 2019, about 4 percent from 2020-10-01) would change
  nothing;
- servings from the releases only (no `servings_later`), and "was even with the prior year" read as no figure, would change nothing;
- the dividends dated from the announcements (2017-02-15, 2018-02-13, 2019-02-15, 2020-02-13) would change nothing;
- no e-commerce watch list would change nothing (text only, by construction).

Judgement calls that could carry hindsight:
- the 2008 core rule, which keeps FY16-FY19 at GAAP, together with the mirror test's threshold, which keeps FY2018's $5.1 billion of tax
  benefits in: the CHEAP and BUY year from 2019-02-15 to 2020-02-07 rests entirely on them (52 classes with the core figures or with
  FY18 without the benefits). Both rules were frozen before PEP was built (2026-11-01 and 2026-11-02) and are applied as written, but
  whether a non-cash tax benefit should anchor a multiple is the question an analyst in 2019 would have asked, and its answer is the
  call that moves the most in this range;
- keeping the extra week, divestitures and acquisitions in growth (1 class);
- ECOMMERCE on the watch list from the FY2017 10-K rather than from the FY2014 10-K's "other distribution channels such as e-commerce"
  (text only);
- `servings_later` from the 10-Qs, "even" read as 0%, and the empty fourth quarters (no class moves);
- dating dividends from their declarations (no class moves);
- the pension recast and the 2019 segment realignment adding nothing, and each 2018 print's operating margin change on its release's
  recast basis (not tested: the releases state no other basis for both years);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2017-2020 went; DURABLE (the class label only).

### PEP 2021-2023: three-year 10-Ks, servings leave every filing, the Juice Transaction at GAAP, GLP-1 off the watch list, RICH on 155 of 156 dates

```bash
python3 retro/build_pep.py --weekly 2021-01-04 2023-12-31                   # 156 dates, 2021-01-08 .. 2023-12-29
for c in 2021-02-20 2022-01-01 2022-02-20 2023-01-01 2023-02-20 2024-01-01; do python3 retro/tools/firewall.py $c PEP; done
```

The 36 8-Ks (one an 8-K/A), nine 10-Qs and three 10-Ks filed from January 2021 to December 2023 were listed from EDGAR with their
acceptance times, and the 8-Ks of October-November 2020 were read again; every 8-K's items were read for guides, figures and dividend
rates, and the twelve releases, the 10-Qs' dividend notes and the FY2020-FY2022 10-Ks were transcribed by Opus directly, each figure
typed and then asserted by script against the parsed row of its own filing, and each acceptance time against EDGAR's submissions data.
353 strings were checked word for word with `verbatim.py` against their own filings. Thresholds, signals, the engine and the builder's
code are unchanged (its comments record the GLP-1 decision below); "Juice Transaction" (first in a PepsiCo filing on 2021-10-05) and
"Russia-Ukraine conflict" (2022-02-24) join the anachronism list (no earlier model of any ticker contains either). Decided before any
2021-2023 outcome was computed:

- **Three vintages, three years each.** The FY2020 10-K (accepted 2021-02-10 17:41 ET, dated 2021-02-11), the FY2021 10-K (2022-02-09
  18:03 ET, dated 2022-02-10) and the FY2022 10-K (2023-02-08 18:06 ET, dated 2023-02-09) have no Item 6, so no five-year summary: each
  supplies the three years of its income statement, and earlier years keep the latest 10-K that reported them (the ACN FY21 rule). The
  histories run 2011-2020 (2015-2017 from the FY2019 10-K, 2014 from the FY2018 10-K, 2013, 2012 and 2011 from the FY2017, FY2016 and
  FY2015 10-Ks), 2012-2021 and 2013-2022. First-year diluted shares come from the latest 10-K that reports them: 2011's 1,597M (FY2013),
  2012's 1,575M (FY2014), 2013's 1,560M (FY2015). No 10-K restates an earlier year's EPS or net revenue. Each 10-K came minutes before
  its Q4 release, so no Q4 print's full year extends a history (as for Q4 2019).
- **FY2020-FY2022 at GAAP (the 2008 core rule):** $5.12, $5.49 and $6.42. Each 10-K's core figure ($5.52, $6.26, $6.79: "Core net income
  attributable to PepsiCo per common share – diluted") also removes the commodity mark-to-market net impact, so none replaces GAAP. GAAP
  2021 carries the charge related to cash tender offers ($0.49 a share); GAAP 2022 is a 53-week year (the 10-K states the extra week's
  1 point of net revenue growth and no per-share figure) and carries the gain associated with the Juice Transaction ($2.08), impairment
  and other charges ($2.12) and a tax benefit related to the IRS audit ($0.23), all as published. Neither test of method r2 for a
  distorted year is met: the listed benefits ($3.2 billion) are smaller than the year's income without them ($5.7 billion), and the
  listed charges ($3.7 billion) smaller than its net income ($8.9 billion). FY2018's tax benefits stay in all three histories, so BEAR is
  2019's -40.8% ($8.78 to $5.20) and XBULL 2016-2018's +41.9%/yr on every date.
- **No guide gives a field.** 2021: "A mid-single digit increase in organic revenue" and "A high-single digit increase in core constant
  currency EPS" (words), then 6 percent organic growth and core EPS of "approximately $6.20" (Q2 2021) and approximately 8 percent and
  "at least $6.20" (Q3 2021); 2022: 6 percent and core EPS of $6.67, then 8 percent and $6.63, 10 percent and $6.63, and 12 percent and
  approximately $6.73; 2023: 6 percent and $7.20, then 8 percent and $7.27, 10 percent and $7.47, and 10 percent and $7.54. The EPS figures
  are on the core basis (the 2008 core rule) and the revenue figures organic, which removes acquisitions, divestitures, currency and the
  extra week: display only, as for 2016-2020. The Q3 2023 release's fiscal 2024 sentence ("results towards the upper end of our long-term
  target ranges") is words about a later year (the UNP 2018 rule). No reiteration 8-K was filed. The last full year's EPS stands (the
  rollover rule): FY19's $5.20 to 2021-02-05, FY20's $5.12 from 2021-02-12, FY21's $5.49 from 2022-02-11, FY22's $6.42 from 2023-02-10.
- **Growth excluding currency: reported growth less the stated currency effect** (the NKE rule, as from Q4 2012), both from the table
  that opens each release; a "—%" is 0%. +10.8% (Q4 2020: +8.8% and 2 points unfavorable), +7.3%, +17.5% and +9.6% (2021: +6.8% with 0.5
  points unfavorable, +20.5% and +11.6% with 3 and 2 points favorable), +12.4% (Q4 2021, "—%"), +10.3%, +8.2% and +11.8% (2022: +9.3%,
  +5.2% and +8.8% against 1, 3 and 3 points), +13.9% (Q4 2022: +10.9% against 3 points; 17 weeks against 16), +12.7%, +12.9% and +8.7%
  (2023: +10.2%, +10.4% and +6.7% against 2.5, 2.5 and 2 points). The 2020 acquisitions (5 to 0.5 points a quarter, to Q4 2021), the
  Juice Transaction (2 to 5 points a quarter, Q1 2022 to Q1 2023: "Acquisitions and divestitures primarily reflect the Juice
  Transaction") and the 53rd week (4 points in Q4 2022) stay in, as published (the AVGO rule). Organic growth (+2.4% to +16.0%), which
  removes them, is not used.
- **Servings leave every filing.** The last filing that states total servings is the Q3 2020 10-Q (+13%). No release, 10-Q or 10-K of
  2021-2023 states them (each was searched; the releases give food/snack, later convenient-food, and beverage unit volume). So every print
  of the range has an empty slot, and the AAPL Mac-unit rule applies, as for NIKE's futures orders: the servings signal keeps its name,
  thresholds and weight, scores BASE with no value (shown "n/r"), and no other measure replaces it (the divisions' unit volumes are a
  different measure: the ACN headcount and UNP GTM rules). The franchise line says each 10-K states none.
- **One-offs in the operating margin, as published.** The Q1 2022 operating profit carries the $3,322M gain associated with the Juice
  Transaction (operating margin +1,691bp), Q2 2022 $1,165M of Russia-Ukraine conflict charges (-601bp), Q4 2022 $1,741M of impairment and
  other charges (-724bp), and Q1 and Q2 2023 compare with those quarters (-1,778bp, +612bp). A core statement also removes the
  mark-to-market item, so none replaces GAAP (the 2008 core rule, as for the Venezuela charges of Q3 2015).
- **Dividends,** the latest declared rate: $1.0225 a quarter from the FY2020 10-K ("On February 4, 2021, the Board of Directors declared a
  quarterly dividend of $1.0225 payable March 31, 2021"), $1.075 from the Q2 2021 10-Q (2021-07-13), $1.15 from the Q2 2022 10-Q
  (2022-07-12) and $1.265 from the Q2 2023 10-Q (2023-07-13), each "Cash dividends declared per common share" in a 10-Q filed after the
  close on the evening before its release's date; each 10-K restates the rate in force. No release of 2021-2023 states a dividend per
  share and no 8-K states a declaration. The increases announced with each year's Q4 results (to $4.30, $4.60 and $5.06 annualized,
  "effective with the dividend expected to be paid in June") were announcements (the AAPL 2012 rule, as for 2010-2020).
- **E-commerce stays on the watch list.** The FY2020 10-K's risk-factor heading no longer names e-commerce ("Changes in the retail
  landscape or in sales to any key customer can adversely affect our business."), but its body does: "Our business can be adversely
  affected if e-commerce channels and hard discounters take significant additional market share away from traditional retailers or we
  fail to find ways to create more powerful digital tools and capabilities for our retail customers to enable them to grow their
  businesses." The FY2021 and FY2022 10-Ks keep the sentence ("increasingly better digital tools"). The rule reads the risk factors, not
  their headings, so ECOMMERCE stays on the list, company-acknowledged, with no market read, each 10-K's wording replacing the last.
- **GLP-1 stays off the watch list.** GLP1 is live from 2023-08-08 and its scope names snacks and beverages, but its dated evidence in
  `taxonomy_eras.json` is a sector-wide sell-off ("medtech and snack stocks sell off") that names no company. PepsiCo's filings to the Q3
  2023 10-Q (2023-10-10) never name GLP-1 drugs or weight-loss medication: the 10-Ks' only obesity wording is a reputational risk
  ("concerns regarding whether certain of our products contribute to obesity or an increase in public health costs"), and the 2023
  releases and 10-Qs say nothing. A theme enters PEP's watch list from a PepsiCo 10-K that names it as a risk (the NKE and LOW rule), as
  ECOMMERCE did: that theme's own sector sell-off (2017-06-16, grocers) left PEP's list empty until the FY2017 10-K. So GLP1 stays off
  through 2023; the FY2023 10-K, after this range, is where the same rule looks again. Picking press coverage of the debate by hand would
  select with hindsight (the ACN rule). Text only by construction: the factor pair nets to zero and the theme signal stays at 2/4.
- **A 53-week year.** Fiscal 2022 ended on 2022-12-31 (the last-Saturday rule; the builder's calendar check passes): "PepsiCo’s fourth
  quarter 2022 includes 17 weeks of results and its 2022 fiscal year includes 53 weeks of results." The extra week stays in the GAAP
  figures and in growth, as published (the LOW and AAPL rule, as for 2011 and 2016).
- **Calendar.** From Q4 2020 to Q2 2023 each release's 8-K, and its 10-Q or 10-K, was accepted after the close (17:37-18:12 ET) on the
  evening before the release's date, so each counts from that date (the Q3 2020 rule); the Q3 2023 8-K and 10-Q came before the open
  (06:05 and 06:03 ET). Question-and-answer calls at 8:15 a.m. ET. No release fell on the week's last trading day, so the weeks' dates
  are the next trading days: 2021-02-12, 2021-04-16, 2021-07-14, 2021-10-06, 2022-02-11, 2022-04-27, 2022-07-13, 2022-10-13, 2023-02-10,
  2023-04-26, 2023-07-14 and 2023-10-11.
- **Durability is unchanged:** DURABLE, risk 2, with each 10-K's own words (FY2020: "a leading global food and beverage company"; from
  FY2021: "a leading global beverage and convenient food company with a complementary portfolio of brands, including Lays, Doritos,
  Cheetos, Gatorade, Pepsi-Cola, Mountain Dew, Quaker and SodaStream", "Lay’s" from FY2022; the U.S. liquid refreshment beverage shares of
  PepsiCo and The Coca-Cola Company were 22% and 20% in 2020, 22% and 19% in 2021, and 20% and 21% in 2022). EV and CRYPTO are scoped to
  other industries; GENAI, live from 2022-11-30, names none of PepsiCo's products.
- **Adds nothing:** the officer, director and annual-meeting 8-Ks; the credit agreements (2021-05-28, 2022-05-27, 2023-05-30); the note
  offerings, cash tender offers, redemptions and defeasance (2021-08-05 to 2023-11-13); and the 10-Qs beyond their dividends. No 8-K of the
  range carries a guide, a figure or a dividend rate, and none reports the Juice Transaction: the Q3 2021 10-Q is the first filing that
  names it ("On August 2, 2021, we entered into an agreement with PAI Partners to sell Tropicana, Naked and other select juice brands").

Controls: altering one value of each print, vintage, guide, dividend and event published from 2020-12-01 changes no date before its
publication and changes the first weekly date on or after it (33 of 33). No string of any dated fact appears in a model dated before it
(790,383 checks over the 835 PEP models), and no model names a 10-K or 10-Q filed after it (7,712 mentions). The firewall at 2021-02-20,
2022-01-01, 2022-02-20, 2023-01-01, 2023-02-20 and 2024-01-01 changes no model before its cutoff (686, 731, 738, 783, 790 and 835
dates); the `servings_later` plant fires at every cutoff, since no print of the range states total servings. The 679 dates of 2008-2020
rebuild byte-identical. Beyond the 156 new entries in the index, the only file shared with other tickers that changed is the anachronism
list.

Seen in the build (method behaviour, not tuned):
- **RICH and AVOID on 155 of 156 dates; FAIR and WATCHLIST on 2023-10-06** (25.0x FY22's $6.42, the 39th percentile; Ratio B 1.71,
  adjusted gap +0.75), the last date before the Q3 2023 print. By year: RICH on all 52 dates of 2021 and all 52 of 2022, and on 51 of
  2023. The tier agrees on 6 to 8 of the 8 robustness variants (8 on 126 dates; 6 only on 2023-10-06), the valuation verdict on 3 to 8
  (8 on 62).
- **EPS anchors on the last full year:** FY19's $5.20 to 2021-02-05 (26.3-27.7x, the 78th-88th percentile), FY20's $5.12 to 2022-02-04
  (25.2-34.3x, the 65th-97th, at $129.19-175.64), FY21's $5.49 to 2023-02-03 (28.0-33.8x, the 81st-96th, at $153.73-185.69) and FY22's
  $6.42 from 2023-02-10 (24.9-30.5x, the 38th-90th, at $159.62-196.12).
- **The EPP floor:** 20x on FY19's, FY20's and FY21's EPS ($104, $102, $110), 21x from 2023-01-06 ($115, then $135 on FY22's $6.42). The
  price was above the floor on every date, by 18.4% (2023-10-27) to 71.5% (2022-01-14).
- **BEAR is -40.8%/yr on every date** (2019, from FY2018's tax benefits), at the 10th-percentile P/E: $27-41. **BULL** is floored at BASE
  on every date: the window's EPS CAGR is +3.2%/yr (2010-2019), +2.7% (2011-2020), +3.8% (2012-2021) and +4.5% (2013-2022), below BASE
  throughout. **XBULL** is +41.9%/yr (2016-2018) on every date ($296-394). The price stood above the BULL value on seven dates (Ratio B
  `inf`: 2021-12-31 to 2022-02-04 and 2022-08-19); on the other RICH dates Ratio B was 2.12 to 639.91.
- **BASE followed the quarter's growth plus the buyback** (+1.3 to +1.5 points): +8.8%/yr (Q3 2020) to 2021-02-05, +12.3% (Q4 2020),
  +8.8%, +19.0% and +11.1% (Q1-Q3 2021), +13.8% (Q4 2021), +11.7%, +9.6% and +13.2% (Q1-Q3 2022), +15.2% (Q4 2022), +14.0%, +14.2% and
  +10.0% (Q1-Q3 2023). The BASE price was $137-171 in 2021, $154-180 in 2022 and $180-219 in 2023; the adjusted gap was -1.35 to +0.49
  on the RICH dates.
- **The proxy composite** was 2.40 on Q3 2020 (servings +13% at XBULL), 2.15 on Q4 2020 (the servings slot empty from here on, scoring
  BASE), 2.30 on Q1 2021 (operating margin +174bp), 2.40 on Q2 2021 (net revenue +20.5% at XBULL, gross margin -176bp at BEAR), 2.25 on Q3
  2021, 2.10 on Q4 2021 (gross margin -161bp and operating margin -244bp at BEAR), 2.60 on Q1 2022 (operating margin +1,691bp at XBULL
  with the Juice Transaction gain), 1.85 on Q2 2022 (operating margin -601bp with the Russia-Ukraine conflict charges), 2.15 on Q3 2022,
  2.35 on Q4 2022 and Q1 2023 (net revenue at XBULL, operating margin at BEAR with the impairments, then against the year-ago gain), 2.80
  on Q2 2023 (operating margin +612bp against the charges) and 2.50 on Q3 2023.

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- the core figures for FY20-FY22 in the history ($5.52, $6.26, $6.79) would change 1 class (RICH to FAIR on 2023-09-29) and no tier;
- the core figures for every year of the window (FY11-FY22, from each 10-K's figure excluding above items) would change 1 class (FAIR to
  CHEAP on 2023-10-06) and 31 tiers (AVOID to WATCHLIST or ACCUMULATE on 30 dates from 2022-03-11, WATCHLIST to BUY on 2023-10-06);
- those and the core EPS guides read as points (FY21 $6.20 from 2021-07-13; FY22 $6.67, $6.63, $6.63, $6.73; FY23 $7.20, $7.27, $7.47,
  $7.54) would change 16 classes (RICH to CHEAP or FAIR, FAIR to CHEAP, 2023-08-18 to 2023-12-15) and 69 tiers (AVOID to WATCHLIST,
  ACCUMULATE or BUY from 2021-07-14, WATCHLIST to BUY);
- the stated organic growth for every print (+2.4% to +16.0%: the acquisitions, the Juice Transaction, the extra week and currency out)
  would change nothing;
- the organic revenue guides read as fiscal-year revenue guides (6 and about 8 percent for 2021 from 2021-07-13; 6, 8, 10 and 12 for 2022;
  6, 8, 10 and 10 for 2023) would change 1 class and 1 tier (FAIR to RICH and WATCHLIST to AVOID on 2023-10-06);
- the dividends dated from the announcements (2021-02-11, 2022-02-10, 2023-02-09) would change nothing;
- the empty servings slot scored below BEAR, or at XBULL, on every print would change nothing either way;
- each print's operating margin change on the core operating profit of its release's reconciliation (a derived figure, as a test only)
  would change nothing;
- GLP1 on the watch list from 2023-08-08 would change nothing (text only, by construction).

Judgement calls that could carry hindsight:
- the 2008 core rule, which keeps FY20-FY22 and the window's earlier years at GAAP, so that FY2018's tax benefits set BEAR (-40.8%/yr)
  and XBULL (+41.9%/yr) on every date (31 tiers with the core history; 16 classes and 69 tiers with the core guides as points: the call
  that moves the most in this range, as in every PEP range since 2011);
- GLP1 off the watch list from August to December 2023, for want of a PepsiCo filing that names it, although the registry dates the
  theme's market pricing for snacks from 2023-08-08: a reader could argue for the watch list from that date (text only either way);
- the empty servings slot scored BASE for three years (no class moves at either bound);
- keeping the acquisitions, the Juice Transaction and the extra week in growth, and the one-offs in the operating margin (no class moves);
- the Q2 10-Qs as the first statements of each declared dividend (no class moves);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2021-2023 went; DURABLE (the class label only).

### PEP 2024-2026: GLP-1 on the watch list, a 2026 revenue guide in constant currency, impairments at GAAP, a borderline 2025

```bash
python3 retro/build_pep.py --weekly 2024-01-01 2026-10-30                   # 148 dates, 2024-01-05 .. 2026-10-30
for c in 2024-01-01 2024-02-20 2025-01-01 2025-02-20 2026-01-01 2026-02-20 2026-11-01; do python3 retro/tools/firewall.py $c PEP; done
```

The 33 8-Ks (one an 8-K/A), nine 10-Qs and three 10-Ks filed from January 2024 to October 2026 were listed from EDGAR with their
acceptance times; every 8-K's items were read for guides, figures and dividend rates, and the twelve releases, the 8-K of 2025-12-08,
the 10-Qs' dividend notes and the FY2023-FY2025 10-Ks were transcribed by Opus directly, each figure typed and then asserted by script
against the parsed row of its own filing, and each acceptance time against EDGAR's submissions data. 388 strings were checked word for
word with `verbatim.py` against their own filings. Thresholds, signals and the engine are unchanged; the builder gained one event kind
(`glp1_company_acknowledged`, below), which changes no earlier output. "International Beverages Franchise" (first in a PepsiCo filing on
2025-02-04) and "Asia Pacific Foods" (2025-04-24) join the anachronism list (no earlier model of any ticker contains either; the other
2025 segment names are older). Decided before any 2024-2026 outcome was computed:

- **Three vintages, three years each.** The FY2023 10-K (accepted 2024-02-08 17:58 ET, dated 2024-02-09), the FY2024 10-K (2025-02-03
  18:22 ET, dated 2025-02-04) and the FY2025 10-K (2026-02-02 18:07 ET, dated 2026-02-03), each with its income statement's three
  years, earlier years from the latest 10-K that reported them (the ACN FY21 rule): the histories run 2014-2023, 2015-2024 and
  2016-2025. First-year diluted shares: 2014's 1,527M (FY2016), 2015's 1,485M (FY2017), 2016's 1,452M (FY2018). Each 10-K came minutes
  before its Q4 release, so no Q4 print's full year extends a history.
- **FY2023-FY2025 at GAAP (the 2008 core rule):** $6.56, $6.95 and $6.00; the core figures ($7.62, $8.16, $8.14) also remove the
  commodity mark-to-market net impact, so none replaces GAAP. GAAP 2023 carries impairment and other charges ($0.68 a share) and the
  product recall-related impact ($0.07); GAAP 2024 restructuring and impairment charges ($0.41), impairment and other charges ($0.38), an
  indirect tax impact ($0.16), a pension and retiree medical-related impact ($0.16) and the recall ($0.10); GAAP 2025 impairment and other
  charges ($1.09, mostly the Rockstar and Be & Cheery brands in Q2 2025), restructuring ($0.58), acquisition and divestiture-related
  charges ($0.25), pension ($0.14) and tax ($0.08), all as published. Neither distortion test of method r2 is met (GAAP is 86%, 85% and
  74% of EPS without the listed items). The mark-to-market item itself was only $0.02, -$0.01 and nil a share in these years, so here
  GAAP and core differ almost only by the one-offs (see the judgement calls). FY2018's tax benefits stay in all three histories: BEAR
  stays 2019's -40.8% and XBULL 2016-2018's +41.9%/yr on every date.
- **No EPS guide gives a field.** 2024: "At least 4 percent increase in organic revenue" and core EPS "of at least $8.15", then
  "Approximately 4 percent" (Q2 2024) and "A low-single-digit increase in organic revenue" (Q3 2024); 2025: low-single-digit organic
  growth and mid-single-digit core constant currency EPS growth, then core EPS "approximately even" with the implied core declines of 3,
  1.5 and 0.5 percent. The 8-K of 2025-12-08 (16:34 ET, dated 2025-12-09), which followed "constructive engagement" with Elliott
  Investment Management, affirms the 2025 outlook (the latest 2025 guide from its date) and gives a preliminary 2026 outlook, a later
  year (the UNP 2018 rule) that the Q4 2025 release supersedes on the day 2026 becomes current. All are organic or core: display only.
- **A revenue guide in numbers for 2026** (the first since 2009). From the Q4 2025 release the fiscal 2026 outlook states reported net
  revenue growth with its currency assumption: "The assumptions and the guidance above imply net revenue growth within a range of 4 to 6
  percent", with "a foreign exchange translation tailwind of approximately 1 percentage point to benefit reported net revenue" (Q4 2025,
  Q1 and Q2 2026 releases); the Q3 2026 release's outlook table gives Net Revenue "Approximately +6%" and Foreign Exchange Translation
  "Approximately +1.5% to net revenue and core EPS growth". Reported growth less the stated currency effect is growth in constant
  currency with acquisitions and divestitures in, the measure of the prints (the NKE rule), so the guide is a fiscal-year net revenue
  guide in constant currency (`rev_guide`): 3-5% from 2026-02-03 and 4.5% (a point: the LOW "approximately" rule) from 2026-10-08. As
  for the 8-K of 2009-12-08, method r2's full-year fallback prefers it to the latest quarter's growth, so it feeds BASE and the growth
  factor (the LOW rule: a guide that states its growth keeps it). The field existed; no builder change.
- **Growth excluding currency: reported growth less the stated currency effect** (the NKE rule, as from Q4 2012): +1.0% (Q4 2023: -0.5%
  against 1.5 points unfavorable; 16 weeks against 17, the prior year's 53rd week's 3 points in, as published), +2.8%, +1.8% and +1.4%
  (2024: +2.3%, +0.8% and -0.6% against 0.5, 1 and 2 points), +1.8% (Q4 2024: -0.2% against 2), +1.2%, +2.5% and +2.1% (2025: -1.8% and
  +1.0% against 3 and 1.5 points unfavorable, +2.6% with 0.5 favorable), +3.6% (Q4 2025: +5.6% with 2 favorable), +5.1%, +4.2% and +4.9%
  (2026). From Q1 2026 the table that opens each release gives net revenue and its change but no currency row; the results discussion
  states the effect to a decimal ("a 3.4-percentage-point benefit from foreign exchange translation", then 2.2 and 0.7 points), kept as
  published (the summary table rounds it). Acquisitions and divestitures (1 to 2.5 points net favorable from Q3 2025) stay in, as
  published (the AVGO rule). Organic growth (+1.2% to +4.5%), which removes them, is not used.
- **Servings still absent:** no release, 10-Q or 10-K of 2024-2026 states total servings, so the slot stays empty and scores BASE (the
  AAPL Mac-unit rule, as since Q4 2020).
- **One-offs in the operating margin, as published:** Q4 2023 against Q4 2022's $1,741M of impairment charges (+313bp), Q4 2024 with
  $704M of impairment and other charges and a $218M indirect tax impact, Q2 2025 with $1,860M of impairment of intangible assets
  (-1,012bp), and Q4 2025 and Q2 2026 against those quarters (+402bp, +877bp). GAAP throughout (the 2008 core rule).
- **Dividends,** the latest declared rate: $1.265 a quarter from the FY2023 10-K ("On February 7, 2024, the Board declared a quarterly
  dividend of $1.265 per share payable April 1, 2024"), $1.355 from the Q2 2024 10-Q (2024-07-11), $1.4225 from the Q2 2025 10-Q
  (2025-07-17) and $1.48 from the Q2 2026 10-Q (2026-07-09). The FY2024 and FY2025 10-Ks state only the year's total ("Cash dividends
  declared per common share were $5.3300", then $5.6225), so those vintages carry the rate in force, dated from the 10-Q that first
  stated it (`dividend_published`, the NKE FY2021 rule). The increases announced with each Q4 release (to $5.42, $5.69 and $5.92
  annualized) were announcements (the AAPL 2012 rule).
- **GLP-1 on the watch list from the FY2023 10-K.** GLP1 (live from 2023-08-08; GLP-1 obesity drugs reduce demand for snacks and
  beverages) needed a PepsiCo filing that names it ("PEP 2021-2023"). The FY2023 10-K is the first: under "Reduction in future demand for
  our products would adversely affect our business.", consumer preferences evolve with "diet (whether due to changes in consumer behavior
  and eating habits, the use of weight-loss drugs or other factors)"; the FY2024 10-K says "increasing use of weight-loss drugs" and the
  FY2025 10-K "increasing use of weight-loss drugs, such as GLP-1 medications". So GLP1 joins the watch list from 2024-02-09,
  company-acknowledged, with no market read (the NKE and LOW rule), each 10-K's wording replacing the last. ECOMMERCE keeps the theme
  signal and factor pair (the ACN CLOUD rule: another live theme with company evidence joins the watch list). No dated evidence ties
  PepsiCo's own multiple to it, so no date is re-filed: text only (`glp1_company_acknowledged`, a new event kind).
- **E-commerce stays on the watch list:** the FY2023-FY2025 10-Ks keep the sentence of the FY2021 10-K. **GENAI stays off:** the FY2025
  10-K adds "use of artificial intelligence shopping agents that autonomously select products that may not be ours" among channel
  preferences, a channel rather than a substitute for PepsiCo's products, which GENAI's scope does not name (as for AAPL and AVGO).
- **New segments from 2025.** From Q1 2025 PepsiCo reports six segments: PepsiCo Foods North America (FLNA and QFNA together), PepsiCo
  Beverages North America, International Beverages Franchise, Europe, Middle East and Africa, Latin America Foods and Asia Pacific Foods.
  The 8-K of 2025-07-16 recasts the FY2023 segment data and the FY2024 10-K's segment discussion and "does not revise nor restate
  PepsiCo's previously reported consolidated financial statements": it adds nothing (the ACN 2024-09-30 rule). The FY2024 vintage keeps
  its 10-K's seven divisions; the FY2025 10-K's six take over from its date.
- **Calendar.** Every release's 8-K, and its 10-Q or 10-K, was accepted after the close (17:46-19:16 ET) on the evening before the
  release's date, so each counts from that date (the Q3 2020 rule). The Q4 2023 release fell on Friday 2024-02-09, the week's last trading
  day; public before that day's open, it meets that day's close (the Q4 2008 and Q4 2018 rule), so that week's date is the release day.
  The other weeks' dates are the next trading days: 2024-04-24, 2024-07-12, 2024-10-09, 2025-02-05, 2025-04-25, 2025-07-18, 2025-10-10,
  2026-02-04, 2026-04-17, 2026-07-10 and 2026-10-09.
- **The last date is 2026-10-30,** the last complete week: the series was built on 2026-11-03 before the open (AVGO ends there too). A
  rebuild after the close of 2026-11-06 adds the week of 2026-11-02. The newest dates have no two-year outcome yet.
- **Durability is unchanged:** DURABLE, risk 2, with each 10-K's own words ("a leading global beverage and convenient food company with a
  complementary portfolio of brands, including Lay’s, Doritos, Cheetos, Gatorade, Pepsi-Cola, Mountain Dew, Quaker and SodaStream"; the
  U.S. liquid refreshment beverage shares of PepsiCo and The Coca-Cola Company were 19% and 20% in 2023, 18% and 21% in 2024, and 16% and
  20% in 2025).
- **Adds nothing:** the officer, director and annual-meeting 8-Ks (among them the CFO change and the North America leadership change),
  the by-law amendment (2024-09-20), the credit agreements (2024-05-24, 2025-05-23, 2026-05-22), the note offerings (2024-02-16 to
  2026-10-16), the segment recast (2025-07-16), and the 10-Qs beyond their dividends.

Controls: altering one value of each print, vintage, guide (display, and each `rev_guide`), dividend and event published from
2023-12-01 changes no date before its publication and changes the first weekly date on or after it (41 of 41). No string of any dated
fact appears in a model dated before it (1,107,006 checks over the 983 PEP models), and no model names a 10-K or 10-Q filed after it
(9,022 mentions). The firewall at 2024-01-01, 2024-02-20, 2025-01-01, 2025-02-20, 2026-01-01, 2026-02-20 and 2026-11-01 changes no
model before its cutoff (835, 842, 887, 894, 939, 946 and 983 dates). The 835 dates of 2008-2023 rebuild byte-identical, and all 983
PEP dates lint clean against the extended anachronism list. Beyond the 148 new entries in the index, the only file shared with other
tickers that changed is the anachronism list.

Seen in the build (method behaviour, not tuned):
- **RICH and AVOID on all 52 dates of 2024; a borderline 2025; RICH again in 2026.** Over the 148 dates RICH on 92, CHEAP on 35 and FAIR
  on 21; AVOID on 92, WATCHLIST on 44 and ACCUMULATE on 12 (2025-04-25 to 2025-07-11). In 2025 CHEAP on 30, FAIR on 17 and RICH on 5,
  alternating week to week (CHEAP at 18.6-21.7x FY24's $6.95, the 10th-16th percentile, Ratio B 0.93-1.73; FAIR at 21.0-22.2x, the
  11th-19th, Ratio B 1.33-1.79); in 2026 RICH on 35, CHEAP on 5 and FAIR on 4 (January, and from 2026-09-18). The price state agrees on
  only 3 to 6 of the 8 robustness variants on the FAIR dates, the tier on 5 to 8 (8 on 59 dates), the valuation verdict on 3 to 8 (8 on
  5): in 2025 the class is not a call.
- **EPS anchors on the last full year:** FY22's $6.42 to 2024-02-02 (25.8-26.6x, the 46th-62nd percentile), FY23's $6.56 to 2025-01-31
  (21.7-27.8x, the 11th-78th, at $142.64-182.19), FY24's $6.95 to 2026-01-30 (18.6-22.2x, the 10th-22nd, at $129.07-154.44) and FY25's
  $6.00 from 2026-02-04 (21.0-28.3x, the 10th-83rd, at $125.89-169.74): GAAP EPS fell 13.7% with the 2025 impairments, so the multiple
  rose without the price.
- **The EPP floor:** 22x on FY22's and FY23's EPS ($141, $144; 23x and $151 on 2024-12-27), 21x on FY24's $6.95 ($146) from
  2025-02-05, 22x on FY25's $6.00 ($132) from 2026-02-04 and 21x ($126) from 2026-09-18. The price was below the floor on 34 dates
  (2025-01-10 to 2026-10-02), by up to 11.6% (2025-06-20).
- **BEAR is -40.8%/yr on every date** ($41-50). **BULL** is the window's EPS CAGR where it beats BASE: +4.9%/yr (2014-2023) from
  2024-02-09 and +7.4% (2015-2024) from 2025-02-05; floored at BASE before (Q3 2023's +10.0%) and from 2026-02-04 (the 2016-2025 CAGR is
  +3.6%). **XBULL** is +41.9%/yr (2016-2018) on every date ($368-427). Ratio B was 0.93 to 13.69, never `inf`.
- **BASE followed the quarter's growth plus the buyback, then the 2026 guide:** +10.0%/yr (Q3 2023) to 2024-02-02, +2.1% (Q4 2023), +3.9%,
  +2.9% and +2.5% (Q1-Q3 2024), +2.6% (Q4 2024), +2.0%, +3.3% and +2.9% (Q1-Q3 2025), then the fiscal 2026 revenue guide: +4.6% (3-5%,
  plus 0.6 points of buyback) from 2026-02-04 and +5.1% (4.5%) from 2026-10-09. The buyback shrank to 1.1, 0.8 and 0.6 points a year.
  The BASE price was $168-203.
- **The proxy composite** was 2.50 on Q3 and Q4 2023 (Q4: gross margin +91bp, operating margin +313bp at XBULL against the year-ago
  impairments), 2.15 on Q1 2024, 2.50 on Q2 2024 (gross margin +126bp, operating margin +160bp), 2.20 on Q3 2024, 2.15 on Q4 2024, 2.20 on
  Q1 2025, 1.85 on Q2 2025 (operating margin -1,012bp at BEAR with the impairment), 1.65 on Q3 2025 (gross margin -184bp and operating
  margin -170bp at BEAR), 2.50 on Q4 2025 (operating margin +402bp at XBULL against the year-ago charges), 2.30 on Q1 2026 (net revenue
  +8.5% at BULL), 2.60 on Q2 2026 (operating margin +877bp against the impairment) and 2.35 on Q3 2026. The servings slot scored BASE
  throughout.

How far each call moves the classes (the 148 dates rebuilt with one encoding changed; no outcome consulted):
- the core figures for FY23-FY25 in the history ($7.62, $8.16, $8.14) would change 91 classes (RICH to CHEAP on 41, RICH to FAIR on 29,
  FAIR to CHEAP on 21, from 2024-02-09) and 115 tiers;
- the core figures for every year of the window (FY14-FY25) would change 63 classes (RICH to CHEAP on 42, FAIR to CHEAP on 21, from
  2024-12-20) and all 148 tiers (to WATCHLIST, ACCUMULATE or BUY);
- those and the core EPS guides read as points (FY24 $8.15; FY25 $7.92, $8.04 and $8.12 from the implied declines on $8.16; FY26 $8.63,
  then $8.38, at the implied midpoints on $8.14) would change 83 classes and all 148 tiers (BUY on 142);
- the stated organic growth for every print (+1.2% to +4.5%) would change 2 classes (FAIR to RICH on 2025-10-24 and 2025-12-12) and no
  tier;
- the fiscal 2026 revenue guide read from the organic figures (2-4%, then about 3%) would change 1 class (FAIR to RICH on 2026-10-16) and
  1 tier (WATCHLIST to AVOID on 2026-09-25); no 2026 revenue guide at all (the latest quarter's growth) would change no class and 1 tier
  (AVOID to WATCHLIST on 2026-09-18);
- the dividends dated from the announcements (2024-02-09, 2025-02-04, 2026-02-03) would change nothing;
- the empty servings slot scored below BEAR on every print would change 9 classes (FAIR to RICH, 2025-10-10 to 2026-10-16), at XBULL 2
  classes (RICH to FAIR on 2025-10-17 and 2026-01-30), and no tier either way;
- each print's operating margin change on the core operating profit of its release (a derived figure, as a test only) would change 3
  classes (RICH to FAIR on 2025-10-17 and 2026-01-30, FAIR to RICH on 2026-10-16) and no tier;
- GLP1 off the watch list would change nothing (text only, by construction).

Judgement calls that could carry hindsight:
- the 2008 core rule, which keeps FY23-FY25 at GAAP with the 2023-2025 impairment and restructuring charges (91 classes and 115 tiers
  with the core figures; 83 classes and every tier with the core guides as points): by far the call that moves the most in this range.
  Its premise is that the core figures also remove a recurring timing item, but that item was $0.02, -$0.01 and nil a share in FY23-FY25,
  so here the rule mostly decides whether the impairments count. It was frozen before PEP was built and is applied as written; whether it
  should yield when the recurring item is immaterial is a question for a new method version, tested on other tickers;
- GLP1 on the watch list from the FY2023 10-K, which names "weight-loss drugs" rather than GLP-1 (the FY2025 10-K first names GLP-1
  medications), and ECOMMERCE keeping the theme slot (text only);
- the fiscal 2026 net revenue guide read in constant currency, reported growth less the stated currency tailwind, a new reading for PEP
  (1 class and 1 tier with the organic figures instead; 1 tier without the guide);
- the empty servings slot scored BASE for a fourth year (9 classes at the BEAR bound, 2 at XBULL: in this borderline range the slot
  matters at the margin);
- from Q1 2026 the currency effect from the results discussion's sentence, and the vintages' dividends dated from the Q2 10-Qs (no class
  moves);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2024-2026 went; DURABLE (the class label only).

## MSFT (Microsoft): the eighth ticker, in staging

The MSFT series is built apart from ACN, UNP, LOW, AAPL, NKE, AVGO and PEP and shares nothing with them but the machinery: its own
fact sheet (`retro/facts/MSFT.json`), builder (`retro/build_msft.py`) and engine (`retro/templates/msft_engine.py.tmpl`, the PEP engine
with software signals). The method is still r2. No fact, parameter, outcome or finding of another ticker enters an MSFT model, and
neither does the repository's live `msft_signal_model.py` (a 2026 analysis). Outputs go to `staging/retrospective/MSFT/`, beside the
others, with the same `index.json` and their own `SERIES.md`.

```bash
python3 retro/build_msft.py --weekly 2008-01-01 2008-12-31                  # 53 dates, 2008-01-04 .. 2008-12-31
for d in staging/retrospective/MSFT/2008-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series MSFT
python3 retro/tools/firewall.py 2008-07-01 MSFT
python3 retro/tools/firewall.py 2009-01-01 MSFT
```

The 10-Ks from FY1998 to FY2008 were read for the history and the decade's signal values (the FY1998-FY2001 10-Ks are plain-text
filings), with the Q4 releases of FY2004-FY2006 for the figures they publish excluding one-offs; every 8-K of July 2007 to November 2008
and the 10-Qs from Q1 FY07 to Q1 FY09 were read, by Opus directly. 289 strings were checked with `verbatim.py` against their own filings,
and every number of the prints, guides and vintages was matched to the text of its cited source. Each source's date comes from EDGAR's
acceptance time (converted from UTC; before 2002 EDGAR gives the filing date only). Decided on 2026-11-03, before any MSFT model was built
or any MSFT outcome computed:

- **Fiscal calendar.** Microsoft's fiscal year ends on June 30 (fiscal 2008 runs from 2007-07-01 to 2008-06-30). The builder maps each
  day to its fiscal year by that rule and checks it against the year-ends the vintages state. Days between June 30 and the Q4 print keep
  the last guided year's EPS (the ACN rollover rule): 2008-07-03 and 2008-07-11.
- **Prices on the as-of share basis** (the UNP rule). Microsoft last split on 2003-02-18 (two-for-one, first stated in the Q2 FY03 10-Q,
  accepted 2003-01-31 17:23 ET and dated 2003-02-03), so for every 2008 date Yahoo's series is the price as traded: $34.38 on 2008-01-04.
  The split restates the per-share facts published before it: FY1998 EPS (the FY2002 10-K, $0.84 → $0.42) and the first year's diluted
  shares (the FY2000 10-K's 5,362M for FY1998 and the FY2001 10-K's 5,482M for FY1999, doubled). The 1998 and 1999 splits precede every
  per-share fact in the fact sheet.
- **Every release came after the close.** Each earnings 8-K from Q4 FY07 to Q1 FY09 was accepted at 16:13-16:26 ET (the webcast at 2:30 p.m.
  Pacific), with the 10-Q filed minutes apart, so a print is dated the next trading day, a Friday each time: 2008-01-25, 2008-04-25,
  2008-07-18 and 2008-10-24 are the week's dates, and those prints meet that day's close, public before the open (the AAPL 2011 and AVGO
  2021-2023 rules). The Q1 FY08 release (2007-10-25) gives no statements; its 10-Q, accepted three minutes earlier, supplies the print.
- **History: each year from the latest 10-K that reports it.** The FY2007 10-K (accepted 2007-08-03 17:13 ET, dated 2007-08-06) gives
  FY2003-FY2007; FY2002 comes from the FY2006 10-K, FY2001 from the FY2005 10-K, FY2000 from the FY2004 10-K, FY1999 from the FY2003 10-K
  and FY1998 from the FY2002 10-K. The Q4 FY08 release extends it with FY08 from 2008-07-18, and the FY2008 10-K (accepted 2008-07-31
  17:23 ET, dated 2008-08-01) moves the window to FY1999-FY2008. Two seams stay in, as published (the LOW and PEP rule):
  - the SFAS 123 restatement in the FY2004 10-K, which restated fiscal 2002 and 2003 for stock-based compensation ("The information
    presented for 2000 and 2001 has not been restated"; the FY2005 10-K's summary "reflects stock-based compensation expense except
    fiscal year 2001"), so FY1998-FY2001 carry no option expense and FY2002 on carry it. The FY2004 10-K gives what FY2000 and FY2001 net
    income would have been, but no EPS, and nothing is derived;
  - the FY1999 10-K's restatement of FY1997-FY1998 revenue and cost of revenue (operating income unchanged), which the FY2002 10-K's
    FY1998 already reflects.
- **EPS** is diluted EPS before the cumulative effect of accounting changes (the NKE rule): FY2001 $0.69 ($0.66 after the SFAS 133
  adoption). A company figure excluding one-offs only replaces it (the ACN rule): FY2006 $1.27 and FY2007 $1.49 "as adjusted" in the
  Q4 FY07 release, excluding the Xbox 360 warranty charges, legal charges and tax benefits (GAAP $1.20 and $1.42). FY2003 $0.69, FY2004
  $0.75 and FY2005 $1.12 stay GAAP: their releases list the per-share effects of stock-based compensation, impairments, legal charges
  and tax benefits ("which included after-tax charges ... of $0.35, charges of $0.17 ...") but publish no EPS without them (no figure is
  derived, the NKE rule). FY2008 enters at GAAP $1.87: the Q4 FY08 release publishes no adjusted figure (the European Commission fine and
  the tax benefit of the IRS settlement, $0.15 a share each, offset). **No year is excluded:** the largest listed items, FY2001's $4.80
  billion and FY2002's $4.32 billion of pre-tax investment impairments, are under each year's net income (the AAPL FY2003 test).
- **Guides in numbers.** Every release guides the next quarter and the fiscal year: revenue, operating income and diluted EPS ranges, in
  dollars. Method r2 maps them as follows:
  - current-FY EPS: the midpoint of the latest fiscal-year EPS range for the current year (the ACN rule): FY08 $1.795 from the Q1 FY08
    release ($1.78-1.81, including about $0.01 of aQuantive integration costs) and $1.865 from the Q2 FY08 release ($1.85-1.88); the Q3
    FY08 release guides only the fourth quarter and, in words, "double-digit revenue, operating income and earnings per share growth for
    this fiscal year", so the January range stands to 2008-07-17 (the ACN Q3 FY08 rule); FY09 $2.15 from the Q4 FY08 release ($2.12-2.18)
    and $2.05 from the Q1 FY09 release ($2.00-2.10). The Q3 FY08 release's "preliminary guidance" for fiscal 2009 ($2.13-2.19) is
    superseded the day fiscal 2009 becomes current;
  - BASE growth and the growth factor: the next-quarter revenue range, read as growth on the same quarter a year earlier from its own
    filing, rounded to 0.1, as published (the AAPL rule; the 2011 rule): Q2 FY08 $15.6-16.1B on Q2 FY07's $12.542B (+24.4% to +28.4%),
    Q3 FY08 $14.3-14.6B on $14.398B (-0.7% to +1.4%), Q4 FY08 $15.5-15.8B on $13.371B (+15.9% to +18.2%), Q1 FY09 $14.7-14.9B on $13.762B
    (+6.8% to +8.3%), Q2 FY09 $17.3-17.8B on $16.367B (+5.7% to +8.8%);
  - no margin step: the operating income ranges are dollar levels, display only (no margin is derived from two guided figures, the AAPL
    and AVGO rule for an outlook's other lines), so the margin signal takes the latest quarter's change; the fiscal-year revenue range
    sets the segment bridge's total (display only) and the quarter's EPS range is shown in the guide line.
- **The technology-guarantee deferral is revenue recognition, not a one-off** (the AAPL Q4 FY08 rule). Fiscal 2007 deferred $1.64
  billion of revenue from its second quarter (the Express Upgrade to Windows Vista and Office Technology Guarantee programs and
  pre-shipments) and recognized $1.67 billion in its third; no fiscal year changes, and Microsoft defers upgrade-right revenue as a matter
  of course (the FY2005 release's "decline in earned revenue from Upgrade Advantage"). So the Q2 and Q3 FY08 prints and the guides read
  against those quarters stay as reported (Q2 FY08 revenue +30.5%, Q3 FY08 +0.4%), with the company's "as adjusted" figures in the notes
  (Q2 FY07 $14,179M; Q3 FY07 $12,729M). A comparable operating income replaces GAAP only when the release gives it for both quarters and
  it excludes only one-offs (the PEP Q4 2007 and Q4 2008 rule): the Q4 FY07 release's pair (the Xbox 360 charges, $1,057M, and Q4 FY06's
  legal charges, $351M). The Q3 FY08 release's pair also removes the technology-guarantee revenue from Q3 FY07, so that print stays GAAP
  and keeps the $1.42 billion fine; the Q4 FY08 release gives no adjusted figures, so Q4 FY07 there is GAAP with its Xbox charge.
- **A recast year-ago quarter** is taken as the release shows it: the Q1 FY09 release presents Q1 FY08 operating income at $5,849M ($5,918M
  first reported) after the change in the presentation of foreign currency remeasurement gains and losses. The 8-K of 2008-11-20 that recasts
  FY2004-FY2008 the same way changes no EPS or revenue and no guided number, so the FY2008 vintage keeps its 10-K's figures (the PEP
  segment-recast rule; operating margins are display only without a margin guide).
- **Dividends,** each from the first filing that states the rate: $0.10 a quarter (FY2007 10-K, declared June 27, 2007), $0.11 from the
  Q1 FY08 10-Q (declared September 12, 2007; dated 2007-10-26), $0.11 again in the FY2008 10-K, $0.13 from the Q1 FY09 10-Q (declared
  September 22, 2008; dated 2008-10-24).
- **Signals.** Six, with ACN's weights, in the PEP and NKE layout: unearned revenue growth (0.20: short- plus long-term unearned revenue
  at the quarter's end against the year-ago quarter's end, the multi-year licensing billed ahead of recognition), gross margin change
  (0.20), revenue growth (0.15, as reported), receivables growth less revenue growth (0.15, lower is better: volume licensing billed ahead
  of collection), the operating-margin change (0.15; the guided step, else the latest quarter) and the theme slot at 2/4. Values are each
  release's or its 10-Q's, derived from the income statement and balance sheets; the year-ago balance sheet comes from that quarter's own
  10-Q or release (the fact sheet keeps the raw figures and the builder re-derives each value).
- **Thresholds by rule T** over the ten years of the FY2007 10-K, the vintage public on 2008-01-04: FY1998-FY2007. Revenue growth from the
  five-year summary of the latest 10-K published by then that reports both years, the margins from the income statements of the latest
  10-K that reports both years, unearned revenue and the receivables gap within each year's own 10-K. A company figure excluding one-offs
  replaces the reported one where it was published for both years on the same basis: FY2006 and FY2007 operating income as adjusted
  ($17,581M and $19,735M). The values are in the fact sheet (`rule_t`); the builder recomputes the thresholds and refuses to build if the
  engine's differ.

  | Signal | Decade (FY1998-FY2007) | BEAR / BASE / BULL / XBULL |
  |---|---|---|
  | unearned revenue growth | 103.67, 46.78, 13.61, 16.57, 37.92, 16.43, -9.3, 12.11, 18.93, 16.0 % | -35 / -9 / 17 / 104 % |
  | gross margin change | 206.2, 186.8, 117.3, -58.1, -464.2, 126.7, 59.2, 274.9, -211.8, -364.1 bp | -1020 / -460 / 90 / 270 bp |
  | revenue growth | 27.87, 29.39, 16.25, 10.19, 12.13, 13.47, 14.44, 8.02, 11.29, 15.45 % | 2 / 8 / 14 / 29 % |
  | receivables less revenue | 21.5, 24.4, 28.5, 2.8, 27.6, -12.2, -1.1, 13.9, 18.5, 6.3 pp | 41 / 29 / 16 / -12 pp |
  | operating margin change | 121.7, 825.0, -274.7, -161.2, -434.3, 49.2, -512.9, 1207.1, 60.1, -109.9 bp | -1000 / -510 / -30 / 1210 bp |

- **Durability.** DURABLE, risk 2, as for the other seven. The "why" is the 10-K's own words: "We generate revenue by developing,
  manufacturing, licensing, and supporting a wide range of software products for many computing devices", "Challenges to our business
  model may reduce our revenues and operating margins", with open source ("the popularization of the open source software model continues
  to pose a significant challenge to our business model"; FY2008: "Certain “open source” software business models challenge our
  license-based software model") and "the software-as-a-service business model" (FY2008: the model of "revenues primarily from
  advertising or subscriptions"), and "We face intense competition". No disruption theme in `taxonomy_eras.json` is live for a software
  maker in 2008 (CLOUD from 2012-10-30, scoped to on-premise IT; OFFSHORE to IT services; GENAI from 2022-11-30); no live theme covers
  the open-source and software-as-a-service risks, so the wording stays in the "why" (the PEP obesity rule). The watch list is empty and
  the builder refuses events until a theme encoding is decided.
- **Segment bridge and EPS check** (display only): the vintage's five segments (Client, Server and Tools, Online Services Business,
  Microsoft Business Division, Entertainment and Devices Division) with each one's growth, the total from the fiscal-year revenue range's
  midpoint; the EPS check runs on the pre-tax margin, which carries investment income ($1.6 billion in FY2007).
- **Adds nothing:** the Xbox 360 warranty 8-K (2007-07-05, booked in the Q4 FY07 print), the aQuantive closing (2007-08-13: "not expected
  to have a significant impact on previously issued fiscal 2008 guidance", words), the XBRL exhibits furnished after each 10-Q and 10-K,
  the officer and director 8-Ks (2008-01-11, 2008-06-17, 2008-07-25, 2008-09-25), the Yahoo! proposal and its sequels (2008-02-01,
  2008-02-11, 2008-04-07, 2008-05-05, 2008-05-19: no guided number), the debt program (2008-09-22), the FX-presentation recast
  (2008-11-20), and the 10-Qs beyond their statements, currency effects and dividends.
- **Anachronism list:** Microsoft names first seen after the start of 2008 (Windows 7, Windows Azure, Bing, Windows Phone 7, Kinect, Office
  365, Windows 8, Surface Pro, Xbox One, Nokia Devices and Services, Windows 10, HoloLens, Dynamics 365, Microsoft Teams) join
  `taxonomy_eras.json`, each dated from the first Microsoft filing that uses it (EDGAR full-text search). No existing model of any ticker
  contains them, so no output changes. MSFT's source ids are `MS1`-`MS29`: plain `M3`-`M5` are Apple chip names on the list.

Controls: altering one value of each print, vintage, guide, dividend and the split changes no date before its publication and changes the
first weekly date on or after it (22 of 22; the Q4 FY07 print's FY07 actuals and the Q4 FY07 release's fiscal 2008 guide are superseded
before 2008-01-04, and the Q3 FY08 release's preliminary fiscal 2009 guide on the day fiscal 2009 becomes current, so those three change
nothing). Rebuilding the 2008 dates of ACN, UNP, LOW, AAPL, NKE and PEP and the 2009 dates of AVGO changes nothing.

Seen in the build (method behaviour, not tuned):
- **CHEAP and BUY on all 53 dates**, robustness 8 of 8 on every date.
- **The EPP floor is the bubble years' multiple.** The median of the calendar-year P/E lows (on 2008-01-04: 1998 32.1x, 1999 48.1x, 2000
  30.1x, 2001 31.4x, 2002 31.0x, 2003 33.0x, 2004 23.7x, 2005 19.1x, 2006 14.9x, 2007 15.5x, 2008 19.2x) is 30x, 26x on 2008-12-31
  when 1998 leaves the window, so the floor is $53-65 against a stock at $19-34: 36-69% below it on every date (+0.20 EPP adjustment).
  The window's median P/E is 35-37x and its 75th percentile 50-51x, so the stock's 9.3-19.2x is at the 0th-10th percentile.
- **BEAR is the restatement seam.** The worst year in the history is FY2002 (-30.4%: FY2001's $0.69 without option expense, FY2002's
  $0.48 with it), so BEAR is -30.4%/yr on every date, at the 10th-percentile P/E: $15-18.
- **BASE follows the quarter guide, and the deferral swings it:** +27.3%/yr to 2008-01-18 (the Q2 FY08 range against a Q2 FY07 that had
  deferred $1.64 billion, plus 0.9%/yr of buyback), +1.3%/yr from 2008-01-25 (the Q3 FY08 range against a Q3 FY07 that recognized it),
  +18.0%/yr from 2008-04-25, +8.8%/yr from the Q4 FY08 print (+9.2% once the FY2008 10-K moves the buyback to FY99-FY08's 1.6%/yr) and
  +8.9%/yr from 2008-10-24. The growth factor reads +0.50, -0.50, +0.36, -0.50 and -0.50 against the history's median revenue growth
  (13.5%; 14.0% with FY2008 from the Q4 print, 13.5% again over FY1999-FY2008).
- **BULL and XBULL** are the FY98-FY07 EPS CAGR (+15.1%/yr; BASE's +27.3% and +18.0% where higher; +16.1% over FY98-FY08 from the Q4
  print) and the FY98-FY00 run (+42.3%/yr); from the FY2008 10-K, FY99-FY08's +11.4%/yr and FY04-FY06's +30.1%/yr.
- **The market composite sits at the bottom of its grid** (1.00-1.38, as for AAPL): the hurdle price lies below the BASE case on every
  date. The adjusted gap is +1.32 to +2.44 and Ratio B 0.03-0.17.
- **The proxy composite** is 2.45 on Q1 FY08, 3.15 on Q2 FY08 (revenue +30.5%, gross margin +722bp and the receivables gap -13.1pp at
  XBULL, all lifted by the year-ago deferral), 1.90 on Q3 FY08 (revenue +0.4% and the operating margin -1,526bp at BEAR: the year-ago
  recognition and the fine), 3.05 on Q4 FY08 (gross margin +611bp at XBULL against a year-ago quarter with the Xbox charge in cost of
  revenue) and 2.15 on Q1 FY09.

How far each call moves the classes (the 53 dates rebuilt with one encoding changed; no outcome consulted):
- the technology-guarantee deferral taken out of the guide reads (Q2 FY07 at $14,179M, Q3 FY07 at $12,729M), out of the Q2 and Q3 FY08
  prints (the company's "as adjusted" pairs), or out of both, would change no class and no tier (BASE +12.7% instead of +27.3% to
  2008-01-18, +14.4% instead of +1.3% from 2008-01-25);
- FY2006 and FY2007 at GAAP ($1.20, $1.42) would change nothing;
- the history and the P/E window from FY2002, the first year on the restated basis (no seam, none of the bubble years), would change no
  class and no tier: BEAR becomes flat, the floor 21x and the EPP gap -9% to -55%;
- FY2001 at net EPS ($0.66) and Q1 FY08 operating income as first reported would change nothing.

Judgement calls that could carry hindsight:
- the signals, chosen by a builder who knows what 2008 and 2009 brought: unearned revenue and the receivables gap (rule T then sets the
  thresholds mechanically);
- the technology-guarantee deferral read as revenue recognition rather than a one-off (it swings BASE between +27% and +1%, and four
  signals on two prints; no class moves);
- keeping the SFAS 123 seam, which sets BEAR at -30.4%/yr, and the ten-year window, whose bubble-era multiples set the floor (no class
  moves without either);
- FY2006 and FY2007 at the company's adjusted figures, legal charges counted as one-offs (no class moves);
- the January FY08 range standing after the Q3 FY08 release, which predates the fine and the offsetting tax benefit;
- leaving the open-source and software-as-a-service risks in the "why" rather than reading them as an early CLOUD theme (the registry's
  live date stands; text only either way);
- DURABLE (the class label only).

### MSFT 2009-2011: a withdrawn guide, operating-expense guides only, the Windows 7 deferral, the first cloud risk factor

```bash
python3 retro/build_msft.py --weekly 2009-01-05 2011-12-31                  # 156 dates, 2009-01-09 .. 2011-12-30
for c in 2009-07-01 2010-07-01 2011-07-01 2012-01-01; do python3 retro/tools/firewall.py $c MSFT; done
```

All 28 8-Ks and the 8-K/A filed from December 2008 to December 2011 were checked: the twelve earnings releases read in full, every
other 8-K read for guides, figures and dividend rates. The FY2009-FY2011 10-Ks were read for the history, the segments, the dividends
and the risk factors, and the nine 10-Qs from Q2 FY09 to Q1 FY12 for their currency effects and dividends. 284 strings were checked
word for word with `verbatim.py` against their own filings, every number of the prints, guides and vintages was matched to the text of
its cited source, and the builder re-derives every print's signal values from its raw figures. Each source's date comes from EDGAR's
acceptance time. Thresholds, signals and the engine are unchanged; the builder gained three encodings (a withdrawn guide, an
operating-expense guide, growth excluding currency when no quarter is guided), decided before any 2009-2011 model was built.
Decided before any 2009-2011 outcome was computed:

- **Three vintages.** The FY2009 10-K (accepted 2009-07-30 06:05 ET, before the open) gives FY2005-FY2009, the FY2010 10-K
  (2010-07-30 11:30 ET, during the session) FY2006-FY2010 and the FY2011 10-K (2011-07-28 14:59 ET, during the session) FY2007-FY2011;
  each is dated the day it was accepted. Each earlier year comes from the latest 10-K that reports it, so the history runs
  FY2000-FY2009, FY2001-FY2010 and FY2002-FY2011. Each Q4 print's fiscal-year figures extend the history for the week before its
  10-K (FY1999-FY2009 on 2009-07-24, FY2000-FY2010 on 2010-07-23, FY2001-FY2011 on 2011-07-22). The first year's diluted shares come
  from the latest 10-K that reports them: FY2000's 5,536M (the FY2002 10-K, doubled for the 2003 split), FY2001's 11,148M (FY2003
  10-K) and FY2002's 11,106M (FY2004 10-K).
- **The SFAS 123 seam leaves the window.** FY2000 and FY2001 carry no stock-based compensation expense in the FY2009 window, FY2001
  alone in the FY2010 window, and the FY2011 window has none. So BEAR stays FY2002's -30.4%/yr to 2011-07-22 and is FY2009's
  -13.4%/yr (FY08 $1.87 to FY09 $1.62) from 2011-07-29.
- **FY2009-FY2011 at GAAP.** No release publishes a figure excluding one-offs. FY09 enters at $1.62: the Q3 FY09 release gives its
  $290 million of severance charges and $420 million of investment impairments only as an effect ("Combined, these two charges reduced
  earnings per share by $0.06"); for the Q4 FY09 quarter's legal charges, impairments and further severance, net of capitalized
  research and development expenses, "Combined, these items also reduced earnings per share by $0.02". FY10 enters at $2.10 and FY11
  at $2.69 (the Q3 FY11 quarter "included a $0.05 tax benefit"). Nothing is derived (the NKE rule).
- **The fiscal 2009 guide withdrawn.** The Q2 FY09 release (2009-01-22) says "Due to the volatility of market conditions going forward,
  Microsoft is no longer able to offer quantitative revenue and EPS guidance for the balance of this fiscal year", and that its
  operating expense guidance "supercedes the fiscal year 2009 guidance that Microsoft provided on Oct. 23, 2008". A withdrawal voids
  its year's earlier guides (the LOW 2020 rule): the Q1 FY09 release's $2.00-2.10 stops, and the no-guide rules apply. FY08's $1.87
  stands as the FY09 anchor to the Q4 FY09 print, through the July 2009 days (the ACN rollover rule).
- **Operating-expense guides only.** From then on every release guides only the fiscal year's operating expenses, in dollars: FY09
  "approximately $27.4 billion", then $26.7-26.9B "including severance charges"; FY10 $26.6-27.0B, $26.2-26.5B (twice) and
  $26.1-26.3B; FY11 $26.9-27.3B (set in the Q4 FY10 release and reaffirmed three times); FY12 $28.0-28.6B (preliminary in the Q3 FY11
  release, reaffirmed in the Q4) and $28.6-29.2B "including Skype and the associated acquisition-related expenses" (Q1 FY12). With no
  revenue guide no margin can be derived (the AAPL and AVGO rule for an outlook's other lines): the ranges are display only, in the
  guide line and catalyst (3), and the margin signal takes the latest quarter's change. With no EPS guide in numbers, each year's
  anchor is the last full year's EPS (the rollover rule): FY09's $1.62 from 2009-07-24, FY10's $2.10 from 2010-07-23, FY11's $2.69
  from 2011-07-22. The preliminary FY2012 range is superseded before fiscal 2012 is current in any model (the Q4 FY11 release
  reaffirms it on the day its print rolls the year), so it changes nothing.
- **No quarter guide: the latest quarter's revenue growth excluding currency** (the NKE and PEP rule) feeds BASE and the growth
  factor. It is the release's growth less the currency effect a filing states: Q2 FY09 +1% (2% less "one percentage point"), Q4 FY09
  -16% (-17% less a "one percentage point decrease") and Q1 FY10 -12% (-14% less a "2 percentage point decrease"). Where a filing calls
  the effect not significant or insignificant (Q3 FY09, Q1 FY11, Q3 FY11, Q4 FY11; the Q2 FY11 10-Q too, though that print's note
  cites only the release), or no filing states it (Q2-Q4 FY10), the reported growth stands: -6% on Q3 FY09, +14%, +6% and +22% on Q2-Q4
  FY10, +25%, +5%, +13% and +8% on Q1-Q4 FY11. Q1 FY12 is +5%: its 10-Q states the effect in dollars ("a favorable foreign currency
  impact of $409 million"), which the first transcription missed (+7%, the reported growth; corrected in "MSFT 2012-2014").
- **The Windows 7 and Office 2010 deferrals are revenue recognition, not one-offs** (the 2008 technology-guarantee rule). Q4 FY09
  deferred $276 million for the Windows 7 Upgrade Option program, Q1 FY10 $1.47 billion for the program and the sales before general
  availability, and Q2 FY10 recognized $1.71 billion; Q3 FY10 deferred $305 million for the Office 2010 Technology Guarantee. The
  prints and BASE take the reported figures, with the company's adjusted ones in the notes (Q1 FY10 $14.39 billion, -4%; Q2 FY10
  $17.31 billion; Q3 FY10 $14.81 billion, +8%; Q1 FY11 +13% "Without the deferral in the prior year" and Q2 FY11 +15% "Without the
  deferred recognition in the prior year").
- **Recast year-ago quarters as each release shows them** (the 2008 rule): Q2 FY08 operating income $6,453M ($6,481M first reported),
  Q3 FY08 $4,290M ($4,409M) and Q4 FY08 $5,679M ($5,684M), after the change in the presentation of foreign currency remeasurement
  gains and losses. The year-ago balance sheets come from that quarter's own release.
- **Segments** (display only): the FY2010 10-K's five (Windows & Windows Live Division, Server and Tools, Online Services Division,
  Microsoft Business Division, Entertainment and Devices Division) replace the FY2009 10-K's in the business line and the bridge from
  2010-07-30.
- **Dividends,** each from the first filing that states the rate: $0.13 a quarter stands through the FY2009 and FY2010 10-Ks (declared
  June 10, 2009 and June 16, 2010), $0.16 from the Q1 FY11 10-Q (declared September 21, 2010; dated 2010-10-29) and $0.20 from the Q1
  FY12 10-Q (declared September 20, 2011; dated 2011-10-21). No 8-K states either increase, so the rate can only lag.
- **Calendar.** Two releases came before the open, Q2 FY09 (Thursday 2009-01-22, 09:04 ET) and Q1 FY10 (Friday 2009-10-23, 08:32 ET),
  and the Q2 FY11 8-K was accepted at 15:57 ET, during the session (Thursday 2011-01-27); the other nine came after the close (16:05-16:28
  ET). The week's date after each print is a Friday, and 2009-10-23 meets that day's close (the print was public before the open).
  Holiday weeks end on Thursdays: 2009-04-09, 2009-07-02, 2009-12-24, 2009-12-31, 2010-04-01, 2010-12-23 and 2011-04-21.
- **Durability is unchanged:** DURABLE, risk 2, with each 10-K's own words. The FY2010 10-K is the first with a risk factor headed "The
  cloud-based computing model presents execution and competitive risks" ("Our competitors are rapidly developing and deploying
  cloud-based services for consumers and business customers"); the FY2011 10-K keeps it and adds hardware and online advertising to the
  business description. CLOUD is live in the registry only from 2012-10-30 (its basis: the earliest verified filing in this archive,
  Accenture's FY2012 10-K), so the watch list stays empty and the words join the "why" (the PEP obesity rule). Microsoft's FY2010 10-K
  is an earlier verified filing of the risk; whether it should move CLOUD's live date is a registry change for every ticker and is left
  to the owner.
- **Adds nothing:** the director and officer 8-Ks (2009-03-10, 2009-09-11, 2009-11-24, 2009-12-04, 2010-05-25, 2010-09-13), the XBRL
  exhibit (2009-03-13), the note offerings and indentures (2009-05-15, 2010-06-08, 2010-06-09, 2010-06-18, 2010-09-27, 2011-02-08), the
  annual meetings (2010-11-19, 2011-11-17 and the 8-K/A of 2011-12-22), the Skype agreement (2011-05-10: "$8.5 billion in cash", no
  guided number; the Q1 FY12 operating-expense guide includes it), the Q2 FY09 release's job cuts and savings ("up to 5,000 jobs",
  "approximately $1.5 billion" off the annual operating expense run rate: no input in the method), and the 10-Qs beyond their currency
  effects and dividends.

Controls: altering one value of each print (its cash and its growth excluding currency), each Q4 print's fiscal-year EPS, each vintage
(its "why" and its first-year EPS), each guide (and removing the withdrawal) and each dividend published from 2009-01-01 changes no
date before its publication and changes the first weekly date on or after it (49 of 49; the Q3 FY11 release's preliminary FY2012 guide
changes nothing). No string or dollar figure of any print, vintage, guide, dividend or source appears in a model dated before it
(149,017 checks over the 209 MSFT models). The firewall at 2009-07-01, 2010-07-01, 2011-07-01 and 2012-01-01 changes no model before its
cutoff. The 53 dates of 2008 rebuild byte-identical; the firewall's new plants (growth excluding currency, an operating-expense guide, a
later withdrawal of every guided year) apply to MSFT only, and no other ticker's file changed.

Seen in the build (method behaviour, not tuned):
- **CHEAP and BUY on all 156 dates.** The tier agrees on 7 or 8 of the 8 robustness variants on every date (the multiples one band
  cheaper read ACCUMULATE on 24 dates and WATCHLIST on 18), the class on all 8 on 154 (RICH under the cheaper multiples on 2010-01-15,
  FAIR on 2010-04-23). The valuation verdict is UNDERVALUED on 137 dates, MODESTLY UNDERVALUED on 12 (2009-09-18 to 2009-11-27 and
  2010-01-22) and FAIRLY VALUED on 7 (2009-12-04 to 2010-01-15).
- **EPS anchors on the last full year:** the FY09 guide midpoint ($2.05) on 2009-01-09 and 2009-01-16 (9.5-9.6x, the 1st percentile of
  its own range), FY08's $1.87 from 2009-01-23 to 2009-07-17 (8.2-13.0x, the 0th-8th), FY09's $1.62 from 2009-07-24 to 2010-07-16
  (14.4-19.1x, the 7th-34th), FY10's $2.10 from 2010-07-23 to 2011-07-15 (11.3-13.6x, the 3rd-17th) and FY11's $2.69 from 2011-07-22
  (8.9-10.2x, the 1st-11th). The window's median P/E falls from 34x to 19x as the bubble years leave it.
- **The floor comes down to the price.** The median of the calendar-year P/E lows is 23x through 2009 ($47 on $2.05, $43 on $1.87, $37
  on $1.62), 21x on 2009-12-31 when 1999 leaves the window, 19x from 2010-01-08 ($31, then $40 on $2.10), 17x on 2010-12-31 and 14x
  from 2011-01-07 ($29, then $38 on $2.69): 2008's 1998-2003 multiples give way to the lows of 2008-2011 (8.6-10.8x on 2011-12-30).
  The stock was 64.5% below the floor on 2009-03-06 ($15.28), within 1.5% of it on six dates from 2010-01-08 to 2010-04-30 (above it
  by 0.3% on 2010-01-15 and 0.6% on 2010-04-23), and 3-40% below it from 2010-07-23.
- **BEAR is -30.4%/yr to 2011-07-22 (the seam) and -13.4%/yr from 2011-07-29**, at the 10th-percentile P/E: $12-21. The price never
  fell below it; Ratio B ran from 0.01 (2009-03-06) to 0.46 (2010-04-23).
- **BASE follows the quarter's growth excluding currency plus the buyback** (1.6-2.9%/yr; no margin step): +8.9%/yr on the Q2 FY09
  guide (2009-01-09 and 2009-01-16), then +2.6% on Q2 FY09, -4.4% on Q3, -14.0% and -13.7% on Q4 (the first deferral), -9.7% on Q1 FY10
  (the $1.47 billion deferral), +16.3% on Q2 FY10 (the recognition), +8.3% on Q3, +24.2% and +24.5% on Q4, +27.5% on Q1 FY11 (against
  the deferral quarter), +7.5% on Q2 FY11 (against the recognition), +15.5% on Q3, +10.6% and +10.9% on Q4 FY11 and +7.9% on Q1 FY12 (+9.9% before the correction).
  The BASE price ran $30-84. The growth factor read -0.50 from 2009-01-09 to Q1 FY10 and on Q3 FY10 and Q2 FY11, +0.19 on Q2 FY10,
  +0.50 on Q4 FY10 and Q1 FY11, +0.09 on Q3 FY11 and -0.39 to -0.50 from Q4 FY11, against an 11.7-13.5% median.
- **BULL and XBULL:** BULL is the window's EPS CAGR (+11.4%/yr over FY99-FY08 to 2009-07-17, +7.4% over FY00-FY09 from the FY2009 10-K,
  +13.2% over FY01-FY10 from the FY2010 10-K, +21.1% over FY02-FY11 from the FY2011 10-K), floored at BASE where BASE is higher (Q2-Q4
  FY10, Q1 and Q3 FY11). XBULL is the FY04-FY06 run (+30.1%/yr) on every date.
- **The market composite** is 1.00-2.05, at the bottom of its grid on 32 dates; the adjusted gap is -0.09 to +2.09.
- **The proxy composite** was 2.00 on Q2 FY09 (revenue +1.6% at BEAR), 2.15 on Q3 FY09, 1.85 on Q4 FY09 and Q1 FY10 (revenue -17.3% and
  -14.2% and the operating margin -542bp and -514bp at BEAR: the downturn and the deferrals), 3.00 on Q2 FY10 (gross margin +442bp and
  the receivables gap -12.2pp at XBULL, revenue +14.4% and the operating margin +904bp at BULL: the recognition), 2.35 on Q3 FY10, 2.45
  on Q4 FY10, 2.80 on Q1 FY11 (revenue +25.3% and the operating margin +925bp at BULL, the receivables gap -13.0pp at XBULL: against
  the deferral quarter), 1.80 on Q2 FY11 (gross margin -515bp and revenue +4.9% at BEAR: against the recognition), 1.95 on Q3 FY11,
  2.15 on Q4 FY11 and 2.00 on Q1 FY12. Unearned revenue scored BASE on every print (-6.6% to +15.4%).

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- the deferrals taken out of the BASE reads (the company's growth without them: Q1 FY10 -2% after currency, Q2 FY10 +4%, Q3 FY10
  +8%, Q1 FY11 +13%, Q2 FY11 +15%), out of the prints' revenue and operating income (the company's adjusted revenue; Q4 FY09's $13,375M
  derived for the test, no company total being published), or out of both, would change no class and no tier (65 to 104 models move);
- reported growth instead of growth excluding currency (Q2 FY09 +2%, Q4 FY09 -17%, Q1 FY10 -14%, and Q1 FY12 +7%) would change nothing;
- keeping the withdrawn FY09 range ($2.05 instead of FY08's $1.87 from 2009-01-23 to 2009-07-17) would change nothing;
- FY09 at $1.70 (Q3 FY09's $0.06 and Q4 FY09's $0.02 of listed items added back) and FY11 at $2.64 (Q3 FY11's $0.05 tax benefit
  out), both derived for the test only, would change nothing;
- the history and the P/E window from FY2002 (no seam; BEAR flat to 2009-07-17 and FY2009's -13.4%/yr after) would change no class
  and no tier.

Judgement calls that could carry hindsight:
- the withdrawal read as voiding the October 2008 range, so that FY08's $1.87 anchors a year whose EPS fell to $1.62 (keeping $2.05
  moves no class);
- the Windows 7 and Office 2010 deferrals as revenue recognition (they swing BASE between -9.7%/yr and +27.5%/yr and the proxy
  composite between 1.80 and 3.00; no class moves);
- reported growth where no filing states the currency effect (Q2-Q4 FY10), and an effect called insignificant read as zero;
- FY2009-FY2011 at GAAP, with the quantified severance, impairments, legal charges and tax benefit left in (no class moves);
- the cloud risk factor kept in the "why" because the registry's CLOUD date (2012-10-30) stands: text only either way, and the date
  itself is the owner's decision;
- the signals, unchanged since 2008 and chosen by a builder who knows how 2009-2011 went; DURABLE (the class label only).

### MSFT 2012-2014: GAAP through the goodwill impairment, the upgrade-offer deferrals, guidance moves to the call, CLOUD on the watch list

```bash
python3 retro/build_msft.py --weekly 2012-01-02 2014-12-31                  # 157 dates, 2012-01-06 .. 2014-12-31
for c in 2012-07-01 2013-01-01 2013-07-01 2014-01-01 2014-07-01 2015-01-01; do python3 retro/tools/firewall.py $c MSFT; done
```

All 45 8-Ks and the 8-K/A filed from January 2012 to December 2014 were checked: the twelve earnings releases read in full, the other
33 8-Ks and the 8-K/A of 2013-05-20 read for guides, figures and dividend rates. The FY2012-FY2014 10-Ks were read for the history, the
segments, the dividends and the risk factors, the nine 10-Qs from Q2 FY12 to Q1 FY15 for their currency effects and dividends (the
10-Q/A of 2012-01-27 only adds the XBRL exhibit), and the FY2005-FY2007 10-Ks for the first year's diluted shares. 312 strings were
checked word for word with `verbatim.py` against their own filings, every number of the prints, guides and vintages was matched to the
text of its cited source, every year-ago figure to the year-ago print (the one difference is the recast below), and the builder
re-derives every print's signal values from its raw figures. Each source's date comes from EDGAR's acceptance time. Thresholds, signals
and the engine are unchanged; the builder gained four encodings (an earlier year restated by a Q4 release, a currency effect stated in
dollars, guidance given only on the call, the CLOUD watch list), decided before any 2012-2014 model was built. Decided before any
2012-2014 outcome was computed:

- **Three vintages, all filed after the close.** The FY2012 10-K (accepted 2012-07-26 16:12 ET, dated 2012-07-27) gives FY2008-FY2012,
  the FY2013 10-K (2013-07-30 16:14 ET, dated 2013-07-31) FY2009-FY2013 and the FY2014 10-K (2014-07-31 17:16 ET, dated 2014-08-01)
  FY2010-FY2014. Each earlier year comes from the latest 10-K that reports it, so the history runs FY2003-FY2012, FY2004-FY2013 and
  FY2005-FY2014; each Q4 print extends it for the week before its 10-K (FY2002-FY2012 on 2012-07-20, FY2003-FY2013 on 2013-07-19,
  FY2004-FY2014 on 2014-07-24). The first year's diluted shares: FY2003's 10,882M (the FY2005 10-K), FY2004's 10,894M (FY2006 10-K)
  and FY2005's 10,906M (FY2007 10-K).
- **FY2011 at the company's $2.64 from the Q4 FY12 release.** Its "2011 As Adjusted (Non-GAAP)" excludes only the $0.05 tax settlement
  (GAAP $2.69): a company figure excluding a one-off (the ACN rule; FY2006's and FY2007's "as adjusted" figures also came from a later
  release). It replaces $2.69 from 2012-07-20 (a Q4 print's new `restates` field, until the FY2012 10-K vintage carries it).
- **FY2012-FY2014 at GAAP.** FY12 enters at $2.00, after the $6.19 billion goodwill impairment of the Online Services Division (announced
  by the 8-K of 2012-07-02). The company's non-GAAP $2.78 also removes the $540 million Windows Upgrade Offer deferral, revenue
  recognition rather than a one-off (the 2008 rule), so it is not a figure excluding a one-off (the NKE FY2007 and AAPL Q4 FY08 rule),
  and no EPS excluding the impairment alone was published ($0.73 a share is an effect; nothing is derived). The year is kept: the
  impairment is under its $16,978M net income (the AAPL FY2003 test). FY13 enters at $2.58 (the company's $2.62 also removes the
  Windows Upgrade Offer recognition; no EPS excluding the $733 million European Commission fine alone; the $900 million Surface RT
  charge, $0.07, is an effect) and FY14 at $2.63 (the Q4 FY14 release gives its "Noted Items", net $(0.03), as effects only).
- **Prints at GAAP.** The company's comparable figures remove deferrals or recognitions as well as one-offs, so no comparable operating
  income replaces GAAP (the PEP Q4 2007 rule): Q4 FY12 reads $192M (the impairment and the deferral in: operating margin -3,447bp),
  Q4 FY13 $6,073M against it (+2,946bp), Q3 FY13 keeps the fine and Q1 FY15 its $1.14 billion of integration and restructuring
  expenses (a Noted Item). The Q1 FY15 release recasts Q1 FY14's cost of revenue to $5,145M ($5,114M first reported), taken as shown
  (the 2008 rule).
- **The upgrade-offer deferrals are revenue recognition, not one-offs** (the 2008 and 2009-2011 rule): the Windows Upgrade Offer
  deferral in Q4 FY12 ($540M), the Q1 FY13 deferral of $1.36 billion (the Windows Upgrade Offer, Windows 8 pre-sales and the Office
  Offer), Q2 FY13's net deferral ($1,329M, less $783M recognized for Windows 8 pre-sales), Q3 FY13's $1,658M net recognition, Q4
  FY13's $782M Office Upgrade Offer recognition and Q1 FY14's $113M Windows 8.1 pre-sales deferral. The prints and BASE take the
  reported figures; the company's non-GAAP revenue and growth go in the notes.
- **Growth excluding currency, an effect stated only in dollars** (new encoding). The Q2 FY12 10-Q states "a favorable foreign currency
  impact of $225 million": growth excluding currency is ($20,885M - $225M) / $19,953M - 1 = +3.5%, rounded half up to +4% as the
  release states growth (`fx_impact_m`; the builder re-derives it). The 10-Qs of Q3 FY12 to Q3 FY13 state only segments' effects (the
  Microsoft Business Division's, Server and Tools'), which are not the quarter's, so the reported growth stands, as it does where no
  filing states an effect (from Q4 FY12; the FY2012 10-K's "insignificant impact on revenue" is the fiscal year's): +6% on Q3 FY12, +4%
  on Q4 FY12, -8% on Q1 FY13, then +3%, +18%, +10%, +16%, +14%, 0% (the release's "(0)%"), +18% and +25% on Q2 FY13 to Q1 FY15.
- **The Q1 FY12 correction.** Reading the Q1 FY12 10-Q (MS52, already a source of that print) for this range found "Revenue for the
  three months ended September 30, 2011 included a favorable foreign currency impact of $409 million", which the 2009-2011
  transcription had missed ("no filing states the quarter's currency effect"). By the same rule Q1 FY12 is +5% ((17,372 - 409) / 16,195
  - 1 = +4.7%), not the reported +7%: a transcription error against the cited filing, corrected in the fact sheet. The 11 dates from
  2011-10-21 to 2011-12-30 were rebuilt and re-run: BASE +7.9%/yr instead of +9.9%, the BASE price $2-3 lower, the conservative
  two-year return about 8pp lower, the growth factor -0.50 instead of -0.49; no class, tier, verdict, Ratio B, adjusted gap, market
  composite or robustness count changes. Those dates had
  been scored on 2026-11-03; their outcomes are refreshed with this range's. The other 2009-2011 10-Qs were re-read for a total effect
  and none was missed (the Q2 FY11 10-Q calls it insignificant: the same +5%).
- **Operating-expense guides, then guidance only on the call.** Every release to Q4 FY13 guides the fiscal year's operating expenses,
  display only: FY12 $28.5-28.9B and $28.3-28.7B ("revising operating expense guidance downward"), FY13 $30.3-30.9B (preliminary in the
  Q3 FY12 release, reaffirmed three times) and $30.2-30.5B "Adjusting for the European Commission fine", FY14 $31.6-32.2B (preliminary)
  and $31.3-31.9B (Q4 FY13). From Q1 FY14 each release says "Microsoft will provide forward-looking guidance in connection with this
  quarterly earnings announcement on its earnings conference call and webcast": the calls are not filings (the AAPL 2020 and NKE rule),
  so nothing is entered, the FY14 range stands as display, the guide line quotes the release (`guide_on_call`), and FY15 has no guide
  in a filing. With no EPS guide in numbers, each year's anchor is the last full year's EPS (the rollover rule): FY11's $2.69 to
  2012-07-13, FY12's $2.00 from 2012-07-20, FY13's $2.58 from 2013-07-19 and FY14's $2.63 from 2014-07-24. The preliminary FY13 and
  FY14 ranges are superseded on the day their year becomes current, so they change nothing.
- **Dividends,** each from the first filing that states the rate: $0.23 a quarter from the 8-K of 2012-09-18 (accepted 16:56 ET, dated
  2012-09-19), $0.28 from the Q1 FY14 10-Q (declared September 16, 2013; dated 2013-10-25; no 8-K states it) and $0.31 from the 8-K
  of 2014-09-17 (06:04 ET, before the open). The 8-K of 2014-03-12 restates $0.28.
- **CLOUD on the watch list from its live date** (new encoding). Each 10-K's cloud risk factor is an event (`cloud_company_acknowledged`,
  id = the 10-K's source): the FY2012 10-K's "Our increasing focus on devices and services presents execution and competitive risks"
  ("Our competitors are rapidly developing and deploying cloud-based services for consumers and business customers. Pricing and
  delivery models are evolving."; "These costs may reduce the operating margins we have previously achieved."), the FY2013 10-K's
  "Our increasing focus on services presents execution and competitive risks" and the FY2014 10-K's (whose costs "will reduce the
  operating margins"). CLOUD is live in the registry from 2012-10-30, so the FY2012 10-K's words stay in the "why" alone from 2012-07-27
  to 2012-10-26 and put CLOUD on the watch list from 2012-11-02 (the first weekly date on or after 2012-10-30, after the Hurricane
  Sandy closure), company-acknowledged, with no market read (the ACN, LOW, NKE, AVGO and PEP rule). The factor pair nets to zero and the
  theme signal stays at 2/4, so only text changes; the theme's market-pricing date (2015-04-23) is after the range, and DURABLE, risk 2,
  stands.
- **Segments** (display only): the FY2012 10-K's five divisions, the FY2013 10-K's (the Windows Division renamed) and, from 2014-08-01,
  the FY2014 10-K's six lines (Devices and Consumer Licensing, Computing and Gaming Hardware, Phone Hardware, new with no prior year,
  Devices and Consumer Other, Commercial Licensing and Commercial Other). The 8-Ks of 2013-09-20, 2013-09-26 and 2013-11-26 recast the
  segments without restating the statements: a segment recast adds nothing, and the bridge keeps the FY2013 10-K's lines until the
  FY2014 10-K (the NKE 2009 rule).
- **Calendar.** All twelve releases came after the close (16:02-16:07 ET; the webcast at 2:30 p.m. Pacific), so each print is dated the
  next trading day, a Friday each time but one: the Q4 FY14 release came on Tuesday 2014-07-22 and is dated Wednesday, so the week's
  date is Thursday 2014-07-24, the day after the print (the AAPL rule). Holiday weeks end on Thursdays: 2012-04-05, 2013-03-28,
  2014-04-17 and 2014-07-03; the week of the Sandy closure ends on 2012-11-02; the range ends on Wednesday 2014-12-31.
- **Anachronism list:** Windows Phone 8 (2012-10-10), Office 365 Home Premium (2012-10-19), Surface RT (2013-04-19), Windows 8.1
  (2013-07-19), Microsoft Azure (2014-04-25) and Surface Pro 3 (2014-07-23) join `taxonomy_eras.json`, each dated from the first
  Microsoft filing that uses it (EDGAR full-text search; each was accepted after the close). No model of any ticker contains them, so no
  output changes.
- **Adds nothing:** the director and officer 8-Ks (2012-02-21, 2012-05-03, 2012-09-18's director retirement, 2012-10-09, 2012-11-16,
  2013-04-18, 2013-05-13 and its 8-K/A, 2013-07-03, 2013-07-11, 2013-08-23 on the CEO's planned retirement, 2013-09-23, the second
  8-K of 2013-09-26, 2014-02-04 on the new CEO, 2014-03-12, 2014-03-20, 2014-07-31, 2014-08-19, 2014-09-17's board changes), the bylaws
  (2012-06-18), the annual meetings (2012-11-29, 2013-11-20, 2014-12-04), the note offerings (2012-11-07, 2013-05-01, 2013-12-06), the
  comprehensive-income recast (2012-11-02), the goodwill impairment 8-K (2012-07-02: no guided number; the charge enters with the Q4
  FY12 print), the ValueAct agreement (2013-08-30), the Nokia agreement (2013-09-03: "accretive to our adjusted earnings per share
  starting in FY15" is not a current-year figure, the UNP merger rule), the restructuring plan (2014-07-17: $1.1-1.6 billion of charges,
  no input in the method), and the 10-Qs beyond their currency effects and dividends.

Controls: altering one value of each print (its cash, its growth excluding currency or its dollar currency effect, its call-only
guidance words), each Q4 print's fiscal-year EPS and the restated FY11, each vintage (its "why" and its first-year EPS), each guide, each
dividend and each cloud event published from 2011-10-21 changes no date before its publication and changes the first weekly date on or
after it (53 of 56; the preliminary FY13 and FY14 ranges change nothing, and the FY2012 10-K's cloud event first acts on 2012-11-02,
CLOUD's live date). No string or dollar figure of any print, vintage, guide, dividend, event or source appears in a model
dated before it (177,294 checks over the 366 MSFT models; the two hits are coincidences: $0.52, a 2009 dividend rate, and $2.00, the
low end of the October 2008 EPS range). The firewall at 2012-07-01, 2013-01-01, 2013-07-01, 2014-01-01, 2014-07-01 and 2015-01-01
changes no model before its cutoff. The 198 dates of 2008-2011 outside the Q1 FY12 correction rebuild byte-identical, and no other
ticker's file changed.

Seen in the build (method behaviour, not tuned):
- **The class moves for the first time.** CHEAP on 109 dates, FAIR on 35 and RICH on 13; BUY on 106, ACCUMULATE on 37 and WATCHLIST on
  14. CHEAP and BUY on all 52 dates of 2012 and on 43 of 2013 (ACCUMULATE on 9 from 2013-05-03 to 2013-07-12); in 2014 FAIR on 35,
  RICH on 13 (2014-04-25 to 2014-07-18) and CHEAP on 5. The verdict is UNDERVALUED on 68 dates, MODESTLY UNDERVALUED on 28, FAIRLY
  VALUED on 38, MODESTLY OVERVALUED on 10 and OVERVALUED on 13.
- **The calls are less robust than in 2008-2011.** The tier agrees on 8 of the 8 variants on 28 dates, 7 on 66, 6 on 37 and 5 on 26;
  the class on 8 on 41, 7 on 85, 6 on 21, 4 on 3 and 3 on 7. The FAIR dates are the least robust (the class on 3-7 of 8). The
  multiples one band cheaper or richer account for most of the disagreement (the tier on 129 and 51 dates).
- **EPS anchors on the last full year:** FY11's $2.69 from 2012-01-06 to 2012-07-13 (10.4-12.1x, the 15th-24th percentile of its own
  range), FY12's $2.00 from 2012-07-20 to 2013-07-12 (13.2-17.8x, the 23rd-61st), FY13's $2.58 from 2013-07-19 to 2014-07-18
  (12.1-17.3x, the 24th-70th) and FY14's $2.63 from 2014-07-24 (16.3-18.9x, the 67th-78th). The window's median P/E falls from 18.9x
  to 14.7x as the 2002-2004 multiples leave it.
- **The floor meets the price.** The median of the calendar-year P/E lows is 14x through 2012 ($37.66 on $2.69, the stock 13-25% below
  it; $28.00 on FY12's $2.00 from 2012-07-20, the stock within -6% and +12% of it), 13x from 2013-01-04 when 2002 leaves the window
  ($26.00; 3-37% above it), and 10x from 2013-07-19, when FY13's $2.58 lowers calendar 2012's and 2013's P/E lows to 10.2x and 10.3x
  ($25.80, then $26.30 on $2.63; 21-89% above it).
- **BEAR is -13.4%/yr to 2012-07-13 and -24.2%/yr from 2012-07-20** (FY11's $2.64 to FY12's $2.00, the impairment year), at the
  10th-percentile P/E: $12-20.
- **BASE follows the quarter's growth plus the buyback** (2.5-2.9%/yr; no margin step): +7.9%/yr on Q1 FY12, +6.9% on Q2, +8.9% on Q3,
  +6.7-6.8% on Q4 FY12, -5.2% on Q1 FY13 (the $1.36 billion deferral; the engine prints it "+-5.2%"), +5.8% on Q2 FY13, +20.8% on Q3
  FY13 (the net recognition), +12.5-12.8% on Q4 FY13, +18.8% on Q1 FY14, +16.8% on Q2 FY14, +2.8% on Q3 FY14, +20.6-20.9% on Q4 FY14
  (with the acquired phone business) and +27.9% on Q1 FY15; the BASE price ran $29-63. The growth factor read -0.50 to Q2 FY13 and on
  Q3 FY14, +0.50 on Q3 FY13, Q1 and Q2 FY14, Q4 FY14 and Q1 FY15, and +0.03 and +0.20 on Q4 FY13, against a 9.7-11.9% median.
- **BULL and XBULL:** BULL is the window's EPS CAGR (+21.1%/yr over FY02-FY11 to 2012-07-13, +15.3% over FY02-FY12 on 2012-07-20,
  +12.6% over FY03-FY12 from the FY2012 10-K, +14.1% and +14.7% over FY03-FY13 and FY04-FY13 from 2013-07-19), floored at BASE where
  BASE is higher (Q3 FY13, Q1 and Q2 FY14, Q4 FY14, Q1 FY15). XBULL is the FY04-FY06 run (+30.1%/yr) to 2014-07-24, then FY09-FY11's
  +27.7% (the FY2014 10-K), floored at BULL (+27.9% on Q1 FY15).
- **Ratio B ran 0.11-1.49,** above 1 on 26 dates from 2014-05-30 (the BEAR downside larger than the BULL upside); the market composite
  1.32-2.67 and the adjusted gap -1.03 to +1.34.
- **The proxy composite** was 2.00 on Q1 and Q2 FY12, 2.35 on Q3 FY12, 2.05 on Q4 FY12 (the operating margin -3,447bp at BEAR: the
  impairment) and Q1 FY13 (revenue -7.9% and the operating margin -830bp at BEAR: the deferral), 2.20 on Q2 FY13, 2.65 on Q3 FY13
  (revenue +17.7% and the operating margin +53bp at BULL: the recognition), 2.25 on Q4 FY13 (the operating margin +2,946bp at XBULL
  against the impairment quarter, the gross margin -510bp at BEAR with the Surface RT charge), 2.45 on Q1 FY14, 2.10 on Q2 FY14 (the
  gross margin -726bp at BEAR), 1.80 on Q3 FY14 (revenue -0.4% and the gross margin -576bp at BEAR), 2.30 on Q4 FY14 and 1.95 on Q1
  FY15 (the gross margin -789bp and the operating margin -900bp at BEAR: the phone business and the restructuring). Unearned revenue
  scored BULL from Q4 FY12 to Q3 FY13 (+17.2% to +29.2%) and BASE otherwise (-1.7% to +16.7%); the receivables gap BULL on every print.

How far each call moves the classes (the 157 dates and the 11 corrected ones rebuilt with one encoding changed; no outcome consulted):
- the company's non-GAAP FY12 $2.78 and FY13 $2.62 instead of GAAP would change no class and 23 tiers (ACCUMULATE to BUY on 14 dates
  in May-July 2013 and March-April 2014, WATCHLIST to ACCUMULATE on 9 in 2014); FY12 at $2.73 (the impairment's $0.73 added back,
  derived for the test only) no class and 22 tiers;
- FY11 kept at GAAP $2.69 would change no class and 6 tiers;
- the deferrals and recognitions taken out of the BASE reads (the company's non-GAAP growth: Q4 FY12 +7%, Q1 FY13 0%, Q2 FY13 +5%, Q3
  FY13 +8%, Q4 FY13 +3%, Q1 FY14 +7%, Q2 FY14 +11%, Q3 FY14 +8%, Q4 FY14 +22%) would change 16 classes (CHEAP to FAIR on 13 dates
  from 2013-05-03 to 2014-02-07, RICH to FAIR on 2014-05-02 and 2014-05-09, FAIR to CHEAP on 2014-08-01) and 21 tiers; taken out of
  the prints' revenue and operating income (the company's non-GAAP figures for both quarters), 19 classes and no tier; out of both,
  38 classes and 21 tiers (118 models move);
- reported growth instead of growth excluding a dollar currency effect (Q1 FY12 +7%, Q2 FY12 +5%) would change nothing;
- CLOUD off the watch list would change nothing (text only).

Judgement calls that could carry hindsight:
- the deferrals and recognitions read as revenue recognition (the 2008 rule, decided before any MSFT model was built): in 2012-2014 it
  moves classes for the first time (up to 38 dates with the company's adjusted figures);
- FY2012 at GAAP with the goodwill impairment in, because the company's figure also removes a deferral (no class moves; 22-23 tiers);
- FY2011 restated to the company's $2.64 from the Q4 FY12 release (no class moves; 6 tiers);
- a currency effect stated in dollars taken off the quarter's revenue, and a segment's effect not used for the quarter (no class moves);
- guidance given only on the conference call left out (the calls are not filings), so FY14 and FY15 have no guide in numbers;
- CLOUD on the watch list from the registry's live date, the 10-K's words read as company acknowledgement and not as market pricing
  (text only); the registry date itself stays the owner's decision (Microsoft's FY2010 10-K is an earlier verified filing of the risk);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2012-2014 went; DURABLE (the class label only).

### MSFT 2015-2017: GAAP through the Windows 10 deferrals, the new revenue standard as a vintage of its own, CLOUD stays on the watch list

```bash
python3 retro/build_msft.py --weekly 2015-01-05 2017-12-31                  # 156 dates, 2015-01-09 .. 2017-12-29
for c in 2015-07-01 2016-01-01 2016-07-01 2017-01-01 2017-07-01 2018-01-01; do python3 retro/tools/firewall.py $c MSFT; done
```

All 36 8-Ks filed from January 2015 to December 2017 were checked: the twelve earnings releases read in full, the other 24 read for
guides, figures and dividend rates. The FY2015-FY2017 10-Ks were read for the history, the segments, the dividends and the risk
factors, the nine 10-Qs from Q2 FY15 to Q1 FY18 for their currency effects and dividends, and the FY2008-FY2010 10-Ks for the first
year's diluted shares. 347 strings were checked word for word with `verbatim.py` against their own filings, every quote in the prints'
notes, the vintages' "why" and the cloud events was found in its own release, 10-Q or 10-K, every number of the prints and vintages was
matched to the text of its cited source, every year-ago figure to the year-ago print (the differences are FY14's restatement and the
recast below), and the builder re-derives every print's signal values from its raw figures. Each source's date comes from EDGAR's
acceptance time. Thresholds, signals and the engine are unchanged; the builder gained three encodings (unearned revenue that is not
comparable, a vintage that keeps an earlier 10-K's words, a receivables caveat), decided on 2026-11-04 before any 2015-2017 model was
built. Decided before any 2015-2017 outcome was computed:

- **Four vintages.** The FY2015 10-K (accepted 2015-07-31 15:07 ET, during the session, so dated that day) gives FY2011-FY2015, the
  FY2016 10-K (2016-07-28 16:12 ET, dated 2016-07-29) FY2012-FY2016 and the FY2017 10-K (2017-08-02 16:15 ET, dated 2017-08-03)
  FY2013-FY2017. The 8-K of 2017-08-03 (16:04 ET, dated 2017-08-04) re-presents FY2016-FY2017 under the new revenue and lease standards,
  adopted from July 1, 2017 by the full retrospective method: diluted EPS $2.56 and $3.25, revenue $91,154M and $96,571M, with restated
  balance sheets and segments. It is a vintage of its own, the latest filing that reports those years (the UNP 2010 and AAPL 2010
  rule); FY2008-FY2015 stay as published, a seam. Its wording (the "why", the business line) and its CLOUD event stay the FY2017 10-K's
  (the AAPL 10-K/A rule; the vintage's new `text_published` gives the 10-K's date). The FY2017 10-K already states the same figures
  under "Expected Impacts to Reported Results"; no weekly date falls between the two filings, so the FY2017 10-K vintage is never the
  latest one on a built date. Each earlier year comes from the latest 10-K that reports it, so the history runs FY2006-FY2015,
  FY2007-FY2016 and FY2008-FY2017; each Q4 print extends it for the week before its 10-K (FY2005-FY2015 on 2015-07-23, FY2006-FY2016 on
  2016-07-21, FY2007-FY2017 on 2017-07-21 and 2017-07-28). The first year's diluted shares: FY2006's 10,531M (the FY2008 10-K),
  FY2007's 9,886M (FY2009 10-K) and FY2008's 9,470M (FY2010 10-K).
- **FY2015 at the company's $2.63, FY2014 restated to $2.64.** The Q4 FY15 release's "2015 As Adjusted (Non-GAAP)" excludes only the
  impairment, integration and restructuring charges ($10,011 million, $1.15 a share; GAAP $1.48) and its "2014 As Adjusted
  (Non-GAAP)" only $127 million of integration and restructuring (GAAP $2.63): figures excluding one-offs (the ACN rule), from
  2015-07-23 (FY14 by `restates`, as FY11 from the Q4 FY12 release) and in the FY2015-FY2017 vintages.
- **FY2016 and FY2017 at GAAP until the recast.** FY16 enters at $2.10 and FY17 at $2.71: the company's $2.79 and $3.31 also remove
  the Windows 10 revenue deferrals (net $6.6 billion and $6.7 billion), revenue recognition rather than one-offs (the 2008 rule), so
  they are not figures excluding only one-offs (the NKE FY2007 rule). No EPS excluding only the impairment and restructuring (FY16
  $0.11, FY17 $0.03) was published, and FY17's "$1.8 billion impact related to the utilization of prior years' losses from
  Microsoft's phone business" ($0.23 a share) is an effect: nothing is derived. On the new basis the deferral is gone and the recast
  gives GAAP only, so $2.56 and $3.25 stand from 2017-08-04 (no adjusted figure on the new basis: the UNP 2010 rule).
- **Prints at GAAP but one.** The Q4 FY15 release gives operating income excluding only "Impairment, Integration, and Restructuring
  Charges" for both quarters, $6,385M against $6,609M (GAAP $(2,053)M and $6,482M), so it replaces GAAP (the PEP Q4 2007 rule): the
  operating margin +52bp, not -3,698bp. From Q1 FY16 every comparable figure also removes the Windows 10 deferrals, so GAAP stands:
  Q4 FY16 reads $3,080M against the impaired $(2,053)M (+2,420bp, as Q4 FY13 against Q4 FY12). Year-ago quarters are taken as each
  release shows them: Q1 FY17's gives Q1 FY16's EPS as $0.61 ($0.57 first reported, before the share-based payment standard adopted
  in Q3 FY16 with effect from July 1, 2015), and Q1 FY18's gives Q1 FY17 under the new standards (revenue $21,928M, operating income
  $6,715M, EPS $0.72; $20,453M, $5,225M and $0.60 first reported).
- **The Windows 10 deferrals are revenue recognition, not one-offs** (the 2008 and 2012-2014 rule): net deferrals of $1,281M in Q1
  FY16, $1,897M in Q2 FY16 (with Halo 5: "Net Impact from Revenue Deferrals"), $1,545M in Q3 FY16, $2,028M in Q4 FY16 and $1,881M,
  $1,976M, $1,467M and $1,383M in FY17. The prints and BASE take the reported figures; the company's non-GAAP revenue, operating income
  and EPS go in the notes. A deferral lowers revenue and raises unearned revenue, so the two signals move in opposite directions.
- **Growth excluding currency.** The release's constant-currency growth of reported revenue where it states one: Q3 FY15 +9% (+6%
  reported), Q4 FY15 -2% (-5%) and Q1 FY18 +11% (+12%). Otherwise the release's growth less the quarter's effect that the 10-Q filed
  with it states: Q2 FY15 +8% + 1% = +9%, Q1 FY16 -12% + 5% = -7%, Q2 FY16 -10% + 5% = -5% ("approximately $1.2 billion or 5%"), Q3
  FY16 -6% + 4% = -2% ("approximately $838 million or 4%"), Q1 FY17 0% + 2% = +2% and Q2 FY17 +1% + 2% = +3%. From Q4 FY16 the releases
  give constant currency only for non-GAAP revenue, with the deferrals removed, which is not the reported revenue's (as a segment's
  effect is not the quarter's); a Q4 has no 10-Q and the Q3 FY17 10-Q states only segments' effects, so the reported growth stands:
  -7% on Q4 FY16, +8% on Q3 FY17 and +13% on Q4 FY17.
- **Q1 FY18 under the new standards.** Its income statement runs against Q1 FY17 as the release restates it. No filing gives the
  September 30, 2016 balance sheet on the new basis, and the recast moves June 30, 2017 unearned revenue from $44,479M to $26,656M, so
  unearned revenue growth is not comparable: the print carries none (`unearned_prior_m` null; the engine's not-reported path scores it
  BASE, and the billings line says "not comparable"). The engine has no such path for receivables, so the gap keeps the Q1 FY17
  release's old-basis balance ($14,561M against $11,129M: +30.8%, +18.9pp against revenue), with the restatement's size in catalyst 4
  (+$2,639M, +13.3% at June 30, 2017; the print's new `receivables_caveat`).
- **No guide in a filing.** Every release says "Microsoft will provide forward-looking guidance in connection with this quarterly
  earnings announcement on its earnings conference call and webcast" (the 2012-2014 rule), so nothing is entered, and each year's
  anchor is the last full year's EPS: FY14's $2.63 to 2015-07-17, FY15's $2.63 from 2015-07-23, FY16's $2.10 from 2016-07-21, FY17's
  $2.71 on 2017-07-21 and 2017-07-28 and the recast $3.25 from 2017-08-04.
- **Dividends,** each from the first filing that states the rate: $0.36 a quarter from the Q1 FY16 10-Q (declared September 15, 2015;
  dated 2015-10-23; no 8-K states it), $0.39 from the Q1 FY17 10-Q (declared September 20, 2016; dated 2016-10-21; the 8-K of
  2016-09-22 covers the bylaws and the meeting date only) and $0.42 from the 8-K of 2017-09-19 (17:14 ET, dated 2017-09-20). Each 10-K
  restates the June rate.
- **CLOUD stays on the watch list.** The FY2015-FY2017 10-Ks keep the FY2014 10-K's risk factor, "Our increasing focus on services
  presents execution and competitive risks" ("At the same time, our competitors are rapidly developing and deploying cloud-based
  services for consumers and business customers. Pricing and delivery models are evolving."; "These costs will reduce the operating
  margins we have previously achieved."), each an event (`cloud_company_acknowledged`). The theme's market-pricing date (2015-04-23,
  Amazon's first AWS segment disclosure) passes in the range, but the registry's evidence names no pricing of Microsoft: re-filing as
  DISRUPTION_EXPOSED needs dated evidence that the market prices cloud substitution of Microsoft's licensed software (as for LOW after
  its theme's pricing date), so the watch list stays, text only, and DURABLE, risk 2, stands.
- **Segments** (display only): the FY2015 10-K's six lines to 2016-07-21; from 2016-07-29 the FY2016 10-K's three (Productivity and
  Business Processes, Intelligent Cloud, More Personal Computing); from 2017-08-04 the recast's restated three. The 8-Ks of 2015-09-29
  and 2015-10-27 recast FY2015 to the new segments without changing the statements: a segment recast adds nothing (the NKE 2009 rule).
- **Calendar.** All twelve releases came after the close (16:04-16:11 ET; the webcast at 2:30 p.m. Pacific). Nine came on Thursdays
  and are dated Friday; the Q2 FY15 release came on Monday 2015-01-26 (dated Tuesday, so the week's date is Wednesday 2015-01-28) and
  the Q4 FY15 and Q4 FY16 releases on Tuesdays (dated Wednesday; the weeks' dates are Thursday 2015-07-23 and 2016-07-21), each the day
  after the print (the AAPL rule). Holiday weeks end on Thursdays: 2015-04-02, 2015-07-02, 2015-12-24, 2015-12-31, 2016-03-24 and
  2017-04-13.
- **Anachronism list:** Intelligent Cloud and Productivity and Business Processes (2015-07-31, the FY2015 10-K's ambitions, accepted
  during the session; EDGAR full-text search) join `taxonomy_eras.json`; Windows 10, HoloLens, Dynamics 365 and Microsoft Teams were
  listed with the 2008 series. Only MSFT models from 2016-07-29 contain the new terms, so no output changes.
- **Adds nothing:** the note offerings (2015-02-12, 2015-11-03, 2016-08-05, 2017-02-03), the bylaws (2015-08-07, 2016-03-17,
  2016-07-05, 2016-09-22 with the meeting date, 2017-06-14), the director and officer 8-Ks (2015-09-11, 2016-07-07, 2017-03-14,
  2017-09-19's director retirement, whose exhibit gives the dividend), the annual meetings (2015-12-03, 2016-12-01, 2017-11-30), the
  derivative settlement notice (2015-12-04), the phone restructurings (2015-07-08 and 2016-05-25: charges, no guided number; they enter
  with the prints), the LinkedIn agreement (2016-06-13; its slides' "Minimally (~1%) dilutive to non-GAAP EPS in FY17 and FY18" is not
  a current-year figure, the UNP merger rule) and completion (2016-12-08), and the 10-Qs beyond their currency effects and dividends.

Controls: altering one value of each print (its cash, its growth excluding currency, its call-only guidance words; Q1 FY18's
receivables caveat and unearned-revenue note), each Q4 print's fiscal-year EPS and the restated FY14, each vintage (its "why" and its
first-year EPS; the recast's FY17 EPS), each dividend and each cloud event published from 2015-01-01 changes no date before its
publication and changes the first weekly date on or after it (55 of 57; the FY2017 10-K vintage changes nothing, as the next day's
8-K replaces it before any weekly date, while its cloud event acts from 2017-08-04 through the recast vintage). No string or dollar
figure of any print, vintage, guide, dividend, event or source appears in a model dated before it (377,426 checks over the 522 MSFT
models; the one new hit, "$1.6 billion" from the Q3 FY16 10-Q, is the frozen engine's own comment on FY07 investment income, and the
two older ones are the 2012-2014 coincidences). The firewall at 2015-07-01, 2016-01-01, 2016-07-01, 2017-01-01, 2017-07-01 and
2018-01-01 changes no model before its cutoff. The 366 dates of 2008-2014 rebuild byte-identical, and no other ticker's file changed.

Seen in the build (method behaviour, not tuned):
- **The class goes RICH and stays.** RICH on 148 dates and FAIR on 8, none CHEAP; AVOID on 145, WATCHLIST on 8 and ACCUMULATE on 3.
  FAIR and ACCUMULATE on the three dates of January 2015 before the Q2 FY15 print; FAIR or RICH, WATCHLIST or AVOID, to 2015-04-17;
  RICH and AVOID on all 141 dates from 2015-04-24 (the Q3 FY15 print). The verdict is OVERVALUED on 147 dates and MODESTLY OVERVALUED on
  9.
- **The calls are robust.** The tier agrees on 8 of the 8 variants on 122 dates, 7 on 19, 6 on 9 and 5 on 6; the class on 8 on 133, 7
  on 16, 6 on 4 and 3 on 3. Every disagreement falls before 2015-10-01 (the class's before 2015-07-17), most of them the multiples one
  band richer (the tier on 34 dates, the class on 15) or cheaper (11 and 8).
- **EPS anchors on the last full year:** FY14's $2.63 from 2015-01-09 to 2015-07-17 (15.3-18.5x, the 57th-81st percentile of its own
  range), FY15's $2.63 from 2015-07-23 to 2016-07-15 (16.2-21.3x, the 68th-99th), FY16's $2.10 from 2016-07-21 to 2017-07-14
  (26.6-34.7x, the 99th-100th), FY17's $2.71 on 2017-07-21 and 2017-07-28 (27.0-27.2x) and the recast $3.25 from 2017-08-04
  (22.3-26.7x, the 99th-100th). The window's median P/E is 14.7x throughout.
- **The floor stays far below.** The median of the calendar-year P/E lows is 10x throughout: $26.30 on $2.63 to 2016-07-15 (the stock
  53-113% above it), $21.00 on $2.10 (166-247% above), $27.10 on $2.71 and $32.50 on $3.25 (123-172% above).
- **BEAR is -24.2%/yr throughout** (FY11's $2.64 to FY12's $2.00, the impairment year), at the 10th-percentile P/E: $13-20.
- **BASE follows the quarter's growth plus the buyback** (no margin step): +27.9%/yr on Q1 FY15 (with the acquired phone business),
  +11.9% on Q2 and Q3 FY15, +0.7-0.8% on Q4 FY15, -4.3% on Q1 FY16, -2.3% on Q2, +0.7% on Q3, -4.2% to -4.6% on Q4 FY16 (the deferrals
  and the strong dollar in the reported growth), then +4.4%, +5.4% and +10.4% on Q1-Q3 FY17, +15.1-15.4% on Q4 FY17 and +13.1% on Q1
  FY18; the BASE price ran $28-63. The growth factor read +0.50 on Q1 FY15, -0.23 on Q2 and Q3 FY15, -0.50 from Q4 FY15 to Q4 FY16,
  -0.49 and -0.39 on Q1 and Q2 FY17, +0.11 on Q3 FY17 and +0.50 on Q4 FY17 and Q1 FY18.
- **BULL and XBULL:** BULL is the window's EPS CAGR (+8.9%/yr over FY05-FY15 on 2015-07-23, +8.4% over FY06-FY15 from the FY2015
  10-K, +5.2% and +3.9% over FY06-FY16 and FY07-FY16 from 2016-07-21), floored at BASE where BASE is higher (Q1-Q3 FY15, from Q1
  FY17). XBULL is FY09-FY11's +27.7%/yr (+27.9% on Q1 FY15, floored at BULL).
- **Ratio B ran from 0.98 to infinite** (BULL below the price on 83 dates from 2015-11-06); the market composite 2.18-3.93 and the
  adjusted gap -1.97 to -0.20.
- **The proxy composite** was 1.95 on Q1 FY15, 2.15 on Q2 FY15 to Q1 FY16, 2.20 on Q2 FY16, 2.00 on Q3 FY16 (revenue -5.5% and the
  gross margin -466bp at BEAR), 2.30 on Q4 FY16 (the operating margin +2,420bp at XBULL against the impaired quarter, revenue -7.1% and
  the gross margin -504bp at BEAR), 2.20 on Q1 FY17, 2.35 on Q2 FY17, 2.40 on Q3 FY17, 2.70 on Q4 FY17 (the gross margin +244bp and
  the operating margin +792bp at BULL) and 2.35 on Q1 FY18. Revenue scored BEAR from Q3 FY15 to Q3 FY17 (-12.2% to +7.6% reported).
  Unearned revenue scored BULL from Q2 FY16 to Q4 FY17 (+17.8% to +38.5%, the deferrals) and BASE otherwise (Q1 FY18 not comparable);
  the receivables gap BULL on every print but Q3 FY15 (-14.4pp, XBULL) and Q1 FY18 (+18.9pp, BASE).

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- FY14 and FY15 at GAAP ($2.63 and $1.48) instead of the company's figures excluding the charges: 128 models move, no class or tier
  changes;
- the company's non-GAAP FY16 $2.79 and FY17 $3.31 until the recast: 54 models move, no class or tier changes (the anchor's P/E
  20.0-26.1x instead of 26.6-34.7x from 2016-07-21, 22.1-22.3x instead of 27.0-27.2x in July 2017);
- no recast vintage (the FY2017 10-K's old basis kept from 2017-08-04): 22 models, no change;
- the deferrals taken out of the BASE reads (the company's non-GAAP constant-currency growth, Q1 FY16 -2% to Q4 FY17 +10%), out of
  the prints' revenue and operating income (the company's non-GAAP figures for both quarters), or both: 105 models each, no change;
- the releases' dollar currency effect (stated with non-GAAP constant currency) taken off reported revenue on Q4 FY16, Q3 FY17 and Q4
  FY17 (-4%, +9%, +14%): 39 models, no change;
- Q1 FY18's unearned revenue against the old-basis balance (-25.9%): 10 models, no change;
- Q4 FY15 operating income at GAAP: 13 models, no change;
- reported growth instead of growth excluding currency: 114 models, 2 classes (FAIR to RICH on 2015-03-13 and 2015-04-17) and 1 tier
  (WATCHLIST to AVOID on 2015-03-06);
- CLOUD off the watch list: 156 models (text only), no change.

Judgement calls that could carry hindsight:
- the Windows 10 deferrals read as revenue recognition (the 2008 rule, decided before any MSFT model was built): GAAP FY16 and FY17
  and the reported prints; no class or tier moves in 2015-2017 with the company's figures, but the anchor's P/E falls by a quarter;
- the 8-K of 2017-08-03 as a vintage of its own (the recast EPS from 2017-08-04) and Q1 FY18's unearned revenue as not comparable,
  with the receivables gap on mixed bases (no class moves);
- FY2015 at the company's $2.63 and FY2014 restated to $2.64 (no class moves);
- constant currency given only for non-GAAP revenue left out (no class moves; reported growth throughout would move 2);
- guidance given only on the conference call left out, so FY15-FY18 have no guide in numbers;
- CLOUD kept on the watch list after its market-pricing date, with no dated evidence of the market pricing Microsoft (text only);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2015-2017 went; DURABLE (the class label only).

### MSFT 2018-2020: the Tax Act and the intangible-property transfer as company figures, FY17 restated again, RICH throughout

```bash
python3 retro/build_msft.py --weekly 2018-01-01 2020-12-31                  # 157 dates, 2018-01-05 .. 2020-12-31
for c in 2018-07-01 2019-01-01 2019-07-01 2020-01-01 2020-07-01 2021-01-01; do python3 retro/tools/firewall.py $c MSFT; done
```

All 29 8-Ks filed from January 2018 to December 2020 were checked: the twelve earnings releases read in full, the other 17 read for
guides, figures and dividend rates. The FY2018-FY2020 10-Ks were read for the history, the segments, the dividends and the risk factors,
the nine 10-Qs from Q2 FY18 to Q1 FY21 for their currency effects, dividends and accounting changes, and the FY2011-FY2013 10-Ks for the
first year's diluted shares. 311 strings were checked word for word with `verbatim.py` against their own filings, the 57 quotes in the
prints' notes, the vintages' "why" and the cloud events were each found in their own release, 10-Q or 10-K, every number of the prints
and vintages was matched to its cited source, every year-ago figure to the year-ago print (the differences are Q2 and Q3 FY17 as
restated under the new standards and FY17's restatement below), and the builder re-derives every print's signal values from its raw
figures. Each source's date comes from EDGAR's acceptance time. Thresholds, signals, engine and builder logic are unchanged (the
builder's docstring only); decided on 2026-11-04 before any 2018-2020 model was built:

- **Three vintages.** The FY2018 10-K (accepted 2018-08-03 11:03 ET, during the session, so dated that day) gives FY2014-FY2018 (FY2016
  on the new revenue and lease standards, FY2014-FY2015 as previously reported: the seam stays), the FY2019 10-K (2019-08-01 16:09 ET,
  dated 2019-08-02) FY2015-FY2019 and the FY2020 10-K (2020-07-30 20:44 ET, dated Friday 2020-07-31; EDGAR files it 2020-07-30)
  FY2016-FY2020. Each earlier year comes from the latest 10-K that reports it, so the history runs FY2009-FY2018, FY2010-FY2019 and
  FY2011-FY2020; each Q4 print extends it for the weeks before its 10-K (FY2008-FY2018 on 2018-07-20 and 2018-07-27, FY2009-FY2019 on
  2019-07-19 and 2019-07-26, FY2010-FY2020 on 2020-07-24). The first year's diluted shares: FY2009's 8,996M (the FY2011 10-K), FY2010's
  8,927M (FY2012 10-K) and FY2011's 8,593M (FY2013 10-K).
- **FY2018 at the company's $3.88, FY2017 restated to $3.29.** The Q4 FY18 release's "2018 As Adjusted (non-GAAP)" excludes only the
  "Net TCJA Impact" ($13,696 million, $1.75 a share; GAAP $2.13), and its "2017 As Adjusted (non-GAAP)" only $306 million of
  restructuring expenses (GAAP $3.25 on the new basis): figures excluding one-offs (the ACN rule), from 2018-07-20 (FY17 by `restates`,
  as FY11 and FY14 before it) and in the FY2018-FY2020 vintages. A company figure exists, so the distorted-year exclusion (NKE FY2018,
  where none was published) does not arise.
- **FY2019 at the company's $4.75, FY2020 at GAAP $5.76.** The Q4 FY19 release's "2019 As Adjusted (non-GAAP)" excludes only the "Net Tax
  Impact of Transfer of Intangible Properties" (a $2,567 million benefit, $0.33) and the TCJA's $157 million charge ($0.02; GAAP $5.06):
  a figure excluding one-offs, benefits included (as FY11's tax settlement). FY20 has no adjusted figure: its $450 million store-closure
  charge stays in, a fraction of the year's net income (the AAPL FY2003 test). FY16 stays at the recast's $2.56 (no adjusted figure on the
  new basis). The tax rates stay as the facts (FY18 54.6% with the TCJA charge, FY19 10.2% with the transfer's benefit): they feed only
  the display-only EPS check (as NKE FY18).
- **Prints at GAAP but one.** Every other adjustment of the range sits below operating income (tax items), so operating income is the
  same either way; Q4 FY18's release gives both quarters excluding only one-offs, $10,379M (no adjustment) against Q4 FY17's $7,988M
  excluding only restructuring (GAAP $7,682M as restated), which replaces GAAP (the PEP Q4 2007 rule, as Q4 FY15). Year-ago quarters are
  taken as each release shows them: Q2-Q4 FY18 run against Q2-Q4 FY17 restated under the new standards (EPS $0.80, $0.70 and $1.03;
  $0.66, $0.61 and $0.83 first reported).
- **Growth excluding currency, from the releases.** Every release states constant-currency revenue growth; the Q3 FY18 10-Q alone
  states a consolidated effect ("a favorable foreign currency impact of 3%", the release's 16% less 3% = 13%). Six releases label the row
  non-GAAP (Q2 FY18, Q4 FY18, Q2 FY19, Q4 FY19, Q2 FY20, Q4 FY20), but the same table's non-GAAP revenue is the reported revenue (every
  adjustment is a tax item or restructuring below revenue), so its constant-currency growth is the reported revenue's. That differs from
  2015-2017, where non-GAAP revenue removed the Windows 10 deferrals and its constant currency was not used; that rule stands for a
  non-GAAP revenue that differs. The reads: +11% on Q2 FY18, +13%, +15%, +18%, +13%, +16%, +14%, +15%, +15%, +16%, +15% and +12% on Q1 FY21.
- **Q2 and Q3 FY18 under the new standards.** No filing gives December 31, 2016 or March 31, 2017 on the new basis, so unearned revenue
  is not comparable (null, the engine's not-reported path) and the receivables keep the year-ago releases' old-basis balances with the
  caveat (the Q1 FY18 rule; gaps of +16.5pp and +18.0pp). From Q4 FY18 both are comparable (June 30, 2017 restated in the release).
- **No guide in a filing.** Every release says guidance is given on the call (`guide_on_call`). The 8-K of 2020-02-26 (17:10 ET, dated
  2020-02-27) quotes the Q2 FY20 call's More Personal Computing range ("between $10.75 and $11.15 billion") and says "we do not expect to
  meet our More Personal Computing segment guidance ... All other components of our Q3 guidance remain unchanged": a segment's range is
  not the quarter's revenue guide (the segment rule), it is withdrawn in the same filing, and the other components are in no filing, so
  it adds nothing (as NIKE's update of 2020-02-04). Each year's anchor is the last full year's EPS: FY17's $3.25 to 2018-07-13, FY18's
  $3.88 from 2018-07-20, FY19's $4.75 from 2019-07-19 and FY20's $5.76 from 2020-07-24.
- **The useful-life change is an accounting estimate, not a one-off.** The FY2020 10-K: "it is estimated this change will increase our
  fiscal year 2021 operating income by $2.7 billion"; the Q1 FY21 10-Q: "an increase in operating income of $927 million and net income
  of $763 million, or $0.10 per both basic and diluted share". No company figure excludes it, so Q1 FY21 stays at GAAP with the effect in
  its note, and an effect is not a guide: no margin step (nothing is derived). The Q3 FY20 release's "COVID-19 had minimal net impact on
  the total company revenue" and the Q4 FY20 release's COVID-19 section are words with no figure to enter (the UNP 2020 rule).
- **Dividends,** each from the first filing that states the rate: $0.46 a quarter from the Q1 FY19 10-Q (declared September 18, 2018;
  dated 2018-10-25), $0.51 from the Q1 FY20 10-Q (declared September 18, 2019; dated 2019-10-24) and $0.56 from the Q1 FY21 10-Q
  (declared September 15, 2020; dated 2020-10-28). No 8-K states them (the 8-Ks of 2018-09-19, 2019-09-19 and 2020-09-21 cover an
  incentive plan, board changes and ZeniMax). Each 10-K restates the June rate.
- **CLOUD stays on the watch list.** The FY2018-FY2020 10-Ks head the risk factor "Our increasing focus on cloud-based services presents
  execution and competitive risks", with the same competitor, margin and offering sentences; each is an event. No dated evidence shows
  the market pricing cloud substitution of Microsoft's licensed software, so the watch list stays, text only, and DURABLE, risk 2,
  stands. No other theme in the registry is live for a software maker (GENAI from 2022-11-30).
- **Segments** (display only): the FY2018, FY2019 and FY2020 10-Ks' three segments, none recast in the range.
- **Calendar.** All twelve releases came after the close (16:02-16:12 ET). The eight Wednesday releases (Q2 FY18, Q1-Q3 FY19, Q1-Q4 FY20)
  are dated Thursday, so the week's date is Friday; the three Thursday releases (Q3 and Q4 FY18, Q4 FY19) are dated Friday, the print's
  own day; the Q1 FY21 release came on Tuesday 2020-10-27, dated Wednesday, so the week's date is Thursday 2020-10-29. Holiday weeks end
  on Thursdays: 2018-03-29, 2019-04-18, 2020-04-09, 2020-07-02 and 2020-12-24; the range ends on Thursday 2020-12-31.
- **Anachronism list:** TCJA (2017-11-13, its first EDGAR full-text hit, a third-party offering statement; Microsoft's first use is the
  Q2 FY18 release and 10-Q) joins `taxonomy_eras.json` beside the Tax Cuts and Jobs Act. Only MSFT models from 2018 contain it, so no
  output changes.
- **Adds nothing:** GitHub (2018-06-04: "minimal dilution of less than 1 percent to earnings per share in fiscal years 2019 and 2020 on a
  non-GAAP basis", not a current-year EPS and an effect, the UNP merger rule), ZeniMax (2020-09-21: "minimal impact to non-GAAP
  operating income in fiscal years 2021 and 2022", words), the TikTok statement (2020-08-03), the Azure blog post (2020-03-31), the store
  closures (2020-06-26: "a pre-tax charge of approximately $450M, or $0.05 per share", entering with the Q4 FY20 print), the debt exchange
  offers (2020-04-30, 2020-05-14, 2020-06-01), the incentive plan (2018-09-19), the board and officer 8-Ks (2019-09-19, 2020-03-13,
  2020-07-01, 2020-07-07), the annual meetings (2018-11-29, 2019-12-05, 2020-12-04), and the 10-Qs beyond their currency effects,
  dividends and the useful-life change.

Controls: altering one value of each print (its cash, its growth excluding currency, its call-only guidance words; Q2 and Q3 FY18's
receivables caveat and unearned-revenue note), each Q4 print's fiscal-year EPS and the restated FY17, each vintage (its "why" and its
first-year EPS), each dividend and each cloud event published from 2018-01-01 changes no date before its publication and changes the
first weekly date on or after it (56 of 56). No string or dollar figure of any print, vintage, guide, dividend, event or source appears
in a model dated before it (622,124 checks over the 679 MSFT models; the three new hits are coincidences: "$0.80 a year", FY11's
dividend, and the 2008 guide ranges "EPS $0.51-0.53" and "$1.78-1.81"); the one later year in a new model is "fiscal 2021", the FY2020
10-K's own words from 2020-07-31, when fiscal 2021 was current. The firewall at 2018-07-01, 2019-01-01, 2019-07-01, 2020-01-01,
2020-07-01 and 2021-01-01 changes no model before its cutoff. The 522 dates of 2008-2017 rebuild byte-identical, and no other ticker's
file changed.

Seen in the build (method behaviour, not tuned):
- **RICH and AVOID on every date.** All 157 dates are RICH, AVOID and OVERVALUED, and all eight robustness variants agree on every one
  (tier and class). The price ran from $87.18 (2018-03-23) to $228.91 (2020-08-28); at the COVID-19 low (2020-03-20, $137.35) the
  multiple was 28.9x, the 94th percentile of its own range.
- **EPS anchors on the last full year:** FY17's $3.25 from 2018-01-05 to 2018-07-13 (26.8-32.4x, the 98th-100th percentile of its own
  range), FY18's $3.88 from 2018-07-20 to 2019-07-12 (25.3-35.8x, the 94th-100th), FY19's $4.75 from 2019-07-19 to 2020-07-17
  (28.1-45.0x, the 94th-100th) and FY20's $5.76 from 2020-07-24 (34.8-39.7x, the 97th-100th). The window's median rose from 14.7x to
  18.3x as the 2008-2010 multiples left it.
- **The floor rose and stayed far below.** The median of the calendar-year P/E lows went from 10x (to 2018-11-16) to 11x, 13x (from
  2019-01-04), 14x and 15x (from 2020-01-03): $32.50 on $3.25, $38.80-50.44 on $3.88, $61.75-71.25 on $4.75 and $86.40 on $5.76, the
  stock 93-224% above it.
- **BEAR is -24.2%/yr throughout** (FY11's $2.64 to FY12's $2.00), at the 10th-percentile P/E: $20-38.
- **BASE follows the quarter's growth plus the buyback:** +13.1%/yr on Q1 and Q2 FY18, +15.1% on Q3 FY18, +16.6-17.0% on Q4 FY18,
  +19.6% on Q1 FY19, +14.6% on Q2 FY19, +17.6% on Q3 FY19, +15.5-15.6% on Q4 FY19, +16.6% on Q1 and Q2 FY20, +17.6% on Q3 FY20,
  +16.3-16.5% on Q4 FY20 and +13.3% on Q1 FY21; the BASE price ran $61-140, below the price on every date. The growth factor read +0.50
  throughout (+0.42 on Q1 FY21).
- **BULL and XBULL:** BULL is floored at BASE on every date (the window's EPS CAGR is lower); XBULL is FY09-FY11's +27.7%/yr to
  2019-07-26, then FY16-FY18's +23.1% (the FY2019 10-K).
- **Ratio B is infinite on 150 dates** (BULL below the price), finite on seven (11.11-454.56: late 2018 and 2020-03-20); the market
  composite 3.71-3.93 and the adjusted gap -1.88 to -1.00.
- **The proxy composite** was 2.00 on Q2 FY18, 2.30 on Q3 FY18, 2.65 on Q4 FY18 and Q1 FY19, 2.50 on Q2 FY19, 2.85 on Q3 FY19 (the
  range's high: revenue, gross margin, operating margin, unearned revenue and receivables at BULL), 2.50 on Q4 FY19 and Q1 FY20, 2.70 on
  Q2 FY20 (the gross margin +477bp at XBULL), 2.65 on Q3 FY20, 2.15 on Q4 FY20 (the gross margin -156bp and the operating margin -154bp,
  the latter with the store-closure charge, both at BASE) and 2.50 on Q1 FY21. Unearned revenue scored BULL from Q4 FY18 to Q3 FY19 (+17.4% to
  +22.7%) and BASE otherwise (Q2 and Q3 FY18 not comparable; +5.3% to +13.7% from Q4 FY19); the receivables gap BASE on Q2 and Q3 FY18
  (the mixed bases) and BULL from Q4 FY18.

How far each call moves the classes (the 157 dates rebuilt with one encoding changed; no outcome consulted): none moves a class or a
tier. FY18 at GAAP $2.13 (129 models move; the anchor's P/E 46.1-65.2x instead of 25.3-35.8x from 2018-07-20), FY17 kept at $3.25 (129),
FY19 at GAAP $5.06 (77), reported growth where the constant-currency row is labelled non-GAAP (79) or on every print (143), Q4 FY18's
operating income at GAAP (14), Q2 and Q3 FY18's unearned revenue against the old-basis balances (38), and CLOUD off the watch list (157,
text only).

Judgement calls that could carry hindsight:
- the tax items read as one-offs, so the company's FY18 $3.88 and FY19 $4.75 replace GAAP (no class moves either way);
- FY17 restated a second time, to the company's $3.29 on the new basis (no class moves);
- constant-currency growth labelled non-GAAP read as the reported revenue's where the table's non-GAAP revenue is the reported revenue
  (no class moves);
- the 8-K of 2020-02-26 read as adding nothing: it withdraws a segment's call range, not a guide in a filing;
- the useful-life change kept in Q1 FY21's GAAP figures, with no margin step from its expected effect;
- CLOUD kept on the watch list, with no dated evidence of the market pricing Microsoft (text only);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2018-2020 went; DURABLE (the class label only).

### MSFT 2021-2023: three-year 10-Ks, the tax items and the Q2 charge as company figures, an FX update in numbers, GENAI on the watch list

```bash
python3 retro/build_msft.py --weekly 2021-01-04 2023-12-31                  # 156 dates, 2021-01-08 .. 2023-12-29
for c in 2021-07-01 2022-01-01 2022-07-01 2023-01-01 2023-07-01 2024-01-01; do python3 retro/tools/firewall.py $c MSFT; done
```

All 31 8-Ks filed from January 2021 to December 2023 were checked: the twelve earnings releases read in full, the other 19 read for
guides, figures and dividend rates. The FY2021-FY2023 10-Ks were read for the history, the segments, the dividends and the risk factors,
the nine 10-Qs from Q2 FY21 to Q1 FY24 for their dividends, the useful-life effects and their risk factors, and the FY2014-FY2016 10-Ks
for the first year's diluted shares. 305 numbers of the prints, vintages, guide and dividends were matched by script to the rows of their
cited filings, 117 strings were checked word for word with `verbatim.py` against their own filings (two misses were fixed before any
model was built: the FY2023 10-K's new revenue sentence, and a guide quote that sat in the 8-K's body, not its exhibit), every year-ago
figure was matched to the year-ago print (no differences), and the builder re-derives every print's signal values from its raw figures.
Each source's date comes from EDGAR's acceptance time. Thresholds, signals and the engine are unchanged; the builder gained one encoding
(GENAI from company evidence), decided on 2026-11-04 before any 2021-2023 model was built. Decided before any 2021-2023 outcome was
computed:

- **Three vintages, all filed after the close, with no five-year summary.** The FY2021 10-K (accepted 2021-07-29 16:21 ET, dated
  2021-07-30), the FY2022 10-K (2022-07-28 16:06 ET, dated 2022-07-29) and the FY2023 10-K (2023-07-27 16:01 ET, dated 2023-07-28) each
  have "ITEM 6. [RESERVED]", so each gives the three years of its income statements and each earlier year comes from the latest 10-K
  that reports it (the ACN FY21 rule): FY2016-FY2018 from the FY2020 10-K's five-year summary, FY2015 from the FY2019 10-K, FY2014 from
  the FY2018 10-K, FY2013 from the FY2017 10-K, FY2012 from the FY2016 10-K, FY2019 from the FY2021 10-K and FY2020 from the FY2022 10-K.
  The history runs FY2012-FY2021, FY2013-FY2022 and FY2014-FY2023; each Q4 print extends it for the week before its 10-K (FY2011-FY2021
  on 2021-07-29, FY2012-FY2022 on 2022-07-28, FY2013-FY2023 on 2023-07-27). The first year's diluted shares: FY2012's 8,506M (the
  FY2014 10-K), FY2013's 8,470M (FY2015 10-K) and FY2014's 8,399M (FY2016 10-K).
- **FY2021-FY2023 at the company's figures.** The Q4 FY21 release's "2021 As Adjusted (non-GAAP)" of $7.97 excludes only the $620
  million net income tax benefit of the India Supreme Court decision on withholding taxes (GAAP $8.05), the Q4 FY22 release's "2022 As
  Adjusted (non-GAAP)" of $9.21 only the $3.3 billion net tax benefit of the transfer of intangible properties from Puerto Rico (GAAP
  $9.65), and the Q4 FY23 release's "2023 As Adjusted" of $9.81 only the Q2 charge ("Severance, hardware-related impairment, and lease
  consolidation costs", $1,171 million; GAAP $9.68): figures excluding one-offs (the ACN rule; tax benefits included, as FY19's). FY20
  stays at GAAP $5.76 and no earlier year is restated. FY23's operating margin uses the company's $89,694M (GAAP $88,523M; the FY15
  precedent). The tax rates stay as the facts (FY21 13.8% and FY22 13.1%, with the benefits): they feed only the display-only EPS check.
- **Prints at GAAP but one.** The tax items sit below operating income, so operating income is the same either way; the Q2 FY23 release
  gives operating income excluding only the Q2 charge for both quarters, $21,570M against Q2 FY22's unadjusted $22,247M (GAAP
  $20,399M), which replaces GAAP (the PEP Q4 2007 rule, as Q4 FY15 and Q4 FY18): the operating margin -211bp, not -433bp. Year-ago
  quarters are taken as each release shows them, and every one matches its own print.
- **Growth excluding currency, from the releases.** Every release states constant-currency revenue growth. Six label the row non-GAAP
  (Q3 FY21 to Q4 FY22); in each the same table's non-GAAP revenue is the reported revenue (the adjustments are tax items, and Q2 and Q4
  FY22 have none), so the row is the reported revenue's (the 2018-2020 rule). The reads: +15% on Q2 FY21, +16%, +17%, +20%, +20%, +21%,
  +16%, +16%, +7%, +10%, +10% and +12% on Q1 FY24.
- **The 8-K of 2022-06-02: a quarter guide in a filing.** Every release gives guidance only on the call (`guide_on_call`). The 8-K of
  2022-06-02 (accepted 09:01 ET, before the open) furnishes a slide, "FY22 Q4 FX Update Through May", whose "Revised Guidance Range" for
  the fourth quarter is revenue $51.94-52.74 billion, operating income $20.60-21.30 billion and diluted EPS $2.24-2.32, after an
  "Additional FX Impact" of $(0.46) billion on revenue. The totals are marked "Calculated as no explicit guidance provided": the April 26
  call guided the three segments, whose revised ranges in the same slide sum to the revenue range. It is the first quarter range in a
  Microsoft filing since the Q1 FY09 release (2008-10-24), and a quarter's revenue range in a filing feeds BASE and the growth factor (the
  2008 encoding, `q_guide`):
  +12.5% to +14.3% on Q4 FY21's $46.152 billion from 2022-06-03 to 2022-07-22, in place of Q3 FY22's +21% excluding currency. It gives no
  fiscal-year range, so FY21's $7.97 stays the anchor. The 8-K of 2020-02-26 added nothing because it gave one segment's call range and
  withdrew it; this one states the quarter's total, so it is entered.
- **The useful-life change of FY23 is an accounting estimate, not a one-off** (the FY2020 rule). The FY2022 10-K: "it is estimated this
  change will increase our fiscal year 2023 operating income by $3.7 billion"; the Q1-Q3 FY23 10-Qs give each quarter's effect ($1.1
  billion, $945 million and $885 million of operating income). No company figure excludes it: GAAP, the effects in the notes, no margin
  step. The FY21 change's quarterly effects (Q2 FY21 $787 million, Q3 FY21 $611 million) are in those prints' notes.
- **No guide in a release; each year's anchor is the last full year's EPS:** FY20's $5.76 to 2021-07-23, FY21's $7.97 from 2021-07-29,
  FY22's $9.21 from 2022-07-28 and FY23's $9.81 from 2023-07-27.
- **Dividends,** each from the first filing that states the rate: $0.62 a quarter from the Q1 FY22 10-Q (declared September 14, 2021;
  dated 2021-10-27), $0.68 from the Q1 FY23 10-Q (declared September 20, 2022; dated 2022-10-26) and $0.75 from the Q1 FY24 10-Q
  (declared September 19, 2023; dated 2023-10-25). No 8-K states them. Each 10-K restates the June rate ($0.56, $0.62, $0.68).
- **CLOUD stays on the watch list.** The FY2021-FY2023 10-Ks keep "Our increasing focus on cloud-based services presents execution and
  competitive risks", with the same competitor, margin and offering sentences; each is an event, text only, and DURABLE, risk 2, stands.
- **GENAI joins the watch list from the FY2023 10-K** (new encoding). GENAI is live from 2022-11-30 and its scope names software seats
  and search, which Microsoft sells, but a theme joins a watch list only from a company filing that names it (the PEP GLP1 rule). The
  FY2021 and FY2022 10-Ks and the Q1-Q3 FY23 10-Qs name AI only as Microsoft's own offerings and their reputational and regulatory risks
  ("Issues in the use of AI in our offerings may result in reputational harm or liability" in the FY2021 10-K, "Issues in the development
  and use of AI may result in reputational harm or liability" from the FY2022 10-K; the FY2023 10-K adds "or competitive harm", still of
  Microsoft's own AI). The FY2023 10-K is the first to name it among
  the business models Microsoft competes with: "We expect AI technology and services to be a highly competitive and rapidly evolving
  market", and some companies compete "using open source AI models" ("Some open source products mimic the features and functionality of
  our products."), pressures that "may cause decreased sales volumes, price reductions, and/or increased operating costs". That is
  company acknowledgement in the sense used for MSFT's CLOUD (a 10-K's competitive-risk wording; `genai_company_acknowledged`, id = the
  10-K's source), with no market read: the registry's dated evidence (ChatGPT, J.P.Morgan on IT services, IBM, Chegg) names no pricing of
  Microsoft. GENAI is on the list from 2023-08-04; the theme signal and factors stay with CLOUD (the ACN CLOUD and PEP GLP1 rule), so only
  text changes, and DURABLE, risk 2, stands. The 10-K's sentence on Microsoft's own AI ("infusing generative AI capabilities into our
  consumer and commercial offerings") is quoted as the offering.
- **Segments** (display only): the FY2021-FY2023 10-Ks' three segments. The FY2023 10-K recasts FY2022's segment revenue ("We have recast
  certain prior period amounts to conform to the way we internally manage and monitor our business": Intelligent Cloud $74,965M and More
  Personal Computing $59,941M, against $75,251M and $59,655M first reported), so FY23's segment growth runs on the recast year. The
  FY2023 10-K also rewrites its revenue sentence ("We generate revenue by offering a wide range of cloud-based solutions, content, and
  other services to people and businesses; ... and designing and selling devices"), and its vintage's "why" quotes that.
- **Calendar.** All twelve releases came after the close (16:02-16:41 ET), on Tuesdays, so each print is dated Wednesday and the week's
  date is Thursday, the day after the print (the AAPL rule). Holiday weeks end on Thursdays: 2021-04-01, 2021-12-23, 2022-04-14 and
  2023-04-06; the range ends on Friday 2023-12-29.
- **Anachronism list:** Xbox Series X (2021-01-27), Windows 11 and Microsoft Viva (2021-07-30), Windows 365 (2021-10-15), Azure OpenAI
  (2022-10-27), Bing Chat and Microsoft Fabric (2023-07-28) join `taxonomy_eras.json`, each dated from the first Microsoft filing that
  uses it (EDGAR full-text search). No model of any ticker contains them, so no output changes.
- **Adds nothing:** the debt exchange offers and the redemption (2021-02-16, 2021-03-02, 2021-03-17, 2021-07-08), the officer and board
  8-Ks (2021-05-20, 2021-06-17), the annual meetings (2021-11-30, 2022-12-16, 2023-12-08), the bylaws (2023-07-03), Nuance (2021-04-12:
  "minimally dilutive (less than 1 percent) in fiscal year 2022" to non-GAAP EPS, not a current-year figure, the UNP merger rule),
  Activision Blizzard (2022-01-18: "accretive to non-GAAP earnings per share upon close", words; the completion of 2023-10-13 and the
  note exchanges of 2023-10-16, 2023-10-30 and 2023-11-06), the workforce reduction (2023-01-18: "a charge of $1.2 billion in the second
  quarter of our 2023 fiscal year, representing a $0.12 negative impact to diluted earnings per share", entering with the Q2 FY23 print),
  the IRS notices of proposed adjustment (2023-10-11: $28.9 billion plus penalties and interest for 2004-2013, contested; no guided
  number), and the 10-Qs beyond their dividends, useful-life effects and risk factors.

Controls: altering one value of each print (its cash, its growth excluding currency, its call-only guidance words), each Q4 print's
fiscal-year EPS, each vintage (its "why" and its first-year EPS), the 8-K guide, each dividend and each CLOUD and GENAI event published from
2021-01-01 changes no date before its publication and changes the first weekly date on or after it (53 of 53). No string or dollar figure
of any print, vintage, guide, dividend, event or source appears in a model dated before it (591,272 checks over the 835 MSFT models; the
four hits are coincidences: "$2.00", the low end of the October 2008 EPS range, and "$2.24" and "$2.48", the annual dividends at $0.56 and
$0.62 a quarter); the one later year in a new model is "fiscal 2023" in the FY2022 10-K's source line (its useful-life change), from
2022-07-29, when fiscal 2023 was current (a warning on 22 dates). The firewall at 2021-07-01, 2022-01-01, 2022-07-01, 2023-01-01,
2023-07-01 and 2024-01-01 changes no model before its cutoff. The 679 dates of 2008-2020 rebuild byte-identical, and no other ticker's file
changed.

Seen in the build (method behaviour, not tuned):
- **RICH on 142 dates, FAIR on 14, none CHEAP.** AVOID on 132, WATCHLIST on 19 and ACCUMULATE on 5. RICH and AVOID on every date to
  2022-08-26; FAIR on 14 dates between 2022-09-23 and 2023-01-20 (2022-09-23 to 2022-11-04, 2022-11-18 and 2022-12-16 to 2023-01-20),
  with ACCUMULATE on five of them (2022-09-30, 2022-10-14, 2022-10-27, 2022-11-04, 2023-01-06); RICH on every date from the Q2 FY23 print
  (2023-01-26). The verdict is OVERVALUED on 142 dates, MODESTLY OVERVALUED on 12 and FAIRLY VALUED on 2 (2022-11-04, 2023-01-06).
- **The calls are less robust around the 2022 low.** The tier agrees on 8 of the 8 variants on 89 dates, 7 on 40, 6 on 12 and 5 on 15;
  the class on 8 on 124, 7 on 13, 6 on 12, 5 on 3 and 3 on 4. The multiples one band richer or cheaper account for most of the
  disagreement (the tier on 67 and 24 dates, the class on 26 and 14).
- **EPS anchors on the last full year:** FY20's $5.76 from 2021-01-08 to 2021-07-23 (36.9-50.3x, the 97th-100th percentile of its own
  range), FY21's $7.97 from 2021-07-29 to 2022-07-22 (31.1-43.1x, the 86th-100th), FY22's $9.21 from 2022-07-28 to 2023-07-21
  (24.0-37.5x, the 63rd-100th) and FY23's $9.81 from 2023-07-27 (32.2-38.5x, the 90th-100th). The window's median P/E rose from 18.3x to
  23.8x and its 75th percentile from 23.0x to 28.7x as the 2011-2013 multiples left it.
- **The floor rose and stayed below.** The median of the calendar-year P/E lows was 15x through 2021 ($86.40 on $5.76, $119.55 on
  $7.97), 16x on 2021-12-31, 17x in 2022 ($135.49 on $7.97, $156.57 on $9.21) and 19x in 2023 ($174.99 on $9.21, $186.39 on $9.81): the
  stock 28.5% (2023-01-06) to 235% above it.
- **BEAR is -24.2%/yr to 2021-07-29 and -2.7%/yr from 2021-08-06** (FY11's $2.64 to FY12's $2.00, then, once the FY2021 10-K drops FY11,
  FY15's $2.63 to FY16's recast $2.56), at the 10th-percentile P/E: $38-158.
- **BASE follows the quarter's growth plus the buyback** (1.2-1.3%/yr; no margin step): +13.3%/yr on Q1 FY21, +16.3% on Q2 FY21, +17.3%
  on Q3, +18.2% on Q4 FY21, +21.2% on Q1 and Q2 FY22, +22.2% on Q3 FY22, +14.6% on the 8-K's Q4 FY22 range, +17.2-17.3% on Q4 FY22 and Q1
  FY23, +8.3% on Q2 FY23, +11.3% on Q3 and Q4 FY23 and +13.3% on Q1 FY24; the BASE price ran $135-300, above the price on 22 dates
  (2022-08-26 to 2023-01-20). The growth factor read +0.50 from Q2 FY21 to Q3 FY22 (+0.42 on Q1 FY21), +0.19 on the 8-K's range, +0.34
  and +0.24 on Q4 FY22 and Q1 FY23, -0.50 on Q2 FY23, -0.36 on Q3 and Q4 FY23 (-0.26 on 2023-07-27) and -0.16 on Q1 FY24, against a
  7.8-13.6% median.
- **BULL and XBULL:** BULL is floored at BASE to 2023-01-20, then the window's EPS CAGR (+15.2%/yr over FY13-FY22, +14.3% over FY13-FY23
  on 2023-07-27, +15.7% over FY14-FY23 from the FY2023 10-K). XBULL is FY16-FY18's +23.1%/yr to 2021-07-23, then FY19-FY21's +29.5%.
- **Ratio B is infinite on 66 dates** (BULL below the price) and below 1 on four (2022-10-14, 2022-10-27, 2022-11-04, 2023-01-06;
  0.86-0.99); the market composite 2.32-3.93 and the adjusted gap -1.75 to -0.08.
- **The proxy composite** was 2.45 on Q2 and Q3 FY21, 2.65 on Q4 FY21 (the gross margin +213bp at BULL), 2.45 on Q1-Q3 FY22, 2.15 on Q4
  FY22 and Q1 FY23 (revenue +12.4% and +10.6% and the operating margin -178bp and -173bp at BASE), 2.00 on Q2 FY23 (revenue +2.0% at
  BEAR), 2.35 on Q3 FY23 (revenue +7.1% at BEAR, both margins at BULL) and 2.50 on Q4 FY23 and Q1 FY24. Unearned revenue scored BASE on
  every print (+6.9% to +13.0%) and the receivables gap BULL on every print; revenue scored BULL from Q2 FY21 to Q3 FY22.

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- FY21-FY23 at GAAP ($8.05, $9.65, $9.68) instead of the company's figures: 127 models move, 7 classes (RICH to FAIR on 2022-09-16,
  2022-11-11, 2022-11-25 and 2022-12-09, FAIR to CHEAP on 2022-10-27, 2022-11-04 and 2023-01-06), 12 tiers and 9 verdicts;
- reported growth instead of constant currency where the row is labelled non-GAAP: 57 models, 4 classes (FAIR to RICH on 2022-09-23,
  2022-09-30, 2022-10-07 and 2022-10-21) and 3 tiers; on every print: 132 models, 10 classes (FAIR to RICH) and 4 tiers;
- no quarter guide from the 8-K of 2022-06-02 (BASE on Q3 FY22's +21%): 8 models, no change;
- Q2 FY23 operating income at GAAP: 13 models, no change; FY23's operating margin at GAAP: 23 models, no change;
- GENAI off the watch list: 22 models (text only), no change.

Judgement calls that could carry hindsight:
- the tax benefits and the Q2 charge read as one-offs, so the company's FY21 $7.97, FY22 $9.21 and FY23 $9.81 replace GAAP (the ACN rule,
  decided long before; at GAAP, 7 classes move around the 2022 low);
- constant-currency growth labelled non-GAAP read as the reported revenue's where the table's non-GAAP revenue is the reported revenue
  (the 2018-2020 rule; 4 classes move without it);
- the 8-K of 2022-06-02 read as a quarter guide in a filing, though the company calls its totals calculated (no class moves);
- GENAI read as company-acknowledged from the FY2023 10-K's competitive wording, which names AI as a competitive market and competitors'
  open source AI models but never says AI replaces Microsoft's products (text only either way);
- the useful-life change kept in GAAP, with no margin step from its expected effect;
- CLOUD kept on the watch list, with no dated evidence of the market pricing Microsoft (text only);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2021-2023 went; DURABLE (the class label only).

### MSFT 2024-2026: the OpenAI impact at GAAP, a revenue guide in an investor-metrics deck, CHEAP for the first time since 2014

```bash
python3 retro/build_msft.py --weekly 2024-01-01 2026-10-30                  # 148 dates, 2024-01-05 .. 2026-10-30
for c in 2024-07-01 2025-01-01 2025-07-01 2026-01-01 2026-07-01 2026-11-01; do python3 retro/tools/firewall.py $c MSFT; done
```

All 24 8-Ks and the 8-K/A filed from January 2024 to October 2026 were checked: the twelve earnings releases read in full, the other
twelve 8-Ks and the 8-K/A read for guides, figures and dividend rates. The FY2024-FY2026 10-Ks were read for the history, the segments,
the dividends and the risk factors, the nine 10-Qs from Q2 FY24 to Q1 FY27 for their dividends and accounting changes (none), and the
FY2017-FY2019 10-Ks for the first year's diluted shares. 304 numbers of the prints, vintages, guide and dividends were matched by script to
the rows of their cited filings, 116 strings were checked word for word with `verbatim.py` against their own filings, every year-ago
figure was matched to the year-ago print (no differences), and the builder re-derives every print's signal values from its raw figures.
Each source's date comes from EDGAR's acceptance time. Thresholds, signals and the engine are unchanged; the builder gained two display
paths (a quarter guide with revenue alone; a cloud margin sentence under a heading of its own), decided on 2026-11-04 before any 2024-2026
model was built, and the 835 dates of 2008-2023 rebuild byte-identical with them. Decided before any 2024-2026 outcome was computed:

- **Three vintages, each filed minutes after its Q4 release.** The FY2024 10-K (accepted 2024-07-30 16:06 ET, three minutes after the
  release; dated 2024-07-31), the FY2025 10-K (2025-07-30 16:11 ET; dated 2025-07-31) and the FY2026 10-K (2026-07-29 16:08 ET; dated
  2026-07-30) each carry their year on the print's own date, so no weekly date sees a Q4 print's fiscal-year figures before the 10-K (the
  three Q4 prints' fiscal-year EPS change nothing). Item 6 is reserved; each 10-K gives three income-statement years and each earlier year
  comes from the latest 10-K that reports it (FY2016-FY2018 still from the FY2020 10-K's five-year summary). The history runs FY2015-FY2024,
  FY2016-FY2025 and FY2017-FY2026; the first year's diluted shares are FY2015's 8,254M (the FY2017 10-K), FY2016's 8,013M (FY2018 10-K)
  and FY2017's 7,832M (FY2019 10-K).
- **FY2024-FY2026 at GAAP.** FY24 enters at $11.80 (the Q4 FY24 release publishes no adjusted figure). From the Q1 FY26 release the
  company's non-GAAP figures exclude the "impact from investments in OpenAI": losses of $523 million, $939 million, $583 million and
  $1,575 million in the quarters of FY25 ($0.49 for the year), then a $3.1 billion loss, a $7.6 billion net gain with the OpenAI
  recapitalization, a $14 million loss and a $480 million gain in FY26 ($0.67 net for the year). That is an equity investee's result in every
  quarter, not a one-off, so the company's FY25 $14.13 and FY26 $17.28 (first published in the Q4 FY26 release) are not figures excluding
  only one-offs (the NKE FY2007 rule, as the Windows 10 deferral years of 2015-2017): FY25 stays at $13.64 and FY26 at $17.95. No year is
  excluded: FY26's net gains ($4,963 million) are a fraction of its $133,749 million net income (the AVGO FY2018 mirror test). The tax
  rates stay as the facts (FY26 19.4% on a pre-tax income that carries the gains): display only.
- **Prints at GAAP but one.** The OpenAI impact sits in other income and expense, below operating income. The Q2 FY24 release gives Q2
  FY23 excluding only the Q2 charge ($21,570M) against Q2 FY24's unadjusted $27,032M, which replaces GAAP for the year-ago quarter (the
  PEP Q4 2007 rule; the Q2 FY23 print's own figure). Activision Blizzard is in the reported growth from Q2 FY24, as the acquired phone
  business was in 2014.
- **Growth excluding currency, from the releases:** +16% on Q2 FY24, +17%, +16%, +16%, +12%, +15%, +17%, +17%, +15%, +15%, +17% and +19% on
  Q1 FY27. From Q3 FY26 the releases print one wide table, whose revenue row (no adjustment) gives the constant-currency growth.
- **A quarter guide in an investor-metrics deck.** Every release gives guidance only on the call. Two 8-Ks restate a call's outlook in a
  slide deck when the segments change. The 8-K of 2024-08-21 ("FY25 Investor Metrics") gives the Q1 FY25 ranges by segment only, "As
  provided on July 30, 2024" and mechanically updated; no total is stated and none is derived, so it adds nothing (the segment rule). The 8-K
  of 2026-09-02 ("FY27 Segments and Investor Metrics"; accepted 16:30 ET, dated 2026-09-03) states the Q1 FY27 outlook as provided on July
  29, 2026, including "Total Company Revenue of $89.85 to $90.95 billion": a quarter's revenue range in a filing, entered as a next-quarter
  guide (the 2008 encoding, as the 8-K of 2022-06-02): +15.7% to +17.1% on Q1 FY26's $77.673 billion from 2026-09-04 to 2026-10-23, in place
  of Q4 FY26's +17%. It gives cost of revenue and operating expense ranges but no operating income or EPS range, and "Operating margin
  Expected to remain relatively flat year-over-year" in words, so there is no margin step and nothing is derived; the builder shows a
  quarter guide with revenue alone. FY26's $17.95 stays the FY27 anchor.
- **No guide in a release; each year's anchor is the last full year's EPS:** FY23's $9.81 to 2024-07-26, FY24's $11.80 from 2024-08-01,
  FY25's $13.64 from 2025-08-01 and FY26's $17.95 from 2026-07-31.
- **Dividends,** each from the first filing that states the rate: $0.83 a quarter from the Q1 FY25 10-Q (declared September 16, 2024;
  dated 2024-10-31), $0.91 from the Q1 FY26 10-Q (declared September 15, 2025; dated 2025-10-30) and $0.98 from the Q1 FY27 10-Q (declared
  September 15, 2026; dated 2026-10-29). No 8-K states them; each 10-K restates the June rate ($0.75, $0.83, $0.91).
- **CLOUD and GENAI stay on the watch list, in each 10-K's own words.** From the FY2024 10-K the cloud competitor sentence moves into
  "Business model competition" ("Our competitors continue to develop and deploy cloud-based services for consumers and business customers,
  and pricing and delivery models are evolving."; from FY2025 "We and our competitors continue to devote significant resources to
  developing and deploying cloud-based strategies and services ..."), and the margin sentence sits under a risk factor of its own ("Our
  focus on cloud-based and AI services presents execution and competitive risks." in FY2024 and FY2025, "Our cloud and AI strategy
  requires substantial investments ..." in FY2026), so the CLOUD event carries that heading too (`margin_heading`, text only). The GENAI
  event quotes the AI bullet of the same section (FY2024: "We expect AI technology and services to be a highly competitive and rapidly
  evolving market, and new competitors continue to enter the market."; FY2025: "AI technology and services are a highly competitive and
  rapidly evolving market ..."; FY2026 adds "Our AI offerings compete with AI products from hyperscalers, open-source offerings, and frontier
  model providers, some of which are also current or potential partners.") and its open-source rivals ("using open source AI models", then
  "developing, making available, or using AI models that are open"). No dated evidence in the registry or the fact sheet shows the market
  pricing generative-AI substitution of Microsoft's software seats or search, and no press coverage is added (the ACN rule after 2023), so
  GENAI is not re-filed: DURABLE, risk 2, stands; the theme signal stays with CLOUD.
- **Segments** (display only): each 10-K's three segments; the FY2025 10-K's carry the recast of the 8-K of 2024-12-03 (Microsoft 365
  commercial brought together in Productivity and Business Processes; "no impact on our consolidated balance sheets, consolidated income
  statements, or consolidated cash flows statements"), so its growth runs on FY24 as recast. The FY27 two-segment structure (Agents and
  Infra, Devices and Consumer; the 8-K of 2026-09-02) and its recast of the FY2026 10-K (the 8-K of 2026-10-28, dated 2026-10-29) add nothing
  (the NKE 2009 rule): the bridge keeps the FY2026 10-K's three segments to the end of the range.
- **Calendar.** All twelve releases came after the close (16:03-16:08 ET). The Q2 and Q4 FY24 releases came on Tuesdays (dated Wednesday;
  the week's date Thursday 2024-02-01 and 2024-08-01), the Q3 FY24 release on Thursday 2024-04-25 (dated Friday 2024-04-26, the print's own
  day, public before that day's open: the AAPL 2011 rule), and from Q1 FY25 every release on a Wednesday (dated Thursday; the week's date
  Friday). Holiday weeks end on Thursdays: 2024-03-28, 2025-04-17, 2025-07-03, 2026-04-02, 2026-06-18 and 2026-07-02. The last date is
  2026-10-30, the last complete week: the series was built on 2026-11-04, so a rebuild after the close of 2026-11-06 adds the week of
  2026-11-02. The newest dates have no two-year outcome yet.
- **Anachronism list:** Azure AI Foundry (the FY2025 10-K, 2025-07-31), Agents and Infra (the 8-K of 2026-09-02, dated 2026-09-03) and
  Microsoft Foundry (the annual report of 2026-10-21, dated 2026-10-22) join `taxonomy_eras.json`, each dated from the first Microsoft filing
  that uses it (EDGAR full-text search). "Devices and Consumer" is left out: the FY2014-FY2016 segments "Devices and Consumer Licensing" and
  "Devices and Consumer Other" would match it. No model of any ticker contains the new terms, so no output changes.
- **Adds nothing:** the cybersecurity incident 8-K and its 8-K/A (2024-01-19, 2024-03-08: no figure), the Cruise impairment (2024-12-11:
  "approximately $800 million in the second quarter of fiscal year 2025 ... recorded in other income and expense", entering with the Q2
  FY25 print, which publishes no figure without it), the OpenAI partnership blog with the Q1 FY26 release (2025-10-29: a stake "valued at
  approximately $135 billion", "an incremental $250B of Azure services"; no guided number), the 2024-12-03 and 2026-10-28 segment recasts, the
  officer and director 8-Ks (2025-01-22, 2025-09-30, 2026-05-14, 2026-06-05), the bylaws (2025-07-01), the annual meetings (2024-12-11,
  2025-12-08 with the 2026 Stock Plan), and the 10-Qs beyond their dividends.

Controls: altering one value of each print (its cash, its growth excluding currency, its call-only guidance words), each vintage (its "why"
and its first-year EPS), the 8-K guide, each dividend and each CLOUD event (its quote and its margin heading) and GENAI event published from
2024-01-01 changes no date before its publication and changes the first weekly date on or after it (55 of 58); the three Q4 prints'
fiscal-year EPS change nothing, because each 10-K carries the year on the same date. No string or dollar figure of any print, vintage,
guide, dividend, event or source appears in a model dated before it (698,561 checks over the 983 MSFT models; the hits are year-ago revenues
that the later releases' wide tables repeat ($70,066M, $76,441M, $77,673M, each public a year earlier), the generic "Constant Currency" and
a coincidence, "$29.63", a 2009 close, against the Q1 FY27 guide's "$29.6"). The firewall at 2024-07-01, 2025-01-01, 2025-07-01, 2026-01-01,
2026-07-01 and 2026-11-01 changes no model before its cutoff. The 835 dates of 2008-2023 rebuild byte-identical, and no other ticker's file
changed.

Seen in the build (method behaviour, not tuned):
- **RICH on 104 dates, CHEAP on 33 and FAIR on 11.** AVOID on 89, BUY on 35, WATCHLIST on 17 and ACCUMULATE on 7. RICH on every date from
  2024-01-05 to 2026-01-09 but 2025-04-04 and 2025-04-17 (FAIR, the April 2025 low); FAIR from 2026-01-16 to 2026-01-30; CHEAP from 2026-02-06,
  the first CHEAP date since 2014-02-07, on 33 of the last 39 dates (FAIR on 2026-04-17, 2026-04-24, 2026-05-15, 2026-05-29, 2026-10-09 and
  2026-10-16). The verdict is OVERVALUED on 104 dates, MODESTLY OVERVALUED on 5, FAIRLY VALUED on 11, MODESTLY UNDERVALUED on 15 and
  UNDERVALUED on 13.
- **The calls are less robust than in 2018-2020.** The tier agrees on 8 of the 8 variants on 51 dates, 7 on 63, 6 on 17 and 5 on 17; the
  class on 8 on 75, 7 on 48, 6 on 6, 5 on 13, 4 on 4 and 3 on 2. The multiples one band richer or cheaper account for most of the
  disagreement (the tier on 73 and 48 dates, the class on 52 and 25).
- **EPS anchors on the last full year:** FY23's $9.81 from 2024-01-05 to 2024-07-26 (37.5-47.7x, the 98th-100th percentile of its own
  range), FY24's $11.80 from 2024-08-01 to 2025-07-25 (30.5-43.5x, the 72nd-100th), FY25's $13.64 from 2025-08-01 to 2026-07-24
  (26.2-38.4x, the 42nd-100th) and FY26's $17.95 from 2026-07-31 (25.9-29.8x, the 42nd-69th). The window's median P/E rose from 23.8x to
  27.9x as the 2014-2016 multiples left it (27.0-27.3x on FY26's $17.95), its 75th percentile from 28.7x to 31.8x.
- **The floor rose to the price.** The median of the calendar-year P/E lows was 20x on FY23's $9.81 ($196.20), 20-21x on FY24's $11.80
  ($236.00-247.80), 21-22x on FY25's $13.64 ($286.44-300.08) and 21x on FY26's $17.95 ($376.95): the stock 18.9% to 138.3% above it.
- **BEAR is -2.7%/yr to 2025-07-25 and flat from 2025-08-01** (FY15's $2.63 to FY16's recast $2.56, then no EPS decline in FY16-FY25 or
  FY17-FY26: the 0% cap), at the 10th-percentile P/E: $158-379.
- **BASE follows the quarter's growth plus a shrinking buyback** (1.3%/yr to 0.6%/yr): +13.3%/yr on Q1 FY24, +17.3% on Q2, +18.3% on Q3,
  +17.1% on Q4 FY24 and Q1 FY25, +13.1% on Q2 FY25, +16.1% on Q3, +17.8% on Q4 FY25 and Q1 FY26, +15.8% on Q2 and Q3 FY26, +17.6% on Q4 FY26,
  +17.0% on the 8-K's Q1 FY27 range and +19.6% on Q1 FY27. The BASE price ran $300-701, above the price on 59 dates. The growth factor read
  -0.20 to +0.41 against a 13.6-14.9% median.
- **BULL and XBULL:** BULL is the window's EPS CAGR (+15.7%/yr over FY14-FY23, floored at BASE on Q2 and Q3 FY24, +18.2% over FY15-FY24,
  +20.4% over FY16-FY25, +20.7% over FY17-FY26); XBULL is FY19-FY21's +29.5%/yr throughout.
- **Ratio B is infinite on 28 dates** (BULL below the price) and below 1 on 40 (0.31-0.97: 2025-04-04 and most dates from 2026-01-30); the
  market composite 1.82-3.93 and the adjusted gap -1.81 to +0.83.
- **The proxy composite** was 2.65 on Q2 FY24 (the gross margin +152bp at BULL), 2.45 on Q3 and Q4 FY24, 2.30 on Q1-Q3 FY25 (the operating
  margin -100bp at BASE on Q1, revenue +12.3% and +13.3% at BASE on Q2 and Q3) and 2.45 from Q4 FY25 to Q1 FY27. Unearned revenue scored
  BASE on every print (+4.4% to +16.2%) and the receivables gap BULL on every print.

How far each call moves the classes (the 148 dates rebuilt with one encoding changed; no outcome consulted):
- FY25 and FY26 at the company's OpenAI-adjusted $14.13 and $17.28, from the Q4 FY26 release that first gives them: 14 models move, 5
  classes (CHEAP to FAIR on 2026-08-28, 2026-09-25, 2026-10-02, 2026-10-23 and 2026-10-30), 1 tier and 10 verdicts;
- the 8-K of 2024-08-21's segment ranges summed into a Q1 FY25 guide ($63.80-64.80 billion, derived for the test only): 10 models, no change;
- no quarter guide from the 8-K of 2026-09-02: 9 models, no change;
- Q2 FY24's year-ago operating income at GAAP: 12 models, no change;
- GENAI off the watch list: 118 models (text only), no change;
- reported growth instead of constant currency on every print: 95 models, no class or tier, 11 verdicts.

Judgement calls that could carry hindsight:
- the OpenAI impact read as a recurring investment result, so FY25 and FY26 stay at GAAP with the recapitalization gains in (5 classes
  move in August-October 2026 with the company's figures);
- the 8-K of 2026-09-02 read as a quarter guide in a filing and the 8-K of 2024-08-21 as adding nothing, because one states a total and the
  other only segments (no class moves either way);
- GENAI kept on the watch list without re-filing: the 2025-2026 software derating is in the registry only as a hindsight note, and no press
  coverage is added after 2023 (text only);
- CLOUD kept on the watch list in each 10-K's restructured wording (text only);
- the signals, unchanged since 2008 and chosen by a builder who knows how 2024-2026 went; DURABLE (the class label only).

## XOM (ExxonMobil): the ninth ticker, in staging

The XOM series is built apart from ACN, UNP, LOW, AAPL, NKE, AVGO, PEP and MSFT and shares nothing with them but the machinery: its own
fact sheet (`retro/facts/XOM.json`), builder (`retro/build_xom.py`) and engine (`retro/templates/xom_engine.py.tmpl`, the MSFT engine with
integrated oil and gas signals). The method is still r2. No fact, parameter, outcome or finding of another ticker enters an XOM model, and
neither does today's live profile of XOM in `data/business_profiles.json` (a 2026 judgement). Outputs go to `staging/retrospective/XOM/`,
beside the others, with the same `index.json` and their own `SERIES.md`.

```bash
python3 retro/build_xom.py --weekly 2008-01-01 2008-12-31                   # 53 dates, 2008-01-04 .. 2008-12-31
python3 retro/build_xom.py --weekly 2009-01-05 2012-12-31                   # 209 dates, 2009-01-09 .. 2012-12-31
python3 retro/build_xom.py --weekly 2013-01-07 2017-12-31                   # 260 dates, 2013-01-11 .. 2017-12-29
python3 retro/build_xom.py --weekly 2018-01-01 2020-12-31                   # 157 dates, 2018-01-05 .. 2020-12-31
python3 retro/build_xom.py --weekly 2021-01-04 2023-12-31                   # 156 dates, 2021-01-08 .. 2023-12-29
python3 retro/build_xom.py --weekly 2024-01-01 2026-10-30                   # 148 dates, 2024-01-05 .. 2026-10-30
for d in staging/retrospective/XOM/20*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series XOM
python3 retro/tools/firewall.py 2008-07-01 XOM
python3 retro/tools/firewall.py 2009-01-01 XOM
python3 retro/tools/firewall.py 2011-01-01 XOM
python3 retro/tools/firewall.py 2013-01-01 XOM
python3 retro/tools/firewall.py 2013-07-01 XOM
python3 retro/tools/firewall.py 2015-01-01 XOM
python3 retro/tools/firewall.py 2016-01-01 XOM
python3 retro/tools/firewall.py 2017-07-01 XOM
python3 retro/tools/firewall.py 2018-01-01 XOM
python3 retro/tools/firewall.py 2018-07-01 XOM
python3 retro/tools/firewall.py 2019-07-01 XOM
python3 retro/tools/firewall.py 2020-10-01 XOM
python3 retro/tools/firewall.py 2021-01-01 XOM
python3 retro/tools/firewall.py 2021-07-01 XOM
python3 retro/tools/firewall.py 2022-07-01 XOM
python3 retro/tools/firewall.py 2023-07-01 XOM
python3 retro/tools/firewall.py 2024-01-01 XOM
for c in 2024-07-01 2025-01-01 2025-07-01 2026-01-01 2026-07-01 2026-11-01; do python3 retro/tools/firewall.py $c XOM; done
```

The 10-Ks from FY1999 to FY2007 were read for the history and the decade's signal values (the FY1999-FY2001 10-Ks are plain-text
filings, the first on the merged Exxon Mobil basis), with the Q4 releases of 2003-2006 for the per-share figures they publish excluding
special items; every 8-K and 10-Q of January 2007 to January 2009 (36 filings, the two analyst-meeting transcripts and slide decks among
them) and the Q2 2001 10-Q for the split were read in full, with no delegated transcription. 173 strings were checked with `verbatim.py` against their own filings,
and every raw value of the six prints was matched again by script to the text of its release. Each source's date comes from EDGAR's
acceptance time (converted from UTC; before 2003 EDGAR gives the filing date only). Decided on 2026-11-05, before any XOM model was built or
any XOM outcome computed:

- **Fiscal calendar.** ExxonMobil's fiscal year is the calendar year. The four dates of January 2008 have no 2007 EPS yet: FY06's stands
  for 2007 and the first days of 2008 (the rollover rule), until the Q4 2007 print adds FY07.
- **Prices on the as-of share basis** (the UNP rule). ExxonMobil last split on 2001-07-19 (two-for-one, approved on May 30, 2001 for
  shareholders of record on June 20, 2001, first stated in the Q2 2001 10-Q, filed 2001-08-13), so for every 2008 date Yahoo's series is the
  price as traded: $92.08 on 2008-01-04. The split restates the per-share facts published before it: 1998 EPS excluding special items (the
  FY2000 10-K, $2.49 → $1.245) and the first year's diluted shares (the FY1999 10-K's 3,581M for 1997 and the FY2000 10-K's 3,533M for 1998,
  doubled). The 1997 split precedes every per-share fact in the fact sheet.
- **Release timing.** The Q2 2007, Q4 2007, Q2 2008 and Q3 2008 earnings 8-Ks were accepted before the open (09:06-09:12 ET; the webcast
  at 10 a.m. Central), the Q3 2007 and Q1 2008 ones during the session (09:41 and 10:03 ET), so each print is dated its release day. The Q4
  2007 print came on Friday 2008-02-01 before the open, so that day is the week's date and meets its close (the AAPL 2011 rule); the
  Thursday prints date their weeks the next day: 2008-05-02, 2008-08-01 and 2008-10-31. The FY2007 10-K, accepted 2008-02-28 16:17 ET, is
  dated 2008-02-29.
- **History: each year from the latest filing that reports it.** The FY2006 10-K (accepted 2007-02-28 14:53 ET) gives 2002-2006 per share
  and 2004-2006 income statements; 2003 revenue comes from the FY2005 10-K, 2002 from the FY2004 10-K, 2001 from the FY2003 10-K, 2000 from
  the FY2002 10-K, 1999 from the FY2001 10-K, 1998 from the FY2000 10-K and 1997 from the FY1999 10-K. The Q4 2007 release extends it with
  2007 from 2008-02-01, and the FY2007 10-K moves the window to 1998-2007. Three seams stay in, as published (the LOW and PEP rule): the 2002
  reclassification of the coal and copper businesses as discontinued operations (the FY2002 10-K's 2000 revenue is $231,846M, the FY2001
  10-K's $232,748M; 1999 and earlier keep them), the netting of purchases and sales with the same counterparty from 2006 (2006 revenue
  +1.9% on a 2005 that still includes $30,810M of them), and the 1999 merger, accounted for as a pooling of interests, so 1997 and 1998 are
  the combined companies as later 10-Ks restate them.
- **Revenue is total revenues and other income**, the one revenue line the releases publish (the Q4 2003 release heads it "Revenue"); the
  history takes it from the 10-K income statements, so the quarter's growth and the history's median growth share a basis. It includes
  sales-based taxes and the equity companies' income.
- **EPS** is diluted EPS from continuing operations before extraordinary items and the cumulative effect of accounting changes (the NKE
  rule). The company's earnings per share assuming dilution excluding special items replace it where a filing publishes them (the ACN rule):
  1998 $1.245 (FY2000 10-K, after the split), 1999 $1.19 (FY2001 10-K), 2000 $2.37 and 2001 $2.25 (FY2002 10-K: merger effects, discontinued
  operations and other special items), 2002 $1.69 (Q4 2003 release), 2003 $2.56 (Q4 2004 release: the $2,230M tax settlement, the $1,700M
  Ruhrgas gain and the accounting change), 2004 $3.97 (Q4 2005 release), 2005 $5.35 and 2006 $6.55 (Q4 2006 release), 2007 $7.28 (no special
  items). 1997 stays GAAP at $1.64 (FY2001 10-K): the FY1999 10-K gives its earnings excluding special items in dollars only, and nothing is
  derived. **No year is excluded:** the largest listed items, 2003's benefits, are under that year's $17,030M of earnings without them (the
  AAPL FY2003 test and its AVGO mirror). The special items of 1998 include write-downs and inventory effects of the oil-price fall; they
  are the company's own list, taken as published.
- **No guide in numbers.** No release, 10-Q, 10-K or other 8-K of 2007-2008 gives an earnings, revenue, volume or margin guide in numbers.
  The analyst meetings of 2007-03-07 and 2008-03-05 (8-Ks of 2007-03-13 and 2008-03-11, with transcripts) show production capacity as
  charts and words and a capital "investment profile in the range of $25 billion to $30 billion per year", a multi-year range that is not
  a current-year input (the LOW rule). So, on every date:
  - current-FY EPS: the last full year's EPS stands: FY06's $6.55 to 2008-01-25, FY07's $7.28 from the Q4 2007 print (the UNP and NKE rule);
  - BASE growth and the growth factor: the latest quarter's revenue growth, as reported (the UNP rule; no filing states a currency effect on
    revenue, so it is the reported growth, the MSFT and PEP fallback): +2.8% (Q3 2007), +29.6% (Q4 2007), +34.0% (Q1 2008), +40.4% (Q2 2008),
    +34.6% (Q3 2008);
  - no margin step: the margin signal takes the latest quarter's change.
  - The Q3 2008 release's "Damage repairs and lower volumes across all business lines associated with the hurricanes are expected to reduce
    fourth quarter earnings by about $500 million." is shown in the guide line and feeds no input (the UNP quarter-guide rule).
- **Dividends,** each from the first filing that states the rate: $0.32 a quarter (FY2006 10-K, declared January 31, 2007), $0.35 from the Q2
  2007 release, $0.35 again in the FY2007 10-K (declared January 30, 2008), $0.40 from the Q2 2008 release.
- **Signals.** Six, with ACN's weights: oil-equivalent production growth (0.20), petroleum product sales growth (0.20), revenue growth (0.15,
  as reported), chemical prime product sales growth (0.15), the pre-tax margin change (0.15: income before income taxes on total revenues and
  other income) and the theme slot at 2/4. The three volumes are the ones each release reports for its three segments (Upstream, Downstream,
  Chemical), as stated, each against the year-ago quarter in the same release; the fact sheet keeps the raw figures and the builder
  re-derives each value.
- **Thresholds by rule T** over the decade of the FY2006 10-K, the vintage public on 2008-01-04: 1997-2006. No 10-K published by then
  reports 1996 on the merged basis (the FY1999 10-K's statements and operating summary start in 1997), so each signal has the nine changes
  1998-2006 (rule T takes the annual values the filings report, the AVGO rule), each from the latest 10-K published by then that reports
  both years. The FY2001 10-K states no oil-equivalent line, so its 1997 and 1998 production is liquids plus gas at the 6-to-1 conversion the
  later 10-Ks state (4,271.5 for 1998 against the FY2002 10-K's stated 4,272). The values are in the fact sheet (`rule_t`); the builder
  recomputes the thresholds and refuses to build if the engine's differ.

  | Signal | 1998-2006 | BEAR / BASE / BULL / XBULL |
  |---|---|---|
  | oil-equivalent production | -1.64, -0.87, 0.99, -0.51, -0.4, -0.83, 0.29, -3.56, 4.23 % | -7 / -4 / -1 / 4 % |
  | petroleum product sales | 1.14, 0.16, -10.06, -0.28, -2.68, 2.76, 3.31, 0.11, -3.62 % | -20 / -10 / 0 / 3 % |
  | revenue growth | -15.91, 9.36, 25.45, -8.22, -3.89, 20.65, 20.79, 24.37, 1.88 % | -41 / -16 / 9 / 25 % |
  | chemical prime product sales | -0.88, 7.0, 1.4, 0.56, 3.2, -0.15, 4.6, -3.64, 2.14 % | -9 / -4 / 1 / 7 % |
  | pre-tax margin change | -246.2, -111.3, 562.5, -32.9, -270.3, 439.3, 88.2, 219.6, 181.5 bp | -630 / -270 / 90 / 560 bp |

- **Durability: CYCLICAL, risk 2, the first ticker that is not DURABLE.** The house taxonomy's CYCLICAL is a "good business whose earnings
  ARE the cycle (commodities, ...)", and the 10-K says so in its own words: "The oil and gas business is fundamentally a commodity business.
  This means the operations and earnings of the Corporation and its affiliates throughout the world may be significantly affected by changes
  in oil, gas and petrochemical prices and by changes in margins on gasoline and other refined products". The "why" quotes that, the
  principal business and "The energy and petrochemical industries are highly competitive". The kind changes the class label only (CHEAP reads
  CYCLICAL, RISK PRICED IN); the price state and the tier do not depend on it. No disruption theme in `taxonomy_eras.json` is live for an oil
  and gas producer in 2008 (ENERGY_TRANSITION, which carries oil, gas and refining, from 2015-12-12), so the 10-K's "the competitiveness of
  alternative hydrocarbon or other energy sources" and its laws "addressing alternative energy sources and the risks of global climate change"
  stay in the "why" (the PEP obesity rule); the watch list is empty and the builder refuses events until a theme encoding is decided.
- **Segment bridge and EPS check** (display only): the 10-K's three segments (Upstream, Downstream, Chemical, by sales and other operating
  revenue) with each one's growth, the total from the fallback growth applied to the last year; the EPS check runs on the pre-tax margin.
- **Adds nothing:** the reserves releases (2007-02-15, 2008-02-15), the Financial and Operating Reviews (2007-03-23, 2008-03-24), the
  analyst-meeting 8-Ks beyond the words above, the Valdez 8-Ks (2007-05-25, 2007-10-29, 2008-06-30), the Cerro Negro 8-Ks (2007-07-02,
  2007-09-12), the German gas transport sale (2008-07-03: a gain "reported in third quarter 2008 results", no guided number), the officer,
  director and compensation 8-Ks, and the 10-Qs beyond their dividends.
- **Anachronism list:** ExxonMobil names first seen in its filings after the start of 2008 (Liza, Payara, Yellowtail, Low Carbon Solutions,
  Exxtend, Proxxima) join `taxonomy_eras.json`, each dated from the first ExxonMobil filing that uses it (EDGAR full-text search). No
  existing model of any ticker contains them, so no output changes. XOM's source ids are `XO1`-`XO20`.

Controls: altering one value of each print, vintage, dividend and the split changes no date before its publication and changes the first
weekly date on or after it (12 of 12, the Q4 2007 print's FY07 actuals among them). Rebuilding the 2008 dates of ACN, UNP, LOW, AAPL, NKE, PEP
and MSFT and the 2009 dates of AVGO changes nothing. A scan of the 53 models for the figures, notes and dividends of every later print and
vintage finds none before its publication (0 of 665).

Seen in the build (method behaviour, not tuned):
- **CHEAP and BUY on all 53 dates**, robustness 7 of 8 on the four January dates and 8 of 8 from 2008-02-01.
- **BASE carries the oil price.** With no guide, BASE is the latest quarter's revenue growth plus the buyback (diluted shares fell 2.0%/yr
  over 1997-2006, 2.5% over 1997-2007 from the Q4 2007 print, 2.7% over 1998-2007): +4.8%/yr to 2008-01-25 (Q3 2007 revenue +2.8%), +32.1% from the Q4 2007 print (+29.6%), +32.3% from
  the FY2007 10-K, +36.7% from Q1 2008, +43.1% from Q2 2008 and +37.3% from Q3 2008, so from February BULL is BASE (the decade CAGR is 16.6%,
  21.7% over 1998-2007) and the growth factor sits at its +0.5 cap (-0.5 in January). This is UNP's fuel-surcharge pattern.
- **BEAR is the 2002 fall** (-24.9%/yr: 2001's $2.25 to 2002's $1.69), at the 10th-percentile P/E (10.2-10.4x): $38-42. XBULL is the
  2002-2004 run (+53.3%/yr).
- **The EPS anchor is the last full year.** FY07's $7.28 stands all year while nine-month 2008 EPS was already $7.11 (the Q3 2008 release),
  so the multiple of 8.6-12.9x is on a year already passed (the AAPL and NKE pattern).
- **The window holds the low-earnings years.** The 1998-2002 multiples (24-27x lows in 1998-1999) set the 75th and 90th percentiles at
  18.7-22.7x and 26.3-29.7x, and the median of the calendar-year lows at 12-14x (11x on 2008-12-31, when 1998 leaves the window). The EPP gap
  is -29% (2008-10-10) to +8%; the stock's own P/E ranks at the 0th-44th percentile.
- **The proxy composite** is 2.00 on Q3 2007 (every signal at BASE), 2.65 on Q4 2007 (production +0.6% and chemical sales +3.3% at BULL,
  revenue +29.6% at XBULL) and 2.10 on Q1-Q3 2008 (production -5.6%, -7.8% and -8.2% at BEAR, revenue +34-40% at XBULL; on Q3 2008 chemical
  sales -9.9% at BEAR and the pre-tax margin +261bp, with the German gain in it, at BULL). The market composite is 1.00-1.93, the adjusted gap
  +0.13 to +1.73 and Ratio B 0.09-0.49.

How far each call moves the classes (the 53 dates rebuilt with one encoding changed; no outcome consulted):
- GAAP EPS in every year instead of the company's figures excluding special items would change no class and no tier;
- BASE on the latest quarter's oil-equivalent production growth instead of revenue growth (-5.5% to +3.3%/yr instead of +4.8% to +43.1%)
  would change no class and no tier, and so would both together; any revenue line between them (sales and other operating revenue grew
  +28.9% in Q4 2007, against +29.6% for total revenues and other income) is bracketed by that test.

Judgement calls that could carry hindsight:
- the signals, chosen by a builder who knows that production fell through 2008 and demand late in the year: one volume per segment, as each
  release reports them (rule T then sets the thresholds mechanically);
- CYCLICAL rather than DURABLE (the class label only), the first departure from the other eight;
- total revenues and other income as the revenue line, and the company's figures excluding special items, 1998's write-downs and inventory
  effects among them (no class moves either way);
- the oil-equivalent production of 1997-1998 from liquids and gas where the 10-K states no oil-equivalent line, and nine rule-T values;
- leaving the alternative-energy and climate-change wording in the "why" rather than reading it as an early energy-transition theme (the
  registry's live date stands; text only either way).

### XOM 2009-2012: the 2009 trough as an anchor, the XTO merger, production outlooks in numbers

Every 8-K, 10-Q and 10-K of February 2009 to February 2013 was read (65 filings, the four analyst-meeting transcripts and slide decks
among them). The prints were extracted by script from each release and checked twice: 255 strings with `verbatim.py` against their own
filings, and every volume against the release's own narrative and its Investor Relations Data Summary. Decided on 2026-11-05, before any
2009-2012 date was built or scored:

- **Four 10-K vintages, each with a Q4 print before it.** The FY2008 10-K (accepted 2009-02-27 16:16 ET, dated 2009-03-02), FY2009
  (2010-02-26 16:17 ET, dated 2010-03-01), FY2010 (2011-02-25 16:07 ET, dated 2011-02-28) and FY2011 (2012-02-24 16:08 ET, dated
  2012-02-27). The FY2010 10-K/A of 2011-02-28 adds the auditors' conformed signature and corrects typographical errors ("no changes in
  any of the financial or other information"), so it adds nothing. Each Q4 release extends the history with its year until the 10-K.
- **Release timing.** Every earnings 8-K of the period was accepted before the open (08:55-09:29 ET) except the Q4 2011 release (09:45 ET,
  during the session). The Q4 2008 print came on Friday 2009-01-30, so that day is the week's date and meets its close (the 2008 rule); the
  Q4 2009 and Q4 2010 prints came on Mondays and the Q4 2011 print on a Tuesday, so those weeks are dated the next day (2010-02-02,
  2011-02-01, 2012-02-01); the Thursday prints date their weeks the Friday.
- **The 2009 accounting changes, as published.** From 2009 ExxonMobil reports noncontrolling interests inside income before income taxes
  and counts unvested share-based awards in basic EPS (both adopted on January 1, 2009). Each release from Q1 2009 shows its year-ago quarter
  restated, which the print takes as the release shows it (the MSFT recast rule: Q1 2008 income before income taxes $20,474M against
  $20,192M first reported). The FY2009 10-K restates 2005-2008 EPS ($5.70, $6.60, $7.26, $8.66) and 2007-2008 income before income taxes;
  each year comes from the latest filing that reports it. One seam stays: 2005 and 2006 keep the company's figures excluding special items
  ($5.35, $6.55), first published on the earlier basis and never republished.
- **EPS:** a year with special items takes the company's per-share figure excluding them from the latest filing that publishes one, a year
  without them GAAP from the latest 10-K (the 2008 rule, unchanged). 2008 is $8.47 from the Q4 2008 release (the German gas transport gain
  and the Valdez charges, $1,160M net; GAAP $8.69), restated to $8.44 by the Q4 2009 release under the new EPS rule ('restates': the history
  carries it from 2010-02-02, the FY2009 10-K from 2010-03-01); 2009 is $4.01 (a $140M Valdez interest charge; GAAP $3.98); 2007 is $7.26
  from the FY2009 10-K; 2010 and 2011 had no special items ($6.22, $8.42). The Q2 2012 release's "net gain of $7.5 billion associated with
  divestments and tax-related items" (the Japan restructuring among them) is not a special item and no figure excluding it is published, so
  it stays in (the ACN Russia rule): it lifts the Q2 2012 pre-tax margin by 573bp (XBULL).
- **Still no earnings, revenue or margin guide in numbers**, so the 2008 rules apply on every date: the last full year's EPS stands, BASE
  takes the latest quarter's revenue growth, and the margin signal the latest quarter's change. From 2009 each analyst meeting states the
  current year's production in numbers: "we expect production in the range of 4 million oil-equivalent barrels per day in 2009" (8-K of
  2009-03-11, after the close: from 2009-03-12), "we continue to expect production to grow between 3% and 4% this year" (8-K of 2010-03-17,
  after the close: from 2010-03-18), "Volumes growth remains strong • 2010-2011: 3 to 4 percent" (8-K of 2011-03-15) and "Volume outlook:
  2011 to 2012: down 3 percent" at 2011 prices (8-K of 2012-03-14). Method r2 has no volume input, so each is shown in the guide line and
  catalyst (3) for its year and feeds nothing (the UNP volume-guide rule). Each release's statement of the next quarter's share purchases
  ("currently anticipated to equal $5 billion in the fourth quarter of 2010") goes into the capital-return line, display only.
- **The XTO Energy merger** (agreement 2009-12-13, 8-K accepted 2009-12-14 17:24 ET; closed 2010-06-25 with 416 million shares issued) adds
  no guided number. Acquisitions stay in, as published (the PEP rule): production grows 20.5% in Q3 2010 and 18.9% in Q4 2010, and the
  diluted share count of 2010 (4,897M) is above 2009's (4,848M).
- **Dividends,** each from the first filing that states the rate: $0.40 (FY2008 10-K), $0.42 from the Q2 2009 release, $0.44 from the Q2
  2010 release, $0.47 from the Q2 2011 release, $0.57 from the Q2 2012 release, and each January declaration in its 10-K.
- **Durability: CYCLICAL, risk 2, unchanged.** From the FY2009 10-K the risk factors are rewritten: "The oil, gas, and petrochemical
  businesses are fundamentally commodity businesses", and a new risk factor, "Climate change and greenhouse gas restrictions", says such
  rules "could make our products more expensive and reduce demand for hydrocarbons, as well as shifting hydrocarbon demand toward relatively
  lower-carbon sources such as natural gas" (from the FY2010 10-K: "could make our products more expensive, lengthen project implementation
  times, and reduce demand for hydrocarbons"). ENERGY_TRANSITION is live only from 2015-12-12, so these words join the "why" (the PEP obesity
  rule, as MSFT's cloud risk factor of 2010). XOM's FY2009 10-K (2010-03-01) is an earlier verified company acknowledgment of the theme than
  the registry's basis (the Paris Agreement); whether to move ENERGY_TRANSITION's date is left to the owner, and moving it would change text
  only unless dated evidence showed the market pricing it.
- **Adds nothing:** the Valdez 8-K of 2009-06-19 (an after-tax charge "of about $150 million will be recorded in the second quarter of
  2009", booked as $140M), the XTO 8-Ks (2009-12-14, 2010-03-16, 2010-06-25), the Baltimore verdict (2011-07-07), the reserves releases, the
  Financial and Operating Reviews, the director-fee, bylaw, annual-meeting, officer and compensation 8-Ks, and the 10-Qs beyond their
  dividends.

Controls: altering one value of each new print (with each Q4 print's full-year actuals and the Q4 2009 restatement of 2008), vintage,
dividend and production outlook changes no date before its publication and changes the first weekly date on or after it (33 of 33). The 53
dates of 2008 rebuild byte-identical. A scan of all 262 XOM models for the figures and notes of every later print, vintage, dividend and
outlook finds none before its publication (0 of 19,842).

Seen in the build (method behaviour, not tuned):
- **2009: CHEAP and BUY on all 52 dates**, robustness 8 of 8. FY08's $8.47 is the anchor all year (7.6-10.7x); BASE is negative from the Q4
  2008 print (-24.3%, -41.8%, -42.7% and -36.9%/yr: revenue -27% to -46%), but BULL is the decade CAGR (21-24%) and XBULL the 2002-2004 run
  (+53.3%) at the window's 75th and 90th percentile multiples (17-19x and 20-26x), so Ratio B stays at 0.11-0.23 and the EPP gap at -24% to
  +7%. From the Q1 2009 print to 2010-01-29 (40 dates) BASE lies below BEAR (BASE -42.7% to -36.9%/yr against BEAR's -24.9%, the decade's
  worst year capped at 0): BASE prices of $33-40 under BEAR's $42-45. The frozen rules order nothing between them.
- **The trough becomes the anchor and the bear.** From the Q4 2009 print FY09's $4.01 is the EPS anchor (16.7x) and the 2009 fall (-52.5%:
  $8.44 to $4.01) the decade's worst year, so BEAR is -52.5%/yr for two years: a BEAR price of $9 to 2011-01-28, $13 on FY10's $6.22 and
  $18 on FY11's $8.42. It stays until 2009 leaves the window. RICH and AVOID on all 12 dates of 2010-02-02 to 2010-04-23 (Ratio B 2.2-3.6).
- **BASE follows revenue, so it follows the oil price:** +45.2%/yr from the Q1 2010 print (revenue +41.0%; CHEAP and BUY on 13 dates),
  +28.4% from Q2 2010 (CHEAP, ACCUMULATE or WATCHLIST), +20.0% from Q3 2010 (FAIR on 3 dates, RICH on 11 to 2011-01-28 at 17.6-19.7x FY09's
  EPS); from the Q4 2010 print, on FY10's $6.22: CHEAP on all 50 dates to 2012-01-13 (+20.8% to +39.7%/yr; FAIR on 2012-01-20); on FY11's $8.42 from
  2012-02-01, CHEAP and FAIR alternate to July (BASE +19.2% then +12.6%), FAIR on the 14 dates of the Q2 2012 print (+5.3%) and RICH on the
  10 of Q3 2012 (revenue -7.7%, BASE -3.9%).
- **Totals over the 209 dates:** CHEAP 148, FAIR 28, RICH 33; BUY 90, ACCUMULATE 74, WATCHLIST 20, AVOID 25; robustness 8 of 8 on 92 dates,
  4-5 of 8 on 25 (mostly 2012, where the price sits near the BASE case).
- **The proxy composite** ranges from 1.55 (Q2 2009) to 3.25 (Q3 2010, with production +20.5% at XBULL); the market composite from 1.38 to
  2.82.

How far each call moves the classes (the 209 dates rebuilt with one encoding changed; no outcome consulted):
- GAAP EPS in every year instead of the company's figures excluding special items would change 21 classes (1 in 2010, 2 in 2011, 18 in
  2012, mostly CHEAP to FAIR from December 2011 to June 2012, as 2008's $8.66 deepens BEAR to -54%) and 37 tiers;
- BASE on the latest quarter's oil-equivalent production growth instead of revenue growth would change 70 classes (33 in 2010 and 30 in
  2011, mostly CHEAP to RICH from the Q1 2010 print) and 74 tiers: in 2010-2011 the revenue fallback, not the business, decides the class;
- both together: 84 classes and 99 tiers.

Judgement calls that could carry hindsight (in addition to the 2008 list, which stands):
- the production outlooks kept as display only, although they are the one forward number the company gives (method r2 has no volume input;
  using one would be a new method version);
- the company's figures excluding special items, 2008's and 2009's among them (21 classes move without them), and the 2005-2006 seam;
- the Q2 2012 gains left in, as no figure excluding them was published;
- the climate-change risk factor left in the "why" rather than putting ENERGY_TRANSITION on the watch list before its registry date (text only).

### XOM 2013-2017: special items leave the releases, the oil-price fall at GAAP, ENERGY_TRANSITION on the watch list

Every 8-K, 10-Q and 10-K of February 2013 to January 2018 was listed (77 filings: 56 8-Ks, one 8-K/A, 15 10-Qs and five 10-Ks). The
earnings releases with their Investor Relations Data Summaries, the five 10-Ks and the five analyst-meeting transcripts and slide decks
were read for the facts; every other 8-K and the 10-Qs were checked for a guided number or a dividend (none earlier than the releases).
The prints were extracted by script from each release and checked twice: 450 strings with `verbatim.py` against their own filings (every
quoted sentence is taken from the converted filing by an exact search), and every volume against the release's own Investor Relations
Data Summary. Decided on 2026-11-05, before any 2013-2017 date was built or scored:

- **Five 10-K vintages, each with a Q4 print before it.** FY2012 (accepted 2013-02-27 16:05 ET, dated 2013-02-28), FY2013 (2014-02-26
  16:07 ET, dated 2014-02-27), FY2014 (2015-02-25 16:26 ET, dated 2015-02-26), FY2015 (2016-02-24 16:09 ET, dated 2016-02-25) and FY2016
  (2017-02-22 16:47 ET, dated 2017-02-23). Each year comes from the latest filing that reports it: the FY2013 10-K restates 2012's total
  revenues and other income to $480,681M ($482,295M first reported), which the vintages carry from 2014-02-27, and each release shows its
  year-ago quarter as restated (the MSFT recast rule). The first year's diluted shares come from the last 10-K that reports them: 2003
  6,662M (FY2005 10-K), 2004 6,519M (FY2006), 2005 6,322M (FY2007), 2006 5,970M (FY2008) and 2007 5,594M (FY2009, restated). From the
  FY2014 10-K the company states one weighted share count, "the same" for basic and diluted.
- **Release timing.** Every earnings 8-K of the period was accepted before the open (08:00-09:29 ET) except the Q3 2013 and Q2 2014
  releases (09:48 and 09:36 ET, during the session). The Thursday prints date their weeks the Friday; the Friday prints (Q4 2012, Q3 2014,
  Q2-Q3 2015, Q1-Q3 2016, Q1-Q3 2017) meet their own day's close (the 2008 rule); the Monday Q4 2014 print and the Tuesday Q4 2015 and
  Q4 2016 prints date their weeks the next day (2015-02-03, 2016-02-03, 2017-02-01).
- **Special items leave the releases.** The Q4 2012 release is the last with a special-items table (none in 2012); from Q1 2013 the
  releases report none, so 2010 and every later year are GAAP, while 2003-2006, 2008 and 2009 keep the company's figures excluding special
  items. Three one-offs have no per-share figure excluding them and stay in (the ACN Russia rule): 2012's "$9.9 billion of divestment and
  restructuring gains, mainly Japan of $6.5 billion", whose effect the Q2 2013 release gives only as a percentage ("earnings per share
  were down 14%"); Q4 2014's "approximately $1 billion of non-cash effects" (U.S. deferred income tax items and a Venezuela arbitration
  ruling); and FY2016's $2 billion impairment, whose exclusion the Q4 2016 release gives in dollars only ("full year earnings were $9.9
  billion"), so FY2016 is GAAP $1.88 (the 1997 rule: nothing is derived). **No year is excluded:** the impairment is under 2016's $7,840M
  of earnings, so reported EPS is not under half the year's EPS without it (the AAPL FY2002 test), and no benefit approaches half a year's
  income (its AVGO mirror). FY2016's income taxes are a $406M benefit, so its effective rate is -5.1%, as published (the EPS check prints
  `(1−-5.1%)`, a display quirk).
- **Still no earnings, revenue or margin guide in numbers**, so the 2008 rules apply on every date: the last full year's EPS stands, BASE
  takes the latest quarter's revenue growth, and the margin signal the latest quarter's change. Each analyst meeting states the current
  year's production in numbers: "Total production will decline about 1% this year in 2013 versus last year." (8-K of 2013-03-12), "We
  anticipate total volumes to be flat in 2014 and grow about 2% to 3% per year from 2015 to 2017." (2014-03-11), "We anticipate total
  volumes to be 4.1 million oil-equivalent barrels per day in 2015 and grow an average of 3% per year in 2016 and 2017." (2015-03-10, at a
  $55 Brent), "we anticipate a range of 4.0 to 4.2 million oil-equivalent barrels per day of production through 2020" (2016-03-08) and
  "We anticipate a range of 4 to 4.4 million oil-equivalent barrels per day of production through the end of the decade." (2017-03-07),
  each 8-K accepted during the session. The last two are ranges that cover the current year (as 2011's two-year growth range did). Each is
  shown in the guide line and catalyst (3) for its year and feeds nothing (the UNP volume-guide rule). Two release sentences are shown as
  the release's words and feed nothing: Q3 2014's production "remains on track with previous full-year estimates of 4 million
  oil-equivalent barrels per day" and Q4 2015's 2016 capital and exploration expenditures of $23.2 billion (method r2 has no capex input).
  From the Q4 2015 release the company buys shares only to offset dilution; the capital-return line quotes its words.
- **Dividends,** each from the first filing that states the rate: $0.57 (FY2012 10-K), $0.63 from the Q2 2013 release, $0.69 from Q2
  2014, $0.73 from Q2 2015, $0.75 from Q2 2016 and $0.77 from Q2 2017, with each January declaration in its 10-K. No 10-Q states a raise
  before its Q2 release.
- **ENERGY_TRANSITION on the watch list from 2015-12-18.** The theme is live from 2015-12-12 and its scope (decarbonisation strands oil,
  gas and coal reserves and refining) covers ExxonMobil. Every 10-K of the period keeps the risk factor "Climate change and greenhouse gas
  restrictions" ("These requirements could make our products more expensive, lengthen project implementation times, and reduce demand for
  hydrocarbons, as well as shift hydrocarbon demand toward relatively lower-carbon sources such as natural gas."). The encoding (the MSFT
  CLOUD rule): from the first weekly date on or after the live date, XOM carries ENERGY_TRANSITION on the watch list, company-acknowledged,
  with no market read, in the latest 10-K's words: the FY2014 10-K's (published 2015-02-26, before the live date, as Microsoft's FY2012
  10-K preceded CLOUD's), then the FY2015 10-K's from 2016-02-25 and the FY2016 10-K's from 2017-02-23. The factor pair (the company's own
  research under "Government sponsorship of alternative energy", +0.2; the climate risk factor, -0.2) nets to zero and the theme signal
  stays at 2/4, so only text changes, and CYCLICAL stands. The theme's market-pricing date (2020-08-31) lies after 2017, and no filing of
  the period shows the market pricing decarbonisation of ExxonMobil's reserves: the shareholders' 2017 vote on a "Report on Impacts of
  Climate Change Policies" (8-K of 2017-06-06) and the board's decision to enhance its climate disclosures (8-K of 2017-12-11) are
  governance, not a market read, and add nothing. From the FY2012 vintage the durability "why" ends with a clause that follows the
  theme's status on the as-of date (`why_theme_tail`): "no disruption theme is live ..." to 2015-12-11, then that ENERGY_TRANSITION is
  on the watch list; the 2008-2012 vintages keep their text, so those dates rebuild byte-identical. The FY2015 and FY2016 10-Ks add "or
  electric vehicles" to the fuel-choice factors; EV is not live until 2020 and the "why" does not quote that clause.
- **Adds nothing:** the reserves releases (2013-02-19, 2014-02-21, 2015-02-24, 2016-02-19, 2017-02-23), the Financial and Operating
  Reviews (2013-03-26, 2014-03-24, 2015-03-23), the debt offerings (2014-03-20, 2015-03-06, 2016-03-03), the Q3 2016 release's warning
  that Kearl's oil sands may not qualify as proved reserves at year-end (no guided number), the Bass family Permian acquisition for $5.6
  billion of shares (8-K of 2017-01-17; Q1 2017's diluted shares, 4,223M, include them as published), the Tillerson agreement
  (2017-01-04), the mini-tender notice (2017-03-27), the officer, director, bylaw and annual-meeting 8-Ks, the 10-Qs beyond their
  dividends, and the new presentation of sales-based taxes (8-K of 2018-01-19, after the range).

Controls: altering one value of each new print (with each Q4 print's full-year actuals and the two release sentences), vintage, dividend,
production outlook and ENERGY_TRANSITION event changes no date before it is visible and changes the first weekly date on or after it
(45 of 45; an event is visible from the theme's live date). The 262 dates of 2008-2012 rebuild byte-identical. A scan of all 522 XOM
models for the figures, notes and quotes of every print, vintage, dividend, outlook and event finds none before it is visible (0 of
124,436). The firewall at 2013-07-01, 2015-01-01, 2016-01-01, 2017-07-01 and 2018-01-01 (planted facts, an ENERGY_TRANSITION event
from 2016, and prices ×10 after each cutoff) changes none of the 287 to 522 earlier models.

Seen in the build (method behaviour, not tuned):
- **2013: FAIR on 36 dates, RICH on 10, CHEAP on 5.** From the Q4 2012 print FY12's $9.70, with the Japan gains in it, is the anchor
  (8.9-10.5x, the 9th-55th percentile; FY11's $8.42 on the three dates before it); BASE is the latest quarter's revenue growth (-12.3% to +1.7%/yr), BEAR the 2009 fall (-52.5%/yr, $18-20), BULL the
  decade CAGR (16-20%), so the price sits between BASE and BULL and Ratio B is 0.9-1.8: ACCUMULATE on 22 dates, WATCHLIST on 28 and AVOID
  on one.
- **RICH and AVOID on all 205 dates from the Q4 2013 print (2014-01-31) to 2017-12-29.** FY13's $7.37 (the gains leave the anchor) at
  11.8-14.1x is the 65th-90th percentile with BASE at +0.1% to +9.1%/yr (Ratio B 3.9 to infinite) in 2014; the oil-price fall then takes
  revenue down 21-37% from the Q4 2014 print, so BASE is -17% to -33%/yr through 2015 while FY14's $7.60 anchors the multiple (9.5-12.3x).
  From the Q4 2015 print FY15's $3.85 is the anchor (20-25x, the 89th-100th percentile) and from the Q4 2016 print FY16's $1.88 (41-45x):
  the price lies above the BULL case on every date from 2016-02-03 (Ratio B infinite). BEAR stays the 2009 fall throughout (the decade's
  worst year: 2015's -49.3% and 2016's -51.2% come close), at $15-20 to 2015 and $4-8 after.
- **The window absorbs the trough multiples.** As the 2015-2017 days at 20-45x join the P/E window, its 75th and 90th percentiles rise from
  12x and 14-16x to 21x and 44x and the median from 10.7x to 12.4x; the median of the calendar-year lows (the EPP floor) moves from 9x to 11x
  with the Q4 2016 print. BULL's decade CAGR falls from +19.5%/yr to -5.7%/yr and is held at BASE's rate whenever it is lower.
- **Totals over the 260 dates:** CHEAP 5, FAIR 40, RICH 215; ACCUMULATE 22, WATCHLIST 32, AVOID 206; robustness 8 of 8 on 151 dates and
  3-5 of 8 on 53 (mostly 2013, where the price sits near the BASE case).
- **The proxy composite** ranges from 1.55 to 2.80 and the market composite from 2.15 to 3.52.

How far each call moves the classes (the 260 dates rebuilt with one encoding changed; no outcome consulted):
- GAAP EPS in every year instead of the company's figures excluding special items would change 14 classes (11 in 2013, 3 in January 2014:
  FAIR or CHEAP to RICH) and 22 tiers;
- BASE on the latest quarter's oil-equivalent production growth instead of revenue growth would change 11 classes (6 in 2013, 5 in 2015:
  RICH to FAIR) and 5 tiers; unlike 2010-2011, the revenue fallback seldom decides the class, because from 2014 the price sits near or
  above the BULL case whatever BASE is;
- both together: 20 classes and 27 tiers;
- as tests only (each figure derived, which the method forbids as an input): 2012 without its $9.9 billion of gains ($7.56: $44,880M less $9,900M over 4,628M shares) and FY2016
  without its impairment ($2.37: the release's $9.9 billion over 4,177M shares) would change 45 classes (41 in 2013 and 4 in January 2014: every FAIR and CHEAP date becomes RICH) and 0
  classes respectively;
- without the ENERGY_TRANSITION events: 0 classes and 0 tiers (text only, as designed).

Judgement calls that could carry hindsight (in addition to the 2008 and 2009-2012 lists, which stand):
- the one-offs left in because no per-share figure excluding them was published: 2012's gains (they lift the 2013 anchor by about a
  fifth, and every FAIR or CHEAP date of 2013 rests on them), Q4 2014's non-cash effects and FY2016's impairment;
- ENERGY_TRANSITION kept on the watch list (company-acknowledged, no market read) from its live date rather than read as priced: the
  builder knows the theme's later course, and re-filing would need dated evidence of the market pricing it for ExxonMobil (text only
  either way: the class label, not the price state, would change);
- the 2016 and 2017 multi-year production ranges read as the current year's outlook, and the two release sentences shown in words
  (display only either way).

### XOM 2018-2020: revenue net of sales taxes, one-offs at GAAP, COVID, the Dow removal re-files the energy transition

Every 8-K, 10-Q and 10-K of January 2018 to January 2021 was listed (52 filings to 2021-01-31: 40 8-Ks, nine 10-Qs and three 10-Ks,
plus the Q4 2020 release of 2021-02-02, after the range and not used). The earnings releases with their Investor Relations Data
Summaries and the three 10-Ks were read for the facts; every other 8-K and the 10-Qs were checked for a guided number or a dividend. The
prints were extracted by script and checked twice: 290 strings with `verbatim.py` against their own filings (every quoted sentence taken
by an exact search), and every volume against the release's Investor Relations Data Summary. One source is not an SEC filing: the S&P
Dow Jones Indices announcement of 2020-08-24 (below). Decided on 2026-11-05, before any 2018-2020 date was built or scored:

- **Three 10-K vintages, each with a Q4 print before it:** FY2017 (accepted 2018-02-28 16:39 ET, dated 2018-03-01), FY2018 (2019-02-27
  16:19 ET, dated 2019-02-28) and FY2019 (2020-02-26 16:15 ET, dated 2020-02-27). The first year's diluted shares come from the last 10-K
  that reports them: 2008 5,221M (FY2010 10-K), 2009 4,848M (FY2011), 2010 4,897M (FY2012). The Q4 2020 print (2021-02-02) lies after the
  range, so FY2020's loss enters no model here.
- **Release timing.** All twelve earnings 8-Ks (Q4 2017 to Q3 2020) were accepted before the open (07:28-08:39 ET) on a Friday, so each
  print meets its own day's close and dates its week (the 2008 rule).
- **Revenue net of sales-based taxes from Q4 2017.** The 8-K of 2018-01-19 announced, and the Q4 2017 release applied, net reporting of
  sales-based taxes; each release from Q4 2017 compares with the year-ago quarter as restated (the MSFT recast rule), and the FY2017 10-K
  restates 2015 and 2016 total revenues and other income ($249,248M and $208,114M against $268,882M and $226,094M first reported). Each
  year comes from the latest filing that reports it, so 2015 on is net and 2014 and earlier stay gross: a seam kept as published (the
  2006 netting rule). It makes 2015's step -39.5% instead of -34.7% and moves no median of revenue growth (-6.0%, -1.2% and -6.0% for the
  three vintages either way); the bridge's display CAGR carries it.
- **EPS at GAAP for 2017, 2018 and 2019.** The releases exclude U.S. tax reform and impairments (2017-2018) and then "identified items"
  (from Q2 2019), but give the full-year figures without them in dollars only: 2017 $15,289M (GAAP $4.63, with a $5,942M tax-reform gain
  and $1,521M of impairments), 2018 $21,038M (GAAP $4.88), 2019 $9,605M (GAAP $3.36, with $4,735M of identified items, mainly the $3.7
  billion Norway gain); no 10-K publishes a per-share figure. So each year stays GAAP (the 1997 rule: nothing is derived), and quarters
  carry the per-share figures their releases give in the note (Q4 2017's $0.88 excluding tax reform and impairments; from Q2 2019 the
  identified items per share). **No year is excluded:** 2017's benefits ($5,942M) and 2019's ($4,735M) are under each year's income
  without them (the AVOID FY2018 mirror test). FY2017's income taxes are a $1,174M benefit (effective rate -6.3%, as published).
- **Still no guide in numbers, and no production outlook in any filing.** The investor days of 2018-2020 were not filed; the one
  presentation filed (Scotia Howard Weil, 8-K of 2019-03-25) says "Volumes consistent with fourth quarter" in words. So the 2008 rules
  apply on every date and the guide line reads "no guide in numbers in any filing" from 2018-02-02. From 2019 ExxonMobil files
  "earnings considerations" 8-Ks after each quarter ends (2019-04-10 to 2020-12-30, eight filings): ranges for the effect of prices,
  margins and identified items on the quarter just ended, before its release. They guide no earnings, revenue or volume figure, so they
  add nothing (the ACN non-earnings 8-K rule), and nor do the capex cut to about $23 billion (8-K of 2020-04-07) or the material
  impairment notice (Item 2.06, 8-K of 2020-11-30: an after-tax charge of $17-20 billion in Q4 2020, which reaches FY2020's EPS only with
  the Q4 2020 print, after the range).
- **Dividends,** each from the first filing that states the rate: $0.77 (FY2017 10-K), $0.82 from the Q2 2018 release, $0.87 from the Q2
  2019 release, with each January declaration in its 10-K ($0.87 on January 29, 2020); no raise in 2020. Share purchases only offset
  dilution throughout; the Bass acquisition shares lift diluted shares to 4,270M from Q4 2017.
- **ENERGY_TRANSITION: the watch list, then a re-file from 2020-09-04.** The FY2017-FY2019 10-Ks keep the climate risk factor ("Such
  policies could make our products more expensive, less competitive, lengthen project implementation times, and reduce demand for
  hydrocarbons, ..." from FY2018), so the watch list continues in each 10-K's words (the FY2019 10-K heads its research paragraph
  "Alternative energy"). The theme registry dates ENERGY_TRANSITION's market pricing to 2020-08-31, "ExxonMobil removed from the Dow
  Jones Industrial Average": dated evidence that names the company, which the earlier XOM text required for a re-file. The second
  encoding (decided before any 2018-2020 date was built): market evidence that names the company (`transition_market_evidence`, an event
  without a `doc`, so it stays in scope once public) counts from the theme's registered market-pricing date and re-files the stock under
  DISRUPTION_EXPOSED (ENERGY_TRANSITION) with risk 3 (the ACN GENAI rule). The source is S&P Dow Jones Indices' announcement of
  2020-08-24 (PR Newswire, issued after the close, dated 2020-08-25): "Salesforce.com (NYSE:CRM) will replace Exxon Mobil Corp.
  (NYSE:XOM)", effective before the open on 2020-08-31. The announcement itself gives a different reason, "prompted by DJIA constituent
  Apple Inc.'s (NASD:AAPL) decision to split its stock 4:1", and the re-filed "why" quotes it. The kind changes the class label only
  (RICH reads TRANSITION-EXPOSED, NOT CHEAP; CHEAP reads TRANSITION-FEAR BASKET): the theme signal and the factor pair are unchanged, so
  no number moves.
- **Adds nothing:** the reserves releases (2018-02-09, 2019-02-26), the earnings-considerations 8-Ks, the capex and impairment 8-Ks above,
  the debt offerings (2019-08-16, 2020-03-19, 2020-04-15, 2020-06-26), the mini-tender notice (2020-07-28), the EDGAR-outage notice
  (2020-07-30), the officer, director, bylaw and annual-meeting 8-Ks, and the 10-Qs beyond their dividends.

Controls: altering one value of each new print (with each Q4 print's full-year actuals), vintage, dividend and ENERGY_TRANSITION event
changes no date before it is visible and changes the first weekly date on or after it (24 of 24; the Dow evidence is visible from the
theme's market-pricing date, so the first date it changes is 2020-09-04). The 522 dates of 2008-2017 rebuild byte-identical. A scan of
all 679 XOM models for the figures, notes and quotes of every print, vintage, dividend, outlook and event finds none before it is visible
(0 of 210,567). The firewall at 2018-07-01, 2019-07-01, 2020-10-01 and 2021-01-01 (planted facts, a later Dow event, and prices
×10 after each cutoff) changes none of the 548 to 679 earlier models.

Seen in the build (method behaviour, not tuned):
- **January 2018:** RICH and AVOID on 4 dates (FY16's $1.88, 46-47x).
- **From the Q4 2017 print to January 2019: FAIR on 28 dates, CHEAP on 12, RICH on 12.** FY17's $4.63, with the tax-reform gain in it, at
  14.7-18.4x (the 50th-77th percentile); revenue +16% to +27% puts BASE at +18.6% to +28.9%/yr, and BULL (the decade CAGR) is held at
  BASE's rate. BEAR is still the 2009 fall (-52.5%/yr, $9-10). CHEAP from late October 2018 to January 2019 as the price fell to $68-82.
- **RICH and AVOID on all 52 dates from the Q4 2018 print (2019-02-01) to 2020-01-24.** FY18's $4.88 at 13.6-16.9x (the 49th-62nd
  percentile) with revenue turning down (BASE +9.5-10.1%/yr, then -4.6% to -13.7%/yr from the Q1 2019 print); Ratio B 2.0-6.6. From the
  FY2018 vintage (2019-02-28) the 2009 fall leaves the history and BEAR becomes 2016's fall (-51.2%/yr).
- **2020: RICH on 45 dates (4 of them before the Q4 2019 print), CHEAP on 6, FAIR on 2.** From the Q4 2019 print FY19's $3.36, with the Norway gain in it, anchors the
  multiple; the COVID fall takes the price to $32.62-62.12 (9.7-18.5x, the 16th-69th percentile): CHEAP on 2 dates of March 2020. The Q1
  2020 print's revenue -11.7% and the Q2 2020 print's -52.8% put BASE at -10.2% and -51.3%/yr ($42 and $12; the latter just below BEAR's
  -51.2%, as in 2009), so RICH on all 26 dates to 2020-10-23; the Q3 2020 print (revenue -29.0%, BASE -27.5%/yr) gives CHEAP on 4 and
  RICH on 6. The 18 dates from 2020-09-04 carry the re-filed labels (14 TRANSITION-EXPOSED, NOT CHEAP; 4 TRANSITION-FEAR BASKET).
- **Totals over the 157 dates:** CHEAP 18, FAIR 30, RICH 109; ACCUMULATE 16, WATCHLIST 44, AVOID 97. Robustness is weak: 8 of 8 on 19
  dates, 2-5 of 8 on 109. The proxy composite ranges from 1.15 (Q2 2020) to 2.80, the market composite from 1.82 to 3.41; the EPP floor
  moves from 11x to 13-14x from late 2018 through 2019 and back to 11-12x in 2020.

How far each call moves the classes (the 157 dates rebuilt with one encoding changed; no outcome consulted):
- GAAP EPS in every year (2008 and 2009 at GAAP) would change no class and one tier;
- BASE on the latest quarter's oil-equivalent production growth instead of revenue growth would change 81 classes (36 in 2018, 16 in
  2019, 29 in 2020; 40 FAIR or CHEAP to RICH, 41 the other way) and 71 tiers: as in 2010-2011, the revenue fallback decides the class;
- both together: the same 81 classes;
- as tests only (each figure derived, which the method forbids as an input): 2017, 2018 and 2019 without their excluded items ($3.59,
  $4.93 and $2.25: the dollar figures over the year's diluted shares) would change 71 classes (41 RICH to FAIR or CHEAP, 30 the other way),
  2019 alone 8 (in 2020, CHEAP or FAIR to RICH);
- without the re-file: no class, 18 labels.

Judgement calls that could carry hindsight (in addition to the earlier XOM lists, which stand):
- the re-file on the theme registry's reading of the Dow removal, when the announcement gives Apple's split as its reason (label only:
  no class, price state or tier moves);
- the one-offs left in at GAAP because only dollar figures excluding them were published (71 classes move without them);
- BASE on revenue growth, which again decides the class (81 classes move on production growth);
- the earnings-considerations and impairment 8-Ks read as adding nothing, and the revenue seam kept as published.

### XOM 2021-2023: FY2020's loss leaves the history, 2019 restated, the 2022 price spike, ENERGY_TRANSITION stays re-filed

Every 8-K, 10-Q and 10-K of February 2021 to December 2023 was listed (64 filings: 52 8-Ks, two of them amendments, nine 10-Qs and three
10-Ks; January 2021's were listed with 2018-2020, and the Q4 2023 release of 2024-02-02 lies after the range and is not used). The
earnings releases with their Investor Relations Data Summaries and the three 10-Ks were read for the facts; every other 8-K and the 10-Qs
were checked for a guided number or a dividend. The prints were extracted by script and checked twice: 316 strings with `verbatim.py`
against their own filings (every quoted sentence taken by an exact search), and each quarter's oil-equivalent production against the
release's Investor Relations Data Summary. Decided on 2026-11-05, before any 2021-2023 date was built or scored:

- **Three 10-K vintages, each with a Q4 print before it:** FY2020 (accepted 2021-02-24 17:01 ET, dated 2021-02-25), FY2021 (2022-02-23
  16:11 ET, dated 2022-02-24) and FY2022 (2023-02-22 16:37 ET, dated 2023-02-23). The FY2023 10-K and the Q4 2023 print lie after the range.
- **Release timing.** All twelve earnings 8-Ks (Q4 2020 to Q3 2023) were accepted before the open (06:02-07:30 ET). The nine Friday
  releases meet their own day's close and date their weeks (the 2008 rule); the three Q4 releases came on a Tuesday (2021-02-02,
  2022-02-01, 2023-01-31), so the Wednesday after dates their weeks (2021-02-03, 2022-02-02, 2023-02-01), as the weekly rule sets.
- **FY2020 is excluded: a loss even on the company's own figure.** The Q4 2020 release reports a GAAP loss of $(5.25) a share (the fourth
  quarter's identified items, mainly non-cash impairments, were $4.73 a share) and $(0.33) excluding identified items; a loss has no P/E, so neither figure can
  anchor the multiple. The method gains a note (see "Retro method r2"; no earlier output changes, so still r2): a year that is a loss
  even on the company-published figure without its one-offs is excluded like a loss with none. As the latest year it is encoded as NKE's
  FY2018 was: it leaves the EPS history (the Q4 2020 print's `fy_actual` carries no EPS and an `excluded_note`; the FY2020-FY2022
  vintages carry `eps_excluded`), its revenue, shares and margins stay, its own days leave the P/E window ("10-yr ex-FY20"), EPS growth is
  measured only between years in the history, and the rollover rule's last full year is the last year in it, so FY2019 stands for FY2021E
  until the Q4 2021 print. A scan of every fact sheet finds no earlier year of any ticker whose company-published figure was a loss.
- **FY2019 restated to $2.25 a share.** The Q4 2020 release is the first filing to publish 2019's earnings per share excluding
  identified items ($2.25; GAAP $3.36, which includes the $3.7 billion Norway gain). It replaces GAAP from the print (the ACN rule; the
  `restates` encoding of the Q4 2009 release), on 2021-02-03, and the FY2020 10-K carries it from 2021-02-25. Every 2020 date keeps
  $3.36: the per-share figure was not public before 2021-02-02 (the 2018-2020 section's derived $2.25 was a test only, never an input).
- **FY2021 and FY2022 at the company's figures excluding identified items,** each published per share in its Q4 release: $5.38 (GAAP
  $5.39) and $14.06 (GAAP $13.26, with the $3.4 billion charge for the exit from Russia's Sakhalin-1 in the first quarter of 2022). The
  quarters carry the per-share figures their releases give in the note.
- **The releases' layout changes twice; the facts follow the release in force.** Q1 2022's key-figure tables run current quarter,
  prior quarter, year-ago quarter; from Q2 2022 the label sits between the three quarters and the two year-to-date columns. The
  extraction matches each value to its column header (`1Q22`, `1Q21`), never to its position. From Q2 2022, after the reorganisation
  into Upstream, Energy Products, Chemical Products and Specialty Products (announced 2022-01-31), the releases report "Energy Products
  sales" and "Chemical Products sales", each with its year-ago figure on the new basis. They feed the product-sales and chemical-sales
  signals as the successors of petroleum product sales and chemical prime product sales, with the rule-T thresholds unchanged, and the
  text names the line the release in force names (`pps_label`, `chem_label`); dates before Q2 2022 keep the old names.
- **Still no guide in numbers in any filing.** The 8-Ks of 2021-11-17, 2022-11-18 and 2023-11-15 announce Corporate Plan updates
  "on the Investors section of our website", with "Website materials are not part of this filing": the capex ranges, earnings and cash
  flow potential and share-repurchase plans they carry were never filed, so they add nothing (website posts are not filings, as for NKE's
  investor-relations posts). The eleven
  earnings-considerations 8-Ks (2021-03-31 to 2023-10-04) guide no earnings, revenue or volume figure and add nothing (the ACN
  non-earnings 8-K rule). The 2008 rules apply on every date and the guide line reads "no guide in numbers in any filing".
- **Dividends,** each from the first filing that states the rate: $0.87 through 2021 (no raise filed until the Q4 2021 release states
  $0.88, 2022-02-01), $0.91 from the Q3 2022 release (2022-10-28) and $0.95 from the Q3 2023 release (2023-10-27). Diluted shares fall
  from 4,275M (FY2021) to 4,205M (FY2022) as published; the repurchase plans themselves were website-only.
- **ENERGY_TRANSITION stays re-filed** under DISRUPTION_EXPOSED (ENERGY_TRANSITION), risk 3, on every date, the "why" quoting the
  FY2020-FY2022 10-Ks' climate risk factor ("Depending on how policies are formulated and applied, ... reduce demand for hydrocarbons
  ..."; headed "Climate change and greenhouse gas restrictions" in the FY2020 10-K and "Greenhouse gas restrictions" from FY2021) and the
  company's own low-carbon work (advanced biofuels and hydrogen, carbon capture and storage; from FY2021 the Low Carbon Solutions (LCS)
  business unit). Label only, as before: the theme signal and the factor pair are unchanged.
- **EV is not recorded on any date** (2020 included). The theme is live from about 2020, scoped to "battery-electric vehicles displace
  ICE powertrains, auto parts suppliers and fuel retail", and every XOM 10-K from FY2015 names electric vehicles or "electric
  transportation" among the fuel-choice factors (the FY2021 and FY2022 10-Ks add "mandates for sales of electric vehicles" to the climate
  risk factor). ExxonMobil's exposure
  through fuel demand is the decarbonisation ENERGY_TRANSITION already covers, the stock is filed under that theme from 2020-09-04, before
  EV's market-pricing date (2020-12-21), and EV's evidence names Tesla and legacy automakers, not ExxonMobil; a second company-acknowledged
  theme would be text only on the watch list and inert after the re-file (the ACN rule that left OFFSHORE out once GENAI had priority).
- **Adds nothing:** the reorganisation release (2022-01-31) and its earnings recast (2022-06-17), the Sakhalin-1 exit release
  (2022-03-03; its charge reaches the Q1 2022 print as an identified item), the Denbury (8-K of 2023-07-13, all stock, closed 2023-11-02)
  and Pioneer (8-K of 2023-10-11, all stock, closed after the range) agreements and filings, whose shares reach no print in the range, the
  debt satisfactions (2021-12-17, 2022-12-23), the Corporate Plan notices above, the vote results of 2021-06-02 (three directors
  nominated by Engine No. 1 elected) and later years, the officer, director, compensation and bylaw 8-Ks, and the 10-Qs beyond their
  dividends.

Controls: altering one value of each new print (with each Q4 print's full-year actuals, Q4 2020's excluded-year note and its 2019
restatement), vintage, dividend and ENERGY_TRANSITION event changes no date before it is visible and changes the first weekly date on or
after it (25 of 25; the event controls alter the risk factor's short form, the text the re-filed "why" shows). The 679 dates of
2008-2020 rebuild byte-identical. A scan of all 835 XOM models for the figures, notes and quotes of every print, vintage, dividend,
outlook and event finds none before it is visible (0 of 320,843); the restated $2.25 for 2019 first appears on 2021-02-03 and "ex-FY20"
in no model before it. The firewall at 2021-07-01, 2022-07-01, 2023-07-01 and 2024-01-01 (planted facts, now with a later Q4 print
that excludes its own year and restates every earlier one, a later vintage that excludes a year and renamed volume lines, and prices ×10
after each cutoff) changes none of the 704 to 835 earlier models; rerun with the new plants, the 2018-07-01 and 2021-01-01 cutoffs
change none of the 548 and 679.

Seen in the build (method behaviour, not tuned):
- **January 2021:** RICH and AVOID on 4 dates (FY19's $3.36, the Q3 2020 print's BASE -27.5%/yr).
- **From the Q4 2020 print to the Q1 2021 print: RICH and AVOID on 12 dates.** With FY2020 out, FY19's restated $2.25 anchors the
  multiple: $47-62 is 21.1-27.5x (the 70th-78th percentile of the ex-FY20 window). The quarter's revenue -30.7% puts BASE at -29.3%/yr
  ($19), and BEAR becomes 2019's restated fall (-53.9%/yr, $4): no upside to any scenario price, so Ratio B is infinite.
- **Q1 2021 print: RICH and AVOID on 13 dates** (revenue +5.3%, BASE +6.8%/yr, $43-45; the price $57-65, 25-29x; Ratio B 14.2 to 5.3).
- **Q2 and Q3 2021 prints (2021-07-30 to 2022-01-28): CHEAP on 23 dates, FAIR on 4; BUY on 24, ACCUMULATE on 3.** Revenue +107.8% on
  the 2020 trough quarter and then +59.7% put BASE at +109.3% and +61.2%/yr ($171-173, then $103-104) on the same $2.25, against $53-75
  at 23-34x (the 71st-85th percentile): the revenue fallback, not the multiple, makes the class. FAIR from 2021-10-22 to 2021-11-12,
  ACCUMULATE on the three dates from 2022-01-14 as the price reached $72-75.
- **From the Q4 2021 print (2022-02-02) to 2023-01-27: CHEAP and BUY on all 52 dates.** FY21's $5.38 anchors at 14.4-21.5x (the
  43rd-72nd percentile) as the price rises from $77 to $116; revenue +82.6%, +53.0%, +70.8% and +51.9% put BASE at +52.8% to +83.9%/yr
  ($210-300). BEAR stays 2019's restated fall ($11-13).
- **From the Q4 2022 print (2023-02-01): CHEAP and BUY on all 48 dates.** FY22's $14.06 anchors at 7.1-8.5x (the 8th-19th percentile).
  Revenue turns down (+12.3%, then -4.3%, -28.3% and -19.0%): BASE falls from +13.3% to -27.7%/yr ($294-298, then $121-215), still above
  the price ($100-119); BEAR $22-23.
- **Totals over the 156 dates:** CHEAP 123, FAIR 4, RICH 29; BUY 124, ACCUMULATE 3, AVOID 29. Robustness is strong: 8 of 8 on 125 dates,
  4-6 of 8 on 14 (all in 2021). Labels: TRANSITION-FEAR BASKET 123, TRANSITION-EXPOSED, NOT CHEAP 29, TRANSITION-EXPOSED, NEUTRALLY VALUED
  4. The proxy composite ranges from 1.45 (2021-02-03) to 3.55, the market composite from 1.02 to 2.99; the EPP floor is 12x in
  January 2021, 14-17x from February 2021 to January 2022 (2016's year at 38.9x and 2019's restated one at 29.6x among the calendar-year
  lows), 12-14x from the Q4 2021 print and 12-13x in 2023.

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted):
- GAAP EPS in every year (2019 at $3.36, FY2021 $5.39, FY2022 $13.26; FY2020 a loss either way) would change 4 classes (FAIR to CHEAP,
  2021-10-22 to 2021-11-12) and 3 tiers;
- FY2019 at GAAP alone (no restatement): the same 4 classes;
- BASE on the latest quarter's oil-equivalent production growth instead of revenue growth would change 77 classes (23 in 2021, 50 in
  2022, 4 in 2023; 63 to RICH, 14 CHEAP to FAIR) and 79 tiers: the revenue fallback decides the class, as in every earlier XOM batch;
- both together: 79 classes;
- without the re-file: no class, 156 labels.

Judgement calls that could carry hindsight (in addition to the earlier XOM lists, which stand):
- FY2020 excluded on the new note (a loss even on the company's figure), which leaves FY19's restated $2.25 as the anchor through 2021;
- BASE on revenue growth, which again decides the class (77 classes move on production growth), and in 2021-2022 runs at +54% to +109%/yr
  on revenue that rebounded from the 2020 trough;
- the renamed Energy Products and Chemical Products sales read as the successors of the old volume lines under unchanged thresholds;
- EV left out, the re-file continued on the 2020 evidence, and the Corporate Plan updates read as adding nothing because they were
  posted to the website and not filed.

### XOM 2024-2026: Pioneer in the volumes, year-ago volumes from the year-ago release, timing effects left in, a successor issuer in Texas

Every 8-K, 10-Q and 10-K of January 2024 to November 2026 was listed for both registrants: Exxon Mobil Corporation (52 filings: 39 8-Ks,
two 8-K/As, eight 10-Qs and three 10-Ks) and, from the redomiciliation of 2026-07-01, ExxonMobil Holdings Corporation (EDGAR CIK 2115436:
the 8-K12B, six 8-Ks and the Q3 2026 10-Q; the Q2 2026 10-Q was filed under both). The twelve earnings releases with their exhibits 99.2
and the three 10-Ks were read for the facts; every other 8-K and the 10-Qs were checked for a guided number, a dividend or a share count.
The prints were extracted by script (each key-figure value matched to its column header, never to its position) and checked twice: 351
strings with `verbatim.py` against their own filings, and every year-ago volume that two filings state (a Q1 release's year-ago column, the
Q2 and Q3 2024 Investor Relations Data Summaries' five quarters) against the year-ago quarter's own release (18 of 18 identical). Decided on
2026-11-05, before any 2024-2026 date was built or scored:

- **Three 10-K vintages, each with a Q4 print before it:** FY2023 (accepted 2024-02-28 16:37 ET, dated 2024-02-29), FY2024 (2025-02-19
  16:39 ET, dated 2025-02-20) and FY2025 (2026-02-18 16:06 ET, dated 2026-02-19). The first year's diluted shares come from the last 10-K
  that reports them: 2014 4,282M (FY2016 10-K), 2015 4,196M (FY2017 10-K), 2016 4,177M (FY2018 10-K). From the FY2024 10-K the segment
  revenue table has no corporate column; the display groups are unchanged.
- **Release timing.** All twelve earnings 8-Ks (Q4 2023 to Q3 2026) were accepted before the open (06:31-06:32 ET) on a Friday, so each
  print meets its own day's close and dates its week (the 2008 rule). Holiday weeks end on Thursdays: 2024-03-28, 2025-04-17, 2025-07-03,
  2026-04-02, 2026-06-18 and 2026-07-02. The last date is 2026-10-30, the day of the Q3 2026 print and the last complete week: the series
  was built on 2026-11-05, so a rebuild after the close of 2026-11-06 adds the week of 2026-11-02. The newest dates have no two-year
  outcome yet.
- **EPS: the company's figures excluding identified items, published per share in each Q4 release** (the ACN rule): FY2023 $9.52 (GAAP
  $8.89, with a $2.0 billion impairment in California), FY2024 $7.79 (GAAP $7.84) and FY2025 $6.99 (GAAP $6.70). From Q1 2026 the releases
  add a figure that also excludes "estimated timing effects" (unsettled derivatives marked to market and LIFO recognition differences,
  "Impacts are expected to unwind in subsequent periods"), and from Q2 2026 they headline it as "Adjusted Earnings/(Loss) Per Common
  Share". Timing effects arise in every quarter (the Q2 2026 release's restated 2025 quarters show them in all four: $0.03, $0.03, $0.04 and
  $0.08 a share), so that figure does not exclude only one-offs (the NKE FY2007 rule, as MSFT's OpenAI impact), and no full year on that
  basis is published inside the range. The quarters carry each figure in their note, display only.
- **Year-ago volumes from the year-ago quarter's own release.** From Q4 2024 the key figures print the current and prior quarters and the
  year to date (the Q1 releases keep a year-ago column; the Q2 and Q3 2024 releases' Investor Relations Data Summaries still give five
  quarters). Where a release prints no year-ago quarter for production, Energy Products sales or Chemical Products sales, the current
  quarter is read against the year-ago quarter's own release, public a year earlier (the AAPL guide and AVGO inventory rule; the print's
  `extra_sources`): Q4 2024 against Q4 2023, Q2-Q4 2025 against Q2-Q4 2024, Q2 and Q3 2026 against Q2 and Q3 2025. Nothing is derived from
  the year-to-date columns. Revenue, pre-tax income and EPS keep the year-ago columns of the release's own income statement.
- **Pioneer in the volumes, as published.** The Pioneer Natural Resources merger (agreed October 2023, closed 2024-05-03 with 545 million
  shares issued) adds no guided number. Acquisitions stay in (the PEP rule, as XTO in 2010): production grows 20.8% in Q2 2024, 24.2% in
  Q3, 20.3% in Q4 2024 and Q1 2025, and diluted shares rise from 3,998M (Q1 2024) to 4,462M (Q3 2024) before the buyback brings them to
  4,140M (Q3 2026). The Q1-Q3 2024 prints say so in a deal note. Denbury (closed 2023-11-02) reaches no print as a share count of its own.
- **Still no guide in numbers in any filing.** The Corporate Plan updates were again announced by 8-K (2024-11-12, 2025-11-18) and posted
  only on the website. The releases' capital-expenditure ranges ("approximately $28 billion" for 2024, "$27 billion to $29 billion" for
  2025, "$27-$29 billion" for 2026) and their project earnings at constant prices and margins ("more than $3 billion of earnings in 2026") give no EPS,
  revenue or volume figure, so they add nothing (as the capex 8-K of 2020-04-07). The twelve earnings-considerations 8-Ks add nothing (the
  ACN non-earnings 8-K rule); the last is renamed "Market and Planned Impacts to Earnings" (2026-10-16). The supplement of 2026-04-08
  ("Impact of Middle East conflict on ExxonMobil activities", before the open) expects the conflict "to lower global oil-equivalent
  production by approximately 6% in first quarter compared with fourth-quarter 2025" and first-quarter EPS "higher than the fourth quarter
  of 2025, excluding unfavorable timing effects": estimates for a quarter already ended, 23 days before its print, with no figure for a
  later period, so it adds nothing either (method r2 has no volume input).
- **Dividends,** each from the first filing that states the rate: $0.99 from the Q3 2024 release (2024-11-01), $1.03 from the Q3 2025
  release (2025-10-31) and $1.07 from the Q3 2026 release (2026-10-30), with each 10-K's declaration ($0.95 on February 1, 2024; $0.99 on
  January 31, 2025; $1.03 on January 29, 2026).
- **A successor issuer.** On 2026-07-01 Exxon Mobil Corporation (New Jersey) completed its redomiciliation merger: each share was
  exchanged for one share of ExxonMobil Holdings Corporation (Texas), "the successor registrant" (8-K12B accepted 12:36 ET), trading as XOM
  on the NYSE from July 2. The Q2 and Q3 2026 releases are the new registrant's. The listed company's name follows from the first weekly
  date on or after the filing, 2026-07-02, until a vintage carries it (`company_names`, the AVGO rule); the exchange is one for one, so the
  price series runs on unchanged.
- **ENERGY_TRANSITION stays re-filed** under DISRUPTION_EXPOSED (ENERGY_TRANSITION), risk 3, on every date, the "why" quoting the
  FY2023-FY2025 10-Ks' "Greenhouse gas restrictions" risk factor ("Depending on how policies are formulated and applied, such policies
  could negatively affect our investment returns, ... and reduce demand for hydrocarbons, ...") and the Low Carbon Solutions business unit.
  Label only. EV stays unrecorded ("XOM 2021-2023").
- **Adds nothing:** the Pioneer completion 8-K (2024-05-03) beyond the shares in the prints, the Pioneer convertible-notes redemption
  (2024-05-10), the floating-rate notes (2024-10-08, 2025-04-01, 2025-11-13, 2026-03-31, 2026-09-25), the XTO notes redemption
  (2026-08-28), the Corporate Plan notices, the officer and director 8-Ks and 8-K/As, the annual-meeting votes (2024-05-31, 2025-05-30,
  2026-05-29), the redomiciliation 8-Ks beyond the name, and the 10-Qs beyond their dividends.

Controls: altering one value of each new print (with each Q4 print's full-year actuals and the Q1-Q3 2024 deal notes), vintage, dividend,
ENERGY_TRANSITION event and company name changes no date before it is visible and changes the first weekly date on or after it (28 of
28). The 835 dates of 2008-2023 rebuild byte-identical. A scan of all 983 XOM models for the figures, notes and quotes of every print,
vintage, dividend, outlook, event and company name, and now every source's title and supports text, finds none before it is visible (0 of
599,484; a string already inside an earlier item's text, such as the line name "Energy Products sales", is not distinctive). The firewall at 2024-07-01, 2025-01-01, 2025-07-01, 2026-01-01, 2026-07-01 and 2026-11-01 (planted facts, a
planted later company name, and prices ×10 after each cutoff) changes none of the 861 to 983 earlier models.

Seen in the build (method behaviour, not tuned):
- **January 2024: CHEAP and BUY on 4 dates** (FY22's $14.06 at 6.9-7.3x, the 8th-11th percentile; BASE -18.4%/yr).
- **From the Q4 2023 print to January 2025: CHEAP on 48 dates, FAIR on 4.** FY23's $9.52 anchors at 10.7-13.1x (the 17th-44th
  percentile) as the price moves between $102 and $125; revenue -11.6%, -4.0%, +12.2% and -0.8% put BASE at -11.0% to +12.8%/yr
  ($124-200). FAIR from 2024-03-28 to 2024-04-19 ($116-121); ACCUMULATE on 35 dates, BUY on 17.
- **From the Q4 2024 print to the Q3 2025 print: CHEAP on 18 dates, FAIR on 21.** FY24's $7.79 anchors at 13.1-15.1x (the 34th-49th
  percentile); revenue -1.1%, +0.1% and -12.4% put BASE at -0.2% to -12.7%/yr ($90-124). WATCHLIST on 27, ACCUMULATE on 10, AVOID on 2.
- **RICH and AVOID on 38 dates from 2025-11-07 to 2026-07-24.** FY24's $7.79 and then, from the Q4 2025 print, FY25's $6.99 anchor at
  14.7-24.5x as the price rises from $116 to $171 (the 78th-83rd percentile in 2026); revenue -5.2%, -1.3% and +2.4% put BASE at -5.5% to
  +2.1%/yr ($104-114); Ratio B 2.0-4.4 in late 2025, infinite on the first dates of 2026, then 7.2-13.1.
- **The Q2 2026 print: FAIR on 11 dates, RICH on 2.** Revenue +42.3% puts BASE at +42.0%/yr ($220) against $153-183 at 21.9-26.2x (the
  82nd-87th percentile); RICH from 2026-10-16. The Q3 2026 print (revenue +32.7%, BASE +32.4%/yr, $191) gives RICH on 2026-10-30 at
  $187.25.
- **Totals over the 148 dates:** CHEAP 70, FAIR 37, RICH 41; BUY 21, ACCUMULATE 45, WATCHLIST 35, AVOID 47. Labels: TRANSITION-FEAR BASKET
  70, TRANSITION-EXPOSED, NOT CHEAP 41, TRANSITION-EXPOSED, NEUTRALLY VALUED 37. Robustness is weak: 8 of 8 on 27 dates, 7 on 65, 2-6 on
  56. BEAR is 2019's restated fall (-53.9%/yr) throughout ($12-22); the EPP floor is 12-13x; the proxy composite ranges from 2.15 to
  3.10, the market composite from 1.48 to 2.85.

How far each call moves the classes (the 148 dates rebuilt with one encoding changed; no outcome consulted):
- GAAP EPS in every year (2019 $3.36, 2021 $5.39, 2022 $13.26, 2023 $8.89, 2024 $7.84, 2025 $6.70) would change 25 classes (19 CHEAP to
  FAIR in 2024 on FY23's $8.89, 4 FAIR to RICH in 2026 on FY25's $6.70, one each way in 2025) and 50 tiers;
- BASE on the latest quarter's oil-equivalent production growth instead of revenue growth would change 24 classes (4 in 2024, 9 in 2025,
  11 in 2026; 13 FAIR to CHEAP, 11 FAIR to RICH) and 47 tiers;
- both together: 28 classes and 69 tiers;
- year-ago volumes from the year-to-date columns instead of the year-ago releases (a test only: a different period): 5 classes (CHEAP to
  FAIR, 2025-02-21 to 2025-04-25), no tier;
- without the re-file: no class, 148 labels.

Judgement calls that could carry hindsight (in addition to the earlier XOM lists, which stand):
- the company's figures excluding identified items for FY2023-FY2025, and the timing-effects figure left out as recurring (25 classes
  move at GAAP);
- year-ago volumes read against the year-ago quarter's own release where a release prints none;
- BASE on revenue growth, which again decides most classes (24 move on production growth), and in Q2-Q3 2026 runs at +32% to +42%/yr;
- the Middle East supplement of 2026-04-08, the Corporate Plan notices and the capex ranges read as adding nothing;
- the re-file kept to the end of the range: the method has no rule that ends one (label only).

## SHW (Sherwin-Williams): the tenth ticker, in staging

The SHW series is built apart from ACN, UNP, LOW, AAPL, NKE, AVGO, PEP, MSFT and XOM and shares nothing with them but the machinery:
its own fact sheet (`retro/facts/SHW.json`), builder (`retro/build_shw.py`, the LOW guide list with the XOM rule-T and raw-figure
checks) and engine (`retro/templates/shw_engine.py.tmpl`, the XOM engine with paint and coatings signals). The method is still r2. No
fact, parameter, outcome or finding of another ticker enters an SHW model, and neither does today's live profile of SHW in
`data/business_profiles.json` (a 2026 judgement, not read for this series). Outputs go to `staging/retrospective/SHW/`, beside the
others, with the same `index.json` and their own `SERIES.md`.

```bash
python3 retro/build_shw.py --weekly 2008-01-01 2008-12-31                   # 53 dates, 2008-01-04 .. 2008-12-31
for d in staging/retrospective/SHW/2008-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series SHW
python3 retro/tools/firewall.py 2008-07-01 SHW
python3 retro/tools/firewall.py 2009-01-01 SHW
for c in 2008-02-01 2008-03-25 2008-04-24 2008-06-05 2008-10-18; do python3 retro/tools/firewall.py $c SHW; done
for c in 2009-07-01 2010-01-01 2010-07-01 2011-01-01 2011-04-21 2011-07-01 2012-01-01; do python3 retro/tools/firewall.py $c SHW; done
for c in 2012-04-10 2012-07-01 2013-01-01 2013-02-22 2013-07-01 2013-10-26 2014-01-01 2014-04-18 2014-07-01 2014-12-13 2015-01-01; do python3 retro/tools/firewall.py $c SHW; done
for c in 2015-01-30 2015-04-17 2015-07-17 2016-01-29 2016-03-22 2016-07-01 2017-01-27 2017-04-21 2017-07-21 2017-10-25 2018-01-01; do python3 retro/tools/firewall.py $c SHW; done
for c in 2018-01-26 2018-07-25 2019-01-16 2019-02-01 2019-07-01 2020-01-31 2020-04-30 2020-07-29 2020-10-28 2021-01-01; do python3 retro/tools/firewall.py $c SHW; done
for c in 2021-01-29 2021-02-04 2021-04-01 2021-04-28 2022-01-14 2022-02-18 2022-07-28 2022-10-26 2023-01-27 2023-07-26 2024-01-01; do python3 retro/tools/firewall.py $c SHW; done
for c in 2024-01-26 2024-02-21 2024-07-24 2025-01-31 2025-02-21 2025-07-23 2025-10-02 2026-01-30 2026-02-20 2026-07-29 2026-10-28 2026-11-02; do python3 retro/tools/firewall.py $c SHW; done
```

The 10-Ks from FY1998 to FY2007 were read for the history and the decade's signal values (the FY1998-FY2004 annual reports, Exhibit 13,
are plain-text filings), and every 8-K and 10-Q of October 2006 to November 2008 (29 filings, the two outlook 8-Ks of 2008-03-24 and
2008-06-03 among them), by Opus directly, with no delegated transcription. The fact sheet is generated from the transcribed raw figures
by a script, so every growth rate, margin and rule-T change is computed, not typed; 202 strings were checked with `verbatim.py` against
their own filings (every statement-of-income row behind a print, every stated comparable-store, Consumer Group and currency figure, every
guide). Each source's date comes from EDGAR's acceptance time (converted from UTC; before 2003 EDGAR gives the filing date only).
Decided on 2026-11-05, before any SHW model was built or any SHW outcome computed:

- **Fiscal calendar.** Sherwin-Williams' fiscal year is the calendar year. The four dates of January 2008 have FY2007 as the current year
  (its EPS guide; no FY07 EPS yet), until the Q4 2007 print adds FY07 on 2008-01-29.
- **Prices on the as-of share basis** (the UNP rule). Sherwin-Williams split three-for-one on 2021-04-01, after every 2008 date, so the
  builder multiplies Yahoo's split-adjusted series by three: $54.08 as traded on 2008-01-04. The two-for-one split of 1997-03-31 precedes
  every per-share fact in the fact sheet (the earliest is the FY1998 10-K), so nothing is restated.
- **Release timing.** The earnings 8-Ks of Q2 2007 to Q3 2008 were accepted during the session on the release day (09:32-10:08 ET; the
  conference call at 11:00 a.m. ET), each on a Tuesday or Thursday, so a print dates its week the next trading day: 2008-01-30,
  2008-04-23, 2008-07-18 and 2008-10-17. The outlook 8-Ks were accepted 2008-03-24 08:52 ET (before the open) and 2008-06-03 09:33 ET.
  The FY2006 10-K, accepted 2007-02-28 17:29 ET, is dated 2007-03-01; the FY2007 10-K, accepted 2008-02-28 09:55 ET, keeps its date.
- **History: each year from the latest filing that reports it.** Net sales from the latest statement of consolidated income that reports
  the year (FY2006 vintage: 2004-2006 from the FY2006 10-K, 2003 from the FY2005 10-K, back to 1997 from the FY1999 10-K); EPS from the
  latest five-year financial summary (2002-2006 from the FY2006 10-K, 2001 from the FY2005 10-K, 1999 from the FY2003 10-K, 1998 from the
  FY2002 10-K, 1997 from the FY2001 10-K); diluted shares of the first and last year from the earnings-per-share notes (1997's
  174,032,342 from the FY1999 10-K). The Q4 2007 release extends the history with FY07 from 2008-01-29, and the FY2007 10-K moves the
  window to 1998-2007. The 1997 Thompson Minwax acquisition (net sales +18.1%) stays in, as published (the LOW and PEP rule).
- **EPS** is diluted EPS before the cumulative effect of the 2002 change in accounting principle (the NKE rule): 2002 $2.04 ($.84 after
  it). The company's figure excluding the 2000 impairment of long-lived assets replaces 2000's GAAP $.10 (the ACN rule): $1.90, from the
  FY2002 10-K's "Results/Ratios Excluding Impairment Charge", the latest filing that publishes it (the $352,040K charge, mostly Consumer
  Segment goodwill, exceeded the year's $16,026K net income). 2005's $22,000K goodwill impairment and 2007's (about $.08 a share; the
  release gives no figure excluding it) stay in. **No year is excluded.**
- **Guides: EPS in numbers, net sales mostly in words.** Every release (and the outlook 8-Ks) guides the next quarter's and the year's
  diluted EPS as ranges. Net sales are guided in numbers only in the Q2 and Q3 2007 releases (Q3 2007 "between 4% and 6%"; Q4 2007
  "between 5.0% and 6.0%, including acquisitions", FY2007 "between 2.5% and 3.5%"); every other statement is words ("a low-to-mid single
  digit percentage increase", "slightly lower than 2007", "plus or minus in the low single digits"), and words are not figures (the UNP
  2016 rule). Method r2 maps them as for LOW:
  - current-FY EPS: the midpoint of the latest fiscal-year EPS range for the current year: FY07 $4.725 ($4.70-4.75, Q3 2007 release) to
    2008-01-25; FY08 $5.075 ($5.00-5.15, Q4 2007 release), $4.775 from the 8-K of 2008-03-24 ($4.70-4.85, reaffirmed 2008-04-22), $3.85
    from the 8-K of 2008-06-03 ($3.60-4.10, reaffirmed 2008-07-17) and $4.07 from the Q3 2008 release ($3.97-4.17);
  - BASE growth and the growth factor: the Q4 2007 net sales guide, +5.0% to 6.0% as published (in dollars, including acquisitions; no
    filing guides in local currency, the MSFT and LOW reading), to 2008-01-25; from the Q4 2007 print, with no net sales guide in numbers,
    the latest quarter's net sales growth less the currency effect the release states (the NKE and PEP rule): +2.0% (Q4 2007: 3.3 less
    1.3), -0.1% (Q1 2008: 1.5 less 1.6), +0.3% (Q2 2008: 1.4 less 1.1), +2.4% (Q3 2008: 3.3 less 0.9); acquisitions stay in (1.7-2.9
    points a quarter);
  - no margin guide, so no margin step: the margin signal takes the latest quarter's pre-tax margin change.
  - The next quarter's EPS range and every statement in words are shown in the guide line and feed no input.
- **Dividends,** from the 10-K that states the rate: $.315 a quarter (FY2006 10-K, increased February 21, 2007), $.35 from the FY2007
  10-K (increased February 20, 2008). The releases state no rate.
- **Signals.** Six, with ACN's weights, in the LOW layout: Paint Stores comparable-store sales (0.20, the release's "net sales from stores
  open for more than twelve calendar months"), gross margin change (0.20), net sales growth (0.15, as reported), Consumer Group net sales
  growth (0.15, as the release states it), the pre-tax margin change (0.15: income before income taxes on net sales; the statement of
  income has no operating-income line) and the theme slot at 2/4. The releases carry no balance sheet, so LOW's inventory signal has no
  quarterly value; its slot goes to the Consumer Group, the one other segment with a decade of history in the 10-Ks (the Global Group
  was formed in 2006 from parts of the other segments, with history from 2004). Margins and net sales growth are derived from the raw
  figures of each release's statement of income (the fact sheet keeps them in thousands and the builder re-derives each value).
- **Thresholds by rule T** over the decade of the FY2006 10-K, the vintage public on 2008-01-04: 1997-2006, each change from the latest
  10-K published by then that reports both years (statements of income for the margins and net sales; the five-year segment tables, in
  millions, or the MD&A table in thousands where the same filing has one, for the Consumer segment's net external sales). No 10-K states
  1997's comparable-store sales, so that signal has the nine years 1998-2006 (rule T takes the annual values the filings report).
  2000's income before income taxes is the company's figure excluding the impairment, $495,446K (the FY2002 10-K; the LOW rule for a
  published excluding figure). Seams stay in, as published: Thompson Minwax in 1997, the FY2002 10-K's restatement of the Consumer
  segment for 2000-2001, the 2006 realignment into the Paint Stores, Consumer and Global Groups. The values are in the fact sheet
  (`rule_t`); the builder recomputes the thresholds and refuses to build if the engine's differ.

  | Signal | 1997-2006 | BEAR / BASE / BULL / XBULL |
  |---|---|---|
  | comparable-store sales (1998-2006) | 4.9, 4.0, 3.7, -1.3, 1.9, 4.0, 10.1, 13.6, 9.1 % | -7 / -1 / 4 / 14 % |
  | gross margin change | 115.2, 21.0, 177.0, -65.8, -46.4, 129.1, 29.8, -121.8, -134.7, 88.4 bp | -290 / -130 / 30 / 180 bp |
  | net sales growth | 18.1, 1.09, 1.41, 4.15, -2.79, 2.34, 4.3, 13.06, 17.61, 8.61 % | -10 / -3 / 4 / 18 % |
  | Consumer Group net sales growth | 21.26, -9.01, -4.52, 2.21, -8.71, 3.15, 1.02, 8.96, 7.62, -1.94 % | -20 / -9 / 2 / 21 % |
  | pre-tax margin change | -32.9, 16.5, 87.6, -28.8, -112.8, 121.1, 8.1, -18.0, -36.4, 155.7 bp | -220 / -110 / 0 / 160 bp |

- **Durability: DURABLE, risk 2** (the LOW precedent). The "why" quotes the 10-K: the company "is engaged in the manufacture,
  distribution and sale of paint, coatings and related products", "a leading manufacturer and retailer", 3,046 (then 3,325)
  company-operated paint stores, and "Portions of our business involve the sale of paint, coatings and related products to segments of
  the economy that are cyclical in nature, particularly segments relating to construction, housing and manufacturing". Portions of a
  business that follow a cycle are not earnings that are the cycle (XOM's "fundamentally a commodity business"), so CYCLICAL is not
  used; the kind changes the class label only. No disruption theme in `taxonomy_eras.json` is live for a paint and coatings maker in
  2008 (ECOMMERCE, scoped to physical retail, from 2015-01-01), so the watch list is empty and the builder refuses events until a theme
  encoding is decided.
- **Segment bridge and EPS check** (display only): the 10-K's segments by net sales (Paint Stores, Global, Consumer, Administrative),
  the total from the fiscal-year net sales guide (FY2007) or the BASE fallback applied to the last year (FY2008); the EPS check runs on
  the pre-tax margin. A renamed reporting line takes its new name from the first print that uses it (the ACN rule): the Global Finishes
  Group from the Q3 2008 release (2008-10-16).
- **Adds nothing:** the credit-agreement, indenture and officer 8-Ks (2007-04-26, 2007-08-29, 2007-09-17, 2007-09-25, 2008-02-26,
  2008-06-02), the XBRL test filing of 2008-11-03, and the 10-Qs beyond their dividends (the releases come first and carry every print
  value).
- **Anachronism list:** Sherwin-Williams names first seen in its filings after the start of 2008 (Global Finishes Group from 2008-10-16,
  Latin America Coatings Group, HGTV HOME, The Americas Group, Consumer Brands Group, Performance Coatings Group) join
  `taxonomy_eras.json`, each dated from the first Sherwin-Williams filing that uses it (EDGAR full-text search). No existing model of any
  ticker contains them, so no output changes. SHW's source ids are `SH1`-`SH20`.

Controls: altering one value of each print, guide and vintage changes no date before its publication and changes the first weekly date
on or after it whenever the value is in scope (37 controls; the four that change nothing are three 2007 EPS ranges that later guides
supersede and the Q2 2007 pre-tax margin, never the latest print on a 2008 date). Rebuilding the 2008 dates of ACN, UNP, LOW, AAPL, NKE, PEP, MSFT and XOM and the 2009 dates of AVGO
changes nothing. A scan of the 53 models for the figures, notes, guides and texts of every later print, guide and vintage finds none
before its first publication (0 of 1,486; the Q1 and Q2 2008 releases' reaffirmed ranges were already public from the 8-Ks of
2008-03-24 and 2008-06-03).

Seen in the build (method behaviour, not tuned):
- **CHEAP to April, RICH from June.** CHEAP on 19 dates (2008-01-04 to 2008-04-23, 2008-05-23, 2008-05-30), FAIR on 2 (2008-05-02,
  2008-05-09) and RICH on 32 (2008-05-16, 2008-06-06 to 2008-12-31). Robustness 8 of 8 on every date to 2008-04-18 and from 2008-07-18,
  1 to 7 of 8 from 2008-04-23 to 2008-07-11. The legacy tier is BUY to 2008-07-11 and then follows the price: ACCUMULATE on 13 dates,
  WATCHLIST on 6, AVOID on 6 between 2008-08-15 and 2008-09-26.
- **The EPS guide carries the call.** The P/E window barely moves all year (10th percentile 11.4-11.6x, median 13.5-13.7x, 90th
  percentile 15.3-16.6x); the current-FY EPS falls from $5.075 to $3.85 between January and June as the guide is cut twice, so a $47-63
  price that was 9.9-12.5x (1st-27th percentile) in January-May is 12.2-16.5x (19th-96th percentile) from June, and the BULL price falls
  from $88-96 to $72-75.
- **BEAR is 2001** (-11.6%/yr: 2000's $1.90 excluding the impairment to 2001's $1.68) at the 10th-percentile P/E (11.4-11.6x): $43-46 in
  January-May, $35-37 from June. XBULL is the 2004-2006 run (+24.1%/yr); BULL the decade CAGR (+12.1%, then +13.0% over 1998-2007).
- **BASE is the guide, then the quarter less currency.** +8.2%/yr to 2008-01-25 (the Q4 2007 guide's 5.5% plus a 2.7% buyback), +4.9%
  from the Q4 2007 print, +5.2% from the FY2007 10-K, +3.1% from Q1 2008, +3.5% from Q2 2008 and +5.6% from Q3 2008 (diluted shares fell
  2.7%/yr over 1997-2006, 2.9% over 1997-2007 and 3.2% over 1998-2007).
- **The proxy composite** is 2.35 through the Q4 2007 print (gross margin +78bp and +192bp at BULL or better, the pre-tax margin at BULL,
  comparable-store sales at BASE until Q4 2007's -2.5%), then 1.65 from Q1 2008 (comps -6.5% and -4.5% at BEAR, gross margin -125bp at
  BASE, the pre-tax margin -297bp and -230bp at BEAR) and 1.45 from Q3 2008 (gross margin -265bp at BEAR). The market composite rises
  from 1.6-2.4 in January-May to 2.6-3.5 from mid-July, so the adjusted gap runs from +1.14 to -2.06.

How far each call moves the classes (the 53 dates recomputed with one encoding changed; no outcome consulted):
- BASE on reported net sales growth instead of growth less currency: 4 classes (2008-05-02 and 2008-05-09 FAIR to CHEAP, 2008-06-27 and
  2008-07-11 RICH to FAIR), no tier;
- the Consumer Group signal at BEAR on every date: 5 classes (2008-04-23 to 2008-05-30, toward RICH); at XBULL on every date: 8 classes
  (2008-05-02 to 2008-07-11, toward CHEAP), no tier either way, which brackets any other choice of the fourth signal;
- the pre-tax margin thresholds with 2000 at GAAP (-1420 / -700 / 10 / 560 bp): 6 classes (2008-05-02 to 2008-07-11, toward CHEAP), no
  tier.
Every move falls in May-July 2008, where the class already changes from week to week; January-April CHEAP and August-December RICH hold
under all of them.

Judgement calls that could carry hindsight:
- the signals, chosen by a builder who knows that housing and DIY demand fell through 2008: Paint Stores comparable-store sales, and the
  Consumer Group for the slot LOW's inventory signal fills (rule T then sets the thresholds mechanically);
- DURABLE rather than CYCLICAL (the class label only), despite the 10-K's "cyclical in nature" for portions of the business;
- the company's 2000 figures excluding the impairment, in the EPS history and in the pre-tax margin's rule-T values (6 classes move at
  GAAP);
- net sales guides in words read as no field, and BASE in 2008 on the latest quarter's growth less the stated currency effect (4 classes
  move on reported growth);
- the Q4 2007 net sales guide used as published, including acquisitions, in dollars.

### SHW 2009-2011: three more vintages, sales guides back in numbers, the 2010 acquisitions, the IRS settlement

```bash
python3 retro/build_shw.py --weekly 2009-01-05 2011-12-31                   # 156 dates, 2009-01-09 .. 2011-12-30
```

Every 8-K, 10-Q and 10-K of January 2009 to December 2011 was read (41 filings), by Opus directly, with no delegated transcription.
The fact sheet's 2009-2011 records are generated by script from the transcribed raw figures, as in 2008; 258 more strings were checked
with `verbatim.py` (460 in all). Thresholds (rule T), signals and the engine are unchanged. Decided before any 2009-2011 date was built
or scored:

- **Three 10-K vintages, each with a Q4 print before it.** The FY2008 10-K (accepted 2009-02-24 15:05 ET), FY2009 (2010-02-24 12:53 ET)
  and FY2010 (2011-02-23 15:33 ET), all during the session, so each keeps its date; the history moves to 1999-2008, 2000-2009 and
  2001-2010, each year from the latest filing that reports it. First-year diluted shares: 1999's 169,026,296 from the FY2001 10-K,
  2000's 162,695,071 from the FY2002 10-K, 2001's 156,893,535 from the FY2003 10-K. Each Q4 release (2009-01-22, 2010-01-26,
  2011-01-25) extends the history with its year until the 10-K.
- **Two restatements, as published.** The FY2008 10-K moves trademark impairments out of cost of goods sold (2007: $4,406,365K against
  $4,406,965K first reported), and the Q4 2008 release shows its year-ago quarter that way (the MSFT recast rule: Q4 2007 cost of goods
  sold $1,021,282K). The FY2010 10-K adopts the two-class EPS method and restates diluted shares (2009: 114,457,488 against 115,422,933);
  diluted EPS is unchanged, and each vintage takes its own year (the LOW FY2006 rule).
- **EPS: GAAP in every new year.** Each release gives its one-offs "including" the item and publishes no figure excluding it (the
  Fremont rule): 2008's asset impairments ($.31 a share), 2009's impairments and loss on dissolution of a foreign subsidiary ($.13),
  2010's health care tax charge ($.10), debt repurchase costs ($.12), impairments ($.04) and site-sale gain ($.04). FY08 $4.00, FY09
  $3.78, FY10 $4.21. No year is excluded. Each vintage's normalization note names only the items of the years it reports.
- **Guides.** Every release gives EPS ranges for the next quarter and the year. Net sales are in numbers for the next quarter in four
  2009 releases and three 2011 releases (Q2 2009 "decline nine to twelve percent", Q3 2009 10-13% below, Q4 2009 8-12% below, Q2 2011
  +8-13%, Q3 2011 +10-15%, Q4 2011 +6-10%) and for the year in two (FY2009 11-12.5% and 11.5-12.5% lower); every 2010 statement and the
  other 2009 and 2011 ones are words. Method r2 maps them as in 2008: current-FY EPS is the latest EPS midpoint (FY09 $3.50, $3.55,
  $3.62; FY10 $4.25, $4.40, $4.32, $4.17; FY11 $4.85, $4.75); BASE takes the next-quarter net sales range while its quarter is unreported,
  else the latest quarter's growth less (or plus) the currency effect the release states: -5.5% (Q4 2008: -8.3 plus 2.8), -7.9% (Q4
  2009), -1.9% (Q1 2010), +8.7% (Q2 2010), +8.2% (Q3 2010), +18.2% (Q4 2010, with acquisitions adding 8.7 points). Acquisitions stay in.
- **A guide with and without an announced item.** The Q3 2011 release (2011-10-25) guides FY2011 at "$4.65 to $4.85 per share before
  the IRS settlement and in the range of $3.93 to $4.13 per share due to the settlement"; the guide is used without the item (the ACN
  FY15 rule), the other range in its note. Its fourth-quarter EPS range ($(.05) to $.15) includes the $.72 charge and is display only.
  The 8-K of 2011-10-24 announcing the settlement (accepted 17:16 ET, dated 2011-10-25) changes no guided number and adds nothing.
- **A release before Good Friday.** The Q1 2011 release came on Thursday 2011-04-21; its 8-K was accepted at 09:51 ET, during the
  session, and no filing states an earlier release time. No trading day followed in its week, so the week's date is the release day and
  the print counts for that close (the UNP Good Friday 2014 rule; the builder now accepts a same-day print accepted "before the close" and
  tags it "released during the session"). Every other print of the period dates its week the next trading day.
- **Dividends,** from the 10-K that states the rate: $.355 a quarter (FY2008 10-K, increased February 18, 2009), $.36 (FY2009 10-K,
  February 17, 2010), $.365 (FY2010 10-K, February 16, 2011). The Q1 2010 and Q1 2011 releases repeat the increases later.
- **Adds nothing:** the director, officer and compensation 8-Ks, the debt and credit-facility 8-Ks (2009-12-17, 2010-01-11,
  2010-07-21, 2011-07-13), the Becker Acroma agreement and completion (2010-05-24, 2010-09-02; no guided number), the IRS notice of
  2011-05-23, and the 10-Qs beyond what the releases give.
- **Builder changes (no 2008 output changes; the 53 dates rebuild byte-identical):** the same-day print rule above; a negative currency
  effect reads "plus the 2.8pp currency drag"; a guide's EPS note and a loss in an EPS range ("$(0.05)-0.15") print.

Controls: altering one value of each new print (with each Q4 print's full-year actuals), guide and vintage changes no date before its
publication and changes the first weekly date on or after it (57 of 57). A scan of all 209 SHW models for the figures, notes, guides and
texts of every print, guide and vintage finds none before its first publication (0 of 24,186); no model carries a calendar year after its
date outside an FY label. The first build of this batch failed that last check: a normalization note shared by the three new vintages
named 2009's and 2010's items in 2009 models, and the lint's warning caught it before anything was committed.

Seen in the build (method behaviour, not tuned):
- **RICH on 151 of 156 dates.** FAIR only on 2011-02-25, 2011-03-04, 2011-03-18, 2011-08-19 and 2011-09-23. The legacy tier is AVOID
  on 130 dates (all 52 of 2010), WATCHLIST on 22 and ACCUMULATE on 4 (2009-03-06, 2009-03-20, 2011-08-19, 2011-09-23); robustness 7-8 of
  8 in 2009-2010, 3-8 of 8 in 2011.
- **The guided trough again.** The P/E window stays tight (10th percentile 11.6-12.1x, median 13.5-14.1x, 90th 15.2-17.4x), while the
  anchor is the guided year: FY09 $3.50-3.62 (from the Q4 2008 print), FY10 $4.17-4.40 (from the Q4 2009 print), FY11 $4.75-4.85 (from
  the Q4 2010 print). The price ($43-63 in 2009, $58-84 in 2010, $70-90 in 2011) is 12-18x, 15-20x and 15-20x of the anchor: the
  22nd-100th percentile of its own range in 2009 and the 82nd-100th in 2010.
- **BEAR is 2008's -14.9%/yr** ($4.70 to $4.00) from the Q4 2008 print, at the 10th-percentile P/E: $29-42. XBULL stays the 2004-2006 run
  (+24.1%/yr). BASE runs from -7.6%/yr (2009's guided sales declines) to +22.4% (Q4 2010's acquisition-swollen +18.2% ex-currency plus
  a 4.1% buyback), so from the Q2 2010 print BULL equals BASE.
- **The proxy composite** reads 1.45-2.20 in 2009 (comps -10% to -13.5% at BEAR; gross margin +233bp and +418bp at XBULL from Q2 2009),
  2.00-2.65 in 2010-2011 (comps +5% to +9% at BULL, gross margin -62bp to -294bp at BASE or BEAR from Q2 2010 as raw materials rose).
  The market composite runs 2.4-3.9, so the adjusted gap stays at -0.2 to -2.5 throughout.

How far each call moves the classes (the 156 dates recomputed with one encoding changed; no outcome consulted):
- BASE on reported net sales growth instead of growth less currency: 1 class (2011-03-11 RICH to FAIR), 3 tiers;
- the Consumer Group signal at BEAR on every date: 4 classes (FAIR to RICH in 2011); at XBULL: 10 classes (RICH to FAIR: 2009-03-06 and
  nine 2011 dates), no tier either way;
- the pre-tax margin thresholds with 2000 at GAAP: 3 classes (RICH to FAIR, 2011-08-26 to 2011-09-09), no tier;
- the FY2011 EPS guide including the IRS settlement ($3.93-4.13) on the 10 dates from 2011-10-26: no class, no tier;
- the Q1 2011 print counted from the next week instead of 2011-04-21: no class, 1 tier (AVOID to WATCHLIST).

Judgement calls that could carry hindsight (in addition to the 2008 list, which stands):
- the FY2011 guide taken before the IRS settlement (no class moves either way);
- the Q1 2011 print counted on its release day from an 8-K accepted during the session (one tier moves);
- net sales guides in words read as no field, with BASE falling back to the quarter's growth less currency, which carries the 2010-2011
  acquisitions (Sayerlack, Becker Acroma, Pinturas Condor, Leighs) into BASE.

### SHW 2012-2014: the DOL settlement, Comex, guides in numbers again, two more same-day prints

```bash
python3 retro/build_shw.py --weekly 2012-01-02 2014-12-31                   # 157 dates, 2012-01-06 .. 2014-12-31
```

Every 8-K, 10-Q and 10-K of January 2012 to December 2014 was read (53 filings), by Opus directly, with no delegated transcription.
The fact sheet's 2012-2014 records (sources `SH36`-`SH53`) are generated by script from the transcribed raw figures, as before; 285 more
strings were checked with `verbatim.py` (745 in all). Thresholds (rule T), signals and the engine are unchanged. Decided before any
2012-2014 date was built or scored:

- **Three 10-K vintages, each with a Q4 print before it.** The FY2011 10-K (accepted 2012-02-23 15:07 ET), FY2012 (2013-02-28 11:06 ET)
  and FY2013 (2014-02-27 14:26 ET), all during the session; the history moves to 2002-2011, 2003-2012 and 2004-2013, each year from the
  latest filing that reports it. First-year diluted shares: 2002's 152,435,310 from the FY2004 10-K, 2003's 147,005,276 from the FY2005
  10-K, 2004's 144,735,589 from the FY2006 10-K. The segments are four from the Q4 2011 release, which reports the Latin America Coatings
  Group on its own; each vintage's business line names them as its own 10-K does.
- **FY2011 at GAAP.** The Q4 2011 release gives $4.14 "including a $.70 per share charge related to the IRS settlement" and publishes no
  figure excluding it (the Fremont rule), though the Q3 2011 guide was framed before it ("SHW 2009-2011"). The year is not excluded.
- **FY2012: the company's figure without the DOL settlement.** The Q4 2012 release (2013-01-31) reported $6.49. The 8-K of 2013-02-21
  recorded the $80.0 million ESOP settlement with the U.S. Department of Labor in the fourth quarter of 2012 and published both columns:
  $6.49 "As Reported" and $6.02 revised; the FY2012 10-K carries $6.02. The vintages from 2013-02-28 take $6.49, the company's figure
  without the one-off (the ACN rule), with $6.02 in the GAAP column and the normalization note; the FY2012 pre-tax margin and tax rate
  are as reported before the settlement. The Q4 2013 release shows its year-ago quarter as revised (the MSFT recast rule: $.65,
  income before income taxes $94,193K). Dates from 2013-02-01 to 2013-02-15 see the Q4 2012 print and nothing of the settlement.
- **FY2013 at GAAP, Comex in.** 2013's Brazil tax assessments ($.21) and early retirement of debt ($.02) are "including" items with no
  figure excluding them: $7.26. The Comex acquisition (agreed 2012-11-12; the U.S. and Canada stores closed in September 2013, the Mexican
  business never did) is an acquired operation, not a one-off: its losses stay in the year and in every guide, as the 2010 acquisitions
  did. The Q3 2013 release guides FY2013 at $7.00-7.30 "including" Comex and $7.40-7.50 without it; the guide with Comex is used, because
  the item is the business bought, not a charge, and the year's actual and the FY2014 guides (published with Comex only) are on that
  basis. Its fourth-quarter net sales range (+5-7%) is "core", before Comex's $95-105 million, and its full-year 5.0-7.0% is "Without
  Comex": both are used as stated, with the note.
- **Guides.** Every release gives EPS ranges for the next quarter and the year. Net sales for the next quarter are in numbers in the
  first two releases of 2012 (Q1 2012 +9-14%, Q2 2012 +10-15%) and in every release from Q1 2013 (Q2 2013 +5-9% to Q4 2014 +6-8%); for
  the year from Q3 2013 (FY2013 5.0-7.0%, FY2014 8-13% and then 9-11%); the Q2 2012 to Q4 2012 releases give them in words. Current-FY EPS
  is the latest EPS midpoint (FY12 $5.52, $5.90, $6.30, $6.45; FY13 $7.50, $7.15; FY14 $8.22, $8.60, $8.75, $8.78). Two outlook 8-Ks
  between releases: 2012-04-09 (11:46 ET, during the session) raises only the Q1 2012 EPS range ($.92-.95 from $.56-.74), so the builder
  now takes each field of a quarter's guide from the latest guide that states it, and the release's +9-14% sales range stands; 2014-12-12
  (07:56 ET) narrows FY2014 to $8.75-8.80 and "approximately nine percent" and gives a preliminary FY2015 ($10.65-10.85, +7-11%), which
  no date of this batch uses (FY2015 becomes current only with the Q4 2014 print).
- **Same-day prints.** The Q3 2013 release came on Friday 2013-10-25 (8-K accepted 07:16 ET) and the Q1 2014 release on Thursday
  2014-04-17, before Good Friday (08:42 ET): both before the open, so each counts for that day's close, the week's date (the 2011-04-21
  rule). Every other print of the period dates its week the next trading day.
- **Dividends,** from the 10-K that states the rate: $.39 a quarter (FY2011 10-K, February 15, 2012), $.50 (FY2012 10-K, February 13,
  2013), $.55 (FY2013 10-K, February 19, 2014).
- **Adds nothing:** the director, officer, compensation and annual-meeting 8-Ks, the credit-facility and note 8-Ks of 2012-2013 (the
  December 2012 $1.0 billion note sale among them), the Comex agreement, amendment and dispute 8-Ks (2012-11-13, 2013-06-27, 2013-08-26,
  2013-09-17, 2014-04-07; no guided number), the lead-pigment trial notice of 2013-07-05, and the 10-Qs beyond what the releases give.
- **Builder change (no 2008-2011 output changes; the 209 dates rebuild byte-identical):** the field-by-field quarter guide above.

Controls: altering one value of each new print (with each Q4 print's full-year actuals), guide and vintage changes no date before its
publication and changes the first weekly date on or after it (75 of 75; the preliminary FY2015 guide changes none, being out of scope). A
scan of all 366 SHW models for the figures, notes, guides and texts of every print, guide and vintage finds none before its first
publication (0 of 76,318); no model carries a calendar year after its date outside an FY label. Two first builds of this batch failed
those checks before anything was committed: the Q4 2012 print's EPS note cited the 8-K of 2013-02-21 (three dates before it saw it), and
the 2014-12-12 source title named "2015" as a calendar year.

Seen in the build (method behaviour, not tuned):
- **RICH and AVOID on all 157 dates,** robustness 7-8 of 8 (8 of 8 throughout 2013).
- **The multiple left its own range.** The price ran $93-159 in 2012, $158-195 in 2013 and $183-265 in 2014, 17.6-24.7x, 21.0-27.3x
  and 22.2-30.2x the guided year: the 87th-100th percentile of its own ten-year range. The window began to move with it: the median rose
  from 14.1x to 15.8x and the 90th percentile from 17.4x to 24.1x, as 2011-2014's own multiples entered it. The EPP floor is 12x, 13x from
  2014-03-28; the price stood 47-132% above it.
- **BEAR is 2008's -14.9%/yr** throughout, at the 10th-percentile P/E (12.1-12.7x): $42-81. XBULL is the 2004-2006 run (+24.1%/yr), the
  2010-2012 run (+24.2%) from the FY2012 10-K and, from the Q4 2013 print, 2011-2013 (+32.4%/yr, from the IRS-depressed $4.14 to $7.26).
  BASE runs +9.9% to +16.7%/yr; BULL is the decade CAGR (+11.2% to +15.7%/yr) or BASE where BASE is higher.
- **The proxy composite** reads 2.15-3.05 (Paint Stores comps +3% to +20%: BULL on 131 dates, BASE on 13, XBULL on 13); the market
  composite 3.19-3.93; the adjusted gap -0.27 to -1.68. The conservative two-year case runs -39% to +6%.

How far each call moves the classes (the 157 dates recomputed with one encoding changed; no outcome consulted): BASE on reported net
sales growth; the Consumer Group signal at BEAR or at XBULL on every date; the pre-tax margin thresholds with 2000 at GAAP; FY2012 at GAAP
$6.02 (97 dates); FY2011 before the IRS charge, $4.84 (154 dates); the FY2013 guide without Comex, $7.40-7.50, and the Q4 2013 sales guide
with Comex's $95-105 million added (14 dates each): no class and no tier, each.

Judgement calls that could carry hindsight (in addition to the 2008 and 2009-2011 lists, which stand):
- FY2012 at the company's $6.49 rather than GAAP $6.02 (no class moves either way);
- Comex treated as an acquired operation (losses in, the FY2013 guide with it) rather than an item (no class moves either way);
- FY2011 at GAAP with the IRS charge, which lifts XBULL to +32.4%/yr from 2014-01-31 (no class moves either way).

### SHW 2015-2017: adjusted EPS from the Valspar costs, the treasury stock method, a revenue reclassification, Valspar in the sales

```bash
python3 retro/build_shw.py --weekly 2015-01-05 2017-12-31                   # 156 dates, 2015-01-09 .. 2017-12-29
```

Every 8-K, 10-Q and 10-K of January 2015 to December 2017 was listed (60 filings: 47 8-Ks, nine 10-Qs, three 10-Ks and the S-4 of
2017-06-23). The twelve earnings releases (Q4 2014 to Q3 2017) and the three 10-Ks were read for the facts, by Opus directly, with no
delegated transcription; every other 8-K, the 10-Qs and the S-4 were checked for a guided number (none has one). The fact sheet's records
(sources `SH54`-`SH68`) are generated by script from the transcribed raw figures, as before; 286 more strings were checked with
`verbatim.py` (1,031 in all), among them every statement-of-income row behind a print, every quoted note and guide, every Regulation G
row behind an adjusted EPS figure, and the first-year diluted share counts of 2005-2007 in the FY2007-FY2009 10-Ks. Thresholds (rule T),
signals and the engine are unchanged. Decided before any 2015-2017 date was built or scored:

- **Three 10-K vintages, each with a Q4 print before it.** The FY2014 10-K (accepted 2015-02-25 14:18 ET), FY2015 (2016-02-24 14:23 ET)
  and FY2016 (2017-02-22 14:13 ET), all during the session; the history moves to 2005-2014, 2006-2015 and 2007-2016, each year from the
  latest filing that reports it. First-year diluted shares: 2005's 141,078,932 from the FY2007 10-K, 2006's 137,342,108 from the FY2008
  10-K, 2007's 130,924,690 from the FY2009 10-K. Each Q4 release (2015-01-29, 2016-01-28, 2017-01-26) extends the history with its year
  until the 10-K.
- **The treasury stock method, as published.** The FY2016 10-K computes EPS by the treasury stock method instead of the two-class method
  and restates 2013-2015 for comparability: $7.25, $8.77 and $11.15 (against $7.26, $8.78 and $11.16). The FY2016 vintage takes them
  (each year from the latest filing that reports it, the LOW FY2006 rule); 2012 stays the company's $6.49 without the DOL settlement, the
  only figure published excluding it.
- **EPS: GAAP until the Valspar costs, then the company's figure without them.** 2014's environmental provisions ($.22), Comex loss ($.18)
  and titanium dioxide settlement gain ($.13) are "including" items with no figure excluding them: FY2014 $8.78. FY2015 has none listed:
  $11.16. From the Q1 2016 release (2016-04-21) every release publishes a Regulation G table beside GAAP, and the company's figure excluding
  the costs of the Valspar acquisition (agreed 2016-03-19, completed 2017-06-01) is used, the GAAP range in the guide's note (the ACN FY15
  rule, as for the 2011 IRS settlement):
  - FY2016 guides: $12.50-12.70 excluding acquisition costs (Q1 2016; GAAP $11.17-11.50); $12.50-12.70 (Q2) and $12.25-12.35 (Q3)
    excluding the acquisition costs and the reduction in the income tax provision from the early adoption of ASU 2016-09, the only
    figures published without the costs. FY2016 enters the history at $12.45 on that basis (Q4 2016 release; GAAP $11.99, the FY2016 10-K,
    which publishes no adjusted figure; its $10,688K goodwill and trademark impairment stays in).
  - FY2017 guides: $13.60-13.80 on the same basis (Q4 2016; GAAP $13.00-13.20); $14.05-14.25 excluding the Valspar costs only, the tax
    benefit now included (Q1 2017; GAAP $13.65-13.85); then "Consolidated excluding Valspar-related costs", without the transaction and
    integration costs, the purchase accounting amortization (inventory step-up and intangibles) and the $.44 charge for the divested North
    American Industrial Wood Coatings business, with Valspar's operations and the new debt's interest: $14.80-15.20 (Q2 2017; GAAP
    $11.86-12.26, continuing operations $12.30-12.70) and $14.85-15.15 (Q3 2017; GAAP $11.20-11.50). Valspar is the business bought,
    not a charge: its operations stay in the guide, as Comex's losses did ("SHW 2012-2014").
  - The next quarter's EPS range is shown on the same basis, with its GAAP range in the note; it feeds no input.
- **FY2016 restated by a later print.** The Q1 2017 release changes the basis: its FY2017 guide includes the ASU 2016-09 benefit, and it
  republishes 2016 "excluding Valspar acquisition costs" only, at $12.85. Each year comes from the latest filing that reports it, so
  $12.85 replaces $12.45 from 2017-04-21. The fact sheet's `restates` field (the XOM and MSFT encoding for a Q4 print before its 10-K)
  now works on any print, until a 10-K vintage published after the print carries the year; the builder gains those lines (no earlier
  output changes: no 2008-2014 print carries the field). The FY2017 10-K, which would carry 2016, lies after the range.
- **Guides in words; BASE.** Net sales are guided in numbers only in the Q1 2015 release (Q2 2015 +6-8%) and the Q2 2015 release (Q3 2015
  +3-5%, FY2015 +3-5%); every other statement of 2015-2017 is words ("a high single digit percentage", "a low to mid single digit
  percentage"), and from Q2 2017 words for "core" sales plus a Valspar figure in dollars ("approximately $1.0 billion in the third
  quarter", "$2.4 billion" then "$2.5 billion" for 2017). Words are no field (the UNP 2016 rule); the dollar figure is shown and not added
  to anything (the Comex rule of the Q4 2013 guide). So BASE takes:
  - to 2015-07-16, the FY2015 range of the 8-K of 2014-12-12 (+7-11%), which the Q4 2014 and Q1 2015 releases restate only in words, and
    the Q2 2015 quarter range while its quarter is unreported; from 2015-07-17 the Q3 2015 and FY2015 ranges (+3-5%);
  - from the Q4 2015 print, with no numeric guide for FY2016 or FY2017, the latest quarter's growth less the currency effect the release
    states: +5.0% (Q4 2015), +7.9% (Q1 2016), +4.3% (Q2 2016), +4.8% (Q3 2016), +7.7% (Q4 2016);
  - from the Q1 2017 print, which states no currency effect on net sales, growth as reported: +7.3% (Q1 2017), +16.0% (Q2 2017, Valspar's
    June adding 11.8 points), +37.4% (Q3 2017, Valspar adding 32.8 points; core +4.6%). Acquisitions stay in, as they have since 2008
    (Q4 2010's +18.2% with 8.7 points of acquisitions), and so does the revenue reclassification of Q3 2016 (third-party service revenue
    grossed up, 2.2-2.3 points a quarter for a year, as published).
- **Signals.** Comparable-store sales as each release states them: "excluding the change in revenue classification" from Q3 2016, and "stores
  in U.S. and Canada" from Q2 2017. From Q2 2017 the Consumer Group is reported inside the new Consumer Brands Group (with Valspar's
  consumer paints); the signal takes the successor's growth as the release states it (+16.0%, +81.6%, Valspar adding 27.9 and 84.4
  points), as it took the Consumer Group's acquisitions before, and the engine's label stays "Consumer Group" (the release's own sentence
  is in the note). Margins come from each release's statement of income at GAAP, the year-ago quarter as that release shows it (Q2 and Q3
  2017 restate 2016's cost of goods sold by a few hundred thousand dollars): the Valspar inventory step-up and amortization are in them,
  as no release publishes a margin without them.
- **Segment bridge** (display only): the 10-K segments (Paint Stores, Global Finishes, Consumer, Latin America Coatings, Administrative)
  stay until the FY2017 10-K. The Americas, Consumer Brands and Performance Coatings Groups of Q2 2017 are new segments with Valspar's
  businesses, not renamed lines, so no rename is recorded; the release's names appear in the print notes from 2017-07-21 (their
  anachronism dates are that release's).
- **Release timing.** All twelve earnings 8-Ks were accepted before the open (07:08-09:03 ET), each on a Thursday or Tuesday, so each print
  dates its week the next trading day. The 8-K of 2016-03-21 announcing the Valspar agreement (press release of Sunday 2016-03-20) changes
  no guided number and adds nothing.
- **Dividends,** from the 10-K that states the rate: $.67 a quarter (FY2014 10-K, February 18, 2015), $.84 (FY2015 10-K, February 17,
  2016), $.85 (FY2016 10-K, February 15, 2017). The releases repeat the increases later.
- **Adds nothing:** the director, officer, bylaw and annual-meeting 8-Ks, the credit-facility, bridge-loan, term-loan, note and
  exchange-offer 8-Ks of 2015-2017 (the July 2015 and May 2017 note sales among them), the Valspar FTC second request (2016-05-11), the
  merger-agreement extension (2017-03-21), the Axalta divestiture agreement (2017-04-12), Valspar's financial statements and the pro forma
  information (2017-05-02), the completion 8-K (2017-06-01) and the S-4: none states a guided number.
- **Watch list.** ECOMMERCE is live from 2015-01-01 but scoped to physical retail; none of the FY2014-FY2016 10-Ks names e-commerce, online
  or internet competition. ENERGY_TRANSITION (from 2015-12-12) is scoped to oil, gas, coal and refining; from the FY2015 10-K
  Sherwin-Williams counts "oil production, refining, storage and transportation" among the cyclical segments it sells to, a customer
  market, and the words join the durability "why". The list stays empty; DURABLE, risk 2.

Controls: altering one value of each new print (with each Q4 print's full-year actuals and the Q1 2017 restatement), guide and vintage
changes no date before its publication and changes the first weekly date on or after it (31 of 31). A scan of all 522 SHW models for the
figures, notes, guides, titles and URLs of every print, guide and vintage finds none of 2015-2017 before its first publication (the scan's
four hits are "Latin America Coatings Group" in four 2012 models, a segment name public since the FY2008 10-K that the scan dates from the
FY2011 vintage's group list); no model carries a calendar year after its date outside an FY label. The firewall gains a planted print
that restates every year of the history. Rebuilding 2008-2014 changes nothing (366 dates byte-identical).

Seen in the build (method behaviour, not tuned):
- **RICH on 125 of 156 dates, FAIR on 22, CHEAP on 9.** 2015: RICH on 51, FAIR on 2015-09-25. 2016: RICH on 43, FAIR on 9 (2016-01-29 to
  2016-02-19, 2016-09-09, 2016-09-16, 2016-10-07, 2016-10-14, 2016-11-04). 2017: RICH on 31 to 2017-10-20, FAIR from 2017-07-21 to
  2017-09-29 (11 dates) and on 2017-12-22, CHEAP on the nine other dates from 2017-10-25. The legacy tier is AVOID on 117 dates,
  WATCHLIST on 26 and ACCUMULATE on 13. Robustness (variants with the same price state) is 5-8 of 8 on every date but three:
  2016-06-24 and 2016-10-26 (RICH, 3 of 8) and 2017-12-22 (FAIR, 4 of 8, the others CHEAP).
- **The multiple stays near the top of its own range.** The price ran $227-291 in 2015, $242-307 in 2016 and $279-413 in 2017 (as traded),
  21-31x, 20-24x and 22-28x the guided year: the 69th-100th, 49th-85th and 61st-99th percentile of its own ten-year range. The window kept
  rising with it: the median from 15.8x to 20.8x, the 90th percentile 24.2-25.3x. The EPP floor is 13x, then 14x from 2016-01-08, 15x
  from 2016-12-30 and 16x from 2017-01-06; the price stood 37-141% above it.
- **BEAR is 2008's -14.9%/yr** throughout, at the 10th-percentile P/E (12.7-14.1x): $81-153. XBULL is the 2011-2013 run (+32.4%/yr,
  +32.3% on the restated 2013) until BASE exceeds it. BULL is the decade CAGR (+11.4% to +13.1%/yr) or BASE where BASE is higher.
- **BASE follows the guides, then the acquisition.** +8.1% to +13.1%/yr in 2015, +8.6% to +12.2% in 2016-Q1 2017, then +19.7% from the
  Q2 2017 print and +41.1% from the Q3 2017 print, where Valspar's acquired sales (32.8 of the 37.4 points) enter the growth rate while
  the FY2017 anchor already holds seven months of Valspar; BULL and XBULL equal BASE from 2017-07-21 and 2017-10-25. The FAIR and CHEAP
  dates of the second half of 2017 come from this.
- **The proxy composite** reads 2.70-2.85 in 2015 (comps +2% to +8% at BASE or BULL, gross margin up 118-336bp at BULL or XBULL), 2.00-3.05 in
  2016 and 2.00-2.50 in 2017 (the Valspar inventory step-up puts the gross margin at -432bp and -770bp, BEAR, while the Consumer Brands
  Group's +81.6% is XBULL); the market composite 1.85-3.75; the adjusted gap -1.13 to +0.60. The conservative two-year case runs -42% to
  +52%.

How far each call moves the classes (the 156 dates recomputed with one encoding changed; no outcome consulted):
- BASE and the Consumer signal on core growth in Q2-Q3 2017 (the stated Valspar points out): 21 classes (every FAIR and CHEAP date from
  2017-07-21 to RICH), 21 tiers; BASE alone on core growth, the same 21 and 21;
- the Valspar items at GAAP (every 2016-2017 guide at its GAAP or continuing-operations range, FY2016 $11.99, no restatement): 26 classes
  (FAIR and CHEAP to RICH: five 2016 dates from 2016-09-09 to 2016-11-04 and the 21 of the second half of 2017), 33 tiers;
- the FY2017 anchor without Valspar from Q2 2017 ("Consolidated excluding Valspar", $14.05-14.25 and $14.10-14.30): 13 classes (six FAIR to
  RICH, seven CHEAP to FAIR), 4 tiers;
- the Consumer Group signal at BEAR on every date: 17 classes (toward RICH: 2016-11-04 and 16 dates of the second half of 2017); at XBULL:
  5 classes (RICH to FAIR in 2016), no tier either way;
- BASE without the revenue reclassification's points: 3 classes (FAIR to RICH: 2016-11-04, 2017-07-21, 2017-09-29), 2 tiers;
- the pre-tax margin thresholds with 2000 at GAAP: 2 classes (2016-10-26 RICH to FAIR, 2017-12-22 FAIR to CHEAP), no tier;
- FY2016 kept at $12.45 (no restatement); BASE on reported net sales growth; the FY2015 range of 2014-12-12 not carried past the Q4 2014
  release's words: no class and no tier, each.

Judgement calls that could carry hindsight (in addition to the 2008, 2009-2011 and 2012-2014 lists, which stand):
- the acquired sales of Valspar left in BASE and in the Consumer signal (the 2008 rule, not new), which alone makes the second half of
  2017 FAIR and CHEAP; on core growth every one of those 21 dates is RICH;
- the company's figures excluding the Valspar costs, including the purchase accounting amortization of intangibles, which recurs, rather
  than GAAP (26 classes move);
- 2016 restated to $12.85 by the Q1 2017 release (no class moves either way);
- Consumer Brands Group read as the Consumer Group's successor line, and the signal labels left unchanged.

### SHW 2018-2020: the Tax Act year, adjusted EPS, Valspar lapped, an inventory accounting change, a withdrawn sales range

```bash
python3 retro/build_shw.py --weekly 2018-01-01 2020-12-31                   # 157 dates, 2018-01-05 .. 2020-12-31
```

Every 8-K, 10-Q and 10-K of January 2018 to December 2020 was listed (46 filings: 34 8-Ks, nine 10-Qs, three 10-Ks); the Q4 2017
release of 2018-01-25 and the preliminary-results 8-K of 2019-01-15 are among them. The twelve earnings releases (Q4 2017 to Q3 2020),
that 8-K and the three 10-Ks were read for the facts, by Opus directly, with no delegated transcription; every other 8-K and the
10-Qs were checked for a guided number (none has one). The fact sheet's records (sources `SH69`-`SH84`) are generated by script from the
transcribed raw figures, as before; 269 more strings were checked with `verbatim.py` (1,300 in all), among them every statement-of-income
row behind a print, every Regulation G row behind an adjusted EPS figure, every guide and quoted note, and the first-year diluted share
counts of 2008-2010 in the FY2010-FY2012 10-Ks. Thresholds (rule T), signals and the engine are unchanged. Decided before any 2018-2020
date was built or scored:

- **Three 10-K vintages, each with a Q4 print before it.** The FY2017 10-K (accepted 2018-02-23 14:11 ET), FY2018 (2019-02-22 14:28 ET)
  and FY2019 (2020-02-21 15:03 ET), all during the session; the history moves to 2008-2017, 2009-2018 and 2010-2019, each year from the
  latest filing that reports it. First-year diluted shares (two-class method, as those 10-Ks report them): 2008's 118,177,979 from the
  FY2010 10-K, 2009's 114,457,488 from the FY2011 10-K, 2010's 108,785,517 from the FY2012 10-K. The FY2019 10-K, a full 10-K without
  Exhibit 13, states its financial statements in millions to one decimal; the vintage takes them so. Each vintage names the new segments
  (The Americas, Consumer Brands and Performance Coatings Groups) in its business line, bridge and "why" ("The Americas Group consisted of
  4,620 company-operated specialty paint stores").
- **EPS: the company's figure excluding acquisition costs and one-off items, as published (the 2015-2017 rule).** Every release publishes
  a Regulation G table:
  - FY2017 enters at $15.07 ("Consolidated excluding Valspar acquisition costs and one-time items": without the one-time benefit of
    $7.04 from the deferred income tax reductions of the Tax Cuts and Jobs Act and Valspar subsidiary mergers, the $.44 discontinued
    operations and $3.00 of acquisition costs and purchase accounting; GAAP $18.67, $19.11 from continuing operations). The release's
    "Adjusted" $14.27, which also takes out Valspar's operations, is not used (the Comex rule: the business bought stays in).
  - FY2018 guides: $18.75-19.35 (Q4 2017 release), $18.35-18.95 (Q1 2018, including a $.40 net reduction from an expanded customer
    agreement), then "adjusted" $19.05-19.35 and $19.05-19.20, without acquisition costs, environmental provisions and the California
    litigation; the preliminary 8-K of 2019-01-15 (07:16 ET, before the open) gives about $18.53, recorded as a guide like the 8-K of
    2014-12-12; FY2018 enters at the adjusted $18.53 (GAAP $11.67).
  - FY2019 guides: adjusted $20.40-21.40 and $20.90-21.30; FY2019 enters at $21.12 (GAAP $16.49). FY2020 guides: adjusted $22.70-23.50
    (without acquisition-related costs), then $19.00-21.00, $21.75-23.25 and $24.00-24.30 (without acquisition-related amortization).
  - The 10-K vintages take the same figures: the FY2017 and FY2018 10-Ks publish none, so the latest release that does supplies them
    (2016's $12.85 and 2017's $15.07 from the Q4 2017 release, 2017's $15.07 and 2018's $18.53 from the Q4 2018 release); the FY2019 10-K
    publishes 2018's $18.53 and 2019's $21.12 itself. GAAP figures are the five-year summaries' EPS from continuing operations.
  - The Q3 2020 release cites a "most recent" FY2020 guide of $20.96-21.46 that no SEC filing carries; it is in that guide's note and
    never a field (facts enter only from filings).
- **The inventory accounting change, as published.** A voluntary change in the fourth quarter of 2018 revised 2017's cost of goods sold
  by $58.9 million ($.47 a share): the Q4 2018 release shows its year-ago quarter revised (the MSFT recast rule), the FY2018 10-K revises
  2017 to $18.20 ($18.64 from continuing operations), and the company's $15.07 is unchanged (the charge joins acquisition costs).
- **The Tax Act year's tax rate** (display only, in the EPS check): the FY2017 10-K's 25.1% for continuing operations excluding the deferred
  income tax reductions (GAAP (18.7)%); the Q4 2017 print's figure the same, from the release's income taxes plus its $668.8 million.
- **Guides in words, numbers and a withdrawal; BASE.** Net sales are guided in numbers from the Q4 2018 release (Q1 2019 +2% to 6%, FY2019
  core +4% to 7%) to the Q4 2019 release (Q1 2020 +2% to 5%, FY2020 +2% to 4%), and again for Q4 2020 (+3% to 7%); the 8-K of 2019-01-15
  states Q4 2018 net sales up "approximately 2%", read as that quarter's guide while it is unreported. The other statements are words, with
  Valspar's sales in dollars through mid-2018 (the Comex rule: shown, added to nothing). So BASE takes:
  - to the Q3 2018 print, the latest quarter's growth as reported, no release stating a currency effect on net sales, acquisitions in
    (the 2008 rule, as in 2017): +37.4% (Q3 2017), +43.0% (Q4 2017, Valspar 36.1 points), +43.6% (Q1 2018, 38.6 points), +27.8% (Q2 2018,
    21.0 points, Valspar annualizing on June 1); BASE EPS growth +30% to +46%/yr;
  - from the Q3 2018 print, growth less the stated currency effect (+6.1%), then the numeric guides (+2% for Q4 2018 from 2019-01-18,
    the quarter and year ranges of 2019 and early 2020);
  - **the withdrawn range.** The Q1 2020 release (2020-04-29) revises FY2020 net sales to words ("flat to down a low single digit
    percentage", or a mid-to-high single digit decrease) and says so: "This is compared to our previous full year 2020 sales guidance of
    an increase of 2% to 4%". That is not a guide restated in words, which keeps the last range: it says the range no longer holds (the
    AAPL 2020-02-17 and LOW 2020 rule). The guide's new `withdrawn` field voids the range in every earlier guide for the year (a builder
    change; no earlier guide withdraws anything, so no earlier date changes); BASE takes Q1 2020's +4.0% less the currency drag, then
    Q2 2020's -4.1%, and the Q4 2020 range from the Q3 2020 print. The FY2020 EPS guide is replaced by a new range, not withdrawn.
- **Signals.** Comparable-store sales as each release states them ("stores in U.S. and Canada"); the Consumer Brands Group's growth as
  stated (+89.1% and +103.0% with Valspar, then organic; the Q4 2018 and Q4 2019 quarters from the segment paragraph's own sentence);
  margins at GAAP from each statement of income, the year-ago quarter as that release shows it. From the Q4 2019 release the statements are
  in millions to one decimal; the raw figures are entered in thousands with a note.
- **Store counts.** The Q4 2018 and Q4 2019 releases give net new stores (76, 62) but no year-end count; the print's count is the latest
  10-K's plus them (4,696 and 4,758, as the next 10-Ks confirm), with a note.
- **Release timing.** All twelve earnings 8-Ks were accepted before the open (07:11-07:55 ET), on a Tuesday, Wednesday or Thursday, so
  each dates its week the next trading day.
- **Dividends,** from the 10-K that states the rate: $.86 a quarter (FY2017 10-K, February 14, 2018), $1.13 (FY2018 10-K, February 13,
  2019), $1.34 (FY2019 10-K, February 19, 2020). The releases repeat them later.
- **Adds nothing:** the director, officer, bylaw and annual-meeting 8-Ks, the credit-facility, term-loan and note 8-Ks (the notes of
  August 2019 and March 2020 among them), the DC Solar 8-K of 2019-06-28 (a $77 million tax charge to come, no guided number; the Q2 2019
  release excludes it as a non-operating item), the CEO trading-plan 8-Ks (2019-11-15, 2020-08-03), and the 10-Qs.
- **COVID enters only through the prints and the withdrawal** (the LOW 2020 rule): the FY2019 10-K predates it, and no SHW filing names
  a disruption theme.
- **Watch list.** It stays empty through 2020. ECOMMERCE is scoped to physical retail and the FY2017-FY2019 10-Ks name no e-commerce or
  online competition; ENERGY_TRANSITION is scoped to oil, gas, coal and refining (oil production stays only among the cyclical segments
  Sherwin-Williams sells to); EV (from 2020-01-01) and CRYPTO (from 2020-10-21) are scoped to other industries. DURABLE, risk 2.

Controls: altering one value of each new print (with each Q4 print's full-year actuals), guide (EPS, and each next-quarter sales range),
the withdrawal and each vintage changes no date before its publication and changes the first weekly date on or after it (37 of 37). A
scan of all 679 SHW models for the figures, notes, guides, titles and URLs of every print, guide and vintage finds none before its first
publication other than segment names already public on the model's date (35 hits, "Consumer Brands Group" and "Latin America Coatings
Group", each on or after its anachronism date); no model carries a calendar year after its date outside an FY label. The first build of
this batch failed that last check: the Q1 2020 guide's words named the next year ("until the first quarter 2021") in 13 models of
2020; the words were cut to the first scenario and the second moved to the note without the year, before anything was committed. The
firewall gains a planted later withdrawal of every guided field. Rebuilding 2008-2017 changes nothing (522 dates byte-identical).

Seen in the build (method behaviour, not tuned):
- **CHEAP on 78 of 157 dates, RICH on 54, FAIR on 25.** 2018: CHEAP on 47 (from the Q4 2017 print, 2018-01-26), FAIR on 5 (the three
  dates before it, 2018-11-16 and 2018-11-30). 2019: CHEAP 19 (January, two dates of March, 2019-04-24 to 2019-07-19), FAIR 14
  (2019-02-01 and 2019-07-24 to 2019-10-18), RICH 19 (February-April between them, and from 2019-10-23). 2020: CHEAP 12 (2020-01-31 to
  2020-04-24 but 2020-02-14), FAIR 6, RICH 35 (from 2020-05-15 nearly throughout).
  The legacy tier is BUY on 84 dates, AVOID on 32, WATCHLIST on 26, ACCUMULATE on 15. Robustness is 5-8 of 8 except on ten dates
  (2018-01-05, 2019-02-01 at 1 of 8, 2019-02-08, 2019-03-01, 2019-03-15, 2019-03-29, 2019-10-23, 2020-01-03, 2020-01-10, 2020-05-15).
- **The multiple sat mid-band; the anchor rose.** The price ran $370-470 in 2018, $390-593 in 2019 and $413-736 in 2020 (as traded),
  19.4-28.9x, 20.0-28.1x and 17.9-31.5x the guided year: the 30th-100th, 30th-99th and 9th-100th percentile of its own ten-year range,
  whose median now held at 20.8-22.7x and 90th percentile at 25.3-26.1x. The anchor rose from $15.07 (FY2017) to the FY2018 guides
  ($18.35-19.35), $20.40-21.40 and $22.70-24.30. The EPP floor is 18x throughout; the price stood -1% to +75% above it.
- **BEAR leaves 2008.** The FY2017 10-K's window (2008-2017) puts BEAR at 2009's -5.5%/yr, the FY2018 10-K's at 2011's -1.7%/yr: the
  bear price rose from $153-266 in 2018 to $261-455 in 2019-2020. XBULL is the 2011-2013 run (+32.3%/yr) unless BASE is higher; BULL is the decade CAGR (+15.9% to
  +19.6%/yr, lifted by the adjusted 2016-2019 figures) or BASE.
- **BASE carried Valspar to October 2018,** at +30% to +46%/yr (above); the CHEAP of January-October 2018 rests on it, while the CHEAP
  of November 2018 to January 2019 rests on BASE +4.5% to +8.6% and a falling price ($370-410).
- **The proxy composite** reads 2.45-2.50 in 2018, 1.65-3.05 in 2019 and 2.65-3.15 in 2020; the market composite 1.42-3.66; the adjusted
  gap -1.21 to +1.58. The conservative two-year case runs -29% to +120%.

How far each call moves the classes (the 157 dates recomputed with one encoding changed; no outcome consulted):
- every EPS figure at GAAP (the 2018-2020 guides at their GAAP ranges, FY2016-FY2019 at GAAP from continuing operations): 72 classes,
  97 tiers, almost all toward RICH;
- BASE on core growth while Valspar is lapped (Q4 2017 core +6.9% and Q1 2018 +4.9% as stated, Q2 2018 less Valspar's 21.0 points):
  21 classes (CHEAP to FAIR or RICH, 2018-01-26 to 2018-10-05), 26 tiers;
- the Consumer Brands Group signal at XBULL on every date: 22 classes (toward CHEAP or FAIR, February-April and October 2019 to January
  2020); at BEAR: 14 (toward RICH), no tier either way;
- the pre-tax margin thresholds with 2000 at GAAP: 12 classes, no tier;
- BASE on reported net sales growth: 1 class (2020-06-26 FAIR to RICH), no tier;
- the FY2020 range kept after the Q1 2020 words, and the 8-K of 2019-01-15 not read as a guide: no class and no tier, each.

Judgement calls that could carry hindsight (in addition to the 2008-2017 lists, which stand):
- the company's adjusted EPS throughout, including the exclusion of acquisition-related amortization, which recurs (72 classes move at
  GAAP), and FY2017 at $15.07 rather than the "Adjusted" $14.27 that also takes out Valspar's operations;
- the acquired sales of Valspar left in BASE to the Q3 2018 print (the 2008 rule, not new; 21 classes move on core growth);
- the Q1 2020 words read as withdrawing the FY2020 sales range, and the 8-K of 2019-01-15 read as a guide (no class moves either way);
- store counts derived from net new stores for the Q4 2018 and Q4 2019 prints (display only).

### SHW 2021-2023: a three-for-one split, adjusted EPS, a preliminary 8-K, currency sentences, segments recast

```bash
python3 retro/build_shw.py --weekly 2021-01-01 2023-12-31                   # 156 dates, 2021-01-08 .. 2023-12-29
```

Every 8-K, 10-Q and 10-K of January 2021 to December 2023 was listed: 57 filings, of which 45 are 8-Ks, nine are 10-Qs and three are 10-Ks.
The facts come from these filings, read directly with no delegated transcription:
- the twelve earnings releases, Q4 2020 to Q3 2023;
- the split 8-K of 2021-02-03;
- the preliminary-results 8-K of 2022-01-14;
- the three 10-Ks.

Every other 8-K and every 10-Q was checked for a guided number, and none has one. From 2022 the company files its press-release
exhibits under its own file names, not `ex99`, and they were fetched by name.

The fact sheet's records are sources `SH85`-`SH101`, generated by script from the transcribed raw figures as before. `verbatim.py`
checked 269 more strings, 1,569 in all. They include every statement-of-income row behind a print, the Regulation G
rows behind the adjusted EPS figures, every guide and quoted note, and the split terms.

Thresholds (rule T), signals and the engine are unchanged. The builder changes in one place: the EPS comment now carries the split note
(display only).

The following was decided before any 2021-2023 date was built or scored.

#### The three-for-one split

- **The announcement.** The 8-K of 2021-02-03 was accepted at 16:16 ET, after the close, so it is published 2021-02-04. It announces a
  stock dividend to holders of record on March 23, 2021, distributed after the close of trading on March 31, 2021.
- **The fact sheet.** The split is the sheet's first `splits` record: effective 2021-04-01, the first split-adjusted trading day, ratio 3.
  The UNP builder's `on_basis` handles it.
- **Before 2021-04-01:** the models stay on the old basis. The price is as traded (Yahoo's split-adjusted close times three).
- **From 2021-04-01:** every per-share fact published before the split is divided by three: the EPS history, the guides and the
  dividend. Share counts are multiplied by three.
- **Years published before the split.** The FY2021 and FY2022 10-Ks state 2019-2021 after the split, but take the earlier years from
  filings made before it. The new `eps_published` and `shares_published` fields give each such year its own publication date.
  `on_basis` divides only those years, and the EPS comment says so: "per share ÷3 ... on 2012-2019 (published before it)".
- **The P/E percentiles run continuously across the split.** The median is 22.8x on both 2021-03-26 and 2021-04-01.
- **One display wart.** A pre-split guide's quoted note keeps its GAAP range as published, so the 2021-04-01 to 2021-04-23 models show
  a pre-split GAAP range ("GAAP $23.87 to $24.67") beside the post-split adjusted range. The note ends "$26.40-27.20 before the split".

#### The 10-K vintages

Three 10-K vintages, each with a Q4 print before it:

| 10-K | accepted (ET) | published | history window | first-year diluted shares |
|---|---|---|---|---|
| FY2020 | 2021-02-19 11:42 | 2021-02-19 | 2011-2020 | 2011's 105,671,973, from the FY2013 10-K |
| FY2021 | 2022-02-17 16:32 (after the close) | 2022-02-18 | 2012-2021 | 2012's 103,930,429, from the FY2014 10-K |
| FY2022 | 2023-02-22 15:39 | 2023-02-22 | 2013-2022 | 2013's 103,048,871, from the FY2015 10-K |

Each year comes from the latest filing that reports it. The FY2021 and FY2022 first-year counts carry their own publication dates, so
they are multiplied by three.

#### EPS: the company's adjusted figure (the 2018-2020 rule, unchanged)

The figure excludes acquisition-related amortization and one-off items, as each release publishes it.

| Fiscal year | Guides, in order (FY2021 from Q1 2021 on, after the split) | Enters at (GAAP) |
|---|---|---|
| FY2020 | (2018-2020 batch) | $24.58 ($22.08) |
| FY2021 | $26.40-27.20 (Q4 2020 release, before the split); $8.80-9.07 (excluding the $0.34 Wattyl divestiture loss); $9.15-9.45; $8.35-8.55; about $8.15 (8-K of 2022-01-14) | $8.15 ($6.98) |
| FY2022 | $9.25-9.65 (twice); $8.50-8.80 (twice) | $8.73 ($7.72) |
| FY2023 | $7.95-8.65 (twice; excluding $0.81 of amortization and $0.25-0.35 of restructuring); $9.30-9.70; $10.10-10.30 | — |

- **The preliminary 8-K.** The 8-K of 2022-01-14 (07:07 ET, before the open) is recorded as a guide, like the 8-Ks of 2014-12-12 and
  2019-01-15.
- **FY2022's exclusions.** FY2022 excludes amortization and restructuring charges, trademark impairments included.
- **The vintages publish the same figures:**
  - the FY2020 10-K: 2019's $21.12 and 2020's $24.58;
  - the FY2021 10-K: 2020's $8.19 and 2021's $8.15, after the split. It gives 2019 only at GAAP ($5.50), so 2019 stays the FY2020 10-K's
    $21.12, divided by three from the split;
  - the FY2022 10-K: 2022's $8.73.

#### Two guide figures no filing carries

- **Q2 2021.** The release is "Reaffirming" an adjusted range first given at the June 8, 2021 Financial Community Presentation.
- **Q3 2021.** The release "reaffirms" an adjusted range that no earlier SEC filing carries.

Each range enters only through the release that states it (the Q3 2020 rule: facts enter only from filings). The guide's note says so.

#### Guides in words; BASE

Net sales are guided only in words throughout ("Up mid-to-high single digit %", "Down mid-single digit % to flat"). The one exception is
the 8-K of 2022-01-14: "Fourth quarter 2021 consolidated net sales increased approximately 6.1%". It is read as Q4 2021's guide while
that quarter is unreported (the 2019-01-15 rule). Words are not figures (the UNP 2016 rule).

BASE takes the Q4 2020 range (+3% to 7%, from the Q3 2020 release) up to the Q4 2020 print. After that it takes the latest quarter's
growth, less a stated consolidated currency effect. Where no effect is stated, it takes growth as reported:

| Quarters | BASE takes |
|---|---|
| Q4 2020 to Q1 2022 | Growth as reported: +9.1% (the release states currency for the year only, "reduced consolidated net sales for the year by 1.1%"), +12.3%, +16.9%, +0.5%, +6.1% (the preliminary figure, then the print), +7.4% |
| Q2 2022 to Q1 2023 | Growth less the stated currency effect: +10.6% (+9.2% with 1.4 points of drag), +19.6% (2.1 points), +11.8% (2.0 points), +9.9% (1.0 point) |
| Q2 2023 to Q3 2023 | Growth as reported: +6.3%, +1.1% |

- **Q3 2021's raw materials.** The release says "Raw material availability issues negatively impacted quarter sales by an estimated
  high single digit percentage". This is noted and adds nothing.
- **Acquisitions stay in** (the 2008 rule). From Q3 2022 the releases state 1.4 to 1.8 points.
- **The resulting BASE EPS growth** runs from +2.1%/yr (Q3 2021) to +21.3%/yr (Q3 2022).

#### The Q1 2021 currency sentence

The Q1 2021 release has one currency sentence on net sales: "Currency translation rate changes increased consolidated net sales by
2.7%". It sits in the Consumer Brands Group's paragraph and is read as the group's figure; the next release's parallel sentence says
"the group's net sales". So Q1 2021 has no stated consolidated effect. The other reading moves one class (below).

#### Signals

- **Comparable-store sales,** as each release states them:
  - the sentence on "stores in U.S. and Canada open more than twelve calendar months", to Q3 2021;
  - from the Q4 2021 release, the segment table's "Same-store sales (1)" row;
  - from Q1 2023, the Paint Stores Group's row ("stores open more than twelve calendar months").
- **Full-year comps** come from the 10-K where the Q4 release states none: +6.0% for FY2021 and +11.7% for FY2022.
- **The Consumer Brands Group's growth** comes from its table row (Q4 2020 from its paragraph).
- **The 2023 recast.** From Q1 2023 the segments are recast: the Paint Stores Group, the Consumer Brands Group with Latin America, and
  the Performance Coatings Group. The models take the recast year-ago rows as that release shows them (the MSFT recast rule). No line
  is renamed, since the Consumer Brands Group keeps its name.
- **Margins** are at GAAP.

#### Other facts

- **Release timing.** All twelve earnings 8-Ks were accepted before the open (07:04-07:16 ET) on a Tuesday, Wednesday or Thursday. Each
  dates its week from the next trading day.
- **Dividends,** from each 10-K:

  | 10-K | Quarterly rate | Declared |
  |---|---|---|
  | FY2020 | $1.65 ($0.55 after the split) | February 17, 2021 |
  | FY2021 | $0.60 | February 16, 2022 |
  | FY2022 | $0.605 | February 15, 2023 |

- **Filings that add nothing:**
  - the director, officer, bylaw and annual-meeting 8-Ks;
  - the credit-facility and note 8-Ks, including the redemptions of 2021-09-15 and 2023-11-01 and the note offerings of 2021-11-10
    and 2022-08-10;
  - the 10-Qs.
- **The watch list stays empty through 2023.**
  - GENAI (live from 2022-11-30) is scoped to software, IT services, information and education.
  - ECOMMERCE is scoped to physical retail. The FY2020-FY2022 10-Ks use "online" only for COVID-era ordering and for employee
    training.
  - ENERGY_TRANSITION is scoped to oil, gas, coal and refining. Oil production appears only among the cyclical segments
    Sherwin-Williams sells to.
  - EV and CRYPTO are scoped to other industries.
  - The classification stays DURABLE, risk 2.

#### Checks

- **Controls: 35 of 35.** One value at a time was altered, and each time no date before its publication changed and the first weekly
  date on or after it did. The values: each new print's comps, with each Q4 print's full-year EPS; each guide's EPS; the preliminary Q4
  2021 sales figure; each vintage's tax rate; a pre-split EPS year in each post-split vintage; and the split ratio, which takes effect
  on its effective date.
- **Leak scan.** All 835 SHW models were scanned for every figure, note, guide, title and URL. Nothing appears before its first
  publication except:
  - segment names already public on the model's date (the same 35 hits as before);
  - two strings that an earlier record already carries word for word:
    - "no consolidated currency effect on net sales stated" (the 2021 records' note), which opens the currency notes of Q2 2017 on;
    - "Currency translation rate changes decreased consolidated net sales by 1.4%" (Q2 2022), which is Q1 2020's own sentence.

  No model carries a calendar year after its date outside an FY label.
- **Firewall.** Now that the fact sheet has a `splits` record, the firewall's existing split plant applies to SHW: a later split,
  announced after the cutoff, on the price data's split date.
- **Regression.** Rebuilding 2008-2020 changes nothing: all 677 dates are byte-identical.

Seen in the build (method behaviour, not tuned):
- **RICH on 83 of 156 dates, CHEAP on 38, FAIR on 35.**

  | Year | RICH | FAIR | CHEAP | When |
  |---|---|---|---|---|
  | 2021 | 38 | 12 | 2 | CHEAP on 2021-02-26 and 2021-03-05; FAIR mostly January to April; RICH from 2021-06-25 to 2022-09-09, 64 dates in a row |
  | 2022 | 36 | 2 | 14 | CHEAP 2022-09-16 to 2022-11-25 and from 2022-12-16 |
  | 2023 | 9 | 21 | 22 | RICH 2023-06-30 to 2023-07-21 and in December |

  - **Legacy tier:** BUY on 47 dates, AVOID on 44, ACCUMULATE on 37, WATCHLIST on 28.
  - **Robustness** is 5-8 of 8 except on 18 dates at 3-4 of 8. Most of those are FAIR dates between a CHEAP and a RICH run (January to
    March 2021, December 2022, and much of 2023).
- **The multiple went to the top of its range and came back.** The table gives prices split-adjusted.

  | Year | Price | P/E on the guided year | Percentile of its own 10-year range |
  |---|---|---|---|
  | 2021 | $225-352 | 25.2-41.7x | 80th-100th |
  | 2022 | $202-323 | 23.3-38.3x | 43rd-98th |
  | 2023 | $211-312 | 23.4-32.4x | 44th-92nd |

  - **The range itself moved up as 2021's highs entered it.** The ten-year median rose from 22.7x to 24.3x and the 90th percentile from
    26.1x to 30.9x. The maximum is 43.2x from 2022-01-14.
  - **The anchor:**
    - FY2021: $26.80 before the split, then $8.93, $9.30, $8.45 and $8.15;
    - FY2022: $9.45, then $8.65;
    - FY2023: $8.30, then $9.50 and $10.20.
  - **The EPP floor** is 18x to 2021-10-15 and 19x from 2021-10-22. The price stood 23% to 119% above it.
- **BEAR goes flat, then slips:**
  - -1.7%/yr (2011) on the first six dates;
  - flat from the FY2020 10-K, since the 2011-2020 window has no down year;
  - -0.5%/yr (2021's $8.15 against 2020's $8.19) from the Q4 2021 print.

  The bear price is $164-209 from 2022, at the 10th-percentile multiple of 19.5-20.7x.
- **BULL and XBULL.**
  - XBULL is the 2011-2013 run (+32.3%/yr) until the FY2021 10-K, then 2013-2015 (+24.0%/yr).
  - BULL is the decade CAGR (+15.0% to +21.9%/yr) or BASE, whichever is higher.
- **BASE reads price inflation as growth.** The CHEAP of 2022-09-16 to 2023-04-14 rests on BASE at +12.3% to +21.3%/yr, from sales
  that the Q3 2022 release attributes largely to "selling price increases". The RICH of mid-2021 to September 2022 rests on the
  FY2021-FY2022 guides at 25-42x.
- **Composites.**
  - The proxy composite reads 1.3-3.15 in 2021, 1.3-3.2 in 2022 and 2.7-3.4 in 2023.
  - The market composite reads 1.93-3.77, and the adjusted gap -2.77 to +1.45.
  - The conservative two-year case runs from -44% to +33%.

How far each call moves the classes. The 156 dates were recomputed with one encoding changed each time; no outcome was consulted.

| Encoding changed | Classes | Tiers | Direction |
|---|---|---|---|
| Every EPS figure at GAAP: the 2021-2023 guides at their GAAP ranges, FY2016-FY2022 at GAAP | 70 | 112 | Toward RICH in 2021 and 2023 (56 in all); toward FAIR in 2022 (14) |
| Consumer Brands Group signal at XBULL on every date | 16 | 0 | Toward CHEAP or FAIR |
| Consumer Brands Group signal at BEAR on every date | 16 | 0 | Toward FAIR or RICH |
| Pre-tax margin thresholds with 2000 at GAAP | 10 | 0 | |
| BASE on reported net sales growth | 4 | 3 | CHEAP to FAIR, 2022-09-16 to 2023-03-03 |
| The Q1 2021 currency sentence read as consolidated | 1 | 0 | 2021-04-28, FAIR to RICH |
| The 8-K of 2022-01-14 not read as a guide | 0 | 0 | |

Judgement calls that could carry hindsight (in addition to the 2008-2020 lists, which stand):
- **The company's adjusted EPS throughout.** It excludes acquisition-related amortization, which recurs, as well as the Wattyl
  divestiture loss and 2022's restructuring and trademark impairments. At GAAP, 70 classes move.
- **The Q1 2021 currency sentence read as the Consumer Brands Group's.** One class moves.
- **The 8-K of 2022-01-14 read as a guide.** No class moves.
- **Two guide ranges first given outside SEC filings.** They enter only with the releases that restate them.
- **Full-year comps for FY2021 and FY2022 from the 10-Ks.** Display only, in the franchise line.

### SHW 2024-2026: guides in words to the end, Suvinil in the sales, the Paint Stores Group's stores, a refreshed price cache

```bash
python3 retro/build_shw.py --weekly 2024-01-01 2026-11-06                   # 149 dates, 2024-01-05 .. 2026-11-06
```

Every 8-K, 10-Q and 10-K of January 2024 to November 2026 was listed: 43 filings, of which 31 are 8-Ks, nine are 10-Qs and three are
10-Ks. The facts come from the twelve earnings releases (Q4 2023 to Q3 2026, each Exhibit 99.1) and the three 10-Ks, read directly with
no delegated transcription. Every other 8-K and every 10-Q was checked for a guided number, and none has one.

The fact sheet's records are sources `SH102`-`SH116`. The transcription script now writes every typed figure back as the filing's own
row text (statement-of-income rows, segment rows, same-store rows, Regulation G rows, guide rows), so a typo fails the check.
`verbatim.py` checked 286 more strings, 1,855 in all.

Thresholds (rule T), signals and the engine are unchanged. The builder changes only in its docstring.

The following was decided on 2026-11-07, before any 2024-2026 date was built or scored.

#### The end of the range

- **The last date is 2026-11-06,** the last complete week: the series was built on Saturday 2026-11-07.
- **A refreshed price cache.** The price cache (`retro/.cache`, not committed) had been fetched at 16:24 ET on 2026-11-06, before Yahoo
  posted that day's close, so its last bar was 2026-11-05. It was refetched for SHW, the S&P 500 and SPY.
- **No earlier model changes.** Rebuilding 2008-2023 from the new cache changes no model.
- **The newest dates have no two-year outcome yet.**

#### The 10-K vintages

Three 10-K vintages, each with a Q4 print before it:

| 10-K | accepted (ET) | published | history window | first-year diluted shares |
|---|---|---|---|---|
| FY2023 | 2024-02-20 15:57 | 2024-02-20 | 2014-2023 | 2014's 98,740,521, from the FY2016 10-K |
| FY2024 | 2025-02-20 17:24 (after the close) | 2025-02-21 | 2015-2024 | 2015's 94,543,543, from the FY2017 10-K |
| FY2025 | 2026-02-19 14:54 | 2026-02-19 | 2016-2025 | 2016's 94,488,086, from the FY2018 10-K |

- **First-year shares.** Each is the latest 10-K that reports the year (treasury stock method). Each was published before the 2021 split,
  so `shares_published` multiplies it by three.
- **Pre-split years.** The years the vintages take from filings published before the split keep their `eps_published` dates, as in
  2021-2023.
- **The new segment basis.** All three vintages name the Paint Stores Group (from the 2023 recast) in their business line and "why": "The
  Paint Stores Group consisted of 4,694 company-operated specialty paint stores", then 4,773 and 4,853. That count is about 240 lower than
  The Americas Group's 4,931 at the end of 2022, because the Latin American stores moved to the Consumer Brands Group. The franchise line
  shows the count; no input reads it.

#### EPS: the company's adjusted figure (the 2018-2020 rule, unchanged)

| Fiscal year | Excludes | Guides, in order | Enters at (GAAP) |
|---|---|---|---|
| FY2023 | the restructuring-plan items, trademark impairment, the Argentine peso devaluation ($0.16) and acquisition-related amortization | (2021-2023 batch) | $10.35 ($9.25) |
| FY2024 | acquisition-related amortization | $10.85-11.35 (twice), $11.10-11.40 (twice) | $11.33 ($10.55) |
| FY2025 | amortization, severance and other restructuring ($0.34) and trademark impairment ($0.05) | $11.65-12.05 (twice), $11.20-11.50, $11.25-11.45 | $11.43 ($10.26) |
| FY2026 | amortization and restructuring | $11.50-11.90 (twice), $11.80-12.20, $11.85-12.15 | — |

- **The 10-Ks publish the same adjusted figures** for both years they show: 2022-2023, 2023-2024 and 2024-2025.
- **No preliminary-results 8-K** falls in the range.
- **Guide changes are new ranges, not withdrawals.** The Q2 2025 release's "Adjusting" guide replaces the range rather than voiding it.

#### Guides in words; BASE

Net sales are guided only in words throughout, both for the next quarter and the year ("Up or down low-single digit %", "Up mid to
high-single digit %"). Words are not figures (the UNP 2016 rule), so BASE takes each latest quarter's growth less a stated consolidated
currency effect, or as reported where none is stated.

| Quarter | Growth | Stated consolidated currency effect | BASE growth input |
|---|---|---|---|
| Q4 2023 | +0.4% | none | +0.4% |
| Q1 2024 | -1.4% | none | -1.4% |
| Q2 2024 | +0.5% | none | +0.5% |
| Q3 2024 | +0.7% | 1.0 point unfavorable | +1.7% |
| Q4 2024 | +0.9% | 1.3 points unfavorable | +2.2% |
| Q1 2025 | -1.1% | about 1 point unfavorable ("an approximate 1% impact") | -0.1% |
| Q2 2025 | +0.7% | none | +0.7% |
| Q3 2025 | +3.2% | none | +3.2% |
| Q4 2025 | +5.6% | none | +5.6% |
| Q1 2026 | +6.8% | 1.7 points favorable | +5.1% |
| Q2 2026 | +7.5% | none | +7.5% |
| Q3 2026 | +7.9% | none | +7.9% |

- **Segment-only currency is not used.** Where only the segments state currency (CBG, PCG), BASE does not net it out; the note says so.
- **The resulting BASE EPS growth** runs from +0.1%/yr (Q1 2024) to +9.3%/yr (Q3 2026).

#### Suvinil in the sales, as published

- **The deal.** The 8-K of 2025-02-18 announced the purchase of BASF's Brazilian architectural paints business (Suvinil). The 8-K of
  2025-10-01 reported its close on October 1, 2025.
- **Neither adds a guided number.** The Q3 2025 guide notes that it "includes the Suvinil acquisition".
- **Acquisitions stay in (the 2008 rule).**
  - The Q4 2025 release states Suvinil "contributed $164.5 million, or 3.1% of the change from the fourth quarter of 2024". BASE takes
    the +5.6% with it.
  - The Q1-Q3 2026 releases say "inclusive of the October 2025 acquisition of Suvinil" without a figure.
  - The Q3 2026 release adds "selling price increases, which impacted Net sales by a mid-single digit percentage". This is noted and
    adds nothing.

#### Signals

- **Comparable-store sales** are the Paint Stores Group's same-store row, labelled "Same-store sales (1)" or "Same-store sales change
  (1)" as each release prints it. The footnote's own capitalization varies between releases ("net sales" or "Net sales") and is quoted
  as printed.
- **Full-year comps** come from each Q4 release's own sentence: +6.8% (2023), +1.7% (2024) and +1.7% (2025).
- **The Consumer Brands Group's growth** comes from its table row: -10.7% to -2.6% through Q3 2025, then +19.2% to +24.5% with Suvinil.
- **Margins** are at GAAP.

#### Other facts

- **Release timing.** All twelve earnings 8-Ks were accepted before the open (07:03-07:12 ET) on a Tuesday or Thursday. Each dates its
  week from the next trading day.
- **Dividends,** from each 10-K:

  | 10-K | Quarterly rate | Declared |
  |---|---|---|
  | FY2023 | $0.715 | February 14, 2024 |
  | FY2024 | $0.79 | February 19, 2025 |
  | FY2025 | $0.80 | January 26, 2026 |

- **Filings that add nothing:**
  - the officer, director, bylaw and annual-meeting 8-Ks, among them the Executive Chairman's retirement (2024-11-14) and the CFO
    succession (2025-11-03);
  - the credit-facility, term-loan and note 8-Ks;
  - the Suvinil 8-Ks beyond the prints;
  - the 10-Qs.
- **The watch list stays empty through 2026.**
  - GENAI is scoped to software, IT services, information and education. The FY2024 and FY2025 10-Ks name artificial intelligence
    only as a risk to the protection of intellectual property ("advances in artificial intelligence technology and increasingly
    widespread use of generative artificial intelligence tools") and to cybersecurity ("advances in artificial intelligence (AI)
    capabilities"). That is a risk to the company's own systems, not substitution of its products.
  - ECOMMERCE is scoped to physical retail. The FY2023-FY2025 10-Ks use "online" only for employee training.
  - ENERGY_TRANSITION, EV and CRYPTO are scoped to other industries.
  - The classification stays DURABLE, risk 2.

#### Checks

- **Controls: 33 of 33.** One value at a time was altered, and each time no date before its publication changed and the first weekly
  date on or after it did. The values: each new print's comps, with each Q4 print's full-year EPS; each guide's EPS; each vintage's tax
  rate; and a pre-split EPS year in each vintage.
- **Leak scan.** All 984 SHW models were scanned for every figure, note, guide, title and URL. Nothing appears before its first
  publication except:
  - the earlier batches' segment-name hits;
  - generic phrases already inside earlier notes: the two currency phrases of 2021-2023, and now "no consolidated acquisition effect
    stated" (Q1 2025's note, already the opening of Q2 2022's).

  No model carries a calendar year after its date outside an FY label.
- **Regression.** The 833 dates of 2008-2023 that a single run produces rebuild byte-identical. The other two, 2008-12-31 and
  2014-12-31, are the ends of their batches.

Seen in the build (method behaviour, not tuned):
- **RICH on 121 of 149 dates, CHEAP on 21, FAIR on 7.**

  | Year | RICH | CHEAP | FAIR | When |
  |---|---|---|---|---|
  | 2024 | 51 | — | 1 | FAIR on 2024-06-07 only |
  | 2025 | 52 | — | — | every date |
  | 2026 | 18 | 21 | 6 | from 2026-03-13 the class turns with the price: CHEAP on 2026-03-13 to 2026-04-02, 2026-04-29 to 2026-06-18, 2026-07-24, 2026-09-04 to 2026-10-16 and 2026-10-28; RICH on 2026-11-06 |

  - **Legacy tier:** WATCHLIST on 49 dates, ACCUMULATE on 41, AVOID on 34 and BUY on 25.
  - **Robustness** is 5-8 of 8 except on nine dates at 3-4 of 8, most at the edges of a RICH run.
- **The multiple stayed high in a band that kept rising.**

  | Year | Price | P/E on the guided year | Percentile of its own 10-year range |
  |---|---|---|---|
  | 2024 | $292-397 | 26.3-35.3x | 67th-95th |
  | 2025 | $321-373 | 28.0-32.9x | 67th-90th |
  | 2026 | $300-370 | 25.6-31.5x | 46th-86th |

  - **The band.** Its median rose from 23.9x to 26.7x and its 90th percentile sat at 30.4-33.0x. 2021's 43.2x stays the maximum.
  - **The anchor:**
    - FY2024: $11.10, then $11.25;
    - FY2025: $11.85, then $11.35 twice;
    - FY2026: $11.70, then $12.00.
  - **The EPP floor** is 19x, and 20x from 2025-10-03. The price stood 28% to 86% above it.
- **BEAR is 2021's -0.5%/yr throughout.** The bear price is $209-248, at the 10th-percentile multiple of 20.7-20.9x.
- **BULL and XBULL.** BULL falls with the decade CAGR, from +15.3% to +11.5%/yr, as the strong 2013-2016 years leave the window. XBULL
  goes from +24.0% to +21.0% and then +20.1%/yr.
- **BASE ran low, then rose with Suvinil.**
  - **To Q3 2025** it took growth of -1.4% to +3.2% (BASE EPS +0.1% to +4.4%/yr) against a price at 26-35x: RICH throughout.
  - **From Q4 2025** it took +5.1% to +7.9% (BASE EPS +6.5% to +9.3%/yr), Suvinil in it.
  - **The CHEAP of 2026** entered at $300-335, 25.6-27.9x, the 46th-62nd percentile, near the band's median.
  - **The RICH dates of 2026** entered at $328-370, 28.2-31.5x.
- **Composites.**
  - The proxy composite reads 2.05-2.80 and the market composite 2.48-3.77.
  - The adjusted gap runs from -1.74 to +0.41.
  - The conservative two-year case runs from -29% to +14%.

How far each call moves the classes. The 149 dates were recomputed with one encoding changed each time; no outcome was consulted.

| Encoding changed | Classes | Tiers | Direction |
|---|---|---|---|
| Every EPS figure at GAAP: the guides in force at their GAAP ranges, FY2016-FY2025 at GAAP | 37 | 115 | RICH to FAIR on 13 dates of January-July 2024; CHEAP to FAIR on 21 dates of 2026; FAIR to RICH on 3 dates of 2026 |
| Consumer Brands Group signal at BEAR on every date | 11 | 0 | All in 2026, toward RICH or FAIR |
| Consumer Brands Group signal at XBULL on every date | 9 | 0 | RICH to FAIR: 8 dates of 2024 and 2026-07-10 |
| Pre-tax margin thresholds with 2000 at GAAP | 0 | 0 | |
| BASE on reported net sales growth (no currency adjustment) | 0 | 0 | |
| BASE on Q4 2025 growth less Suvinil's stated 3.1 points | 0 | 0 | |

Judgement calls that could carry hindsight (in addition to the 2008-2023 lists, which stand):
- **The company's adjusted EPS throughout.** It excludes recurring amortization, as well as 2023's Argentine peso devaluation and
  2025's restructuring and trademark impairment. At GAAP, 37 classes move.
- **Approximate currency figures read as figures.** "approximately 1.0%" (Q3 2024) and "an approximate 1% impact" (Q1 2025) are taken as
  -1.0 points. No class moves either way.
- **Suvinil's acquired sales left in BASE** (the 2008 rule, not new). No class moves without its one stated figure.
- **The Paint Stores Group's store count replacing The Americas Group's.** Display only.
- **The refreshed price cache.** It changes no earlier model, and the new dates read the close of 2026-11-06.

## WMT (Wal-Mart Stores): the eleventh ticker, in staging

The WMT series is built apart from ACN, UNP, LOW, AAPL, NKE, AVGO, PEP, MSFT, XOM and SHW and shares nothing with them but the
machinery: its own fact sheet (`retro/facts/WMT.json`), builder (`retro/build_wmt.py`, the SHW builder with LOW's fiscal calendar and
guide fields) and engine (`retro/templates/wmt_engine.py.tmpl`, the SHW engine with LOW's retail signal layout). The method is still r2.
No fact, parameter, outcome or finding of another ticker enters a WMT model, and neither do the live `wmt_signal_model.py` files on
other branches or any profile of Walmart in `data/business_profiles.json` (2026 judgements, not read for this series). Outputs go to
`staging/retrospective/WMT/`, beside the others, with the same `index.json` and their own `SERIES.md`.

```bash
python3 retro/build_wmt.py --weekly 2008-01-01 2008-12-31                   # 53 dates, 2008-01-04 .. 2008-12-31
for d in staging/retrospective/WMT/2008-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series WMT
python3 retro/tools/firewall.py 2008-07-01 WMT
python3 retro/tools/firewall.py 2009-01-01 WMT
for c in 2008-02-01 2008-02-19 2008-04-01 2008-05-13 2008-08-14 2008-11-13; do python3 retro/tools/firewall.py $c WMT; done
```

Read for the history and the decade's signal values: the eleven-year financial summaries of the FY2007 and FY2008 10-Ks and the
statements of income of the FY1999 to FY2007 10-Ks (the FY2001 10-K/A, which carries the full financial statements, in place of the
FY2001 10-K; the FY2004 10-K/A carries none). Read for the prints and guides: every 8-K and 10-Q of September 2006 to December 2008
(26 8-Ks and 7 10-Qs) and the two 10-Ks. All by Opus directly, with no delegated transcription. The fact sheet is generated by a script
from the transcribed raw figures, so every growth rate, margin and rule-T value is computed, not typed. 306 strings were checked with
`verbatim.py` against their own filings: every statement row behind a print, every comparable-sales row, guide and quoted sentence,
every summary row behind the history and rule T. Each source's date comes from EDGAR's acceptance time (converted from UTC; before 2003
EDGAR gives the filing date only). Decided on 2026-11-07, before any WMT outcome was computed (one display label of the revenue bridge
was reworded after the first build; no input changed):

- **Fiscal calendar.** Walmart's fiscal year N ends on January 31 of calendar year N (fiscal 2008 ended 2008-01-31). The seven dates
  from 2008-01-04 to 2008-02-15 have FY2008 as the current year; the days from 2008-02-01 belong to fiscal 2009 but keep FY08's EPS
  (the ACN rollover rule) until the Q4 FY08 print adds FY08 on 2008-02-19.
- **Prices on the as-of share basis** (the UNP rule). Walmart split three-for-one on 2024-02-26, after every 2008 date, so the builder
  multiplies Yahoo's split-adjusted series by three: $45.72 as traded on 2008-01-04. The two-for-one split of 1999 precedes every
  per-share fact in the fact sheet (the FY1999 10-K is already on the post-split basis), so nothing is restated.
- **Release timing.** The earnings 8-Ks of Q4 FY07 to Q3 FY09 were accepted before the open on the release day (06:08-06:23 ET; a
  pre-recorded call followed), each on a Tuesday or Thursday, so a print dates its week the next trading day: 2008-02-20, 2008-05-14,
  2008-08-15 and 2008-11-14. The FY2007 10-K, accepted 2007-03-27 16:40 ET, is dated 2007-03-28; the FY2008 10-K, accepted 2008-03-31
  16:12 ET, is dated 2008-04-01.
- **History: the latest 10-K's Eleven-Year Financial Summary.** It is the latest filing that reports every year, restated for the
  dispositions of McLane (fiscal 2004) and of the South Korean and German operations (fiscal 2007): net sales and diluted income per
  share from continuing operations, fiscal 1998-2007 in the FY2007 vintage and 1999-2008 in the FY2008 vintage. Diluted shares of the
  first year come from the statements of income of the latest 10-K that reports them (fiscal 1998: 4,533 million, FY2000 10-K; fiscal
  1999: 4,485 million, FY2001 10-K/A), of the last year from its own 10-K. The Q4 FY08 release extends the history with FY08 ($3.16
  from continuing operations) from 2008-02-19.
- **EPS** is diluted income per share from continuing operations, fiscal 2000 before the cumulative effect of the Sam's Club membership
  accounting change ($198 million). Walmart publishes no figure excluding a one-off for any year, and no year's one-offs come near half
  its income, so **no year is excluded**. Q4 FY07's "$0.02 per share net benefit" from tax matters and Q4 FY08's "net charge of
  approximately $0.02 per share for certain items" stay in (no figure excluding them).
- **Guides: EPS in numbers, no net sales or margin guide.** Each release guides diluted EPS from continuing operations for the next
  quarter, and every release but the Q1 ones the fiscal year; most guide U.S. comparable store sales for the next quarter. Method r2
  maps them as for LOW:
  - current-FY EPS: the midpoint of the latest fiscal-year range: FY08 $3.15 ($3.13-3.17, Q3 FY08 release; earlier $3.15-3.23 from
    2007-02-20 and $3.05-3.13 from 2007-08-14) to 2008-02-15; FY09 $3.365 ($3.30-3.43, Q4 FY08 release; the Q1 FY09 release gives no
    full-year range, so it stands), $3.465 from 2008-08-15 ($3.43-3.50) and $3.44 from 2008-11-14 ($3.42-3.46);
  - BASE growth and the growth factor: no release guides net sales, so the latest quarter's net sales growth as reported (the LOW and SHW
    rule; no release of the period states a currency effect on net sales, which the 10-Qs and 10-K state weeks later): +8.8% (Q3 FY08),
    +8.3% (Q4 FY08), +10.2% (Q1 FY09), +10.4% (Q2 FY09), +7.5% (Q3 FY09). Currency and International acquisitions stay in;
  - no margin guide, so no margin step: the margin signal takes the latest quarter's operating-margin change.
  - The next quarter's EPS and comparable-sales ranges are shown in the guide line and feed no input.
- **Dividends,** from the 10-K that states the rate: $0.88 a year from the FY2007 10-K (increased March 8, 2007), $0.95 from the FY2008
  10-K (increased March 6, 2008, by a press release not filed with the SEC, so the model lags it by 26 days; the LOW rule).
- **Signals.** LOW's six, with ACN's weights: U.S. comparable store sales (0.20; the release's Total U.S. figure with fuel, the measure
  the 10-Ks report), gross margin change (0.20), net sales growth (0.15), inventory growth less net sales growth (0.15, lower is better),
  the operating-margin change (0.15) and the theme slot at 2/4. The releases carry full statements of income and balance sheets, so
  every value is derived from each release's raw figures (net sales, membership and other income, cost of sales, operating, selling,
  general and administrative expenses, operating income, inventories; the builder re-derives and checks them), each against the
  year-ago quarter in the same release. The Q2 and Q3 FY09 releases restate the year-ago quarter for a discontinued operation; the
  restated figures are used, as published.
- **Thresholds by rule T** over fiscal 1998-2007, the decade of the FY2007 10-K, the vintage public on 2008-01-04. Each change comes from
  the latest 10-K published by then that reports both years. For net sales, cost of sales, comparable store sales and inventories that is
  the FY2007 10-K's summary (one table, one basis; comparable store sales in whole percents as the table gives them, with the fiscal 2007
  change of definition left in). The summary has no operating income, so each operating-margin change comes from the statements of
  income of the latest 10-K that reports both years (fiscal 1998 from the FY1999 10-K ... fiscal 2006 and 2007 from the FY2007 10-K).
  Operating income is revenues less cost of sales and operating, selling, general and administrative expenses: the statements show it as
  a line from the FY2003 10-K, and before that it is derived the same way. Seams stay in, as published: the 1999-2000 Asda acquisition,
  the 2005-2006 Seiyu consolidation, the FY2003 10-K's move of interest income out of other income. The values and the raw figures are in
  the fact sheet (`rule_t`); the builder re-derives the values from the raw figures and refuses to build if the engine's thresholds
  differ.

  | Signal | Fiscal 1998-2007 | BEAR / BASE / BULL / XBULL |
  |---|---|---|
  | U.S. comparable store sales | 6, 9, 8, 5, 6, 5, 4, 3, 3, 2 % | -1 / 2 / 5 / 9 % |
  | gross margin change | 47.9, 16.3, 60.4, 18.4, -18.7, 34.0, 10.6, 47.3, 10.8, 35.5 bp | -60 / -20 / 30 / 60 bp |
  | net sales growth | 12.42, 15.32, 18.72, 16.1, 13.0, 12.58, 11.62, 11.35, 9.75, 11.67 % | 7 / 10 / 13 / 19 % |
  | inventory less sales | -9.5, -15.0, -0.7, -6.9, -7.8, -2.0, -2.6, 0.7, -1.3, -6.1 pp | 6 / 1 / -4 / -15 pp |
  | operating margin change | 5.6, 38.7, 22.4, -11.8, -43.1, 11.4, 7.2, 13.1, -8.9, -11.6 bp | -90 / -40 / 10 / 40 bp |

- **Durability: DURABLE, risk 2** (the LOW precedent). The "why" quotes the 10-K: Walmart "operates retail stores in various formats
  around the world and is committed to saving people money so they can live better", at "every day low prices", "The retail business is
  highly competitive", and "General economic conditions, globally or in one or more of the markets we serve, may adversely affect our
  financial performance". No disruption theme in `taxonomy_eras.json` is live for a discount retailer in 2008 (ECOMMERCE, scoped to
  physical retail, from 2015-01-01; OFFSHORE to IT services), so the watch list is empty and the builder refuses events until a theme
  encoding is decided. The FY2007 and FY2008 10-Ks name "internet-based retailers and catalog businesses" among the competitors of every
  segment in their risk factors; ECOMMERCE is not live, so those words stay in the "why" (the PEP obesity rule). Whether this earlier
  filing should move ECOMMERCE's live date is left to the owner (the MSFT and XOM precedent).
- **Segment bridge and EPS check** (display only): the 10-K's segments by net sales (Wal-Mart Stores, International, Sam's Club), the
  total from the BASE growth applied to the last year. A renamed reporting line takes its new name from the first print that uses it (the
  ACN rule): Walmart U.S. from the Q2 FY09 release (2008-08-14). The EPS check runs on the last full year's operating margin less net
  interest (minority interest left out).
- **Adds nothing:** the January sales 8-K of 2008-02-08 (it estimates February comparable sales and expects Q4 FY08 EPS "within our
  previously stated guidance of $0.99 to $1.03", a quarter range already published); the 8-K of 2007-02-02 (Walmart stops its Saturday
  sales estimates); the litigation statement of 2007-02-08; the debt-offering 8-Ks (2006-12-18, 2006-12-20, 2007-04-05, 2007-08-23,
  2008-01-29, 2008-04-14); the bylaw, officer and director 8-Ks (2006-09-25, 2006-11-20, 2007-01-10, 2007-04-03, 2008-01-18, 2008-01-25,
  2008-11-21); the settlement 8-K of 2008-08-21; and the 10-Qs (no guidance; the releases come first and carry every print value).
  Walmart's other monthly sales releases were not filed with the SEC and are not used.
- **Anachronism list:** Walmart names first seen in its filings after the start of 2008 (Walmart U.S. from 2008-08-14, Walmart
  International, Jet.com, Walmart Inc., Flipkart) join `taxonomy_eras.json`, each dated from the first Walmart filing that uses it
  (EDGAR full-text search). No model of any other ticker contains them, so no output changes. WMT's source ids are `WM1`-`WM18` (`WM0`
  the prices).

Controls: altering one value of each print, guide and vintage changes no date before its publication and changes the first weekly date
on or after it whenever the value is in scope (26 controls; the eight that change nothing are values that are never the latest on a 2008
date: the comparable sales of Q4 FY07 and Q1 FY08, the capital-return text of Q4 FY07 to Q2 FY08, and three guides superseded before 2008: the FY08
ranges of 2007-02-20 and 2007-08-14 and the Q2 FY08 range). A scan of the 53 models for the figures, notes, guide ranges and texts of every later print, guide and vintage finds
none before its first publication (0 of 747). Rebuilding the 2008 dates of ACN, UNP, LOW, AAPL, NKE, PEP, MSFT, XOM and SHW and the 2009
dates of AVGO changes nothing.

Seen in the build (method behaviour, not tuned):
- **CHEAP on all 53 dates.** The legacy tier is BUY on all 53, and robustness is 8 of 8 on every date.
- **The decade's multiple carries the call.** The P/E window runs from 1998 and holds the late-1990s multiples: the calendar-year P/E
  lows fall from 32.1x (1999) to 13.4x (2007), so their median, the EPP floor, is 21-22x. On guided EPS the stock traded at 14.5-18.0x
  in 2008 (the 3rd-33rd percentile of the window), 18-33% below the floor on every date.
- **BEAR is flat EPS** (no down year in fiscal 1998-2008) at the 10th-percentile P/E (15.3-15.5x): $49-53, about the price, so Ratio B
  runs from -0.03 to 0.10 (negative when the price is under the BEAR price). XBULL is the fiscal 1998-2000 run (+28.2%/yr), then the
  1999-2001 run (+23.8%) from the FY2008 vintage; BULL is the decade CAGR (+16.1%, +15.3%, then +14.4%).
- **BASE is the latest quarter plus about 1% of buyback:** +9.7%/yr to 2008-02-15, +9.4% from the Q4 FY08 print, +11.3% from Q1 FY09,
  +11.5% from Q2 FY09 and +8.6% from Q3 FY09 (diluted shares fell 0.9%/yr over fiscal 1998-2007 and 1.1% over 1998-2008 and 1999-2008).
- **The proxy composite** is 1.95 on the Q3 FY08 print (comparable sales +1.5% and net sales +8.8% at BEAR, inventory and the operating
  margin at BULL), 2.05 on Q4 FY08, 2.15 on Q1 FY09, 2.55 on Q2 FY09 (comparable sales +5.0% and gross margin +31.5bp at BULL) and 2.20
  on Q3 FY09. The market composite stays at 1.00-1.43, so the adjusted gap runs from +1.06 to +1.97.

How far each call moves the classes (the 53 dates re-run with one encoding changed; no outcome consulted): none moves a class or a
tier. With every signal at its BEAR value on every date the adjusted gap falls to -0.06 to +0.42, still above CHEAP's -0.45 line while
the price sits below the EPP floor; the comparable-sales signal at XBULL, forward sales growth 3 points lower (currency out) or higher,
and an EPP floor at the 10th-percentile P/E move nothing either. The signals, the BASE rule and the thresholds cannot reach the class;
the decade of multiples does.

Judgement calls that could carry hindsight:
- the signals, chosen by a builder who knows that Walmart's comparable sales rose through the 2008 recession (the LOW layout, unchanged,
  so no WMT-specific choice; rule T then sets the thresholds mechanically, and no class depends on them);
- the latest 10-K's eleven-year summary as the history: restated continuing-operations EPS is lower than first reported for the oldest
  years (fiscal 1999: $0.94 against the $0.99 first reported), which lifts their P/E and the EPP floor (the rule, each year from the
  latest filing that reports it, applied to Walmart's restated table);
- operating income derived for the statements before the FY2003 10-K, and comparable store sales in the table's whole percents;
- BASE on reported net sales growth, currency and acquisitions included (no class moves 3 points either way);
- filed documents only: Walmart's monthly sales releases, which sometimes commented on the quarter's EPS, were not filed (except
  January 2008's) and are not used, so a guide change made only in one of them is missing;
- DURABLE rather than CYCLICAL (the class label only).

### WMT 2009-2011: a re-presented FY2008, five-year summaries, the company's EPS excluding one-offs, constant currency, a sales guide

```bash
python3 retro/build_wmt.py --weekly 2009-01-05 2011-12-31                   # 156 dates, 2009-01-09 .. 2011-12-30
for c in 2009-01-13 2009-02-17 2009-04-01 2009-07-01 2010-01-01 2010-02-18 2010-03-31 2010-07-01 2010-11-16 2011-01-01 2011-02-22 \
         2011-03-31 2011-07-01 2011-11-15 2012-01-01; do python3 retro/tools/firewall.py $c WMT; done
```

Every 8-K, 10-Q and 10-K of January to December 2009-2011 was read (48 filings: 36 8-Ks, 9 10-Qs, 3 10-Ks), by Opus directly, with no
delegated transcription. The 2009-2011 records are generated by script from the transcribed raw figures, as in 2008; 425 more strings
were checked with `verbatim.py` (731 in all). Thresholds (rule T), signals and the engine are unchanged. Decided before any 2009-2011 date
was scored (one label of the revenue bridge was reworded after the first build to say "at constant currency"; no input changed):

- **An 8-K that re-presents the 10-K is a vintage of its own** (the UNP 2010 rule). The 8-K of 2009-01-13 (accepted 13:17 ET, during the
  session) re-presents the FY2008 annual report with Gazeley and the Seiyu restructuring as discontinued operations: net sales FY07
  $344,759M and FY08 $374,307M (first reported $344,992M and $374,526M), EPS unchanged. It changes the revenue history, so from that date
  the history takes 1999-2008 from its eleven-year summary. It carries no Item 1 or 1A, so the FY2008 10-K's words stay in the "why".
- **Three 10-K vintages, each with a Q4 print before it, and five-year summaries.** The FY2009 10-K (accepted 2009-04-01 15:48 ET, during
  the session), FY2010 (2010-03-30 17:07 ET, dated 2010-03-31) and FY2011 (2011-03-30 17:31 ET, dated 2011-03-31) move the history to
  fiscal 2000-2009, 2001-2010 and 2002-2011. From the FY2009 10-K Walmart publishes a Five-Year Financial Summary, so each vintage takes its
  five years from its own 10-K and the older years from the latest filing that still reports them: fiscal 2005 from the FY2009 10-K,
  2006 from the FY2010 10-K, and 2000-2004 from the re-presented eleven-year summary of 2009-01-13. Seams stay in, as published: the
  FY2010 10-K reclassifies revenue and expense items (FY08 net sales $373,821M) and the FY2011 10-K adjusts FY07-FY10 for a change in
  inventory accounting (FY07 $2.93, FY08 $3.15, FY10 $3.73; FY09 unchanged at $3.35). First-year diluted shares come from the latest
  10-K that reports them: fiscal 2000's 4,474M (FY2002 10-K), 2001's 4,484M (FY2003 10-K), 2002's 4,481M (FY2004 10-K). Each Q4 release
  (2009-02-17, 2010-02-18, 2011-02-22) extends the history with its year until the 10-K.
- **EPS: the company's figure excluding one-offs where it publishes one** (the ACN rule), each from the latest filing that publishes it
  (the SHW 2000 rule):
  - FY09 $3.42, "underlying EPS" excluding the settlement of 63 wage-and-hour class actions (reported $3.35; Q4 FY09 release, repeated
    as "adjusted" in the Q4 FY10 release);
  - FY10 $3.66, "adjusted" excluding $0.10 of net tax benefits and $0.04 of restructuring charges (reported $3.72; Q4 FY10 release);
  - FY11 $4.07, "underlying" excluding about $0.11 of tax benefits (reported $4.18; Q4 FY11 release, whose text also prints $4.072,
    $4.073 and $4.074; the reconciliation table's $4.07 is used).
  - **A year restated before an excluding figure exists on the new basis keeps the old one** (the UNP 2005 rule). The Q3 FY11 release
    (2010-11-16) gives FY10 as adjusted for the inventory change at $3.734, "which included the same six cents benefit", with no figure
    excluding it, so FY10 stays $3.66 until the Q4 FY11 release (2011-02-22) publishes $3.67 on the new basis. That later print replaces
    the year until the FY2011 vintage carries it (`restates`, the SHW rule; the builder gains the field).
  - No year is excluded. A one-off with no published figure excluding it stays in: Q3 FY11's tax benefit (about $0.05), the FY11 guide
    that reflects it ($4.08-4.12), and the operating margins of Q4 FY09 and Q4 FY10, which include the litigation and restructuring
    charges (the releases publish no consolidated operating income excluding them).
- **Guides.** Every release gives the next quarter's EPS range. The Q4, Q2 and Q3 releases give the fiscal year's: FY10 $3.45-3.60, then
  $3.50-3.60 and $3.57-3.61; FY11 $3.90-4.00, then $3.95-4.05 and $4.08-4.12; FY12 $4.35-4.50, then $4.41-4.51 and the Q3 FY12 release's
  "implies a full year EPS from continuing operations range of $4.45 to $4.51", read as a range in numbers. The Q1 releases give none,
  so the last range stands. Net sales are guided in numbers once: "net sales for fiscal 2012 to grow between four and six percent" (Q4
  FY11 release), used as published from 2011-02-22 (the fiscal-year net sales guide; no filing guides in local currency, the MSFT and LOW
  reading). The comparable-sales guides, now for Walmart U.S. and Sam's Club separately, are shown in the guide line and feed nothing.
- **BASE growth before the FY12 guide: the latest quarter excluding the currency effect the release states** (the NKE, PEP and SHW rule).
  Most releases state a consolidated constant-currency growth rate (Q1-Q3 FY10 +4.5%, +2.7%, +3.8%; Q2 FY11 +2.0%; Q4 FY11 +1.9%; Q1-Q3
  FY12 +3.0%, +3.2%, +6.8%). Q4 FY10 and Q1 FY11 state the consolidated currency benefit in dollars ($1.9 billion, $2.5 billion), and Q3
  FY11 states International's ($349 million); Walmart has no other segment outside the United States, so these are the company's dollars.
  Each is converted on the year-ago net sales of the same release: +2.8%, +3.3%, +2.3%. Q4 FY09 states a constant-currency rate for
  International only (+9.0%) and no consolidated figure or dollars, so it is not converted (the SHW 2008 rule): BASE takes the reported
  +1.7%. The builder re-derives each dollar-based rate and checks each stated rate against the stated dollars.
- **Dividends,** from the 10-K that states the rate: $1.09 a year (FY2009 10-K, increased March 5, 2009), $1.21 (FY2010 10-K, March 4,
  2010), $1.46 (FY2011 10-K, March 3, 2011). The re-presentation of 2009-01-13 repeats the $0.95 of March 2008.
- **Renamed lines** (the ACN rule): International becomes Walmart International from the Q1 FY11 release (2010-05-18).
- **Adds nothing:** the 8-K of 2010-01-28, which estimates Q4 FY10 restructuring charges at about $0.04 a share without restating a
  range; the communication-policy 8-Ks of 2009-02-05 and 2009-05-14 (comparable-sales forecasts every 13 weeks; full-year EPS forecasts
  promised in the Q4 release); the debt-offering 8-Ks (2009-01-22, 2009-03-26, 2009-05-20, 2009-07-24, 2009-09-18, 2010-04-01,
  2010-07-07, 2010-10-22, 2011-04-15); the officer, director, vote and registration-rights 8-Ks; the litigation statement of 2010-04-26;
  and the 10-Qs (no guidance).
- **Builder changes (no 2008 output changes; the 53 dates rebuild byte-identical):** the constant-currency fallback, `restates`, the
  segment comparable-sales guide text and a currency line in the volumes text.

Controls: altering one value of each new print (with its constant-currency rate, each Q4 print's full-year EPS and the restated FY10),
guide (with the FY12 net sales range) and vintage changes no date before its publication and changes the first weekly date on or after
it (57 new controls, 83 of 83 in all). A scan of all 209 WMT models for the figures, notes, guides and texts of every print, guide and
vintage finds none before its first publication (0 of 11,026); no model carries a calendar year after its date outside an FY label.

Seen in the build (method behaviour, not tuned):
- **CHEAP and BUY on all 156 dates.** Robustness is 8 of 8 on every date but six (2010-09-24 to 2010-11-12), where the variant with
  multiples one band cheaper reads FAIR or RICH (7 of 8).
- **The floor comes down to the stock.** The EPP floor, the median of the calendar-year P/E lows, falls as each new year adds a 12-15x low
  and the late-1990s years leave the window: 20x in early 2009, 18x by its end, 15x in 2010, 14x in 2011. The P/E on guided EPS is
  13.5-15.3x in 2009, 12.2-15.0x in 2010 and 11.2-13.8x in 2011 (0th-19th percentile of the window throughout), so the price sits 17-33%
  under the floor in 2009 and 0-20% under it in 2010-2011.
- **The anchor is the guided year:** FY09 $3.44 to 2009-02-13; FY10 $3.525, $3.55 and $3.59; FY11 $3.95, $4.00 and $4.10; FY12 $4.425,
  $4.46 and $4.48.
- **BEAR is flat EPS** (no down year in any vintage) at the 10th-percentile P/E (12.7-15.3x): $51-59, about the price, so Ratio B runs from
  -0.10 to 0.05. XBULL is fiscal 1999-2001 (+23.8%/yr) until the FY2009 vintage, then fiscal 2002-2004 (+17.8%); BULL is the decade CAGR
  (+14.4% falling to +10.9%, then +11.7% in the FY2011 vintage).
- **BASE** is +8.6%/yr in January 2009, +3.0-3.1% on the Q4 FY09 print's reported +1.7%, +3.6% to +5.9% on the constant-currency
  quarters, and +7.0-7.2% on the FY12 sales guide from 2011-02-23 (each with 1.1-2.2% of buyback).
- **The proxy composite** runs 1.30-2.35: comparable sales at BEAR (below 2%) on every print but Q3 FY09, Q4 FY09, Q1 FY10 and Q3
  FY12; net sales growth at BEAR (below 10%) on every print; gross margin at BULL or XBULL through FY10 (+35bp to +85bp), then BASE or
  BEAR (-52bp to +1bp). The market composite stays at 1.00-1.63, so the adjusted gap runs from +0.11 to +1.57.

How far each call moves the classes (the 156 dates rebuilt with one encoding changed; no outcome consulted): none moves a class or a
tier. Tested: Q4 FY09's International rate converted to a company figure (BASE +6.1% instead of +1.7%); reported EPS for FY09-FY11
instead of the company's figures; FY10 at the restated $3.73 from the Q3 FY11 print; BASE on reported growth throughout; the Q3 FY12
implied range read as no guide; the FY12 net sales guide ignored; the 2009-01-13 re-presentation read as no vintage; and every signal at
its BEAR value (the adjusted gap falls to -0.28 to +0.37, still above CHEAP's -0.45 line with the price at or below the floor).

Judgement calls that could carry hindsight (in addition to the 2008 list, which stands):
- the company's "underlying" and "adjusted" EPS in the history (no class moves at reported EPS);
- FY10 kept at $3.66 between the inventory restatement and the first figure excluding the one-offs on the new basis;
- a currency effect in dollars converted to a rate, and International's dollars read as the company's (no class moves either way);
- the Q3 FY12 "implies" range read as a guide, and the FY12 net sales growth guide used in dollars as published.

### WMT 2012-2014: the Vips restatement, an underlying FY14, a guide in words, net sales guides, currency from dollars

```bash
python3 retro/build_wmt.py --weekly 2012-01-02 2014-12-31                   # 157 dates, 2012-01-06 .. 2014-12-31
for c in 2012-02-21 2012-03-28 2012-07-01 2013-01-01 2013-02-21 2013-03-27 2013-08-15 2013-11-14 2014-01-01 2014-01-31 \
         2014-02-20 2014-03-24 2014-07-01 2014-11-13 2015-01-01; do python3 retro/tools/firewall.py $c WMT; done
```

Every 8-K, 10-Q and 10-K of January 2012 to December 2014 was read (46 filings: 33 8-Ks and one 8-K/A, 9 10-Qs, 3 10-Ks),
directly, with no delegated transcription. The records are generated by script from the transcribed raw figures, as before; 418 more
strings were checked with `verbatim.py` (1,149 in all). Thresholds (rule T), signals and the engine are unchanged. Decided before any
2012-2014 date was scored. After the first build, and before any outcome was computed, the Q4 FY14 release's restated FY13 was added
(checking the `restates` precedent, below) and two notes were reworded (the Q3 FY14 print's Vips note now quotes the release; the Q3
FY15 guide note lost a nested parenthesis):

- **Three 10-K vintages, each with a Q4 print before it.** The FY2012 10-K (accepted 2012-03-27 17:22 ET, dated 2012-03-28), FY2013
  (2013-03-26 17:09 ET, dated 2013-03-27) and FY2014 (Friday 2014-03-21 17:10 ET, dated Monday 2014-03-24) move the history to fiscal
  2003-2012, 2004-2013 and 2005-2014. Each takes its five years from its own Five-Year Financial Summary and the older years from the
  latest filing that still reports them: fiscal 2003-2004 from the eleven-year summary re-presented on 2009-01-13, 2005 from the FY2009
  10-K, 2006 from FY2010, 2007 from FY2011, 2008 from FY2012. First-year diluted shares: 2003's 4,446M (FY2005 10-K), 2004's 4,373M
  (FY2006 10-K), 2005's 4,266M (FY2007 10-K). Each Q4 release (2012-02-21, 2013-02-21, 2014-02-20) extends the history until the 10-K.
- **The Vips restatement, as published.** The Vips restaurants in Mexico, being sold, move to discontinued operations in Q3 FY14: the
  Q3 FY14 release's year-ago $1.07 "reflects $0.01 per share from Vips restaurants in Mexico now in discontinued operations". The Q4
  FY14 release gives FY13 at $5.01 (first reported $5.02). Each year comes from the latest filing that reports it, so $5.01 replaces
  $5.02 from 2014-02-20 (`restates`, the XOM, MSFT and SHW encoding of a later print's figure) until the FY2014 10-K carries it. That
  10-K restates FY10-FY13 net sales ($404,743M, $418,500M, $443,416M, $465,604M) and FY10, FY12 and FY13 EPS ($3.72, $4.53, $5.01; FY11
  stays $4.18), and the vintage takes them as published.
- **EPS: GAAP for FY12 and FY13, the company's underlying figure for FY14.** FY12 ($4.54) includes about $0.05 of net benefits (tax
  matters, real estate) and FY13 ($5.02) a lower-than-expected tax rate; no filing publishes either year without them, so they stay in.
  FY14 enters at the company's "underlying" $5.11, excluding $0.26 of six discrete items (Brazil non-income tax and employment
  contingencies, the Brazil and China store closures, China lease charges, the India transaction and the Sam's Club restructuring;
  reported $4.85), from the Q4 FY14 release and in the FY2014 vintage (the ACN rule). FY10 keeps the company's underlying $3.67,
  published before the Vips restatement, since no figure excluding its one-offs exists on the new basis (the UNP 2005 rule); FY09 and
  FY11 keep $3.42 and $4.07. No year is excluded. FY14's operating margin (the EPS check only) takes reported operating income, the
  discrete items in: the release gives the underlying figure only rounded ("$27.8 billion").
- **Guides.** Every release gives the next quarter's EPS range; the Q4, Q2 and Q3 releases the fiscal year's: FY13 $4.72-4.92,
  $4.83-4.93, $4.88-4.93; FY14 $5.20-5.40 (with "around $0.09" of e-commerce costs), $5.10-5.30, then "underlying" $5.11-5.21, which
  excludes about $0.10 for the store closures in Brazil and China and the India transaction (Q3 FY14 release; reported $5.01-5.11 in the
  note): the range without the items (the ACN rule); FY15 $5.10-5.45, $4.90-5.15, $4.92-5.02 (with about $0.03 for Walmart Japan
  closures; no range without it). The Q4 FY14 quarter range is underlying too ($1.60-1.70; reported $1.50-1.60).
  - **A guide in words.** The 8-K of 2014-01-31 (07:52 ET, before the open) expects underlying EPS "at or slightly below the low end of
    our range of $5.11 to $5.21", with the discrete items now about $0.26. Words, so the range stands (the ACN rule); the words are shown
    in the guide line until a later numeric range replaces them (`fy_words`, new in the WMT builder).
  - **Net sales, guided twice and used as published** (the FY12 reading): FY14 "net sales to grow between 2 and 3 percent for the full
    year versus our previous range of 5 to 6 percent" (Q2 FY14 release, 2013-08-15); FY15 "In October, we forecasted a 3 to 5 percent
    net sales increase for fiscal 2015 ... we expect to be toward the low end of the net sales guidance" (Q4 FY14 release, 2014-02-20).
    Neither earlier range was filed (both were given outside a filing), so each enters with the release that states it; the "low end"
    words go to the guide line (`rev_guide_note`, new), the range standing.
- **BASE growth without a sales guide: the latest quarter excluding the currency effect, from the release's dollars.** From Q4 FY12 the
  releases' constant-currency rate also leaves out acquisitions (Massmart, Netto: "The impact of acquisitions is excluded from the
  calculation until the acquisitions are included in both comparable periods"), so it is not the company's growth excluding currency.
  Every release states the currency effect in dollars, in its text or its constant-currency table, so each rate is derived from those
  dollars on the year-ago net sales of the same release (the 2009-2011 conversion), with acquisitions kept in, as SHW keeps them in
  BASE: Q4 FY12 +6.6% (the release's +4.5% before acquisitions), Q1 FY13 +9.3% (+7.5%), Q2 FY13 +6.5% (+4.7%), Q3 FY13 +4.9% (+4.9%),
  Q4 FY13 +3.8% (a $147 million benefit; +3.7%), Q1 FY14 +1.9% (+1.8%). These feed BASE until the FY14 sales guide of 2013-08-15; the
  later quarters' rates (+2.1% to +3.4%) are only shown.
- **Dividends.** The Q4 FY13 release states the FY14 dividend ("The company announced its annual fiscal year 2014 dividend of $1.88 per
  share"), so $1.88 a year enters on 2013-02-21. $1.59 (approved March 1, 2012, after the Q4 FY12 release) and $1.92 (approved
  February 20, 2014; the Q4 FY14 release points to a separate dividend release, which was not filed) enter with the FY2012 and FY2014
  10-Ks (the LOW lag).
- **The "why"** takes each 10-K's Item 1 and 1A words: FY2012 and FY2013 as before ("under 69 banners" from FY2013), and the FY2014 10-K's
  "helps people around the world save money and live better – anytime and anywhere – in retail stores, online, and through their mobile
  devices" and its competition from retailers "whether through physical retail, e-commerce retail or through a combination of both
  areas". ECOMMERCE is not live before 2015-01-01, so the words stay in the "why" (the PEP obesity rule).
- **Adds nothing:** the 8-Ks of 2014-10-30 (about 30 Seiyu stores in Japan to close, charges of about $0.04-0.05 a share over several
  quarters) and 2014-12-16 (the Braun/Hummel ruling, about $0.06 a share in Q4 FY15, "not in" the guidance), which estimate charges
  without restating a range (the 2010-01-28 rule); the debt-offering 8-Ks (2013-04-10, 2013-10-01, 2014-04-07, 2014-04-21, 2014-10-17);
  the officer, director, vote and bylaw 8-Ks (2012-01-25, 2012-06-04, 2012-07-30, 2013-06-12, 2013-11-22, 2013-11-25, 2013-12-10, the
  8-K and 8-K/A of 2014-01-29, 2014-02-13, 2014-06-10, 2014-07-24, 2014-09-29, 2014-11-24); and the 10-Qs (no guidance).
- **Builder changes (the 209 dates of 2008-2011 rebuild byte-identical):** `fy_words` and `rev_guide_note` in the guide line. The
  firewall's WMT plant gains both and a later print that restates every year of the history.

Controls: altering one value of each new print (with its derived constant-currency rate, each Q4 print's full-year EPS and the
restated FY13), guide (with the FY14 and FY15 net sales ranges, the FY15 note and the words of 2014-01-31), the FY14 dividend and each
new vintage changes no date before its publication and changes the first weekly date on or after it (60 new controls, 143 of 143 in
all). A scan of all 366 WMT models for the figures, notes, guides and texts of every print, guide, vintage and dividend finds none
before its first publication (0 of 39,756); no model carries a calendar year after its date outside an FY label.

Seen in the build (method behaviour, not tuned):
- **From CHEAP to RICH.** CHEAP on 49 of the 52 dates of 2012 (RICH 2012-11-23 to 2012-12-07); in 2013 CHEAP on 2, FAIR on 3 and RICH
  on 47; RICH on all 53 of 2014 (2014-12-31 covers ISO week 2015-W01). The model tier is BUY on 140 dates, ACCUMULATE on 2013-11-29 and seven dates from 2014-09-05 to
  2014-10-31, WATCHLIST on 2014-11-07 and AVOID on the eight dates from 2014-11-14 ($83-88, at or above the BASE price of $85; Ratio B
  2.2-4.9). Robustness is 6 to 8 of 8 on 135 dates and 1 to 5 of 8 on 22, all between 2012-11-23 and 2013-10-04, where the adjusted
  gap sits near RICH's line (the FAIR dates agree with 1 of 8).
- **The asymmetry, not the floor, turns the call.** The EPP floor falls to 14x in 2012 and 13x from 2013 ($62.72-68.90 on guided EPS).
  The price rises from $59 to $76 in 2012, $69-81 in 2013 and $73-88 in 2014, from 13% under the floor to 35% over it; the P/E on guided
  EPS is 12.2-15.5x in 2012 (7th-51st percentile of the window), 13.3-15.7x in 2013 (22nd-64th) and 13.9-17.6x in 2014 (33rd-92nd). With
  BASE at $83-96, the market composite (the scenario mix the price needs for 15%/yr) climbs from 1.39-2.35 in 2012 to 1.95-2.94 in 2013
  and 2.41-3.77 in 2014, while the proxy composite stays at 1.30-1.85, so the adjusted gap falls from +0.60 to -2.24 and crosses RICH's
  -0.50 line in late 2012. In 2008-2011 the floor carried the call; from 2013 the price relative to BASE does.
- **The anchor is the guided year:** FY12 $4.48 to 2012-02-17; FY13 $4.82, $4.88 and $4.905; FY14 $5.30, $5.20 and $5.16; FY15 $5.275,
  $5.025 and $4.97.
- **BEAR is flat EPS** (no down year in any vintage) at the 10th-percentile P/E (12.3-12.7x): $57-65. BULL is the decade CAGR, +11.7%
  falling to +8.5%, raised to BASE's +12.1% on the Q1 FY13 print (BULL never sits below BASE); XBULL the best two-year run, +17.8%
  (FY02-FY11) falling to +11.1% (FY05-FY14).
- **BASE** is +7.2%/yr in January 2012, +9.2-12.1% on the derived Q4 FY12 to Q2 FY13 rates, +4.8-7.7% on Q3 FY13 to Q1 FY14, +5.4% on
  the FY14 sales guide and +6.9-7.0% on the FY15 guide (each with 2.2-3.0% of buyback).
- **The proxy composite** runs 1.30-1.85: net sales growth at BEAR (below 10%) on every print; comparable sales at BASE (+2.4% to
  +3.2%) on Q4 FY12 to Q2 FY13, then BEAR (below 2%); gross margin at BEAR (-28bp to -40bp) on Q4 FY12, Q1 FY13 and Q4 FY14, BASE on
  the other nine; inventories growing more than 1pp faster than sales (BEAR) on eight of the twelve prints; the operating margin at
  BASE except Q3 FY14 (+10.5bp, BULL) and Q4 FY14 (-105bp with the discrete items in, BEAR).

How far each call moves the classes (the 157 dates rebuilt with one encoding changed; no outcome consulted). Two calls move something.
The release's own constant-currency rate (acquisitions out) instead of the rate derived from its dollars moves six classes (CHEAP to
FAIR on five dates from 2012-08-03 to 2012-10-26, FAIR to RICH on 2013-03-08) and no tier. FY14 at reported $4.85 with the reported
FY14 range moves no class and 13 tiers (BUY to ACCUMULATE on ten dates, ACCUMULATE to WATCHLIST on three, 2013-11-22 to 2014-10-17).
Nothing moves with the 2014-01-31 words read as the low end ($5.11), FY10 at the restated $3.72 in the FY2014 vintage, the FY14 and FY15
net sales guides ignored, or the FY15 guide read as +3%. Every signal at its BEAR value turns 31 dates RICH (28 CHEAP and 3 FAIR,
2012-06-08 to 2013-03-15; the adjusted gap falls to -2.81 to +0.01).

Judgement calls that could carry hindsight (in addition to the 2008 and 2009-2011 lists, which stand):
- the company's underlying FY14 ($5.11) and underlying FY14 range ($5.11-5.21) instead of reported (13 tiers move, no class);
- the currency effect derived from the release's dollars with acquisitions kept in, instead of the release's own constant-currency rate
  (six classes move);
- the 2014-01-31 words read as words (the range stands), and the FY15 "toward the low end" words kept out of the range;
- the FY14 and FY15 net sales guides used from the release that states them, the earlier unfiled ranges ignored;
- FY10 kept at the underlying $3.67 across the Vips restatement.

### WMT 2015-2017: ECOMMERCE on the watch list, adjusted EPS, sales guides at constant currency, the October 2015 reset

```bash
python3 retro/build_wmt.py --weekly 2015-01-05 2017-12-31                   # 156 dates, 2015-01-09 .. 2017-12-29
for c in 2015-01-01 2015-02-19 2015-04-02 2015-10-14 2016-02-18 2016-03-31 2016-08-18 2016-11-17 2017-02-21 2017-04-03 \
         2017-06-16 2017-11-16 2018-01-01; do python3 retro/tools/firewall.py $c WMT; done
```

Every 8-K, 10-Q and 10-K of January 2015 to December 2017 was read (48 filings: 34 8-Ks and two 8-K/As, 9 10-Qs, 3 10-Ks),
directly, with no delegated transcription. The records are generated by script from the transcribed raw figures, as before; 411 more
strings were checked with `verbatim.py` (1,560 in all). Thresholds (rule T), signals and the engine are unchanged. Decided before any
2015-2017 date was scored; after the first build, and before any outcome was computed, two notes were corrected: the FY2015 and FY2016
vintages' normalization notes named the later releases that repeat a company figure (the Q4 FY16 and Q4 FY17 releases), so each now names
only the releases public by its date, and two notes now elide a fiscal year after the date ("approved the ... annual dividend", as in the
FY2014 vintage; the 2015-10-14 guide note). No input changed.

- **Three 10-K vintages, each with a Q4 print before it.** The FY2015 10-K (accepted 2015-04-01 16:44 ET, dated 2015-04-02), FY2016
  (2016-03-30 17:18 ET, dated 2016-03-31) and FY2017 (Friday 2017-03-31 16:54 ET, dated Monday 2017-04-03) move the history to fiscal
  2006-2015, 2007-2016 and 2008-2017. Each takes its five years from its own Five-Year Financial Summary and the older years from the latest
  filing that still reports them (fiscal 2006 from the FY2010 10-K ... 2012 from the FY2016 10-K). The summaries restate nothing.
  First-year diluted shares: 2006's 4,188M (FY2008 10-K), 2007's 4,168M (FY2009 10-K), 2008's 4,072M (FY2010 10-K). Each Q4 release
  (2015-02-19, 2016-02-18, 2017-02-21) extends the history until the 10-K.
- **EPS: the company's figure excluding one-offs, each year** (the ACN rule, each from the latest filing that publishes it, the SHW rule):
  FY15 the "underlying" $5.07 (reported $4.99: a wage-and-hour litigation matter and Walmart Japan closures); FY16 the "adjusted" $4.59
  (reported $4.57: the closure of 269 stores, discrete tax items and the Q3 FY16 lease accounting adjustment); FY17 the "adjusted" $4.32
  (reported $4.38: the Yihaodian gain, U.S. discontinued real estate projects and severance). FY14 keeps $5.11 (repeated in the Q4 FY15
  release). No year is excluded. FY16 is the first down year of any vintage (-9.5% on FY15), so BEAR stops being flat EPS from 2016-02-19.
- **Guides.** Every release gives the next quarter's EPS range except Q3 FY17 and Q3 FY18 (comparable sales only); the Q4, Q2 and Q3
  releases the fiscal year's: FY16 $4.70-5.05, $4.40-4.70, $4.50-4.65; FY17 $4.00-4.30, then "adjusted" $4.15-4.35 (excluding the $0.14
  Yihaodian gain; GAAP $4.29-4.49) and $4.20-4.35 (GAAP $4.34-4.49); FY18 $4.20-4.40, then "adjusted" $4.30-4.40 (GAAP $4.18-4.28) and
  $4.38-4.46 (GAAP $3.84-3.92, the debt extinguishment, FCPA accrual, Suburbia gain and international impairments): the range without the
  items (the ACN rule), the GAAP range in the note. The Q1 releases give no fiscal-year range, so the last one stands.
- **Net sales guides at constant currency, method r2's local-currency guide** (the PEP 2026 rule; "approximately" makes a point, the LOW rule):
  - FY16: +1-2% in the Q4 FY15 release, as published ("Given the potential impact of currency headwinds"; the October 2014 "2 to 4
    percent" was not filed). The 8-K of 2015-10-14 (the meeting for the investment community, accepted 10:46 ET, during the session, so it
    meets that day's close) expects reported growth "to be relatively flat" (words) and "Excluding the impact of currency exchange
    fluctuations, net sales growth would be approximately 3 percent for fiscal year 2016" (numbers): +3% (`rev_basis`, new) from
    2015-10-14, repeated in the Q3 FY16 release ("around 3 percent").
  - FY17: the Q4 FY16 release expects reported growth "to be relatively flat" and says "Excluding the impact of currency and store
    closures, our net sales growth guidance would have remained in the 3 to 4 percent growth range": +3-4%, which is also the last numeric
    range if "relatively flat" is read as words (the 8-K of 2015-10-14's "3 and 4 percent annually over the next three years").
  - FY18: no release or 8-K guides net sales in numbers, so BASE takes the latest quarter excluding the currency effect, derived from the
    release's dollars on the year-ago net sales (the 2012-2014 rule): +2.9% (Q4 FY17), +2.4%, +3.0%, +3.8% (Q3 FY18, a $454 million
    favourable effect). The earlier quarters' rates (+2.1% to +3.9%) are only shown.
- **Operating one-offs, release by release** (the 2009-2011 wording of the ACN rule, now encoded): a one-off inside operating income that
  the release itself states in dollars, with the change excluding it, leaves that release's operating margin (`op_oneoff_m`,
  `op_oneoff_prior_m`, new): Q2 FY17's $535 million Yihaodian gain ("Excluding this gain, consolidated operating income declined 7.2%")
  and, in Q3 FY17, the year-ago quarter's $156 million lease accounting benefit ("Excluding last year's lease accounting benefit of $156
  million, operating income decreased 7.9%"). Items stated only per share stay in (Q4 FY16's store closures, Q4 FY17's real estate and
  severance, Q2 and Q3 FY18's Suburbia gain, FCPA accrual and impairments), as does Q3 FY16's lease benefit in its own quarter (the dollars
  came a year later and are never back-filled) and the Yihaodian gain in Q2 FY18's year-ago quarter (that release states nothing without
  it). The full-year operating margins (EPS check only) stay as reported.
- **Comparable sales, with fuel, as published.** From the Q4 FY17 release the table's first column is "With Fuel" (before, "Without
  Fuel | With Fuel"), and from Q1 FY18 the headline Walmart U.S. comp excludes fuel; the signal keeps the Total U.S. figure with fuel.
- **Dividends** with the 10-Ks (the LOW lag; each Q4 release points to a separate dividend release that was not filed): $1.96 a year from
  2015-04-02 (approved February 19, 2015), $2.00 from 2016-03-31, $2.04 from 2017-04-03.
- **ECOMMERCE on the watch list from 2015-01-09** (decided 2026-11-07 for this batch, before any 2015 date was built; the MSFT CLOUD and
  XOM rule for an acknowledgement that predates the live date). ECOMMERCE is live from 2015-01-01 and its scope, physical retail with
  grocery, covers Walmart. Each 10-K's competition risk factor (`ecommerce_company_acknowledged`) puts it on the watch list from the theme's
  live date in the latest 10-K's words: the FY2014 10-K's "whether through physical retail, e-commerce retail or through a combination of
  both areas" to 2015-03-27 (2014-12-31 covers ISO week 2015-W01, so 2015-01-09 is the first weekly date after the live date), then the
  FY2015-FY2017 10-Ks' "digital retail"; the offering side is each 10-K's e-commerce contribution to comparable sales (about 0.3%, 0.3%,
  0.2%, 0.4% for Walmart U.S.). The factor pair nets to zero and the theme signal stays at 2/4, so only text changes. The registry's
  market-pricing event (2017-06-16, "grocers and food retailers sell off the same day") names no company, so it is quoted from its date and
  re-files nothing (the LOW and PEP reading); DURABLE stands. The "why" from the FY2014 vintage takes its theme clause by rule
  (`why_theme_tail`, the XOM encoding), so the 2014 dates keep "no disruption theme is live for it" byte for byte.
- **Adds nothing:** the 8-Ks of 2016-01-15 (269 store closures, $0.20-0.22 a share "not included" in the guidance), 2016-06-20 (the JD.com
  alliance), 2016-08-08 and 2016-09-19 (the Jet.com agreement and closing; "some marginal dilution above its initial estimate", words without
  a range); the 8-K of 2015-10-14's FY17 to FY19 outlook (FY17 EPS "to decline between 6 and 12 percent", a change rather than a range, and
  FY17 is not the current year until the Q4 FY16 release replaces it); the investment-community 8-Ks of 2016-10-06 (FY17 reaffirmed; FY18
  "relatively flat to fiscal year 2017 adjusted EPS", words) and 2017-10-10 (FY18 reaffirmed; FY19 after this range); the tender-offer and
  debt 8-Ks (2017-06-15, 2017-06-29, 2017-07-14, 2017-10-06, 2017-10-18, 2017-10-23, 2017-11-06); the officer, director, vote, bylaw and
  name-change 8-Ks (2015-06-08, 2015-10-09, 2016-01-29, 2016-06-07, 2016-11-18, 2017-01-06, 2017-01-27, 2017-06-06, 2017-11-08,
  2017-12-06; the new name takes effect on 2018-02-01); and the 10-Qs.
- **Anachronism list:** "Walmart Inc." was first in a Wal-Mart filing in the name-change 8-K of 2017-12-06 (accepted 09:00 ET), not the
  Form 4 of 2018-01-31; `taxonomy_eras.json` is corrected. It only loosens the gate by eight weeks, and no model uses the name.
- **Builder changes (the 366 dates of 2008-2014 rebuild byte-identical):** events gated by the theme's live date, `why_theme_tail`,
  `rev_basis`, `op_oneoff_m`, `op_oneoff_prior_m` and `op_margin_note`. The firewall's WMT plant gains the last five.

Controls: altering one value of each new print (its comparable sales, its currency effect, each Q4 print's full-year EPS and each
operating one-off), guide (each EPS, net sales and quarter range), vintage (first-year EPS and shares, the dividend) and ECOMMERCE event
changes no date before its publication (the theme's live date for the FY2014 10-K) and changes the first weekly date on or after it (67 new
controls, 210 in all). A scan of all 522 WMT models for the figures, notes, guides and texts of every print, guide, vintage and event
finds none before its first publication (0 of 125,725); no model carries a calendar year after its date outside a fiscal-year label.

Seen in the build (method behaviour, not tuned):
- **RICH on 151 of 156 dates.** 2015: RICH 47, CHEAP 4 (2015-10-30, 2015-11-13, 2015-12-11, 2015-12-18), FAIR 1 (2015-10-23); 2016 and
  2017 RICH throughout. The model tier is AVOID on 116 dates (18 in 2015, 46 in 2016, all 52 of 2017), BUY on 22, ACCUMULATE on 15 and
  WATCHLIST on 3. Robustness is 8 of 8 on 142 dates and 2 to 7 of 8 on the 14 dates from 2015-10-16 to 2016-01-22, where the adjusted gap
  sits near RICH's -0.50 line.
- **The guided year falls, then the multiple rises.** The anchor is FY15 $4.97 to 2015-02-13; FY16 $4.875, $4.55 and $4.575; FY17 $4.15,
  $4.25 and $4.275; FY18 $4.30, $4.35 and $4.42. The EPP floor is 13x (12x on 2016-12-30 alone), $51-65. The price runs $56-89 in 2015,
  $62-74 in 2016 and $66-99 in 2017; on guided EPS that is 12.4-18.0x in 2015 (11th-95th percentile of its own window), 13.5-17.8x in 2016
  (29th-98th) and 15.4-22.3x in 2017 (70th-100th), 4-72% over the floor after the October 2015 low (-5% to +38% in 2015).
- **The October 2015 reset is the one window near the line.** On 2015-10-16 the price is $58.89 after the 8-K of 2015-10-14, and BASE
  rises from +4.4% to +5.9% on the +3% constant-currency guide; the adjusted gap runs -0.24 to -0.82 from 2015-10-16 to 2015-12-24, the
  five CHEAP and FAIR dates among them. Elsewhere it is -1.0 to -2.5.
- **BEAR turns.** BEAR is flat EPS at the 10th-percentile P/E (12.3x) to 2015-02-13, then -0.8%/yr (FY15 under FY14), and -9.5%/yr from
  2016-02-19 (FY16 under FY15): $42-45, so Ratio B runs to infinity whenever the price passes the BULL price in 2016-2017. BULL is the
  decade CAGR, +8.5% falling to +7.2%, then held at BASE's rate from 2016-02-19 (the CAGR falls below it; BULL never sits below BASE);
  XBULL stays +11.1%, the fiscal 2010-2012 run.
- **BASE** is +7.0%/yr in January 2015 (the FY15 +3-5% guide), +4.3-4.4% on the FY16 +1-2% guide, +5.9% on the +3% constant-currency guide,
  +6.2-6.4% on the FY17 +3-4% guide and +5.4-6.8% on the FY18 quarters at constant currency (each with about 2.9% of buyback).
- **The proxy composite** runs 1.35-2.00: comparable sales between BEAR and BASE (+0.1% to +2.0%) on every print but Q3 FY18 (+3.0%), net
  sales growth below BEAR's 7% on every print, gross margin above BULL (+34bp to +60bp) from Q3 FY16 to Q3 FY17, then +5bp to -30bp from Q4 FY17
  to Q3 FY18, inventories growing 2-5 points slower than sales from Q1 FY17, and the operating-margin change -92bp (Q4 FY16) to
  +38bp (Q4 FY15). The market composite (the scenario mix the price needs for 15%/yr) is 2.15-3.91.

How far each call moves the classes (the 156 dates rebuilt with one encoding changed and classified offline; no outcome consulted):
- the FY16 "relatively flat" read as words, so the +1-2% stands to 2016-02-18: three classes (FAIR to RICH on 2015-10-23, CHEAP to FAIR on
  2015-10-30 and 2015-12-11), no tier. Sales on the reported basis throughout (that, the FY17 guide as 0%, the quarters as reported) moves
  the same three;
- reported EPS for FY14-FY17 with the GAAP ranges of FY17 and FY18: two classes (FAIR to CHEAP on 2015-10-23, RICH to FAIR on 2015-11-06)
  and six tiers (four in 2015, two in early 2017);
- every signal at its BEAR value: five classes (the four CHEAP dates and the FAIR one to RICH), no tier;
- nothing moves with no FY17 sales guide in numbers, operating margins as reported, or Q2 FY18 measured against the year-ago quarter
  without the Yihaodian gain. ECOMMERCE re-filed from 2017-06-16 would change the class label only (the ACN GENAI rule).

Judgement calls that could carry hindsight (in addition to the 2008, 2009-2011 and 2012-2014 lists, which stand):
- the FY16 constant-currency figure ("approximately 3 percent") preferred to the reported "relatively flat" (three classes move);
- the company's underlying and adjusted EPS for FY15-FY17 and the adjusted FY17 and FY18 ranges (two classes, six tiers);
- the FY17 "3 to 4 percent" excluding currency and store closures (nothing moves without it);
- operating one-offs taken out only where the release states them in dollars (nothing moves either way);
- ECOMMERCE kept on the watch list after 2017-06-16 for the largest U.S. grocer: the registry's evidence is a grocers' sell-off that names
  no company, and adding press coverage that names Walmart would mean picking articles by hand (label only);
- filed documents only: the dividend releases and investor-conference statements that were not filed are not used.

### WMT 2018-2020: Walmart Inc., adjusted EPS through the Tax Act and the JD.com marks, guides in words, the FY21 withdrawal

```bash
python3 retro/build_wmt.py --weekly 2018-01-01 2020-12-31                   # 157 dates, 2018-01-05 .. 2020-12-31
for c in 2018-02-01 2018-02-20 2018-04-02 2018-08-16 2018-10-16 2019-02-19 2019-03-29 2019-08-15 2020-02-18 2020-03-23 \
         2020-05-19 2020-11-17 2021-01-01; do python3 retro/tools/firewall.py $c WMT; done
```

Every 8-K, 10-Q and 10-K of January 2018 to December 2020 was read (60 filings: 47 8-Ks and one 8-K/A, 9 10-Qs, 3 10-Ks),
directly, with no delegated transcription. The records are generated by script from the transcribed raw figures; 401 more strings were
checked with `verbatim.py` (1,961 in all). Thresholds (rule T), signals and the engine are unchanged. Decided before any 2018-2020 date
was scored; after the first build, and before any outcome was computed, the withdrawal quote was cut to its stem ("the company is
withdrawing financial guidance"), so that no model carries "fiscal year 2021" before 2021 (the 2015-2017 elision). No input changed.

- **Walmart Inc.** The legal name changes on 2018-02-01 (the 8-K of that day, accepted 09:27 ET, before the open; announced in the 8-K
  of 2017-12-06). `company_names` (the ACN rule) gives the new name from 2018-02-02, eight weeks before the FY2018 10-K carries it.
- **Three 10-K vintages, each with a Q4 print before it.** The FY2018 10-K (accepted Friday 2018-03-30 16:01 ET, Good Friday with the
  market closed, dated Monday 2018-04-02), FY2019 (2019-03-28 16:56 ET, dated 2019-03-29) and FY2020 (2020-03-20 16:51 ET, dated
  2020-03-23) move the history to fiscal 2009-2018, 2010-2019 and 2011-2020. From FY2018 the 10-K carries the statements itself (no
  Exhibit 13); each takes its five years from its own Item 6 summary and older years from the latest filing that reports them. The new
  revenue (FY19) and lease (FY20) standards were adopted without recasting the summaries, which restate nothing. First-year diluted
  shares: 2009's 3,951M (FY2011 10-K), 2010's 3,877M (FY2012 10-K), 2011's 3,670M (FY2013 10-K).
- **EPS: the company's adjusted figure, each year** (the ACN rule; each from the latest filing that publishes it, as every Q4 release
  repeats the year before): FY18 $4.42 (reported $3.28: the loss on extinguishment of debt, restructuring, impairments, the FCPA accrual,
  a lump-sum bonus, the Tax Act benefit, the Suburbia gain, a legal recovery); FY19 $4.91 (reported $2.26: the $4.8 billion loss on the
  Walmart Brazil sale, unrealized JD.com losses, which a new accounting standard put into net income from FY19, and Tax Act adjustments);
  FY20 $4.93 (reported $5.19: a JD.com gain, restructuring and income tax items). No year is excluded. FY19's reported EPS is under half
  its adjusted figure, but the company publishes the figure without the items, so the AAPL distorted-year test never applies.
- **Guides.** From FY19 Walmart gives fiscal-year guidance only, no quarter EPS range:
  - FY19: EPS $4.75-5.00 and net sales +1.5% to +2.0% at constant currency (Q4 FY18 release); adjusted $4.90-5.05 excluding Flipkart,
    which had not closed (GAAP $2.90-3.05), and net sales "About 2%" (Q2 FY19); adjusted $4.65-4.80 including about $0.25 of Flipkart
    dilution (GAAP $2.65-2.80; the 8-K of 2018-10-16, accepted 06:31 ET, before the open); adjusted $4.75-4.85 (Q3 FY19; GAAP $2.26-2.36).
    The adjusted range is the range without the items (the ACN rule); the 8-Ks of 2018-04-30, 2018-05-09 and 2018-06-04 estimate the
    Asda, Flipkart and Brazil effects without restating a range and add nothing (the 2010-01-28 rule).
  - FY20: no EPS range in numbers. The 8-K of 2018-10-16 and the Q4 FY19 release expect EPS to "Decline by a low single-digit percentage
    range compared with FY19 adjusted EPS", the Q2 FY20 release a "Slight decrease to slight increase", the Q3 FY20 release "to increase
    slightly": words, so FY19's $4.91 stands all year (the rollover rule) and the words are shown (`fy_words`, now "words, no range").
    Net sales: "At least 3 percent in constant currency" is a one-sided bound and gives no field (the PEP, UNP and LOW rule; `rev_words`,
    new, shows it), so BASE takes the latest quarter at constant currency (+3.2%, +2.6%) until the Q2 FY20 release's "Around 3% in constant
    currency" (+3%, a point).
  - FY21: EPS $5.00-5.15 and net sales "Around 3% in constant currency" (Q4 FY20 release, 2020-02-18). The Q1 FY21 release (2020-05-19):
    "Due to unprecedented variability in the macro environment brought on by COVID-19, the company is withdrawing financial guidance for
    fiscal year 2021." A withdrawal voids every earlier field for its year (the LOW and SHW rule; `withdrawn`, new in the WMT builder), so
    FY20's $4.93 stands and BASE takes the latest quarter at constant currency (+9.7%, +7.6%, +6.2%). No later filing of 2020 restores a guide.
- **Operating one-offs, release by release** (the 2015-2017 rule): from Q4 FY20 the releases publish adjusted operating income in dollars,
  so the margins exclude Q4 FY20's $546 million of restructuring charges, Q2 FY21's $380 million restructuring charge and $77 million
  discrete tax item, and in Q3 FY21 the year-ago quarter's $293 million Jabong.com impairment. Q3 FY20's own release states that impairment
  only rounded ("$0.3 billion", with the change excluding it in words), so its print keeps it (the FY14 precedent). Q4 FY18's discrete
  charges are stated per share only ("would have decreased less than 1.0 percent", words) and stay in, which also sets Q4 FY19's year-ago
  base. The Walmart Brazil loss and the JD.com marks sit below operating income.
- **Comparable sales, with fuel, as published** (the table's first column). The FY20 table compares 14 weeks with 14 weeks (a 53-week
  calendar), as published.
- **Dividends** with the 10-Ks (the LOW lag; no release states them): $2.08 a year from 2018-04-02, $2.12 from 2019-03-29, $2.16 from
  2020-03-23. From FY2019 the 10-K says "The Board of Directors approved, effective February 19, 2019, the ... annual dividend".
- **ECOMMERCE stays on the watch list** in each 10-K's words: the FY2018 10-K's competition "whether through physical retail, digital
  retail or the integration of both"; the FY2019 and FY2020 10-Ks drop that heading and name competition with "global eCommerce and
  omni-channel retailers" in the body. The offering side is each 10-K's eCommerce contribution to comps (about 0.7%, 1.3%, 1.7%). EV
  (from 2020-01-01, scoped to fuel retail among others) and CRYPTO (from 2020-10-21) are not recorded: no filing names electric vehicles
  or crypto as a risk, and their registered evidence names no retailer. The "why" quotes the MD&A's "We operate in the highly competitive
  (omni-channel) retail industry in all of the markets we serve", the 10-Ks no longer saying "The retail business is highly competitive".
- **Adds nothing:** the tender-offer and debt 8-Ks (2018-01-09, 2018-01-25, 2018-06-26, 2019-04-22, 2019-09-23); the Asda-Sainsbury's,
  Flipkart, Walmart Brazil, Asda pension buy-in, Asda, Argentina and Seiyu sale 8-Ks (2018-04-30, 2018-05-09, 2018-05-11, 2018-06-04,
  2019-10-18, 2020-10-02, 2020-11-06, 2020-11-16), each estimating a loss or dilution without restating a range; the FCPA resolution
  (2019-06-20); the TikTok statements (2020-09-14, 2020-09-21); the opioid and DEA statements (2020-10-23, 2020-12-22); the officer,
  director, vote, bylaw and trading-plan 8-Ks; the 2018-10-16 8-K's FY20 outlook until FY20 is current, when the Q4 FY19 release restates it;
  and the 10-Qs.
- **Builder changes (the 522 dates of 2008-2017 rebuild byte-identical):** `withdrawn` (with `withdrawn_quote`) and `rev_words`. The
  firewall's WMT plant gains `rev_words` and a later withdrawal of every guided field.

Controls: altering one value of each new print (comparable sales, currency effect, each Q4 full-year EPS, each operating one-off), guide
(each EPS range, net sales range and words), vintage (first-year EPS and shares, the dividend), ECOMMERCE event, the company name, and
removing the withdrawal changes no date before its publication and changes the first weekly date on or after it (57 of 59 new controls;
269 in all). The other two are the 8-K of 2018-10-16's FY20 words, never the latest on any date: FY20 becomes current only with the Q4
FY19 release, which restates them. A scan of all 679 WMT models for the figures, notes, guides and texts of every print, guide, vintage,
event and the company name finds none before its first publication (0 of 205,351); no model carries a calendar year after its date
outside a fiscal-year label.

Seen in the build (method behaviour, not tuned):
- **RICH and AVOID on all 157 dates, robustness 8 of 8 on every one.** The price runs $82-108 in 2018, $93-120 in 2019 and $108-152 in
  2020 (as traded), against an EPP floor of 13x ($57-66): 30-136% over it. On guided EPS that is 16.9-24.5x in 2018 (81st-100th
  percentile of its own window), 19.5-24.5x in 2019 (93rd-100th) and 21.2-30.8x in 2020 (90th-100th). Ratio B is infinite (the price over
  the BULL price) on every date from 2019.
- **The anchor:** FY18 $4.42 to 2018-02-16; FY19 $4.875, $4.975, $4.725 (Flipkart) and $4.80; FY20 FY19's $4.91 all year; FY21 $5.075,
  then FY20's $4.93 from the withdrawal.
- **BEAR is -9.5%/yr** (FY16 under FY15) at the 10th-percentile P/E (12.3-12.4x): $45-51. BULL sits at BASE's rate on every date: the
  decade EPS CAGR (2-4%/yr, FY08-FY17 to FY11-FY20) stays below BASE. XBULL is +11.1% (fiscal 2010-2012), +10.9% (fiscal 2011-2013) from
  the FY2020 vintage, and BASE's +12.5% while BASE exceeds it after the withdrawal.
- **BASE** is +6.8%/yr in January 2018, +4.8% on the FY19 +1.5-2.0% guide, +5.1% on "About 2%", +6.2-6.3% and +5.7% on the FY20 quarters at
  constant currency, +6.1% on "Around 3%", +5.8-6.1% on the FY21 guide, and +12.5%, +10.4% and +9.0% on the COVID quarters after the
  withdrawal (each with 2.7-3.0% of buyback).
- **The proxy composite** runs 1.50-3.10: comparable sales +2.0% to +5.2% from Q4 FY18 to Q4 FY20 (around BASE to BULL) and +9.7%, +9.0%
  and +6.6% in FY21 (up to XBULL); net sales growth below BEAR's 7% on every print but Q1 FY21 (+8.7%); gross margin down 15-66bp on every
  print to Q1 FY21, then up 63bp and 50bp; inventories growing 5-17 points slower than sales on the three FY21 prints. The highest reading, 3.10 on the Q2 FY21
  print, lifts the adjusted gap to -0.77, still past RICH's -0.50 line; the market composite is 3.75-3.93 throughout.

How far each call moves the classes (the 157 dates rebuilt with one encoding changed and classified offline; no outcome consulted):
nothing moves a class or a tier with "at least 3 percent" read as +3%, the FY21 withdrawal ignored, operating margins as reported,
reported EPS for FY14-FY20 with the GAAP ranges of FY18 and FY19 (the adjusted gap reaches -0.03 on its highest date), the FY19 sales
guides ignored, or every signal at its BEAR value (-2.89 to -2.60). The price relative to every scenario carries the call.

Judgement calls that could carry hindsight (in addition to the earlier lists, which stand):
- the company's adjusted EPS for FY18-FY20 and the adjusted guide ranges (no class moves at reported EPS);
- "at least 3 percent" as no field, and FY20's words as no range (no class moves);
- the withdrawal read as voiding the FY21 guide (no class moves);
- operating one-offs taken out only where the release states them in dollars (no class moves);
- the name change applied from its effective date, not the 2017-12-06 announcement (text only);
- ECOMMERCE, EV and CRYPTO as encoded above (label only).

### WMT 2021-2023: three-year 10-Ks, EPS guided as growth, quarter net sales guides, currency effects in dollars, divestitures in

```bash
python3 retro/build_wmt.py --weekly 2021-01-04 2023-12-31                   # 156 dates, 2021-01-08 .. 2023-12-29
for c in 2021-02-18 2021-03-22 2021-07-01 2021-08-17 2021-11-16 2022-01-01 2022-02-17 2022-03-21 2022-07-26 2022-08-16 \
         2022-11-15 2023-01-01 2023-02-21 2023-03-20 2023-08-17 2023-11-16 2024-01-01; do python3 retro/tools/firewall.py $c WMT; done
```

Every 8-K, 10-Q and 10-K of January 2021 to December 2023 was read (54 filings: 41 8-Ks and one 8-K/A, 9 10-Qs, 3 10-Ks), directly, with
no delegated transcription; the 10-Qs were searched in full for guidance and carry none. The records are generated by script from the
transcribed raw figures; 552 more strings were checked with `verbatim.py` (2,513 in all), 57 of them every quoted fragment of the new guide,
print and dividend notes. Thresholds (rule T), signals and the engine are unchanged. Decided before any 2021-2023 date was scored; after the
first build, and before any outcome was computed, two guide notes of the 8-K of 2022-07-25 were requoted in the 8-K's own words (they had
paraphrased "decline 11 to 13%" and "about 4.5%" inside quotation marks) and that source's title lost a calendar year after its date
("fiscal year 2023" now reads FY2023). No input changed.

- **Three 10-K vintages, each with a Q4 print before it, Item 6 reserved.** The FY2021 10-K (accepted 2021-03-19 16:40 ET, dated
  2021-03-22), FY2022 (Friday 2022-03-18 17:03 ET, dated Monday 2022-03-21) and FY2023 (Friday 2023-03-17 17:02 ET, dated Monday 2023-03-20)
  move the history to fiscal 2012-2021, 2013-2022 and 2014-2023. From the FY2021 10-K Item 6 is reserved ("early adoption" of the deletion of
  Item 301), so each vintage takes the three years of its own statements of income and every earlier year from the latest 10-K that reports
  it (the ACN FY21 rule): fiscal 2016-2018 from the FY2020 10-K's summary, 2019 from the FY2021 10-K, 2020 from the FY2022 10-K. Nothing is
  restated. First-year diluted shares: 2012's 3,474M (FY2014 10-K), 2013's 3,389M (FY2015 10-K), 2014's 3,283M (FY2016 10-K). Each Q4
  release (2021-02-18, 2022-02-17, 2023-02-21) extends the history until the 10-K.
- **EPS: the company's adjusted figure, each year** (the ACN rule; each from the latest filing that publishes it, as every Q4 release
  repeats the year before): FY21 $5.48 (reported $4.75: the loss on the U.K. and Japan operations held for sale or sold, equity investment
  gains, a business restructuring charge, an officer compensation charge, discrete tax items); FY22 $6.46 (reported $4.87: equity investment
  losses, the loss on extinguishment of debt, the incremental loss on the U.K. and Japan sales, restructuring); FY23 $6.29 (reported $4.27:
  equity investment losses, opioid legal charges, business reorganization and restructuring charges, the gain on the Brazil equity method
  investment, a discrete tax item). No year is excluded.
- **Fiscal 2022: words, then numbers.** The Q4 FY21 and Q1 FY22 releases guide EPS in words only ("Decline slightly", then "Increase high
  single-digits"), so FY21's $5.48 stands to 2021-08-13 (the rollover rule; `fy_words` shown). Then adjusted EPS of $6.20-6.35 (Q2 FY22; the
  guidance "is provided on a non-GAAP basis" and no GAAP range is given) and "around $6.40" (Q3 FY22, a point, the LOW "approximately" rule;
  GAAP "around $5.00" in the note).
- **Net sales on the reported basis, divestitures in.** Walmart sold Walmart Argentina (November 2020), Asda (2021-02-16) and Seiyu (March
  2021). Its FY22 net sales outlook on the reported basis is words throughout ("Decline in constant currency", "Decline low single-digits in
  constant currency", "Slightly positive in constant currency"); the only figures, "up 6% to 7%, or more than $30 billion", exclude the
  divestitures. Method r2's measure is constant-currency growth with acquisitions and divestitures in (the NKE and PEP measure; the 2012-2014
  rule kept WMT's acquisitions in), so the figures excluding divestitures are shown (`rev_words`) and give no field, and BASE takes the latest
  quarter at constant currency (+7.6%, +1.9%, +0.5%, +3.1%). The same holds for every later "excluding divestitures" figure: display only. The
  prints report net sales as published; their constant-currency rate comes from the release's dollars, the divested sales in.
- **Fiscal 2023: EPS guided as growth** (the NKE rule, new in the WMT builder: `eps_growth`). The Q4 FY22 release gives words ("Increase mid
  single-digits"), so FY22's $6.46 stands to 2022-05-13. Every later FY23 EPS guide is a growth rate on prior-year adjusted EPS ("Growth rates
  reflect an adjusted basis for prior year results"), the basis of the history, so the current-year EPS is FY22's $6.46 times the midpoint:
  "Decrease about 1%" (Q1 FY23; $6.40), "decline ... 11 to 13%" (the 8-K of 2022-07-25, accepted 16:15 ET, after the close, so dated
  2022-07-26; $5.68), 9.0% to 11.0% (Q2 FY23; $5.81) and 6.0% to 7.0% (Q3 FY23; $6.04). The latest EPS guide in either form stands.
- **Fiscal 2023 net sales: a reported guide is used as published unless the same filing states the guided period's currency effect in
  dollars; then it is converted on the year-ago net sales** (the PEP 2026 rule and the 2012-2014 conversion; `rev_reported`,
  `rev_currency_m`, `rev_prior_m`, which the builder re-derives). "Increase about 3% in constant currency" (Q4 FY22) and "about 4%" (Q1 FY23)
  are local-currency guides. From July 2022 the full-year guide is reported growth: "about 4.5%" in the 8-K of 2022-07-25 and the Q2 FY23
  release, each stating the currency headwind for parts of the year only, so used as published (the FY12 and FY14 reading); "about 5.5%" with
  "a headwind of about $4.1 billion for the year" (Q3 FY23) converts to +6.2% on FY22's $567,762M.
- **Next-quarter net sales guides** (method r2's first choice, the first WMT guides to give one): the Q2 FY23 "about 7.5%" with "a headwind
  from currency of about $1 billion" (the 8-K of 2022-07-25), the Q3 FY23 "about 5%" and the Q4 FY23 "about 3.0%", each "negatively affected
  by approximately $1.3 billion from currency fluctuations", convert to +8.2%, +5.9% and +3.9% on the year-ago quarters' net sales (`sales_basis`,
  `sales_reported`, `currency_m`, `prior_m`). From the Q4 FY23 release the quarter guides are in constant currency: +4.5% to +5.0% (Q1 FY24),
  about +4.0% (Q2), about +3.0% (Q3). The Q2 FY23 guide of the Q1 FY23 release, "Increase over 5%", is a one-sided bound and gives no field.
  After the Q3 FY24 print no quarter guide remains, so BASE takes the fiscal-year guide.
- **Fiscal 2024**: adjusted EPS $5.90-6.05 (Q4 FY23, "including an expected $0.14 impact from LIFO"), $6.10-6.20, $6.36-6.46 and $6.40-6.48;
  net sales +2.5% to +3.0%, about +3.5%, +4.0% to +4.5% and +5.0% to +5.5% in constant currency. The investment-community 8-K of 2023-04-04
  (16:22 ET, dated 2023-04-05) repeats the Q1 and FY24 ranges unchanged and adds nothing (the LOW 2022-12-07 rule); its 3-5-year framework
  (about 4% sales growth) is multi-year and not entered (the LOW rule).
- **Operating one-offs, release by release** (the 2015-2017 rule, from the adjusted operating income each release publishes): Q4 FY21's $175
  million officer compensation charge (against Q4 FY20's $546 million), Q2 FY22's year-ago $457 million, Q4 FY22's $108 million of
  restructuring (against the $175 million), Q3 FY23's $3,325 million of opioid legal charges, Q4 FY23's $849 million of reorganization and
  restructuring (against the $108 million), Q2 FY24's $93 million of incremental opioid settlement expense and Q3 FY24's year-ago $3,325 million.
  The $173 million Walmart Chile insurance settlement in Q2 FY23 stays in: the release states no change excluding it and the company's adjusted
  figures keep it. The full-year operating margins (EPS check only) stay as reported.
- **Loss quarters** (Q4 FY21, Q3 FY23) keep the statement's diluted shares (2,826M and 2,711M, equal to basic; display only) and reported EPS,
  with the adjusted figure in the note.
- **Dividends** with the 10-Ks (the LOW lag; no release states the rate): $2.20 a year from 2021-03-22, $2.24 from 2022-03-21, $2.28 from
  2023-03-20, with the fiscal year after the date elided in the note.
- **ECOMMERCE stays on the watch list** in each 10-K's words: competition with "local, regional, national and global physical, eCommerce and
  omni-channel retailers" (FY2021), joined by "companies that offer services in digital advertising, fulfillment and delivery services, health
  and wellness, and financial services" (FY2022) and "social commerce platforms" (FY2023). The offering side is each 10-K's eCommerce
  contribution to Walmart U.S. comps (about 5.4%, 0.7%, 0.7%). The FY2023 10-K calls Walmart "a people-led, technology-powered omni-channel
  retailer". GENAI (live 2022-11-30) and GLP1 (2023-08-08) are scoped to other businesses, and no Walmart filing of 2021-2023 names
  artificial intelligence, generative AI, GLP-1 drugs or weight-loss medication, so neither is recorded (the PEP GLP1 rule).
- **Adds nothing:** the 8-K of 2021-02-18 (17:09 ET) on the Asda sale, which estimates about $0.20 of FY22 EPS dilution without restating a
  range (the 2010-01-28 rule); the opioid, DEA and FTC statements and settlement 8-Ks (2021-02-05, 2021-11-23, 2022-06-28, 2022-08-17, the
  framework of 2022-11-15, 2022-12-20, 2023-08-22); the PhonePe separation (2022-12-23, reorganization expenses without an amount); the
  tender-offer and debt 8-Ks (2021-09-08, 2021-09-15, 2021-09-22, 2022-09-09, 2023-04-17); the officer, director, vote, bylaw and
  trading-plan 8-Ks (the 8-K and 8-K/A of 2021-01-15 and 2021-01-29, 2021-03-05, 2021-03-12, 2021-06-04, 2021-11-29, 2022-04-12, 2022-06-03,
  2022-08-17, 2022-11-16, 2023-02-24, 2023-03-06, 2023-03-24, 2023-06-02, 2023-08-16); and the 10-Qs.
- **Builder changes (the 679 dates of 2008-2020 rebuild byte-identical):** `eps_growth` (with `eps_growth_note`), `sales_basis` on a quarter
  guide, and the converted-guide fields with their re-derivation (`check_guide`). The firewall's WMT plant gains a later EPS guide stated as
  growth, a quarter guide's basis and the converted-guide fields.

Controls: altering one value of each new print (comparable sales, its currency effect, each operating one-off, each Q4 full-year EPS), guide
(each EPS range or growth rate, net sales range or currency effect, quarter range, words), vintage (first-year EPS and shares, the dividend,
the "why") and ECOMMERCE event changes no date before its publication and changes the first weekly date on or after it (95 of 95 new controls;
364 in all). A scan of all 835 WMT models for the figures, notes, guides and texts of every print, guide, vintage and event finds none before
its first publication, or before the first publication of a longer text containing it (0 of 291,017); `retro_tool run` validates all 156
dates with no warning.

Seen in the build (method behaviour, not tuned):
- **RICH on all 156 dates, robustness 8 of 8 on every one.** The model tier is AVOID on 149 and WATCHLIST on the seven dates from 2022-05-18
  to 2022-07-08 ($118-125, after the Q1 FY23 print). The price runs $129-150 in 2021, $118-157 in 2022 and $137-166 in 2023 (as traded,
  before the 2024 split); on guided EPS that is 21.5-29.7x in 2021 (76th-100th percentile of its own window), 18.5-25.4x in 2022 (58th-96th)
  and 22.9-26.2x in 2023 (82nd-97th). Ratio B is infinite (the price over the BULL price) on 65 dates; its lowest reading is 1.12 (2022-06-17).
- **The floor rises with the window and stays far below the price.** The EPP floor is 14x in 2021 ($69-90), 15x in 2022 ($85-97) and 16x in 2023
  ($96-103), as the 2011 and 2012 lows (10.7x, 11.4x) leave the window and the 18.8-19.9x lows of 2019-2022 join it; the price sits 23-112% above it.
- **The anchor:** FY20's $4.93 to 2021-02-12 (the FY21 withdrawal), FY21's $5.48 to 2021-08-13, then $6.275 and $6.40; FY23 FY22's $6.46,
  $6.40, $5.68, $5.81 and $6.04; FY24 $5.975, $6.15, $6.41 and $6.44.
- **BEAR is -9.5%/yr** (FY16 under FY15) at the 10th-percentile P/E (12.4-15.1x): $50-80. BULL sits at BASE's rate on every date (the decade
  CAGR stays below it). XBULL is +10.9% (fiscal 2011-2013) to 2021-03-19, then the fiscal 2017-2019 run (+6.6%, raised to BASE's rate while
  BASE exceeds it), and +14.5% (fiscal 2020-2022) from the Q4 FY22 print.
- **BASE** is +9.0%/yr in January 2021, +10.2% on Q4 FY21's +7.6% at constant currency, +4.1% and +2.7% on the divestiture quarters (+1.9%,
  +0.5%), +5.3% on Q3 FY22, +5.1-6.1% on the FY23 guides, +10.3% on the July 2022 quarter guide, +8.0% and +6.0% on the Q3 and Q4 FY23 guides,
  +6.8-6.9%, +6.1% and +5.1% on the FY24 quarter guides and +7.3% on the FY24 guide (each with 2.0-2.8% of buyback).
- **The proxy composite** runs 1.55-2.60 and the market composite 2.96-3.93, so the adjusted gap runs from -2.24 to -1.25, past RICH's
  -0.50 line on every date.

How far each call moves the classes (the 156 dates rebuilt with one encoding changed and classified offline; no outcome consulted):
- reported EPS for FY14-FY23 in the history, with the FY22 GAAP point ("around $5.00") and the adjusted guides elsewhere: 12 classes (RICH to
  FAIR on 2023-02-22 to 2023-03-24, 2023-05-26 and 2023-11-17 to 2023-12-22; the adjusted gap reaches +0.07) and 19 tiers;
- the figures excluding divestitures as the guides (FY22 net sales +6-7%; FY23 net sales and EPS growth ex-divestitures): no class, 3 tiers
  (2022-05-27 to 2022-07-15); the FY22 figure alone: nothing;
- the FY23 EPS growth guides read as words (FY22's $6.46 standing all year): no class, 9 tiers (2022-06-17 and 2022-07-29 to 2022-10-14,
  AVOID to WATCHLIST);
- nothing moves with the reported guides left unconverted, the quarter guides ignored (the fiscal-year guide instead), operating margins as
  reported, or every signal at its BEAR value (-2.84 to -1.68).

Judgement calls that could carry hindsight (in addition to the earlier lists, which stand):
- the company's adjusted EPS for FY21-FY23 and the adjusted FY22 and FY24 ranges (12 classes move at reported EPS, all in 2023);
- the figures excluding divestitures as display only, the measure keeping divestitures in (no class moves);
- an EPS growth rate read as a guide on the prior year's adjusted EPS (no class moves);
- a reported net sales guide converted only where the same filing states the guided period's currency effect (no class moves either way);
- the Walmart Chile insurance benefit left in Q2 FY23's operating margin (no class moves with every margin as reported);
- GENAI and GLP1 left off the watch list for want of a Walmart filing that names them (label only).

### WMT 2024-2026: the three-for-one split, quarter guides in constant currency, Nasdaq, the Total U.S. comp leaves the filings

```bash
python3 retro/build_wmt.py --weekly 2024-01-01 2026-11-06                   # 149 dates, 2024-01-05 .. 2026-11-06
for c in 2024-01-31 2024-02-20 2024-02-26 2024-03-18 2024-08-15 2025-01-01 2025-02-20 2025-03-17 2025-11-20 2025-12-09 \
         2026-02-19 2026-03-16 2026-05-21 2026-08-20 2026-11-07; do python3 retro/tools/firewall.py $c WMT; done
```

Every 8-K, 10-Q and 10-K of January 2024 to November 2026 was read (51 filings: 38 8-Ks and two 8-K/As, 8 10-Qs, 3 10-Ks), directly,
with no delegated transcription; the 10-Qs were searched for guidance and carry none. The records are generated by script from the
transcribed raw figures; 472 more strings were checked with `verbatim.py` (2,985 in all), every quoted fragment of the new notes among
them. Thresholds (rule T), signals and the engine are unchanged. Decided on 2026-11-08, before any 2024-2026 date was scored:

- **The end of the range is 2026-11-06,** the last complete week (built on Sunday 2026-11-08 from a price cache fetched that day, whose
  last bar is Friday's close). The Q3 FY27 release (due in mid-November) is after it. The newest dates have no two-year outcome yet.
- **The three-for-one split** (the SHW 2021 encoding, the sheet's first `splits` record). The 8-K of 2024-01-30 (17:40 ET, after the
  close, so published 2024-01-31) announces it; trading on the new basis starts 2024-02-26, the effective date, which matches the price
  data. Until then the models stay on the old basis (the price as traded is Yahoo's split-adjusted close times three); from it every
  per-share fact published before it is divided by three (the EPS history, the guides, the dividend) and share counts are multiplied by
  three. The Q4 FY24 release (2024-02-20) guides on both bases ("$6.70 to $7.12 pre-split; $2.23 to $2.37 post-split"); the pre-split range
  is the guide, published before the split, and the builder's division gives $2.233-2.373. The P/E percentiles run continuously across it
  (the median is 20.2x on 2024-02-21 and 20.3x on 2024-03-01).
- **Three 10-K vintages, Item 6 reserved.** The FY2024 10-K (accepted 2024-03-15 16:54 ET, dated Monday 2024-03-18), FY2025 (2025-03-14
  16:40 ET, dated 2025-03-17) and FY2026 (2026-03-13 16:06 ET, dated 2026-03-16) move the history to fiscal 2015-2024, 2016-2025 and
  2017-2026, each with its three income-statement years and earlier years from the latest 10-K that reports them. Years taken from
  filings published before the split keep their own dates (`eps_published`, `shares_published`), so the builder divides only those.
  First-year diluted shares: 2015's 3,243M (FY2017 10-K), 2016's 3,217M (FY2018 10-K), 2017's 3,112M (FY2019 10-K), each pre-split.
- **EPS: the company's adjusted figure, each year, from the latest release that publishes it:** FY24 $6.65 before the split (reported
  $1.91 after it; the Q4 FY24 release, published before the split, and then $2.22 in the Q4 FY25 release), FY25 $2.51 (reported $2.41), FY26
  $2.64 (reported $2.73: net gains on equity investments, $722 million of incremental non-cash share-based compensation, legal matters,
  reorganization). FY22 and FY23 keep $6.46 and $6.29 from releases published before the split: no later release repeats them. No year is
  excluded.
- **Guides, all in numbers and at constant currency:** the next quarter's net sales and adjusted EPS (except Q4 of each year and Q2 FY26's
  EPS) and the fiscal year's: FY25 +3.0-4.0% and $6.70-7.12 pre-split, then +3.75-4.75% and $2.35-2.43, then +4.8-5.1% and $2.42-2.47; FY26
  +3.0-4.0% and $2.50-2.60, +3.75-4.75% and $2.52-2.62, +4.8-5.1% and $2.58-2.63; FY27 +3.5-4.5% and $2.75-2.85, then +4.0-5.0% and
  $2.80-2.87. The Q1 FY25 update, "High-end or slightly above original guidance", is words (`fy_words`; the ranges stand), and the Q1 FY26
  and Q1 FY27 tables say "Unchanged" (the ranges stand). The next-quarter net sales guide is method r2's first choice and feeds BASE on every
  date but those after a Q3 print, which take the fiscal-year guide. The leap-year and VIZIO effects the guides state are in the notes.
- **Operating one-offs, release by release** (the 2015-2017 rule, from each release's adjusted operating income): Q4 FY24's year-ago
  $849 million; Q1 FY25's $255 million of reorganization (and Q1 FY26's year-ago); Q2 FY25's year-ago $93 million; Q4 FY25's $99 million
  opioid-related legal benefit (a benefit, so the margin is lower without it; and Q4 FY26's year-ago); Q2 FY26's $440 million of legal
  matters and $150 million of reorganization (and Q2 FY27's year-ago); Q3 FY26's $722 million of incremental share-based compensation net
  of a $155 million legal reversal; Q1 FY27's $181 million of reorganization.
- **The Total U.S. comparable sales figure leaves the filings.** From the Q4 FY26 release (2026-02-19) the comparable sales table gives
  Walmart U.S. and Sam's Club U.S. only, and the FY2026 10-K and the 10-Qs give no Total U.S. figure either. The AAPL Mac-unit rule applies
  (as for NIKE's futures and PepsiCo's servings): the signal keeps its name, thresholds and weight and scores BASE with no value ("n/r"),
  and no other measure replaces it (Walmart U.S. is a segment, a different measure); the note keeps the segment rows. The franchise line
  says the FY2026 10-K gives no Total U.S. figure (a builder change, text only). The Q4 FY25 comp (+4.7%) compares 14 weeks with 13, as
  published.
- **Nasdaq** (the PEP 2017 encoding, `listings`; display only). The 8-K of 2025-11-20 (06:58 ET, Item 3.01) moves the listing: NYSE trading
  ends at the close of 2025-12-08 and Nasdaq trading begins 2025-12-09, so the models say Nasdaq from 2025-12-12.
- **A renamed reporting line:** Sam's Club U.S. from the Q4 FY25 release (2025-02-20), the first whose segment table uses it (the ACN rule).
- **Dividends:** $0.83 a year from the FY2024 10-K (2024-03-18; the Q4 FY24 release says only "raises annual dividend 9%"), $0.94 from the
  FY2025 10-K, and $0.99 from the Q4 FY26 release (2026-02-19), the first release of the series to state a rate ("Increased annual dividend
  to $0.99 per share"; the FY14 precedent), repeated by the FY2026 10-K. The FY2023 vintage's $2.28 becomes $0.76 at the split.
- **ECOMMERCE stays on the watch list** in each 10-K's words; the FY2026 10-K adds "emerging agentic shopping tools and platforms" to the
  competitors and "more rapid development of AI capabilities and agentic tools by these competitors" to the risk. GENAI's registered
  scope (software seats, IT services, BPO, professional information, search, education, mobility) does not name retail, and its dated
  evidence names no retailer, so GENAI is not recorded; the words stay in the ECOMMERCE quote. The FY2025 and FY2026 10-Ks name AI as
  Walmart's own investment (the offering side, text only). No filing names GLP-1 drugs or weight-loss medication.
- **Adds nothing:** the 8-K of 2024-02-23 (the certificate of amendment), the investment-community 8-K of 2025-04-09 (the Q1 and FY26
  outlook "remains unchanged", in words), the CEO succession (2025-11-14 and the 8-K/A of 2026-01-16), the other officer, director, vote,
  charter and trading-plan 8-Ks, the derivative-settlement notice (2024-10-18), the debt 8-Ks (2025-04-28, 2026-04-30, 2026-10-23) and the
  10-Qs.
- **Builder changes (the 835 dates of 2008-2023 rebuild byte-identical):** `listings`, the split note in the EPS comment, and the franchise
  line for a year with no Total U.S. comparable sales figure. The firewall's generic plant already covers a later split and a later listing.

Controls: altering one value of each new print (comparable sales or, when not reported, its note; its currency effect; each operating
one-off; each Q4 full-year EPS), guide (each EPS and net sales range, quarter range, words), vintage (first-year EPS and shares, the dividend,
the "why"), ECOMMERCE event, the split, the listing, the dividend of 2026-02-19 and the rename changes no date before its publication (or
effective date) and changes the first weekly date on or after it (92 of 92 new controls; 456 in all). A scan of all 984 WMT models for the
figures, notes, guides and texts of every print, guide, vintage, event, split, listing and dividend finds none before its first publication
(0 of 410,516); `retro_tool run` validates all 149 dates with no warning.

Seen in the build (method behaviour, not tuned):
- **RICH and AVOID on all 149 dates, robustness 8 of 8 on every one.** The price runs $157-174 before the split and $59-96 after it in
  2024, $83-117 in 2025 and $103-134 in 2026; on guided EPS that is 24.3-39.1x in 2024 (91st-100th percentile of its own window),
  32.6-44.8x in 2025 (96th-100th) and 36.4-51.4x in 2026 (85th-100th). Ratio B is infinite on 140 dates; its lowest reading is 6.79
  (2024-01-05).
- **The floor rises to 18-19x and the price stays 35-171% above it.** The EPP floor is 18x to the end of 2025 and 19x in 2026 ($116-124
  before the split, $41-54 after it), as the 12-15x lows of 2014-2016 leave the window and the 19-36x lows of 2019-2026 join it (2025's
  low was 31-32x and 2026's 36x).
- **The anchor:** FY24 $6.44 to 2024-02-16; FY25 $6.91 on 2024-02-21, $2.303 from the split, then $2.39 and $2.445; FY26 $2.55, $2.57 and
  $2.605; FY27 $2.80 and $2.835.
- **BEAR** is -9.5%/yr (FY16) to 2025-03-14, -5.9% (FY17) from the FY2025 vintage and -2.6% (FY23) from the FY2026 vintage, at the
  10th-percentile P/E (15.1-17.8x): $80-86 before the split and $29-48 after it. BULL is BASE's rate until the FY2025 vintage and the decade CAGR above it on 42
  dates (+7.0% from the FY2026 vintage). XBULL stays +14.5% (fiscal 2020-2022) throughout.
- **BASE** is +5.1% to +7.3%/yr: the quarter guides of +3.0% to +5.0% at constant currency and the fiscal-year guides after the Q3 prints,
  plus 1.7-2.1% of buyback.
- **The proxy composite** runs 1.70-2.55 and the market composite 3.75-3.93, so the adjusted gap runs from -2.43 to -1.33.

How far each call moves the classes (the 149 dates rebuilt with one encoding changed and classified offline; no outcome consulted):
- reported EPS in the history (each year on the basis of the filing that reports it) with the adjusted guides: 8 classes (RICH to FAIR on
  the seven dates to 2024-02-16 and to CHEAP on 2024-02-21) and 8 tiers, all before the FY2024 vintage;
- nothing moves with Walmart U.S. comparable sales in place of the missing Total U.S. figure, the quarter guides ignored (the fiscal-year
  guides instead), operating margins as reported, or every signal at its BEAR value (-2.98 to -2.54).

Judgement calls that could carry hindsight (in addition to the earlier lists, which stand):
- the company's adjusted EPS for FY24-FY26 (8 classes move at reported EPS, all in early 2024);
- the missing Total U.S. comparable sales scored BASE rather than replaced by Walmart U.S. (no class moves either way);
- GENAI left off the watch list although the FY2026 10-K names agentic shopping tools among its competitors, for want of a registered scope
  that covers retail (label only);
- the pre-split FY25 guide used on its own basis and divided at the split, rather than the rounded post-split range the release also gives
  (a third of a cent).

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
  name "growing competition from online and multi-channel retailers" ("LOW 2015-2016"). It stays there after the
  theme's market-pricing date (2017-06-16, a grocers' sell-off): no dated evidence shows the market pricing it for
  Lowe's ("LOW 2017-2018", "LOW 2019-2020", "LOW 2021-2023", "LOW 2024-2026").
  AAPL in 2008 carries none: no theme in the registry is live for a personal-computer and consumer-electronics maker
  (CLOUD from 2012-10-30; OFFSHORE is scoped to IT services), so its watch list is empty ("AAPL"). It stays empty through 2026:
  CLOUD's scope is on-premise enterprise IT, STREAMING's linear TV and ECOMMERCE's physical retail, and Apple's FY2012-FY2019
  10-Ks name cloud and streaming only as its own services ("AAPL 2012-2015", "AAPL 2016-2019"); GENAI's scope (from 2022-11-30),
  EV's, CRYPTO's and GLP1's name none of Apple's products ("AAPL 2020-2023"), and the FY2024 and FY2025 10-Ks name artificial
  intelligence only as Apple's own features and their risks ("AAPL 2024-2026").
  NKE in 2008-2014 carries none either: no theme in the registry is live for an athletic footwear and apparel brand (ECOMMERCE
  from 2015-01-01, scoped to physical retail; OFFSHORE to IT services), so its watch list is empty ("NKE", "NKE 2009-2011",
  "NKE 2012-2014"). Its FY2015 and FY2016 10-Ks name e-commerce only as NIKE's own channel, so the list stays empty; from its
  FY2017 10-K (2017-07-21), the first whose risk factors name "the rising trend of digital commerce" as "a risk factor
  implicating our DTC and wholesale operations", NKE carries ECOMMERCE on the watch list, company-acknowledged, with no market
  read ("NKE 2015-2017"). The FY2018 and FY2019 10-Ks repeat the sentence (for "our NIKE Direct and wholesale operations") and
  the FY2020-FY2023 10-Ks name "the continued proliferation of digital commerce", so it stays there through 2023 ("NKE 2018-2020",
  "NKE 2021-2023"). The FY2024-FY2026 10-Ks drop that phrase but say NIKE Direct competes "with digital commerce platforms" and
  keep "shifts in the ways in which consumers shop" as a risk factor, so it stays there through 2026, a judgement call
  ("NKE 2024-2026").
  AVGO in 2009-2015 carries none: no theme in the registry is live for an analog semiconductor maker (CLOUD from 2012-10-30, scoped
  to on-premise IT; OFFSHORE to IT services; GENAI from 2022-11-30), and its FY2012-FY2015 10-Ks name cloud only for their own IT
  service providers, so its watch list is empty ("AVGO", "AVGO 2010-2012"). From the FY2016 10-K of Broadcom Limited (2016-12-23),
  the first whose risk factors name "the shift to cloud-based IT solutions and services, such as hyperscale computing" as a risk to
  its wired infrastructure and enterprise storage segments, AVGO carries CLOUD on the watch list, company-acknowledged, with no
  market read ("AVGO 2013-2016"). The FY2017 10-K repeats that sentence and the FY2018-FY2020 10-Ks of Broadcom Inc. name the shift
  as affecting sales "for use in traditional enterprise data centers", so it stays there through 2020; EV and CRYPTO, live from
  2020, are scoped to other industries ("AVGO 2017-2020"). The FY2021-FY2023 10-Ks repeat that sentence, so it stays there through
  2023. GENAI, live from 2022-11-30, stays off the list: its scope names none of Broadcom's products, and the FY2022 and FY2023 10-Ks
  name AI only as features of its own products and in one regulatory risk, never as a substitute for them ("AVGO 2021-2023").
  The FY2024 and FY2025 10-Ks keep the cloud risk (sales "for use in traditional enterprise data centers", then "for use in enterprise
  data centers"), so CLOUD stays through 2026; they name AI as Broadcom's own market, a possibly unsustainable upturn, a source of
  cyber attacks and a reason for new business models, never as a substitute, so GENAI stays off ("AVGO 2024-2026").
  PEP in 2008 carries none: no theme in the registry is live for a beverage and convenient-food company (GLP1, whose scope names
  snacks and beverages, from 2023-08-08; ECOMMERCE is scoped to physical retail, OFFSHORE to IT services), so its watch list is
  empty ("PEP"). Its FY2006 and FY2007 10-Ks name "consumer health concerns about obesity" as a risk, which no theme in the registry
  covers before GLP1; the wording stays in the durability "why". The list stays empty through 2017: the FY2014-FY2016 10-Ks name e-commerce
  only among the channels larger retailers might use. From the FY2017 10-K (2018-02-14), the first whose risk-factor heading names
  "disruption in the retail landscape, including rapid growth in hard discounters and the e-commerce channel" as a risk to its business,
  PEP carries ECOMMERCE on the watch list, company-acknowledged, with no market read (the NKE and LOW rule); the FY2018 and FY2019 10-Ks
  keep the heading, so it stays there through 2020. EV and CRYPTO, live from 2020, are scoped to other industries ("PEP 2017-2020").
  The FY2020-FY2022 10-Ks move the risk into the body of a risk factor on the retail landscape ("Our business can be adversely affected if
  e-commerce channels and hard discounters take significant additional market share away from traditional retailers"), so it stays
  there through 2023. GLP1, live from 2023-08-08 and scoped to snacks and beverages, stays off the list: no PepsiCo filing to the Q3 2023
  10-Q names GLP-1 drugs, and the theme's dated evidence is a sector-wide sell-off that names no company, as ECOMMERCE's grocers' sell-off
  of 2017-06-16 left PEP's list empty until its FY2017 10-K; GENAI names none of PepsiCo's products ("PEP 2021-2023").
  From the FY2023 10-K (2024-02-09), whose risk factors name "the use of weight-loss drugs" among the shifts in diet that can reduce
  demand for PepsiCo's products ("such as GLP-1 medications" from the FY2025 10-K), PEP also carries GLP1 on the watch list,
  company-acknowledged, with no market read; the theme signal stays with ECOMMERCE (the ACN CLOUD rule). The FY2025 10-K's "artificial
  intelligence shopping agents" are a channel, not a substitute for PepsiCo's products, so GENAI stays off ("PEP 2024-2026").
  MSFT in 2008 carries none: no theme in the registry is live for a software maker (CLOUD from 2012-10-30, scoped to on-premise IT;
  OFFSHORE to IT services; GENAI from 2022-11-30), so its watch list is empty ("MSFT"). Its FY2007 and FY2008 10-Ks name open source and
  "the software-as-a-service business model" (FY2008: revenues "primarily from advertising or subscriptions") as challenges to its
  license-based model, which no live theme covers; the wording stays in the durability "why" (the PEP obesity rule). The list stays
  empty through 2011: from the FY2010 10-K (2010-07-30) a risk factor is headed "The cloud-based computing model presents execution and
  competitive risks", but CLOUD is not live until 2012-10-30, so those words join the "why" too. Microsoft's FY2010 10-K is an earlier
  verified filing of the risk than the registry's basis (Accenture's FY2012 10-K); whether to move CLOUD's date is left to the owner
  ("MSFT 2009-2011"). From 2012-11-02, the first weekly date on or after CLOUD's live date, MSFT carries CLOUD on the watch list,
  company-acknowledged, with no market read, in the latest 10-K's own words: the FY2012 10-K's "Our increasing focus on devices and
  services presents execution and competitive risks" (its competitors "rapidly developing and deploying cloud-based services"), then the
  FY2013 and FY2014 10-Ks' "Our increasing focus on services" (whose costs "will reduce the operating margins" in FY2014). The theme's
  market-pricing date (2015-04-23) lies after 2014, so DURABLE stands ("MSFT 2012-2014"). It stays on the list through 2017 in the
  FY2015-FY2017 10-Ks' words (from 2017-08-04 the FY2017 10-K's, kept by the recast vintage): the market-pricing date passes, but no
  dated evidence shows the market pricing cloud substitution of Microsoft's licensed software, so DURABLE stands ("MSFT 2015-2017").
  The FY2018-FY2020 10-Ks head the risk factor "Our increasing focus on cloud-based services presents execution and competitive risks";
  the status is unchanged through 2020 ("MSFT 2018-2020"). The FY2021-FY2023 10-Ks keep it, so CLOUD stays there through 2023. GENAI,
  live from 2022-11-30 and scoped to software seats and search, stays off the list until the FY2023 10-K (2023-07-28): the FY2021 and
  FY2022 10-Ks and the 10-Qs to Q3 FY23 name AI only as Microsoft's own offerings and their risks, and the FY2023 10-K is the first to
  name "AI technology and services" as "a highly competitive and rapidly evolving market" and competitors "using open source AI models"
  among the business models Microsoft competes with. From 2023-08-04 MSFT carries GENAI on the watch list as well, company-acknowledged,
  with no market read; the theme signal stays with CLOUD (the ACN CLOUD rule) ("MSFT 2021-2023"). The FY2024-FY2026 10-Ks keep both, the
  cloud competitor sentence now inside "Business model competition" beside the AI one, so CLOUD and GENAI stay on the list through 2026;
  no dated evidence shows the market pricing generative-AI substitution of Microsoft's software seats or search, so neither is re-filed
  ("MSFT 2024-2026").
  XOM in 2008 carries none: no theme in the registry is live for an oil and gas producer (ENERGY_TRANSITION, scoped to oil, gas, coal and
  refining, from 2015-12-12; OFFSHORE to IT services), so its watch list is empty ("XOM"). Its FY2006 and FY2007 10-Ks list "the
  competitiveness of alternative hydrocarbon or other energy sources" and laws "addressing alternative energy sources and the risks of global
  climate change" among the factors behind its results, which no live theme covers; the wording stays in the durability "why" (the PEP
  obesity rule). XOM is also the first ticker filed CYCLICAL rather than DURABLE, on the 10-K's own "fundamentally a commodity business".
  The list stays empty through 2012: from the FY2009 10-K (2010-03-01) a risk factor headed "Climate change and greenhouse gas
  restrictions" says such rules could "reduce demand for hydrocarbons", but ENERGY_TRANSITION is not live until 2015-12-12, so those words
  join the "why" too; XOM's FY2009 10-K is an earlier verified filing of the risk than the registry's basis, and whether to move the date is
  left to the owner ("XOM 2009-2012"). From 2015-12-18, the first weekly date on or after ENERGY_TRANSITION's live date, XOM carries
  it on the watch list, company-acknowledged, with no market read, in the latest 10-K's own words (the MSFT CLOUD rule): the FY2014
  10-K's climate-change risk factor, then the FY2015 and FY2016 10-Ks', which repeat it. The theme's market-pricing date (2020-08-31)
  lies after 2017 and no dated evidence shows the market pricing decarbonisation of ExxonMobil's reserves, so CYCLICAL stands
  ("XOM 2013-2017"). It stays on the watch list in the FY2017-FY2019 10-Ks' words until the theme's registered market-pricing event,
  ExxonMobil's removal from the Dow Jones Industrial Average (announced 2020-08-24, effective 2020-08-31): from 2020-09-04 XOM is
  re-filed under DISRUPTION_EXPOSED (ENERGY_TRANSITION), risk 3, label only, with the announcement's own reason (Apple's stock split)
  quoted beside it ("XOM 2018-2020"). The re-file stands through 2023, in the FY2020-FY2022 10-Ks' words; EV, live from about 2020 and
  scoped to fuel retail among others, is not recorded: the stock is already filed under ENERGY_TRANSITION, and EV's evidence names
  automakers, not ExxonMobil ("XOM 2021-2023"). Both stand through 2026, in the FY2023-FY2025 10-Ks' words ("XOM 2024-2026").
  SHW in 2008 carries none: no theme in the registry is live for a paint and coatings maker (ECOMMERCE, scoped to physical retail,
  from 2015-01-01; OFFSHORE to IT services), so its watch list is empty ("SHW"). Its FY2006 and FY2007 10-Ks say portions of the
  business sell to "segments of the economy that are cyclical in nature, particularly segments relating to construction, housing and
  manufacturing"; that is a cycle, not a disruption theme, and the wording stays in the durability "why", which files SHW DURABLE (the
  LOW precedent) rather than CYCLICAL. The list stays empty through 2011, and the FY2008-FY2010 10-Ks repeat the sentence ("SHW 2009-2011");
  it stays empty through 2014, and the FY2011-FY2013 10-Ks repeat it again ("SHW 2012-2014"). It stays empty through 2017: ECOMMERCE (from
  2015-01-01) is scoped to physical retail and the FY2014-FY2016 10-Ks name no e-commerce, online or internet competition; ENERGY_TRANSITION
  (from 2015-12-12) is scoped to oil, gas, coal and refining, and the FY2015 and FY2016 10-Ks name "oil production, refining, storage and
  transportation" only among the cyclical segments Sherwin-Williams sells to, words that join the "why" ("SHW 2015-2017"). It stays
  empty through 2020: the FY2017-FY2019 10-Ks name no e-commerce or online competition, and EV and CRYPTO, live from 2020, are scoped to
  other industries ("SHW 2018-2020") It stays empty
  through 2023: GENAI (from 2022-11-30) is scoped to software, IT services, information and education, and the FY2020-FY2022 10-Ks use
  "online" only for COVID-era ordering and employee training ("SHW 2021-2023") It stays empty through 2026: the FY2024 and FY2025 10-Ks
  name artificial intelligence only as a risk to intellectual-property protection and cybersecurity, not as a substitute for paint and
  coatings, and GENAI is scoped to software, IT services, information and education ("SHW 2024-2026").
  WMT in 2008 carries none: no theme in the registry is live for a discount retailer (ECOMMERCE, scoped to physical retail, from
  2015-01-01; OFFSHORE to IT services), so its watch list is empty ("WMT"). Its FY2007 and FY2008 10-Ks name "internet-based
  retailers and catalog businesses" among every segment's competitors in their risk factors; ECOMMERCE is not live, so the words
  stay in the durability "why" (the PEP obesity rule), and whether this earlier filing should move ECOMMERCE's live date is left to
  the owner (the MSFT and XOM precedent). The list stays empty through 2011: ECOMMERCE is not live until 2015-01-01, and the FY2009-FY2011
  10-Ks repeat the "internet-based retailers and catalog businesses" wording, which stays in the "why" ("WMT 2009-2011"). It stays
  empty through 2014: the FY2012 and FY2013 10-Ks repeat that wording, and the FY2014 10-K's competition "whether through physical
  retail, e-commerce retail or through a combination of both areas" stays in the "why" too, ECOMMERCE not being live before 2015-01-01.
  ECOMMERCE's scope (physical retail) covers Walmart, so a 2015 batch must decide when it joins the watch list (the LOW FY2015 10-K
  rule: company-acknowledged, no market read; here the acknowledgement predates the live date) ("WMT 2012-2014"). From 2015-01-09, the
  first weekly date on or after ECOMMERCE's live date, WMT carries it on the watch list, company-acknowledged, with no market read, in the
  latest 10-K's own words (the MSFT CLOUD and XOM rule): the FY2014 10-K's competition "whether through physical retail, e-commerce retail
  or through a combination of both areas", then the FY2015-FY2017 10-Ks' "digital retail". The theme's market-pricing date (2017-06-16, a
  grocers' sell-off) passes, but its evidence names no company and no other dated evidence shows the market pricing online substitution of
  Walmart's store sales, so DURABLE stands through 2017 (the LOW and PEP reading; "WMT 2015-2017"). It stays on the watch list through
  2020 in the FY2018 10-K's "digital retail" heading, then the FY2019 and FY2020 10-Ks' competition with "global eCommerce and omni-channel
  retailers"; EV (scoped to fuel retail among others) and CRYPTO, live from 2020, are not recorded, as no Walmart filing names them as a
  risk ("WMT 2018-2020").

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
