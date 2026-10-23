#!/usr/bin/env python3
"""
Build ACN retrospective models from the dated fact sheet (retro/facts/ACN.json).

For each as-of date the builder
  1. selects only the prints and events whose 'published' date is <= AS_OF,
  2. computes every market statistic from daily prices truncated at AS_OF
     (close, 52-week range, 1-yr realized vol and beta vs the S&P 500, the 10-yr
     P/E distribution on current-fiscal-year EPS, calendar-year P/E lows),
  3. writes archive/retrospective/ACN/<AS_OF>/model.py = those facts + the frozen
     engine (retro/templates/acn_engine.py.tmpl), which derives every scenario input
     by rule. Nothing in a model is chosen by hand, so later knowledge has no way in.

Weekly dates (--weekly START END): one per week, the week's last trading day, except
in a week with an earnings release, where it is the first trading day after it.

Usage
  python3 retro/build_acn.py --weekly 2023-01-01 2023-06-30
  python3 retro/build_acn.py 2023-03-17 2023-06-23
Then: python3 retro/retro_tool.py run archive/retrospective/ACN/<AS_OF>  (validation + classification)
"""
import argparse
import datetime as dt
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import retro_tool  # noqa: E402

FACTS = os.path.join(HERE, "facts", "ACN.json")
ENGINE = os.path.join(HERE, "templates", "acn_engine.py.tmpl")
OUT = os.path.join(ROOT, "archive", "retrospective", "ACN")
WHY = ("Accenture: #1-scale IT-services and consulting franchise that took share through the cloud "
       "cycle; discretionary consulting demand is cyclical, the franchise is not")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]


def load_series(symbol):
    """{date: (open, high, low, close)} from the retro_tool Yahoo cache (full history)."""
    retro_tool.fetch_prices(symbol)
    with open(os.path.join(retro_tool.CACHE, f"{symbol.replace('^', '_')}.json"), encoding="utf-8") as fh:
        d = json.load(fh)["chart"]["result"][0]
    off, q = d["meta"]["gmtoffset"], d["indicators"]["quote"][0]
    out = {}
    for i, t in enumerate(d["timestamp"]):
        if q["close"][i] is None:
            continue
        day = dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
        out[day] = (q["high"][i], q["low"][i], q["close"][i])
    return out


def minus_years(date, n):
    return f"{int(date[:4]) - n}{date[4:]}"


def weekly_dates(start, end, trading_days, prints):
    """Last trading day of each ISO week; in an earnings week, the first trading day after the release."""
    weeks = {}
    for d in trading_days:
        if start <= d <= end:
            weeks.setdefault(dt.date.fromisoformat(d).isocalendar()[:2], []).append(d)
    out = []
    for _, days in sorted(weeks.items()):
        after = [d for p in prints for d in days if days[0] <= p["published"] <= days[-1] and d > p["published"]]
        out.append(min(after) if after else days[-1])
    return out


def ordinal(n):
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def build(as_of, facts, acn, spx, engine):
    if as_of not in acn:
        sys.exit(f"{as_of} is not a trading day")
    prints = [p for p in facts["prints"] if p["published"] <= as_of]
    events = [e for e in facts["events"] if e["published"] <= as_of]
    h = facts["history"]
    if not prints or h["published"] > as_of:
        sys.exit(f"{as_of}: no print in the fact sheet is public yet")
    latest = prints[-1]
    prev = (prints[-2]["consulting_lc"], prints[-2]["quarter"]) if len(prints) > 1 else (h["q4fy22_consulting_lc"], "Q4 FY22")
    eps_now = round(sum(latest["fy_eps_guide"]) / 2, 3)

    # ── market statistics, prices truncated at AS_OF ──
    days = sorted(d for d in acn if d <= as_of)
    close = acn[as_of][2]
    yr = [d for d in days if d > minus_years(as_of, 1)]
    low52, high52 = min(acn[d][1] for d in yr), max(acn[d][0] for d in yr)
    common = [d for d in yr if d in spx]
    ra = [math.log(acn[common[i]][2] / acn[common[i - 1]][2]) for i in range(1, len(common))]
    rm = [math.log(spx[common[i]][2] / spx[common[i - 1]][2]) for i in range(1, len(common))]
    ma, mm = sum(ra) / len(ra), sum(rm) / len(rm)
    vol = (sum((x - ma) ** 2 for x in ra) / len(ra)) ** 0.5 * 252 ** 0.5
    beta = (sum((x - ma) * (y - mm) for x, y in zip(ra, rm)) / len(ra)) / (sum((y - mm) ** 2 for y in rm) / len(rm))
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}   # reported history only: the rules use this
    eps = {**eps_hist, max(eps_hist) + 1: eps_now}                     # + current-FY guide, for the P/E series
    fy = lambda d: int(d[:4]) + (1 if int(d[5:7]) >= 9 else 0)
    window = [d for d in days if d > minus_years(as_of, 10)]
    pe = {d: acn[d][2] / eps[fy(d)] for d in window}
    srt = sorted(pe.values())
    q = lambda p: round(srt[int(p * (len(srt) - 1))], 1)
    pctl = {"p5": q(.05), "p10": q(.10), "p25": q(.25), "median": q(.5), "p75": q(.75), "p90": q(.9), "max": round(srt[-1], 1)}
    pe_now_pctl = round(sum(v <= close / eps_now for v in srt) / len(srt) * 100)
    yearly = []
    for y in sorted({d[:4] for d in window}):
        dd = min((d for d in window if d.startswith(y)), key=lambda d: pe[d])
        yearly.append((y, round(pe[dd], 1), dd))
    ref = min(yr, key=lambda d: acn[d][2])

    # ── era-dependent text, from facts only ──
    stage = ("losers" if any(e["kind"] == "genai_loser_repricing" for e in events) else
             "sellside" if any(e["kind"] == "genai_sellside" for e in events) else "chatgpt_only")
    ai_inv = any(e["kind"] == "company_ai_investment" for e in events)
    val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
    pe_txt = f"{close / eps_now:.1f}x FY23E — {val_word}, not an AI discount."
    reason = {
        "chatgpt_only": f"Live since 2022-11-30 (ChatGPT), but there is no sell-side or price read on IT services yet and the stock trades at {pe_txt}",
        "sellside": f"Live since 2022-11-30, but the sell-side read for ACN was share gain (J.P.Morgan, 2023-02-10) and the stock trades at {pe_txt}",
        "losers": ("Live since 2022-11-30 and already repricing obvious losers (Chegg, 2023-05-02), but the sell-side read for ACN "
                   f"was share gain (J.P.Morgan, 2023-02-10) and the stock trades at {pe_txt}"),
    }[stage] + " Re-file under AI_EXPOSED only when the multiple starts discounting deflation or GenAI shows up as shrinking billable hours."
    genai_opp = ("GenAI as the next services cycle: $3B Data & AI investment, practitioners 40k -> 80k" if ai_inv else
                 "GenAI as a services opportunity: J.P.Morgan expects global consultancies to gain share first" if stage != "chatgpt_only" else
                 "GenAI as a services opportunity: ChatGPT opens an advisory/implementation market; no client data yet")
    genai_risk = ("GenAI as a deflation driver for legacy delivery hours (J.P.Morgan) — not yet in the numbers" if stage != "chatgpt_only" else
                  "GenAI as a deflation risk for coding/testing hours — untested, not in the numbers")
    genai_summary = ("GenAI is live but there is no read yet on what it does to IT services" if stage == "chatgpt_only" else
                     "GenAI is a live theme, read by the sell side as share gain for consultancies, not a threat")
    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{latest['next_q']} FY23 print)"

    sources = [dict(id="S1", **facts["sources"]["S1"]), dict(id="S2", **facts["sources"]["S2"])]
    sources += [dict(id=p["source"], **facts["sources"][p["source"]]) for p in prints]
    sources += [dict(id=e["id"], **facts["sources"][e["id"]]) for e in events]
    sources.append({"id": "S12", "published": as_of, "title": "Yahoo Finance daily prices, ACN and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/ACN/history",
                    "supports": f"close ${close:.2f}, 52-week range, realized vol, beta, the 10-yr P/E distribution"})
    for s in sources:
        assert s["published"] <= as_of, (as_of, s["id"])

    latest_keys = ("quarter", "release", "revenue_b", "revenue_lc", "consulting_lc", "managed_lc", "bookings_b", "bookings_lc",
                   "consulting_bookings_b", "consulting_revenue_b", "margin_label", "margin", "margin_bp", "eps_label",
                   "fy_eps_guide", "fy_eps_guide_note", "fy_rev_guide_lc", "fy_rev_guide_note", "fy_fx",
                   "next_q", "next_q_guide_b", "next_q_guide_lc")
    rev = {int(k): v for k, v in h["revenue_usd_b"].items()}
    shares = {int(k): v for k, v in h["diluted_shares_m"].items()}
    opt = f"; {latest['optimization']} defends margin" if latest["optimization"] else ""
    R = repr
    head = f'''#!/usr/bin/env python3
"""
ACN Signal Model  ·  RETROSPECTIVE as of {as_of}  {tag}  (methodology v2, retro method r2)
──────────────────────────────────────────────────────────────────────
Accenture plc (NYSE: ACN)  ·  IT Services & Consulting — Strategy & Consulting, Technology, Operations
Generated by retro/build_acn.py from retro/facts/ACN.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "ACN"
COMPANY     = "Accenture plc"
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md)")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as it should have been judged ON AS_OF — not today's AI_EXPOSED profile.
PIT_PROFILE = {{
    "kind": "DURABLE",
    "risk": 2,
    "why": {R(WHY)},
    "theme_watch": [{{"theme": "GENAI", "status": {R("live, no read on IT services yet" if stage == "chatgpt_only" else "live, priced as a tailwind")},
                     "reason": {R(reason)}}}],
    "evidence": {R([e["id"] for e in events])},
}}

# ── FACTS: market (prices truncated at AS_OF) ─────────────────────────────────
CURRENT_PRICE   = {close:.2f}   # USD, NYSE close {as_of}
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
PE_PCTL         = {R(pctl)}   # current-FY P/E, the 10 years to AS_OF
PE_NOW_PCTL     = {pe_now_pctl}    # share of those daily P/Es at or below today's
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {acn[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history (S1, S2) ───────────────────────────────────────────
EPS_NORM      = {R(eps_hist)}   # reported, {h["normalization"]}
REVENUE_HIST  = {R(rev)}   # USD bn
SHARES_HIST   = {R(shares)}   # diluted, millions
FY22_MARGIN   = {h["fy22_op_margin"]}
CONS_DIVIDEND = {h["dividend_quarterly"] * 4:.2f}   # ${h["dividend_quarterly"]:.2f}/quarter (S1)
VOL_DIVIDEND  = CONS_DIVIDEND

# ── FACTS: latest print and guide ({latest["source"]}, published {latest["published"]}) ──
LATEST          = {R({k: latest[k] for k in latest_keys})}
PREV_CONSULTING = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # FY2023E {latest["eps_label"]}, guide midpoint
FY_MARGIN_GUIDE_MID = {sum(latest["fy_margin_guide"]) / 2}
FY23E_REVENUE_B = {rev[2022] * (1 + (sum(latest["fy_rev_guide_lc"]) / 2 + latest["fy_fx"]) / 100):.2f}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in latest["groups"]])}
GROUPS_BASIS    = {R(latest["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Share-gainer at scale: FY22 revenue +{h['fy22_revenue_lc_growth']}% LC, record ${h['fy22_bookings_b']}B bookings; {latest['quarter'].split()[0]} revenue {latest['revenue_lc']:+d}% LC")}
BALANCE_TEXT    = {R(f"Cash ${latest['cash_b']}B, FCF guide ${latest['fcf_guide_b'][0]}-{latest['fcf_guide_b'][1]}B, >=$7.1B returned{opt}")}
GENAI_OPP_TEXT  = {R(genai_opp)}
GENAI_RISK_TEXT = {R(genai_risk)}
GENAI_SUMMARY   = {R(genai_summary)}
'''
    os.makedirs(os.path.join(OUT, as_of), exist_ok=True)
    with open(os.path.join(OUT, as_of, "model.py"), "w", encoding="utf-8") as fh:
        fh.write(head + engine)
    return tag, latest["quarter"], stage


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dates", nargs="*")
    ap.add_argument("--weekly", nargs=2, metavar=("START", "END"))
    a = ap.parse_args()
    with open(FACTS, encoding="utf-8") as fh:
        facts = json.load(fh)
    with open(ENGINE, encoding="utf-8") as fh:
        engine = fh.read()
    acn, spx = load_series("ACN"), load_series("^GSPC")
    dates = list(a.dates)
    if a.weekly:
        dates += weekly_dates(a.weekly[0], a.weekly[1], sorted(acn), facts["prints"])
    for d in sorted(set(dates)):
        tag, q, stage = build(d, facts, acn, spx, engine)
        print(f"{d}  {tag:<32}  latest print {q:<8}  GenAI evidence: {stage}")


if __name__ == "__main__":
    main()
