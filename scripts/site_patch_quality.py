#!/usr/bin/env python3
"""
Patches the built VeeRock site (the static/ tree inside veerock.tar.gz) so the
Research / Signals pages render the quality × price classes produced by
scripts/quality_classify.py instead of the legacy BUY/ACCUMULATE/WATCHLIST/AVOID
tier.

Touches exactly four files and verifies every replacement lands once:
  _next/static/chunks/174-*.js                 badge map, legend, sector chips
  _next/static/chunks/app/signals/[ticker]/*.js badge colour map on the detail page
  research/index.html, signals/index.html       SSR markup of the legend (must
                                                match the client render or React
                                                bails on hydration)

    python3 scripts/site_patch_quality.py --site /path/to/extracted/static
"""
import argparse
import glob
import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from quality_classify import CLASSES  # noqa: E402

TONE = {
    "green": dict(bg="bg-green-500/10", border="border-green-500/30", text="text-green-700", det="text-green-700 border-green-500/40 bg-green-500/10"),
    "amber": dict(bg="bg-amber-500/10", border="border-amber-500/30", text="text-amber-700", det="text-amber-700 border-amber-500/40 bg-amber-500/10"),
    "blue":  dict(bg="bg-blue-500/10",  border="border-blue-500/30",  text="text-blue-700",  det="text-blue-700  border-blue-500/40  bg-blue-500/10"),
    "red":   dict(bg="bg-red-500/10",   border="border-red-500/30",   text="text-red-700",   det="text-red-700   border-red-500/40   bg-red-500/10"),
}
LEGACY = {  # keep the legacy keys so old data never renders unstyled
    "ACCUMULATE": ("◎", "amber"), "WATCHLIST": ("◐", "blue"), "AVOID": ("✕", "red"),
    "BUY": ("◉", "green"), "HOLD": ("▷", "blue"), "HOLD/TRIM": ("▷", "blue"), "ACQUIRED": ("◐", "blue"),
}
LEGEND_NOTE = {
    "COMPOUNDER AT LOW PRICE": "Durable × cheap",
    "QUALITY, NEUTRALLY VALUED": "Durable × fair",
    "QUALITY, PRICED FOR PERFECTION": "Durable × rich",
    "CYCLICAL, RISK PRICED IN": "Cyclical × cheap",
    "CYCLICAL, NEUTRALLY VALUED": "Cyclical × fair",
    "TOO MUCH CYCLE RISK": "Cyclical × rich",
    "CHEAP, BUT STRUCTURAL RISK": "Structural × cheap",
    "STRUCTURAL RISK, NOT CHEAP": "Structural × fair/rich",
    "TURNAROUND BET": "Broken earnings, intact franchise",
    "SPECIAL SITUATION": "Deal, binary or bond",
}


def js_str(s):
    return '"' + s.replace('"', '\\"') + '"'


def badge_map_js():
    parts = []
    for key, c in CLASSES.items():
        t = TONE[c["tone"]]
        parts.append(f'{js_str(key)}:{{icon:{js_str(c["icon"])},bg:"{t["bg"]}",border:"{t["border"]}",text:"{t["text"]}"}}')
    for key, (icon, tone) in LEGACY.items():
        t = TONE[tone]
        parts.append(f'{js_str(key)}:{{icon:{js_str(icon)},bg:"{t["bg"]}",border:"{t["border"]}",text:"{t["text"]}"}}')
    return "let n={" + ",".join(parts) + "}"


def detail_map_js():
    parts = []
    for key, c in CLASSES.items():
        parts.append(f'{js_str(key)}:"{TONE[c["tone"]]["det"]}"')
    for key, (icon, tone) in LEGACY.items():
        parts.append(f'{js_str(key)}:"{TONE[tone]["det"]}"')
    return "let i={" + ",".join(parts) + "}"


def legend_js():
    items = []
    for key, c in CLASSES.items():
        items.append(f'{{label:{js_str(c["icon"] + " " + key)},note:{js_str(LEGEND_NOTE[key])},desc:{js_str(c["desc"])},cls:"{TONE[c["tone"]]["text"]}"}}')
    return "[" + ",".join(items) + "]"


def legend_html():
    cells = []
    for key, c in CLASSES.items():
        cells.append(
            '<div class="p-3 rounded-lg bg-vr-surface">'
            f'<div class="font-mono font-bold text-sm mb-1 {TONE[c["tone"]]["text"]}">{html.escape(c["icon"] + " " + key, quote=False)}</div>'
            f'<div class="text-vr-text text-xs font-medium mb-0.5">{html.escape(LEGEND_NOTE[key], quote=False)}</div>'
            f'<div class="text-vr-faint text-xs">{html.escape(c["desc"], quote=False)}</div>'
            '</div>'
        )
    return "".join(cells)


OLD_MAP = ('let n={ACCUMULATE:{icon:"◎",bg:"bg-amber-500/10",border:"border-amber-500/30",text:"text-amber-700"},'
           'WATCHLIST:{icon:"◐",bg:"bg-blue-500/10",border:"border-blue-500/30",text:"text-blue-700"},'
           'AVOID:{icon:"✕",bg:"bg-red-500/10",border:"border-red-500/30",text:"text-red-700"},'
           'BUY:{icon:"◉",bg:"bg-green-500/10",border:"border-green-500/30",text:"text-green-700"}}')
OLD_LEGEND = ('[{label:"◉ BUY",note:"Ratio B < 0.75x",desc:"Floor gap dominated by upside",cls:"text-green-700"},'
              '{label:"◎ ACCUMULATE",note:"Ratio B 0.75–1.1x",desc:"Balanced; edge to upside",cls:"text-amber-700"},'
              '{label:"◐ WATCHLIST",note:"Ratio B 1.1–1.75x",desc:"Floor gap exceeds EPS upside",cls:"text-blue-700"},'
              '{label:"✕ AVOID",note:"Ratio B > 1.75x",desc:"Growth fully priced in",cls:"text-red-700"}]')
OLD_CHIPS = '["BUY","ACCUMULATE","WATCHLIST","AVOID"].map(e=>{let t=a[e];'
OLD_DETAIL = ('let i={ACCUMULATE:"text-amber-700 border-amber-500/40 bg-amber-500/10",'
              'WATCHLIST:"text-blue-700  border-blue-500/40  bg-blue-500/10",'
              'AVOID:"text-red-700   border-red-500/40   bg-red-500/10",'
              'BUY:"text-green-700 border-green-500/40 bg-green-500/10"}')
OLD_LEGEND_HTML = (
    '<div class="p-3 rounded-lg bg-vr-surface"><div class="font-mono font-bold text-sm mb-1 text-green-700">◉ BUY</div>'
    '<div class="text-vr-text text-xs font-medium mb-0.5">Ratio B &lt; 0.75x</div><div class="text-vr-faint text-xs">Floor gap dominated by upside</div></div>'
    '<div class="p-3 rounded-lg bg-vr-surface"><div class="font-mono font-bold text-sm mb-1 text-amber-700">◎ ACCUMULATE</div>'
    '<div class="text-vr-text text-xs font-medium mb-0.5">Ratio B 0.75–1.1x</div><div class="text-vr-faint text-xs">Balanced; edge to upside</div></div>'
    '<div class="p-3 rounded-lg bg-vr-surface"><div class="font-mono font-bold text-sm mb-1 text-blue-700">◐ WATCHLIST</div>'
    '<div class="text-vr-text text-xs font-medium mb-0.5">Ratio B 1.1–1.75x</div><div class="text-vr-faint text-xs">Floor gap exceeds EPS upside</div></div>'
    '<div class="p-3 rounded-lg bg-vr-surface"><div class="font-mono font-bold text-sm mb-1 text-red-700">✕ AVOID</div>'
    '<div class="text-vr-text text-xs font-medium mb-0.5">Ratio B &gt; 1.75x</div><div class="text-vr-faint text-xs">Growth fully priced in</div></div>'
)


def replace_once(path, old, new, label):
    with open(path, encoding="utf-8") as fh:
        s = fh.read()
    n = s.count(old)
    if n == 0 and s.count(new) >= 1:
        print(f"  {label}: already patched")
        return
    if n != 1:
        sys.exit(f"  {label}: expected exactly 1 occurrence in {path}, found {n}")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(s.replace(old, new))
    print(f"  {label}: patched")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True, help="path to the extracted static/ directory")
    a = ap.parse_args()
    site = a.site
    chunk = glob.glob(os.path.join(site, "_next/static/chunks/174-*.js"))
    detail = glob.glob(os.path.join(site, "_next/static/chunks/app/signals/[[]ticker[]]/page-*.js"))
    if len(chunk) != 1 or len(detail) != 1:
        sys.exit(f"could not locate chunks: {chunk} {detail}")
    new_chips = "[" + ",".join(js_str(k) for k in CLASSES) + "].map(e=>{let t=a[e];"
    print(chunk[0])
    replace_once(chunk[0], OLD_MAP, badge_map_js(), "badge map")
    replace_once(chunk[0], OLD_LEGEND, legend_js(), "legend")
    replace_once(chunk[0], OLD_CHIPS, new_chips, "sector chips")
    print(detail[0])
    replace_once(detail[0], OLD_DETAIL, detail_map_js(), "detail badge map")
    for page in ("research/index.html", "signals/index.html"):
        p = os.path.join(site, page)
        print(p)
        replace_once(p, OLD_LEGEND_HTML, legend_html(), "SSR legend")
    print("done")


if __name__ == "__main__":
    main()
