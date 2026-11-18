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
  own 1997-2006 rule-T thresholds, engine and records) SO (2008-01-04 to 2026-11-13 so far, at the owner's request) CTVA (from its 2019 listing: 2021-02-05 to 2026-09-25), KMI (from its 2011 listing: 2013-01-18 to 2026-11-13 so far) LMT (2008-01-04 to 2026-11-13 so far), MU (2008-01-04 to 2021-12-31 so far) and GOOG (2008-01-04 to 2009-12-31 so far) sit in `staging/retrospective/` until the owner adds
  them to the archive (retro/README.md, "UNP", "LOW", "AAPL", "NKE", "AVGO", "PEP", "MSFT", "XOM", "SHW", "WMT", "RCL", "MAR", "BKR", "PFE", "CMCSA", "CAT",
  "BMY", "NVDA", "F", "SO", "CTVA", "KMI", "LMT", "MU", "GOOG"). The live `nke_signal_model.py`, `avgo_*.py`, `msft_signal_model.py`, `rcl_signal_model.py`, `wmt_signal_model.py`, `mar_signal_model.py` and `bmy_signal_model.py` (other branches) and `cat_signal_model.py` and `mu_signal_model.py` files
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
  From 2014 the same encodings carry Sikorsky (from 2015-11-06) and the IS&GS divestiture (discontinued from the Q3 2016 release): the
  Q4 2016 release restates FY2015's EPS until the FY2016 10-K, whose 2012-2016 exclude IS&GS while 2007-2011 keep it (a seam, as
  published, which sets BEAR from 2017-02-10); ECOMMERCE, STREAMING and ENERGY_TRANSITION are read as out of scope, and the FY2016
  10-K's one mention of cloud computing leaves CLOUD out of scope (retro/README.md, "LMT 2014-2017"). From 2018: FY2017's GAAP EPS
  fails the AAPL test (the Tax Act), so it is the company's figure ($13.33, restated to $13.27 by the Q4 2018 release); 2016 on are on
  ASC 606 from the FY2018 10-K (a seam); the 2018 sales guide is read on the 2017 pro forma base the release states; the 2021 EPS outlook
  is the figure without the pension settlement; EV and CRYPTO are out of scope (retro/README.md, "LMT 2018-2021"). From 2022: GAAP EPS
  throughout, as the company's adjusted EPS also removes recurring mark-to-market items (2021-2023) or results of programs in
  performance (2024); an outlook that includes a booked one-off with no figure without it stands as published (2022's pension settlement,
  2025's program losses); segment profit excludes intangible amortization from 2023, each print against the year-ago quarter as its
  release recasts it; GENAI and GLP1 are out of scope; the last date is 2026-11-13 (retro/README.md, "LMT 2022-2026").
  MU (Micron) EPS is GAAP diluted EPS; FY2003 is a loss and takes the years before it, so the history and the P/E window start with
  FY2004 (2003-08-29); FY2006 is excluded by the mirror test (the $230M sale of NAND designs to Intel and $23M of reimbursements
  against $155M of income without them) and, since FY2007 is a loss, leaves only itself (the "would leave neither" note applied to a
  year that is not the latest, the owner's call); FY2007-FY2009 are losses and gaps, so FY05's $0.29 anchors every 2008-2009 date;
  no filing guides revenue, EPS or a margin, so BASE is the latest quarter's revenue growth; DURABLE (no 10-K calls the business
  cyclical); the listing moves to NASDAQ on 2009-12-30 (retro/README.md, "MU"). From 2010: the 8-K of 2010-03-04 that adjusts the FY2009
  10-K is a vintage of its own; FY2010's $1.85 is kept (the Numonyx gain under the test), FY2011 is excluded by the mirror test (the
  Samsung cross-license gains) and FY2013 by it too (the Elpida gain; a loss without it), FY2012 is a loss, and FY2006 stays a gap, so
  FY10's $1.85 anchors 2010-10-08 to 2013-12-31; the FY2011 and FY2006 readings are the series' largest calls (118 and 152 classes the
  other way) (retro/README.md, "MU 2010-2013"). From 2014: GAAP still (the non-GAAP figures remove recurring items: debt discount
  amortization, currency results, from FY17 stock compensation); FY2014 ($2.54), FY2015 ($2.47) and FY2017 ($4.41) are kept, FY2016 is
  a loss and a gap; the outlook reaches the filings on 8-K slides from 2016-11-29 (two conference updates, then each quarter's guidance
  slide), read against the year-ago quarter (the NVDA level rule, with a dollar plus-or-minus form); guidance given only on the call is not
  a filing (retro/README.md, "MU 2014-2017"). From 2018: GAAP still, and FY2018-FY2021 are all kept ($11.51, $5.51, $2.37, $5.14;
  the company's adjustments are 4-17% of each year's income); the outlook is in filings on the Q2 FY18 slide and in 8-K updates, on the call
  only for the Q3 FY18-Q3 FY19 releases (two 8-Ks that restate the call's range in numbers, 2018-07-05 and 2018-11-28, are read as guides),
  then in each release's Business Outlook from Q4 FY19; the first dividend ($0.10 a quarter) counts from 2021-08-03; spare parts leave
  inventories from Q2 FY21 while the year-ago 10-Qs keep them, a seam in the inventory signal (retro/README.md, "MU 2018-2021").
  GOOG (Google) is the Class A common stock that traded as NASDAQ: GOOG from the 2004-08-19 listing (Yahoo's GOOG series before 2014,
  as traded); the models print only GOOG. EPS is GAAP diluted EPS, except FY2004 at the company's $1.49 before non-recurring items (the
  later non-GAAP figures also remove stock-based compensation, which recurs); FY1999-FY2000 are losses and the first years, so the history
  starts with FY2001's $0.04 and the P/E window at the listing; no filing guides revenue, EPS or a margin (the 10-Ks' words that growth
  will decline are display only), so BASE is the latest quarter's revenue growth; CYCLICAL on the 10-K's own "cyclicality ... in our
  business"; receivables replace inventories among the signals, under rule T over the years the filings report (1999 on, start-up years
  included); a quarter its own 10-Q restates takes the 10-Q's figures from the 10-Q's date (Q3 2008, the Authors Guild settlement)
  (retro/README.md, "GOOG").
- **Never use the owner's personal email** in request headers to external
  services (SEC asks for a contact in the User-Agent).
