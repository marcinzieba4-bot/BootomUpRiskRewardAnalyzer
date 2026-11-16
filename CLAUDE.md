# Notes for Claude sessions in this repo

## Retrospective (point-in-time) history: `retro/`, `archive/retrospective/`

The owner builds this history as training data. Its one rule: **never infer anything
from information that was not public before the as-of date.** You know what happened
later; the process exists to keep that knowledge out. Read `retro/README.md` before
touching either directory.

- **Facts:** enter only through `retro/facts/<TICKER>.json`, each with a source and
  its `published` date. Never type a number straight into a generated `model.py`.
- **Parameters:** derive them by the frozen method rules. Never carry assumptions
  from a later-dated analysis back to an earlier one. Never hand-tune per date.
- **Outcomes:** `outcome.json` and any pattern found in it are labels, not inputs.
  Don't fold outcome-derived rules into the archive. Changing a rule means a new
  method version and a full re-run, with the reason recorded.
- **Before you report a result:** run `retro/retro_tool.py run` (point-in-time
  validation) on every date you built. Grep earlier dates for facts from later
  prints. Say plainly which judgement calls remain and could carry hindsight.
- **Adding dates:** follow `retro/README.md`, "Adding dates" (tools in `retro/tools/`). Results so far,
  labelled as hindsight, are in `archive/retrospective/ACN/FINDINGS.md`; they are hypotheses, never inputs.
- **Tickers are separate.** Each has its own fact sheet, builder and engine; nothing from one ticker's facts,
  outcomes or findings enters another's models. UNP (2008-2026 so far), LOW (2008-2026 so far), AAPL (2008-2026 so far),
  NKE (2008-2026 so far), AVGO (from its 2009-08-06 listing to 2026-10-30 so far), PEP (2008 to 2026-10-30 so far), MSFT
  (2008 to 2026-10-30 so far), XOM (2008 to 2026-10-30 so far), SHW (2008 to 2026-11-06 so far), WMT (2008 to 2026-11-06 so far), RCL (2008 to 2026-11-06 so far), MAR (2008 to 2026-11-03 so far), BKR (2008 to 2017-06-30, then 2019-02-01 to 2026-11-06 so far), PFE (2008 to 2026-11-04 so far), CMCSA (2008 to 2026-11-06 so far), CAT (2008 to 2026-11-06 so far), BMY (2008 to 2026-11-06 so far), NVDA (2008 to 2026-11-06 so far), F (2008-01-04 to 2026-11-06 so far; 2022-01-07 onward was built first at the owner's request, and dates before 2022 are an early era with its
  own 1997-2006 rule-T thresholds, engine and records) SO (2008-01-04 to 2021-12-31 so far, at the owner's request) CTVA (from its 2019 listing: 2021-02-05 to 2026-09-25), KMI (from its 2011 listing: 2013-01-18 to 2026-11-13 so far) and LMT (2008-01-04 to 2013-12-31 so far) sit in `staging/retrospective/` until the owner adds
  them to the archive (retro/README.md, "UNP", "LOW", "AAPL", "NKE", "AVGO", "PEP", "MSFT", "XOM", "SHW", "WMT", "RCL", "MAR", "BKR", "PFE", "CMCSA", "CAT",
  "BMY", "NVDA", "F", "SO", "CTVA", "KMI", "LMT"). The live `nke_signal_model.py`, `avgo_*.py`, `msft_signal_model.py`, `rcl_signal_model.py`, `wmt_signal_model.py`, `mar_signal_model.py` and `bmy_signal_model.py` (other branches) and `cat_signal_model.py` files
  and today's profiles in `data/business_profiles.json` (NVDA's and SO's included) are 2026 analyses: never inputs to a retrospective. AVGO did not trade
  before its IPO, so its series starts at the listing (the listing and bounds rules of method r2). BKR's 2008 to 2017-06-30 dates are Baker
  Hughes Incorporated, listed as BHI: BKR is only the series key (and Yahoo's symbol for the history); the models print BHI. Its dates from
  2019-02-01 are Baker Hughes, a GE company (BHGE, then BKR), a new listing with its own facts and engine: no date between is built, as
  the new company had no full year of EPS before its Q4 2018 release (retro/README.md, "BKR 2018-2021"). SO's P/E windows to 2011-04-01 reach back before the
  2001 Mirant spin-off: by the `distributions` rule those days are priced as traded, with Mirant, against EPS that excludes it
  (retro/README.md, "SO"; the largest call of the series). CTVA (Corteva) has no 2008-2009 dates: neither the company (formed 2018) nor its stock
  (listed 2019-06-03) existed, and DuPont's or Dow's history was not substituted. From the listing its EPS is GAAP (Operating EPS removes
  recurring amortization), so no date precedes the first full year (FY2020, released 2021-02-03), and none follows the 2026-10-01
  reverse spin-off of the seed business (Vylor), after which the only per-share history is pro forma; both gaps are the owner's call
  (retro/README.md, "CTVA"). KMI (Kinder Morgan) has no 2008-2009 dates: no KMI stock traded then (the old KMI went private on
  2007-05-30; today's KMI listed on 2011-02-11), and KMP's or KMR's history was not substituted. From the listing (2013-01-18 to
  2026-11-13 so far) its EPS is GAAP from continuing operations per Class P share; 2011 is excluded (EPS from the February 2011 IPO only),
  so no date precedes the first full year (FY2012, released 2013-01-16); 2015-2017 and 2020 are excluded as distorted (certain items over
  income; the adjusted EPS also removes recurring items), so FY14's $0.89 anchors 2015-2018; KMI guides no revenue, so BASE reads revenue as
  reported; from the 2021 budget KMI guides GAAP net income, which sets current-FY EPS (the per-share figure where stated, else net income
  over the release's diluted shares) (retro/README.md, "KMI", "KMI 2015-2018", "KMI 2019-2022", "KMI 2023-2026"). LMT (Lockheed Martin) EPS is GAAP
  diluted EPS with the unusual items' per-share effects in (no filing publishes a figure without them); FY2002 is excluded (its unusual
  items exceed its earnings, no per-share figure without them), so its history and P/E window start with FY2003; BASE is the fiscal-year
  net sales guide, the segment operating profit guide is display only, and OFFSHORE is read as out of scope (retro/README.md, "LMT").
  From 2010 its EPS is from continuing operations where reported (PAE and EIG divested), releases that republish earlier years restate
  their EPS until a later 10-K (the Q1 2011 revenue-recognition table included), outlook words keep the last numeric range, the year-ago
  backlog stays the year-ago release's (recast tables unused), and CLOUD is read as out of scope (retro/README.md, "LMT 2010-2013").
- **Never use the owner's personal email** in request headers to external
  services (SEC asks for a contact in the User-Agent).
