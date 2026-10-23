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
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
          "October", "November", "December"]


def load_series(symbol):
    """{date: (high, low, close)} as traded on each day, from the retro_tool Yahoo cache (full history). Yahoo prices
    are split-adjusted; undoing the later splits restores the price printed that day (ACN has none, UNP two after 2008)."""
    d = retro_tool.chart(symbol)
    off, q = d["meta"]["gmtoffset"], d["indicators"]["quote"][0]
    out = {}
    for i, t in enumerate(d["timestamp"]):
        if q["close"][i] is None:
            continue
        day = dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
        f = retro_tool.split_factor(d, day)
        out[day] = (q["high"][i] * f, q["low"][i] * f, q["close"][i] * f)
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
    vintages = [v for v in facts["history_vintages"] if v["published"] <= as_of]
    if not vintages:
        sys.exit(f"{as_of}: no history vintage in the fact sheet is public yet")
    h = vintages[-1]                                   # latest annual history public on AS_OF
    # prints published by AS_OF that guide a fiscal year after the history (a Q4 print guides the next year,
    # so it stays in scope after the 10-K that follows it); events published since the vintage
    first_fy = max(int(k) for k in h["eps_normalized"]) + 1
    guide_fy = lambda p: 2000 + int(p["quarter"][-2:]) + (1 if p["quarter"].startswith("Q4") else 0)
    prints = [p for p in facts["prints"] if p["published"] <= as_of and guide_fy(p) >= first_fy]
    # a 10-K's wording (an event with a "doc") is replaced by the next 10-K; market and company-action evidence
    # (an event without one) stays in scope once public
    events = [e for e in facts["events"] if e["published"] <= as_of and (h["published"] <= e["published"] or "doc" not in e)]
    if not prints:
        sys.exit(f"{as_of}: no quarterly print guiding FY{first_fy} is public yet")
    # a Q4 print's full-year actuals extend the annual history from its release until the next 10-K vintage
    h = {**h, "extended": ""}
    for p in prints:
        a = p.get("fy_actual")
        if a and str(a["fy"]) not in h["eps_normalized"]:          # the 10-K vintage, once out, wins
            y = str(a["fy"])
            h.update(fy_label=a["fy_label"], why=a.get("why", h["why"]),
                     eps_normalized={**h["eps_normalized"], y: a["eps_normalized"]},
                     revenue_usd_b={**h["revenue_usd_b"], y: a["revenue_usd_b"]},
                     diluted_shares_m={**h["diluted_shares_m"], y: a["diluted_shares_m"]},
                     normalization=f'{h["normalization"]}; {a["normalization_note"]}',
                     prev_fy_op_margin=a["op_margin"], prev_fy_revenue_lc_growth=a["revenue_lc_growth"],
                     prev_fy_bookings_b=a["bookings_b"], prev_fy_bookings_record=a.get("bookings_record", True), extended=f'{h["extended"]}, FY{y[2:]} from {p["source"]} ({p["published"]})')
    carried = lambda k: next((p[k] for p in reversed(prints) if k in p), h[k])   # latest print that states it, else the vintage
    latest = prints[-1]
    prev = (prints[-2]["consulting_lc"], prints[-2]["quarter"]) if len(prints) > 1 else (h["prev_q_consulting_lc"], h["prev_q_label"])
    eps_now = round(sum(latest["fy_eps_guide"]) / 2, 3)
    eps_hist = {int(k): v for k, v in h["eps_normalized"].items()}   # reported history only: the rules use this
    cur_fy = max(eps_hist) + 1
    fy_e, fy_e_s, fy_h, fy_now = f"FY{cur_fy}E", f"FY{cur_fy % 100:02d}E", f"FY{cur_fy + 2}E", f"FY{cur_fy % 100:02d}"

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
    eps = {**eps_hist, cur_fy: eps_now}                                # + current-FY guide, for the P/E series
    # fiscal year of a day (ACN's ends Aug 31); a day past the last guided year, before the Q4 print, keeps that year's EPS
    fy = lambda d: min(int(d[:4]) + (1 if int(d[5:7]) >= 9 else 0), cur_fy)
    window = [d for d in days if d > minus_years(as_of, 10) and (not h["pe_window_start"] or d >= h["pe_window_start"])]
    assert all(fy(d) in eps for d in window), (as_of, "P/E window needs EPS for every fiscal year")
    years = (dt.date.fromisoformat(as_of) - dt.date.fromisoformat(window[0])).days / 365.25
    window_label = "10-yr" if years > 9.9 else f"{years:.1f}-yr"
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

    # ── forward guide and margin step (documented fallbacks when the company did not guide them) ──
    if latest.get("next_q_guide_lc"):
        fwd, fwd_label, fwd_period = latest["next_q_guide_lc"], f"{latest['next_q']} guide", latest["next_q"]
    else:                                    # no next-quarter LC guide: use the full-year LC guide
        fwd, fwd_label, fwd_period = latest["fy_rev_guide_lc"], f"{fy_now} guide", fy_now
    margin_guided = bool(latest.get("fy_margin_guide"))
    fy_margin_base = sum(latest["fy_margin_guide"]) / 2 if margin_guided else h["prev_fy_op_margin"]
    # a margin guide measured against a prior year the company restated for an accounting change is stepped from
    # that restated base, never from the reported one (ACN FY19: +10-30bp from a revised FY18 14.4%, 14.8% reported)
    restated = latest.get("fy_margin_guide_base") if margin_guided else None
    prev_margin = (f'{restated}   # {h["fy_label"]} as restated for the {fy_now} margin guide ({h["prev_fy_op_margin"]} as reported)'
                   if restated is not None else h["prev_fy_op_margin"])
    fx = latest.get("fy_fx")

    # ── era-dependent text, from facts only: which disruption theme has dated evidence on AS_OF ──
    val_word = "a premium" if pe_now_pctl >= 70 else "a discount to its own history" if pe_now_pctl <= 30 else "near its own median"
    themes = {e["theme"] for e in events}
    kind, pit_risk, why, assigned = "DURABLE", 2, h["why"], None
    k10 = [e for e in events if e["kind"] == "genai_company_acknowledged"]     # the latest 10-K's own words on AI substitution
    if k10:
        # from the first 10-K after GenAI went live (ACN FY23), the company's own words carry the theme; the re-file test is
        # the one the earlier GenAI text states: the multiple at a discount to its own history (the 30th-percentile line of
        # val_word) or managed-services growth below 3% LC (the managed-services signal's lowest band)
        e10 = k10[-1]
        g = [e for e in events if e["theme"] == "GENAI"]
        ai_inv = any(e["kind"] == "company_ai_investment" for e in g)
        note = next(((p["genai_note"], p["quarter"]) for p in reversed(prints) if "genai_note" in p), None)
        discounted, ms_weak = pe_now_pctl <= 30, latest["managed_lc"] < 3
        stage = "refiled" if discounted or ms_weak else "company"
        pe_txt = f"{close / eps_now:.1f}x {fy_e_s} — {val_word}"
        own = f"Accenture's own {e10['doc']} says '{e10['risk_quote']}'"
        books = f" It reported {note[0]} ({note[1]})." if note else ""
        rule = ("Re-file under DISRUPTION_EXPOSED (GENAI) when the multiple falls to a discount to its own history (30th "
                "percentile or lower) or managed-services growth drops below 3% LC.")
        if stage == "refiled":
            why_bits = ([f"the stock trades at {pe_txt} ({pe_now_pctl}th percentile of its {window_label} range)"] if discounted else []) + \
                       ([f"managed-services growth is {latest['managed_lc']:+d}% LC in {latest['quarter']}"] if ms_weak else [])
            kind, pit_risk, assigned = "DISRUPTION_EXPOSED", 3, "GENAI"
            why = (f"{h['why']}; re-filed under GenAI: {' and '.join(why_bits)}, while its own {e10['doc_short']} says "
                   f"{e10['risk_short']}. Back to DURABLE when the multiple is above the 30th percentile and managed services "
                   "grow 3% LC or more")
            watch = []
            theme_summary = f"GenAI is a live disruption theme the stock is priced for: {' and '.join(why_bits)}"
        else:
            watch = [{"theme": "GENAI", "status": "live, company-acknowledged; not discounted",
                      "reason": f"Live since 2022-11-30. {own}{books} The stock trades at {pe_txt}. {rule}"}]
            theme_summary = f"GenAI is live and company-acknowledged ({e10['doc_short']}), but the multiple does not discount it"
        opp = (f"GenAI as the next services cycle: {note[0]} ({note[1]})" if note else
               "GenAI as the next services cycle: $3B Data & AI investment, practitioners 40k -> 80k" if ai_inv else
               "GenAI as a services opportunity: no bookings figure in the prints in scope")
        factors = [(opp, 0.2, 0.10), (f"AI substitution of services ({e10['doc_short']}): {e10['risk_short']}", -0.2, 0.10)]
        sig_name = "GenAI: net effect on services"
        trigger = "AI substitution cuts demand faster than GenAI work replaces it"
        key_tail = ("A JOINT event: a demand recession alone hits consulting, AI substitution\n"
                    f"  ({e10['doc_short']}) alone hits run/maintain work — the bear needs both.")
        cat3 = (f"(3) GenAI bookings — {note[0]} ({note[1]}); does AI work outgrow what it replaces?" if note else
                "(3) GenAI bookings — no figure in the prints in scope; does AI work outgrow what it replaces?")
        cat4 = "(4) Managed-services growth — where AI substitution would show first (re-file below 3% LC)"
    elif "GENAI" in themes:
        g = [e for e in events if e["theme"] == "GENAI"]
        stage = ("losers" if any(e["kind"] == "genai_loser_repricing" for e in g) else
                 "sellside" if any(e["kind"] == "genai_sellside" for e in g) else "chatgpt_only")
        ai_inv = any(e["kind"] == "company_ai_investment" for e in g)
        pe_txt = f"{close / eps_now:.1f}x {fy_e_s} — {val_word}, not an AI discount."
        reason = {
            "chatgpt_only": f"Live since 2022-11-30 (ChatGPT), but there is no sell-side or price read on IT services yet and the stock trades at {pe_txt}",
            "sellside": f"Live since 2022-11-30, but the sell-side read for ACN was share gain (J.P.Morgan, 2023-02-10) and the stock trades at {pe_txt}",
            "losers": ("Live since 2022-11-30 and already repricing obvious losers (Chegg, 2023-05-02), but the sell-side read for ACN "
                       f"was share gain (J.P.Morgan, 2023-02-10) and the stock trades at {pe_txt}"),
        }[stage] + (" Re-file under DISRUPTION_EXPOSED (GENAI) only if dated evidence shows the market pricing AI substitution of IT-services work."
                    if stage == "chatgpt_only" else
                    " Re-file under DISRUPTION_EXPOSED (GENAI) only when the multiple starts discounting the legacy-services deflation J.P.Morgan "
                    "describes, or it shows up in managed-services growth.")
        watch = [{"theme": "GENAI", "status": "live, no read on IT services yet" if stage == "chatgpt_only" else "live, priced as a tailwind",
                  "reason": reason}]
        opp = ("GenAI as the next services cycle: $3B Data & AI investment, practitioners 40k -> 80k" if ai_inv else
               "GenAI as a services opportunity: J.P.Morgan expects global consultancies to gain share first" if stage != "chatgpt_only" else
               "GenAI as a services opportunity: ChatGPT opens an advisory/implementation market; no client data yet")
        risk = ("GenAI as a deflation driver for legacy delivery hours (J.P.Morgan) — not yet in the numbers" if stage != "chatgpt_only" else
                "GenAI as a risk to delivery hours — no evidence yet, not in the numbers")
        factors = [(opp, 0.2, 0.10), (risk, -0.2, 0.10)]
        sig_name = "GenAI: net effect on services"
        # every GenAI sentence follows the evidence public on AS_OF: before the J.P.Morgan note (2023-02-10)
        # nothing dated described a deflation mechanism for IT services, so the text does not either
        if stage == "chatgpt_only":
            trigger = "No dated evidence yet on GenAI's net effect on services demand"
            key_tail = ("A demand recession hits discretionary consulting first; the bear needs it\n"
                        "  to spread to run/maintain work as well.")
            cat3 = "(3) Consulting vs managed-services bookings mix — where a slowdown shows first"
            cat4 = "(4) Managed-services renewal pricing"
        else:
            trigger = "Legacy-services pricing deflates faster than GenAI advisory grows"
            key_tail = ("A JOINT event: a demand recession alone hits consulting, legacy-services\n"
                        "  deflation (J.P.Morgan's mechanism) alone hits run/maintain work — the bear needs both.")
            cat3 = "(3) First disclosed GenAI bookings — does the share gain J.P.Morgan expects show up?"
            cat4 = "(4) Managed-services renewal pricing — where legacy-services deflation would show first"
        theme_summary = ("GenAI is live but there is no read yet on what it does to IT services" if stage == "chatgpt_only" else
                         "GenAI is a live theme, read by the sell side as share gain for consultancies, not a threat")
    elif "OFFSHORE" in themes:
        stage = "offshore"
        e = [e for e in events if e["theme"] == "OFFSHORE"][-1]      # the latest 10-K's wording
        quote = e.get("competitors_quote", "particularly Indian providers ... often at highly competitive prices")
        rivals = e.get("competitors_short", "Offshore Indian providers 'often at highly competitive prices'")
        # a 10-K that gives no delivery headcount says so in gdn_clause / gdn_factor (ACN from FY17)
        gdn = e.get("gdn_clause") or f"Global Delivery Network {e.get('gdn_verb', 'grew to')} {e.get('gdn_people')} people"
        gdn_factor = e.get("gdn_factor") or f"Global Delivery Network: {e.get('gdn_people')} people ({e.get('gdn_added')})"
        watch = [{"theme": "OFFSHORE", "status": "live, company-acknowledged; no market read",
                  "reason": (f"Live: Accenture's own {e['doc']} names off-shore providers, "
                             f"'{quote}', "
                             f"among its competitors and {e['warning']}, while its own {gdn}. The stock trades at "
                             f"{close / eps_now:.1f}x {fy_e_s} — {val_word}. Re-file as DISRUPTION_EXPOSED (OFFSHORE) only if dated "
                             "evidence shows the market pricing offshore substitution for ACN specifically.")}]
        factors = [(f"{gdn_factor} — Accenture runs the offshore model itself", 0.2, 0.10),
                   (f"{rivals}; {e['warning_short']}", -0.2, 0.10)]
        sig_name = "Offshore: net effect on services"
        trigger = "Offshore pricing pressure accelerates faster than global-delivery savings"
        key_tail = ("A JOINT event: a demand recession alone hits consulting, accelerating offshore\n"
                    f"  pricing pressure ({e['doc_short']}) alone hits outsourcing margins — the bear needs both.")
        bt = latest.get("fy_bookings_target_b")
        cat3 = f"(3) Bookings run-rate vs the ${bt[0]}-{bt[1]}B {fy_now} target" if bt else "(3) Bookings run-rate"
        cat4 = "(4) Outsourcing pricing — where offshore pressure would show first"
        theme_summary = "offshore competition is live and company-acknowledged; no dated evidence ties the multiple to it"
    else:
        stage, watch, factors = "none", [], []
        sig_name, trigger = "Disruption theme: none live", "No live disruption theme"
        key_tail = ("A demand recession hits discretionary consulting first; the bear needs it\n"
                    "  to spread to run/maintain work as well.")
        cat3, cat4 = "(3) Consulting vs outsourcing bookings mix — where a slowdown shows first", "(4) Outsourcing renewal pricing"
        theme_summary = "no disruption theme has dated evidence"
    # another live theme with company evidence joins the watch list; the theme signal and factors stay with the first
    for e in [e for e in events if e["theme"] == "CLOUD"][-1:]:
        watch.append({"theme": "CLOUD", "status": "live, company-acknowledged; no market read",
                      "reason": (f"Live: Accenture's own {e['doc']} says '{e['risk_quote']}' At the same time {e['offering']}. "
                                 f"The stock trades at {close / eps_now:.1f}x {fy_e_s} — {val_word}. Re-file as DISRUPTION_EXPOSED (CLOUD) "
                                 "only if dated evidence shows the market pricing cloud substitution of ACN's outsourcing specifically.")})
    after_print = [p for p in prints if p["published"] < as_of and not any(p["published"] < d < as_of for d in days)]
    tag = f"(day after the {after_print[-1]['quarter']} print)" if after_print else f"(pre-{latest['next_q']} {fy_now} print)"
    same_day = [p for p in prints if p["published"] == as_of]     # only a release made before the open can meet AS_OF's close
    if same_day:
        assert "before the open" in same_day[-1].get("release_time", ""), (as_of, same_day[-1]["quarter"], "released on AS_OF, not before the open")
        tag = f"(day of the {same_day[-1]['quarter']} print, released before the open)"

    # a change of company name filed after the vintage (ACN: Accenture plc replaced Accenture Ltd on 2009-09-01)
    renames = [n for n in facts.get("company_names", []) if h["published"] < n["published"] <= as_of]
    company = renames[-1]["name"] if renames else h["company"]
    ids = (list(h["sources"]) + [x for p in prints for x in [p["source"]] + p.get("extra_sources", [])] + [e["id"] for e in events]
           + [n["source"] for n in renames])
    sources = [dict(id=i, **facts["sources"][i]) for i in dict.fromkeys(ids)]
    sources.append({"id": "S12", "published": as_of, "title": "Yahoo Finance daily prices, ACN and S&P 500, truncated at AS_OF",
                    "url": "https://finance.yahoo.com/quote/ACN/history",
                    "supports": f"close ${close:.2f}, 52-week range, realized vol, beta, the {window_label} P/E distribution"})
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
{company} (NYSE: ACN)  ·  {h["business_line"]}
Generated by retro/build_acn.py from retro/facts/ACN.json: the constants below are the facts public on
AS_OF; the engine underneath derives every scenario input from them by frozen rules. Do not edit by hand.

Format: segment bridge → signal dashboard → bear anatomy → updated EPP →
        conservative growth → volatility context → probability → robustness
"""

# ── RETROSPECTIVE FRAME ───────────────────────────────────────────────────────
TICKER      = "ACN"
COMPANY     = {R(company)}
AS_OF       = "{as_of}"
PRICE_DATE  = "{as_of}"
METHODOLOGY = ("house v2 (EPP-distance adjustment), 6-section format; retro method r2: scenario inputs "
               "derived from dated facts by frozen rules (retro/README.md)")
SOURCES = {json.dumps(sources, ensure_ascii=False, indent=4)}

# Durability as judged on AS_OF from the dated facts and events above.
PIT_PROFILE = {{
    "kind": "{kind}",{chr(10) + '    "theme": "' + assigned + '",' if assigned else ""}
    "risk": {pit_risk},
    "why": {R(why)},
    "theme_watch": {R(watch)},
    "evidence": {R(list(dict.fromkeys(e["id"] for e in events)))},
}}

# ── FACTS: market (prices truncated at AS_OF) ─────────────────────────────────
CURRENT_PRICE   = {close:.2f}   # USD, NYSE close {as_of}
REQUIRED_RETURN = 0.15
HORIZON_YEARS   = 2
PE_PCTL         = {R(pctl)}   # current-FY P/E over the window below
PE_NOW_PCTL     = {pe_now_pctl}    # share of those daily P/Es at or below the AS_OF one
WINDOW_LABEL    = {R(window_label)}   # P/E window: {window[0]} .. AS_OF
YEARLY_MIN_PE   = {R(yearly)}   # (calendar year, lowest P/E, date)
VOL_ANNUAL_PCT  = {vol:.3f}   # 1-yr realized, daily log returns
VOL_BETA        = {beta:.2f}    # 1-yr beta vs S&P 500
VOL_52W_LOW     = {low52:.2f}
VOL_52W_HIGH    = {high52:.2f}
REF_LOW         = {acn[ref][2]:.2f}   # lowest close of the last 52 weeks, {ref}
REF_LOW_LABEL   = {R(MONTHS[int(ref[5:7]) - 1])}

# ── FACTS: company history ({", ".join(h["sources"])}, vintage {h["published"]}{h["extended"]}) ──
EPS_NORM      = {R(eps_hist)}   # reported, {h["normalization"]}
REVENUE_HIST  = {R(rev)}   # USD bn
SHARES_HIST   = {R(shares)}   # diluted, millions
FY_E, FY_E_S, FY_H, FY_PREV = {R(fy_e)}, {R(fy_e_s)}, {R(fy_h)}, {R(h["fy_label"])}
PREV_FY_MARGIN = {prev_margin}
TAX_RATE      = {latest.get("tax_rate", h["tax_rate"])}   # latest tax-rate guide midpoint
CONS_DIVIDEND = {carried("dividend_annual"):.2f}   # {carried("dividend_note")}
VOL_DIVIDEND  = CONS_DIVIDEND
SERVICE_LINE  = {R(carried("service_line"))}
MARGIN_SIGNAL_NAME = {R(h["margin_signal_name"])}

# ── FACTS: latest print and guide ({latest["source"]}, published {latest["published"]}) ──
LATEST          = {R({k: latest.get(k) for k in latest_keys})}
PREV_CONSULTING = {R(prev)}
EPP_TODAY_EPS   = {eps_now}   # {fy_e} {latest["eps_label"]}, guide midpoint
FWD_GUIDE_LC    = {R(tuple(fwd))}   # {"next-quarter" if fwd_period == latest["next_q"] else "full-year (no next-quarter LC guide given)"} revenue guide, LC
FWD_GUIDE_LABEL, FWD_PERIOD = {R(fwd_label)}, {R(fwd_period)}
MARGIN_GUIDED   = {margin_guided}   # False: no margin guide, so no guided step; the signal uses the latest quarter's change
FY_MARGIN_BASE  = {fy_margin_base}
FY_REVENUE_B    = {rev[max(rev)] * (1 + (sum(latest["fy_rev_guide_lc"]) / 2 + (fx or 0)) / 100):.2f}
FX_TEXT         = {R(f"{fx:+.1f}% FX" if fx is not None else "FX not guided")}
SHARES_DIL_B    = {latest["diluted_shares_m"] / 1000:.4f}
GROUPS          = {R([tuple(g) for g in latest["groups"]])}
GROUPS_BASIS    = {R(latest["groups_basis"])}
NEXT_PRINT      = {R(latest["next_print"])}
SHARE_GAIN_TEXT = {R(f"Share-gainer at scale: {h['fy_label']} revenue {h['prev_fy_revenue_lc_growth']:+}% LC, {'record ' if h.get('prev_fy_bookings_record', True) else ''}${h['prev_fy_bookings_b']}B bookings; {latest['quarter'].split()[0]} revenue {latest['revenue_lc']:+d}% LC")}
BALANCE_TEXT    = {R(f"Cash ${latest['cash_b']}B, FCF guide ${latest['fcf_guide_b'][0]}-{latest['fcf_guide_b'][1]}B, {latest.get('cash_return_text', h['cash_return_text'])}{opt}")}
THEME_FACTORS   = {R(factors)}
THEME_SIGNAL_NAME    = {R(sig_name)}
THEME_SIGNAL_TRIGGER = {R(trigger)}
THEME_SUMMARY        = {R(theme_summary)}
KEY_TRIGGER_TAIL     = {R(key_tail)}
CATALYST_3      = {R(cat3)}
CATALYST_4      = {R(cat4)}
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
        print(f"{d}  {tag:<32}  latest print {q:<8}  theme evidence: {stage}")


if __name__ == "__main__":
    main()
