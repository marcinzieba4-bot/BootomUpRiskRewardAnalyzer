#!/usr/bin/env python3
"""
Injects FLOOR_DATA, worst_case_floor(), and a downside-floor print section
into every signal model file.

Floor formula (per share):
  floor = trough_2022 × 1.17  +  cum_FCF_2023-2025  -  net_debt_delta

  trough_2022      : calendar-2022 52-week low
  cum_fcf_per_share: FCF/share earned FY2023-FY2025 — locked-in, cannot be un-earned
  debt_delta       : +ve = net debt GREW (floor lower); −ve = balance sheet improved
  reflation = 0.17 : ~17% cumul. US CPI Jan 2022 – May 2026
"""
import re, pathlib, subprocess, sys

# ── PER-STOCK FLOOR PARAMETERS ───────────────────────────────────────────────
FLOOR = {
    # file                   trough  cum_fcf  debt_delta  currency  caveat (or None)
    "orcl_signal_model.py": (  65.0,   11.2,    5.2, "$", None),
    "msft_signal_model.py": ( 213.0,   29.5,    3.0, "$", None),
    "avgo_signal_model.py": (  44.0,   11.9,    5.7, "$", "post-10:1 split (Jul 2024); trough adjusted"),
    "sap_signal_model.py":  (  75.0,   13.2,   -3.6, "$", None),
    "nke_signal_model.py":  (  82.0,    8.0,    2.0, "$",
        "Stock is trading BELOW floor — China brand loss may be a permanent impairment,\n"
        "     not a cyclical trough. Floor assumes earnings-power can be restored."),
    "pypl_signal_model.py": (  63.0,   12.0,   -2.7, "$",
        "Stock is trading BELOW floor — OS-level displacement (Apple/Google) is\n"
        "     structural. FCF floor may overstate true downside support."),
    "cat_signal_model.py":  ( 160.0,   42.0,   -1.9, "$", None),
    "xtb_signal_model.py":  (  28.0,   12.0,   -3.0, "PLN", None),
    "rcl_signal_model.py":  (  50.0,   37.7,  -19.3, "$", None),
    "coin_signal_model.py": (  33.0,   22.9,  -12.5, "$", None),
    "apd_signal_model.py":  ( 210.0,   18.0,   40.6, "$", None),
    "wmb_signal_model.py":  (  26.0,    6.5,    0.8, "$", None),
    "syk_signal_model.py":  ( 190.0,   21.4,    4.8, "$", None),
    "pm_signal_model.py":   (  82.0,   17.6,    9.0, "$", None),
}

REFLATION = 0.17

# ── SCORE-SECTION CODE (inserted before "# ── SCORING ─") ────────────────────
FUNC_TEMPLATE = """\

FLOOR_DATA = {{
    "trough_2022":        {trough},
    "cum_fcf_per_share":  {fcf},
    "debt_delta":         {ddt},   # +ve = debt grew (floor lower); -ve = balance sheet improved
    "reflation":           0.17,   # cumul. US CPI Jan 2022 - May 2026
}}

def worst_case_floor():
    t, refl = FLOOR_DATA["trough_2022"], FLOOR_DATA["reflation"]
    fcf, ddt = FLOOR_DATA["cum_fcf_per_share"], FLOOR_DATA["debt_delta"]
    ref_adj = t * (1 + refl)
    floor   = ref_adj + fcf - ddt
    bear_p  = SCENARIOS["BEAR"][2]
    gap_pct = (floor - CURRENT_PRICE) / CURRENT_PRICE * 100
    bvf_pct = (bear_p - floor) / floor * 100
    return ref_adj, floor, gap_pct, bear_p, bvf_pct

"""

# ── PRINT SECTION (inserted before 'WHAT THE GAP MEANS') ─────────────────────
# Written as raw Python source — no nested f-strings needed.
PRINT_TEMPLATE_USD = '''\
# Downside floor
_ref_adj, _floor, _gap_pct, _bear_p, _bvf = worst_case_floor()
_t   = FLOOR_DATA["trough_2022"]
_fcf = FLOOR_DATA["cum_fcf_per_share"]
_ddt = FLOOR_DATA["debt_delta"]
print(f"\\n  DOWNSIDE FLOOR  (why the 2022 low cannot recur at same nominal price)")
print("  " + "─" * (W-2))
print(f"  2022 reference trough:                  ${_t:.0f}")
print(f"    + Reflation (+17% cumul. CPI since 2022):  +${_t*0.17:.0f}  \\u2192  ${_t*1.17:.0f}")
print(f"    + Cumul. FCF earned FY2023-2025:           +${_fcf:.0f}  \\u2192  ${_t*1.17+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since 2022 / share:    -${_ddt:.0f}  \\u2192  ${_floor:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:       +${-_ddt:.0f}  \\u2192  ${_floor:.0f}")
print(f"  {chr(32)*4}{chr(45)*62}")
print(f"  ANALYTICAL FLOOR (2026 equiv.):         ${_floor:.0f}")
print(f"  Current price:                          ${CURRENT_PRICE:.0f}   downside to floor: {_gap_pct:+.0f}%")
if _bvf >= 0:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is +{_bvf:.0f}% above floor  \\u2713  adequate cushion")
else:
    print(f"  BEAR scenario (${_bear_p:.0f}):   BEAR is {_bvf:.0f}% BELOW floor  \\u2190 structural break scenario")
{caveat_block}print(f"  \\u2192 The 2022 low (${_t:.0f}) cannot recur: ${_fcf:.0f}/share FCF already locked in,")
print(f"    17% inflation raised every nominal anchor. Floor ratchets up each year.")

'''

PRINT_TEMPLATE_PLN = '''\
# Downside floor
_ref_adj, _floor, _gap_pct, _bear_p, _bvf = worst_case_floor()
_t   = FLOOR_DATA["trough_2022"]
_fcf = FLOOR_DATA["cum_fcf_per_share"]
_ddt = FLOOR_DATA["debt_delta"]
print(f"\\n  DOWNSIDE FLOOR  (why the 2022 low cannot recur at same nominal price)")
print("  " + "─" * (W-2))
print(f"  2022 reference trough:                  PLN {_t:.0f}")
print(f"    + Reflation (+17% cumul. CPI since 2022):  +PLN {_t*0.17:.0f}  \\u2192  PLN {_t*1.17:.0f}")
print(f"    + Cumul. FCF earned FY2023-2025:           +PLN {_fcf:.0f}  \\u2192  PLN {_t*1.17+_fcf:.0f}")
if _ddt > 0:
    print(f"    - Net debt increase since 2022 / share:    -PLN {_ddt:.0f}  \\u2192  PLN {_floor:.0f}  (leverage drag)")
else:
    print(f"    + Balance sheet improvement / share:       +PLN {-_ddt:.0f}  \\u2192  PLN {_floor:.0f}")
print(f"  {chr(32)*4}{chr(45)*62}")
print(f"  ANALYTICAL FLOOR (2026 equiv.):         PLN {_floor:.0f}")
print(f"  Current price:                          PLN {CURRENT_PRICE:.0f}   downside to floor: {_gap_pct:+.0f}%")
if _bvf >= 0:
    print(f"  BEAR scenario (PLN {_bear_p:.0f}):   BEAR is +{_bvf:.0f}% above floor  \\u2713  adequate cushion")
else:
    print(f"  BEAR scenario (PLN {_bear_p:.0f}):   BEAR is {_bvf:.0f}% BELOW floor  \\u2190 structural break scenario")
{caveat_block}print(f"  \\u2192 The 2022 low (PLN {_t:.0f}) cannot recur: PLN {_fcf:.0f}/share FCF already locked in,")
print(f"    17% inflation raised every nominal anchor. Floor ratchets up each year.")

'''

GAP_ANCHOR = 'print(f"\\n  WHAT THE GAP MEANS")'
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

    trough, fcf, ddt, currency, caveat = FLOOR[fname]

    # -- 1. Inject FLOOR_DATA + function before SCORING section ---------------
    func_code = FUNC_TEMPLATE.format(
        trough = f"{trough:.1f}",
        fcf    = f"{fcf:.1f}",
        ddt    = f"{ddt:.1f}",
    )
    idx = src.find(SCORING_ANCHOR)
    if idx == -1:
        print(f"  ✗ SCORING anchor not found in {fname}")
        return False
    src = src[:idx] + func_code + src[idx:]

    # -- 2. Inject print section before 'WHAT THE GAP MEANS' ------------------
    template = PRINT_TEMPLATE_PLN if currency == "PLN" else PRINT_TEMPLATE_USD
    caveat_block = build_caveat_block(caveat)
    print_code = template.replace("{caveat_block}", caveat_block)

    # Find the WHAT THE GAP MEANS anchor (after func injection)
    idx2 = src.find(GAP_ANCHOR)
    if idx2 == -1:
        print(f"  ✗ GAP anchor not found in {fname}")
        return False

    # Walk back to the start of the # Verdict comment line (or just the \n before)
    # Insert before the comment above WHAT THE GAP MEANS (usually "# Verdict\n")
    insert_at = idx2
    # Try to include the "# Verdict" comment
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
