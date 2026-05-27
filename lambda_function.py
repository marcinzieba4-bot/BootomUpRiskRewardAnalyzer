"""
veerock-signal-api  v3
Runs the actual signal model .py files and caches results in S3.

GET  /signals                → list of tickers with summary metadata
GET  /signals/{TICKER}       → full report text (Part 2 + Part 3) as JSON
GET  /signals/{TICKER}/raw   → plain text (for terminal / embedding)
POST /signals/refresh        → regenerate all models and save to S3
EventBridge scheduled event  → same as POST /signals/refresh (auto daily)
"""
import json, io, os, contextlib, runpy, boto3, datetime
from botocore.exceptions import ClientError

S3_BUCKET = "s3bucketmz"
S3_PREFIX = "veerock-signals/"

MODELS = {
    "ISRG": "isrg_signal_model.py",
    "MSFT": "msft_signal_model.py",
    "MU":   "mu_signal_model.py",
    "WMB":  "wmb_signal_model.py",
    "AAPL": "aapl_signal_model.py",
    "SO":   "so_signal_model.py",
    "TSLA": "tsla_signal_model.py",
    "NVDA": "nvda_signal_model.py",
    "LRCX": "lrcx_signal_model.py",
    "HD":   "hd_signal_model.py",
    "AVGO": "avgo_signal_model.py",
    "MCD":  "mcd_signal_model.py",
    "CRM":  "crm_signal_model.py",
    "ORCL": "orcl_signal_model.py",
    "CSCO": "csco_signal_model.py",
    "SAP":  "sap_signal_model.py",
    "NOW":  "now_signal_model.py",
    "KTY":  "kty_signal_model.py",
    "ACN":  "acn_signal_model.py",
    "IBM":  "ibm_signal_model.py",
    "AMD":  "amd_signal_model.py",
    "ADBE": "adbe_signal_model.py",
    "INTU": "intu_signal_model.py",
    "QCOM": "qcom_signal_model.py",
    "TXN":  "txn_signal_model.py",
    "PLTR": "pltr_signal_model.py",
    "PANW": "panw_signal_model.py",
    "INTC": "intc_signal_model.py",
    "PKN":  "pkn_signal_model.py",
    "MRVL": "mrvl_signal_model.py",
    "CAT":  "cat_signal_model.py",
    "LLY":  "lly_signal_model.py",
    "UNH":  "unh_signal_model.py",
    "JNJ":  "jnj_signal_model.py",
    "ABBV": "abbv_signal_model.py",
    "MRK":  "mrk_signal_model.py",
    "TMO":  "tmo_signal_model.py",
    "ABT":  "abt_signal_model.py",
    "PFE":  "pfe_signal_model.py",
    "DHR":  "dhr_signal_model.py",
    "AMGN": "amgn_signal_model.py",
    "BSX":  "bsx_signal_model.py",
    "SYK":  "syk_signal_model.py",
    "BMY":  "bmy_signal_model.py",
    "GILD": "gild_signal_model.py",
    "VRTX": "vrtx_signal_model.py",
    "ELV":  "elv_signal_model.py",
    "BRK":  "brk_signal_model.py",
    "JPM":  "jpm_signal_model.py",
    "V":    "v_signal_model.py",
    "MA":   "ma_signal_model.py",
    "BAC":  "bac_signal_model.py",
    "WFC":  "wfc_signal_model.py",
    "GS":   "gs_signal_model.py",
    "AXP":  "axp_signal_model.py",
    "SPGI": "spgi_signal_model.py",
    "MS":   "ms_signal_model.py",
    "BLK":  "blk_signal_model.py",
}

# Warm-invocation memory cache
_cache: dict = {}

SUMMARY = {
    "ISRG": {"ticker": "ISRG", "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 452.00,  "date": "2026-05-09", "epp_gap_pct": 26.5,  "ratio_b_fmt": "0.92x",
              "sector_group": "Healthcare",
              "company": "Intuitive Surgical",     "sector": "Surgical Robotics · Medical Devices",
              "summary": "Best-in-class surgical robotics with the da Vinci 5 platform driving a multi-year procedure growth cycle. 27% above EPP floor with balanced risk/reward."},
    "MSFT": {"ticker": "MSFT", "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",  "signal_color": "#60a5fa",
              "price": 417.42, "date": "2026-05-20", "epp_gap_pct": 44.3,  "ratio_b_fmt": "1.22x",
              "sector_group": "Technology",
              "company": "Microsoft",               "sector": "Enterprise Software · Cloud · AI",
              "summary": "Azure and Copilot execution strong, but market composite slightly above proxy. Watch for AI monetisation evidence before adding."},
    "MU":   {"ticker": "MU",   "signal": "✕ AVOID",      "signal_short": "AVOID",      "signal_color": "#f87171",
              "price": 120.55, "date": "2026-05-21", "epp_gap_pct": 119.8, "ratio_b_fmt": "N/A",
              "sector_group": "Technology",
              "company": "Micron Technology",       "sector": "Semiconductor Memory · HBM · DRAM/NAND",
              "summary": "HBM opportunity is real but fully priced. Memory cycle volatility (Beta 1.35) and 120% EPP gap leave no margin of safety."},
    "WMB":  {"ticker": "WMB",  "signal": "✕ AVOID",      "signal_short": "AVOID",      "signal_color": "#f87171",
              "price": 78.41,  "date": "2026-05-20", "epp_gap_pct": 133.4, "ratio_b_fmt": "N/A",
              "sector_group": "Energy",
              "company": "The Williams Companies",  "sector": "Midstream Energy · Natural Gas Pipelines",
              "summary": "AI infrastructure re-rating paradox. All 6 signals BULL but market has priced it at 37x P/E. BASE scenario below current price."},
    "AAPL": {"ticker": "AAPL", "signal": "✕ AVOID",      "signal_short": "AVOID",      "signal_color": "#f87171",
              "price": 302.25, "date": "2026-05-21", "epp_gap_pct": 102.3, "ratio_b_fmt": "N/A",
              "sector_group": "Technology",
              "company": "Apple Inc.",               "sector": "Consumer Technology · Hardware & Software Ecosystem",
              "summary": "AI Intelligence re-rating at 40x trailing P/E for 7%/yr EPS compounder. Cross-read composite below market. China at BASE is the key drag."},
    "TSLA": {"ticker": "TSLA", "signal": "✕ AVOID",      "signal_short": "AVOID",      "signal_color": "#f87171",
              "price": 414.75, "date": "2026-05-21", "epp_gap_pct": 893,   "ratio_b_fmt": "N/A",
              "sector_group": "Consumer Discretionary",
              "company": "Tesla, Inc.",               "sector": "EV · AI Autonomy · Energy Storage",
              "summary": "Priced for the BULL scenario (Cybercab at scale, Optimus deployed) at 104x FY2027E consensus EPS. Method B target $320 is below current price. Re-evaluate below $280."},
    "SO":   {"ticker": "SO",   "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",  "signal_color": "#60a5fa",
              "price": 93.05,  "date": "2026-05-21", "epp_gap_pct": 27.3,  "ratio_b_fmt": "1.31x",
              "sector_group": "Utilities",
              "company": "Southern Company",         "sector": "Regulated Electric Utility · Nuclear · AI Infrastructure",
              "summary": "Vogtle nuclear + AI data-centre demand re-rating in progress. Execution confirmed but at 20.5x forward the risk/reward is balanced. Rate path is the swing factor."},
    "NVDA": {"ticker": "NVDA", "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 220.66, "date": "2026-05-21", "epp_gap_pct": 44.6,  "ratio_b_fmt": "0.93x",
              "sector_group": "Technology",
              "company": "NVIDIA Corporation",        "sector": "Semiconductors · AI Infrastructure",
              "summary": "CUDA moat + annual architecture cadence = durable AI monopoly. 26.5x FY2027E is the cheapest mega-cap by PEG. EPP floor of $153 rising to $336 by FY2028E — floor surpasses today's price within 18-24 months at consensus EPS."},
    "HD":   {"ticker": "HD",   "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",  "signal_color": "#60a5fa",
              "price": 309.91, "date": "2026-05-21", "epp_gap_pct": 17.2,  "ratio_b_fmt": "1.44x",
              "sector_group": "Consumer Discretionary",
              "company": "Home Depot, Inc.",          "sector": "Home Improvement Retail · Housing Cycle",
              "summary": "Dominant duopoly moat + aging US housing stock provide structural floor. Housing freeze (7%+ mortgages) caps near-term EPS at $14-15. EPP floor $264 only 17% below current price — well-protected downside. Await rate cuts or comp inflection to upgrade to ACCUMULATE."},
    "LRCX": {"ticker": "LRCX", "signal": "✕ AVOID",      "signal_short": "AVOID",      "signal_color": "#f87171",
              "price": 298.46, "date": "2026-05-21", "epp_gap_pct": 216.3, "ratio_b_fmt": "N/A",
              "sector_group": "Technology",
              "company": "Lam Research Corporation",  "sector": "Semiconductor Equipment · WFE · Etch",
              "summary": "Etch monopoly (~50% global share) is real but fully priced. At 53.8x FY2026E, the market is pricing the BULL scenario as the floor. Method B target $160 is 46% below current price. Re-evaluate below $165."},
    "AVGO": {"ticker": "AVGO", "signal": "✕ AVOID",      "signal_short": "AVOID",      "signal_color": "#f87171",
              "price": 417.76, "date": "2026-05-21", "epp_gap_pct": 282.8, "ratio_b_fmt": "N/A",
              "sector_group": "Technology",
              "company": "Broadcom Inc.",               "sector": "Semiconductors · AI Infrastructure · Enterprise Software",
              "summary": "Hyperscaler XPU near-monopoly (Google TPU, Meta MTIA) + VMware software transformation = AI compounding machine. But market prices 33x FY2027E — all three catalysts already in. Method B target $356 is 15% below current. EPP floor $109 at +283% gap. Re-evaluate below $300."},
    "MCD":  {"ticker": "MCD",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 280.27, "date": "2026-05-21", "epp_gap_pct": 14.9,  "ratio_b_fmt": "0.83x",
              "sector_group": "Consumer Staples",
              "company": "McDonald's Corporation",      "sector": "QSR · Franchise Model · Consumer Staple-Like",
              "summary": "95% franchised real-estate model with $8.2B annual rent income. Near 52-week low ($272) with EPP gap of only 15% — lowest in coverage. Four consecutive positive comp quarters; Q1 2026 +3.8%. Ratio B 0.83x. 2.7% dividend yield while waiting for re-rating to 24x."},
    "CRM":  {"ticker": "CRM",  "signal": "◉ BUY",        "signal_short": "BUY",        "signal_color": "#22c55e",
              "price": 176.31, "date": "2026-05-21", "epp_gap_pct": -25.6, "ratio_b_fmt": "-0.32x",
              "sector_group": "Technology",
              "company": "Salesforce, Inc.",              "sector": "Enterprise SaaS · CRM · Agentic AI Platform",
              "summary": "Only name in coverage trading 25.6% BELOW EPP floor. 8.4% FCF yield, $50B buyback, 29K Agentforce deals. Market pricing maximum AI disruption fear at 13.4x FY2027E. Q1 FY2027 earnings May 27. First BUY signal in coverage universe."},
    "ORCL": {"ticker": "ORCL", "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 189.50, "date": "2026-05-22", "epp_gap_pct": 76.0,  "ratio_b_fmt": "0.90x",
              "sector_group": "Technology",
              "company": "Oracle Corporation",             "sector": "Enterprise Cloud · Database · AI Infrastructure",
              "summary": "$523B RPO backlog equals market cap — unprecedented revenue visibility. OCI growing +84% YoY; down 45% from $345 peak. Ratio B 0.90x; 76% above EPP floor. Q4 FY2026 catalyst ~Jun 2026. Risk: $50B capex compressing near-term FCF."},
    "CSCO": {"ticker": "CSCO", "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 118.20, "date": "2026-05-22", "epp_gap_pct": 97.3,  "ratio_b_fmt": "1.94x",
              "sector_group": "Technology",
              "company": "Cisco Systems, Inc.",            "sector": "Enterprise Networking · AI Infrastructure · Security",
              "summary": "Near 52-week highs; up 90% in 12 months. AI orders raised to $9B FY2026; Silicon One winning GPU cluster fabric. But at 27.6x FY2026 EPS the easy money is made. Method B $148 (+25%). Accumulate on pullback to $95–105."},
    "SAP":  {"ticker": "SAP",  "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 167.27, "date": "2026-05-22", "epp_gap_pct": 4.5,   "ratio_b_fmt": "0.09x",
              "sector_group": "Technology",
              "company": "SAP SE",                         "sector": "Enterprise ERP Cloud · Business AI · HR/Finance SaaS",
              "summary": "Stock at EPP structural floor ($160) after 47% drawdown from $313 ATH. Trading at 20x forward EPS — 20-year multiple low. S/4HANA 2027 migration deadline locks 300M users into cloud. Cloud +27% YoY; €63B backlog. Method B $252 (+51%). Ratio B 0.09x."},
    "NOW":  {"ticker": "NOW",  "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 100.58, "date": "2026-05-22", "epp_gap_pct": 14.3,  "ratio_b_fmt": "0.11x",
              "sector_group": "Technology",
              "company": "ServiceNow, Inc.",               "sector": "Enterprise SaaS · Workflow Automation · Agentic AI Platform",
              "summary": "Down 52% from $211.48 ATH; 5-for-1 split Dec 2025. Q1 2026 non-GAAP EPS $0.97 beat $0.55 est by 76%. RPO $27.7B +24%. Trading at 25x FY2026E — lowest multiple since 2018. Method B $215 (+114%). Ratio B 0.11x. Agentic AI fear vs platform moat mispricing."},
    "ACN":  {"ticker": "ACN",  "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 177.52, "date": "2026-05-21", "epp_gap_pct": -19.5, "ratio_b_fmt": "-0.23x",
              "sector_group": "Technology",
              "company": "Accenture plc",                 "sector": "IT Consulting & Services · Digital Transformation · Agentic AI",
              "summary": "Down 49% from ATH ~$345. Trading at 12.9x FY2026E — lowest P/E in modern history; COVID trough was 21x. Stock 19.5% below EPP floor ($220). FCF yield 9.8% ($10.9B / $111B mkt cap). AI bookings $2.2B Q1 FY26 (+100% YoY). Record $22.1B Q2 bookings. DOGE headwind is 1-1.5% of revenue — not existential. Method B $368 (+107%). BUY."},
    "KTY":  {"ticker": "KTY",  "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 1155.00,"date": "2026-05-22", "epp_gap_pct": 62.5,  "ratio_b_fmt": "3.24x",
              "sector_group": "Basic Resources",
              "company": "Grupa Kęty SA",                  "sector": "Aluminium Processing · Building Systems · Flexible Packaging",
              "summary": "Note: PLN-denominated stock (WSE/GPW). Near ATH 1,179 PLN (May 6 2026). Strong fundamentals — CBAM tailwind, SELT synergies, 85% payout — but fully priced at 17.9x FY2026E. Avg analyst target 950 PLN (-18%). Method B PLN 1,292 (+12%). Ratio B 3.24x. Accumulate on pullback to 850-950 PLN."},
    "IBM":  {"ticker": "IBM",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE",  "signal_color": "#f0b429",
              "price": 253.84, "date": "2026-05-22", "epp_gap_pct": 32.7,  "ratio_b_fmt": "1.02x",
              "sector_group": "Technology",
              "company": "International Business Machines Corporation", "sector": "Hybrid Cloud · Enterprise AI (watsonx) · Quantum Computing",
              "summary": "Post-Kyndryl IBM: Software +11% Q1 2026; watsonx AI + Red Hat OpenShift + HashiCorp. $1B govt quantum investment drove +17.2% surge. Pre-surge ~$216 was ◉ BUY (ratio_b ~0.12x). Post-surge ACCUMULATE. FCF ~$14B; 2.66% dividend yield. Method B $315 (+24%). Add on pullback to $215–230."},
    "AMD":  {"ticker": "AMD",  "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 467.51, "date": "2026-05-24", "epp_gap_pct": 187.7, "ratio_b_fmt": "3.30x",
              "sector_group": "Technology",
              "company": "Advanced Micro Devices, Inc.", "sector": "Semiconductors · AI GPU · Data Center · PC/Client CPU",
              "summary": "ATH $481.41 (May 22 2026); +317% 12-month surge. Q1 2026 Data Center +57% to $5.8B; EPS $1.37 beat. Real business, but at 72x FY2026E the market prices perfection. NVIDIA CUDA moat and custom ASIC (Google/Meta/AWS) are structural risks. Method B $560 (+20%) vs BEAR $80 (-83%). EPP floor $162.50 (+188% gap). Re-evaluate on pullback to $250–300."},
    "ADBE": {"ticker": "ADBE", "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 244.48, "date": "2026-05-24", "epp_gap_pct": -30.3, "ratio_b_fmt": "-0.33x",
              "sector_group": "Technology",
              "company": "Adobe Inc.", "sector": "Creative SaaS · Document Cloud · AI Generative Tools",
              "summary": "Down 65% from $699 ATH; trading at 10.4x FY2026E non-GAAP EPS — lowest P/E in 15+ years. 30% BELOW EPP structural floor ($351). FCF yield ~11%. EPS growing 19% YoY (Q1 FY2026). Firefly AI $400M direct revenue; 41M CC subscribers still adding. AI disruption fear is the thesis — but churn hasn't materialised. CEO Narayen transition (Mar 2026) adds uncertainty. Method B $572 (+134%). BUY."},
    "INTU": {"ticker": "INTU", "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 319.94, "date": "2026-05-24", "epp_gap_pct": -32.8, "ratio_b_fmt": "-0.34x",
              "sector_group": "Technology",
              "company": "Intuit Inc.", "sector": "SMB Financial Software · Tax · AI Financial Platform",
              "summary": "Down 61% from $813.70 ATH; trading at 13.4x FY2026E non-GAAP EPS — lowest in 15+ years. 33% BELOW EPP structural floor ($476). FCF yield ~7%. FY2026E EPS guidance RAISED to $23.82 on May 20 despite stock falling -20% on workforce cuts (17%, 3,000 jobs) + revenue decel fears. QB Online Ecosystem +19% YoY. IRS Direct File expanded to 25 states (W-2 only). Method B $783 (+145%). Deepest below-EPP in coverage. BUY."},
    "QCOM": {"ticker": "QCOM", "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 238.16, "date": "2026-05-22", "epp_gap_pct": 80.9,  "ratio_b_fmt": "2.23x",
              "sector_group": "Technology",
              "company": "QUALCOMM Incorporated", "sector": "Semiconductors · Smartphone Modems · Automotive ADAS · AI Edge",
              "summary": "Post-Q2 surge +11.6% to $238 (from ~$214); pre-surge was ◐ WATCHLIST. Apple modem exit drives EPS decline from $12.03 (FY2025) to $9.40E (FY2026) — 100% Apple, not business deterioration. Automotive annualised >$5B rate (+38% Q2, +50% guided Q3). Hyperscaler custom chip Dec 2026 tape-out. Method B $286 (+20%; FY2028E $13 × 22x). HOLD existing; add aggressively on pullback to $185-210."},
    "TXN":  {"ticker": "TXN",  "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 308.65, "date": "2026-05-24", "epp_gap_pct": 121.3, "ratio_b_fmt": "50.5x",
              "sector_group": "Technology",
              "company": "Texas Instruments Incorporated", "sector": "Analog Semiconductors · Embedded Processors · Industrial / Auto / AI",
              "summary": "World's best analog semi franchise up +58% YTD driven by AI/data center re-rating (+90% DC revenue YoY Q1 2026) and 300mm capex payoff story. But at 40× FY2026E EPS, the 2028–2030 recovery is already fully priced. Method B $312 is only +1.1% above current price. Avg analyst target ~$284 — BELOW current price. Capex cycle 83% done; SM1 Sherman began Dec 2025. ADD trigger: $200–220 pullback. BUY below $155."},
    "PANW": {"ticker": "PANW", "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 260.00, "date": "2026-05-24", "epp_gap_pct": 77.1,  "ratio_b_fmt": "5.66x",
              "sector_group": "Technology",
              "company": "Palo Alto Networks, Inc.", "sector": "Cybersecurity Platform · Zero Trust · AI-Powered SOC · Cloud Security",
              "summary": "#1 cybersecurity platform at ALL-TIME HIGH ($261.41) heading into Q3 FY2026 earnings June 2. NGS ARR $8.5B+ growing 53–54% YoY; 1,550 platform customers with 119% NRR; Rule of 60 + 40% FCF margin FY2028 target. But at 71× FY2026E EPS, Method B ($7.00 × 40× = $280) offers only +7.7% upside — asymmetric risk going into earnings. AVOID. WATCHLIST ~$185–195; ACCUMULATE ~$165."},
    "PLTR": {"ticker": "PLTR", "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 135.90, "date": "2026-05-24", "epp_gap_pct": 132.3, "ratio_b_fmt": "4.41x",
              "sector_group": "Technology",
              "company": "Palantir Technologies Inc.", "sector": "AI Operating System · Government Defense AI · Enterprise SaaS",
              "summary": "Extraordinary business — government AI OS with FedRAMP High classified monopoly + AIP bootcamp commercial flywheel (+133% US commercial YoY Q1 2026). Q1: Revenue $1.6B (+85%), adj op margin 60%, Rule of 40 = 145%. But at 104× FY2026E and 43× P/S, the franchise is priced for perfection and beyond. Method B $153 (+13%) at 55× FY2028E — still AVOID. Even the 52-wk LOW ($118.93) = 91× fwd EPS. WATCHLIST ~$85; BUY ~$50."},
    "INTC": {"ticker": "INTC", "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 119.00, "date": "2026-05-24", "epp_gap_pct": 395.8, "ratio_b_fmt": "N/A",
              "sector_group": "Technology",
              "company": "Intel Corporation", "sector": "Semiconductor IDM · x86 CPU · Intel Foundry (IFS) · AI PC",
              "summary": "One of the greatest mega-cap recoveries ever: +527% from 52-wk low $18.97 to $119. 18A in HVM (Oct 2025), yields +7%/month, Panther Lake H2 2026, Microsoft as foundry customer, $19B CHIPS Act backing. But at 99× FY2026E EPS, Method B (FY2028E $3.00 × 35× = $105) is BELOW current price. Avg analyst target $87.86 — 26% below current. Priced for perfection. WATCHLIST ~$70–80; ACCUMULATE ~$50."},
    "CAT":  {"ticker": "CAT",  "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 880.00, "date": "2026-05-25", "epp_gap_pct": 229.8, "ratio_b_fmt": "N/A",
              "sector_group": "Industrials",
              "company": "Caterpillar Inc.", "sector": "Heavy Equipment · Construction · Mining · Power & Energy",
              "summary": "+191% from 52-wk low $302; near ATH $931. Q1 2026: Rev $17.4B (+22%), adj EPS $5.54 (+30%), record backlog $63B, Power & Energy +41% (AI data centre turbines). World's best industrial franchise. BUT at 39× FY2026E adj EPS, Method B (FY2027E $27.73 × 22× = $610) is 31% BELOW current. Even at 35× = $970 (BULL scenario), only +10% upside. Analyst avg target $714-778 (-12-19%). WATCHLIST $620-660; ACCUMULATE $530-570."},
    "MRVL": {"ticker": "MRVL", "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 196.00, "date": "2026-05-25", "epp_gap_pct": 419.2, "ratio_b_fmt": "N/A",
              "sector_group": "Technology",
              "company": "Marvell Technology, Inc.", "sector": "Semiconductors · AI Custom Silicon (ASIC) · Optical Interconnect · Data Center",
              "summary": "+235% from 52-wk low $58.61; at ALL-TIME HIGH heading into Q1 FY2027 earnings May 27. Amazon Trainium custom silicon + optical interconnect franchise is real. FY2026 EPS $2.84 → FY2028E $5.44 (mgmt: 'well over $5'). But Method B ($5.44 × 35×) = $190 — already BELOW current price. At 36× FY2028E, the 3rd hyperscaler win is priced in. Analyst PT upgrades (Citi $215, Melius $220) racing to catch a stock that's run away. WATCHLIST $140-155; ACCUMULATE $120-135."},
    "DHR":  {"ticker": "DHR",  "signal": "◉ BUY",        "signal_short": "BUY",        "signal_color": "#4ade80",
              "price": 172.93,  "date": "2026-05-25", "epp_gap_pct": 33.0,  "ratio_b_fmt": "0.61x",
              "sector_group": "Healthcare",
              "company": "Danaher Corporation", "sector": "Life Sciences Tools · Bioprocessing (Cytiva/Pall) · Diagnostics (Cepheid) · DBS",
              "summary": "Bioprocessing supercycle confirmed: Cytiva equipment orders +30% YoY in Q1 2026 — first positive growth in 2 years. Destocking winter (2022-2024) is over. Down 29% from Jan 2026 high. At 20.5× FY2026E $8.45 — pricing near-zero recovery despite order data. DBS compounds at 15-20%/yr historically. Masimo ($9.9B, H2 2026) adds diagnostics. EPP $130 (20× × $6.50); Method B $243.75 (25× × FY2027E $9.75). Ratio B 0.61×. BUY $165-185; strong add $155-165."},
    "PFE":  {"ticker": "PFE",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 25.90,   "date": "2026-05-25", "epp_gap_pct": 30.8,  "ratio_b_fmt": "0.86x",
              "sector_group": "Healthcare",
              "company": "Pfizer Inc.", "sector": "Pharmaceuticals · Oncology (Seagen ADCs) · Vaccines · Obesity",
              "summary": "Post-COVID normalization complete; LOE cliff now the central risk: Eliquis 2026, Ibrance 2027 — ~$17-18B revenue at risk by 2028. Counter: Seagen ADCs +20% Q1 2026; $4B+ cost cuts by 2027; obesity (PF'3944 Phase IIb positive; 10 Phase III 2026). At 8.9× FY2026E — cheapest since FY2023 trough. 6.6% dividend yield paid while waiting. Ratio B 0.86×. ACCUMULATE $22-28; BUY on panic $20-23."},
    "ABT":  {"ticker": "ABT",  "signal": "◉ BUY",        "signal_short": "BUY",        "signal_color": "#4ade80",
              "price": 87.41,   "date": "2026-05-25", "epp_gap_pct": 36.6,  "ratio_b_fmt": "0.62x",
              "sector_group": "Healthcare",
              "company": "Abbott Laboratories", "sector": "MedTech · Diagnostics · Nutrition · CGM · Cologuard · Established Pharma",
              "summary": "World-class franchise at a litigation discount. FreeStyle Libre (global #1 CGM, 60%+ share, CMS Type 2 expansion) + Cologuard (#1 non-invasive colon cancer screen, $21B Exact Sciences acquired March 2026) at 16× FY2026E — trough multiple. Down 37% from Jun 2025 high on NEC baby formula MDL (782 cases; $70M April verdict). NEC is quantifiable and manageable ($1.5-2B settlement most likely). Dividend King 52+ years; 2.9% yield. Ratio B 0.62×. BUY $78-90; strong add $74-82 on August 2026 trial panic."},
    "TMO":  {"ticker": "TMO",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 448.28,  "date": "2026-05-25", "epp_gap_pct": 42.3,  "ratio_b_fmt": "0.85x",
              "sector_group": "Healthcare",
              "company": "Thermo Fisher Scientific Inc.", "sector": "Life Sciences Tools · Instruments · Bioproduction · CRO Services",
              "summary": "Dominant picks-and-shovels franchise for life sciences: #1 lab tools, instruments, CRO, and bioproduction globally. Off 30% from Jan 2026 high on NIH funding cuts ($500M) + tariffs ($400M) + China weakness. These are quantifiable policy headwinds, not structural impairments. Bioproduction (mRNA, gene therapy) +13% Q4 2025. FY2026 guidance raised: adj EPS $24.64-25.12 (+8-10%). At 18× FY2026E — low end of 5-yr range. Ratio B 0.85×. WATCHLIST $415-440; ACCUMULATE $370-395; BUY $310-340."},
    "MRK":  {"ticker": "MRK",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 122.55,  "date": "2026-05-25", "epp_gap_pct": 45.0,  "ratio_b_fmt": "1.91x",
              "sector_group": "Healthcare",
              "company": "Merck & Co., Inc.", "sector": "Pharmaceuticals · Oncology · Cardiovascular · Vaccines · Animal Health",
              "summary": "Keytruda $8.03B/qtr (+12% YoY) near peak, but US patent cliff arrives 2028 — $35B+ revenue at risk. Winrevair $525M (+88%); Qlex SC launch $128M. At 12.9× FY2027E $9.50, cheap on fwd earnings but cliff discount caps multiple. Ratio B 1.91×. WATCHLIST $100-108; ACCUMULATE $88-95; BUY $75-85."},
    "ABBV": {"ticker": "ABBV", "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",   "signal_color": "#60a5fa",
              "price": 215.70,  "date": "2026-05-25", "epp_gap_pct": 77.6,  "ratio_b_fmt": "1.30x",
              "sector_group": "Healthcare",
              "company": "AbbVie Inc.", "sector": "Pharmaceuticals · Immunology · Oncology · Neuroscience · Aesthetics",
              "summary": "Humira cliff largely absorbed — Skyrizi ($4.5B/qtr) + Rinvoq ($2.1B/qtr) already beat AbbVie's own 2027 combined target. CEO: 'we see upside to consensus.' Q1 2026: revenues $15.0B (+12.4%), adj EPS $2.65. FY2027E $16 adj EPS at 13.5× forward — one of cheapest big pharma. 3.2% dividend yield. Ratio B 1.30×. Emraclidine (schizophrenia) PhIII read-out 2026 is key binary catalyst. ACCUMULATE $178-188; BUY $140-155."},
    "JNJ":  {"ticker": "JNJ",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 234.34,  "date": "2026-05-25", "epp_gap_pct": 55.3,  "ratio_b_fmt": "1.86x",
              "sector_group": "Healthcare",
              "company": "Johnson & Johnson", "sector": "Pharmaceuticals · MedTech · Oncology · Immunology · Cardiovascular",
              "summary": "AAA-rated dividend king (62-yr streak); post-Kenvue pure pharma+MedTech. Darzalex+Carvykti+Rybrevant compounding; Abiomed heart pump monopoly; Q1 2026 revenue +9.9%. BUT: 67K+ talc MDL cases pending; $1.5B single verdict Dec 2025; 3rd bankruptcy rejected. 52-wk low $149 = EPP floor exactly. At 18.5× FY2027E, ratio_b 1.86× — HOLD/TRIM. Talc resolution unlocks re-rate to 24×. WATCHLIST $195-210; ACCUMULATE $165-180."},
    "UNH":  {"ticker": "UNH",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 387.30,  "date": "2026-05-25", "epp_gap_pct": 116.5, "ratio_b_fmt": "2.25x",
              "sector_group": "Healthcare",
              "company": "UnitedHealth Group Incorporated", "sector": "Managed Care · Medicare Advantage · Optum Health & Rx",
              "summary": "World's largest health insurer — post-crisis recovery at +65% from 52-wk low $234.60. 2025 crisis: Medicare Advantage cost explosion, CEO Witty resigned, guidance pulled, DOJ criminal + civil probe (MA billing fraud). Q1 2026: $111.7B revenue, adj EPS $7.23. Hemsley back. Franchise intact but DOJ is existential tail risk. At 16× FY2027E $24, ratio_b 2.25× — HOLD/TRIM. WATCHLIST $310-330; ACCUMULATE $260-280."},
    "LLY":  {"ticker": "LLY",  "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 1065.00, "date": "2026-05-25", "epp_gap_pct": 287.8, "ratio_b_fmt": "4.73x",
              "sector_group": "Healthcare",
              "company": "Eli Lilly and Company", "sector": "Pharmaceuticals · GLP-1 Obesity/Diabetes · Oncology · Neuroscience",
              "summary": "Best-in-class GLP-1 franchise (Mounjaro + Zepbound $12.8B Q1 2026; +56% YoY rev). Q1 2026: EPS $8.55 (+156% YoY); FY2026 guidance $35.50-37 non-GAAP. Pipeline: retatrutide (triple agonist, Phase 3 — potentially best-ever weight-loss drug), orforglipron (oral GLP-1), donanemab. Quality is undeniable. But at 29× FY2026E, Method B (FY2027E $44 × 28×) = $1,232 gives only +15.7% upside vs $790 EPP downside. Ratio B 4.73×. WATCHLIST $820-880; ACCUMULATE $680-740."},
    "PKN":  {"ticker": "PKN",  "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 144.50, "date": "2026-05-25", "epp_gap_pct": 151.7, "ratio_b_fmt": "~290x",
              "sector_group": "Energy",
              "company": "Orlen S.A.", "sector": "Integrated Energy · Oil Refining · Upstream Gas · Petrochemicals · Power",
              "summary": "Note: PLN-denominated stock (WSE/GPW). Near ATH PLN 146.98 (May 12, 2026) after +110% surge from 52-wk low PLN 69.20. Poland's largest company — Lotos + PGNiG + Energa mega-merger. FY2025 adj EPS PLN 9.57; EBITDA LIFO PLN 41.5B; dividend PLN 8/share (5.5% yield). BUT: Method B (FY2027E PLN 14.48 × 10×) = PLN 144.8 — AT current price. Avg analyst target PLN 120-127 (-12-17%). Stock has priced in its 2-year fair value. WATCHLIST PLN 105-115; ACCUMULATE PLN 90-100."},
    "SYK":  {"ticker": "SYK",  "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#4ade80",
              "price": 316.48,  "date": "2026-05-26", "epp_gap_pct": 31.9,  "ratio_b_fmt": "0.64x",
              "sector_group": "Healthcare",
              "company": "Stryker Corporation", "sector": "MedTech · Orthopedics (Mako Robotics) · MedSurg · Neurotechnology · Emergency Care",
              "summary": "Decade-long compounder disrupted by a one-time cyberattack (Iran-linked Handala, March 2026; 3-wk manufacturing shutdown; $310M Q1 miss). Business reality: FY2026 adj EPS guidance $14.90-$15.10 MAINTAINED. Mako robotics (3,000+ installs; <30% global TKA penetration) + LIFEPAK 35 hospital refresh + Inari Medical VTE ($500M, 25-30%/yr). At 21.1× FY2026E — lowest fwd P/E since COVID 2020. EPP $240 (24× × $10 stress EPS); 52-wk low $281 = 28.1× stress EPS. Order book held through outage; demand deferred not destroyed. Ratio B 0.64×. BUY $280-320; ACCUMULATE $320-360."},
    "BSX":  {"ticker": "BSX",  "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#4ade80",
              "price": 57.78,   "date": "2026-05-25", "epp_gap_pct": 11.1,  "ratio_b_fmt": "0.14x",
              "sector_group": "Healthcare",
              "company": "Boston Scientific Corporation", "sector": "MedTech · Cardiovascular · Electrophysiology (Farapulse) · WATCHMAN · Neurovascular",
              "summary": "Trading at the EPP floor ($52.00) after -47% drawdown from Dec 2025 high $109.50. The 52-wk low $52.52 = exactly 20.2× stress EPS — the market priced in permanent impairment. Business reality: revenue +11.6%, adj EPS +6.7%, guidance +9-11% in FY2026. Farapulse PFA $1B+ first year, +35% Q4 even with J&J Varipulse competition. WATCHMAN softness is unexplained but structural driver (AF + anticoagulant alternatives) is intact. Penumbra $14.5B (neurovascular/thrombectomy) adds optionality. Securities litigation manageable ($100-350M range). At 17.1× FY2026E — lowest fwd multiple in 10+ years. 31 analysts: Strong Buy; avg target $83.47. Ratio B 0.14×. BUY $52-65; ACCUMULATE $65-78."},
    "AMGN": {"ticker": "AMGN", "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 331.70,  "date": "2026-05-25", "epp_gap_pct": 58.0,  "ratio_b_fmt": "2.02x",
              "sector_group": "Healthcare",
              "company": "Amgen Inc.", "sector": "Biotechnology · Inflammation/Oncology · Rare Disease (Horizon) · Obesity Pipeline (MariTide)",
              "summary": "Waiting for MariTide — fairly priced while the clock ticks. EPS growing 9-13%/yr (FY2025 $19.84 → FY2026E $22.40); Q1 2026 EPS $5.15 (+13%), revenue $8.62B (+9%), guidance raised. Repatha +22%, Tepezza +24%. But $331.70 = 14.8× FY2026E — already reflecting EPS growth; MariTide Phase 3 (monthly dosing GLP-1) is option not value. Enbrel erosion (-13%) and Otezla LOE Feb 2028 are known headwinds. Horizon debt $28B overhang caps multiple. Ratio B 2.02×. 2.77% dividend while waiting. BUY $250-270; ACCUMULATE $270-295; WATCHLIST $295-330."},
    "ELV":  {"ticker": "ELV",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 392.52,  "date": "2026-05-26", "epp_gap_pct": 180.4, "ratio_b_fmt": "2.15x",
              "sector_group": "Healthcare",
              "company": "Elevance Health, Inc.", "sector": "Managed Care · Commercial · Medicaid (Anthem) · Medicare Advantage · Carelon",
              "summary": "Second-largest US health insurer recovering from simultaneous Medicaid + MA crisis. Stock fell 32% in 2025 to $271 low — the entry. Now +45% to $392. Q1 2026: adj EPS $12.58 (strong recovery); FY2026 guidance raised to ≥$26.75. Two headwinds: (1) Medicaid -1.75% margin trough (26+ state contracts; rate re-rates 2026-2027 are THE key driver); (2) CMS sanctions threatening MA new enrollment (high-teens member loss guided; $935M RADV accrual). Carelon (health services; $1.1B Q1 gain) is ELV's Optum analogue. At 14.7× FY2026E — historically cheap MCO. FY2027E ≥$28.84 (+12%). Ratio B 2.15×. HOLD; ACCUMULATE $310-345; TRIM above $430."},
    "VRTX": {"ticker": "VRTX", "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 433.00,  "date": "2026-05-26", "epp_gap_pct": 140.6, "ratio_b_fmt": "2.36x",
              "sector_group": "Healthcare",
              "company": "Vertex Pharmaceuticals", "sector": "Large-Cap Biopharma · CF Monopoly (TRIKAFTA/ALYFTREK) · Pain (JOURNAVX) · Kidney (Povetacicept)",
              "summary": "World's only CF treatment company — near-monopoly on 90% of CF patients ($13B+ revenue; patents 2037-38; no competitor before 2030). World-class compounder but fairly priced at $433 (24.3× FY2026E; -15% from $508 high). 52-wk low $362.50 was the entry (ratio_b ~1.0×). Now at 2.36×: HOLD. Three growth vectors: povetacicept IgAN (BLA filed H1 2026; -52% proteinuria in RAINIER), suzetrigine DPN (BTD; Phase 3 data 2027; $3B+ peak), T1D cell therapy (Phase 1/2; insulin independence data). EPP $180 = 20× stress EPS; 52-wk low was still 40× above EPP — the CF moat is extraordinary. Trim above $500; re-enter $370-395 or on pove IgAN approval."},
    "GILD": {"ticker": "GILD", "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 134.36,  "date": "2026-05-26", "epp_gap_pct": 144.3, "ratio_b_fmt": "2.17x",
              "sector_group": "Healthcare",
              "company": "Gilead Sciences, Inc.", "sector": "Large-Cap Biopharma · HIV (Biktarvy/Lenacapavir) · Oncology (Trodelvy/Yescarta) · Virology",
              "summary": "Dominant HIV franchise ($30B revenue; Biktarvy $12B+) at a lenacapavir inflection point. PURPOSE-1/2 trials showed 0 and ~0 HIV infections — potentially the biggest HIV prevention breakthrough since oral PrEP. Lenacapavir oral BIC combo (FDA Priority Review) could replace Biktarvy entirely. But stock +44% from $93 low to $134 (fair value); three 2026 acquisitions ($11.5B IPR&D: Arcellx myeloma CAR-T, Ouro HIV, Tubulis ADC) create GAAP loss in FY2026 and execution risk. At 15.5× FY2026E non-GAAP, lenacapavir optionality is partially priced in. Ratio B 2.17×. HOLD; ACCUMULATE $105-115; TRIM above $145; ADD on oral LEN/BIC approval."},
    "BMY":  {"ticker": "BMY",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 59.46,   "date": "2026-05-26", "epp_gap_pct": 88.8,  "ratio_b_fmt": "2.23x",
              "sector_group": "Healthcare",
              "company": "Bristol-Myers Squibb Company", "sector": "Large-Cap Pharma · Oncology (Opdivo/Opdualag) · Cardiovascular (Eliquis/Camzyos) · Haematology",
              "summary": "Managing two patent cliffs simultaneously — Revlimid (fully generic Jan 2026) and Eliquis (EU May 2026; US ~Apr 2028). Stock +39% from $42.52 low to near 52-wk high $62.89; optimal entry was below $50. Q1 2026: adj EPS $1.58 beat $1.43 (+10.5%); FY2026E $6.20 guided. Growth portfolio (Reblozyl $2B+, Camzyos $1B+, Cobenfy, Opdualag) bridging LOE. Key binary catalyst: milvexian (oral FXI) AF + stroke Phase 3 readouts mid-2026 — positive = 15-20% re-rate; failed = multiple stays compressed at 9-10×. Net debt $34B post-$10B paydown; 4.25% dividend (17 consecutive increases). Ratio B 2.23×. HOLD current; TRIM above $63; RE-ENTER below $50 or on milvexian data."},
    "MA":   {"ticker": "MA",   "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",  "signal_color": "#60a5fa",
              "price": 498.54,  "date": "2026-05-22", "epp_gap_pct": 74.3,  "ratio_b_fmt": "1.17x",
              "sector_group": "Finance",
              "company": "Mastercard Incorporated", "sector": "Payment Networks · Value-Added Services · Cross-Border Payments · Open Banking",
              "summary": "Visa's natural twin — same asset-light network, same ~50% operating margins, zero credit risk. But MA is cheaper (P/E 25.6× vs V 27.5×), growing faster (Q1 adj EPS +23% vs V +20%), and has no DOJ antitrust lawsuit. Q1 2026: revenue $8.4B (+16%), adj EPS $4.60 (+23%); Value-Added Services (cybersecurity, analytics, open banking) +18% = ~36% of revenue. 52-wk low $480.50 (Apr 2026) was ACCUMULATE at ratio_b ~0.99×; +4% to current $499. $5.7B returned in 4M (Q1+Apr). Key risk: UK interchange class action (~£14B claim). Method B $680 (+36%). Ratio B 1.17×. WATCHLIST; ACCUMULATE $420-480; BUY $345-375."},
    "V":    {"ticker": "V",    "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",  "signal_color": "#60a5fa",
              "price": 329.96,  "date": "2026-05-22", "epp_gap_pct": 87.5,  "ratio_b_fmt": "1.71x",
              "sector_group": "Finance",
              "company": "Visa Inc.", "sector": "Payment Networks · Digital Commerce Infrastructure · Cross-Border Payments",
              "summary": "World's largest payment network: 300B transactions/year, 14,500+ financial institutions, 175M+ merchant locations. Q2 FY2026: revenue $11.23B (+17% YoY, strongest since 2022), adj EPS $3.31 (+20%). FY2026 guidance raised to 'low double-digit to low teens' revenue growth. Agentic commerce: Trusted Agent Protocol + 16B tokens position Visa as THE AI payment infrastructure. 52-wk low $293.89 (Apr 1, 2026) was ACCUMULATE at ratio_b 0.93×; now +12% to $330 = WATCHLIST. DOJ antitrust (debit monopoly) is the key risk; behavioural remedy likely, not structural breakup. Tap-to-pay >80% globally; US ~70%. Method B $420 (+27%). Ratio B 1.71×. WATCHLIST; ACCUMULATE $285-315; BUY $255-275."},
    "JPM":  {"ticker": "JPM",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 307.40,  "date": "2026-05-26", "epp_gap_pct": 156.2, "ratio_b_fmt": "2.27x",
              "sector_group": "Finance",
              "company": "JPMorgan Chase & Co.", "sector": "Global Banking · Investment Banking · Commercial Banking · Asset & Wealth Management",
              "summary": "World's #1 bank by market cap (~$824B) and ROTCE leader (23% vs BAC 14%, WFC 15%). Q1 2026: record $16.5B net income, EPS $5.94 (+17%), IB fees +28%, markets +20%. CET1 14.3% fortress. BUT: at 2.83× TBV and 13.7× FY2026E EPS — peak-cycle valuation with peak-cycle ROTCE. NII guided $103B (trimmed from $104.5B); each 25bps Fed cut = ~$1.5-2B headwind. If ROTCE mean-reverts to 16% (mild recession), warranted P/TBV = 2.4× → implied $261 (-15%). Entry was 52-wk low $256 (2.35× TBV); now HOLD. Dimon flagged retirement 'a few years'; succession premium risk. Method B $390 (+27%). Ratio B 2.27×. HOLD; ACCUMULATE $240-270; BUY $195-220."},
    "AXP":  {"ticker": "AXP",  "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",  "signal_color": "#60a5fa",
              "price": 311.01,  "date": "2026-05-26", "epp_gap_pct": 146.8, "ratio_b_fmt": "1.60x",
              "sector_group": "Finance",
              "company": "American Express Company", "sector": "Closed-Loop Payment Network · Premium Card Issuing · Travel & Lifestyle Services",
              "summary": "The only closed-loop payment network: AXP owns both the network AND issues cards (unlike Visa/MA). Three engines: merchant discount revenue, net interest income, and $10B/yr net card fees (+18% FY2025; zero credit risk). ROE 35% Q1 2026; billed business $428B (+10%). DEFINING SIGNAL: Buffett sold ENTIRE Visa + Mastercard positions in Q1 2026 but HELD all 151.61M AXP shares — earns $576M/yr dividends. AXP cheapest payment network at 17.7× FW P/E (vs V 27.5×, MA 25.6×). 60%+ new card acquisitions = Millennials/Gen-Z — 20-30yr spending horizon ahead. 52-wk low $281.47 (Apr 2026) was ACCUMULATE at ratio_b 1.07×; +10.5% recovery to current WATCHLIST. Analyst avg PT $362-375 (+16-20%). Method B $426 (+37%). Ratio B 1.60×. WATCHLIST; ACCUMULATE $270-295; BUY $230-260."},
    "GS":   {"ticker": "GS",   "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 1000.00, "date": "2026-05-26", "epp_gap_pct": 263.6, "ratio_b_fmt": "6.25x",
              "sector_group": "Finance",
              "company": "The Goldman Sachs Group, Inc.", "sector": "Investment Banking · Global Markets (Trading) · Asset & Wealth Management",
              "summary": "World's premier IB franchise at ALL-TIME HIGH $1,000 — surged 4.9% on SpaceX IPO lead mandate. Q1 2026: EPS $17.55 (+24% YoY), ROTE 21.3% (2nd-highest quarterly revenue ever). The problem is not the business, it's the price. Gordon Growth trap: looks cheap at Q1 ROTE 21.3% (warranted P/TBV 3.46× = $1,176) but FY2025 full-year ROE 15% → warranted P/TBV 2.20× = $748 — BELOW current. Analyst avg PT $901 is 10% below current. IB cyclicality is extreme: FY2023 EPS $22.87 (-47% from FY2022) in one year. SpaceX lead = $200-400M fees; market added $14.7B to GS market cap on the announcement (35-75× the fee value). Method B $1,116 (+11.6%) vs BEAR $275 (-72.5%). Ratio B 6.25×. AVOID; revisit below $800; ACCUMULATE $500-650."},
    "WFC":  {"ticker": "WFC",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 76.33,   "date": "2026-05-26", "epp_gap_pct": 142.3, "ratio_b_fmt": "1.79x",
              "sector_group": "Finance",
              "company": "Wells Fargo & Company", "sector": "Consumer Banking · Commercial Banking · Corporate & Investment Banking · Wealth Management",
              "summary": "Third-largest US bank ($234B market cap) — the REFORM STORY now an EXECUTION STORY. Defining catalyst: asset cap REMOVED June 2025 after 7 years, unlocking balance sheet growth for the first time since the 2016 fake-accounts scandal. Q1 2026: EPS $1.60 (+15% YoY), NII $12.1B (+5%), ROTCE 14.5% (from 13.6% a year ago). Gordon Growth twist: WFC is the ONLY major bank trading below its warranted P/TBV at current ROTCE (1.77× vs warranted 2.10× = $90.36). But recession ROTCE 10% → warranted 1.20× → $51.64 (32% below current). NIM compression (2.47%, down from 2.60% YoY) is the key bear case — most rate-sensitive of big-4. 52-wk low $71.93 (Apr 2026 sell-off) was WATCHLIST at ratio_b 1.37×; now +6% = HOLD. Method B $101.40 (+33%). Ratio B 1.79×. HOLD; ACCUMULATE $60-72; BUY $45-55."},
    "SPGI": {"ticker": "SPGI", "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",  "signal_color": "#60a5fa",
              "price": 417.95,  "date": "2026-05-26", "epp_gap_pct": 109.0, "ratio_b_fmt": "1.51x",
              "sector_group": "Finance",
              "company": "S&P Global Inc.", "sector": "Financial Data & Analytics · Credit Ratings Duopoly · Indices (S&P 500) · Market Intelligence",
              "summary": "Regulated duopoly (S&P + Moody's = 80% global credit ratings) + S&P 500 index perpetual annuity (≥$10T AUM tracking; each index point ≈ $35M/yr licensing fees). IMMINENT CATALYST: Mobility Global (MBGL) spin-off July 1, 2026 — CARFAX + Polk spun as pure auto-data play; record date June 15. Post-spin SPGI becomes purer financial data/analytics business deserving 27-30× (vs 21.4× today). Q1 2026: adj EPS $4.97 (+14% beat), Ratings +13%, Indices +17%, adj margin 52% record. FY2026 guidance $19.40-$19.65 raised. At 21.4× FW vs Moody's 30× — SPGI at 29% discount to duopoly peer. Analyst avg PT $533-562 (+27-34%). Method B $562.50 (+35%). Ratio B 1.51×. WATCHLIST; ACCUMULATE $370-415 (post-MBGL-spin dislocation zone); BUY below $340."},
    "BLK":  {"ticker": "BLK",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 1073.15, "date": "2026-05-26", "epp_gap_pct": 125.5, "ratio_b_fmt": "2.05x",
              "sector_group": "Finance",
              "company": "BlackRock, Inc.", "sector": "Asset Management · Passive Investing (iShares) · Alternatives (GIP + HPS) · Aladdin Technology",
              "summary": "World's largest asset manager ($13.9T AUM) in strategic transformation: GIP ($170B infrastructure, Oct 2024) + HPS ($190B private credit, July 2025) pivot BLK from pure passive to top-5 alternatives platform. Q1 2026: adj EPS $12.53 (+10.9%), revenue $6.7B (+27%), NNA $135.9B, organic growth 13% (vs 3% Q1 2024). The business is excellent — the price is fairly valued. BASE scenario = FY2026E $54.29 × 20× = $1,086 ≈ current $1,073. 52-wk low $917.39 (Apr 2026) was ACCUMULATE at ratio_b 0.99×; +17% to current HOLD. Analyst avg PT $1,251-1,254 (+17%): bullish but implies only moderate upside. EPP $476 (17× × $28 trough). Method B $1,364 (+27.1%). Ratio B 2.05×. HOLD; ACCUMULATE $860-920 on next macro scare; BUY below $740."},
    "MS":   {"ticker": "MS",   "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 200.92,  "date": "2026-05-26", "epp_gap_pct": 204.4, "ratio_b_fmt": "3.64x",
              "sector_group": "Finance",
              "company": "Morgan Stanley", "sector": "Investment Banking · Global Markets (Trading) · Wealth Management (~$7T AUM) · Investment Management",
              "summary": "World-class IB+WM hybrid at ALL-TIME HIGH ($201.03 May 22, 2026). Q1 2026 exceptional: ROTCE 27.1% (record), EPS $3.43 (+13.6% beat), revenue $20.6B record — driven by tariff-volatility trading spike. The problem is not the business, it's the price. Gordon Growth trap: Q1 ROTCE 27.1% → warranted P/TBV 4.62× = $238 (looks cheap), but FY2025 normalized ROTCE 19.5% → warranted 3.10× = $160 (BELOW current). Analyst avg PT $176-190 — both BELOW current $200.92. IB cyclicality: FY2023 EPS $5.18 (-16%) in non-recessionary freeze. 52-wk low $123.88 (Apr 2025) was BUY at ratio_b 0.51×; now AVOID at ATH. Method B $238 (+18.5% = very limited upside vs EPP floor $66 = -67%). Ratio B 3.64×. AVOID; revisit below $155; ACCUMULATE $120-140."},
    "BAC":  {"ticker": "BAC",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 51.70,   "date": "2026-05-26", "epp_gap_pct": 187.2, "ratio_b_fmt": "2.17x",
              "sector_group": "Finance",
              "company": "Bank of America Corporation", "sector": "Consumer Banking · Global Markets & Investment Banking · NII Franchise · Wealth Management (MLWM)",
              "summary": "Second-largest US bank ($368B market cap) — dramatically improved since the GFC under CEO Moynihan. Q1 2026: EPS $1.11 (+25% YoY), NII $15.9B (+9%), trading best in 15 years, ROTCE 16%. Gordon Growth: at peak ROTCE 16%, warranted P/TBV is 2.4× → implied $69.55; but recession ROTCE 12% → warranted 1.6× → $46.37. DEFINING SIGNAL: Buffett/Berkshire sold entire ~1B share position at $35-45 (2024-2025) — his revealed fair value. Current $51.70 is +23% above Buffett's exit price. NII sensitivity ($2T deposits; most rate-sensitive major US bank) is the key risk: each 25bps cut → ~$1-1.5B NII headwind. Method B $67.20 (+30%). Ratio B 2.17×. HOLD; ACCUMULATE $38-47; BUY $26-32."},
    "BRK":  {"ticker": "BRK",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 485.95,  "date": "2026-05-26", "epp_gap_pct": 44.6,  "ratio_b_fmt": "1.09x",
              "sector_group": "Finance",
              "company": "Berkshire Hathaway (BRK.B)", "sector": "Diversified Conglomerate · Insurance (GEICO/BH Re) · Railroad (BNSF) · Utilities (BHE)",
              "summary": "World's largest conglomerate (~$1.05T market cap) with $397B cash — a record $184/B in liquid assets. Greg Abel's first quarter as CEO (Q1 2026): operating earnings $11.35B (+18% YoY); book value per B $337.15 (+11.1% YoY). GEICO turnaround complete (87.1% combined ratio). Ex-cash P/E = (485.95 − 184) / 21.05 = 14.35× — the actual business is cheap. Buffett buyback floor = 1.2× book ≈ $404/B provides structural downside protection. Primary risk: BHE PacifiCorp wildfire litigation ($20-30B worst case); Greg Abel's capital deployment track record is unproven at scale. Three insurance pillars (GEICO + BH Re + General Re) generate $176B float at essentially zero cost. Ratio B 1.09×. ACCUMULATE $455-495; BUY on pullback to $404-440 (1.2-1.3× book)."},
}

CORS = {
    "Access-Control-Allow-Origin":  "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}

_s3 = None

def s3():
    global _s3
    if _s3 is None:
        _s3 = boto3.client("s3")
    return _s3


def s3_key(ticker: str) -> str:
    return f"{S3_PREFIX}{ticker}.json"


def load_from_s3(ticker: str) -> dict | None:
    try:
        obj = s3().get_object(Bucket=S3_BUCKET, Key=s3_key(ticker))
        return json.loads(obj["Body"].read())
    except ClientError:
        return None


def save_to_s3(ticker: str, payload: dict):
    s3().put_object(
        Bucket=S3_BUCKET,
        Key=s3_key(ticker),
        Body=json.dumps(payload, ensure_ascii=False),
        ContentType="application/json",
    )


def run_model_fresh(ticker: str) -> str:
    fname = MODELS[ticker]
    path  = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        runpy.run_path(path, run_name="__main__")
    return buf.getvalue()


def get_report(ticker: str) -> dict:
    """Return report dict: try memory cache → S3 cache → run model."""
    if ticker in _cache:
        return _cache[ticker]

    cached = load_from_s3(ticker)
    if cached:
        _cache[ticker] = cached
        return cached

    return generate_and_save(ticker)


def generate_and_save(ticker: str) -> dict:
    """Run the model, extract parts, persist to S3, update memory cache."""
    output   = run_model_fresh(ticker)
    sections = extract_parts(output)
    payload  = {
        **SUMMARY[ticker],
        "ticker":       ticker,
        "report":       sections["full"],
        "part2":        sections["part2"],
        "part3":        sections["part3"],
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    save_to_s3(ticker, payload)
    _cache[ticker] = payload
    return payload


def extract_parts(full_output: str) -> dict:
    lines = full_output.split("\n")
    p2_start = p3_start = None
    for i, line in enumerate(lines):
        if "PART 2" in line and "ANALYST COMMENTARY" in line:
            p2_start = i
        elif "PART 3" in line and "NUMBERS & SIGNALS" in line:
            p3_start = i
    part2 = "\n".join(lines[p2_start:p3_start]).strip() if p2_start else ""
    part3 = "\n".join(lines[p3_start:]).strip()           if p3_start else ""
    return {"part2": part2, "part3": part3, "full": full_output}


def resp(status: int, body, content_type="application/json", extra_headers=None):
    h = {**CORS, "Content-Type": content_type}
    if extra_headers:
        h.update(extra_headers)
    if content_type == "application/json" and not isinstance(body, str):
        body = json.dumps(body, ensure_ascii=False)
    return {"statusCode": status, "headers": h, "body": body}


def refresh_all() -> dict:
    """Regenerate every model and persist to S3. Returns summary."""
    _cache.clear()
    results = {}
    for ticker in MODELS:
        try:
            generate_and_save(ticker)
            results[ticker] = "ok"
        except Exception as e:
            results[ticker] = f"error: {e}"
    return results


def lambda_handler(event, context):
    # EventBridge scheduled trigger
    if event.get("source") == "aws.events" or event.get("detail-type") == "Scheduled Event":
        results = refresh_all()
        print(f"Scheduled refresh complete: {results}")
        return {"statusCode": 200, "body": json.dumps(results)}

    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path   = event.get("rawPath", event.get("path", "/"))
    parts  = [p for p in path.strip("/").split("/") if p]

    if method == "OPTIONS":
        return resp(200, "")

    # POST /signals/refresh  →  regenerate all models now
    if method == "POST" and parts == ["signals", "refresh"]:
        results = refresh_all()
        return resp(200, {"refreshed": results, "timestamp": datetime.datetime.utcnow().isoformat() + "Z"})

    # GET /signals  →  summary list
    if parts == ["signals"]:
        return resp(200, {"signals": list(SUMMARY.values())})

    # GET /signals/{TICKER}  →  full JSON with report text
    if len(parts) == 2 and parts[0] == "signals":
        ticker = parts[1].upper()
        if ticker not in MODELS:
            return resp(404, {"error": f"unknown ticker: {ticker}"})
        data = get_report(ticker)
        return resp(200, data)

    # GET /signals/{TICKER}/raw  →  plain text
    if len(parts) == 3 and parts[0] == "signals" and parts[2] == "raw":
        ticker = parts[1].upper()
        if ticker not in MODELS:
            return resp(404, {"error": f"unknown ticker: {ticker}"})
        data = get_report(ticker)
        body = data.get("part2", "") + "\n\n" + data.get("part3", "")
        return resp(200, body, content_type="text/plain; charset=utf-8")

    return resp(404, {"error": "not found", "path": path})
