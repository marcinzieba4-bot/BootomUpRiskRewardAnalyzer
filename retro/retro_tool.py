#!/usr/bin/env python3
"""
Retrospective (point-in-time) analyses: validate, classify, archive, score.

A retrospective is one directory  archive/retrospective/<TICKER>/<AS_OF>/  holding
model.py — a signal model in the house 6-section format whose every input was
public on AS_OF.  This tool never edits model.py; it only judges and files it.

  run      execute model.py, enforce point-in-time discipline, classify with the
           era-appropriate durability profile, write report.txt + analysis.json,
           update archive/retrospective/index.json
  outcome  HINDSIGHT: what the stock actually did after AS_OF (+6m/+1y/+2y vs SPY
           and the 15%/yr hurdle, which scenario band it landed in).  Written to
           outcome.json, never read back by `run`
  lint     point-in-time checks only, no classification
  index    rebuild index.json from every analysis.json / outcome.json
  series   markdown table of one ticker's retrospectives -> archive/retrospective/<T>/SERIES.md

Point-in-time rules enforced by `run` (errors abort, nothing is written):
  1. every SOURCES[i]["published"] <= AS_OF, and PRICE_DATE <= AS_OF
  2. no anachronism (retro/taxonomy_eras.json) whose first_seen > AS_OF appears in
     model.py, and no ISO date later than AS_OF  (model may whitelist in LINT_ALLOW)
  3. PIT_PROFILE kind is legal in the era: a disruption theme (AI_EXPOSED is the
     GENAI theme) needs theme.live_from <= AS_OF plus cited evidence from SOURCES;
     every theme_watch entry must also be live on AS_OF
  4. CURRENT_PRICE matches the actual close on PRICE_DATE (when prices are reachable)
  Calendar years after AS_OF that are not fiscal-year labels (FY2025 / FY25E) are
  reported as warnings.

Usage
  python3 retro/retro_tool.py run      archive/retrospective/ACN/2023-06-30
  python3 retro/retro_tool.py outcome  archive/retrospective/ACN/2023-06-30
  python3 retro/retro_tool.py lint     archive/retrospective/ACN/2023-06-30
  python3 retro/retro_tool.py index
  python3 retro/retro_tool.py series   ACN
"""
import argparse
import contextlib
import datetime as dt
import glob
import io
import json
import math
import os
import re
import runpy
import sys
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from quality_classify import classify, price_state, KIND_LABEL  # noqa: E402

ARCHIVE = os.path.join(ROOT, "archive", "retrospective")
INDEX = os.path.join(ARCHIVE, "index.json")
TAXONOMY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "taxonomy_eras.json")
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cache")
REQUIRED_RETURN = 0.15          # the house hurdle used by every signal model
BASE_KINDS = ("DURABLE", "CYCLICAL", "STRUCTURAL", "TURNAROUND", "SPECIAL")


def load_taxonomy():
    with open(TAXONOMY, encoding="utf-8") as fh:
        return json.load(fh)


# ─────────────────────────────────────────────────────────────────────────────
# Model execution
# ─────────────────────────────────────────────────────────────────────────────
def load_model(folder):
    path = os.path.join(folder, "model.py")
    if not os.path.exists(path):
        sys.exit(f"no model.py in {folder}")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        g = runpy.run_path(path, run_name="__retro__")
    with open(path, encoding="utf-8") as fh:
        src = fh.read()
    for k in ("TICKER", "AS_OF", "PRICE_DATE", "CURRENT_PRICE", "SOURCES", "PIT_PROFILE", "RESULT"):
        if k not in g:
            sys.exit(f"{path}: missing required constant {k}")
    return g, buf.getvalue(), src


# ─────────────────────────────────────────────────────────────────────────────
# Point-in-time checks
# ─────────────────────────────────────────────────────────────────────────────
def pit_checks(g, src, tax):
    """Return (errors, warnings)."""
    errs, warns = [], []
    as_of = g["AS_OF"]
    allow = {a.lower() for a in g.get("LINT_ALLOW", [])}

    # 1. sources and price date
    ids = set()
    for s in g["SOURCES"]:
        ids.add(s["id"])
        if s["published"] > as_of:
            errs.append(f"source {s['id']} published {s['published']} after AS_OF {as_of}")
    if g["PRICE_DATE"] > as_of:
        errs.append(f"PRICE_DATE {g['PRICE_DATE']} after AS_OF {as_of}")

    # 2. anachronisms and future dates in the model text
    for t in tax["anachronisms"]["terms"]:
        if t["first_seen"] > as_of and t["term"].lower() not in allow:
            if re.search(r"(?<![\w-])" + re.escape(t["term"]) + r"(?![\w-])", src, re.I):
                errs.append(f"anachronism '{t['term']}' (first seen {t['first_seen']}) in a {as_of} analysis")
    for d in sorted(set(re.findall(r"\b(?:19|20)\d\d-[01]\d-[0-3]\d\b", src))):
        if d > as_of and d not in allow:
            errs.append(f"date {d} is after AS_OF {as_of}")
    years = sorted({m.group(1) for m in re.finditer(r"(?<![\w-])((?:19|20)\d\d)(?![\d-])(?!E\b)", src)
                    if src[max(0, m.start() - 2): m.start()] != "FY"})
    late = [y for y in years if y > as_of[:4] and y not in allow]
    if late:
        warns.append(f"calendar year(s) {', '.join(late)} after {as_of[:4]} outside FY labels — make sure they are forecasts")

    # 3. era-legal durability profile
    p = g["PIT_PROFILE"]
    themes = tax["themes"]
    kind, theme = p.get("kind"), p.get("theme")
    if kind == "AI_EXPOSED":
        theme = theme or "GENAI"
    if kind not in BASE_KINDS + ("AI_EXPOSED", tax["disruption_kind"]):
        errs.append(f"unknown kind {kind}")
    if kind in ("AI_EXPOSED", tax["disruption_kind"]):
        if theme not in themes:
            errs.append(f"kind {kind} needs a theme from taxonomy_eras.json, got {theme}")
        else:
            th = themes[theme]
            if th["live_from"] > as_of:
                errs.append(f"theme {theme} only live from {th['live_from']}; cannot classify a {as_of} analysis under it")
            cited = [e for e in p.get("evidence", []) if e in ids]
            if not cited:
                errs.append(f"theme {theme} assigned without point-in-time evidence (PIT_PROFILE.evidence -> SOURCES ids)")
    for w in p.get("theme_watch", []):
        th = themes.get(w.get("theme"))
        if th is None:
            errs.append(f"theme_watch names unknown theme {w.get('theme')}")
        elif th["live_from"] > as_of:
            errs.append(f"theme_watch {w['theme']} not live until {th['live_from']}")
    if not 1 <= int(p.get("risk", 0)) <= 5:
        errs.append("PIT_PROFILE.risk must be 1..5")
    return errs, warns


# ─────────────────────────────────────────────────────────────────────────────
# Prices (Yahoo chart API, cached; used for the as-of price check and outcomes)
# ─────────────────────────────────────────────────────────────────────────────
def fetch_prices(symbol):
    """{date: close} and [(ex_date, amount)] for the full history."""
    os.makedirs(CACHE, exist_ok=True)
    fp = os.path.join(CACHE, f"{symbol.replace('^', '_')}.json")
    if not os.path.exists(fp) or (dt.datetime.now().timestamp() - os.path.getmtime(fp)) > 86400:
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.request.quote(symbol)}"
               f"?period1=946684800&period2={int(dt.datetime.now().timestamp())}&interval=1d&events=div")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30) as r, open(fp, "wb") as fh:
            fh.write(r.read())
    with open(fp, encoding="utf-8") as fh:
        d = json.load(fh)["chart"]["result"][0]
    off = d["meta"]["gmtoffset"]
    day = lambda t: dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
    closes = {day(t): c for t, c in zip(d["timestamp"], d["indicators"]["quote"][0]["close"]) if c is not None}
    divs = sorted((day(v["date"]), v["amount"]) for v in d.get("events", {}).get("dividends", {}).values())
    return closes, divs


def close_on_or_before(closes, date):
    ds = [d for d in closes if d <= date]
    return (max(ds), closes[max(ds)]) if ds else (None, None)


def add_months(date, months):
    y, m = divmod(int(date[:4]) * 12 + int(date[5:7]) - 1 + months, 12)
    return f"{y:04d}-{m + 1:02d}-{min(int(date[8:]), 28 if m + 1 == 2 else 30):02d}"


# ─────────────────────────────────────────────────────────────────────────────
# Classification with the point-in-time profile
# ─────────────────────────────────────────────────────────────────────────────
def retro_classify(entry, profile, tax):
    kind, theme = profile["kind"], profile.get("theme")
    if kind == "AI_EXPOSED":
        theme = "GENAI"
    themed = kind == tax["disruption_kind"]
    q = classify(entry, profile=("AI_EXPOSED" if themed else kind, int(profile["risk"]), profile["why"]))
    if themed:      # the AI_EXPOSED class family, relabelled for the era's theme
        label = tax["themes"][theme]["label"]
        for k in ("quality_class", "quality_label"):
            q[k] = q[k].replace("AI-", f"{label}-")
        q["quality_note"] = q["quality_note"].replace(KIND_LABEL["AI_EXPOSED"], f"{label}-exposed franchise")
        q["business_kind"] = kind
    q["theme"] = theme
    return q


def cmd_run(folder, offline=False):
    tax = load_taxonomy()
    g, report, src = load_model(folder)
    errs, warns = pit_checks(g, src, tax)
    if not offline:
        try:
            closes, _ = fetch_prices(g.get("YAHOO_SYMBOL", g["TICKER"]))
            _, actual = close_on_or_before(closes, g["PRICE_DATE"])
            if actual is None or abs(actual / g["CURRENT_PRICE"] - 1) > 0.005:
                errs.append(f"CURRENT_PRICE {g['CURRENT_PRICE']} != actual close {actual} on {g['PRICE_DATE']}")
        except OSError as e:
            warns.append(f"price check skipped ({e})")
    for w in warns:
        print(f"WARNING: {w}")
    if errs:
        for e in errs:
            print(f"ERROR: {e}")
        sys.exit("point-in-time validation failed — nothing written")

    entry = dict(g["RESULT"], report=report)
    q = retro_classify(entry, g["PIT_PROFILE"], tax)
    # the classifier re-parses the narrative; it must agree with the model's own numbers
    r = g["RESULT"]
    assert abs(q["_rb"] - r["ratio_b"]) < 0.01 and abs(q["_adj"] - r["adj_gap"]) < 0.01, (q, r)
    assert q["_cons"] is not None and abs(q["_cons"] - r["cons_return_2yr"]) < 0.1, (q, r)

    robustness = r.get("robustness") or []
    for row in robustness:     # same price rules as the live site, one variant at a time
        row["price_state"] = price_state(row["ratio_b"], row["epp_gap_pct"], row["adj_gap"],
                                         row.get("cons_return_2yr"), row["verdict"])
    analysis = {
        "_doc": "Point-in-time retrospective. Every input was public on as_of; see sources. "
                "Hindsight lives only in outcome.json.",
        "ticker": g["TICKER"], "company": r.get("company"), "as_of": g["AS_OF"],
        "price_date": g["PRICE_DATE"], "price": g["CURRENT_PRICE"],
        "methodology": g.get("METHODOLOGY", ""),
        "pit_profile": g["PIT_PROFILE"],
        "classification": {k: v for k, v in q.items() if not k.startswith("_")},
        "legacy_signal_short": r["signal_short"], "legacy_signal": r["signal"],
        "metrics": {k: r[k] for k in ("ratio_b", "ratio_b_fmt", "epp", "epp_gap_pct", "epp_adj",
                                      "proxy_composite", "sca", "adj_composite", "market_composite",
                                      "adj_gap", "valuation", "cons_return_2yr", "scenarios") if k in r},
        "robustness": robustness,
        "robustness_price_states": sorted({row["price_state"] for row in robustness}),
        "summary": r["summary"],
        "sources": g["SOURCES"],
        "warnings": warns,
        "generated": dt.date.today().isoformat(),
    }
    with open(os.path.join(folder, "report.txt"), "w", encoding="utf-8") as fh:
        fh.write(report)
    with open(os.path.join(folder, "analysis.json"), "w", encoding="utf-8") as fh:
        json.dump(analysis, fh, ensure_ascii=False, indent=1)
    cmd_index()
    print(f"{g['TICKER']} @ {g['AS_OF']}: {q['quality_label']}  "
          f"[{q['business_kind']}/{q['obsolescence_risk']}, price {q['price_state']}, model tier {r['signal_short']}]")


# ─────────────────────────────────────────────────────────────────────────────
# Outcome (hindsight)
# ─────────────────────────────────────────────────────────────────────────────
def total_return(closes, divs, start, end):
    d0, p0 = close_on_or_before(closes, start)
    d1, p1 = close_on_or_before(closes, end)
    cash = sum(a for d, a in divs if d0 < d <= d1)
    return d1, p1, (p1 + cash) / p0 - 1, cash


def cmd_outcome(folder):
    with open(os.path.join(folder, "analysis.json"), encoding="utf-8") as fh:
        a = json.load(fh)
    g, _, _ = load_model(folder)
    closes, divs = fetch_prices(g.get("YAHOO_SYMBOL", a["ticker"]))
    bc, bd = fetch_prices(g.get("BENCHMARK", "SPY"))
    as_of, today = a["as_of"], max(closes)
    horizons = {}
    for label, months in (("6m", 6), ("1y", 12), ("2y", 24), ("3y", 36)):
        end = add_months(as_of, months)
        if end > today:
            continue
        d1, p1, tr, cash = total_return(closes, divs, as_of, end)
        _, _, btr, _ = total_return(bc, bd, as_of, end)
        horizons[label] = {"date": d1, "price": round(p1, 2), "dividends": round(cash, 2),
                           "total_return_pct": round(tr * 100, 1),
                           "benchmark_total_return_pct": round(btr * 100, 1),
                           "excess_pct": round((tr - btr) * 100, 1),
                           "hurdle_pct": round(((1 + REQUIRED_RETURN) ** (months / 12) - 1) * 100, 1)}
    window = sorted(d for d in closes if as_of < d <= add_months(as_of, 24))
    path = [closes[d] for d in window]
    peak, mdd = a["price"], 0.0
    for p in path:
        peak = max(peak, p)
        mdd = min(mdd, p / peak - 1)
    hi = max(window, key=lambda d: closes[d])
    lo = min(window, key=lambda d: closes[d])
    # a single 2-year endpoint is hostage to that day's price; the average price over
    # months 12-24 is the endpoint-robust read (price return, dividends excluded)
    late = [closes[d] for d in window if d > add_months(as_of, 12)]
    out = {"_doc": "HINDSIGHT — computed after the fact from market data; not an input to the analysis.",
           "ticker": a["ticker"], "as_of": as_of, "computed": dt.date.today().isoformat(),
           "data_source": f"Yahoo Finance daily closes + dividends ({a['ticker']}, benchmark {g.get('BENCHMARK', 'SPY')})",
           "horizons": horizons,
           "within_2y": {"high": {"date": hi, "price": round(closes[hi], 2)},
                         "low": {"date": lo, "price": round(closes[lo], 2)},
                         "max_drawdown_pct": round(mdd * 100, 1),
                         "return_to_avg_price_m12_m24_pct": round((sum(late) / len(late) / a["price"] - 1) * 100, 1) if late else None}}
    sc = a["metrics"].get("scenarios")
    if sc and "2y" in horizons:
        p2 = horizons["2y"]["price"]
        out["scenario_landing_2y"] = min(sc, key=lambda k: abs(sc[k]["price"] - p2))
    if "2y" in horizons:
        h, ps = horizons["2y"], a["classification"]["price_state"]
        if ps == "RICH":
            expect, hit = "RICH: should miss the hurdle and lag the benchmark", h["total_return_pct"] < h["hurdle_pct"] and h["excess_pct"] < 0
        elif ps == "CHEAP":
            expect, hit = "CHEAP: should clear the hurdle or beat the benchmark", h["total_return_pct"] >= h["hurdle_pct"] or h["excess_pct"] > 0
        else:
            expect, hit = "FAIR: should land within +/-15pp of the benchmark", abs(h["excess_pct"]) <= 15
        out["call_check_2y"] = {"expectation": expect, "hit": bool(hit)}
    # how the durability call drifted between AS_OF and today's live profile
    try:
        with open(os.path.join(ROOT, "data", "business_profiles.json"), encoding="utf-8") as fh:
            today_p = json.load(fh)["profiles"].get(a["ticker"])
    except (OSError, ValueError, KeyError):
        today_p = None
    if today_p:
        then = a["pit_profile"]
        out["profile_drift"] = {"then": {"kind": then["kind"], "risk": then["risk"]},
                                "today": {k: today_p[k] for k in ("kind", "risk", "why", "reviewed") if k in today_p}}
    with open(os.path.join(folder, "outcome.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    cmd_index()
    print(json.dumps(out, indent=1))


# ─────────────────────────────────────────────────────────────────────────────
# Index
# ─────────────────────────────────────────────────────────────────────────────
def cmd_index():
    rows = []
    for fp in sorted(glob.glob(os.path.join(ARCHIVE, "*", "*", "analysis.json"))):
        with open(fp, encoding="utf-8") as fh:
            a = json.load(fh)
        c, m = a["classification"], a["metrics"]
        row = {"ticker": a["ticker"], "as_of": a["as_of"], "company": a.get("company"),
               "price": a["price"], "class": c["quality_class"], "kind": c["business_kind"],
               "theme": c.get("theme"), "risk": c["obsolescence_risk"], "price_state": c["price_state"],
               "legacy_tier": a["legacy_signal_short"], "ratio_b": m.get("ratio_b"),
               "epp_gap_pct": m.get("epp_gap_pct"), "adj_gap": m.get("adj_gap"),
               "cons_return_2yr": m.get("cons_return_2yr"),
               "path": os.path.relpath(os.path.dirname(fp), ROOT), "generated": a["generated"],
               "outcome": None}
        op = os.path.join(os.path.dirname(fp), "outcome.json")
        if os.path.exists(op):
            with open(op, encoding="utf-8") as fh:
                o = json.load(fh)
            row["outcome"] = {"hindsight": True,
                              **{f"tr_{k}": v["total_return_pct"] for k, v in o["horizons"].items()},
                              **{f"excess_{k}": v["excess_pct"] for k, v in o["horizons"].items()},
                              "avg_m12_m24": o["within_2y"].get("return_to_avg_price_m12_m24_pct"),
                              "scenario_landing_2y": o.get("scenario_landing_2y"),
                              "call_hit_2y": (o.get("call_check_2y") or {}).get("hit")}
        rows.append(row)
    os.makedirs(ARCHIVE, exist_ok=True)
    with open(INDEX, "w", encoding="utf-8") as fh:
        json.dump({"_doc": "Index of point-in-time retrospective analyses (retro/retro_tool.py). "
                           "'outcome' is hindsight and is filled in separately.",
                   "updated": dt.date.today().isoformat(), "count": len(rows), "entries": rows},
                  fh, ensure_ascii=False, indent=1)
    return rows


def cmd_series(ticker):
    """Markdown table of every retrospective of one ticker -> archive/retrospective/<T>/SERIES.md."""
    rows = [r for r in cmd_index() if r["ticker"] == ticker.upper()]
    if not rows:
        sys.exit(f"no retrospectives for {ticker}")
    out = [f"# {ticker.upper()} retrospective series", "",
           "Point-in-time columns use only information public on the as-of date. The last four columns are "
           "hindsight: 2-year total return incl. dividends, its excess vs SPY, the return to the average price over "
           "months 12-24 (endpoint-robust), and whether the price-state call held.", "",
           "| as of | price | latest results known | proxy | adj gap | Ratio B | model tier | class | robustness | 2y TR | vs SPY | m12-24 avg | call |",
           "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda x: x["as_of"]):
        with open(os.path.join(ROOT, r["path"], "analysis.json"), encoding="utf-8") as fh:
            a = json.load(fh)
        results = [s for s in a["sources"] if " results " in f" {s['title']} "]
        known = max(results, key=lambda s: s["published"])["title"].split(" (")[0] if results else "-"
        rob = a.get("robustness") or []
        same = sum(1 for x in rob if x.get("price_state") == r["price_state"])
        o = r["outcome"] or {}
        tr = f"{o['tr_2y']:+.1f}%" if "tr_2y" in o else "-"
        ex = f"{o['excess_2y']:+.1f}pp" if "excess_2y" in o else "-"
        hit = {True: "✓", False: "✗"}.get(o.get("call_hit_2y"), "-")
        avg = f"{o['avg_m12_m24']:+.1f}%" if o.get("avg_m12_m24") is not None else "-"
        out.append(f"| {r['as_of']} | ${r['price']:.2f} | {known} | {a['metrics']['proxy_composite']:.2f} | "
                   f"{r['adj_gap']:+.2f} | {r['ratio_b']:.2f}x | {r['legacy_tier']} | {r['class']} ({r['price_state']}) | "
                   f"{same}/{len(rob)} {r['price_state']} | {tr} | {ex} | {avg} | {hit} |")
    path = os.path.join(ARCHIVE, ticker.upper(), "SERIES.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    print("\n".join(out))
    print(f"\n-> {os.path.relpath(path, ROOT)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["run", "outcome", "lint", "index", "series"])
    ap.add_argument("folder", nargs="?", help="retrospective folder (series: the ticker)")
    ap.add_argument("--offline", action="store_true", help="skip the as-of price check")
    a = ap.parse_args()
    if a.cmd == "index":
        print(f"{len(cmd_index())} entries -> {os.path.relpath(INDEX, ROOT)}")
        return
    if a.cmd == "series":
        if not a.folder:
            ap.error("series needs a ticker")
        cmd_series(a.folder)
        return
    if not a.folder:
        ap.error("folder required")
    folder = os.path.abspath(a.folder)
    if a.cmd == "run":
        cmd_run(folder, offline=a.offline)
    elif a.cmd == "outcome":
        cmd_outcome(folder)
    else:
        g, _, src = load_model(folder)
        errs, warns = pit_checks(g, src, load_taxonomy())
        for w in warns:
            print(f"WARNING: {w}")
        for e in errs:
            print(f"ERROR: {e}")
        print("PIT lint:", "FAILED" if errs else "clean")
        sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
