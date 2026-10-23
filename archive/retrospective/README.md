# Retrospective archive

Point-in-time analyses: what the house model would have said on a past date,
using only information public on that date. Method, rules and the era-aware
taxonomy are in [`retro/README.md`](../../retro/README.md).

- `index.json` lists every entry: class, metrics and, under `outcome`, the
  hindsight scorecard.
- `<TICKER>/<AS_OF>/analysis.json` is the publishable record. It holds the
  classification, metrics, robustness checks and the dated source list.
- `<TICKER>/<AS_OF>/outcome.json` is hindsight, computed separately. Never feed it
  back into an analysis.

Rebuild the index with `python3 retro/retro_tool.py index`.
