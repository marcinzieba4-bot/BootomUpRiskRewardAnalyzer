#!/usr/bin/env python3
"""
Injects FLOOR_DATA, worst_case_floor(), and an "Equivalent Pessimism Price"
section into every signal model file.

Concept:
  2022 was a moment of maximum pessimism — market priced in the worst case.
  If that same LEVEL of pessimism returned today, what price would we see?

  EPP = trough_2022 × (1+CPI) + cum_FCF_2023-2025 − net_debt_delta + structural_delta

  trough_2022      : calendar-2022 52-week low (peak pessimism)
  CPI = 0.17       : ~17% cumul. US CPI Jan 2022 – May 2026 (nominal anchor shift)
  cum_fcf_per_share: FCF/share earned FY2023-FY2025 — locked-in value, cannot be un-earned
  net_debt_delta   : +ve = net debt GREW (EPP lower); −ve = balance sheet improved
  structural_delta : +ve = moat/earnings-power improved since 2022 (EPP higher)
                     −ve = structural deterioration since 2022 (EPP lower — same pessimism
                           hits a weaker business, so price is actually lower than CPI-adj 2022)
"""
import re, pathlib, subprocess, sys

# ── PER-STOCK PARAMETERS ─────────────────────────────────────────────────────
# file                   trough  cum_fcf  debt_delta  struct_delta  currency  caveat (or None)
FLOOR = {
    "orcl_signal_model.py": (  65.0,  11.2,   5.2,  +12.0, "$",
        None),
    "msft_signal_model.py": ( 213.0,  29.5,   3.0,  +20.0, "$",
        None),
    "avgo_signal_model.py": (  44.0,  11.9,   5.7,  +15.0, "$",
        "post-10:1 split (Jul 2024); trough & struct_delta adjusted"),
    "sap_signal_model.py":  (  75.0,  13.2,  -3.6,   +8.0, "$",
        None),
    "nke_signal_model.py":  (  82.0,   8.0,   2.0,  -15.0, "$",
        "EPP < CPI-adj trough: China market share permanently lost to Anta/Li-Ning (~$1.5B revenue).\n"
        "     Same pessimism today hits a structurally weaker business."),
    "pypl_signal_model.py": (  63.0,  12.0,  -2.7,  -10.0, "$",
        "EPP < CPI-adj trough: OS-level displacement (Apple Pay/Google Pay) is structural.\n"
        "     Take rate compression is permanent, not cyclical."),
    "cat_signal_model.py":  ( 160.0,  42.0,  -1.9,   -5.0, "$",
        None),
    "xtb_signal_model.py":  (  28.0,  12.0,  -3.0,   +3.0, "PLN",
        None),
    "rcl_signal_model.py":  (  50.0,  37.7, -19.3,  +10.0, "$",
        None),
    "coin_signal_model.py": (  33.0,  22.9, -12.5,   +8.0, "$",
        None),
    "apd_signal_model.py":  ( 210.0,  18.0,  40.6,  -20.0, "$",
        "EPP < CPI-adj trough: $13.5B H2 megaproject capex at risk of write-down.\n"
        "     New CEO strategy reset adds execution uncertainty."),
    "wmb_signal_model.py":  (  26.0,   6.5,   0.8,   +5.0, "$",
        None),
    "syk_signal_model.py":  ( 190.0,  21.4,   4.8,  +10.0, "$",
        None),
    "pm_signal_model.py":   (  82.0,  17.6,   9.0,   +8.0, "$",
        None),
    "mu_signal_model.py":   (  51.0,   3.5,   5.0,   +8.0, "$",
        "cum_fcf is net of FY2023 deeply negative year (-$4/sh); EPP math less reliable than stable compounders."),
}

REFLATION = 0.17

# ── SCORE-SECTION CODE (inserted before "# ── SCORING ─") ────────────────────
FUNC_TEMPLATE = """\

FLOOR_DATA = {{
    "trough_2022":        {trough},
    "cum_fcf_per_share":  {fcf},
    "debt_delta":         {ddt},     # +ve = debt grew (EPP lower); -ve = balance sheet improved
    "structural_delta":   {sdelta},  # +ve = fundamentals improved; -ve = structurally weaker
    "reflation":           0.17,     # cumul. US CPI Jan 2022 - May 2026
}}

def worst_case_floor():
    t, refl   = FLOOR_DATA["trough_2022"], FLOOR_DATA["reflation"]
    fcf, ddt  = FLOOR_DATA["cum_fcf_per_share"], FLOOR_DATA["debt_delta"]
    sdelta    = FLOOR_DATA["structural_delta"]
    ref_adj   = t * (1 + refl)
    epp       = ref_adj + fcf - ddt + sdelta
    bear_p    = SCENARIOS["BEAR"][2]
    gap_pct   = (CURRENT_PRICE - epp) / epp * 100   # +ve = price above EPP; -ve = below
    bvf_pct   = (bear_p - epp) / epp * 100
    return ref_adj, epp, gap_pct, bear_p, bvf_pct

"""

# ── PRINT SECTION (inserted before 'WHAT THE GAP MEANS') ─────────────────────
# Raw string templates — only {caveat_block} is substituted at injection time.
# All other {_x:.0f} expressions remain as-is (they are valid Python f-string
# syntax in the injected code, NOT template substitution targets).

PRINT_TEMPLATE_USD = '''\
# Equivalent Pessimism Price
_ref_adj, _epp, _gap_pct, _bear_p, _bvf = worst_case_floor()
_t      = FLOOR_DATA["trough_2022"]
_fcf    = FLOOR_DATA["cum_fcf_per_share"]
_ddt    = FLOOR_DATA["debt_delta"]
_sdelta = FLOOR_DATA["structural_delta"]
print(f"\\n  EQUIV. PESSIMISM PRICE  (if 2022 pessimism returned today, price would be:)")
print("  " + "─" * (W-2))
print(f"  2022 pessimism trough:                  ${_t:.0f}")
print(f"    + Reflation (+17% cumul. CPI since 2022):  +${_t*0.17:.0f}  \\u2192  ${_t*1.17:.0f}")
print(f"    + Cumul. FCF earned FY2023-2025:           +${_fcf:.0f}  \\u2192  ${_t*1.17+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since 2022 / share:    -${_ddt:.0f}  \\u2192  ${_t*1.17+_fcf-_ddt:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:       +${-_ddt:.0f}  \\u2192  ${_t*1.17+_fcf-_ddt:.0f}")
if _sdelta > 0:
    print(f"    + Structural improvement since 2022:       +${_sdelta:.0f}  \\u2192  ${_epp:.0f}  (moat/earnings-power \\u2191)")
elif _sdelta < 0:
    print(f"    - Structural deterioration since 2022:     -${-_sdelta:.0f}  \\u2192  ${_epp:.0f}  (weaker business today)")
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
    print(f"    Structural damage since 2022 means equal pessimism = lower price than CPI-adj 2022.")
elif _sdelta > 0:
    print(f"    Structural gains since 2022 means equal pessimism = higher price than CPI-adj 2022.")

'''

PRINT_TEMPLATE_PLN = '''\
# Equivalent Pessimism Price
_ref_adj, _epp, _gap_pct, _bear_p, _bvf = worst_case_floor()
_t      = FLOOR_DATA["trough_2022"]
_fcf    = FLOOR_DATA["cum_fcf_per_share"]
_ddt    = FLOOR_DATA["debt_delta"]
_sdelta = FLOOR_DATA["structural_delta"]
print(f"\\n  EQUIV. PESSIMISM PRICE  (if 2022 pessimism returned today, price would be:)")
print("  " + "─" * (W-2))
print(f"  2022 pessimism trough:                  PLN {_t:.0f}")
print(f"    + Reflation (+17% cumul. CPI since 2022):  +PLN {_t*0.17:.0f}  \\u2192  PLN {_t*1.17:.0f}")
print(f"    + Cumul. FCF earned FY2023-2025:           +PLN {_fcf:.0f}  \\u2192  PLN {_t*1.17+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since 2022 / share:    -PLN {_ddt:.0f}  \\u2192  PLN {_t*1.17+_fcf-_ddt:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:       +PLN {-_ddt:.0f}  \\u2192  PLN {_t*1.17+_fcf-_ddt:.0f}")
if _sdelta > 0:
    print(f"    + Structural improvement since 2022:       +PLN {_sdelta:.0f}  \\u2192  PLN {_epp:.0f}  (moat/earnings-power \\u2191)")
elif _sdelta < 0:
    print(f"    - Structural deterioration since 2022:     -PLN {-_sdelta:.0f}  \\u2192  PLN {_epp:.0f}  (weaker business today)")
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
    print(f"    Structural damage since 2022 means equal pessimism = lower price than CPI-adj 2022.")
elif _sdelta > 0:
    print(f"    Structural gains since 2022 means equal pessimism = higher price than CPI-adj 2022.")

'''

GAP_ANCHOR    = 'print(f"\\n  WHAT THE GAP MEANS")'
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

    trough, fcf, ddt, sdelta, currency, caveat = FLOOR[fname]

    # -- 1. Inject FLOOR_DATA + function before SCORING section ---------------
    func_code = FUNC_TEMPLATE.format(
        trough = f"{trough:.1f}",
        fcf    = f"{fcf:.1f}",
        ddt    = f"{ddt:.1f}",
        sdelta = f"{sdelta:.1f}",
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
