#!/usr/bin/env python3
"""
Leak scan: no model may contain a token of a fact published after its AS_OF.

    python3 retro/tools/leak_scan.py SCHW [--from 2010-01-01] [--to 2013-12-31] [--show 60]

Tokens are each later source's id ("SCHW31"), title and 'supports' text, each later fact's strings of 12 characters or more, and its raw figures of four
significant digits or more (years left out), formatted as the builders print them (1,476 / 1,476.0 / 1476.00 / 1476.2).
A token that an earlier fact or the ticker's engine template already carries is dropped (a carried phrase is no leak), as is
one inside an earlier fact's text. A figure must stand alone in the model (not inside a longer number).

Positive control: the latest print in force at each AS_OF (or its latest restatement) must show at least one of its own
tokens in that model, so the scan can see a fact when one is there.

Read retro/README.md, "Adding dates", before relying on a clean result: it is one check among several.
"""
import argparse
import bisect
import glob
import os
import re
import signal
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from factwalk import RETRO, dated_facts, load_sheet, models, numbers, strings  # noqa: E402


def fmt(v):
    """The printed forms of a raw figure with 4+ significant digits; years (integers 1990-2035) left out."""
    if float(v).is_integer() and 1990 <= v <= 2035:
        return set()
    digits = re.sub(r"[^\d]", "", f"{abs(v):g}").lstrip("0")
    if len(digits) < 4:
        return set()
    out = {f"{v:,.0f}" if float(v).is_integer() else f"{v:,.1f}", f"{v:,.2f}", f"{v:g}"}
    return {x for x in out if len(re.sub(r"[^\d]", "", x)) >= 4}


def tokens(label, fields):
    t = set()
    if label.startswith("source "):
        t |= {fields["id"], fields["title"]} | ({fields["supports"]} if len(fields["supports"]) >= 12 else set())
        return t
    t |= {s for s in strings(fields) if len(s) >= 12}
    for v in numbers(fields):
        t |= fmt(v)
    return t


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker")
    ap.add_argument("--from", dest="start", default="0000")
    ap.add_argument("--to", dest="end", default="9999")
    ap.add_argument("--show", type=int, default=60)
    a = ap.parse_args()
    sheet = load_sheet(a.ticker)
    engine = "\n".join(open(p, encoding="utf-8").read()
                       for p in glob.glob(os.path.join(RETRO, "templates", f"{a.ticker.lower()}*engine*.tmpl")))
    if not engine:
        sys.exit(f"no engine template for {a.ticker} in retro/templates")
    facts = sorted(((p, lab, tokens(lab, f)) for p, lab, f in dated_facts(sheet)), key=lambda x: x[0])
    pubs = [p for p, _, _ in facts]
    ms = [(d, p) for d, p in models(a.ticker) if a.start <= d <= a.end]
    if not ms:
        sys.exit(f"no models of {a.ticker} in range")
    pairs = hits = dropped = ctl = 0
    report, no_ctl = [], []
    for as_of, path in ms:
        text = open(path, encoding="utf-8").read()
        k = bisect.bisect_right(pubs, as_of)
        carried = set().union(*[t for _, _, t in facts[:k]])
        later = set().union(*[t for _, _, t in facts[k:]]) if k < len(facts) else set()
        carried_text = "\n".join(carried)
        live = {t for t in later if t not in carried and t not in engine and t not in carried_text}
        dropped += len(later) - len(live)
        pairs += len(live)
        for t in live:
            if t in text and re.search(r"(?<![\d.,])" + re.escape(t) + r"(?![\d])", text):
                hits += 1
                report.append((as_of, t[:100]))
        # positive control: the latest print (or restatement of one) in force shows one of its tokens
        last = next(((p, lab, t) for p, lab, t in reversed(facts[:k]) if lab.startswith("prints[") and t), None)
        if last and any(re.search(r"(?<![\d.,])" + re.escape(x) + r"(?![\d])", text) for x in last[2]):
            ctl += 1
        else:
            no_ctl.append((as_of, last[1] if last else None))
    print(f"{a.ticker}: {len(ms)} models, {len(facts)} dated facts")
    print(f"positive control: the latest print in force shows a token of its own in {ctl} of {len(ms)} models")
    for x in no_ctl[:10]:
        print("  no control token:", x)
    print(f"{pairs} (model, later token) pairs, {dropped} later tokens dropped as already carried; {hits} hits")
    for r in report[:a.show]:
        print(" ", r)
    sys.exit(1 if hits else 0)


if __name__ == "__main__":
    main()
