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
  own 1997-2006 rule-T thresholds, engine and records) SO (2008-01-04 to 2026-11-13 so far, at the owner's request) CTVA (from its 2019 listing: 2021-02-05 to 2026-09-25), KMI (from its 2011 listing: 2013-01-18 to 2026-11-13 so far) LMT (2008-01-04 to 2026-11-13 so far), MU (2008-01-04 to 2021-12-31 so far), GOOG (2008-01-04 to 2026-11-13 so far), JPM (2008-01-04 to 2026-11-13 so far), V (2009-10-29 to 2026-11-13 so far), SPGI (2008-01-04 to 2026-11-20 so far), CB (2008-01-04 to 2026-11-20 so far), LLY (2008-01-04 to 2026-11-20 so far), UNH (2008-01-04 to 2026-11-20 so far), CRM (2008-01-04 to 2026-11-20 so far), SCHW (2008-01-04 to 2017-12-29 so far) and NEE (2008-01-04 to 2009-12-31 so far) sit in `staging/retrospective/` until the owner adds
  them to the archive (retro/README.md, "UNP", "LOW", "AAPL", "NKE", "AVGO", "PEP", "MSFT", "XOM", "SHW", "WMT", "RCL", "MAR", "BKR", "PFE", "CMCSA", "CAT",
  "BMY", "NVDA", "F", "SO", "CTVA", "KMI", "LMT", "MU", "GOOG", "JPM", "V", "SPGI", "CB", "LLY", "UNH", "CRM", "SCHW", "NEE"). The live `nke_signal_model.py`, `avgo_*.py`, `msft_signal_model.py`, `rcl_signal_model.py`, `wmt_signal_model.py`, `mar_signal_model.py` and `bmy_signal_model.py` (other branches) and `cat_signal_model.py`, `mu_signal_model.py`, `v_signal_model.py`, `spgi_signal_model.py` and `lly_signal_model.py` (other branches) files
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
  NEE (FPL Group, Inc., NYSE: FPL; NextEra Energy from 2010) is the series key and Yahoo's symbol; the models print FPL (the SPGI encoding),
  prices as traded (x4 for the 2020 split), the 2005 two-for-one split restating per-share facts published before it (`on_basis`). EPS is
  GAAP diluted before cumulative effects, except 1999 and 2000 at the company's figures excluding only one-offs (FY2002 10-K); every EPS
  guide of 2007-2009 is an adjusted range that also removes the mark-to-market effect of non-qualifying hedges (and OTTI from 2008),
  recurring items, so the guides are display only (the PEP 2008 core rule) and the last full GAAP year stands (FY06 $3.23, FY07 $3.27, FY08
  $4.07); BASE is the latest quarter's revenue as reported; the signals are FPL's energy sales, FPL's net income, revenue, EPS and the
  operating margin under rule T over 1997-2006; DURABLE, no live theme; RICH 53, CHEAP 32, FAIR 20 of 105 dates; the adjusted outlook as
  the anchor moves 21 classes and 39 tiers, the largest call (retro/README.md, "NEE").
- **Never use the owner's personal email** in request headers to external
  services (SEC asks for a contact in the User-Agent).
