# Retrospective (point-in-time) analyses

Build a history of what the house model *would have said* on a past date, using only
what was public on that date, then score it against what actually happened.

```
retro/
  facts/<TICKER>.json    dated fact sheet: every value carries a source and its publication date
  templates/             the frozen engine appended to every generated model
  build_acn.py           facts + prices truncated at AS_OF -> archive/.../<AS_OF>/model.py
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
| History | The latest annual history vintage published by AS_OF; only prints and events published since that vintage are in scope |
| Segment bridge | FY revenue from the FY guide; groups pro rata to the latest actuals; bear flat, bull at the decade revenue CAGR |

Fallbacks for facts a company did not publish (decided before any outcome of the affected dates was computed):

- **No next-quarter guide in local currency:** BASE growth and the growth factor use the full-year LC revenue guide.
  Example: ACN FY08 guided Q2 in dollars only.
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

Known limitation: the growth factor compares a local-currency guide with dollar revenue history. That penalizes
periods of a weak dollar, such as ACN in 2004–07. Fixing it needs LC history in the fact sheet and a new
method version.

The ⑦ robustness block re-runs the verdict with one input moved at a time; a class
that survives only one set of assumptions is not a call.

## Categories change with the era

The five base kinds (DURABLE, CYCLICAL, STRUCTURAL, TURNAROUND, SPECIAL) are
timeless. `AI_EXPOSED` is not: it is the current instance of a recurring
pattern, a franchise that is cheap because the market prices a substitution
story. A retrospective uses the kind `DISRUPTION_EXPOSED` plus the theme live
on its date, and the class names follow the theme:

| theme (label) | live from | first market pricing | class family |
|---|---|---|---|
| GENAI (AI) = today's `AI_EXPOSED` | 2022-11-30 | 2023-05-02 (Chegg) | AI-FEAR BASKET / AI-EXPOSED, … |
| CLOUD | ~2013 | 2015-04-23 (AWS disclosed) | CLOUD-FEAR BASKET / … |
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

## Workflow

```bash
# 1. add newly published facts to retro/facts/ACN.json (each with source + published date)
python3 retro/build_acn.py --weekly 2023-01-01 2023-06-30        # dates chosen by rule, models generated
python3 retro/build_acn.py --weekly 2008-01-01 2008-01-31        # any era with a history vintage in the fact sheet
python3 retro/build_acn.py --weekly 2008-05-05 2008-09-30        # start a range on a Monday when the prior week is built
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
