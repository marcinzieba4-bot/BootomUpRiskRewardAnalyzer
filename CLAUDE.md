# VeeRock Signal Analyzer — Project Notes for Claude

## ⚠️ CRITICAL: Always Use Live Prices

**Before refreshing or creating any signal model, you MUST fetch the current stock price from the internet — never use a hardcoded or remembered value.**

Steps required for every model refresh:
1. `WebSearch` → e.g. `"NVDA stock price today 2026"` to get current price + 52W range
2. `WebFetch` → Google Finance or Investing.com page for confirmation + P/E, EPS
3. `WebSearch` → latest earnings results + full-year EPS/revenue consensus estimates
4. Only then write or update the `*_signal_model.py`

Knowledge cutoff means stored prices are stale. Always verify against live sources. The user will consider it a bug if a model is deployed with a price from a prior session.

## Deployment Workflow

For each ticker model refresh:
1. Write/update `<ticker>_signal_model.py`
2. Verify: `python3 -c "from <ticker>_signal_model import RESULT as r; print(r)"`
3. Update SUMMARY entry in `lambda_function.py` (signal, price, date TODAY, epp_gap_pct, ratio_b_fmt, summary text)
4. `zip -q lambda_deploy.zip lambda_function.py *_signal_model.py`
5. `aws lambda update-function-code --function-name veerock-signal-api --zip-file fileb://lambda_deploy.zip`
6. Wait for `LastUpdateStatus=Successful`
7. Bump `CACHE_BUST` env var + delete `s3://s3bucketmz/veerock-signals/<TICKER>.json`
8. Wait for config update success
9. Verify via `aws lambda invoke` — check `signal`, `ratio_b_fmt`, `price`, `report` key length (~10K+ chars)
10. `git add *.py lambda_function.py && git commit && git push -u origin claude/adoring-meitner-tq1vwe`

## Infrastructure

- Lambda: `veerock-signal-api`, region `eu-north-1`
- S3 bucket: `s3bucketmz`, signals prefix: `veerock-signals/`
- Website: CloudFront `E15IJW4438D21G` → `https://d7g7nkeytae81.cloudfront.net`
- Website deploy: `bash deploy_website.sh` (builds Next.js static export, syncs to S3, invalidates CF)
- Git branch: `claude/adoring-meitner-tq1vwe`
- AWS CLI may need `pip install awscli` if not present in session

## Signal Thresholds

- ◉ BUY: ratio_b < 0.75 (color `#4ade80`)
- ◎ ACCUMULATE: ratio_b < 1.10 (color `#f0b429`)
- ◐ WATCHLIST: ratio_b < 1.75 (color `#60a5fa`)
- ✕ AVOID: ratio_b ≥ 1.75 (color `#f87171`)

## Model Template

Use `aapl_signal_model.py` as the canonical template. Key structure:
- `CENTERS = {"BEAR": 1.25, "BASE": 2.00, "BULL": 2.75, "XBULL": 3.75}`, `T = 0.60`
- `back_solve_market_composite()` using `1.15²` hurdle
- 6 weighted SIGNALS summing to 1.0, scored 1–4
- EPP = pessimistic P/E × current/bear EPS
- Export `RESULT` dict at the end (required — missing this causes Lambda ImportError)

## MODELS Dict Ordering

Tickers in `lambda_function.py` MODELS dict must be in strict alphabetical order. Double-check position before inserting.
