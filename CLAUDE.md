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
  own 1997-2006 rule-T thresholds, engine and records) SO (2008-01-04 to 2026-11-13 so far, at the owner's request) CTVA (from its 2019 listing: 2021-02-05 to 2026-09-25), KMI (from its 2011 listing: 2013-01-18 to 2026-11-13 so far) LMT (2008-01-04 to 2026-11-13 so far), MU (2008-01-04 to 2021-12-31 so far), GOOG (2008-01-04 to 2026-11-13 so far), JPM (2008-01-04 to 2026-11-13 so far), V (2009-10-29 to 2026-11-13 so far), SPGI (2008-01-04 to 2026-11-20 so far), CB (2008-01-04 to 2026-11-20 so far), LLY (2008-01-04 to 2026-11-20 so far), UNH (2008-01-04 to 2026-11-20 so far), CRM (2008-01-04 to 2026-11-20 so far), SCHW (2008-01-04 to 2026-11-20 so far), NEE (2008-01-04 to 2026-11-20 so far), NEM (2008-01-04 to 2026-11-27 so far), LYB (from its 2010 share issue: 2012-02-10 to 2026-11-20 so far), CHTR (from its first
  anchoring year: 2019-02-01 to 2026-11-20 so far), FANG (from its first anchoring year: 2014-02-21 to 2026-11-27 so far), TRGP (from its first full year of EPS: 2012-02-24 to 2026-11-27 so far) and OKE (2008-01-04 to 2026-11-27 so far) sit in `staging/retrospective/` until the owner adds
  them to the archive (retro/README.md, "UNP", "LOW", "AAPL", "NKE", "AVGO", "PEP", "MSFT", "XOM", "SHW", "WMT", "RCL", "MAR", "BKR", "PFE", "CMCSA", "CAT",
  "BMY", "NVDA", "F", "SO", "CTVA", "KMI", "LMT", "MU", "GOOG", "JPM", "V", "SPGI", "CB", "LLY", "UNH", "CRM", "SCHW", "NEE", "NEM", "LYB", "CHTR", "FANG", "TRGP", "OKE"). The live `nke_signal_model.py`, `avgo_*.py`, `msft_signal_model.py`, `rcl_signal_model.py`, `wmt_signal_model.py`, `mar_signal_model.py` and `bmy_signal_model.py` (other branches) and `cat_signal_model.py`, `mu_signal_model.py`, `v_signal_model.py`, `spgi_signal_model.py` and `lly_signal_model.py` (other branches) files
  and today's profiles in `data/business_profiles.json` (NVDA's, SO's, V's, SPGI's, CB's, LLY's, UNH's, CRM's and NEE's included) are 2026 analyses: never inputs to a retrospective. AVGO did not trade
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
  line, receivables and the operating margin; DURABLE, no live theme (retro/README.md, "V"). From 2010: EPS is the company's figure
  excluding only one-offs where published (FY10 $3.91 and FY11 $4.99 without the Visa Europe put-option gains, FY12 $6.20 without the
  $4.1 billion covered-litigation provision and two tax items; FY09 and FY13 GAAP); FY2009's diluted shares are restated to 759M by the
  Q4 FY10 release (`restates`); each outlook field comes from the latest print that gives it in numbers (revenue 11-15% for FY2010 and
  FY2011, FY2012 in words so the latest quarter stands, FY2013 "Around 13%" from Q3 FY13; operating margin "About 60%" for FY2011-FY2013,
  a guided step; EPS "Around 20%" for FY2013 from Q2 FY13, $7.44 on FY12's $6.20, bounds and words otherwise no field); Q3 FY12's
  operating margin excludes the provision as the release does (`op_one_off_m`, year-ago quarters included); the fiscal 2011 net
  presentation and CyberSource are in the growth rates as published; FY2008's exclusion still moves 78 of the 209 classes
  (retro/README.md, "V 2010-2013"). From 2014: the four-for-one split is effective on Yahoo's split date, 2015-03-19 (`splits`, the GOOG
  and NVDA basis helper), each history figure on the basis of its own filing (the Q4 FY15 release restates FY14 to $2.27); EPS is the
  company's figure excluding only one-offs every year (FY14 $9.07, FY15 $2.62, FY16 $2.84, FY17 $3.48: the covered-litigation provision,
  the put-option revaluations, the Visa Europe acquisition items, severance and tax remeasurements, the deferred tax elimination and the
  charitable contribution); revenue ranges in constant dollars feed BASE with their stated currency effect in the bridge only
  (`revenue_fx`; FY2014 10-11% then 9-10%, FY2016 7-8%, the Q3 FY16 Europe increment in the note), nominal ranges convert by their stated
  currency effect (`revenue_nominal`; FY2017 17.0-19.5%, 18.0-20.5%, 22%), the EPS ranges and levels are numbers (FY2014 17.5-18.5% at its
  midpoint, FY2017 "approximately 20%" on the adjusted $2.84); the opex signal leaves out the operating one-offs the releases' adjusted
  expenses exclude (`opex_one_off_m`); Visa Europe is in the prints as published from Q4 FY16; RICH on all 208 dates (retro/README.md,
  "V 2014-2017"). From 2018: EPS is the company's figure excluding only one-offs to FY2019 (FY18 $4.61 without the Tax Act
  items, the covered-litigation provision and the Visa Foundation donation; FY19 $5.44 without the $370M provision) and GAAP from FY2020
  ($4.89, $5.63), as the fiscal 2020 non-GAAP methodology also removes equity investment results and acquired-intangible amortization,
  which recur; the FY2020 10-K's recast FY18-FY19 figures are unused, so FY18-FY19 keep the FY2019 10-K's (a seam that sets BEAR at
  FY2020's -10.1%/yr from 2020-10-29; the largest EPS call of the batch); every outlook is words (FY2018-FY2020) or withdrawn and not
  given (from the Q2 FY20 release: `withdrawn` on a guide, a field only from guides after the year's last withdrawal), so BASE is the
  latest quarter's revenue growth on every date; the March 2020 Item 7.01 8-Ks give no field and are not encoded (text only); each
  vintage holds the ten fiscal years to the latest one (FY2009 leaves with the FY2019 10-K); ASC 606 from FY2019 without restatement (a
  seam); operating one-offs to Q4 FY19 only; CRYPTO (live 2020-10-21, scoped to payments networks) joins the watch list from its live
  date on the 10-Ks' own words (`crypto_quote`, the JPM encoding), with a factor pair that nets to zero from the FY2021 10-K, which names
  Visa's own crypto offering (`crypto_own_quote`); RICH on 199 of 209 dates, FAIR on the 10 after the Q4 FY21 print (retro/README.md,
  "V 2018-2021") From 2022: GAAP EPS every year (FY22 $7.00 to FY26 $12.32; the non-GAAP figures still remove recurring
  investment results and amortization), FY2017-FY2019 kept at the company's figures (the seam, so BEAR stays FY2020's -10.1%/yr; GAAP
  throughout moves 88 classes, the batch's largest EPS call); no outlook in numbers: the Q4 FY23 release's FY2024 table is words, and the
  Q1-Q4 FY24 releases point to an earnings presentation on the website, not filed (`outlook_elsewhere`, quoted in the guide line, no
  field), so BASE is the latest quarter's revenue growth on every date; litigation provisions stay in the margin; dividends $0.45 to $0.78
  from the Q4 releases; CRYPTO stays on the watch list on each 10-K's words, its factor pair only where a 10-K names Visa's own offering
  (FY2025, FY2026), and GENAI is out of scope; the last date is 2026-11-13 (retro/README.md, "V 2022-2026").
  SPGI is The McGraw-Hill Companies, Inc., NYSE: MHP, in 2008-2009 (McGraw Hill Financial from 2013, S&P Global from 2016): SPGI is only
  the series key and Yahoo's symbol, the models print MHP (the BKR encoding), and later McGraw-Hill and S&P names are on the anachronism
  list. Yahoo's 1057:1000 factor of 2026-07-01 is the Mobility Global distribution, not a split: it follows every built date, so Yahoo's
  close times it is the price as traded, and the builder refuses later dates until it is encoded (the `distributions` rule). EPS is diluted
  EPS from continuing operations before the extraordinary item and the cumulative adjustment, from each 10-K's Eleven-Year Financial Review
  (one basis for eleven years); no filing publishes a figure excluding only one-offs on that basis (the FY1998-FY1999 10-Ks' figures
  predate the 2003 restatement), so none is adjusted and none excluded, and 2001's restructuring sets BEAR. The guides: FY2007 in words
  (no field), FY2008 as growth of 3-5% on FY07's $2.94 without the two items the guide excludes ($2.99), then ranges, FY2009 ranges; revenue
  only by segment for 2007-2008 (components: no total derived, so BASE is the latest quarter's reported growth) and consolidated for 2009;
  signals Financial Services and Education revenue, revenue, diluted EPS and the segment margin, as reported; DURABLE (the risk factor
  "Cyclical Nature of Customers' Businesses" is the customers' adoption cycle); no live theme (retro/README.md, "SPGI"). From 2010:
  each year from the latest filing that reports it (the FY2009 eleven-year review, the FY2010 five-year review, the FY2011 and FY2012
  10-Ks' continuing operations without Broadcasting, then without McGraw-Hill Education, and the FY2012 10-K/A of 2013-03-20 as a vintage
  of its own), seams as published (2007 with Education beside 2008 without it sets BEAR from 2013-03-01); EPS is the company's figure
  excluding only one-offs where a release on the same basis prints it (2009 $2.37, 2010 $2.69/$2.68, 2011 $2.91/$2.09, 2012 $2.75),
  GAAP otherwise; releases that republish a year on a new basis restate it until the next 10-K (`restates`); the EPS guides are ranges
  (words keep the range), revenue is never guided in numbers (2013's "high single-digit" is words), so BASE is the latest quarter's
  growth as reported; dividends from each 10-K ($0.235 to $0.28; the 2012 special dividend is not a rate); the Financial Services line
  is the releases' Standard & Poor's (S&P Ratings) and McGraw-Hill Financial (S&P Capital IQ, S&P Dow Jones Indices) less the royalty
  elimination (`fs_parts`); Education is n/r from the Q4 2012 release through `spgi2_engine.py.tmpl`, the None-tolerant copy (the BKR
  `bkr3` encoding); McGraw Hill Financial, Inc. from 2013-05-06 and NYSE: MHFI from 2013-05-14 (`company_names`, `listings`); DURABLE
  (the FY2009-FY2011 10-Ks' "Our education businesses operate in a cyclical environment" is the adoption cycle); this batch was
  decided in the session that wrote the 2008-2009 findings, disclosed (retro/README.md, "SPGI 2010-2013").
  From 2014: McGraw Hill Construction is discontinued and the 8-K of 2014-11-05 recasting FY2013 without it is a vintage of its own (the
  MSFT recast rule); the company's figures excluding only one-offs stand for 2013-2015 (FY2014 $3.88 against GAAP $(1.08), the legal
  settlements); from 2016 the adjusted figures and guides also remove deal-related amortization, which recurs, so FY2016 is GAAP ($7.94),
  the FY2016 guides feed nothing (`eps_guide_amort`, guide line only: FY15's $4.53 stands) and FY2017 uses the GAAP ranges; FY2017's
  "unchanged" reported revenue is 0% (the "flat is 0" rule) and its later words leave it standing; the Financial Services line keeps
  the old scope, with Market Intelligence from its own row inside Market and Commodities Intelligence; a year-ago loss measures EPS growth
  on its absolute value (the CAT rule); S&P Global Inc. from 2016-05-02 and NYSE: SPGI from the S-3 of 2016-06-29 (dated 2016-06-30);
  the 2007-2008 Education seam sets BEAR on every date (the batch's largest call); built in a new session without opening the 2008-2013
  outcomes or findings (retro/README.md, "SPGI 2014-2017").
  From 2018: GAAP every year (FY17 $5.78 with the Tax Act charge, FY18 $7.73, FY19 $8.60, FY20 $9.66); the GAAP ranges are the guides
  (the Kensho and Investor Day 8-Ks of 2018 included), and FY2021 has none until the Q3 2021 release, so FY20's $9.66 stands to 2021-10-22;
  the Investor Day's FY2018 GAAP operating margin guide (44-45%) is method r2's guided margin step from the FY2017 10-K's 43.05%
  (`op_margin_guide`); four segments from Q1 2018, the Financial Services line their Ratings, Market Intelligence and Indices, Corporate
  revenue (Kensho) outside it (`other_k`); the Education seam leaves BEAR on 2018-02-12, after which BEAR is GAAP 2016-2017's -27.2%/yr;
  RICH on 206 of 209 dates; decided in the session that scored 2014-2017, disclosed (retro/README.md, "SPGI 2018-2021").
  From 2022: GAAP every year still (FY21 $12.51 to FY25 $14.66; each 10-K gives three years, Item 6 being reserved); IHS Markit
  (merged 2022-02-28) is in the figures as published, so BASE runs +39-44% on the merger quarters' reported growth (2022's "more than
  40%" and "more than 30%" are bounds, no field); the March 2022 guidance was never filed and the 2022-06-01 suspension is a withdrawal
  (`withdrawn`); from 2023 the GAAP reported revenue ranges feed BASE and the GAAP margin guides are the guided step, as a level on the
  prior year's GAAP margin (2023, 2025) or as the expansion itself (`op_margin_step_bp`, 2024 and 2026); FY2023 and FY2026 have no GAAP
  EPS guide until April and July; the 2026-07-01 Mobility Global spin-off is a distribution (`distributions`, the CMCSA code), the
  history keeping Mobility until a GAAP filing restates it (the pro forma statements add nothing) and FY2026 from the Q2 2026 release's
  continuing-operations guide; GENAI is on the watch list from the FY2023 10-K (text only, the GOOG rule); RICH 163, FAIR 67, CHEAP 25
  of 255 dates; built in a new session without opening the 2008-2021 outcomes or findings (retro/README.md, "SPGI 2022-2026").
  CB is ACE Limited, NYSE: ACE, in 2008-2009 (Chubb Limited from 2016): CB is only the series key and Yahoo's symbol for ACE's history, the
  models print ACE (the BKR and SPGI encoding), and "Chubb Limited" is on the anachronism list. The Chubb Corporation, which traded as CB in
  2008-2009, is a different company and is not this series (its own ticker and a non-Yahoo price source would be the owner's call). The first
  insurer: revenue is total revenues as the statement of operations adds them (realized gains and losses in); EPS is GAAP diluted before the
  cumulative effect, as the company's "income excluding net realized gains (losses)" also removes recurring realized gains and losses (the
  NKE FY2007, AVGO, PFE and V rule; FY08 $3.53 against the company's $7.72, the series' largest call, 52 classes); FY2002 is excluded by
  the AAPL test (the $354M asbestos charge against $100M), so the history and the P/E window start with FY2003, and FY2005 is kept with its
  listed catastrophe and A&E items summed against its realized gains ($976M against $1,029M; charges alone would exclude it, 46 classes);
  the FY2007 "Earnings per Common Share" range is the FY2007E anchor as published, the FY2008 operating income range feeds nothing (the
  SPGI eps_guide_amort rule) and net premiums earned guides are components (the MSFT segment rule), so BASE is the latest quarter's revenue
  growth less net share issuance; fiscal 1996-1998 ended September 30 (the BKR transition rule, rule T only); signals are net premiums
  earned, the combined ratio, investment income, book value per share and the pre-tax margin; CYCLICAL on the 10-Ks' own "historically
  cyclical"; dividends in dollars as each filing states them after the Swiss Continuation; CHEAP 51, FAIR 6, RICH 48 of 105 dates (RICH on
  every date from the Q4 2008 print) (retro/README.md, "CB"). From 2010: GAAP still (FY09 $7.55, FY10 $9.11, FY11 $4.65, FY12 $7.89;
  the company's operating figures also remove realized gains and losses), each year from the latest filing that reports it, with two
  restatements from the release that first prints each (`restates`, now in `build_cb.py`): the two-class method of ASC Topic 260 (FY08
  $3.50 from the Q4 2009 release, FY05-FY08 from the FY2009 10-K) and the deferred acquisition cost accounting adopted 2012-01-01 (FY11
  $4.52 from the Q4 2012 release, FY08-FY11 from the FY2012 10-K), earlier years as first published (seams); the Q1 2012 supplement's
  restated 2011 net income is not made a per-share figure; every guide is operating income per share, so none feeds a field and the last
  full year's GAAP EPS stands; no revenue guide, so BASE is the latest quarter's revenue growth less net issuance (+34.4% on Q4 2009
  against 2008's realized losses); dividends $0.33 to $0.51 from the first filing that states each (the 2011 rate from the Q2 2011 10-Q,
  the 2012 increase from the FY2011 10-K: the meeting 8-Ks give votes only); CYCLICAL, no live theme; FY11's $4.65 makes all 52 dates
  from the Q4 2011 print RICH (the operating basis too; it moves 79 classes, mostly 2011's to RICH); CHEAP 48, FAIR 68, RICH 93 of
  209 dates; decided in the session that scored 2008-2009, disclosed (retro/README.md, "CB 2010-2013"). From 2014: GAAP still (FY13 $10.92,
  FY14 $8.42, FY15 $8.62, FY16 $8.87; the operating figure also removes realized gains and losses and, from 2016, the recurring fair value
  amortization), no restatement; no guide in any filing (the operating ranges end with Q3 2013; run rates and call guidance feed nothing),
  so the last full year's GAAP EPS stands on every date and BASE is the latest quarter's revenue growth less net issuance; the ten years to
  the latest one (FY2003 and the FY2002 note leave with the FY2013 10-K, FY2005 with the FY2015 10-K); The Chubb Corporation, acquired
  2016-01-14, is in the figures as published (BASE +56-75% on Q1-Q4 2016: every one of the 51 CHEAP dates rests on it, the batch's largest
  call; pro forma and "as if" figures unused); Chubb Limited, NYSE: CB, from the 8-K of 2016-01-15 (`company_names`, `listings`, the SPGI
  encoding, now in `build_cb.py`); the P&C combined ratio from the supplement; dividends $0.63 to $0.71, each from the first filing that
  states it; CYCLICAL, no live theme's scope names insurance; a text-only leak in the FY2009-FY2011 vintages' notes (later years' realized
  gains) found and corrected (157 models, one comment line); built in a new session without opening the 2008-2013 outcomes or findings
  (retro/README.md, "CB 2014-2017"). From 2018: GAAP still (FY17 $8.19 with the 2017 Tax Reform's $450M one-time benefit, as no
  filing publishes the year excluding only it; FY18 $8.49, FY19 $9.71, FY20 $7.79 with the $1,193M after-tax COVID-19 charge read as a
  catastrophe loss, which moves 13 classes of 2021); the FY2020 10-K gives three years (Item 6 "Not required."); no guide in any filing; the
  ten-year roll moves BEAR from FY07-FY08 to FY10-FY11 (2018-02-23) and FY13-FY14 (2021-02-26); dividends $0.73 to $0.80 from the Q2
  10-Qs; RICH on 200 of 209 dates (FAIR 3, CHEAP 6 in March-May 2020); decided in the session that scored 2014-2017, disclosed
  (retro/README.md, "CB 2018-2021") From 2022: GAAP still where no filing publishes the year excluding only a one-off (FY21 $19.27, with
  $3,023M of after-tax realized gains, anchors 48 CHEAP dates of 2022; FY22 $12.55; FY25 $25.68); FY23 $19.06 and FY24 $22.56 are the
  company's "Net income excluding tax benefit" (the Bermuda deferred tax benefits; GAAP $21.80 and $22.70, the ACN, UNP 2005, LMT and JPM
  rule; 44 classes); the LDTI restatement (FY21 $19.24, FY22 $12.39) from the Q1 2023 supplement, the first filing that prints it (the
  print-level `restates` of LMT, PFE and CAT, now in `build_cb.py`); market risk benefits in total revenues as the statement adds them;
  Cigna's Asian business (2022-07-01) and Huatai at 100% (2023-07-01) as published, EPS on Chubb net income; no guide in any filing; BEAR
  moves to FY21-FY22 (-34.9%/yr, then -35.6% adjusted); dividends $0.83 to $1.02 from the Q2 10-Qs; CHEAP 82, FAIR 94, RICH 79 of 255
  dates; built in a new session without opening the 2008-2021 outcomes or findings (retro/README.md, "CB 2022-2026").
  LLY (Eli Lilly and Company, NYSE: LLY) EPS is GAAP diluted EPS from continuing operations before extraordinary items and accounting
  changes, each year from the latest filing that reports it (PCS discontinued from the FY1998 10-K; 2005 at $1.83 before its cumulative
  effect): the company's adjusted, pro forma adjusted and pro forma non-GAAP figures also remove acquired in-process research and
  development, which recurs (2001, 2002, 2004, 2007, 2008), and add ICOS and ImClone pro forma, so they are shown only (the NKE FY2007,
  PFE and BMY rule); no year to 2007 is distorted (2004 the near case at 59%), FY2008 ($(1.89), a loss) is excluded as the latest year
  (the BMY FY2015 encoding: its own days leave the window, FY2009 is current from the Q4 2008 print); the FY2007 10-K/A of 2008-10-21
  (balance sheets only) is a vintage of its own; current-FY EPS is the reported range's midpoint (the 8-K of 2008-03-13 included), and a
  range whose midpoint is a loss has no P/E, so the 8-K of 2008-12-11's FY2008 loss guide is read as no numeric guide and FY07's $2.71
  stands (decided here); revenue is guided in words, so BASE is the latest quarter's growth ex-FX as each release states it (Q4 2008's
  "essentially flat" is 0); the PFE signal set with Lilly's own rule-T thresholds, company-wide U.S. and outside-U.S. growth from the
  release from Q4 2008, from each 10-Q's date for Q2 2007-Q3 2008 (`geo_later`, the PEP servings rule) and n/r for Q4 2007; dividends
  from the 10-Ks; DURABLE, no live theme; CHEAP and BUY on all 105 dates, robustness 8 of 8, and no tested encoding moves a class; a
  self-text scan (each fact's words, figures and years in a filing by its own date) caught and corrected a first-draft leak in the
  vintages' notes (retro/README.md, "LLY"). From 2010: the FY2009-FY2012 vintages are GAAP every year ($3.94, $4.58, $3.90, $3.66; 2012's
  only listed benefit, the $.43 Amylin income, is under its EPS without it) and FY2008 stays excluded; revenue is the FY2009 10-K's total
  revenue (EITF 07-1), FY2008's restated from the Q4 2009 release on four dates (`restates_revenue`, the JPM encoding), and 2005 stays at
  $1.83 before its cumulative effect (the FY2009 10-K's $1.81 is after it); the reported EPS ranges are used as published (FY2010's
  "excluding the potential impact of health care reform" until Q1 2010, the Amylin income in FY2012, the exenatide income and 2012's R&D
  tax credit in FY2013; the 8-K of 2012-01-05's FY2011 range on four dates), the non-GAAP ranges shown with their own reason (`adj_why`);
  revenue is guided in words to FY2011 (BASE the latest quarter ex-FX) and in dollars for FY2012-FY2013, read as growth on the last full
  year (`rev_guide_usd_b`, the BMY code: -10.2% to -6.1%, then -0.0% to +3.5%); the mid-term floors through 2014 add nothing; every
  release states the U.S. split; dividends $0.49 from the 10-Ks, repurchases text only; DURABLE, no live theme; CHEAP and BUY on all 209
  dates, which rest on the ten-year window (a five-year one makes 106 dates from 2011-12-30 RICH); decided in the session that scored
  2008-2009, disclosed (retro/README.md, "LLY 2010-2013").
  From 2014: the FY2013-FY2016 vintages are GAAP every year ($4.32, $2.23, $2.26, $2.58; each over half the non-GAAP figure, which also
  removes recurring in-process research and development and, from 2015, amortization), FY2008 still excluded; the reported EPS ranges are
  used as published, one-offs in, the guidance 8-Ks' updates of the current year included (FY2014 $2.15-2.23 from 2015-01-07, FY2015
  $2.28-2.33, FY2016 $2.57-2.67, FY2017 $1.56-1.66), so FY17E falls to $1.78 and $1.61 against a non-GAAP $4.15-4.25 (the CoLucid and
  streamlining charges); revenue is guided in dollars every year, read as growth on the last full year (FY2014 -16.9% to -14.3% after the
  Cymbalta and Evista U.S. expiries); Novartis Animal Health (2015-01-01) in the figures as published; a Friday release (Q4 2014) dates its
  own week; the dividend rates $0.50 and $0.51 from the Q4 2014 and Q4 2015 releases that first state them (LLY's first `dividends`
  facts), $0.52 from the FY2016 10-K; no builder change; DURABLE, no live theme; CHEAP and BUY on the 4 dates of January 2014 (FY13E),
  RICH and AVOID on the 205 from the Q4 2013 print, as the window median stays 12.7x (the 2009-2013 regime holds most of its days) while
  the FY14E-FY17E guides trade at 19-54x; built in a new session without opening the 2008-2013 outcomes or findings (retro/README.md,
  "LLY 2014-2017").
  From 2018: FY2017 ($(0.19), a loss on the U.S. tax reform charge; $(0.08) from continuing operations) is excluded like FY2008, its days
  out of every window ("ex-FY17"); Elanco Animal Health is consolidated to its 2019 disposition, and the 8-K of 2019-10-24 recasting the
  FY2018 10-K without it is a vintage of its own (2014-2018 from continuing operations, a seam with 2013's animal health that sets BEAR at
  -53.5%); EPS is from continuing operations wherever reported, so the FY2019 guides are the continuing-operations ranges ($4.64-4.76), not
  the reported totals with the Elanco gain ($8.57-8.69, the batch's largest call: 39 classes); the Elanco-free FY2019 revenue guide is read
  against FY2018 with Elanco until the recast (the LOW 2011 and PFE rule; no class either way); the FY2020 10-K has no Item 6, so 2018-2020
  come from its statements (the ACN FY21 rule); the January 2018 dates keep FY17E $1.61; dividends $0.5625-$0.85 from the 10-Ks; the Q1 2018
  release's figures come from its exhibit's text layer (slide images); DURABLE, no live theme; RICH 168, FAIR 39, CHEAP 2 of 209 dates (the
  window's median rising from 12-13x to 23-27x in 2019 as the 2009-2013 regime leaves); decided in the session that scored 2014-2017,
  disclosed (retro/README.md, "LLY 2018-2021").
  From 2022: the FY2021-FY2025 10-Ks are GAAP every year ($6.12, $6.90, $5.80, $11.71, $22.95; Item 6 reserved, three years from each
  statement; the FY2025 10-K's rounded millions replace the earlier exact figures), FY2017 still excluded; the company's non-GAAP measures
  keep acquired IPR&D from Q1 2022 (the 8-K of 2022-04-14) but still remove amortization, so GAAP stands; the reported EPS ranges are used
  as published, acquired IPR&D charges in (FY23E $6.05 after Q3 2023), and FY2026 is guided on a non-GAAP basis only, so FY25's $22.95
  stands (the rollover rule, the BMY FY2024 encoding; a text-only builder change, "non-GAAP only"); revenue guided in dollars every year
  (+18% to +42%), the 8-K of 2025-01-14's "approximately $45.0 billion" a point for FY2024; from Q1 2022 the releases state U.S. revenue to
  $0.01B (then $0.1B), so no million-level identity; dividends $0.98-$1.73 from the 10-Ks; DURABLE, no live theme (GLP1 is Lilly's own
  market); Foundayo and Onswik join the anachronism list; RICH and AVOID on all 156 dates to 2025-01-31, CHEAP and BUY on the 52 of the
  FY2025 guide, CHEAP 35, RICH 5, FAIR 2 in 2026; the CHEAP calls move with the signals at BEAR (59 dates); built in a new session without
  opening the 2008-2021 outcomes or findings (retro/README.md, "LLY 2022-2026").
  UNH (UnitedHealth Group Incorporated, NYSE: UNH), the first health benefits company: EPS is diluted EPS, each year from the latest filing
  that reports it (2002-2006 as the FY2006 10-K restates them for the stock option review under FAS 123R; 2001 and earlier as first
  published, a seam), at the company's figure excluding only one-offs where a filing on the same basis prints it (1998 $1.31 without the
  realignment and other charges, GAAP a loss; 1999 $0.79; 2000 $1.05; FY07 $3.50 without the IRS Section 409A charges; FY08 $2.95 without
  the settlements, severance and the Nevada gain, each from its Q4 release in every vintage), per-share facts restated for the 2000, 2003
  and 2005 splits after their own filing (`splits`, the shared on_basis helper); current-FY EPS is the guide midpoint, at the company's figure
  where a guide is given with and without announced items; revenue is guided in dollars, read as growth on the last full year (no
  next-quarter revenue guide); the Q1 and Q2 2008 outlook schedules' operating margins are method r2's guided step, and the 8-K of
  2008-07-02's is derived from its guided earnings from operations and revenues (decided here); the Q2 2007 print is restated by its 10-Q
  from 2007-08-06 (`restated`); the signals are premiums, the medical care ratio, fees (services and products), the operating cost ratio and
  the operating margin, with UnitedHealth's own rule-T thresholds over 1997-2006; DURABLE (no 10-K calls the business cyclical), no live
  theme; dividends $0.03 a year from the 10-Ks; CHEAP and BUY on all 105 dates, robustness 8 of 8, and no tested encoding moves a class;
  OptumRx, OptumInsight, UnitedHealthcare Community & State, Optum360 and OptumCare join the anachronism list (retro/README.md, "UNH").
  From 2010: GAAP every new year (FY09 $3.24 to FY12 $5.28; no filing prints an EPS excluding one-offs, so 2010's $200M Ingenix
  charges stay in), 2007 and 2008 kept at the company's figures; the reported EPS ranges as published (the Q1-Q3 2011 ranges with the
  estimated Penn Treaty assessment in, no range without it is published); revenue guided in dollars every year ("approaching" a level,
  "to exceed" a bound, no field); the guided margin step from the Q1 2010 schedule (6.6%-7.1%) and derived from the Q1 2011 schedule's
  earnings from operations range and revenue (7.28%, BASE -5.8% for the rest of 2011), none for FY2012-FY2013; the 8-K of 2011-05-23
  (a segment recast) and the preliminary 8-K of 2012-10-09 add nothing; dividend rates $0.50 to $1.12 from the Q2 releases that first
  state them (`dividends`, annual rates passed around the split helper); Amil (2012-10-26) in the figures as published; DURABLE; CLOUD
  (live 2012-10-30) out of scope, every live theme's scope quoted from 2012-11-02 (the CB wording); CHEAP 185, FAIR 24 (from
  2013-07-12, as the window's median falls to 11.4x and the EPP floor to 9x), and no tested encoding moves a class (a five-year window
  moves 154, the signals at BEAR 51); decided in the session that scored 2008-2009, disclosed (retro/README.md, "UNH 2010-2013").
  From 2014: GAAP every new year (FY13 $5.50 to FY16 $7.25), as the releases' adjusted EPS (from Q4 2015) also excludes the recurring
  amortization of acquisition-related intangibles; the GAAP guide ranges as published (the Catamaran costs of 2015 and the exchange losses
  of the 8-K of 2015-11-19 in), the GAAP $7.10-7.30 standing through the Q1 2016 release (adjusted range only); FY2016 is $7.48 in the Q4
  release and $7.25 in the 10-K (the $350M Penn Treaty assessments), and the Q4 2016 print is restated by the 10-K (`restated`, lines as
  its year less the nine months); the Q4 2015 pharmacy fulfillment reclassification is used as each release shows the year-ago quarter;
  revenue guided in dollars every year, Catamaran in as published; no guided margin step; dividend rates $1.50 to $3.00 from the Q2
  releases; DURABLE; the FY2015 and FY2016 10-Ks' "cloud-enabled collaboration" (an OptumInsight offering) leaves CLOUD out of scope
  (`cloud_words`, text only); RICH 192, FAIR 16 (2014-01-10 to 2014-04-11, 2016-02-05, 2016-02-12) against a ten-year median of 11.3x;
  built in a new session without opening the 2008-2013 outcomes or findings (retro/README.md, "UNH 2014-2017").
  From 2018: GAAP every year (FY17 $10.72 with the $1.22 Tax Reform benefit, as no filing prints a per-share figure excluding only it,
  the batch's EPS call; FY18 $12.19 to FY20 $16.03); the GAAP guide ranges as published ("to approach" a level, the FY2021 ranges with
  the potential COVID-19 effects in, the FY2020 range "maintained" through COVID-19); revenue guided in dollars only in the conference
  outlook releases; no guided margin step; the FY2020 10-K has no selected data, so 2018-2020 come from its statements; 2008 leaves the
  history with the FY2018 10-K, so BEAR is the 0% cap from 2018-02-14 and XBULL the 2015-2017 run (+33.6%/yr); dividend rates $3.60 and
  $4.32 from the Q2 releases, $5.00 and $5.80 from the Q2 10-Qs; DURABLE; the FY2020 10-K no longer names cloud (`cloud_dropped`, text
  only); 53 dates carry a false calendar-year warning (the 0.2081 tax rate); RICH 180, FAIR 22, CHEAP 7 (the window's median rising
  from 11.3x to 18.0x); decided in the session that scored 2014-2017, disclosed (retro/README.md, "UNH 2018-2021").
  From 2022: GAAP every year (FY21 $18.08 to FY25 $13.23; FY2024's $15.51 carries the Brazil sale and the cyberattack costs, which leave
  it above half the year's EPS without them, so no year is distorted, and its -35.0% is BEAR from 2025-01-17); the GAAP guide ranges as
  published, one-offs in ($17.60-18.20 to $15.50-15.75 for FY2024; the January 2024 affirmation without the Brazil sale keeps $26.20-26.70,
  the ACN rule); the 8-K of 2025-05-14 suspends the outlook (`withdrawn`, the SPGI and V encoding, new in this builder), and "at least",
  "greater than" and "more than" are one-sided bounds, no field (`eps_bound`, text only), so FY24's $15.51 and FY25's $13.23 stand until
  the Q2 2026 range; the Q2 2025 schedule's 4.8%-5.0% and the Q4 2025 table's ~5.5% are guided margin steps (BASE -52.6% from 2025-07-30,
  +35.8% from 2026-01-28); revenue guided in dollars to FY2025, FY2026 as a bound; dividend rates from the Q2 10-Qs ($6.60, $7.52, $8.40,
  $9.28) and the Q2 2025 release ($2.21 a quarter); DURABLE, no live theme (GENAI and GLP1 out of scope; the FY2023-FY2025 10-Ks' AI words,
  `ai_words`, text only); 51 dates carry a false calendar-year warning (the 0.2052 tax rate); RICH 158, CHEAP 52, FAIR 45; the adjusted-EPS
  reading moves 65 classes, the suspension 36, the margin steps 36; built in a new session without opening the 2008-2021 outcomes or
  findings (retro/README.md, "UNH 2022-2026").
  CRM (salesforce.com, NYSE: CRM) runs from its 2004-06-23 listing (the window rule; prices as traded, the 2013 four-for-one split undone);
  the fiscal year ends on January 31. EPS is GAAP diluted EPS (the releases print GAAP only from Q4 FY07), except FY2006 at the company's
  $0.181 without the tax valuation allowance reversal and the lease recovery (Q4 FY06 release; GAAP $0.24); fiscal 2000-2003 are losses
  and FY2004 is excluded by the mirror test (its $3,445K lease recovery against $794K of pre-tax income without it), taking the years
  before it, so the history starts with FY2005; FY2007's $0.00 has no P/E (the F rule) and is excluded as the latest year, then a gap;
  current-FY EPS is the fiscal-year GAAP range's midpoint (FY2009's with the InStranet acquisition, whose effect recurs); BASE is the
  next-quarter revenue guide, a dollar range, against the year-ago quarter; no margin guide, no dividend; the signals are subscription and
  support revenue, deferred revenue (current and noncurrent), the gross margin, the opex gap and the operating margin, under rule T over
  fiscal 2002-2007 (start-up years in); DURABLE, no live theme (the 10-Ks' cloud computing words are its own model); FAIR on the 8 dates
  before the Q4 FY08 print, CHEAP on the 97 after, BUY on all 105 (retro/README.md, "CRM"). From 2010: GAAP still (FY10 $0.63, FY11
  $0.47), FY2012's $(0.09) excluded as a loss and the latest year (its days out of the window, "ex-FY07 ex-FY12"; the non-GAAP $1.36
  removes recurring items); every FY2012 range from Q1 FY12 and every FY2013 range is a GAAP loss, which has no P/E, so FY11's $0.47
  stands from 2011-05-20 (the LLY 2008 rule; the last positive range instead moves 40 tiers); the Jigsaw 8-K's EPS effect is not a range,
  so $0.58-0.60 stands to the Q1 FY11 range that includes it (4 classes otherwise); guidance in unfiled press releases (2011-03-30,
  2012-06-04) is unused; a fiscal-year revenue guide stated as growth (`rev_guide_pct`) and the convertible notes (`debt_note`) are
  display only; CLOUD (live 2012-10-30) is out of scope, every live theme's scope quoted from 2012-11-02; RICH 134, CHEAP 19 (to
  2010-05-14), FAIR 4 of 157 dates; decided in the session that scored 2008-2009, disclosed (retro/README.md, "CRM 2010-2012").
  From 2013-02-25 CRM is a **reduced-data batch**: SEC's www.sec.gov refused the session's document downloads (no deliverable contact),
  so the facts are only the 10-Qs' and 10-Ks' XBRL company facts (data.sec.gov), each dated by its filing, flagged `reduced_data`;
  no earnings release, guide, other 8-K or 10-K text is in it, and the models say "not in this fact sheet", never "none given". The
  10-Q or 10-K is the print, Q4 is the fiscal year less nine months, subscription and support is total revenues less professional
  services (the tags change meaning in 2015), the 2013-04-18 four-for-one split comes from the price series' event, FY2013-FY2016
  are GAAP losses (excluded, then gaps), FY2017 is GAAP $0.26, and the current year rests on the last full year (FY11's $0.1175,
  then FY17's $0.26); ECOMMERCE, STREAMING and ENERGY_TRANSITION name no software business; RICH on all 261 dates (robustness 8 of
  8), no tested encoding moves a class; redo it from the filings when they can be downloaded (retro/README.md, "CRM 2013-2017").
  From 2018 the same reduced data: ASC 606 from the FY2019 10-K (FY17 $0.46 and FY18 $0.49 restated, FY2016 and earlier a seam), unearned
  revenue for deferred revenue from Q1 FY19 (Q1-Q3 FY19 against pre-606 balances, a seam), total revenues standing in for subscription
  and support from Q2 FY19 (professional services is tagged only in segment detail), two re-accepted filings dated from their filing
  dates (no later date or accession in any text), FY2019-FY2021 GAAP ($1.43, $0.15, $4.38: no item listed as a one-off in the sheet), EV
  and CRYPTO out of scope; the class follows the last full year's EPS: RICH 115, CHEAP 94 (2019-03-08 to 2020-02-28 on FY19's $1.43,
  2021-03-19 on on FY21's $4.38); FY2021 excluded by the mirror test moves all 42 CHEAP dates of 2021 to RICH, the batch's largest
  call; decided in the session that scored 2013-2017, disclosed (retro/README.md, "CRM 2018-2021").
  From 2022 CRM is **full data again** (`reduced_data.full_from` 2022-01-01: SEC served the documents to a generic client name; facts
  marked `full_data`, CR77-CR108, are read only from that day, so 2008-2021 is unchanged): the releases are the prints (subscription and
  support, unearned revenue from the release's roll-forward); the decade's years face the AAPL FY2002 test and its mirror on the items
  the filings list, so FY2017 and FY2019 (valuation allowance releases), FY2020 (the $166M one-time charge), FY2021 (the IPO gains and the
  $2.0B tax benefit), FY2022 (the strategic investments' $0.93) and FY2023 (restructuring) are excluded and stay gaps, FY2018 and
  FY2024-FY2026 kept; the GAAP EPS guide midpoint; the fiscal-year GAAP operating margin guide is a guided step (new for CRM, the ACN
  rule); dividends from 2024-02-29 ($0.40, $0.416, $0.44 a quarter); Salesforce, Inc. from 2022-04-04; GENAI on the watch list from the
  FY2025 10-K (its competitor list names AI vendors; the MSFT and GOOG rule, text only), GLP1 out of scope; RICH 34, FAIR 13 (2022),
  CHEAP 208 (2022-12-02 on); the one-off readings move up to 47 classes, all before 2023-03-03, the margin step 38; built in a new session
  without opening the 2008-2021 outcomes or findings (retro/README.md, "CRM 2022-2026").
  SCHW (The Charles Schwab Corporation, Nasdaq: SCHW), the first securities broker, is a full-data batch: `www.sec.gov` accepted a plain
  client name (no contact address) in its session. Revenue is net revenues, continuing operations (U.S. Trust discontinued from the FY2006
  10-K; the earlier 10-Ks include it, a seam in rule T); EPS is GAAP diluted EPS from continuing operations (no filing publishes a figure
  excluding one-offs on that basis; Q3 2008's $.04 of securities charges stay in, FY08 $1.06); FY2002 is excluded by the AAPL test ($287M
  of excluded items after tax against $117M of continuing income), so the history and the P/E window start with FY2003; no filing guides
  revenue, EPS or a margin (the 2009 expense goal of cuts of 7 to 8% of 2008's spending is a cost component, unencoded), so the last full
  year's EPS stands and BASE is the latest quarter's revenue growth plus the buyback; the earnings 8-Ks were accepted during the session,
  so each print keeps its day, and the Friday Q4 2008 print dates its own week (the UNP Good Friday rule, "released during the session");
  the signals are net revenue, client assets, the expense gap, daily average revenue trades and the pre-tax margin, from the FY2006 10-K's
  own key metrics, with Schwab's rule-T thresholds over 1997-2006; dividends $0.05 and $0.06 a quarter from the 10-Qs that first state them;
  DURABLE, no live theme; CHEAP and BUY on all 105 dates, and no tested encoding but the signals at BEAR (13 classes) moves a class
  (retro/README.md, "SCHW").
  From 2010: the listing moves to the NYSE on 2010-03-05, as the FY2009 10-K states (`listings`, the PEP encoding); EPS stays GAAP every
  year (FY09 $0.68, FY10 $0.38, FY11 $0.70, FY12 $0.69), as the releases' figures excluding the YieldPlus and other charges are net income
  in dollars, never per share (FY2010 kept at $0.38 is the batch's largest call: a derived $0.65 moves 67 of 209 classes); Q1 2010 is
  restated twice, from the 8-K of 2010-04-20 ($172M reserve) and the Q1 2010 10-Q (`restated`, the JPM encoding, now in `build_schw.py`);
  the Q1 2010 and Q3 2013 outlooks are bounds and words ("at least", "mid-$.70s"), text only (`outlook_words`), and two outlook press
  releases were never filed (unused); optionsXpress (2011) and the 2012 preferred stock as published; from 2012-11-02 the "why" quotes every
  live theme's scope; CHEAP 90, FAIR 48, RICH 71 of 209 dates; decided in the session that scored 2008-2009, disclosed (retro/README.md,
  "SCHW 2010-2013").
  From 2014: GAAP every year (FY13 $0.78, FY14 $0.95, FY15 $1.03, FY16 $1.31), as the Q3 2015 to Q4 2016 releases' "EPS Impact of
  Certain Non-Recurring Items" tables give each item's per-share effect, never an EPS without them (the derived FY15 $0.97 and FY16 $1.30
  move 4 classes, the batch's largest call); from Q3 2014 the earnings 8-Ks are accepted after the close and dated the next trading day,
  and the two that land on a Friday (Q2 2015, Q3 2015) meet that Friday's close (the AVGO and CRM rule, now in `build_schw.py`); no guide in
  a range or a level (the Q1 2015 expense outlook is words, `outlook_words`; the March 2015 press release, the February business updates and
  the CFO commentary were never filed, unused); dividends $0.07 from the Q1 2016 10-Q and $0.08 from the FY2016 10-K; FY2003 and the FY2002
  note leave with the FY2013 10-K; from ECOMMERCE's live date the "why" names each live theme's subject, and the FY2015-FY2016 10-Ks' one
  cloud sentence (an accounting standard) is quoted (`cloud_words`, text only); DURABLE, no live theme; RICH 200, FAIR 8 of 208 dates, as
  BEAR stays FY09-FY10's -44.1%/yr and the ten-year median 24-26x; built in a new session without opening the 2008-2013 outcomes or
  findings (retro/README.md, "SCHW 2014-2017").
  From 2018: GAAP every year (FY17 $1.61 with the tax reform charge's $0.03, FY18 $2.45, FY19 $2.67, FY20 $2.12), as no filing prints an
  EPS excluding only one-offs and the releases' adjusted EPS from Q2 2020 also removes the amortization of acquired intangibles, which
  "will continue in future periods" (the AVGO, PFE and V rule; the adjusted FY20 $2.45 moves 23 classes); TD Ameritrade (2020-10-06),
  USAA's Investment Management Company and Wasmer Schroeder are in the figures as published, pro forma unused, so BASE runs +58% to
  +85%/yr on the four acquisition quarters' reported revenue growth (the batch's largest call: BASE at 0% there moves 50 classes); no
  guide in any filing (the business updates the releases cite were never filed, unused; the merger's year-three accretion and the proxy
  supplement's projections are no guide); revenue trades are not reported from the Q1 2020 release (only DATs, display only), so the
  trades signal is n/r and BASE through `schw2_engine.py.tmpl`, the None-tolerant copy (the BKR and SPGI encoding); dividends $0.10,
  $0.13, $0.17 and $0.18 a quarter from the 10-K or 10-Q that first states each; four Friday prints meet their own Friday; CRYPTO (live
  2020-10-21, scoped to banks) stays off the watch list, as no Schwab 10-K names crypto (text only); DURABLE; CHEAP 135, RICH 42, FAIR 32 of
  209 dates; built in a new session without opening the 2008-2017 outcomes or findings (retro/README.md, "SCHW 2018-2021").
  From 2022: Item 6 is reserved, so each 10-K vintage takes three years from the MD&A overview and the statements of income, earlier
  years from the latest earlier vintage (no restatement); GAAP every year (FY21 $2.83, FY22 $3.50, FY23 $2.54, FY24 $2.99, FY25 $4.65), as
  the releases' adjusted EPS also removes the recurring amortization of acquired intangibles (the adjusted figures move 69 classes, the
  batch's largest call; FY2023 without only its restructuring and integration costs 22); the Q1 2023 breakage fee and the Q4 2023 FDIC
  special assessment stay in; no guide in any filing (the business updates and CFO commentary were never filed, unused; the 2023 cost
  savings are a cost component); the 8-K's acceptance dates each print, though from Q1 2023 the release hosts its business update "this
  morning" (the AVGO Q3 FY11 rule; 1 class), and three Friday prints meet their own Friday; dividends $0.20, $0.22, $0.25, $0.27 and $0.32
  a quarter from the filing that first states each; Forge Global (2026-03-02) as published; DURABLE; CLOUD and GENAI out of scope with the
  10-Ks' own cloud and AI words quoted (`cloud_reading`, `ai_words`, text only), and CRYPTO on the watch list from the FY2025 10-K
  (2026-02-27) on its digital-asset words and Schwab's own planned spot crypto trading (`crypto_quote`, `crypto_own_quote`: the JPM and V
  encodings, a factor pair netting to zero); the last date is 2026-11-20; RICH 122, CHEAP 96, FAIR 37 of 255 dates; built in a new
  session without opening the 2008-2021 outcomes or findings (retro/README.md, "SCHW 2022-2026").
  NEE (FPL Group, Inc., NYSE: FPL; NextEra Energy from 2010) is the series key and Yahoo's symbol; the models print FPL (the SPGI encoding),
  prices as traded (x4 for the 2020 split), the 2005 two-for-one split restating per-share facts published before it (`on_basis`). EPS is
  GAAP diluted before cumulative effects, except 1999 and 2000 at the company's figures excluding only one-offs (FY2002 10-K); every EPS
  guide of 2007-2009 is an adjusted range that also removes the mark-to-market effect of non-qualifying hedges (and OTTI from 2008),
  recurring items, so the guides are display only (the PEP 2008 core rule) and the last full GAAP year stands (FY06 $3.23, FY07 $3.27, FY08
  $4.07); BASE is the latest quarter's revenue as reported; the signals are FPL's energy sales, FPL's net income, revenue, EPS and the
  operating margin under rule T over 1997-2006; DURABLE, no live theme; RICH 53, CHEAP 32, FAIR 20 of 105 dates; the adjusted outlook as
  the anchor moves 21 classes and 39 tiers, the largest call (retro/README.md, "NEE").
  From 2010: NextEra Energy, Inc. from the 8-K of 2010-05-24 (`company_names`) and NYSE: NEE from its announced 2010-06-23 (`listings`,
  the SPGI encoding); six Friday releases date their own weeks; GAAP still (FY09 $3.97 to FY12 $4.56; every guide adjusted, display only),
  2000 at the company's figure in the FY2009 vintage; Q1 2013's EPS keeps the release's total with its discontinued gain (noted); from
  2012-11-02 the "why" quotes every live theme's scope (CLOUD out of scope); RICH 105, CHEAP 74, FAIR 30 of 209 dates (RICH on all 53 of
  2013); the adjusted anchor moves 29 classes and 62 tiers; decided in the session that scored 2008-2009, disclosed (retro/README.md,
  "NEE 2010-2013").
  From 2014: GAAP still (FY13 $4.47 to FY16 $6.25, on net income attributable to NEE; every guide adjusted, display only); FY2013 keeps
  its Maine hydro gain from discontinued operations, as NEE's own rule is EPS before the cumulative effect (the 10-Ks' continuing $4.03,
  then $3.93, display only; 5 classes); three Friday releases date their own weeks; the FY2016 10-K's missing FPL statistics come from the
  Q4 2016 release (`franchise_note`); ENERGY_TRANSITION is on the watch list from 2015-12-18 on the 10-Ks' words on NEER's oil and gas
  production assets and the greenhouse gas limits (the XOM and SO rule, text only); RICH 189, CHEAP 13 (early 2015, on Q4 2014's revenue
  with hedge marks), FAIR 6 of 208 dates; the signals at BEAR move 19 classes; built in a new session without opening the 2008-2013
  outcomes or findings (retro/README.md, "NEE 2014-2017").
  From 2018: GAAP still (FY17 $11.38, then $11.39 restated, with the tax reform and FiberNet gains; FY18 $13.88 with the NEP
  deconsolidation gain; FY19 $7.76; FY20 $1.48 after the split), as the mirror of the AAPL FY2002 test is not met on the company's net
  after-tax lines (FY2018 by $40 million; the 10-K's gross components would meet it) and no filing excludes only the one-offs: the
  batch's largest call (the adjusted $6.70 and $7.70 move 100 classes, every CHEAP and FAIR date); every guide adjusted, display only;
  from the Q4 2017 release no filing tabulates FPL's energy sales or customer accounts, so the signal is n/r through `nee2_engine.py.tmpl`,
  the None-tolerant copy (`nr_engine`, the BKR, SPGI and SCHW encoding; 22 classes at BEAR); the four-for-one split effective 2020-10-27
  is the second `splits` record (prices as traded, earlier per-share facts divided by 4, from the 8-K of 2020-09-14); the FY2020 10-K
  omits Item 6, so 2018-2020 come from its statements; Gulf Power (2019) in the figures as published; five Friday releases date their
  own weeks; ENERGY_TRANSITION stays on the watch list (text only); RICH 109, CHEAP 93 (2018-2019, on the GAAP gains), FAIR 7 of 209 dates;
  built in a new session without opening the 2008-2017 outcomes or findings (retro/README.md, "NEE 2018-2021").
  From 2022: GAAP still (FY21 $1.81 to FY25 $3.30), as each Q4 release's after-tax one-off items (the hedge and decommissioning-fund
  marks left out as recurring) meet neither the AAPL FY2002 test nor its mirror; the FY2021-FY2025 10-Ks reserve Item 6, so each vintage
  takes three years from its statements; every guide adjusted, display only, the current-year ranges of four Item 7.01 8-Ks (2022-06-14,
  2024-06-11, 2025-12-08, 2026-01-02) included, each quote cut to the current year's range; the Q4 2021 print's year-ago EPS is $0.00, so
  its EPS growth is None (n/m, the F rule) through `nee3_engine.py.tmpl` on its 12 dates; four Friday releases date their own weeks; the
  Dominion Energy merger agreement (8-K of 2026-05-18, not closed by the last date) adds nothing; ENERGY_TRANSITION stays on the watch
  list on the 10-Ks' natural gas and oil words (text only), GENAI and GLP1 out of scope; "XPLR Infrastructure" joins the anachronism list;
  CHEAP 99, RICH 95, FAIR 61 of 255 dates; FY2021-FY2025 at the adjusted EPS moves 121 classes, the batch's largest call; the last date
  is 2026-11-20; built in a new session without opening the 2008-2021 outcomes or findings (retro/README.md, "NEE 2022-2026").
  NEM (Newmont Mining Corporation, NYSE: NEM), the first gold miner, a full-data batch: EPS is GAAP diluted EPS from continuing
  operations before the cumulative effect, each year from the latest filing that reports it, with two 8-K recasts as vintages of their
  own (2007-10-16, Merchant Banking discontinued; 2009-09-15, FSP APB 14-1, FAS 160 and Kori Kollo); 1998-2001 are losses, so FY2001
  takes the years before it and the history and the P/E window start with FY2002 (the MU FY2003 rule); FY2007 ($(2.13), $1,544M of listed
  after-tax charges, no per-share figure without them) is excluded as the latest year, a gap ("ex-FY07"); the releases' adjusted net
  income (FY07 $1.33, FY08 $1.99 in the Q4 2008 release) also removes recurring legacy closure obligations and securities write-downs, so
  GAAP stands (the PEP 2008 core rule); anchors FY06's $1.18, then $1.25 (FY2007 10-K), FY08's $1.82, then $1.80 (recast); the equity
  gold sales, unit-cost and cost-component outlooks are display only (the XOM production and MSFT segment rules), so BASE is the latest
  quarter's revenue growth; signals gold ounces sold, costs applicable to sales per ounce (lower is better), revenue, EPS and the pre-tax
  margin under rule T over 1997-2006 (the old Newmont's 10-Ks, CIK 71824, for 1997-2000); DURABLE, no live theme; CHEAP and BUY on all
  105 dates, as the stock's own 2002-2009 window (median 42-47x on the low 2002-2006 earnings) is the call they rest on; no tested
  encoding moves a class but the signals at BEAR (2) (retro/README.md, "NEM"). From 2010: the FY2009-FY2012 vintages (ten fiscal
  years to the latest; FY2002 and the FY2001 note leave with the FY2012 10-K), GAAP still (FY09 $2.68, FY10 $4.61, FY12 $3.78); FY2011 is
  excluded by the AAPL FY2002 test (the $1,609M Hope Bay write-down and other listed items, $1,668M net, exceed its $502M continuing
  income; the adjusted $4.39 also removes recurring items), as the latest year and then a gap, so FY10's $4.61 stands to 2013-02-15
  ("ex-FY07 ex-FY11"); from Q1 2010 the releases tabulate ounces produced, not sold, so the ounces signal reads consolidated ounces
  produced (`oz_basis`) through `nem2_engine.py.tmpl`, which names it; the Q4 2011 and Q4 2012 releases print the year only, so sales,
  EPS and shares come from the 10-K's quarterly data and pre-tax income is the year less the nine months (`source_10k`); after-close
  releases on a Thursday date the Friday (the AVGO, CRM and SCHW rule); dividends $0.15 to $0.425 a quarter (the gold price-linked policy)
  from the first release that states each as approved, winning over the vintage's; outlooks display only; DURABLE, CLOUD out of scope
  (every live theme's scope quoted from 2012-11-02); CHEAP and BUY on all 209 dates, robustness 8 of 8, and no tested encoding moves a
  class (a five-year window and the signals at BEAR included); built in a new session without opening the 2008-2009 outcomes or
  findings (retro/README.md, "NEM 2010-2013"). From 2014: five more vintages (the FY2013-FY2016 10-Ks and the 8-K of 2014-06-13
  recasting the FY2013 10-K's Items 6-8, a vintage of its own; FY12 $3.78 to $3.76), GAAP still; FY2013 ($(5.06)) and FY2016 ($(0.41))
  are losses and FY2015 ($0.38) fails the AAPL FY2002 test ($314M of listed items against $193M; the FY2011 encoding), each excluded as
  the latest year and then a gap ("ex-FY13 ex-FY15 ex-FY16"), so FY14's $1.10 (then $1.30 as the FY2016 10-K restates it, Batu Hijau
  discontinued; 2007-2011 keep it, a seam) anchors 2015-02-20 on; from Q2 2014 the ounces signal reads consolidated gold ounces sold
  again (the costs applicable to sales reconciliation's denominator, rule T's line) through the original engine; the unfiled dividend cut
  of 2014-02-19 waits for the Q1 2014 release ($0.025, then $0.05 and $0.075); ECOMMERCE, STREAMING and ENERGY_TRANSITION are out of
  scope, the 10-Ks' climate risk factor quoted (`climate_words`, text only); CHEAP 105 (2014-2015), FAIR 6, RICH 98 (2016-2017) of 209
  dates; the adjusted EPS moves 22 classes, a five-year window 22, the signals at BEAR 29, all in 2015; built in a new session without
  opening the 2008-2013 outcomes or findings (retro/README.md, "NEM 2014-2017"). From 2018: five more vintages (the FY2017-FY2020 10-Ks and the
  8-K of 2018-04-26 re-filing the FY2017 10-K's Items 1, 2, 6, 7 and 8, a vintage of its own; FY14 $1.30 to $1.28), the FY2020 10-K's
  three years from its statements (no Item 6), GAAP still; FY2017 ($(0.11), then $(0.14)) is a loss, FY2018 ($0.53) fails the AAPL FY2002
  test ($438M of listed items, every line summed, against $280M) and FY2019 ($3.91) its mirror (the $2,390M Nevada Gold Mines gain; $1,907M
  of net benefits against $970M), each excluded as the latest year and then a gap, so FY14's $1.28 anchors to 2021-02-12 ("ex-FY15 ex-FY16
  ex-FY17 ex-FY18 ex-FY19") and FY2020's $3.31 (kept: its benefits under half its income without them) from 2021-02-19; Goldcorp
  (2019-04-18) and Nevada Gold Mines (2019-07-01) as published, so BASE runs +36-57% on the acquisition quarters; the Q4 2019 and Q2 2020
  prints' year-ago EPS is $0.00, so their EPS growth is None (n/m) through `nem3_engine.py.tmpl`; Newmont Goldcorp Corporation from
  2019-04-22 and Newmont Corporation from 2020-01-07 (`company_names`, the CB encoding); CYCLICAL from the FY2018 10-K's "The metals
  markets are cyclical" (the CB rule); dividends $0.14 to $0.55 a quarter, the 2019 special dividend not a rate; EV and CRYPTO out of
  scope, the FY2020 10-K's crypto words quoted (`crypto_words`, text only); RICH 183, CHEAP 15, FAIR 11 of 209 dates; a five-year window
  moves 58 classes, FY2018 and FY2019 kept at GAAP 48; built in a new session without opening the 2008-2017 outcomes or findings
  (retro/README.md, "NEM 2018-2021"). From 2022: five more vintages (the FY2021-FY2025 10-Ks, Item 6 reserved, so three years from each
  statement of operations; the 10-K/A of 2022-07-28 and the segment recast 8-K of 2023-07-20 change no figure the models read, so neither
  is a vintage), GAAP still; FY2021 ($1.39) fails the AAPL FY2002 test (the Q4 2021 release's $1,262M of listed items, the Yanacocha
  reclamation charges above all, against $1,109M) and FY2022 ($(0.58)) and FY2023 ($(3.00)) are losses, each excluded as the latest year
  and then a gap, so FY20's $3.31 anchors to 2025-02-14, FY24's $2.86 (kept) from 2025-02-21 and FY25's $6.39 (kept) from 2026-02-20; the
  Q4 2023 release came a week before its 10-K, so its preliminary year ($(2.97), a loss) extends the vintage from the print
  (`fy_actual`, the NEE and LYB encoding, new in `build_nem.py`; one date); from Q1 2024 the releases' statements are quarterly columns,
  read by position with the header asserted; from Q4 2025 the costs applicable to sales signal reads the 'Summary of Results' table's
  co-product line (the reconciliation gives the by-product figure only); diluted shares from each release; Newcrest (2023-11-06) and the
  divestitures as published (BASE +24% to +85% on the Newcrest quarters); releases after the close from Q2 2024 (the AVGO, CRM and SCHW
  rule); dividends $0.55 to $0.26 a quarter, $0.25 from the FY2023 10-K; GENAI and GLP1 out of scope, the FY2023-FY2025 10-Ks' AI words
  quoted (`ai_words`, text only); the last date is 2026-11-27 (built after that day's early close, a week past the other 2022-2026
  batches); CHEAP 139, RICH 106, FAIR 11 of 256 dates; FY2021 kept at GAAP moves 108 classes, the adjusted EPS 103-110; built in a new
  session without opening the 2008-2021 outcomes or findings (retro/README.md, "NEM 2022-2026").
  LYB (LyondellBasell Industries N.V., NYSE: LYB) has no 2008-2009 dates: no LYB share existed (the company was formed on 2009-10-15
  and its capital issued on 2010-04-30, at the emergence of LyondellBasell AF's businesses from bankruptcy; the predecessor was private,
  and Lyondell Chemical's NYSE: LYO stock was delisted on the 2007-12-20 Basell acquisition), and neither LYO's nor the predecessor's
  history was substituted. From the share issue (the P/E window from 2010-04-30; Pink Sheets to 2010-10-13, NYSE from 2010-10-14) 2010
  is two periods (the Predecessor to April 30, the Successor after fresh-start accounting) and not a year of EPS, its days out of the
  window ("ex-FY10"), so no date precedes the first full year (FY2011, released Friday 2012-02-10 during the session, which dates its own
  week); the 93 weeks between are the owner's call. The combined 2010 that each 10-K's MD&A prints is a year of revenues (and in rule T),
  never of EPS. EPS is GAAP diluted from continuing operations (the adjusted EPS also removes recurring items: the warrants' mark to
  market, impairments, inventory adjustments); the Q2 2012 release's Berre refinery in discontinued operations restates FY2011 to $4.32
  until the FY2012 10-K (`restates`); no filing guides revenue, EPS or a margin, so the last full year's EPS stands and BASE is the latest
  quarter's revenue growth; signals O&P–Americas and Intermediates & Derivatives operating income (the FY2010 10-K's two largest),
  revenue and two GAAP margins, rule T over the 2007-2011 values the first date's filings report; CYCLICAL on the 10-Ks' own words, no
  live theme; dividends from the first filing that states each interim rate (specials are not a rate); RICH and AVOID on all 100 dates,
  robustness 8 of 8, and no tested encoding moves a class (retro/README.md, "LYB"). From 2014: GAAP still (FY13 $6.76, FY14 $8.00,
  FY15 $9.60, FY16 $9.15), as Table 1's figures "Excluding LCM Impact" remove the lower of cost or market adjustments, which recur
  (23 classes); every year passes the one-off test; still no guide in numbers (each outlook is words); the releases' new table layout
  from Q1 2014 is read by title; the ten fiscal years to the latest one (2006 leaves with the FY2016 10-K), 2010 still the combined
  $38,939M; dividends $0.60-$0.90 a quarter, each from the release that first states it; the annual meetings' repurchase authorities
  display only; CYCLICAL on the 10-Ks' "cyclical and volatile nature" risk factor; ENERGY_TRANSITION on the watch list from 2015-12-18
  through the Refining segment and the 10-Ks' GHG sentence ("could significantly increase our costs or reduce demand for products we
  produce"; text only, the KMI encoding); RICH 183, CHEAP 21, FAIR 5 of 209 dates; the frozen rule-T signals are the largest call (at
  XBULL 129 classes move); built in a new session without opening the 2012-2013 outcomes or findings (retro/README.md, "LYB 2014-2017").
  From 2018: GAAP still (FY17 $12.28 with the U.S. tax reform benefit, as the release gives the items' per-share effect, never an EPS
  without them, and the mirror of the AAPL FY2002 test is not met: $816M of net after-tax benefits against $4,879M; FY18 $12.03, FY19
  $9.60, FY20 $4.25 with the Houston refinery impairment), each Q4 release's net-income figure until its 10-K; from Q1 2018 the releases
  drop the income statement and charges tables, so pre-tax income is income from continuing operations plus the provision from the
  EBITDA reconciliation, the one-off test sums the after-tax items each Q4 release lists, and the four releases with no consolidated
  operating income (Q1-Q2 2018, Q2-Q3 2021) take it from the 10-Q accepted the same Friday during the session (`oi_source`); Advanced
  Polymer Solutions (A. Schulman, from Q3 2018) recasts O&P–Americas, the frozen signals unchanged; still no guide in numbers (the 8-K
  of 2020-04-15's preliminary net income range is no print and no field); the ten fiscal years to the latest one, shares included (the
  2010 count and the combined 2010 leave with the FY2020 10-K); dividends $1.00, $1.05, $1.13 from the releases that first state them;
  EV and CRYPTO out of scope, the 10-Ks' one cloud words quoted (`cloud_quote`, text only), ENERGY_TRANSITION on the watch list on the
  FY2020 10-K's new GHG words; RICH 108, CHEAP 82, FAIR 19 of 209 dates; the frozen signals at XBULL move 71 classes, FY2017 at a derived
  $10.23 45; built in a new session without opening the 2012-2017 outcomes or findings (retro/README.md, "LYB 2018-2021") From 2022:
  GAAP still (FY21 $16.77, FY22 $11.83, FY23 $6.48, FY24 $4.14), as the company's EPS excluding identified items also removes recurring
  write-downs and LCM (26 classes); FY2025 ($(2.48) from continuing operations) is a loss, excluded as the latest year ("ex-FY25"; the MU
  and NEM rule, `eps_gaap`); Item 6 reserved, so each vintage takes three years from its statements, and the EPS history is cut to the ten
  years (new; 10 classes); the FY2025 10-K restates FY23-FY24 without the refining business, discontinued from Q1 2025 (FY24 $4.39), as
  published; no release prints a consolidated operating income, so Q1-Q3 take it from the same-day 10-Q and the Q4 prints' operating
  margin (and Q4 2025's pre-tax margin) is n/r through `lyb2_engine.py.tmpl`, the None-tolerant copy; Q3 2026's year-ago segment quarter
  is the Q3 2025 release's (its tables print none); still no guide in numbers (the 2027 targets are mid-cycle aspirations); dividends
  $1.19-$1.37, then $0.69 from the FY2025 10-K; GENAI and GLP1 out of scope (`ai_quote`), ENERGY_TRANSITION out of scope from the FY2025
  10-K (`refining_exit_quote`); RICH 193, CHEAP 55 (2022, on FY21), FAIR 7 of 255 dates; the last date is 2026-11-20; built in a new
  session without opening the 2012-2021 outcomes or findings (retro/README.md, "LYB 2022-2026").
  CHTR (Charter Communications, Inc., CIK 1091667) is set up in staging with no date built: its fact sheet, generator
  (`retro/generators/chtr/`), gate builder (`retro/build_chtr.py`) and engine (`chtr_engine.py.tmpl`, the cable engine with every
  threshold unset) exist, and the builder refuses every weekly date of 2008-01-04 to 2013-12-31 (314) with its reason
  (`staging/retrospective/CHTR/GATE.md`). Every fiscal year from 1999 to 2013 is a loss per share, so no year anchors a P/E (the F, MU and
  CRM loss rule); 2009 is reported as the Predecessor's eleven months ($12.61, the Plan and fresh start gains) and the Successor's
  December ($0.02), neither a year (the CTVA 2017 rule); from the 2009-11-30 emergence only the Successor's years count (the BKR 2018
  rule); and Yahoo's CHTR series starts on 2010-01-05 (the new Class A, OTC: CCMM, then NASDAQ: CHTR from 2010-09-14), so 2008-2009 has
  no close either (the old Class A was suspended from NASDAQ on 2009-04-07 and cancelled on 2009-11-30). The first buildable date lies
  after 2013 and was not determined; annualizing December 2009 or anchoring on the eleven months would be a new rule, the owner's call
  (retro/README.md, "CHTR", "CHTR 2008-2009"). 2014-2017 cannot be built either, so the gate refuses all 523 weekly dates of
  2008-01-04 to 2017-12-29 (a full-data batch, `gen_chtr_1417.py` appending the FY2014-FY2016 10-Ks and Q4 releases): 2014 $(1.70) and
  2015 $(2.43) are losses (recast to $(1.88) and $(2.68) by the FY2016 10-K for the 0.9042 Parent Merger Exchange Ratio of 2016-05-18,
  which Yahoo's series records no event for and which is recorded, not encoded), and FY2016's $15.94, the only positive year, carries the
  "approximately $3.3 billion" valuation allowance reversal the 10-K calls non-recurring against $222M of income without it, with no
  figure excluding only it, so it is excluded by the mirror of the AAPL FY2002 test (the batch's deciding call: kept, 46 dates of 2017
  would pass; the Q4 2016 release's pro forma $3.91 is unused); a Q4 release's year extends its vintage until the 10-K (`q4_actuals`),
  the later vintages' years are the priced shares' (`priced_issuers`); no guide, no dividend; the engine is unchanged (no signal or rule-T
  value derived); the first buildable date lies after 2017 and was not determined, as FY2017's 2018 filings were not read
  (retro/README.md, "CHTR 2014-2017"). From 2018 (a full-data batch, `gen_chtr_1821.py`): FY2017's $34.09 carries the "approximately
  $9.3 billion" Tax Reform benefit against $595M of income without it, so it is excluded by the mirror test and the 56 weekly dates of
  2018-01-05 to 2019-01-25 are refused; FY2018's GAAP $5.22 (the Q4 2018 release and the FY2018 10-K, the morning of 2019-01-31) is the
  first anchor, so the first built date is 2019-02-01 and 153 dates are built to 2021-12-31; FY2017 not being the latest year once FY2018
  is in, the history and the P/E window start with 2018 (`history_start`; the bounds rule on the first vintage), FY18-FY20 GAAP ($5.22,
  $7.45, $15.40); no guide in numbers (the capex outlooks are words, display only), so BASE is the latest quarter's revenue growth plus
  the net buyback; prices as traded, and the 2016-05-18 Parent Merger Exchange Ratio precedes every day a model reads, so it needs no
  encoding (asserted); the engine has CHTR's own signals (total customer relationships, the first customer line of every release,
  revenue, the Adjusted EBITDA margin, capital intensity, the operating margin) with rule T over the FY2018 10-K's decade, the
  Successor's 2011-2018 changes; DURABLE (the 10-Ks' "seasonal and cyclical variations" are advertising and seasonal-area patterns),
  STREAMING on the watch list from each 10-K's online-video words (the CMCSA encoding); no dividend; RICH 77, CHEAP 66, FAIR 10 of 153
  dates; FY2017 kept at GAAP moves 56 classes, the batch's largest call (retro/README.md, "CHTR 2018-2021"). From 2022: the 10-Ks reserve Item 6, so each vintage takes
  three years from its statements of operations and the earlier years from the latest earlier vintage (`statement_years`,
  `carried_from`); GAAP every year (FY21 $24.47 to FY25 $36.21; no year near the one-off tests); no guide in numbers (the capex outlooks
  are in dollars from 2022, a cost component, display only); Adjusted EBITDA from the releases' reconciliation of non-GAAP measures from Q2
  2022; all 20 prints before the open on a Friday; the Cox Transactions (closed 2026-08-19) in the Q3 2026 actual figures as published,
  pro forma unused, the year-ago customer relationships from the addendum's actual summary (`basis_note`); STREAMING stays on the watch
  list on each 10-K's words, GENAI and GLP1 out of scope (the FY2023-FY2025 10-Ks' AI sentence quoted, `ai_quote`, text only); CHEAP and
  BUY on all 255 dates, and no tested encoding (a five-year window included) moves a class; the last date is 2026-11-20; built in a new
  session without opening the 2019-2021 outcomes or findings (retro/README.md, "CHTR 2022-2026").
  FANG (Diamondback Energy, Inc., CIK 1539838, NASDAQ: FANG) is set up in staging with no date built: its fact sheet, generator
  (`retro/generators/fang/`), gate builder (`retro/build_fang.py`) and engine (`fang_engine.py.tmpl`, the XOM engine with every
  threshold unset and placeholder producer signals) exist, and the builder refuses every weekly date of 2008-01-04 to 2013-12-31 (314)
  with its reason (`staging/retrospective/FANG/GATE.md`). The stock first traded on 2012-10-12 (Yahoo's series starts there), so
  2008-2012-10-05 has no close; the predecessors (Windsor Permian LLC and Windsor UT LLC, controlled by Wexford Capital) were limited
  liability companies with no shares and are never substituted (KMI, CTVA, LYB); and no filing to 2013-12-31 prints a GAAP EPS for any
  full year: the offering documents and the FY2012 10-K print only pro forma per-share figures (2011 $(0.04), 2012 $0.60), which are
  unused (the CTVA and CHTR rule), and FY2012 is a GAAP net loss ($36.5M) whose $54.1M first-day deferred tax charge of the Merger exceeds
  its $18.4M of income before income taxes (the AAPL FY2002 test). The first full year of the company's own EPS is FY2013, in filings
  accepted 2014-02-19 after the close (not read), so the first buildable date lies after 2013-12-31 and was not determined; counting the
  pro forma $0.60 would let 44 dates (2013-03-08 to 2013-12-31) pass the gate, the batch's deciding call and the owner's
  (retro/README.md, "FANG", "FANG 2008-2009"). From 2014 (a full-data batch, `gen_fang_1417.py`): FY2013's GAAP $1.29 (the FY2013 10-K
  and the Q4 2013 release, both after the close on 2014-02-19) is the first anchor, so the 7 dates of 2014-01-03 to 2014-02-14 stay refused
  and 202 are built, 2014-02-21 to 2017-12-29; EPS is GAAP diluted on net income attributable to Diamondback, the one-off test on each Q4
  release's listed items (impairment, debt extinguishment, asset sales) with the non-cash derivative marks read as recurring (the NEE and
  PEP 2008 core rule), so FY13 $1.29 and FY14 $3.64 are kept and FY2015 $(8.74) and FY2016 $(2.20), losses after the full cost ceiling
  impairments, are excluded as the latest year and then gaps ("ex-FY15 ex-FY16"; the adjusted $1.81 and $1.87 also remove the marks), so
  FY14's $3.64 anchors from 2015-02-19; the window runs from the 2012-10-12 listing less 2012 (no GAAP EPS), and the bounds rule covers the
  two-year history; no guide in numbers (production, unit cost and capex outlooks only), so BASE is the latest quarter's revenue growth plus
  the net buyback (share issuance, -17% to -21%/yr); the engine is now the LYB engine with FANG's own signals (oil-equivalent and oil
  production, revenue, LOE per BOE, the pre-tax margin) and rule T over the 2009-2013 changes the FY2013 and FY2012 10-Ks report, the
  Predecessors' years as published; CYCLICAL on the 10-Ks' "The oil and natural gas industry is cyclical", ENERGY_TRANSITION on the watch list
  from 2015-12-18 on the climate legislation risk factor (text only); no dividend; Viper Energy Partners as consolidated; FAIR 104, CHEAP 81,
  RICH 17 and BUY on all 202 dates; the derivative marks call (FY13-FY14 at the adjusted $1.21 and $2.24) moves 75 classes, the losses kept
  at the adjusted figures 56 classes and 63 tiers (retro/README.md, "FANG 2014-2017"). From 2018 (a full-data batch, `gen_fang_1821.py`): FY17 $4.94 and
  FY18 $8.06 are kept (GAAP; the one-off test on each Q4 release's listed items, the derivative and investment revaluation marks read as
  recurring), FY2019 ($1.47) is distorted by the AAPL FY2002 test (the $790M impairment and $56M debt loss against $362M of pre-tax income)
  and FY2020 ($(28.59)) a loss, each excluded as the latest year and then a gap ("ex-FY19 ex-FY20"), so FY18's $8.06 anchors from
  2019-02-21 to the last date; ten fiscal years from each latest filing (the FY2020 10-K reserves Item 6, so three statement years and
  the rest carried); still no guide in numbers, so BASE is the latest quarter's revenue growth plus the net share change; the dividend
  ($0.50 from the Q4 2017 release to $2.00 from Q3 2021, each from the release that first states it); ENERGY_TRANSITION stays on the watch
  list (the FY2020 10-K's Item 1 climate sentence once the risk factor heading is gone), EV and CRYPTO out of scope; Energen, Rattler,
  Guidon and QEP as published; CHEAP and BUY on all 209 dates (2018-01-05 to 2021-12-31); FY2019 kept at GAAP moves 93 classes and 67
  tiers, the batch's deciding call; built in a new session without opening the 2014-2017 outcomes or findings (retro/README.md,
  "FANG 2018-2021"). From 2022 (a full-data batch, `gen_fang_2226.py`): FY21 $12.30 (restated to $12.24 by the two-class method from the
  Q4 2022 release, `prior_eps_gaap`), FY22 $24.61, FY23 $17.34 and FY24 $15.53 are kept (GAAP; the one-off test on each Q4 release's
  listed items, the derivative marks recurring), FY2025 ($5.73) is distorted by the AAPL FY2002 test (the $3,652M Q4 2025 impairment
  against $1,874M) and excluded as the latest year ("ex-FY25"), so FY24's $15.53 anchors from 2025-02-26 to the last date; each 10-K
  reserves Item 6 (three statement years, the rest carried); still no guide in numbers (BASE the latest quarter's revenue growth plus the
  net share change, the Endeavor shares in as published); the base dividend ($2.40 to $4.72, each from the filing that first states it,
  the merger 8-K of 2024-02-12 and the Q1 2026 letter included), the variable dividends not a rate; the Item 2.02 8-Ks without a release
  are no print; ENERGY_TRANSITION stays on the watch list, EV, GENAI and GLP1 out of scope (the 10-Ks' electric vehicle and AI words
  quoted, `ev_quote`, `ai_words`, text only); Rattler, Viper, Endeavor and Double Eagle as published; CHEAP 173, RICH 66, FAIR 17 of 256
  dates; the frozen signals at XBULL move 82 classes, FY2025 kept at GAAP 17 classes and 40 tiers; the last date is 2026-11-27 (built
  after that day's early close, the NEM rule); built in a new session without opening the 2014-2021 outcomes or findings
  (retro/README.md, "FANG 2022-2026").
  TRGP (Targa Resources Corp., NYSE: TRGP) has no 2008-2009 dates: its common stock listed on 2010-12-07 ("No public market currently
  exists for our common stock", the IPO prospectus) and 2008-2009 have no EPS to common shareholders; Targa Resources Partners LP (NYSE:
  NGLS), which TRC controls and consolidates, is a separate listed partnership, and its unit prices and per-unit history were not
  substituted (what TRC's filings consolidate is in as published). From the listing 2010 is a loss per share ($(30.94), the pre-IPO
  recapitalization), excluded with its days out of the window ("ex-FY10"), so no date precedes the first full year (FY2011, $0.74, the Q4
  2011 release of 2012-02-23): the 63 weeks between are the owner's call, and the builder refuses every earlier date with its reason.
  EPS is GAAP diluted (no figure excluding one-offs is published; FY2011 and FY2012 pass the one-off test); no filing guides TRC's revenue,
  EPS or a margin (the outlooks are the Partnership's Adjusted EBITDA and TRC's dividend growth, display only), so BASE is the latest
  quarter's revenue growth plus the buyback; shares from 2011 (2010's 6.5M is pre-conversion); signals the Partnership's Gathering and
  Processing and Logistics and Marketing segment operating margins, revenue and two GAAP margins, rule T over 2007-2011; DURABLE (the
  distribution policy's "seasonal and cyclical factors" read as boilerplate, the CHTR reading), no live theme; RICH 88, FAIR 9, CHEAP 1 of
  98 dates (the GAAP EPS of a general partner's holding company is small against its dividends, so its own short window prices it at
  57-97x); the dividend outlook as BASE and FY2010's pre-IPO share count are the largest calls (10 classes each) (retro/README.md,
  "TRGP", "TRGP 2008-2009", "TRGP from the first full year"). From 2014 (a full-data batch, `gen_trgp_1417.py` appending to the
  2012-2013 sheet, every earlier fact asserted unchanged): GAAP still (FY13 $1.55, FY14 $2.43, FY15 $1.09); FY2015 is kept on the one
  item its release states on TRC's basis (the goodwill impairment's $25.6M against $58.3M; the batch's largest EPS call: 75 classes if
  excluded), and FY2016 ($(1.80); the Q4 2016 release prints only the net loss, so `eps_gaap` None) is a loss, excluded as the latest
  year and then a gap ("ex-FY10 ex-FY16"); the Atlas mergers (2015-02-27) and the buy-in of the Partnership's public common units
  (2016-02-17, 104.5M TRC shares) are in the figures as published, so the buyback reads -23.1%/yr of dilution from the FY2016 10-K; TRC's
  own releases from Q1 2016 print no EPS or shares, which come from each 10-Q (Q4 2016 from the 10-K's quarterly data) from its own date
  (`restated`, the JPM and SCHW encoding), n/r before through `trgp2_engine.py.tmpl`; the 8-K of 2014-10-23 revises 2011-2013 revenues to
  the net basis of NGL buy-sell transactions (`revenue_restatements`, new); the recast 8-K of 2016-05-23 (two segments) is a vintage of
  its own; still no guide in numbers (dividend outlooks display only); ENERGY_TRANSITION out of scope (no reserves or refinery: the BKR
  reading, text only), ECOMMERCE and STREAMING named by no 10-K; CHEAP 107, RICH 61, FAIR 41 of 209 dates; the frozen signals at BEAR move
  96 classes; built in a new session without opening the 2012-2013 outcomes or findings (retro/README.md, "TRGP 2014-2017"). From 2018
  (a full-data batch, `gen_trgp_1821.py` appending to the 2012-2017 sheet, every earlier fact asserted unchanged): FY2017 $(0.31) (with the
  Tax Act benefit), FY2018 $(0.53), FY2019 $(1.44) and FY2020 $(7.26) are losses to common shareholders, each excluded as the latest year
  and then a gap, so FY15's $1.09 is the last full year on every date ("ex-FY16 ex-FY17 ex-FY18 ex-FY19 ex-FY20"); new: from the Q4 2018
  release each release reconciles its Adjusted EBITDA outlook to an estimated GAAP net income attributable to TRC, read as a GAAP earnings
  guide (the KMI 2019-2022 rule): less 4 x the release's quarter's Series A preferred dividends (cash and deemed), over the latest public
  basic share count, a loss guide leaving FY15's $1.09 (FY2019E, the 2020 updates from Q1 2020), so FY2020E $0.329 (11 dates) and FY2021E
  $0.699, $1.522, $1.740, $2.045; the releases print no EPS, so the 10-Qs' (Q4s from the next 10-K's quarterly data; Q4 2020 n/r, the FY2020
  10-K having none); Logistics and Marketing renamed Logistics and Transportation from Q4 2019, the same division; dividends $0.91, then
  $0.10 from the Q1 2020 release; the $500M repurchase program of 2020-10-05 unencoded; EV and CRYPTO out of scope (no 10-K names them),
  ENERGY_TRANSITION still out of scope with each 10-K's splitter and climate words quoted (text only); CHEAP 112, FAIR 57, RICH 40 of 209
  dates; the loss years kept at a pre-tax upper bound without their impairments move 106 classes, the signals at BEAR 80, the preferred
  deduction 55, the earnings-guide reading 14; built in a new session without opening the 2012-2017 outcomes or findings (retro/README.md,
  "TRGP 2018-2021"). From 2022 (a full-data batch, `gen_trgp_2226.py` appending to the 2012-2021 sheet, every earlier fact asserted
  unchanged): Item 6 is reserved, so each vintage takes three years from its statements, and the ten-year rule now cuts the EPS and share
  histories too (no earlier vintage changes); FY2021 $(0.07) is a loss, excluded; FY22 $3.88, FY23 $3.66 (with the $510.1M Grand Prix
  premium on repurchase of noncontrolling interests, 61% of its income), FY24 $5.74 and FY25 $8.49 are GAAP and kept; the estimated net
  income attributable to TRC stays the earnings guide, and new: from the Q1 2022 release (the Series A redeemed in full) the deduction is
  what the latest statement has recorded for the guide's year (deemed dividends, premiums), not 4 x the quarter, so FY22E $5.13 to $4.18,
  FY23E $5.43 to $3.97, FY26E $10.18 to $11.61; the 8-K of 2022-06-17's standalone estimate is a guide; the Q4 prints carry no full year
  (each 10-K is public by the week date; the builder refuses a date between); dividends $0.35 to $1.25 a quarter; DURABLE (no 10-K says
  cyclical), GENAI and GLP1 out of scope with the 10-Ks' AI words quoted (`ai_text`, text only); CHEAP 153, RICH 71, FAIR 32 of 256
  dates; the earnings-guide reading moves 107 classes, the signals at BEAR 103; the last date is 2026-11-27 (built after that day's early
  close); built in a new session without opening the 2012-2021 outcomes or findings (retro/README.md, "TRGP 2022-2026").
  OKE (ONEOK, Inc., NYSE: OKE, CIK 1039684), a full-data batch: EPS is diluted EPS from continuing operations, each year from the latest
  filing that reports it, at the company's figures without the gains on sale for 2005 ($2.53) and 2006 ($2.40) (the FY2006 10-K; the
  ACN rule); FY2001 is excluded by the AAPL FY2002 test on the latest filing that reports it (the FY2005 10-K's $0.36 and $43.5M of
  continuing income against the FY2001 10-K's $72.0M of listed items, the OCC ruling and the Enron bankruptcy), taking the years before
  it, so the history and the P/E window start with FY2002 and the August fiscal years and the 1999 transition period stay out (kept,
  43 classes move: the largest call); current-FY EPS is the midpoint of ONEOK's latest 'net income guidance' range per diluted share
  (13 ranges from the releases and the Item 7.01 guidance 8-Ks; GAAP); no revenue or margin guide, so BASE is the latest quarter's
  revenue growth as reported (commodity revenues: +29-51% in 2008, -29% to -47% in 2009; on net margin 28 classes move); the signals are
  net margin, the Distribution segment's operating income, revenue and two margins, under rule T over 1997-2006 (fiscal 1997-1999 ended
  August 31; calendar 2000 against fiscal 1999, the BKR transition rule); Yahoo's 2012 split and its 2014 ONE Gas factor follow every
  date and are undone (the price as traded), the builder refusing dates from 2012-06-04; ONEOK Partners (NYSE: OKS) is never priced, its
  consolidation in as published; the live `oke_signal_model.py`, OKE's profile in `data/business_profiles.json`, `scripts/quality_classify.py` and `reports/*.json`
  are 2026 analyses, never inputs; DURABLE, no live theme; CHEAP 58, RICH 32, FAIR 15 of 105 dates (retro/README.md, "OKE"). From 2010:
  the Q4 2009 release files no earnings tables, so the quarter comes from the FY2009 10-K's quarterly data (pre-tax income the year less
  the Q3 2009 release's nine months, diluted shares the year's; `source_10k`, the NEM encoding); GAAP EPS from continuing operations every
  new year (FY09 $2.87, FY10 $3.10, FY11 $3.34, FY12 $1.64), the FY2011 10-K restating 2007-2010 for the retail marketing business
  (discontinued, sold 2012-02-01) while 2002-2006 stay as first reported (a seam); from the 2010 guidance ONEOK guides net income in
  dollars, so current-FY EPS is the range's midpoint over the diluted shares of the latest print public on the guide's date (the KMI rule,
  `ni_guide_m`, `shares_print`; words keep the last range); the 2012 two-for-one split is the `splits` record, effective 2012-06-04
  (Yahoo's date; the shared on_basis helper, each history year by its own filing's date, prices as traded), and the builder now refuses
  dates from 2014-02-03 (the ONE Gas factor); the FY2013 range after the energy services wind down ($235-285M, one-time charges in) is used
  as published, no range without them being filed; dividends $0.44 to $0.61, then $0.33 to $0.38 post-split, from the 8-Ks; FY2002 and
  the FY2001 note leave with the FY2012 10-K; CLOUD out of scope (every live theme's scope quoted from 2012-11-02), DURABLE; RICH 168,
  CHEAP 32, FAIR 9 of 209 dates (CHEAP and FAIR all in 2010; RICH on every date of 2011-2013 at 20-50x against a 14-16x median); BASE on
  net margin and the signals at BEAR move 41 classes each, all in 2010; built in a new session without opening the 2008-2009 outcomes or
  findings (retro/README.md, "OKE 2010-2013"). From 2014: the ONE Gas separation (one share for every four, after the close on 2014-01-31)
  is the `distributions` record, Yahoo's 11422:10000 factor of 2014-02-03 undone for the days before it (prices as traded, the window's
  earlier days with ONE Gas, the SO Mirant reading); the history keeps the distribution business until the FY2014 10-K restates 2010-2014
  from continuing operations (2010 $0.66 to 2014 $1.52; 2005-2009 as first reported, a seam that sets BEAR at -52.9%/yr); GAAP every new
  year (FY13 $1.27, FY15 $1.19, FY16 $1.67; listed items under half); from Q1 2014 no release reports a Distribution segment, so that
  signal is n/r and scored at BASE, and from Q4 2015 net margin is revenues less cost of sales and fuel (`cost_m`); ONEOK gives net
  income attributable to ONEOK only in its guidance tables, read as point guides over the latest print's shares (`ni_guide_note`:
  $285M, $316M, $317M, ~$360M), the FY2017 range of 2017-02-02 assumes the pending ONEOK Partners merger (`pro_forma_ni_m`, unused), and
  the Q2 2017 $635-795M divides by that quarter's 214.0M shares (FY17E $3.34; $1.87 on Q3's 383.4M), the merger in as published; dividends
  $0.40 to $0.745; ENERGY_TRANSITION out of scope (no reserves of its own; the TRGP reading, text only), DURABLE; RICH 112, CHEAP 55,
  FAIR 42 of 209 dates (RICH on all of 2014); BASE on net margin moves 77 classes, a five-year window 65, the unrestated 2010-2013 55;
  built in a new session without opening the 2008-2013 outcomes or findings (retro/README.md, "OKE 2014-2017"). From 2018: the earnings
  releases are slide images with a text layer, read by label and number (`trow`, each match checked word for word); the ONEOK Partners
  merger in the figures as published (FY17 on 299.8M shares, the merger and equity issues read as dilution in BASE); EPS from continuing
  operations each year from the latest filing that reports it (the FY2018-FY2020 Item 6 prints totals, so the statements, 2014-2015 kept);
  FY2017 ($1.29 with the Tax Act) and FY2020 ($1.42 with the impairments) kept at GAAP by the AAPL FY2002 test; current-FY EPS the GAAP
  net income guide over the latest print's shares, per share where stated (2020-2021, the Q3 2021 $3.33 midpoint a point); the Q1 2020
  outlook ($500-900M, impairments in) read as the guide as the release withdraws the February one (1 class otherwise); words and "above
  the midpoints" no field; dividends $0.77 to $0.935; ENERGY_TRANSITION out of scope with ONEOK as the holder of no reserves and the climate-
  demand words quoted (text only), EV and CRYPTO out of scope (no 10-K names them), DURABLE; "Medallion Midstream" joins the anachronism
  list; CHEAP 168, FAIR 40, RICH 1 of 209 dates; no EPS guide moves 96 classes, the signals at BEAR 120; built in a new session without
  opening the 2008-2017 outcomes or findings (retro/README.md, "OKE 2018-2021"). From 2022: Item 6 is reserved, so each 10-K vintage
  takes three years from its statement of income (in millions from the FY2023 10-K, the rounded figures replacing the exact ones), the
  earlier years carried; GAAP every year (FY21 $3.35, FY22 $3.84, FY23 $5.48 with the Medford insurance gain, a net 87 cents under half,
  FY24 $5.17, FY25 $5.42); Magellan (2023-09-25, about 135 million shares), EnLink, Medallion and the 2026 transactions as published, the
  merger shares read as dilution in BASE; current-FY EPS is the stated per-share guide, a range or a midpoint stated alone (a point), the
  FY2025 range from the 8-K of 2025-02-26 (the Q4 2024 release gives none), one-offs in; the Q3 2023 consolidated midpoint ($5.36, Magellan
  closed) is used over the pre-acquisition one, and the Q3 2024 stand-alone midpoint ($5.02) over the consolidated one that assumes the then
  pending Medallion acquisition (the pending-deal rule); dividends $0.955 to $1.07, the 2025 and 2026 increases from the Q4 releases (no
  dividend 8-K); GENAI and GLP1 out of scope (the FY2025 10-K's one AI sentence is its computing policy, text only), the climate risk
  heading quoted for ENERGY_TRANSITION (text only), DURABLE; a digit separator where a positive figure reads as a later year (+2,095bp);
  the last date is 2026-11-27; CHEAP 242, FAIR 14 of 256 dates; built in a new session without opening the 2008-2021 outcomes or
  findings (retro/README.md, "OKE 2022-2026").
- **Never use the owner's personal email** in request headers to external
  services (SEC asks for a contact in the User-Agent).
