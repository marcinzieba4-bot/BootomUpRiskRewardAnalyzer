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
  own 1997-2006 rule-T thresholds, engine and records) SO (2008-01-04 to 2026-11-13 so far, at the owner's request) CTVA (from its 2019 listing: 2021-02-05 to 2026-09-25), KMI (from its 2011 listing: 2013-01-18 to 2026-11-13 so far) LMT (2008-01-04 to 2026-11-13 so far), MU (2008-01-04 to 2021-12-31 so far), GOOG (2008-01-04 to 2026-11-13 so far), JPM (2008-01-04 to 2026-11-13 so far) and V (2009-10-29 to 2009-12-31 so far) sit in `staging/retrospective/` until the owner adds
  them to the archive (retro/README.md, "UNP", "LOW", "AAPL", "NKE", "AVGO", "PEP", "MSFT", "XOM", "SHW", "WMT", "RCL", "MAR", "BKR", "PFE", "CMCSA", "CAT",
  "BMY", "NVDA", "F", "SO", "CTVA", "KMI", "LMT", "MU", "GOOG", "JPM", "V"). The live `nke_signal_model.py`, `avgo_*.py`, `msft_signal_model.py`, `rcl_signal_model.py`, `wmt_signal_model.py`, `mar_signal_model.py` and `bmy_signal_model.py` (other branches) and `cat_signal_model.py`, `mu_signal_model.py` and `v_signal_model.py` (other branches) files
  and today's profiles in `data/business_profiles.json` (NVDA's, SO's and V's included) are 2026 analyses: never inputs to a retrospective. AVGO did not trade
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
  (retro/README.md, "GOOG"). From 2010: the filings print millions (stored in thousands); the Q1 2011 10-Q restates the quarter for the
  $500M DOJ charge (the same encoding); Motorola is in the prints as published from Q2 2012 and FY2012 is EPS from continuing operations
  (Motorola Home discontinued); the Q3 2012 release, filed during the session, is dated that day; the decade rolls, so FY2001 and
  FY2002 leave the history; CLOUD is out of scope; each fact's text is scanned for dates, years and quarters after its own publication,
  which found and corrected a leak in two 2008-2009 vintage notes (retro/README.md, "GOOG 2010-2013"). From 2014: the Class C dividend
  is a two-for-one split effective on its record date, 2014-03-27 (Yahoo's split date), each history figure restated on the basis of its
  own filing; Yahoo's GOOG series is the Class C capital stock from that date and EPS is the priced class's (FY2015 $24.34 for Class C,
  which carries the $522M Adjustment Payment; $22.84 for Class A and B); Motorola Mobile is discontinued from the Q1 2014 release, while
  FY2013 keeps it until the FY2014 10-K; Alphabet Inc. is the successor issuer from 2015-10-05; the Q2 2017 EC fine is at the company's
  figure without it (the ACN rule); the 8-K recast of 2016-05-03 is a vintage of its own (display cash flow only); the classes now rest
  mostly on the signals' rule-T bands (retro/README.md, "GOOG 2014-2017"). From 2018: FY2017 stays at GAAP $18.00 because its listed
  one-offs (the Tax Act's $9,857M and the EC fine's $2,736M) fall $69M short of its $12,662M income (the AAPL FY2002 test) and no filing
  publishes the year without them, so BEAR is -35.4%/yr from 2018-02-02 and the tier AVOID on most dates (the series' largest call: 67
  tiers move if FY2017 is excluded); FY2018-FY2020 are GAAP; quarters whose release publishes a figure without an EC fine or the Tax Act
  use it, year-ago quarters included (the ACN rule); RICH on 190 of 209 dates (retro/README.md, "GOOG 2018-2021"). From 2022: the
  20-for-one split is effective on Yahoo's split date, 2022-07-18 (the first split-adjusted trading day); dividends count from the first
  filing that states each rate ($0.20 from 2024-04-26); FY2024-FY2025 EPS is the Class C figure of the 10-K's EPS note ($8.03, $10.80);
  the Q3 2025 EC fine is out of the quarter's operating margin at the company's published 33.9% (EPS stays GAAP); GENAI is on the watch
  list from the FY2023 10-K's competition wording (2024-02-01 on), company-acknowledged, never re-filed (retro/README.md, "GOOG 2022-2026").
  JPM (JPMorgan Chase) is the first bank: revenue is total net revenue on the reported basis (not the managed basis), acquisitions in
  as published (Bear Stearns, Washington Mutual); EPS is diluted EPS from continuing operations (before the 2008 extraordinary gain), at
  the company's figure excluding merger costs where a supplement on the same basis prints it (FY2005 on); FY2002 is excluded by the AAPL
  test (its operating EPS is on an earlier basis), so the history and the P/E window start with FY2003, and FY2004's $1.48 is kept (the
  test passed by $515M): the two largest calls (39 and 33 classes the other way); no filing guides revenue, EPS or a margin, so BASE is
  the latest quarter's revenue growth less the net share issuance (the Bank One merger); the signals are a bank's (net revenue, the
  provision as a share of revenue, the expense gap, nonperforming assets against loans, the pre-tax margin) under rule T over
  1997-2006; two 10-Q restatements of nonperforming assets (Q2 and Q3 2008) and the EPS revision 8-K of 2009-05-29 are dated facts of
  their own; DURABLE; parts of the filings were not read (retro/README.md, "JPM", lists them). From 2010: FY08 is restated to $0.88
  by the Q4 2009 supplement (a `restates` field) and FY09 is $2.32; FY05-FY07 keep the company's pre-revision figures (a seam); the
  supplements print no figure excluding merger costs from Q1 2011, so FY11 $4.48 and FY12 $5.20 are GAAP; Q1 2012 is restated twice
  (its 10-Q for nonperforming assets, the Q2 2012 release for the synthetic credit portfolio; `restated` is a list); dividends $0.25
  (2011-03-18), $0.30 (2012-03-14) and $0.38 only from the first filing that states it as declared (2013-07-12); nine Friday releases
  are dated their own day; BEAR and XBULL are the 2008 trough on every date; FY2004 kept moves 102 of 209 classes, the signals 123
  (retro/README.md, "JPM 2010-2013"). From 2014: GAAP every year (FY13 $4.35, FY14 $5.29, FY15 $6.00, FY16 $6.19;
  two releases print a quarter without significant items, none a full year); the affordable housing accounting (2015-01-01) revises
  2011-2014 from the filing that first prints each figure: FY2014 revenue from the Q4 2015 supplement (`restates_revenue`), 2011-2014
  from the FY2015 10-K, 2010 kept (a seam); the outlooks are components only (net interest income, managed noninterest revenue, adjusted
  expense), so nothing is derived (the MSFT segment rule); each declared dividend ($0.40-$0.56) from the warrant-adjustment or CCAR 8-K
  that first states it, intentions unused; Q3 2015 released after the close (dated 2015-10-14); between a Q4 print and its 10-K the
  history holds eleven years, which holds most of the 13 FAIR dates; RICH on 195 of 208 dates, as BEAR stays FY2008's -80.1%/yr
  (retro/README.md, "JPM 2014-2017"). From 2018: FY2017 is the company's $6.87 excluding significant items (the Tax Act and a
  legal benefit; GAAP $6.31), from the Q4 2017 release in every vintage that holds it; FY2018-FY2020 are GAAP; FY2017 and FY2019 revenue are
  restated from the Q4 supplements that first revise them (`restates_revenue`); the Q3 2020 10-Q restates the quarter's nonperforming
  assets (`restated`); the outlooks stay components (the MSFT segment rule); dividends $0.80 (2018-10-05), $0.90 (2019-10-15), $1.00
  (2021-10-13); FY2008 leaves BEAR on 2018-03-02 (FY2007 leaves the ten years) and the history on 2019-02-27; CRYPTO (live 2020-10-21,
  scoped to banks) joins the watch list from its live date on the 10-K's own cryptocurrency sentence (`crypto_quote`, text only, the SO
  encoding); this batch was decided in the session that wrote the 2008-2017 findings, disclosed (retro/README.md, "JPM 2018-2021") From 2022:
  FY2024 is the company's $18.22 excluding significant items (the Visa gains among them; GAAP $19.75), from the Q4 2024 release in every
  vintage that holds it, as FY2017; FY2021-FY2023 and FY2025 are GAAP; the 10-Ks give three years of selected data from FY2021, so
  earlier years keep the latest 10-K that reported them; FY2020 revenue is restated by the Q4 2021 supplement (`restates_revenue`) and
  Q4 2024's nonperforming assets by the FY2024 10-K (`restated`); First Republic, the Visa and equity gains and the 2024 tax-credit
  accounting are in the figures as published; the outlooks stay components; dividends $1.05 to $1.65, each from the supplement that
  first states it; CRYPTO stays on the watch list on the FY2025 10-K's tokenized-securities and stablecoin words, and GENAI is out of
  scope (its registered scope names no bank); the CRYPTO line names the 10-K in force (a text fix that corrected six 2021 models); the
  last date is 2026-11-13 (retro/README.md, "JPM 2022-2026").
  V (Visa) is the class A common stock, NYSE: V, from its 2008-03-19 listing (prices as traded: the 2015 four-for-one split undone);
  the fiscal year ends on September 30. Of 2008-2009 only 2009-10-29 to 2009-12-31 (10 dates) can be built: Visa U.S.A. was a
  non-stock company, so FY2008 is the first year with EPS, and FY2008 is excluded as a distorted year (the AAPL test: the $1,457M
  covered-litigation reserve exceeds its $804M net income after tax) with no figure excluding only one-offs (the adjusted $2.25 also
  removes recurring step-up amortization: the NKE FY2007, AVGO and PFE rule), so no year is in the history until the Q4 FY09 print
  adds FY2009 (GAAP $3.10); the 32 weeks from the listing and the 52 after the Q4 FY08 print are the owner's call (an EPS anchor, or
  FY2008 at $2.25: that call flips all 10 built dates from RICH to CHEAP or FAIR). EPS is GAAP diluted class A; BASE is the fiscal-year
  net revenue range (FY2010 11-15%, "at the lower end" in the note), the EPS growth bound ("greater than 20%") gives no field, and the
  margin words no step; the bounds rule applies (FY2009 alone); rule T is on Visa U.S.A. 2002-2007 and Visa Inc. 2008 as published,
  nothing pro forma; the signals are revenue, the share of gross revenues kept after client incentives, opex excluding the litigation
  line, receivables and the operating margin; DURABLE, no live theme (retro/README.md, "V").
- **Never use the owner's personal email** in request headers to external
  services (SEC asks for a contact in the User-Agent).
