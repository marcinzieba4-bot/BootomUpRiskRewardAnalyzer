#!/usr/bin/env python3
"""
Firewall test: plant fake future facts and prices after CUTOFF, rebuild every archived date before it,
and require byte-identical models. Restores the fact sheet and the price cache afterwards, even on failure.

    python3 retro/tools/firewall.py 2015-01-01
    python3 retro/tools/firewall.py 2008-03-31 UNP          # the UNP series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 LOW          # the LOW series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 AAPL         # the AAPL series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 NKE          # the NKE series in staging/retrospective
    python3 retro/tools/firewall.py 2009-10-01 AVGO         # the AVGO series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 PEP          # the PEP series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 MSFT         # the MSFT series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 XOM          # the XOM series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 SHW          # the SHW series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 WMT          # the WMT series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 RCL          # the RCL series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 MAR          # the MAR series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 BKR          # the BKR series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 PFE          # the PFE series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 CMCSA        # the CMCSA series in staging/retrospective
    python3 retro/tools/firewall.py 2008-07-01 CAT          # the CAT series in staging/retrospective

Plants a print, a history vintage, an event per live theme and a company name (UNP: also a guide and a
dividend; LOW and AAPL: also a guide with every guided field; NKE: a guide in words, and futures orders on the last print before
CUTOFF that a filing after it states, the 'futures_later' rule; AVGO: a later guide for every guided quarter; PEP: a display-only guide, and total servings that a filing after CUTOFF
first states on the last print before it, the 'servings_later' rule, and a listing on a new exchange; MSFT: a guide with every guided field, a later
range for every quarter the fact sheet guides, a later withdrawal of every guided year, call-only guidance words and a receivables
caveat; XOM: a guide with a production outlook for every guided year and a dividend, and a later print with outlook words, renamed
volume lines and full-year actuals that exclude its own year and restate every earlier one, and a later vintage that excludes a year; SHW: a guide
with every guided field, a later range for every quarter the fact sheet guides, and a later print that renames every reporting line and restates
every year of the history (the 'restates' field of SHW 2015-2017), and a later withdrawal of every guided field (SHW 2018-2020); WMT: a guide
with every guided field (words and a net sales note included), a later range for every quarter the fact sheet guides, and a later print that
renames every reporting line and restates every year of the history, with operating one-offs, a constant-currency rate and a guide basis
(WMT 2015-2017), and a later withdrawal of every guided field (WMT 2018-2020), with an EPS guide stated as growth, a quarter guide's basis and
the fields of a guide converted from reported growth (WMT 2021-2023); RCL: a guide with every guided field (Net Yields as published and at
constant currency, capacity, the display fields, an EPS guide note), a later range for every quarter the fact sheet guides, and a print
whose Net Yields, Net Cruise Costs, occupancy and raw figures are absurd and which restates every year of the history (the 'restates'
field of RCL 2010-2013), a later withdrawal and a later outlook in words for every guided year, the planted print's full-year actuals
excluding its own year and a later vintage that excludes a year, and APCD and occupancy that a filing after CUTOFF first states on the
last print before it (the 'stats_later' rule of RCL 2018-2021), a later dollar revenue guide for every guided quarter and a later
vintage with an income tax line (RCL 2022-2026); MAR: a guide with every guided field (fiscal-year and next-quarter fee ranges and
percentages, the display, note and words fields), a later range for every quarter the fact sheet guides, and a print whose fees, RevPAR,
occupancy, raw figures and full-year actuals are absurd; BKR: a print whose regional revenues, margins, outlook, rig-count note, raw
figures, pro forma table, basis note and full-year actuals are absurd and whose actuals restate every year, and a later display-only
outlook for every quarter an 8-K guides and the two after the last print, and a later vintage excluding a year (the guide and dividend
every fact sheet with a 'guides' list gets, too), and from the 2017 listing of Baker Hughes, a GE company the same in the new company's
own fields (orders, the segment margin, the work in hand; "era" on the planted print, guides and dividend; BKR 2018-2021); PFE: a
print whose full-year actuals are absurd and which restates every year of the history (the 'restates' field of PFE 2010-2013), a later
withdrawal of every guided field of every guided year and a later reissue of the last print before CUTOFF (PFE 2014-2017), a later
vintage excluding a year (PFE 2018-2021), and a later Q4 print whose full-year actuals exclude its own year (PFE 2022-2026); CMCSA: a
print whose subscribers, margins, capital expenditures, raw figures and full-year actuals are absurd (for the year after the latest
vintage before CUTOFF) and which restates every year of the history (CMCSA 2010-2013), a later guide with every guided field (a range,
the words of a one-sided bound, the label and note); CAT: a print whose Machinery, Engines, sales, margins, profit per share, raw figures
and full-year actuals are absurd (for the year after the latest vintage before CUTOFF), with the 2011 segments' raw figures and basis
(CAT 2010-2013) and Energy & Transportation's, restating every year of the history (CAT 2014-2017), a later vintage of the other kind
with planted segment, normalization and theme-tail notes, a later withdrawal of every guided field (CAT 2018-2022), and a later guide
with every guided
field in both forms (dollar and growth ranges for sales and revenues and for profit per share, their bases, words and notes); every
fact sheet with a 'splits' list, SHW's from 2021-2023: a later split on the price data's next split date; a CLOUD event
from a later 10-K, as for every live theme), all dated after CUTOFF and filled with absurd values, and multiplies every price of the ticker and
the S&P 500 from CUTOFF on by 10. Run it on a clean working tree (commit first). Exit code 0 means no model
before CUTOFF changed.

Controls (does altering one real input change exactly the dates after its release?) are case by case;
see retro/README.md, "Adding dates".
"""
import copy
import datetime as dt
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
cutoff = sys.argv[1]
TICKER = sys.argv[2].upper() if len(sys.argv) > 2 else "ACN"
FACTS = os.path.join(ROOT, "retro", "facts", f"{TICKER}.json")
CACHE = [os.path.join(ROOT, "retro", ".cache", n) for n in (f"{TICKER}.json", "_GSPC.json")]
OUTDIR = {"ACN": "archive/retrospective/ACN", "UNP": "staging/retrospective/UNP", "LOW": "staging/retrospective/LOW",
          "AAPL": "staging/retrospective/AAPL", "NKE": "staging/retrospective/NKE", "AVGO": "staging/retrospective/AVGO",
          "PEP": "staging/retrospective/PEP", "MSFT": "staging/retrospective/MSFT", "XOM": "staging/retrospective/XOM",
          "SHW": "staging/retrospective/SHW", "WMT": "staging/retrospective/WMT", "RCL": "staging/retrospective/RCL",
          "MAR": "staging/retrospective/MAR", "BKR": "staging/retrospective/BKR",
          "PFE": "staging/retrospective/PFE", "CMCSA": "staging/retrospective/CMCSA", "CAT": "staging/retrospective/CAT"}[TICKER]
ARCHIVE = os.path.join(ROOT, OUTDIR)
BUILDER = os.path.join(ROOT, "retro", f"build_{TICKER.lower()}.py")
# absurd values for every field the builder reads from a print
PLANT = {"ACN": dict(quarter="Q9 FY99", revenue_lc=-60, margin_bp=-999, fy_eps_guide=[0.1, 0.2], fy_rev_guide_lc=[-40, -30],
                     fy_fx=-50.0, fy_margin_guide=[1, 2], tax_rate=0.9, groups=[["PLANTED", 1, -99]],
                     cash_return_text="PLANTED", dividend_annual=9.99, dividend_note="PLANTED"),
         "UNP": dict(quarter="Q1 2099", fy=2099, commodity_pct=-60, carloads_pct=-60, arc_pct=-60, gtm_per_employee_pct=-60,
                     op_ratio=199.0, op_ratio_pt=99.0, groups=[["PLANTED", 1, -99]], cash_return_text="PLANTED",
                     outlook_short="PLANTED", diluted_shares_m=1.0, cash_b=99.0),
         "LOW": dict(quarter="Q1 FY99", fy=2099, q=1, sales_b=0.01, sales_pct=-60.0, comps_pct=-60.0, gross_margin=1.0,
                     gross_margin_bp=-999, op_margin=-50.0, op_margin_bp=-999, inventory_pct=99.0, inventory_gap_pp=99.0,
                     eps_q=0.01, eps_q_prior=9.99, stores=1, sq_ft_pct=-60.0, cash_return_text="PLANTED",
                     outlook_short="PLANTED", next_print="PLANTED", diluted_shares_m=1.0, cash_b=99.0),
         "AAPL": dict(quarter="Q1 FY99", fy=2099, q=1, sales_b=0.01, sales_pct=-60.0, gross_margin=1.0, gross_margin_bp=-999,
                      op_margin=-50.0, op_margin_bp=-999, mac_units_k=1, mac_units_pct=-60.0, non_mac_pct=-60.0, ipod_units_k=1,
                      ipod_units_pct=-60.0, iphone_units_k=1, eps_q=0.01, eps_q_prior=9.99, deferred_iphone_b=99.0,
                      non_gaap_note="PLANTED", cash_return_text="PLANTED", outlook_short="PLANTED", next_print="PLANTED",
                      diluted_shares_m=1.0, cash_b=99.0, mac_sales_pct=-60.0, iphone_sales_pct=-60.0),
         "NKE": dict(quarter="Q1 FY99", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, lc_pct=-60.0,
                     lc_note="PLANTED", futures_pct=-60.0, futures_fx_pp=-99.0, futures_b=0.01, futures_note="PLANTED",
                     futures_fx_note="PLANTED", gross_margin=1.0, gross_margin_bp=-999.0, pretax_margin=-50.0,
                     pretax_margin_bp=-999.0, inventory_b=99.0, inventory_pct=99.0, inventory_gap_pp=99.0, eps_q=0.01,
                     eps_q_prior=9.99, eps_note="PLANTED", diluted_shares_m=1.0, cash_b=99.0, next_print="PLANTED",
                     cash_return_text="PLANTED"),
         "AVGO": dict(quarter="Q1 FY99", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, seq_pct=-60.0,
                      sales_note="PLANTED", gross_margin=1.0, gross_margin_bp=-999.0, op_margin=-50.0, op_margin_bp=-999.0,
                      opex_pct=99.0, opex_gap_pp=99.0, inventory_b=99.0, inventory_pct=99.0, inventory_gap_pp=99.0,
                      inventory_note="PLANTED", eps_q=0.01, eps_q_prior=9.99, eps_note="PLANTED", shares_note="PLANTED",
                      diluted_shares_m=1.0, cash_b=99.0, ltd_b=99.0, next_print="PLANTED", cash_return_text="PLANTED",
                      raw=dict(sales_m=1, sales_prior_m=99, sales_prev_q_m=99, cogs_m=1, cogs_prior_m=1, rd_m=99, rd_prior_m=1,
                               sga_m=99, sga_prior_m=1, op_income_m=-99, op_income_prior_m=99, inventory_m=99, inventory_prior_m=1)),
         "PEP": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, lc_pct=-60.0, lc_note="PLANTED",
                     servings_pct=-60.0, servings_note="PLANTED", gross_margin=1.0, gross_margin_bp=-999.0, op_margin=-50.0,
                     op_margin_bp=-999.0, inventory_b=99.0, inventory_pct=99.0, inventory_gap_pp=99.0, eps_q=0.01, eps_q_prior=9.99,
                     eps_note="PLANTED", diluted_shares_m=1.0, cash_b=99.0, next_print="PLANTED", cash_return_text="PLANTED",
                     raw=dict(sales_m=1, sales_prior_m=99, cogs_m=1, cogs_prior_m=1, op_m=-99, op_prior_m=99, inventory_m=99,
                              inventory_prior_m=1)),
         "MSFT": dict(quarter="Q1 FY99", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, unearned_b=0.01, unearned_pct=-60.0,
                      receivables_b=99.0, receivables_pct=99.0, receivables_gap_pp=99.0, gross_margin=1.0, gross_margin_bp=-999.0,
                      op_margin=-50.0, op_margin_bp=-999.0, eps_q=0.01, eps_q_prior=9.99, eps_note="PLANTED", diluted_shares_m=1.0,
                      cash_b=99.0, next_print="PLANTED", cash_return_text="PLANTED", fx_note="PLANTED", sales_note="PLANTED",
                      unearned_note="PLANTED", receivables_note="PLANTED", lc_pct=-60.0, lc_note="PLANTED", guide_on_call="PLANTED",
                      receivables_caveat="PLANTED",
                      raw=dict(sales_m=1, sales_prior_m=99, cogs_m=1, cogs_prior_m=1, op_m=-99, op_prior_m=99, ar_m=99, ar_prior_m=1,
                               unearned_m=1, unearned_prior_m=99)),
         "XOM": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, pretax_margin=-50.0,
                     pretax_margin_bp=-999.0, production_pct=-60.0, product_sales_pct=-60.0, chem_pct=-60.0, eps_q=0.01, eps_q_prior=9.99,
                     eps_note="PLANTED", diluted_shares_m=1.0, cash_b=99.0, next_print="PLANTED", cash_return_text="PLANTED",
                     production_note="PLANTED", sales_note="PLANTED", capex_note="PLANTED", outlook_words="PLANTED",
                     pps_label="PLANTED", chem_label="PLANTED",
                     raw=dict(rev_m=1, rev_prior_m=99, pretax_m=-99, pretax_prior_m=99, oe_kbd=1, oe_prior_kbd=99, pps_kbd=1,
                              pps_prior_kbd=99, chem_kt=1, chem_prior_kt=99)),
         "SHW": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, lc_pct=-60.0, comps_pct=-60.0,
                     consumer_pct=-60.0, gross_margin=1.0, gross_margin_bp=-999.0, pretax_margin=-50.0, pretax_margin_bp=-999.0,
                     eps_q=0.01, eps_q_prior=9.99, eps_note="PLANTED", diluted_shares_m=1.0, next_print="PLANTED",
                     cash_return_text="PLANTED", comps_note="PLANTED", consumer_note="PLANTED", currency_pp=-50.0,
                     currency_note="PLANTED", acq_note="PLANTED",
                     renames={"Paint Stores Group": "PLANTED", "Consumer Group": "PLANTED", "Global Group": "PLANTED"},
                     raw=dict(ns_k=1, ns_prior_k=99, cogs_k=1, cogs_prior_k=1, pretax_k=-99, pretax_prior_k=99, diluted_shares=1)),
         "WMT": dict(quarter="Q1 FY99", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, comps_pct=-60.0,
                     comps_note="PLANTED", gross_margin=1.0, gross_margin_bp=-999.0, op_margin=-50.0, op_margin_bp=-999.0,
                     inventory_pct=99.0, inventory_gap_pp=99.0, eps_q=0.01, eps_q_prior=9.99, eps_note="PLANTED",
                     diluted_shares_m=1.0, cash_b=99.0, next_print="PLANTED", cash_return_text="PLANTED", period_end="PLANTED",
                     segments=[["PLANTED", 0.01, -99.0]], op_margin_note="PLANTED", lc_pct=-60.0, currency_m=-99999,
                     currency_note="PLANTED",
                     renames={"Wal-Mart Stores": "PLANTED", "Walmart U.S.": "PLANTED", "Sam's Club": "PLANTED", "International": "PLANTED"},
                     raw=dict(ns_m=1, ns_prior_m=99, other_m=1, other_prior_m=1, cogs_m=1, cogs_prior_m=1, sga_m=1, sga_prior_m=1,
                              op_m=0, op_prior_m=98, inv_m=99, inv_prior_m=1, diluted_shares_m=1.0, op_oneoff_m=99, op_oneoff_prior_m=-99)),
         "RCL": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, ny=1.0, ny_prior=99.0, ny_pct=-60.0,
                     ny_cc_pct=-60.0, ny_stated_pct=-60.0, ny_note="PLANTED", ncc=999.0, ncc_prior=1.0, ncc_pct=99.0, ncc_stated_pct=99.0,
                     ncc_note="PLANTED", capacity_pct=-60.0, occupancy=1.0, occupancy_bp=-999.0, op_margin=-50.0, op_margin_bp=-999.0,
                     eps_q=0.01, eps_q_prior=9.99, eps_note="PLANTED", diluted_shares_m=1.0, cash_b=99.0, next_print="PLANTED",
                     cash_return_text="PLANTED", fuel_note="PLANTED", period_end="PLANTED",
                     raw=dict(rev_k=1, rev_prior_k=99, comm_k=0, comm_prior_k=0, onboard_k=0, onboard_prior_k=0, opex_k=99, opex_prior_k=1,
                              msa_k=1, msa_prior_k=1, opinc_k=-99, opinc_prior_k=99, apcd=1, apcd_prior=99, occ=1.0, occ_prior=99.0,
                              diluted_shares_k=1, cash_k=99)),
         "MAR": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, fees_m=1, fees_prior_m=999,
                     fees_pct=-60.0, revpar_pct=-60.0, occupancy=1.0, occupancy_pts=-99.0, occupancy_bp=-9900.0, op_margin=-50.0,
                     op_margin_bp=-999.0, eps_q=0.01, eps_q_prior=9.99, eps_note="PLANTED", diluted_shares_m=1.0, cash_b=99.0,
                     next_print="PLANTED", cash_return_text="PLANTED", ww_revpar_note="PLANTED", basis_note="PLANTED", period_end="PLANTED",
                     raw=dict(base_m=1, base_prior_m=999, fran_m=0, fran_prior_m=0, inc_m=0, inc_prior_m=0, rev_total_m=1, rev_total_prior_m=99,
                              opinc_m=-99, opinc_prior_m=99, diluted_shares_m=1.0, cash_m=99)),
         "BKR": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, na_pct=-60.0, intl_pct=-60.0,
                     gross_margin=1.0, gross_margin_bp=-999.0, op_margin=-50.0, op_margin_bp=-999.0, eps_q=0.01, eps_q_prior=9.99,
                     eps_note="PLANTED", diluted_shares_m=1.0, cash_b=99.0, cash_note="PLANTED", capex_note="PLANTED", next_print="PLANTED",
                     cash_return_text="PLANTED", sales_note="PLANTED", na_note="PLANTED", intl_note="PLANTED", margin_note="PLANTED",
                     rig_note="PLANTED", outlook=["PLANTED"], period_end="PLANTED", basis_note="PLANTED",
                     pro_forma=dict(rev_m=1, rev_prior_m=99, na_m=1, na_prior_m=99, ind_m=0, ind_prior_m=0),
                     raw=dict(rev_m=1, rev_prior_m=99, cos_m=1, cos_prior_m=1, cosr_m=1, cosr_prior_m=1, rne_m=1, rne_prior_m=1,
                              oi_m=-99, oi_prior_m=99, na_m=1, na_prior_m=99, oilfield_m=1, oilfield_prior_m=99, ind_m=0, ind_prior_m=0,
                              ind_label="PLANTED")),
         "PFE": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, us_pct=-60.0, intl_pct=-60.0,
                     gross_margin=1.0, gross_margin_bp=-999.0, pretax_margin=-50.0, pretax_margin_bp=-999.0, eps_q=0.01, eps_q_prior=9.99,
                     diluted_shares_m=1.0, next_print="PLANTED", cash_return_text="PLANTED", note="PLANTED", period_end="PLANTED",
                     release_time="PLANTED",
                     raw=dict(rev_m=2, rev_prior_m=198, cos_m=1, cos_prior_m=1, pretax_m=-99, pretax_prior_m=99, us_m=1, us_prior_m=99,
                              intl_m=1, intl_prior_m=99, diluted_shares_m=1)),
         "CMCSA": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, video_pct=-60.0, ocf_margin=1.0,
                       ocf_margin_bp=-999.0, op_margin=-50.0, op_margin_bp=-999.0, capex_pct=99.0, capex_bp=9999.0, eps_q=0.01,
                       eps_q_prior=9.99, diluted_shares_m=1.0, next_print="PLANTED", cash_return_text="PLANTED", note="PLANTED",
                       period_end="PLANTED", release_time="PLANTED",
                       raw=dict(rev_m=2, rev_prior_m=198, ocf_m=1, ocf_prior_m=99, oi_m=-99, oi_prior_m=99, capex_m=99, capex_prior_m=1,
                                video_k=1, video_prior_k=99, video_columns="PLANTED", diluted_shares_m=1)),
         "CAT": dict(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, mach_pct=-60.0, eng_pct=-60.0,
                     op_margin=-50.0, op_margin_bp=-999.0, eps_q=0.01, eps_q_prior=9.99, eps_pct=-99.9, diluted_shares_m=1.0,
                     next_print="PLANTED", cash_return_text="PLANTED", note="PLANTED", period_end="PLANTED", release_time="PLANTED",
                     lines_basis="PLANTED",
                     raw=dict(mach_m=1, mach_prior_m=99, eng_m=1, eng_prior_m=99, rev_m=2, rev_prior_m=198, oi_m=-99, oi_prior_m=99,
                              diluted_shares_m=1, ci_m=1, ci_prior_m=99, ri_m=1, ri_prior_m=99, ps_m=1, ps_prior_m=99, et_m=1,
                              et_prior_m=99))}[TICKER]
# LOW and AAPL guides carry more fields than UNP's: plant every one the builder reads (NKE's are words only)
GUIDE_PLANT = {"LOW": dict(comps_guide=[-50, -40], op_margin_guide_bp=[-999, -999], margin_def="PLANTED", stores_guide=1,
                           store_opening_m=9999, fy_words="PLANTED",
                           q_guide={"quarter": "Q4 FY99", "sales": [-40, -30], "comps": [-50, -40], "eps": [0.1, 0.2]}),
               "AAPL": dict(gm_guide_pct=[1, 2], q_guide_note="PLANTED",
                            q_guide={"quarter": "Q4 FY99", "sales_usd_b": [0.1, 0.2], "eps": [0.1, 0.2], "prior_sales_b": 99.0,
                                     "prior_source": "A14", "prior_label": "PLANTED", "gm_pct": [1, 2], "opex_usd_b": [99.0, 99.0],
                                     "oie_usd_b": [99.0, 99.0], "tax_pct": [99.0, 99.0]}),
               "NKE": dict(words=["PLANTED"]),
               "AVGO": dict(quarter="Q9 FY99", seq_pct=[-50, -40], base_quarter="PLANTED", base_sales_m=1, level_m=[0.5, 0.6],
                            prior_label="PLANTED", prior_sales_m=1, prior_source="V1", yoy_pct=[-50, -40], quote="PLANTED",
                            display="PLANTED"),
               "PEP": dict(display="PLANTED", unused="PLANTED"),
               "XOM": dict(production_quote="PLANTED", note="PLANTED"),
               "WMT": dict(eps_guide_note="PLANTED", fy_words="PLANTED", rev_guide_note="PLANTED", rev_basis="PLANTED", rev_words="PLANTED",
                           rev_reported=[-50, -40], rev_currency_m=-99999, rev_prior_m=1,
                           q_guide={"quarter": "Q4 FY99", "sales": [-40, -30], "comps": [-50, -40], "eps": [0.1, 0.2],
                                    "sales_basis": "PLANTED", "sales_reported": [-50, -40], "currency_m": -99999, "prior_m": 1}),
               "MAR": dict(note="PLANTED", words="PLANTED", fy_display="PLANTED", eps_guide_note="PLANTED",
                           fy_fees={"level_m": [1, 2], "pct": [-60, -50], "prior_m": 1, "prior_label": "PLANTED", "prior_source": "MA1"},
                           q_guide={"quarter": "Q4 2099", "fees_m": [1, 2], "fees_pct": [-60, -50], "prior_m": 1, "prior_label": "PLANTED",
                                    "prior_source": "MA1", "eps": [0.1, 0.2], "revpar": "PLANTED"}),
               "RCL": dict(note="PLANTED", fy_display="PLANTED", eps_guide_note="PLANTED", fy_rev={"ny": [-50, -40], "ny_cc": [-50, -40], "capacity": -50.0},
                           q_guide={"quarter": "Q4 2099", "ny": [-50, -40], "ny_cc": [-50, -40], "capacity": -50.0, "eps": [0.1, 0.2]}),
               "PFE": dict(rev_guide_usd_b=[0.1, 0.2], eps_adj=[0.1, 0.2], rev_label="PLANTED", note="PLANTED"),
               "CMCSA": dict(rev_guide_pct=[-50, -40], rev_words="PLANTED", rev_label="PLANTED", note="PLANTED"),
               "CAT": dict(rev_guide_usd_b=[0.1, 0.2], rev_guide_pct=[-50, -40], rev_growth_base_b=0.01, rev_growth_base_note="PLANTED",
                           eps_growth=[-99, -98], eps_growth_base=0.01, eps_growth_base_note="PLANTED", eps_guide_note="PLANTED",
                           rev_words="PLANTED", note="PLANTED"),
               "SHW": dict(fy_words="PLANTED", note="PLANTED",
                           q_guide={"quarter": "Q4 2099", "sales": [-40, -30], "eps": [0.1, 0.2], "words": "PLANTED"}),
               "MSFT": dict(rev_guide_usd_b=[0.1, 0.2], op_income_guide_usd_b=[0.1, 0.2], note="PLANTED", opex_guide_usd_b=[0.1, 0.2],
                            q_guide={"quarter": "Q4 FY99", "sales_usd_b": [0.1, 0.2], "op_income_usd_b": [0.1, 0.2], "eps": [0.1, 0.2],
                                     "eps_words": "PLANTED", "prior_sales_b": 99.0, "prior_source": "MS1", "prior_label": "PLANTED"})}.get(TICKER, {})

git = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True, check=True).stdout
if git("status", "--porcelain", "retro/facts", OUTDIR).strip():
    sys.exit("commit first: the fact sheet or the archive has uncommitted changes")

later = (dt.date.fromisoformat(cutoff) + dt.timedelta(days=10)).isoformat()
dates = sorted(os.path.basename(d) for d in glob.glob(os.path.join(ARCHIVE, "20*")) if os.path.basename(d) < cutoff)
backup = tempfile.mkdtemp()
changed = planted = ["not run"]
saved = {p: os.path.join(backup, f"{i}.json") for i, p in enumerate([FACTS] + CACHE)}   # two files are named ACN.json
for p, b in saved.items():
    shutil.copy(p, b)
try:
    with open(FACTS, encoding="utf-8") as fh:
        f = json.load(fh)
    last = copy.deepcopy(max(f["prints"], key=lambda p: p["published"] if p["published"] < cutoff else ""))
    last.pop("fy_actual", None)
    last.pop("servings_later", None)
    own = set(last)
    last.update(published=later, **PLANT)
    if TICKER == "BKR" and last.get("era"):   # the company listed in 2017: the planted print keeps only that company's fields, absurd
        for k in set(last) - own:
            del last[k]
        last.update(quarter="Q1 2099", fy=2099, q=1, release="PLANTED", sales_b=0.01, sales_pct=-60.0, orders_pct=-60.0, gross_margin=1.0,
                    gross_margin_bp=-999.0, seg_margin=1.0, seg_margin_bp=-999.0, op_margin=-50.0, op_margin_bp=-999.0, eps_q=0.01,
                    eps_q_prior=9.99, eps_note="PLANTED", diluted_shares_m=1.0, cash_b=99.0, cash_note="PLANTED", capex_note="PLANTED",
                    rpo_note="PLANTED", next_print="PLANTED", cash_return_text="PLANTED", sales_note="PLANTED", orders_note="PLANTED",
                    seg_note="PLANTED", margin_note="PLANTED", segments_note="PLANTED", period_end="PLANTED", basis_note="PLANTED",
                    raw=dict(orders_m=1, orders_prior_m=99, rev_m=4, rev_prior_m=400, cor_m=4, cor_prior_m=1, segoi_m=-99, segoi_prior_m=99,
                             oi_m=-99, oi_prior_m=99, ofs_m=1, ofs_prior_m=100, ofe_m=1, ofe_prior_m=100, tps_m=1, tps_prior_m=100,
                             ds_m=1, ds_prior_m=100))
        if "segments" in last:
            last["segments"] = [["PLANTED", 4, 400]]
    f["prints"].append(last)
    if "guides" in f:      # a guide for every fiscal year in the fact sheet, and a dividend
        for y in {g["fy"] for g in f["guides"]} | {2099}:
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "eps_guide": [0.1, 0.2],
                                "rev_guide": [-40, -30], "rev_guide_label": "PLANTED", "volume_guide": [-50, -40], **GUIDE_PLANT})
        f["dividends"].append({"published": later, "source": last["source"], "quarterly": 9.99, "note": "PLANTED"})
    if TICKER == "AAPL":   # a later withdrawal of every field of every guided quarter (the update of 2020-02-17 rule)
        for g in [g for g in f["guides"] if g["published"] < cutoff and "sales_usd_b" in g.get("q_guide", {})]:
            f["guides"].append({"fy": g["fy"], "published": later, "source": last["source"], "doc": "PLANTED", "quote": "PLANTED",
                                "q_guide": {"quarter": g["q_guide"]["quarter"],
                                            "withdrawn": ["sales_usd_b", "eps", "gm_pct", "opex_usd_b", "oie_usd_b", "tax_pct"]}})
    if TICKER == "NKE":    # futures orders that a filing after CUTOFF first states, on the last print before it
        p0 = max((p for p in f["prints"] if p["published"] < cutoff), key=lambda p: p["published"])
        if p0.get("futures_later", {}).get("published", cutoff) >= cutoff:     # a real one public before CUTOFF stays
            p0["futures_later"] = {"published": later, "source": p0["source"], "futures_pct": -60.0, "futures_fx_pp": -99.0,
                                   "futures_b": 0.01, "futures_note": "PLANTED", "futures_fx_note": "PLANTED"}
    if TICKER == "PEP":    # total servings that a filing after CUTOFF first states, on the last print before it (servings_later)
        p0 = max((p for p in f["prints"] if p["published"] < cutoff), key=lambda p: p["published"])
        if p0["servings_pct"] is None and p0.get("servings_later", {}).get("published", cutoff) >= cutoff:
            p0["servings_later"] = {"published": later, "source": p0["source"], "pct": -60.0, "note": "PLANTED"}
    if TICKER == "AVGO":   # a later guide for every quarter or fiscal year guided before CUTOFF, with absurd values (the latest guide
                           # for a quarter or year wins), absurd margin levels, and a later withdrawal of every fiscal year guided before it
        for g in [g for g in f["guides"] if g["published"] < cutoff]:
            f["guides"].append({**copy.deepcopy(g), "published": later, "doc": "PLANTED", "seq_pct": [-50, -40], "level_m": [0.5, 0.6],
                                "yoy_pct": [-99, -98], "quote": "PLANTED", "display": "PLANTED",
                                **({"op_margin_guide_pct": [1.0, 2.0], "margin_quote": "PLANTED"} if "op_margin_guide_pct" in g else {})})
        for y in sorted({(g["fy"], g["period"]) for g in f["guides"] if g.get("period") and g["published"] < cutoff}):
            f["guides"].append({"fy": y[0], "published": later, "source": last["source"], "doc": "PLANTED", "period": y[1],
                                "withdrawn": True, "quote": "PLANTED", "display": "PLANTED"})
    if "capital_return" in f:      # AAPL: a capital return statement (catalyst 5)
        f["capital_return"].append({"published": later, "source": last["source"], "doc": "PLANTED", "text": "PLANTED"})
    if "splits" in f:      # a split announced after CUTOFF, on a split date of the price data after CUTOFF
        with open(CACHE[0]) as fh:
            r = json.load(fh)["chart"]["result"][0]
        off = r["meta"]["gmtoffset"]
        days = sorted(dt.datetime.fromtimestamp(v["date"] + off, dt.timezone.utc).date().isoformat()
                      for v in r.get("events", {}).get("splits", {}).values())
        f["splits"] += [{"published": later, "source": last["source"], "effective": d, "ratio": 10, "note": "PLANTED"}
                        for d in days if d > later][:1]
    if TICKER == "MSFT":   # a later range for every quarter guided in the fact sheet, with absurd values (the latest guide for a quarter
                           # wins): a later guide may never reach an earlier date
        for q in sorted({g["q_guide"]["quarter"] for g in f["guides"] if "q_guide" in g}):
            f["guides"].append({"fy": 2000 + int(q.split("FY")[1]), "published": later, "source": last["source"], "doc": "PLANTED",
                                "eps_guide": [0.1, 0.2], "q_guide": {**GUIDE_PLANT["q_guide"], "quarter": q}})
        for y in sorted({g["fy"] for g in f["guides"] if g["published"] < cutoff}):   # and a later withdrawal of every guided year
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "withdrawn": True,
                                "quote": "PLANTED", "opex_guide_usd_b": [0.1, 0.2]})
    if TICKER == "SHW":    # a later range for every quarter guided in the fact sheet, with absurd values (the latest guide for a quarter
                           # wins): a later guide may never reach an earlier date
        for q in sorted({g["q_guide"]["quarter"] for g in f["guides"] if "q_guide" in g}):
            f["guides"].append({"fy": int(q.split()[1]), "published": later, "source": last["source"], "doc": "PLANTED",
                                "eps_guide": [0.1, 0.2], "rev_guide": [-40, -30], "fy_words": "PLANTED",
                                "q_guide": {**GUIDE_PLANT["q_guide"], "quarter": q}})
        v0 = max((x for x in f["history_vintages"] if x["published"] < cutoff), key=lambda x: x["published"])
        last.update(restates={y: 0.01 for y in v0["eps_normalized"]}, restates_note="PLANTED")
        for y in sorted({g["fy"] for g in f["guides"] if g["published"] < cutoff}):   # and a later withdrawal of every guided field
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "fy_words": "PLANTED",
                                "withdrawn": ["rev_guide", "eps_guide"]})
    if TICKER == "RCL":    # a later range for every quarter guided in the fact sheet, with absurd values (the latest guide for a quarter
                           # wins): a later guide may never reach an earlier date
        # (and a later dollar revenue guide for each, read against a planted year-ago quarter: the 'q_rev' field of RCL 2022-2026)
        for q in sorted({g[k]["quarter"] for g in f["guides"] for k in ("q_guide", "q_rev") if k in g}):
            f["guides"].append({"fy": int(q.split()[1]), "published": later, "source": last["source"], "doc": "PLANTED",
                                "eps_guide": [0.1, 0.2], **{k: v for k, v in GUIDE_PLANT.items() if k != "q_guide"},
                                "q_guide": {**GUIDE_PLANT["q_guide"], "quarter": q},
                                "q_rev": {"quarter": q, "level_b": [0.01, 0.02], "prior_k": 1, "prior_source": last["source"],
                                          "prior_label": "PLANTED", "quote": "PLANTED"}})
        v0 = max((x for x in f["history_vintages"] if x["published"] < cutoff), key=lambda x: x["published"])
        last.update(restates={y: 0.01 for y in v0["eps_normalized"]}, restates_note="PLANTED")
        for y in sorted({g["fy"] for g in f["guides"] if g["published"] < cutoff}):   # a later withdrawal and outlook in words (RCL 2018-2021)
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "withdrawn_quote": "PLANTED",
                                "withdrawn": ["eps_guide", "fy_rev", "fy_display", "q_guide", "note"]})
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "words": "PLANTED"})
        p0 = max((p for p in f["prints"] if p["published"] < cutoff), key=lambda p: p["published"])
        if p0.get("stats_later", {}).get("published", cutoff) >= cutoff:     # a real one public before CUTOFF stays
            p0["stats_later"] = {"published": later, "source": p0["source"], "apcd": 1, "apcd_prior": 99, "occ": 1.0, "occ_prior": 99.0,
                                 "capacity_pct": -99.0, "occupancy": 1.0, "occupancy_bp": -9800.0}
        fa = copy.deepcopy(max((p for p in f["prints"] if "fy_actual" in p and p["published"] < cutoff), key=lambda p: p["published"])["fy_actual"])
        fa.update(fy=2099, fy_label="FY99", eps_normalized=None, excluded_note="PLANTED", normalization_note="PLANTED", revenue_usd_b=0.01)
        last.update(fy_actual=fa, no_ny_ncc=True, no_ny_ncc_note="PLANTED", ratio_note="PLANTED", ytd_sales_pct=-99.0, ytd_label="PLANTED")
    if TICKER == "MAR":    # a later range for every quarter guided in the fact sheet, with absurd values (the latest guide for a quarter
                           # wins): a later guide may never reach an earlier date; and absurd full-year actuals on the planted print
        for q in sorted({g["q_guide"]["quarter"] for g in f["guides"] if "q_guide" in g}):
            f["guides"].append({"fy": int(q.split()[1]), "published": later, "source": last["source"], "doc": "PLANTED",
                                "eps_guide": [0.1, 0.2], **{k: v for k, v in GUIDE_PLANT.items() if k != "q_guide"},
                                "q_guide": {**GUIDE_PLANT["q_guide"], "quarter": q}})
        withfy = [p for p in f["prints"] if "fy_actual" in p]           # before the first Q4 print, the earliest one's fields, planted later
        fa = copy.deepcopy(max([p for p in withfy if p["published"] < cutoff] or withfy[:1], key=lambda p: p["published"])["fy_actual"])
        fa.update(fy=2099, fy_label="FY99", eps_normalized=0.01, normalization_note="PLANTED", revenue_usd_b=0.01, revpar_pct=-99.0,
                  op_margin=-99.0, fees_pct=-99.0, tax_note="PLANTED", op_margin_note="PLANTED", doc="PLANTED")
        last["fy_actual"] = fa
    if TICKER == "BKR":    # absurd full-year actuals on the planted print (before the first Q4 print, the earliest one's fields)
        withfy = [p for p in f["prints"] if "fy_actual" in p]
        fa = copy.deepcopy(max([p for p in withfy if p["published"] < cutoff] or withfy[:1], key=lambda p: p["published"])["fy_actual"])
        fa.update(fy=2099, fy_label="FY99", eps_normalized=0.01, normalization_note="PLANTED", revenue_usd_b=0.01, diluted_shares_m=1.0,
                  op_margin=-99.0, op_margin_note="PLANTED", sales_growth=-99.0, na_pct=-99.0, na_note="PLANTED", check_pretax_margin=-99.0,
                  check_pretax_note="PLANTED", tax_rate=0.99, tax_note="PLANTED", groups=[["PLANTED", 1, -99]], groups_basis="PLANTED")
        v0 = max((x for x in f["history_vintages"] if x["published"] < cutoff), key=lambda x: x["published"])
        fa["restates"] = {y: 0.01 for y in v0["eps_normalized"]}          # and a restatement of every year (BKR 2010-2013)
        if last.get("era"):    # the company listed in 2017: its own full-year fields (BKR 2018-2021)
            for k in ("na_pct", "na_note", "restates", "one_off_test"):
                fa.pop(k, None)
            fa.update(orders_pct=-99.0, orders_note="PLANTED", sales_note="PLANTED", eps_basis="company adjusted", restates_note="PLANTED",
                      restates={y: 0.01 for y in list(v0["eps_normalized"]) + list(v0.get("eps_excluded", {}))})   # every year, the excluded too (BKR 2022-2026)
        last["fy_actual"] = fa
        # a later display-only outlook for every quarter an 8-K guides, and for the quarters after the last print before CUTOFF
        p0 = max((p for p in f["prints"] if p["published"] < cutoff), key=lambda p: p["published"])
        nxt = [f"Q{(p0['q'] + k - 1) % 4 + 1} {p0['fy'] + (p0['q'] + k - 1) // 4}" for k in (1, 2)]
        for q in sorted({g["quarter"] for g in f["guides"] if "quarter" in g} | set(nxt)):
            f["guides"].append({"fy": int(q.split()[1]), "published": later, "source": last["source"], "doc": "PLANTED", "quarter": q,
                                "display": "PLANTED"})
        if last.get("era"):    # a later fiscal-year revenue guide in dollars for the year of the last print and the next (BKR 2022-2026)
            for y in (p0["fy"], p0["fy"] + 1):
                f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "rev_guide_m": [1, 2],
                                    "rev_guide_note": "PLANTED"})
        if last.get("era"):    # the planted guides and dividend belong to the company listed in 2017
            for x in f["guides"] + f["dividends"]:
                if x["published"] == later:
                    x["era"] = last["era"]
    if TICKER == "WMT":    # a later range for every quarter guided in the fact sheet, with absurd values (the latest guide for a quarter
                           # wins): a later guide may never reach an earlier date
        for q in sorted({g["q_guide"]["quarter"] for g in f["guides"] if "q_guide" in g}):
            f["guides"].append({"fy": 2000 + int(q.split("FY")[1]), "published": later, "source": last["source"], "doc": "PLANTED",
                                "eps_guide": [0.1, 0.2], "rev_guide": [-40, -30], "eps_guide_note": "PLANTED",
                                "fy_words": "PLANTED", "rev_guide_note": "PLANTED", "rev_basis": "PLANTED",
                                "q_guide": {**GUIDE_PLANT["q_guide"], "quarter": q}})
        v0 = max((x for x in f["history_vintages"] if x["published"] < cutoff), key=lambda x: x["published"])
        last.update(restates={y: 0.01 for y in v0["eps_normalized"]}, restates_note="PLANTED")
        for y in sorted({g["fy"] for g in f["guides"] if g["published"] < cutoff}):   # and a later withdrawal of every guided field
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "withdrawn_quote": "PLANTED",
                                "withdrawn": ["rev_guide", "eps_guide", "rev_words"], "fy_words": "PLANTED"})
            # and a still later EPS guide stated as growth on the last full year (WMT 2021-2023)
            f["guides"].append({"fy": y, "published": (dt.date.fromisoformat(later) + dt.timedelta(days=1)).isoformat(),
                                "source": last["source"], "doc": "PLANTED", "eps_growth": [-99, -98], "eps_growth_note": "PLANTED"})
    if "listings" in f:    # PEP: an exchange change announced and effective after CUTOFF
        f["listings"].append({"published": later, "effective": later, "exchange": "PLANTED", "source": last["source"], "note": "PLANTED"})
    v = copy.deepcopy(max((x for x in f["history_vintages"] if x["published"] < cutoff), key=lambda x: x["published"]))
    v.update(published=later, why="PLANTED", company="PLANTED")
    v["eps_normalized"] = {**v["eps_normalized"], "2099": 0.01}
    f["history_vintages"].append(v)
    if TICKER == "RCL":    # a later vintage excluding a year (RCL 2018-2021), with a tax line and Net Cruise Costs without Net Yields (RCL 2022-2026)
        v["eps_excluded"] = {**v.get("eps_excluded", {}), "2098": "PLANTED"}
        v.update(tax_rate=0.99, tax_note="PLANTED", other_expense_note="PLANTED", units_note="PLANTED", prev_fy_ny_pct=None,
                 prev_fy_ncc_pct=-99.0)
    if TICKER == "PFE":    # absurd full-year actuals on the planted print, for the year after the latest vintage
        last["fy_actual"] = {"fy": int(max(v["eps_normalized"])), "fy_label": "FY99", "eps_normalized": 0.01, "revenue_usd_b": 0.01,
                             "diluted_shares_m": 1.0, "normalization_note": "PLANTED", "gross_margin": 1.0, "pretax_margin": -50.0,
                             "pretax_margin_note": "PLANTED", "sales_growth": -60.0, "us_pct": -60.0, "intl_pct": -60.0, "tax_rate": 0.99,
                             "tax_note": "PLANTED"}
        # a later print restating every year of the history (the 'restates' field of PFE 2010-2013)
        last["restates"] = {y: {"eps": 0.01, "revenue_usd_b": 0.01} for y in v["eps_normalized"] if y != "2099"}
        last["restates_note"] = "PLANTED"
        last.pop("reissued", None)
        v["eps_excluded"] = {**v.get("eps_excluded", {}), "2098": "PLANTED"}     # a later vintage excluding a year (PFE 2018-2021)
        # a later Q4 print whose full-year actuals exclude its own year (the 'excluded_note' of PFE 2022-2026)
        q4 = copy.deepcopy(last)
        q4.update(quarter="Q4 2098", fy=2098, q=4, published=later)
        q4["fy_actual"] = {**last["fy_actual"], "fy": 2098, "fy_label": "FY98", "eps_normalized": None, "excluded_note": "PLANTED"}
        q4.pop("restates", None)
        f["prints"].append(q4)
        # a later withdrawal of every guided field of every guided year, with the GAAP-EPS policy words (PFE 2014-2017)
        for y in sorted({g["fy"] for g in f["guides"] if g["published"] < cutoff}):
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "withdrawn_quote": "PLANTED",
                                "eps_none": "PLANTED", "withdrawn": ["eps_guide", "rev_guide_usd_b", "eps_adj"]})
        # a later reissue of the last print before CUTOFF with absurd figures and full-year actuals (the 'reissued' field of PFE 2014-2017)
        p0 = max((p for p in f["prints"] if p["published"] < cutoff), key=lambda p: p["published"])
        if p0.get("reissued", {}).get("published", cutoff) >= cutoff:     # a real reissue public before CUTOFF stays
            p0["reissued"] = {"published": later, "source": last["source"], "release_time": "PLANTED", "note": "PLANTED",
                              "raw": {"pretax_m": -99999, "diluted_shares_m": 1}, "pretax_margin": -999.0, "pretax_margin_bp": -99999.0,
                              "eps_q": -9.99, "diluted_shares_m": 1.0,
                              "fy_actual": {"eps_normalized": 0.01, "normalization_note": "PLANTED", "pretax_margin": -50.0,
                                            "pretax_margin_note": "PLANTED", "tax_rate": 0.99, "tax_note": "PLANTED"}}
    if TICKER == "CMCSA":  # absurd full-year actuals on the planted print, for the year after the latest vintage before CUTOFF
        v0 = max((x for x in f["history_vintages"] if x["published"] < cutoff), key=lambda x: x["published"])
        y0 = max(int(y) for y in v0["eps_normalized"]) + 1
        last["fy_actual"] = {"fy": y0, "fy_label": "FY99", "eps_normalized": 0.01, "revenue_usd_b": 0.01, "diluted_shares_m": 1.0,
                             "normalization_note": "PLANTED", "op_margin": -50.0, "ocf_margin": 1.0, "pretax_margin": -50.0,
                             "pretax_margin_note": "PLANTED", "sales_growth": -60.0, "capex_pct": 99.0, "video_pct": -60.0,
                             "video_note": "PLANTED", "tax_rate": 0.99, "tax_note": "PLANTED"}
        # a later print restating every year of the history (the 'restates' field of CMCSA 2010-2013)
        last["restates"] = {y: {"eps": 0.01} for y in v0["eps_normalized"]}
        last["restates_note"] = "PLANTED"
    if TICKER == "CAT":    # absurd full-year actuals on the planted print, for the year after the latest vintage before CUTOFF
        # the later vintage of the other kind, with planted segment and normalization notes (CAT 2010-2013)
        v.update(kind="DURABLE" if v.get("kind") == "CYCLICAL" else "CYCLICAL", groups_basis="PLANTED", lines_basis="PLANTED",
                 normalization="PLANTED", why_theme_tail="PLANTED")
        v0 = max((x for x in f["history_vintages"] if x["published"] < cutoff), key=lambda x: x["published"])
        y0 = max(int(y) for y in v0["eps_normalized"]) + 1
        # a later print restating every year of the history before CUTOFF (the 'restates' field of CAT 2014-2017)
        last["restates"] = {y: {"eps": 0.01, "note": "PLANTED"} for y in v0["eps_normalized"]}
        # a later withdrawal of every guided field of every guided year (the 'withdrawn' field of CAT 2018-2022)
        for y in sorted({g["fy"] for g in f["guides"] if g["published"] < cutoff}):
            f["guides"].append({"fy": y, "published": later, "source": last["source"], "doc": "PLANTED", "withdrawn_quote": "PLANTED",
                                "note": "PLANTED", "withdrawn": ["eps_guide", "eps_growth", "rev_guide_usd_b", "rev_guide_pct", "rev_words"]})
        last["fy_actual"] = {"fy": y0, "fy_label": "FY99", "eps_normalized": 0.01, "revenue_usd_b": 0.01, "diluted_shares_m": 1.0,
                             "normalization_note": "PLANTED", "op_margin": -50.0, "pretax_margin": -50.0, "pretax_margin_note": "PLANTED",
                             "sales_growth": -60.0, "mach_pct": -60.0, "eng_pct": -60.0, "tax_rate": 0.99, "tax_note": "PLANTED"}
        # and a still later guide for every guided year in the growth forms only, so the latest guide in either form is a growth guide
        for y in sorted({g["fy"] for g in f["guides"]} | {2099}):
            f["guides"].append({"fy": y, "published": (dt.date.fromisoformat(later) + dt.timedelta(days=1)).isoformat(),
                                "source": last["source"], "doc": "PLANTED", "rev_guide_pct": [-50, -40], "eps_growth": [-99, -98],
                                "eps_growth_base": 0.01, "eps_growth_base_note": "PLANTED", "rev_growth_base_b": 0.01,
                                "rev_growth_base_note": "PLANTED", "note": "PLANTED"})
    if TICKER == "BKR":    # a later vintage excluding a year (BKR 2014-2017: the 2015 and 2016 losses)
        v["eps_excluded"] = {**v.get("eps_excluded", {}), "2098": "PLANTED"}
    if TICKER == "XOM":    # the excluded-year and restatement fields (XOM 2021-2023): a later vintage excluding a year, and the planted
                           # print's full-year actuals excluding its own year and restating every earlier one
        v["eps_excluded"] = {**v.get("eps_excluded", {}), "2098": "PLANTED"}
        fa = copy.deepcopy(max((p for p in f["prints"] if "fy_actual" in p and p["published"] < cutoff), key=lambda p: p["published"])["fy_actual"])
        fa.update(fy=2099, fy_label="FY99", eps_normalized=None, excluded_note="PLANTED", normalization_note="PLANTED", revenue_usd_b=0.01,
                  restates={y: 0.01 for y in v["eps_normalized"] if y != "2099"})
        last["fy_actual"] = fa
    for theme in {e["theme"] for e in f["events"] if e["published"] < cutoff}:
        e = copy.deepcopy(max((e for e in f["events"] if e["theme"] == theme and e["published"] < cutoff), key=lambda e: e["published"]))
        e.update(published=later, doc="PLANTED")
        f["events"].append(e)
    f.setdefault("company_names", []).append({"published": later, "name": "PLANTED", "source": last["source"]})
    with open(FACTS, "w", encoding="utf-8") as fh:
        json.dump(f, fh, indent=1)
    ts_cut = dt.datetime.fromisoformat(cutoff).timestamp()
    for c in CACHE:
        with open(c) as fh:
            d = json.load(fh)
        r = d["chart"]["result"][0]
        for blk in r["indicators"].get("quote", []) + r["indicators"].get("adjclose", []):
            for arr in blk.values():
                if isinstance(arr, list):
                    for i, t in enumerate(r["timestamp"]):
                        if t >= ts_cut and arr[i] is not None:
                            arr[i] *= 10
        with open(c, "w") as fh:
            json.dump(d, fh)
    subprocess.run([sys.executable, BUILDER, *dates], check=True, capture_output=True)
    changed = [l for l in git("status", "--porcelain", OUTDIR).splitlines() if l.strip()]
    planted = [d for d in dates if "PLANTED" in open(os.path.join(ARCHIVE, d, "model.py"), encoding="utf-8").read()]
    print(f"{len(dates)} dates before {cutoff}: {len(changed)} files changed, {len(planted)} models contain planted text")
finally:
    for p, b in saved.items():
        shutil.copy(b, p)
    git("checkout", "--", OUTDIR)
sys.exit(1 if changed or planted else 0)
