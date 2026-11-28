#!/usr/bin/env python3
"""
Forward-reference scan: the author's own words in each dated fact may not name a later date, year or quarter.

    python3 retro/tools/forward_refs.py SCHW [--from 2010-01-01] [--to 2013-12-31]

For every dated fact (factwalk.py: sources, vintages, prints, their restatements, dividends, listings, guides, events, ...),
its string fields less quoted keys ('rows', 'quote', ...) and less text in single quotes (filing text, which verbatim.py checks)
(and less 'next_print', the label of the quarter after a print) are searched for
  - a quarter "Q1 2010" whose quarter end is on or after the fact's publication date,
  - a year after the publication year (not "FY2010", which labels fiscal years; review those by hand when a fiscal year
    differs from the calendar year),
  - an ISO date after the publication date.
Each hit is printed with its context. A forward reference can be legitimate (an outlook for next year, a date the filing
itself states, such as a listing's effective date or a dividend's payment date) only when the filing says it: then the
words belong in a quotation. The GOOG 2010-2013 and SCHW batches found and corrected leaks this way.
"""
import argparse
import os
import re
import signal
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from factwalk import dated_facts, load_sheet, own_texts  # noqa: E402

# 'next_print' names the quarter after a print ("Q1 2007 print (the quarter ends in March)"): a calendar fact, not hindsight
SKIP = {"next_print"}

QEND = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}


def scan(published, text):
    for m in re.finditer(r"\bQ([1-4]) ((?:19|20)\d\d)\b", text):
        if f"{m.group(2)}-{QEND[int(m.group(1))]}" >= published:
            yield "QUARTER", m
    for m in re.finditer(r"(?<!FY)(?<![\d-])((?:19|20)\d\d)(?![\d-])", text):
        if m.group(1) > published[:4]:
            yield "YEAR", m
    for m in re.finditer(r"\b(?:19|20)\d\d-\d\d-\d\d\b", text):
        if m.group(0) > published:
            yield "DATE", m


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticker")
    ap.add_argument("--from", dest="start", default="0000")
    ap.add_argument("--to", dest="end", default="9999")
    a = ap.parse_args()
    n = facts = 0
    for published, label, fields in dated_facts(load_sheet(a.ticker)):
        if not a.start <= published <= a.end:
            continue
        facts += 1
        for text in own_texts({k: v for k, v in fields.items() if k not in SKIP}):
            for kind, m in scan(published, text):
                n += 1
                print(f"{kind:8} {published} {label}: {m.group(0)}  ...{text[max(0, m.start() - 70):m.end() + 30]}...")
    print(f"{a.ticker}: {facts} dated facts scanned, {n} forward references")
    sys.exit(1 if n else 0)


if __name__ == "__main__":
    main()
