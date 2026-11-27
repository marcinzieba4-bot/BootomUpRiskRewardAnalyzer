#!/usr/bin/env python3
"""
Self-text scan (the LLY scan): every capitalized word, dollar figure and year in a fact's own words must appear in one of the
company's filings published by the fact's own date.

    python3 -I retro/tools/selftext.py SCHW --filings <dir> [--from 2010-01-01] [--to 2013-12-31] [--allow WORD ...]

<dir> holds the downloaded filings, one folder per accession number (0001193125-10-008163/, at any depth), as
retro/tools/edgar.py writes them; every *.txt in a folder (the converted .rows.txt and the plain-text documents) is that
filing's text. A filing is dated by the fact sheet's source for its accession where there is one (the acceptance-time rule),
else by EDGAR's filing date from <dir>/allrows.json (edgar.py index), else it is left out and counted.

The author's own words are each dated fact's string fields less quoted keys ('rows', 'quote', ...) and less text in single
quotes, which verbatim.py checks. Method words (tickers of retro/facts, GAAP, FY, Q1, ...) and any --allow word pass. Each miss
is printed: a word that no filing of the date carries is either the author's (a method term: --allow it) or a leak.
Run it with -I: it reads downloaded files.
"""
import argparse
import glob
import json
import os
import re
import signal
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from factwalk import RETRO, dated_facts, load_sheet, own_texts  # noqa: E402

ACC = re.compile(r"^\d{10}-\d\d-\d{6}$")
METHOD_WORDS = {"FY", "GAAP", "EPS", "P", "E", "K", "Q1", "Q2", "Q3", "Q4", "ET", "M", "B", "U.S.", "Yahoo", "S&P", "NYSE",
                "Nasdaq", "NASDAQ", "IT", "DURABLE", "CYCLICAL", "OFFSHORE", "CLOUD", "GENAI", "CRYPTO", "EV", "GLP1", "ECOMMERCE",
                "STREAMING", "ENERGY_TRANSITION", "BEAR", "BASE", "BULL", "XBULL", "CHEAP", "FAIR", "RICH", "EDGAR", "SEC", "XBRL",
                "Item", "Exhibit", "Form"}


def corpus(filings, sheet):
    pub = {}
    for s in sheet.get("sources", {}).values():
        m = re.search(r"/(\d{18})/", s.get("url", ""))
        if m:
            a = m.group(1)
            pub[f"{a[:10]}-{a[10:12]}-{a[12:]}"] = s["published"]
    rows = {}
    if os.path.exists(os.path.join(filings, "allrows.json")):
        rows = {r[3]: r[0] for r in json.load(open(os.path.join(filings, "allrows.json"), encoding="utf-8"))}
    out, undated = [], 0
    for d in sorted(glob.glob(os.path.join(filings, "**", "*-*-*"), recursive=True)):
        acc = os.path.basename(d)
        if not (os.path.isdir(d) and ACC.match(acc)):
            continue
        p = pub.get(acc, rows.get(acc))
        if not p:
            undated += 1
            continue
        text = " ".join(open(x, encoding="utf-8" if x.endswith(".rows.txt") else "latin-1", errors="replace").read()
                        for x in sorted(glob.glob(os.path.join(d, "*.txt"))))
        out.append((p, re.sub(r"\s+", " ", text)))
    return sorted(out, key=lambda x: x[0]), undated


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker")
    ap.add_argument("--filings", required=True)
    ap.add_argument("--from", dest="start", default="0000")
    ap.add_argument("--to", dest="end", default="9999")
    ap.add_argument("--allow", nargs="*", default=[])
    a = ap.parse_args()
    sheet = load_sheet(a.ticker)
    docs, undated = corpus(a.filings, sheet)
    if not docs:
        sys.exit(f"no dated filings under {a.filings}")
    allow = METHOD_WORDS | set(a.allow) | {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(RETRO, "facts", "*.json"))}
    cache = {}
    miss, n, facts = set(), 0, 0
    for date, label, fields in dated_facts(sheet):
        if not a.start <= date <= a.end:
            continue
        facts += 1
        if date not in cache:
            cache[date] = " ".join(t for p, t in docs if p <= date)
        avail = cache[date]
        for own in own_texts(fields):
            toks = set(re.findall(r"\$[\d,]+(?:\.\d+)?[MBK]?", own)) | set(re.findall(r"(?<![\d-])(?:19|20)\d\d(?![\d-])", own)) | \
                set(re.findall(r"\b[A-Z][A-Za-z&.]+(?:\s[A-Z][A-Za-z&.]+)*", own))
            for tok in toks:
                n += 1
                base = tok.rstrip("MBK").replace("$", "") if tok.startswith("$") else tok
                if tok in allow or all(w in allow for w in tok.split()) or base in avail or tok in avail:
                    continue
                if tok.startswith("$") and base.split(".")[0] in avail:     # a computed figure: its digits must be filed
                    continue
                miss.add((date, label, tok))
    print(f"{a.ticker}: {len(docs)} dated filings ({undated} undated left out), {facts} facts, {n} tokens, {len(miss)} misses")
    for m in sorted(miss):
        print(" ", m)
    sys.exit(1 if miss else 0)


if __name__ == "__main__":
    main()
