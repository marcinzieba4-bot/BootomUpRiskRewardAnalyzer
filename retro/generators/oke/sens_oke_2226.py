#!/usr/bin/env python3
"""How far each OKE 2022-2026 judgement call moves the classes: rebuild the 256 dates with one encoding changed (in memory, into a
scratch folder) and classify offline with retro_tool's own classifier. No outcome is read.

    python3 retro/generators/oke/sens_oke_2226.py <scratch-out>
"""
import contextlib, copy, io, json, os, runpy, shutil, sys, types
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, "retro"))
import build_oke as B  # noqa: E402
import retro_tool as T  # noqa: E402
from build_acn import load_series, weekly_dates  # noqa: E402
facts0 = json.load(open(B.FACTS, encoding="utf-8"))
engine0 = open(B.ENGINE, encoding="utf-8").read()
raw, spx = load_series("OKE"), load_series("^GSPC")
dates = weekly_dates("2022-01-01", "2026-11-27", sorted(raw), facts0["prints"])
assert len(dates) == 256
tax = T.load_taxonomy()


def variant_module(old, new):
    """A copy of build_oke with one line of its source replaced (the module on disk is untouched)."""
    src = open(B.__file__, encoding="utf-8").read()
    assert src.count(old) == 1, old
    m = types.ModuleType("build_oke_variant")
    m.__file__ = B.__file__
    exec(compile(src.replace(old, new), B.__file__, "exec"), m.__dict__)
    return m


def classify_all(facts, engine, tag, mod=B):
    out = os.path.join(OUT, tag)
    shutil.rmtree(out, ignore_errors=True)
    res = {}
    for d in dates:
        with contextlib.redirect_stdout(io.StringIO()):
            mod.build(d, facts, raw, spx, engine, out)
        mp = os.path.join(out, d, "model.py")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            g = runpy.run_path(mp, run_name="__retro__")
        q = T.retro_classify(dict(g["RESULT"], report=buf.getvalue()), g["PIT_PROFILE"], tax)
        res[d] = (q["price_state"], g["RESULT"]["signal_short"])
    return res


def diff(a, b):
    mv = {}
    for d in dates:
        if a[d][0] != b[d][0]:
            k = f"{a[d][0]}->{b[d][0]}"
            mv[k] = mv.get(k, 0) + 1
    ch = [d for d in dates if a[d][0] != b[d][0]]
    return len(ch), sum(a[d][1] != b[d][1] for d in dates), mv, (ch[0], ch[-1]) if ch else None


base = classify_all(facts0, engine0, "main")
cnt, tiers = {}, {}
for d in dates:
    cnt[base[d][0]] = cnt.get(base[d][0], 0) + 1
    tiers[base[d][1]] = tiers.get(base[d][1], 0) + 1
print("main:", cnt, tiers)
json.dump(base, open(os.path.join(OUT, "main_oke_2226.json"), "w"), indent=0)
V = {}


def set_guide(f, doc, fy, **kw):
    g = next(g for g in f["eps_guides"] if g["doc"] == doc and g["fy"] == fy)
    for k in ("eps_guide", "eps_guide_note", "ni_guide_m", "ni_guide_note", "shares_print"):
        g.pop(k, None)
    g.update(kw)


# 1. the Q3 2023 guide on the pre-acquisition basis ($5.81, Magellan out) instead of the consolidated $5.36
f = copy.deepcopy(facts0)
set_guide(f, "Q3 2023 release", 2023, eps_guide=[5.81, 5.81], eps_guide_note="the pre-acquisition midpoint (sensitivity)")
V["the Q3 2023 guide on the pre-acquisition basis ($5.81)"] = (f, engine0, B)
# 2. the Q3 2024 consolidated guide ($5.11, the pending Medallion in) instead of the stand-alone $5.02
f = copy.deepcopy(facts0)
set_guide(f, "Q3 2024 release", 2024, eps_guide=[5.11, 5.11], eps_guide_note="the consolidated midpoint (sensitivity)")
V["the Q3 2024 consolidated guide ($5.11, Medallion pending)"] = (f, engine0, B)
# 3. the Q3 2026 guide without the quarter's one-time tax benefit ($6.30 less $0.53)
f = copy.deepcopy(facts0)
set_guide(f, "Q3 2026 release", 2026, eps_guide=[5.77, 5.77], eps_guide_note="without the tax benefit (sensitivity)")
V["the Q3 2026 guide without the $0.53 tax benefit ($5.77)"] = (f, engine0, B)
# 4. the stated per-share midpoints replaced by their net income ranges over the release's own diluted shares
f = copy.deepcopy(facts0)
NI = {("Q2 2023 release", 2023): (2390, 2590), ("Q3 2023 release", 2023): (2600, 2600), ("Q1 2024 release", 2024): (2730, 3030),
      ("Q3 2024 release", 2024): (2870, 3020), ("Q1 2026 release", 2026): (3210, 3790), ("Q2 2026 release", 2026): (3410, 3790),
      ("Q3 2026 release", 2026): (4090, 4270)}
for (doc, fy), r in NI.items():
    set_guide(f, doc, fy, ni_guide_m=list(r), shares_print=doc.replace(" release", ""),
              **({"ni_guide_note": "the consolidated point (sensitivity)"} if r[0] == r[1] else {}))
V["the stated midpoints replaced by net income over the release's shares"] = (f, engine0, B)
# 5. no EPS guide used from FY2022
f = copy.deepcopy(facts0)
f["eps_guides"] = [g for g in f["eps_guides"] if g["fy"] < 2022]
V["no EPS guide used from FY2022: the last full year's EPS"] = (f, engine0, B)
# 6. FY2023 and FY2024 at derived figures without their listed net benefits (87 and 30 cents)
f = copy.deepcopy(facts0)
for v in f["history_vintages"]:
    for y, x in (("2023", 4.61), ("2024", 4.87)):
        if y in v["eps_normalized"]:
            v["eps_normalized"][y] = x
V["FY2023 at $4.61 and FY2024 at $4.87 without their listed net benefits"] = (f, engine0, B)
# 7. BASE on the latest quarter's net margin growth instead of revenue growth as reported (carried)
mod = variant_module('    fwd = [latest["sales_pct"]] * 2\n', '    fwd = [latest["nm_pct"]] * 2\n')
V["BASE on the latest quarter's net margin growth instead of revenues"] = (facts0, engine0, mod)
# 8. no share-count term in BASE (the Magellan and EnLink shares read as dilution as published)
e = engine0.replace("BUYBACK           = _cagr(", "BUYBACK           = 0.0 * _cagr(", 1)
assert e != engine0
V["no share-count term in BASE (the merger shares not read as dilution)"] = (facts0, e, B)
# 9. a five-year P/E window
mod = variant_module('    window = [d for d in days if d > minus_years(as_of, 10) and d >= h["pe_window_start"]]\n',
                     '    window = [d for d in days if d > minus_years(as_of, 5) and d >= h["pe_window_start"]]\n')
V["a five-year P/E window"] = (facts0, engine0, mod)
# 10. the window's days before the ONE Gas separation at Yahoo's adjusted price (without ONE Gas) instead of as traded (carried)
mod = variant_module('    for x in [x for x in dists if x["effective"] <= as_of]:\n', '    for x in []:\n')
V["days before 2014-02-03 at Yahoo's adjusted price (without ONE Gas)"] = (facts0, engine0, mod)
# 11. 2010-2013 EPS as the FY2013 10-K reports them (the FY2014 restatement unused; carried)
f = copy.deepcopy(facts0)
v13 = next(v for v in f["history_vintages"] if v["fy_label"] == "FY13")
for v in f["history_vintages"]:
    if v["published"] > v13["published"] and v["fy_label"] != "FY13":
        for y in ("2010", "2011", "2012", "2013"):
            if y in v["eps_normalized"]:
                v["eps_normalized"][y] = v13["eps_normalized"][y]
                v["eps_published"][y] = v13["eps_published"][y]
V["2010-2013 EPS as the FY2013 10-K reports them (no restatement)"] = (f, engine0, B)
# 10./11. the Distribution signal (n/r from Q1 2014, scored at BASE) at its BEAR or XBULL value
for lab, val in (("BEAR", "-88.0"), ("XBULL", "57.0")):
    e = engine0.replace('_f(LATEST["dist_pct"])', f'(_f(LATEST["dist_pct"]) if LATEST["dist_pct"] is not None else {val})', 1)
    assert e != engine0
    V[f"the n/r Distribution signal at its {lab} value"] = (facts0, e, B)
# 12./13. every data signal at its BEAR or XBULL value
for lab, vals in (("BEAR", ("-8.0", "-88.0", "-38.0", "-1350.0", "-1150.0")), ("XBULL", ("38.0", "57.0", "261.0", "430.0", "620.0"))):
    e = engine0
    i0, i1 = e.index("SIGNALS = ["), e.index("THEME_SIGNAL_NAME, \"/4\"")
    blk = e[i0:i1]
    for key, val in zip(('_f(LATEST["nm_pct"])', '_f(LATEST["dist_pct"])', '_f(LATEST["sales_pct"])', '_f(LATEST["opm_bp"])',
                         '_f(LATEST["ptm_bp"])'), vals):
        assert key in blk
        blk = blk.replace(key, val)
    V[f"every data signal at its {lab} value"] = (facts0, e[:i0] + blk + e[i1:], B)
for name, (f, e, m) in V.items():
    r = classify_all(f, e, "v", m)
    c, t, mv, span = diff(base, r)
    print(f"{name}: {c} classes, {t} tiers {mv} {span or ''}", flush=True)
