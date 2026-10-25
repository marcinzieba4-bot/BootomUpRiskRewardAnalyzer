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
for d in staging/retrospective/UNP/2008-*/; do
  python3 retro/retro_tool.py --archive staging/retrospective run "$d"
  python3 retro/retro_tool.py --archive staging/retrospective outcome "$d"
done
python3 retro/retro_tool.py --archive staging/retrospective series UNP
python3 retro/tools/firewall.py 2013-01-01 UNP
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
