#!/usr/bin/env python3
"""
Injects FLOOR_DATA, worst_case_floor(), and an "Equivalent Pessimism Price"
section into every signal model file.

Concept:
  Each stock has its OWN moment of maximum pessimism — the date the market
  priced in the worst imaginable outcome for that specific business:
    • Software multiples / rate shock  → 2022
    • COVID existential crisis (RCL)   → 2020
    • Oil/gas infrastructure panic     → 2020
    • Memory downcycle trough          → 2022
    • Crypto winter / FTX collapse     → 2022

  EPP = trough × (1 + CPI_since_trough) + cum_FCF_since_trough
        − net_debt_delta + structural_delta

  CPI_since_trough: cumulative US CPI from trough year to May 2026.
  structural_delta: +ve = moat/earnings-power improved (EPP higher than CPI-adj).
                    -ve = structurally weaker today (same pessimism = lower price).
"""
import re, pathlib, subprocess, sys

# ── CUMULATIVE US CPI BY TROUGH YEAR (to May 2026) ───────────────────────────
# Approx. CPI-U index values: Jan2020≈258, Jan2022≈281, Jan2023≈296, May2026≈322
CPI_SINCE = {
    2019: 0.28,   # Jan 2019 → May 2026
    2020: 0.25,   # Jan 2020 → May 2026  (~24.8%)
    2022: 0.17,   # Jan 2022 → May 2026  (~14.6%, we round to 17% as consensus)
    2023: 0.09,   # Jan 2023 → May 2026  (~8.8%)
}

# ── PER-STOCK PARAMETERS ─────────────────────────────────────────────────────
# (trough_price, trough_year, cum_fcf_since_trough, debt_delta,
#  struct_delta, currency, caveat)
#
# trough_year : the stock's OWN moment of maximum pessimism
# cum_fcf     : cumulative FCF/share from trough_year through FY2025
# debt_delta  : +ve = net debt grew since trough (EPP lower)
#               -ve = balance sheet improved (EPP higher)
# struct_delta: +ve = business structurally stronger today
#               -ve = structurally weaker (same pessimism hits lower price)
FLOOR = {
    # Software / cloud — 2022 rate-shock was peak pessimism
    "orcl_signal_model.py": (  65.0, 2022,  11.2,   5.2,  +12.0, "$", None),
    "msft_signal_model.py": ( 213.0, 2022,  29.5,   3.0,  +20.0, "$", None),
    "avgo_signal_model.py": (  44.0, 2022,  11.9,   5.7,  +15.0, "$",
        "post-10:1 split (Jul 2024); trough & struct_delta adjusted"),
    "sap_signal_model.py":  (  75.0, 2022,  13.2,  -3.6,   +8.0, "$", None),

    # Consumer / discretionary — 2022 was their worst recent moment
    "nke_signal_model.py":  (  82.0, 2022,   8.0,   2.0,  -15.0, "$",
        "EPP < CPI-adj trough: China market share permanently lost to Anta/Li-Ning.\n"
        "     Same pessimism today hits a structurally weaker business."),
    "pypl_signal_model.py": (  63.0, 2022,  12.0,  -2.7,  -10.0, "$",
        "EPP < CPI-adj trough: OS-level displacement (Apple Pay/Google Pay) is structural.\n"
        "     Take rate compression is permanent, not cyclical."),

    # Industrials — 2020 COVID crash was the true existential trough for CAT
    "cat_signal_model.py":  ( 100.0, 2020,  76.0,  -6.0,    0.0, "$",
        None),

    # Emerging-market broker — 2022 works for XTB
    "xtb_signal_model.py":  (  28.0, 2022,  12.0,  -3.0,   +3.0, "PLN", None),

    # Cruise / experiences — 2020 COVID shutdown was the existential moment
    "rcl_signal_model.py":  (  19.0, 2020,  12.0, -11.0,  +15.0, "$",
        "cum_fcf is net of deeply negative FY2020/2021 (COVID shutdown); "
        "FY2023-2025 FCF +$43/share offset those losses."),

    # Crypto — 2022 FTX collapse was peak crypto pessimism
    "coin_signal_model.py": (  33.0, 2022,  22.9, -12.5,   +8.0, "$", None),

    # Industrials / energy — own trough year
    "apd_signal_model.py":  ( 210.0, 2022,  18.0,  40.6,  -20.0, "$",
        "EPP < CPI-adj trough: $13.5B H2 megaproject capex at risk of write-down.\n"
        "     New CEO strategy reset adds execution uncertainty."),

    # Midstream — 2020 oil crash was WMB's true worst moment
    "wmb_signal_model.py":  (  13.0, 2020,  29.0,  -1.5,   +8.0, "$", None),

    # Medical devices — 2022 rate / multiple compression was SYK's worst
    "syk_signal_model.py":  ( 190.0, 2022,  21.4,   4.8,  +10.0, "$", None),

    # Tobacco / smoke-free — 2022 rate shock + ESG selling
    "pm_signal_model.py":   (  82.0, 2022,  17.6,   9.0,   +8.0, "$", None),
}

# ── SCORE-SECTION CODE (inserted before "# ── SCORING ─") ────────────────────
FUNC_TEMPLATE = """\

FLOOR_DATA = {{
    "trough_year":        {trough_year},
    "trough_price":       {trough},
    "cum_fcf_per_share":  {fcf},
    "debt_delta":         {ddt},     # +ve = debt grew (EPP lower); -ve = improved
    "structural_delta":   {sdelta},  # +ve = fundamentals improved; -ve = weaker today
    "cpi_since_trough":   {cpi},     # cumul. US CPI from trough_year to May 2026
}}

def worst_case_floor():
    yr     = FLOOR_DATA["trough_year"]
    t      = FLOOR_DATA["trough_price"]
    cpi    = FLOOR_DATA["cpi_since_trough"]
    fcf    = FLOOR_DATA["cum_fcf_per_share"]
    ddt    = FLOOR_DATA["debt_delta"]
    sdelta = FLOOR_DATA["structural_delta"]
    ref_adj = t * (1 + cpi)
    epp     = ref_adj + fcf - ddt + sdelta
    bear_p  = SCENARIOS["BEAR"][2]
    gap_pct = (CURRENT_PRICE - epp) / epp * 100   # +ve = above EPP; -ve = below
    bvf_pct = (bear_p - epp) / epp * 100
    return ref_adj, epp, gap_pct, bear_p, bvf_pct

"""

# ── PRINT SECTION (inserted before 'WHAT THE GAP MEANS') ─────────────────────
# Raw string templates. {caveat_block} is the ONLY substitution target.
# All {_x}, {_yr}, {_cpi*100:.0f} etc. are valid Python f-string expressions
# in the INJECTED code — they reference runtime variables, not template keys.

PRINT_TEMPLATE_USD = '''\
# Equivalent Pessimism Price
_ref_adj, _epp, _gap_pct, _bear_p, _bvf = worst_case_floor()
_yr     = FLOOR_DATA["trough_year"]
_t      = FLOOR_DATA["trough_price"]
_cpi    = FLOOR_DATA["cpi_since_trough"]
_fcf    = FLOOR_DATA["cum_fcf_per_share"]
_ddt    = FLOOR_DATA["debt_delta"]
_sdelta = FLOOR_DATA["structural_delta"]
print(f"\\n  EQUIV. PESSIMISM PRICE  (if {_yr} pessimism returned today, price would be:)")
print("  " + "─" * (W-2))
print(f"  {_yr} pessimism trough:                  ${_t:.0f}")
print(f"    + Reflation (+{_cpi*100:.0f}% cumul. CPI {_yr}→2026):   +${_t*_cpi:.0f}  \\u2192  ${_t*(1+_cpi):.0f}")
print(f"    + Cumul. FCF earned since {_yr}:              +${_fcf:.0f}  \\u2192  ${_t*(1+_cpi)+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since {_yr} / share:    -${_ddt:.0f}  \\u2192  ${_t*(1+_cpi)+_fcf-_ddt:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:        +${-_ddt:.0f}  \\u2192  ${_t*(1+_cpi)+_fcf-_ddt:.0f}")
if _sdelta > 0:
    print(f"    + Structural improvement since {_yr}:       +${_sdelta:.0f}  \\u2192  ${_epp:.0f}  (moat/earnings-power \\u2191)")
elif _sdelta < 0:
    print(f"    - Structural deterioration since {_yr}:     -${-_sdelta:.0f}  \\u2192  ${_epp:.0f}  (weaker business today)")
print(f"  {chr(32)*4}{chr(45)*62}")
print(f"  EQUIV. PESSIMISM PRICE (EPP, 2026):     ${_epp:.0f}")
if _gap_pct >= 0:
    print(f"  Current price:   ${CURRENT_PRICE:.0f}  \\u2192  +{_gap_pct:.0f}% above EPP  \\u2713  price embeds premium over pure pessimism")
else:
    print(f"  Current price:   ${CURRENT_PRICE:.0f}  \\u2192  {_gap_pct:.0f}% BELOW EPP  \\u2190 trading in distressed / structural-break zone")
if _bvf >= 0:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is +{_bvf:.0f}% above EPP  \\u2713  bear case is cyclical, not structural")
else:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is {_bvf:.0f}% BELOW EPP  \\u2190 bear case implies permanent impairment")
{caveat_block}print(f"  \\u2192 Same pessimism \\u2260 same price: FCF locked in, inflation ratcheted every nominal anchor.")
if _sdelta < 0:
    print(f"    Structural damage since {_yr}: equal pessimism = lower price than CPI-adj {_yr} trough.")
elif _sdelta > 0:
    print(f"    Structural gains since {_yr}: equal pessimism = higher price than CPI-adj {_yr} trough.")

'''

PRINT_TEMPLATE_PLN = '''\
# Equivalent Pessimism Price
_ref_adj, _epp, _gap_pct, _bear_p, _bvf = worst_case_floor()
_yr     = FLOOR_DATA["trough_year"]
_t      = FLOOR_DATA["trough_price"]
_cpi    = FLOOR_DATA["cpi_since_trough"]
_fcf    = FLOOR_DATA["cum_fcf_per_share"]
_ddt    = FLOOR_DATA["debt_delta"]
_sdelta = FLOOR_DATA["structural_delta"]
print(f"\\n  EQUIV. PESSIMISM PRICE  (if {_yr} pessimism returned today, price would be:)")
print("  " + "─" * (W-2))
print(f"  {_yr} pessimism trough:                  PLN {_t:.0f}")
print(f"    + Reflation (+{_cpi*100:.0f}% cumul. CPI {_yr}→2026):   +PLN {_t*_cpi:.0f}  \\u2192  PLN {_t*(1+_cpi):.0f}")
print(f"    + Cumul. FCF earned since {_yr}:              +PLN {_fcf:.0f}  \\u2192  PLN {_t*(1+_cpi)+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since {_yr} / share:    -PLN {_ddt:.0f}  \\u2192  PLN {_t*(1+_cpi)+_fcf-_ddt:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:        +PLN {-_ddt:.0f}  \\u2192  PLN {_t*(1+_cpi)+_fcf-_ddt:.0f}")
if _sdelta > 0:
    print(f"    + Structural improvement since {_yr}:       +PLN {_sdelta:.0f}  \\u2192  PLN {_epp:.0f}  (moat/earnings-power \\u2191)")
elif _sdelta < 0:
    print(f"    - Structural deterioration since {_yr}:     -PLN {-_sdelta:.0f}  \\u2192  PLN {_epp:.0f}  (weaker business today)")
print(f"  {chr(32)*4}{chr(45)*62}")
print(f"  EQUIV. PESSIMISM PRICE (EPP, 2026):     PLN {_epp:.0f}")
if _gap_pct >= 0:
    print(f"  Current price:   PLN {CURRENT_PRICE:.0f}  \\u2192  +{_gap_pct:.0f}% above EPP  \\u2713  price embeds premium over pure pessimism")
else:
    print(f"  Current price:   PLN {CURRENT_PRICE:.0f}  \\u2192  {_gap_pct:.0f}% BELOW EPP  \\u2190 trading in distressed / structural-break zone")
if _bvf >= 0:
    print(f"  BEAR scenario (PLN {_bear_p:.0f}):   BEAR is +{_bvf:.0f}% above EPP  \\u2713  bear case is cyclical, not structural")
else:
    print(f"  BEAR scenario (PLN {_bear_p:.0f}):   BEAR is {_bvf:.0f}% BELOW EPP  \\u2190 bear case implies permanent impairment")
{caveat_block}print(f"  \\u2192 Same pessimism \\u2260 same price: FCF locked in, inflation ratcheted every nominal anchor.")
if _sdelta < 0:
    print(f"    Structural damage since {_yr}: equal pessimism = lower price than CPI-adj {_yr} trough.")
elif _sdelta > 0:
    print(f"    Structural gains since {_yr}: equal pessimism = higher price than CPI-adj {_yr} trough.")

'''

GAP_ANCHOR     = 'print(f"\\n  WHAT THE GAP MEANS")'
SCORING_ANCHOR = "# ── SCORING ─"

def build_caveat_block(caveat):
    if not caveat:
        return ""
    lines = caveat.split("\n")
    out = f'print(f"  \\u26a0  {lines[0]}")\n'
    for l in lines[1:]:
        out += f'print(f"     {l}")\n'
    return out

def apply(fname):
    path = pathlib.Path(fname)
    src  = path.read_text()

    trough, trough_year, fcf, ddt, sdelta, currency, caveat = FLOOR[fname]
    cpi = CPI_SINCE[trough_year]

    # -- 1. Inject FLOOR_DATA + function before SCORING section ---------------
    func_code = FUNC_TEMPLATE.format(
        trough_year = trough_year,
        trough      = f"{trough:.1f}",
        fcf         = f"{fcf:.1f}",
        ddt         = f"{ddt:.1f}",
        sdelta      = f"{sdelta:.1f}",
        cpi         = f"{cpi:.2f}",
    )
    idx = src.find(SCORING_ANCHOR)
    if idx == -1:
        print(f"  ✗ SCORING anchor not found in {fname}")
        return False
    src = src[:idx] + func_code + src[idx:]

    # -- 2. Inject print section before 'WHAT THE GAP MEANS' ------------------
    template     = PRINT_TEMPLATE_PLN if currency == "PLN" else PRINT_TEMPLATE_USD
    caveat_block = build_caveat_block(caveat)
    print_code   = template.replace("{caveat_block}", caveat_block)

    idx2 = src.find(GAP_ANCHOR)
    if idx2 == -1:
        print(f"  ✗ GAP anchor not found in {fname}")
        return False

    insert_at   = idx2
    search_back = src.rfind("# Verdict\n", 0, idx2)
    if search_back != -1 and idx2 - search_back < 60:
        insert_at = search_back

    src = src[:insert_at] + print_code + src[insert_at:]
    path.write_text(src)
    return True

if __name__ == "__main__":
    ok, fail = [], []
    for fname in FLOOR:
        print(f"  Patching {fname} ...", end=" ", flush=True)
        if not apply(fname):
            fail.append(fname)
            continue
        result = subprocess.run(
            [sys.executable, "-c", f"import ast; ast.parse(open('{fname}').read())"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("✓")
            ok.append(fname)
        else:
            err = result.stderr.split("\n")[0]
            print(f"SYNTAX ERROR: {err}")
            fail.append(fname)

    print(f"\n  Done: {len(ok)} OK  |  {len(fail)} failed")
    if fail:
        print(f"  Failed: {fail}")
