#!/usr/bin/env python3
"""
Download a company's SEC filings for a fact sheet: index, list, fetch (full submissions), split into documents, date them.

    python3 retro/tools/edgar.py index CIK DIR                      # DIR/allrows.json: every filing EDGAR lists
    python3 retro/tools/edgar.py list DIR --from 2010-01-01 --to 2013-12-31 [--forms 10-K 10-Q 8-K]
    python3 retro/tools/edgar.py fetch CIK DIR --from 2010-01-01 --to 2013-12-31 [--forms ...] [--acc ACC ...]
    python3 -I retro/tools/edgar.py split DIR/eightk/0001193125-10-008163.txt [...]
    python3 retro/tools/edgar.py when DIR ACC --ticker SCHW         # acceptance time in ET and the date the fact gets

Keep DIR outside the repository (the session's scratchpad): filings are inputs, read and cited by URL, never committed.

index   reads data.sec.gov/submissions/CIK##########.json and its older pages (filings.files), and writes DIR/allrows.json,
        a sorted list of [filingDate, acceptanceDateTime, form, accession, primaryDocument, items, description].
fetch   downloads each matching filing's full submission (Archives/edgar/data/CIK/ACC/ACC.txt) into DIR/tenk, DIR/tenq,
        DIR/eightk or DIR/other (10-K*, 10-Q*, 8-K*, the rest), skips files already there, and splits each one.
split   writes DIR/<sub>/<ACC>/<TYPE>__<filename> for each document of a full submission, and runs html2rows.py (-I) on the
        HTML ones (<TYPE>__<name>.rows.txt: one table row per line, "cell | cell | ...").
when    prints the publication date by the acceptance-time rule: EDGAR's acceptance time converted to ET; accepted at or after
        16:00 ET, the next trading day (from Yahoo's series for --ticker); before 09:30 ET, that day, before the open; a time of
        exactly 00:00 ET (EDGAR gives the date only) is treated as before the open. Note the README rules that refine this
        (a release accepted during the session on the week's last trading day dates its own week: the UNP Good Friday rule).

The User-Agent: SEC asks automated clients for a contact. Never put the owner's email (or any personal address) there; the
default is a plain client name, which www.sec.gov and data.sec.gov accepted in the SCHW sessions (2026-11). If SEC refuses it
(403, or an "Undeclared Automated Tool" page), stop and record the batch as reduced-data or ask the owner (the CRM 2013-2017
batch). The tool refuses a User-Agent containing "@". Requests are spaced by --sleep seconds (default 0.3; SEC's limit is 10/s).
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "BottomUpRetro research-bot"
ET = ZoneInfo("America/New_York")


def get(url, ua, sleep):
    if "@" in ua:
        sys.exit("refusing a User-Agent with an email address in it (CLAUDE.md: never the owner's email)")
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "identity"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            time.sleep(sleep)
            return data
        except urllib.error.HTTPError as e:
            if e.code in (403, 404):
                raise
            time.sleep(2 ** attempt)
        except (urllib.error.URLError, TimeoutError):
            time.sleep(2 ** attempt)
    raise RuntimeError(f"failed: {url}")


def cik10(cik):
    return f"{int(cik):010d}"


def index(cik, d, ua, sleep):
    os.makedirs(d, exist_ok=True)
    main = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik10(cik)}.json", ua, sleep))
    pages = [main["filings"]["recent"]]
    with open(os.path.join(d, "sub.json"), "w", encoding="utf-8") as fh:
        json.dump(main, fh)
    for f in main["filings"].get("files", []):
        page = json.loads(get(f"https://data.sec.gov/submissions/{f['name']}", ua, sleep))
        with open(os.path.join(d, f["name"]), "w", encoding="utf-8") as fh:
            json.dump(page, fh)
        pages.append(page)
    rows = set()
    for r in pages:
        n = len(r["form"])
        items = r.get("items", [""] * n)
        for i in range(n):
            rows.add((r["filingDate"][i], r["acceptanceDateTime"][i], r["form"][i], r["accessionNumber"][i],
                      r["primaryDocument"][i], items[i], r["primaryDocDescription"][i]))
    rows = sorted(rows)
    with open(os.path.join(d, "allrows.json"), "w", encoding="utf-8") as fh:
        json.dump(rows, fh)
    print(main.get("name"), main.get("tickers"), main.get("exchanges"), "fiscal year end", main.get("fiscalYearEnd"))
    print(len(rows), "filings,", rows[0][0], "to", rows[-1][0], "->", os.path.join(d, "allrows.json"))


def load_rows(d):
    with open(os.path.join(d, "allrows.json"), encoding="utf-8") as fh:
        return json.load(fh)


def select(rows, start, end, forms, accs):
    for r in rows:
        if accs:
            if r[3] in accs:
                yield r
        elif start <= r[0] <= end and (not forms or r[2] in forms):
            yield r


def sub(form):
    return "tenk" if form.startswith("10-K") else "tenq" if form.startswith("10-Q") else "eightk" if form.startswith("8-K") else "other"


def split(path):
    acc = os.path.basename(path)[:-4]
    out = os.path.join(os.path.dirname(path), acc)
    os.makedirs(out, exist_ok=True)
    raw = open(path, encoding="latin-1").read()
    m = re.search(r"ACCEPTANCE-DATETIME:\s*(\d+)", raw)
    print(acc, "accepted", m.group(1) if m else None)
    for doc in re.findall(r"<DOCUMENT>(.*?)</DOCUMENT>", raw, re.S):
        t = re.search(r"<TYPE>([^\n<]+)", doc).group(1).strip()
        fn = (re.search(r"<FILENAME>([^\n<]+)", doc) or re.search(r"<SEQUENCE>([^\n<]+)", doc)).group(1).strip()
        body = re.search(r"<TEXT>(.*)</TEXT>", doc, re.S)
        body = body.group(1) if body else doc
        name = os.path.join(out, f"{t.replace('/', '_')}__{fn}")
        with open(name, "w", encoding="latin-1") as fh:
            fh.write(body)
        if re.search(r"<(html|table|TABLE|HTML)", body[:5000]) or fn.lower().endswith((".htm", ".html")):
            subprocess.run([sys.executable, "-I", os.path.join(HERE, "html2rows.py"), name], check=True, capture_output=True)
        print("  ", t, fn, len(body))


def fetch(cik, d, rows, ua, sleep):
    n = 0
    for r in rows:
        acc = r[3]
        folder = os.path.join(d, sub(r[2]))
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, f"{acc}.txt")
        if not os.path.exists(path):
            data = get(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{acc}.txt", ua, sleep)
            if b"<DOCUMENT>" not in data:
                sys.exit(f"{acc}: no <DOCUMENT> in the response (SEC refused the client?); first bytes: {data[:200]!r}")
            with open(path, "wb") as fh:
                fh.write(data)
            n += 1
        if not os.path.isdir(os.path.join(folder, acc)):
            split(path)
    print(n, "downloaded")


def trading_days(ticker):
    sys.path.insert(0, os.path.dirname(HERE))
    import retro_tool
    chart = retro_tool.chart(ticker)
    off = chart["meta"]["gmtoffset"]
    return sorted({dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date().isoformat()
                   for t, c in zip(chart["timestamp"], chart["indicators"]["quote"][0]["close"]) if c is not None})


def published(acceptance, tdays):
    """(date, words) by the acceptance-time rule; acceptance is EDGAR's acceptanceDateTime (UTC, ...Z)."""
    t = dt.datetime.fromisoformat(acceptance.replace("Z", "+00:00")).astimezone(ET)
    d = t.date().isoformat()
    if t.strftime("%H:%M:%S") == "00:00:00":
        return d, f"accepted {d} (EDGAR gives the date only; treated as before the open)"
    hm = t.strftime("%H:%M")
    if hm >= "16:00":
        return min(x for x in tdays if x > d), f"accepted {d} {hm} ET (after the close), so dated the next trading day"
    if hm < "09:30":
        return d, f"accepted {d} {hm} ET (before the open)"
    return d, f"accepted {d} {hm} ET (during market hours)"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ua", default=UA, help="User-Agent (never an email address)")
    ap.add_argument("--sleep", type=float, default=0.3)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("index")
    p.add_argument("cik")
    p.add_argument("dir")
    for name in ("list", "fetch"):
        p = sp.add_parser(name)
        if name == "fetch":
            p.add_argument("cik")
        p.add_argument("dir")
        p.add_argument("--from", dest="start", default="0000")
        p.add_argument("--to", dest="end", default="9999")
        p.add_argument("--forms", nargs="*", default=[])
        p.add_argument("--acc", nargs="*", default=[])
    p = sp.add_parser("split")
    p.add_argument("files", nargs="+")
    p = sp.add_parser("when")
    p.add_argument("dir")
    p.add_argument("acc", nargs="+")
    p.add_argument("--ticker", required=True)
    a = ap.parse_args()
    if a.cmd == "index":
        index(a.cik, a.dir, a.ua, a.sleep)
    elif a.cmd == "list":
        for r in select(load_rows(a.dir), a.start, a.end, set(a.forms), set(a.acc)):
            print(r[2], r[3], r[0], r[1], r[5] or "-", "|", (r[6] or "")[:70])
    elif a.cmd == "fetch":
        fetch(a.cik, a.dir, list(select(load_rows(a.dir), a.start, a.end, set(a.forms), set(a.acc))), a.ua, a.sleep)
    elif a.cmd == "split":
        for f in a.files:
            split(f)
    elif a.cmd == "when":
        rows = {r[3]: r for r in load_rows(a.dir)}
        tdays = trading_days(a.ticker)
        for acc in a.acc:
            print(acc, rows[acc][2], *published(rows[acc][1], tdays))


if __name__ == "__main__":
    main()
