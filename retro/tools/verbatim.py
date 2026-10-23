#!/usr/bin/env python3
"""
Check that every quoted fact appears word for word in the filing it is attributed to.

    python3 -I retro/tools/verbatim.py checklist.json

checklist.json maps a converted filing (a *.rows.txt path, or a glob matching exactly one) to the strings
that must appear in it:

    {"/scratch/sec2015/q2fy15__ex991.rows.txt": ["$7.7 billion", "Products | 1,930,331 | 1,801,062 | 7 | 10"]}

Whitespace is collapsed on both sides. Check each string against its own release: the same phrase in a
different quarter's release proves nothing (this once caught a buyback sentence taken from the wrong file).
Exits non-zero if anything is missing.
"""
import glob
import json
import re
import sys

norm = lambda s: re.sub(r"\s+", " ", s)
with open(sys.argv[1], encoding="utf-8") as fh:
    checklist = json.load(fh)
ok = total = 0
for pattern, needles in checklist.items():
    paths = glob.glob(pattern)
    if len(paths) != 1:
        sys.exit(f"{pattern}: matches {len(paths)} files, expected 1")
    with open(paths[0], encoding="utf-8", errors="replace") as fh:
        text = norm(fh.read())
    for needle in needles:
        total += 1
        if norm(needle) in text:
            ok += 1
        else:
            print(f"MISSING in {paths[0]}: {needle[:140]}")
print(f"{ok}/{total} verbatim")
sys.exit(0 if ok == total else 1)
