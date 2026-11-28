#!/usr/bin/env python3
"""
Walk a retro fact sheet (retro/facts/<TICKER>.json) as dated facts, for the point-in-time scans in this folder.

    from factwalk import load_sheet, dated_facts, own_texts, models

A dated fact is
  - each source (its id and title, dated by its 'published'),
  - each element of a top-level list whose items carry 'published' (history_vintages, prints, guides, dividends, events,
    listings, splits, company_names, ...), or a top-level dict that carries one,
  - each dict, or list of dicts, carrying 'published' nested inside one of those ('restated', 'seg_later', 'geo_later',
    'servings_later', 'reissued', ...): a restatement or a field set published later, split out as a fact of its own date.
Undated parts (rule_t, fiscal_calendar, price_basis, _doc) are not facts here.

Nothing in this module reads outcomes, and it imports nothing from a downloaded file.
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RETRO = os.path.dirname(HERE)
ROOT = os.path.dirname(RETRO)

# keys whose values are labels, dates or pointers, not content
META_KEYS = {"published", "filed", "fy", "q", "quarter", "fy_label", "release", "kind", "exchange", "company",
             "margin_signal_name", "pe_window_start", "fiscal_year", "source", "sources", "eps_sources", "revenue_sources",
             "shares_sources", "url", "effective"}


def load_sheet(ticker):
    with open(os.path.join(RETRO, "facts", f"{ticker}.json"), encoding="utf-8") as fh:
        return json.load(fh)


def _is_dated(x):
    return isinstance(x, dict) and isinstance(x.get("published"), str)


def _facts(obj, label):
    own, nested = {}, []
    for k, v in obj.items():
        if _is_dated(v):
            nested += list(_facts(v, f"{label} {k}"))
        elif isinstance(v, list) and v and all(_is_dated(x) for x in v):
            for i, x in enumerate(v):
                nested += list(_facts(x, f"{label} {k}[{i}]"))
        else:
            own[k] = v
    yield obj["published"], label, own
    yield from nested


def _name(key, i, x):
    tag = x.get("quarter") or x.get("fy_label") or x.get("fy") or ""
    return f"{key}[{i}] {tag}".strip()


def dated_facts(sheet):
    """Yield (published, label, fields) for every dated fact; fields exclude the nested dated parts."""
    for sid, s in sheet.get("sources", {}).items():
        yield s["published"], f"source {sid}", {"id": f'"{sid}"', "title": s.get("title", ""), "supports": s.get("supports", "")}
    for key, v in sheet.items():
        if key == "sources":
            continue
        if isinstance(v, list):
            for i, x in enumerate(v):
                if _is_dated(x):
                    yield from _facts(x, _name(key, i, x))
        elif _is_dated(v):
            yield from _facts(v, key)


def strings(x, skip=META_KEYS):
    """Every string value under x, skipping label keys."""
    if isinstance(x, dict):
        for k, v in x.items():
            if k not in skip:
                yield from strings(v, skip)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v, skip)
    elif isinstance(x, str):
        yield x


def numbers(x, skip=META_KEYS):
    """Every number under x (bools out), skipping label keys."""
    if isinstance(x, dict):
        for k, v in x.items():
            if k not in skip:
                yield from numbers(v, skip)
    elif isinstance(x, list):
        for v in x:
            yield from numbers(v, skip)
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        yield x


# text the fact sheet copies from filings (verbatim.py checks it), not the author's own words
QUOTED_KEYS = {"rows", "row", "quote", "quotes", "crypto_quote", "crypto_own_quote", "title", "supports"}


QUOTATION = re.compile(r"(?<![A-Za-z])'.*?'(?![A-Za-z])")     # an apostrophe ("company's") neither opens nor closes one


def own_texts(fields):
    """The author's own words in a fact: its string fields less quoted keys, with '...' quotations blanked."""
    for s in strings(fields, META_KEYS | QUOTED_KEYS):
        yield QUOTATION.sub(" ", s)


def models(ticker):
    """(as_of, path) of every built model of the ticker, staging and archive."""
    out = []
    for base in ("staging", "archive"):
        for p in glob.glob(os.path.join(ROOT, base, "retrospective", ticker, "[12][09][0-9][0-9]-*", "model.py")):
            out.append((p.split(os.sep)[-2], p))
    return sorted(out)
