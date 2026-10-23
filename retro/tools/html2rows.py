#!/usr/bin/env python3
"""
Convert SEC filing HTML to text with one table row per line ("cell | cell | ...").

    python3 -I retro/tools/html2rows.py <file.htm> [...]     # writes <file>.rows.txt next to each input

Run it with -I on downloaded filings (untrusted input) so nothing is imported from their folder.
"""
import re
import sys
from html.parser import HTMLParser


class Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lines, self.cur, self.cell = [], [], []
        self.skip = self.intd = False

    def flush_cell(self):
        t = re.sub(r"\s+", " ", "".join(self.cell)).strip()
        if t and t not in ("$", "%", ")"):
            self.cur.append(t)
        elif t in ("%", ")") and self.cur:
            self.cur[-1] += t
        self.cell = []

    def end_row(self):
        if self.cur:
            self.lines.append(" | ".join(self.cur))
        self.cur = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip = True
        if tag in ("td", "th"):
            self.flush_cell()
            self.intd = True
        if tag == "tr":
            self.flush_cell()
            self.end_row()
        if tag in ("p", "br", "div", "h1", "h2", "h3", "li") and not self.intd:
            self.flush_cell()
            self.end_row()

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = False
        if tag in ("td", "th"):
            self.flush_cell()
            self.intd = False
        if tag in ("tr", "table"):
            self.flush_cell()
            self.end_row()

    def handle_data(self, data):
        if not self.skip:
            self.cell.append(data)


for path in sys.argv[1:]:
    p = Rows()
    with open(path, encoding="latin-1") as fh:
        p.feed(fh.read())
    p.flush_cell()
    p.end_row()
    out = path.rsplit(".", 1)[0] + ".rows.txt"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(p.lines))
    print(out, len(p.lines))
