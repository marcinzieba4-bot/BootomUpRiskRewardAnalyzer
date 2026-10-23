# Retrospective (point-in-time) analyses

Build a history of what the house model *would have said* on a past date, using only
what was public on that date, then score it against what actually happened.

```
retro/
  retro_tool.py          run / outcome / lint / index
  taxonomy_eras.json     era-aware durability themes + anachronism list
archive/retrospective/
  index.json             one row per retrospective (outcome = hindsight, filled separately)
  <TICKER>/<AS_OF>/
    model.py             the signal model, house 6-section format, methodology v2
    report.txt           its printed report
    analysis.json        point-in-time classification, metrics, robustness, sources
    outcome.json         HINDSIGHT: +6m/+1y/+2y/+3y vs SPY and the 15%/yr hurdle
```

## Point-in-time rules

`retro_tool.py run` refuses to write anything unless all of these hold:

1. **Sources.** Every number in `model.py` traces to a `SOURCES` entry whose
   `published` date is on or before `AS_OF`. Use filings (8-K, 10-Q, 10-K, XBRL
   facts filed by then), the company's own guidance, and dated news. Never use
   consensus you can't date, restated figures, or "current" pages without a
   vintage.
2. **No anachronisms.** No term in `taxonomy_eras.json → anachronisms` whose
   `first_seen` is after `AS_OF` (for example *agentic*, *DOGE*, *Agentforce* in a 2023
   analysis), and no ISO date after `AS_OF`. Calendar years after `AS_OF` outside
   `FY2025`/`FY25E` labels raise a warning.
3. **An era-legal category** (see below).
4. **The real price.** `CURRENT_PRICE` must match the actual close on `PRICE_DATE`
   (Yahoo, ±0.5%).

Hindsight leaks that a linter can't see (scenario assumptions that happen to
match what followed) are handled by method, not trust:

- **Scenario multiples are mechanical.** They are percentiles of the stock's own P/E
  on current-fiscal-year EPS over the 10 years before `AS_OF`: BEAR = p10,
  BASE = median, BULL = p75, XBULL = p90. The EPP P/E is the median of the
  panic troughs in the same window.
- **The valuation structural factor is mechanical too.** It is scored from where
  today's P/E sits in that 10-year distribution: −0.5 at the 80th percentile or
  above, 0 at the median, +0.5 at the 20th or below (`VALUATION_SCORE`).
- **Scenario EPS comes from guidance and history.** It starts from company guidance
  and the reported growth history, cross-checked by the segment bridge.
- **The ⑦ robustness block** re-runs the verdict with one input moved at a time.
  A class that survives only one set of assumptions is not a call.
- **Outcomes are written after the analysis.** `outcome.json` is produced by a
  separate command and `run` never reads it.

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

What the gates enforce:

- **Before `live_from`.** The theme cannot be assigned, and it cannot even sit on
  the `theme_watch` list. A 2016 analysis that mentions GenAI fails.
- **On or after `live_from`.** The theme still needs dated evidence that the
  market was pricing it *for this company* (`PIT_PROFILE.evidence`). A theme that
  is live but where the stock is priced as a beneficiary stays on `theme_watch`.
  That was ACN in June 2023: AI was live, but ACN traded at a premium, not an AI
  discount.
- **Themes that fizzled stay in the registry** (CRYPTO, ENERGY_TRANSITION). A
  registry of only the themes that later mattered would itself be hindsight.
- **What this means by depth.** For shallow dates (late 2025 on), the categories
  are today's, but each ticker's kind must still be re-earned from evidence dated
  by then. For mid-depth dates (2023 to 2024), AI is live but mostly a watch item.
  For deep dates (2016 and earlier), the disruption slot belongs to cloud,
  Amazon, streaming or the energy transition, and `AI_EXPOSED` is illegal.

## Workflow

```bash
mkdir -p archive/retrospective/XYZ/2019-03-29          # pick a trading day
cp archive/retrospective/ACN/2023-06-30/model.py archive/retrospective/XYZ/2019-03-29/
# rewrite every constant from point-in-time sources; update SOURCES and PIT_PROFILE
python3 retro/retro_tool.py lint    archive/retrospective/XYZ/2019-03-29
python3 retro/retro_tool.py run     archive/retrospective/XYZ/2019-03-29
python3 retro/retro_tool.py outcome archive/retrospective/XYZ/2019-03-29   # hindsight, last
python3 retro/retro_tool.py series  XYZ                                     # table -> archive/retrospective/XYZ/SERIES.md
```

When copying a model forward, rewrite it. Don't edit only the numbers: the
lint exists because narrative text is where hindsight leaks first.

**Weekly series: picking the dates.** Use one date per week, normally that
week's Friday close (or the last trading day if Friday is a holiday). In an
earnings week, use the first close *after* the release, so the print and the
market's reaction are both in the information set.

- **Copying across an earnings date.** When you copy a model from after the print
  to a date before it, remove every fact the print introduced: its sources,
  quarter figures, the new guidance and the narrative built on them.
- **Grep before running.** Search the copy for the print's tell-tale numbers before
  `run`. The lint only sees dates and terms, not numbers.
- **Example:** `ACN/2023-06-02 … 06-30` runs three pre-print weeks on Q2 FY23 data
  and the March guide, and two post-print weeks on Q3 FY23.

Data sources that worked from the cloud session:

- **Prices and dividends:** the Yahoo chart API (`retro_tool` caches it in
  `retro/.cache/`).
- **EPS history with filing dates:** SEC XBRL company facts
  (`data.sec.gov/api/xbrl/companyfacts/CIK##########.json`). SEC asks for a
  `User-Agent` with a contact. Use a project or role address, not a personal one.
- **Quarterly detail:** the 8-K earnings exhibits listed in
  `data.sec.gov/submissions/CIK##########.json`.

## Which model to run it on

Pricing per million tokens, input / output (cached 2026-10-06): Haiku 5.5
$0.10 / $0.50, Sonnet 5.5 $2 / $10, Opus 5.5 $4 / $20, Fable 5.1 $10 / $50.

**Recommended: Claude Sonnet 5.5 (`claude-sonnet-5-5`) at effort `high`.** It is
the cheapest model that reliably does the whole loop: dated web and SEC research,
a ~500-line model in the house format, and the era judgement. The
judgement-heavy parts are fenced in by the validator and the mechanical
multiples, so the extra reasoning of Opus buys little on mid-depth dates. One
retrospective costs roughly 0.3–0.6M input and 30–50K output tokens, about
$1–2 on Sonnet 5.5 before caching (an estimate, not a measurement).

- **Opus 5.5:** use it for deep dates (before ~2018), where choosing the live theme
  and finding dated evidence is the hard part, and for reviewing a batch of
  retrospectives. The daily classification routine already uses Opus for the
  same kind of judgement.
- **Haiku 5.5:** not for the whole task. It can extract numbers from 8-K exhibits
  into a fact sheet if you orchestrate sub-agents, but era judgement and keeping
  hindsight out of narrative and assumptions need a stronger model.
- **No model is blind.** Every current model knows what happened after 2023.
  Picking a different model doesn't protect against look-ahead; the source
  ledger, the lint and the mechanical rules above do.
