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
    "PGR":  "pgr_signal_model.py",
    "C":    "c_signal_model.py",
    "BX":   "bx_signal_model.py",
    "FISV": "fisv_signal_model.py",
    "SCHW": "schw_signal_model.py",
    "MRSH": "mrsh_signal_model.py",
    "CB":   "cb_signal_model.py",
    "KKR":  "kkr_signal_model.py",
    "PYPL": "pypl_signal_model.py",
    "LIN":  "lin_signal_model.py",
    "APD":  "apd_signal_model.py",
    "SHW":  "shw_signal_model.py",
    "PPG":  "ppg_signal_model.py",
    "ECL":  "ecl_signal_model.py",
    "FCX":  "fcx_signal_model.py",
    "NEM":  "nem_signal_model.py",
    "DNP":  "dnp_signal_model.py",
    "CTVA": "ctva_signal_model.py",
    "VMC":  "vmc_signal_model.py",
    "DOW":  "dow_signal_model.py",
    "LYB":  "lyb_signal_model.py",
    "META":  "meta_signal_model.py",
    "GOOGL": "googl_signal_model.py",
    "NFLX":  "nflx_signal_model.py",
    "KNEBV": "knebv_signal_model.py",
    "T":     "t_signal_model.py",
    "TTWO":  "ttwo_signal_model.py",
    "CMCSA": "cmcsa_signal_model.py",
    "TMUS":  "tmus_signal_model.py",
    "VZ":    "vz_signal_model.py",
    "EA":    "ea_signal_model.py",
    "CHTR":  "chtr_signal_model.py",
    "WBD":   "wbd_signal_model.py",
    "PSX":   "psx_signal_model.py",
    "OKE":   "oke_signal_model.py",
    "XOM":   "xom_signal_model.py",
    "COP":   "cop_signal_model.py",
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
    "PGR":  {"ticker": "PGR",  "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 199.51,  "date": "2026-05-22", "epp_gap_pct": 101.5, "ratio_b_fmt": "0.576x",
              "sector_group": "Finance",
              "company": "The Progressive Corporation", "sector": "Personal Auto Insurance · Commercial Lines · Property · Snapshot Telematics",
              "summary": "America's most precise auto insurer — Snapshot telematics (30M+ vehicles) gives PGR unmatched individual risk pricing vs demographics-only peers. Near 52-wk low ($192) while FY2025 EPS was record $19.23 and Q1 2026 $4.96 (+2.9% beat). The paradox: record earnings + 31% drawdown from ATH $289.82. Market is pricing CR normalization from 86.4% → 96% target (EPS would fall from $19 to ~$10). But even at analyst consensus 91-92% CR, EPS $16-17 at even 18× = $288-306 = +45-53% upside. At $199 the BEAR case (CR 95%+) is roughly priced in — downside only ~17% to $165; upside to $374 (+87.5%). Unique dividend: $13.50 variable paid Jan 2026 (6.77% yield for FY2025); annual variable formula based on profitability. FW P/E 12.2× is historically cheap for PGR (normally 20-28×). Analyst avg PT $231 (+16%). Ratio B 0.576×. BUY below $217; ACCUMULATE $217-244."},
    "C":    {"ticker": "C",    "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 126.20,  "date": "2026-05-27", "epp_gap_pct": 250.6, "ratio_b_fmt": "1.85x",
              "sector_group": "Finance",
              "company": "Citigroup Inc.", "sector": "Global Banking · Investment Banking · Markets · Treasury & Trade Solutions · Wealth Management",
              "summary": "The ultimate transformation story: Jane Fraser's 2024-2026 restructuring (5 business lines, 20K job cuts, $20B buyback) is delivering — Q1 2026 EPS $3.06 (annualised $12.24) beat by 16%, revenue $24.6B (+14%) was best in a decade, ROTCE 13.1% ALREADY exceeds the 10-11% FY2026 guidance. Cheapest US SIFI at 1.27× TBV ($99.01/sh); peers JPM/BAC trade 2-3× TBV. Gordon Growth cross-check: at Citi's own 10.5% FY2026 ROTCE target, fair value = 1.30× TBV = $128 ≈ current price — stock needs to EXCEED target (Q1 proves it can). Fraser's medium-term 14.5% ROTCE would warrant 2.10× TBV = $208. The stock has already run +63% in 12 months (from $73 BUY to current HOLD). EPP $36 (9× × $4 trough). Method B $175 (FY2027E $12.50 × 14×). Ratio B 1.85×. HOLD; re-enter ACCUMULATE $100-113 on any macro dislocation; deep BUY below $100 (near TBV)."},
    "BX":   {"ticker": "BX",   "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE",  "signal_color": "#f0b429",
              "price": 118.51,  "date": "2026-05-27", "epp_gap_pct": 88.1,  "ratio_b_fmt": "1.05x",
              "sector_group": "Finance",
              "company": "Blackstone Inc.", "sector": "Alternative Asset Management · Private Equity · Real Estate · Credit & Insurance · Infrastructure",
              "summary": "World's dominant alternative asset manager ($1.30T AUM, record Q1 2026) trading 38% below its $190 ATH — AUM at all-time high, stock in deep value. The paradox: AUM +12% YoY to record while stock -38% from peak. Q1 2026: DE $1.36/sh (+25% YoY), FRE $1.26/sh (+22%), inflows $69B. FY2025 was 'best 40-year results in history' (Schwarzman): DE $5.57/sh, inflows $240B. KEY: Fee-Related Earnings (FRE) LTM $4.90/sh is 100% contractual (10-year locked funds = no redemption risk unlike mutual funds). AI data centre + power infrastructure mega-cycle is the single largest PE deployment opportunity in BX history — data centre FRE growing >40% YoY. At $118.51 = 18× FY2026E DE vs 5-yr historical avg 27-30× = historically cheap multiple. Analyst avg PT $156-157 (+33%). EPP $63 (18× × $3.50 trough). Method B $172 (FY2027E $7.80 × 22×). Ratio B 1.05×. ACCUMULATE $110-120; BUY below $110 (near 52-wk low $101.73)."},
    "FISV": {"ticker": "FISV", "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 57.13,   "date": "2026-05-27", "epp_gap_pct": 27.0,  "ratio_b_fmt": "0.18x",
              "sector_group": "Finance",
              "company": "Fiserv, Inc.", "sector": "Financial Technology · Payment Processing · Core Banking · Merchant Acquiring (Clover)",
              "summary": "The classic 'fallen quality' setup: Fiserv — dominant US bank-processing infrastructure ($21B revenue, 2,500 bank/CU contracts) + Clover (50M SMB merchants) — crashed 76% from its $237 ATH after a 44% single-session collapse on Oct 29, 2025. Trigger: Argentina peso devaluation wiped out float income from LatAm operations; Merchant Solutions margin fell from 34% to 26%. Management cut adj EPS guidance from $10.15E → $8.64 actual FY2025. BUT: new leadership (CFO Paul Todd ex-Global Payments, co-presidents Dec 2025), Q1 2026 beat 13% ($1.79 vs $1.58E), guidance reaffirmed $8.00-8.30. Core Financial Solutions (50% revenue, 40% margin, multi-year contracts) was NEVER impaired — it's growing 2-3%. At 7× FW earnings, stock is priced for permanent Argentina destruction; even modest recovery to 14× on FY2027E $9.00 = $126 (+120%). Analyst avg PT $70 (+23%). EPP $45 (10× × $4.50). Method B $126 (FY2027E $9.00 × 14×). Ratio B 0.18×. BUY. Watch Q2 2026 organic growth — first clean Argentina comp."},
    "SCHW": {"ticker": "SCHW", "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE",  "signal_color": "#f0b429",
              "price": 90.21,   "date": "2026-05-27", "epp_gap_pct": 140.6, "ratio_b_fmt": "0.88x",
              "sector_group": "Finance",
              "company": "The Charles Schwab Corporation", "sector": "Retail Brokerage · Wealth Management · Banking · Asset Management",
              "summary": "Schwab has resolved BOTH crises that depressed earnings for three years. (1) Cash sorting: $200B+ of client cash moved to money market funds 2022-2024 crushing NIM to 1.75% trough — now fully stabilised; NIM recovered to 2.88% Q1 2026 (+35bps YoY) with 12bps more to go as FHLB debt ($80B+ repaid) rolls off. (2) TD Ameritrade integration: 100% complete end 2025; $2B annual synergies fully realised. Q1 2026 was the first clean quarter showing the combined benefit: adj EPS $1.43 (+38% YoY, record), revenue $6.5B (+16%), net income $2.5B (+30%). Record NNA $519B FY2025 (+42%) → $11.77T client assets (+19%). 2026 guidance $5.70-5.80, tracking above after Q1 beat. At $90 = 15.4× FY2026E — near the empirical floor multiple (SVB panic 2023 = ~15×). FY2027E $6.80 at 22× = $150 (+66%). Analyst avg PT $113-116 (+25%). EPP $37.50 (15× × $2.50). Ratio B 0.88×. ACCUMULATE. BUY below $86 (just $4 from current)."},
    "MRSH": {"ticker": "MRSH", "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 164.11,  "date": "2026-05-27", "epp_gap_pct": 30.2,  "ratio_b_fmt": "0.37x",
              "sector_group": "Finance",
              "company": "Marsh & McLennan Companies, Inc.", "sector": "Insurance Brokerage & Risk Advisory · Reinsurance Broking · HR Consulting · Management Consulting",
              "summary": "Marsh McLennan (rebranded MMC→MRSH Jan 2026) is the world's #1 insurance broker + Guy Carpenter (#2 reinsurance broker) + Mercer (#1 HR consulting) + Oliver Wyman (elite mgmt consulting). 18 consecutive years of margin expansion; targeting the 19th in 2026. NO underwriting risk — pure fee/commission model; insurers bear the risk. $27B revenue, $4.5B+ FCF, EPS compounding at 8-10%/yr. At $164, the stock is 31% below its $235.78 ATH and trading at 15.5× FY2026E adj EPS — near COVID-crash multiples — despite zero business impairment. Q1 2026: adj EPS $3.29 (+8% YoY), underlying revenue +4%, Risk & Insurance margin 38.3%, Consulting margin 21.6%. FY2025: adj EPS $9.75 (+9%), 18th consecutive margin expansion. Peers Aon (~23-24× FW EPS) and Gallagher (~30-35×) trade at 50-100% premiums. FY2027E $11.60 at 23× = $267 (+63%). Analyst avg PT $202 (+23%; 9 Buy / 1 Sell). EPP $126 (18× × $7.00 trough). Ratio B 0.37×. BUY. Double compounder: multiple re-rating 15.5×→22× + EPS growth 9-10%/yr = $200-267 over 2 years."},
    "CB":   {"ticker": "CB",   "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE",  "signal_color": "#f0b429",
              "price": 328.75,  "date": "2026-05-27", "epp_gap_pct": 58.1,  "ratio_b_fmt": "0.80x",
              "sector_group": "Finance",
              "company": "Chubb Limited", "sector": "P&C Insurance · Life Insurance · Global Commercial Insurance · High-Net-Worth Personal Lines",
              "summary": "Chubb is the world's largest publicly-traded P&C insurer (NPW $51B+; 54 countries) at COVID-crash multiples. At $328.75 = 12.2× FY2026E core operating EPS — near the lowest multiple in 15 years — despite record FY2025 results ($24.79 core EPS, +10%; 'best year in company history'), a record Q4 2025 combined ratio of 81.2%, and CEO Greenberg guiding double-digit EPS growth in 2026. Warren Buffett's Berkshire Hathaway holds 8.78% ($11.2B; 8th largest Berkshire holding) and was actively adding in Q3/Q4 2025 at $270-325 — implying intrinsic value well above $370+. $7.5B buyback authorized at <12× EPS = massive accretion; 5.2% dividend increase. Q1 2026 missed by 12% (spring cats) but guidance intact. FY2027E $30 at 16× = $480 (+46%). Buffett's view implies $400-570. EPP $208 (13× × $16 trough). Ratio B 0.80×. ACCUMULATE. BUY below $325. Dual compounder: 10% EPS growth + 3.5% buyback yield + potential multiple re-rating 12×→16×."},
    "KKR":  {"ticker": "KKR",  "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 94.19,   "date": "2026-05-27", "epp_gap_pct": 49.5,  "ratio_b_fmt": "0.37x",
              "sector_group": "Finance",
              "company": "KKR & Co. Inc.", "sector": "Alternative Asset Management · Private Equity · Credit · Infrastructure · Insurance (Global Atlantic)",
              "summary": "KKR — founder of modern PE (1976) — is trading at 11.6× FY2027E distributable earnings while every business metric is at all-time highs: AUM $758B (+14% YoY), FPAUM $615B (+17%), $129B raised FY2025, $120B dry powder. Down 39% from $153.87 Nov 2025 high; market extrapolating deal-market distress into perpetuity. The FRE floor ($4.13/share, +23% YoY in Q1 2026) is secured by $615B of LOCKED-UP capital that cannot redeem — in 2009, KKR's fees did not stop. Global Atlantic ($219B insurance AUM) adds permanent capital growing 15%/yr. At $94: market cap/AUM ratio = 11.2% — historically anomalous (BX at trough was 12-15%). The market is pricing $0 for $120B dry powder + future carry from $95B deployed in FY2025 at attractive prices. FY2026E $6.77 (mgmt guides $7+); FY2027E $8.13. EPP $63 (18× × $3.50 FRE trough). Ratio B 0.37×. BUY. Target: $130-179 (+38-90%)."},
    "PYPL": {"ticker": "PYPL", "signal": "◉ BUY",        "signal_short": "BUY",         "signal_color": "#22c55e",
              "price": 44.16,   "date": "2026-05-27", "epp_gap_pct": 26.2,  "ratio_b_fmt": "0.24x",
              "sector_group": "Finance",
              "company": "PayPal Holdings, Inc.", "sector": "Digital Payments · Peer-to-Peer (Venmo) · Commerce Platform · BNPL · Fastlane",
              "summary": "PayPal at $44.16 = 8.1× FY2026E non-GAAP EPS and 13-15% FCF yield — the cheapest valuation in PYPL's history as a public company, 86% below the $309 ATH (July 2021). The valuation case is entirely about the buyback flywheel: $6B/yr in buybacks (~15% of market cap annually) at 8× earnings compounds EPS to ~$8-9 by 2029 even with zero revenue growth. Venmo (90M+ US accounts; TPV +14% for 6th consecutive double-digit quarter; Pay with Venmo +23%) is deeply undermonetised at 0.9% take rate vs. 2.2% PayPal branded — the $4.3B annual gap represents real optionality. Bears are right: branded checkout losing share to Apple Pay/Stripe; Q1 2026 transaction margin flat; GAAP EPS fell -6% vs non-GAAP +1%. This is a FCF/buyback BUY, not a high-quality franchise BUY — conviction comes from the capital return math, not the business momentum. Analyst avg PT $55-58. EPP $35 (10× × $3.50 trough). Ratio B 0.24×. BUY below $56."},
    "LIN":  {"ticker": "LIN",  "signal": "✕ AVOID",      "signal_short": "AVOID",       "signal_color": "#f87171",
              "price": 516.00,  "date": "2026-05-27", "epp_gap_pct": 80.4,  "ratio_b_fmt": "3.65x",
              "sector_group": "Industrials",
              "company": "Linde plc", "sector": "Industrial Gases · Hydrogen (Clean Energy) · Semiconductor Specialty Gases · Take-or-Pay Contracts",
              "summary": "Linde is the world's largest industrial gas company — an oligopolist alongside Air Products and Air Liquide controlling ~75% of global supply. The business is structurally exceptional: on-site ASUs built at customer facilities cannot be moved (zero churn); 10–20 year take-or-pay contracts guarantee revenue regardless of volume; 30% operating margins; $10B clean energy backlog ($2.5–3B starting 2026); AI semiconductor gas demand accelerating. Q1 2026: adj EPS $4.33 (+10%), revenue $8.78B (+8%), op margin 30.0%. FY2026 guidance $17.40–$17.90. The problem is entirely the price: $516 = 29× FY2026E adj EPS, near the $521.28 ATH (May 2026). Method B (FY2027E $19.30 × 30× = $579) implies only +12% in 2 years from the BULL scenario. The BASE case ($480) is BELOW the current price — the market has already priced in clean energy + AI tailwinds. Analyst avg PT $541–553 = only 5–7% upside. Bears don't need deterioration — just multiple compression from 29× to 25× brings the stock to ~$440. The April 2026 tariff-panic low of $387.78 was a BUY at ratio_b 0.53×. EPP $286 (22× × $13 trough). Ratio B 3.65×. AVOID. ACCUMULATE $412–440. BUY below $412."},
    "APD":  {"ticker": "APD",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE",  "signal_color": "#f0b429",
              "price": 290.00,  "date": "2026-05-27", "epp_gap_pct": 38.1,  "ratio_b_fmt": "1.00x",
              "sector_group": "Industrials",
              "company": "Air Products and Chemicals, Inc.", "sector": "Industrial Gases · Hydrogen (NEOM Green H2 + Louisiana Blue H2) · Take-or-Pay · Dividend King",
              "summary": "Air Products at $290 = 22× FY2026E adjusted EPS — the same industrial gas oligopoly moat as Linde (take-or-pay contracts, on-site ASUs, zero customer churn, ~75% global market with LIN/Air Liquide) but at a 7-turn PE discount because of uncertainty around two mega-projects: NEOM Green Hydrogen (>90% complete; 2.2GW; commercial 2027; Yara distribution deal 'anticipated' H1 2026) and Louisiana Blue Hydrogen ($8-9B; FID expected mid-2026; online 2030; US IRA $3/kg credit makes economics compelling). New CEO Eduardo Menezes (ex-Linde EVP EMEA, appointed Feb 2025) is doing the right things: exited 3 risky US projects, raised FY2026 guidance twice to $13.00-$13.25 (+9%), pursuing Yara distribution deal. 44 consecutive annual dividend increases (Dividend King; $7.24/yr = 2.5% yield). Q2 FY2026: adj EPS $3.20 (+19% YoY). At $290, NEOM + Louisiana are essentially free call options — core gas alone is worth ~$286-295 at 22× FY2027 core EPS. If both H2 projects confirm (Yara deal + Louisiana FID), the BULL scenario ($370) opens up. EPP $210 (20× × $10.50 trough). Ratio B 1.00×. ACCUMULATE. BUY below $279."},
    "SHW":  {"ticker": "SHW",  "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",   "signal_color": "#60a5fa",
              "price": 316.00,  "date": "2026-05-27", "epp_gap_pct": 79.5,  "ratio_b_fmt": "1.52x",
              "sector_group": "Materials",
              "company": "The Sherwin-Williams Company", "sector": "Architectural Coatings · Professional Contractors · Paint Stores (4,900+) · Industrial & Performance Coatings",
              "summary": "Sherwin-Williams at $316 = 27× FY2026E adjusted EPS — the world's largest paint company and a quasi-monopoly on professional architectural coatings: 4,900+ company-owned stores in the Americas create distribution density no competitor can match. Professional painters don't switch because they've invested years in SHW's color formulas, tinting systems, and contractor loyalty tiers (up to 40% volume discounts). 47 consecutive annual dividend increases. The business is excellent — the current challenge is housing: high mortgage rates suppress existing home sales (the biggest repaint trigger) and FY2026 guidance is only +2.4% adj EPS growth. Q1 2026 was encouraging: adj EPS $2.35 (+4.4%), revenue $5.67B (+6.8%), record Q1 EBITDA $998M (+8.8%). The aging US housing stock (avg 42 years) and eventual rate normalisation are powerful multi-year tailwinds — every year of deferred painting creates future demand. April 2026 tariff-panic low $294.32 was ACCUMULATE (ratio_b 1.04×); current $316 is fairly valued in WATCHLIST. Analyst avg PT $380-385 requires housing recovery to materialise. EPP $176 (22× × $8.00 trough). Ratio B 1.52×. WATCHLIST. ACCUMULATE below $298. BUY below $275."},
    "PPG":  {"ticker": "PPG",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 108.50,  "date": "2026-05-31", "epp_gap_pct": 13.0,  "ratio_b_fmt": "0.93x",
              "sector_group": "Materials",
              "company": "PPG Industries, Inc.", "sector": "Paints & Coatings · Performance Coatings · Industrial Coatings · NYSE: PPG",
              "summary": "Global coatings leader at 49th pct of 52W range ($86–$132). Three converging signals: Boeing 737 Max at 40/month (BULL) + raw material basket −4% YoY (BULL) + restructuring $165M delivered (BULL). China architectural −6% is the structural drag (~15% of rev). Segment margin recovery bridge: +$560M incremental OI at through-cycle targets (15%→18.5% Performance; 11%→14.5% Industrial) = +$1.86/EPS = +$26/share at 14×. EPP floor $96 (+13% gap). Conservative 2yr: −5.2% — stock prices BASE recovery. 54-yr Dividend Aristocrat (yield 2.5%) provides income floor. Adj composite 2.46 vs market 2.49 — FAIRLY VALUED. Ratio B 0.93×. ACCUMULATE $88–117; BUY below $96 (EPP zone). Catalyst: Boeing 42/month → BULL upgrade."},
    "FCX":  {"ticker": "FCX",  "signal": "▷ HOLD/TRIM",  "signal_short": "HOLD",        "signal_color": "#a78bfa",
              "price": 63.63,   "date": "2026-05-28", "epp_gap_pct": 324.2,  "ratio_b_fmt": "2.28x",
              "sector_group": "Materials",
              "company": "Freeport-McMoRan Inc.", "sector": "Copper Mining · Gold Byproduct · Grasberg (Indonesia) · Americas Operations · US Tariff Beneficiary",
              "summary": "World's largest publicly traded copper producer at $63.63 — near its 52-wk high of $70.97 as copper hits $6/lb all-time highs driven by AI data centre buildout, EV electrification, and grid investment. Two major tailwinds: US 50% copper import tariff creates a 28% COMEX-LME premium adding ~$1.6B/yr to FCX's Americas profits; and Grasberg Block Cave (Indonesia) recovery progressing toward full capacity end-2027 (1.6B lbs Cu + 1.3M oz Au/yr = EPS step-change from ~$2.32 to $5-7+). Q1 2026: adj EPS $0.57 (+21% beat); Americas operating income 2.5× higher YoY compensating for Grasberg's 82M lb recovery quarter. Balance sheet transformed: net debt $2.3B vs $20B in 2016; $8.7B operating CF at $6/lb; $2.9B buyback authorized. But the stock has priced most of it: Method B ($3.86 × 22× = $85) is only 34% above current; analyst avg PT $70-72 is nearly there already. 52-wk low $35.15 was the BUY (ratio_b 0.40×). EPP $15 (20× × $0.75 trough). Ratio B 2.28×. HOLD/TRIM. Re-enter WATCHLIST $52-60; ACCUMULATE $45-52; BUY below $45."},
    "ECL":  {"ticker": "ECL",  "signal": "◐ WATCHLIST",  "signal_short": "WATCHLIST",   "signal_color": "#60a5fa",
              "price": 254.00,  "date": "2026-05-27", "epp_gap_pct": 130.9,  "ratio_b_fmt": "1.24x",
              "sector_group": "Materials",
              "company": "Ecolab Inc.", "sector": "Water Treatment · Hygiene & Sanitation · Pest Elimination · Life Sciences · Data Center Cooling (CoolIT)",
              "summary": "Ecolab at $254 = 30× FY2026E adjusted EPS — world leader in water, hygiene, and infection prevention. 45,000+ field reps visit 3M+ customer locations daily; once integrated into Nalco One digital water platform, switching = years of re-implementation. Non-discretionary compliance demand (food safety, water treatment, sterilization regulations). FY2025 adj EPS $7.53 (+13%); FY2026 guidance $8.43-$8.63 (+13%); Q1 2026 adj EPS $1.70 (+13%), record EBITDA. March 2026: CoolIT acquisition ($4.75B; AI data center liquid cooling; ~$550M revenue, growing fast) extends ECL's thermal/water management into the highest-growth infrastructure segment. CoolIT adds $4.75B debt (EPS dilutive year 1) but positions ECL as water and cooling solutions for AI data centers — multi-decade TAM. 34 consecutive annual dividend increases. Near 52-wk low $243 — UBS upgraded to Buy May 20, 2026. EPP $110 (22× × $5.00 trough). Ratio B 1.24×. WATCHLIST. ACCUMULATE below $244. BUY below $215."},
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
    "NEM":  {"ticker": "NEM",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 50.00,   "date": "2026-05-28", "epp_gap_pct": 39.0,  "ratio_b_fmt": "0.97x",
              "sector_group": "Basic Resources",
              "company": "Newmont Corporation",        "sector": "Gold Mining · Precious Metals · Copper Byproduct · Newcrest Acquired",
              "summary": "World's largest gold miner at gold ATH ($3,300/oz). Proxy composite 2.90 (BULL) vs market-implied 2.15 (BASE): market prices gold mean-reversion; signals show CB de-dollarisation demand, weak USD, and record ETF inflows. $0.40 EPS per +$100/oz gold = high operating leverage. EPP floor $36 (+39% cushion; 8× trough P/E). Conservative case flat; bull-case proxy EV $87 (+74%). Bear EPS goes negative at $1,800 gold. ACCUMULATE on dips; requires gold-continuation thesis."},
    "VMC":  {"ticker": "VMC",  "signal": "◐ WATCHLIST", "signal_short": "WATCHLIST", "signal_color": "#60a5fa",
              "price": 268.94,  "date": "2026-05-28", "epp_gap_pct": 92.0,  "ratio_b_fmt": "1.59x",
              "sector_group": "Basic Resources",
              "company": "Vulcan Materials Company", "sector": "Construction Aggregates · Asphalt · Concrete · NYSE: VMC",
              "summary": "World's largest aggregates producer at the 21st pct of its 52-wk range ($252–$331): -18.8% from high after a Q1 2026 beat (+20.5% adj EPS, +5% volumes). Investor Day $20/ton cash GP target on 265M tons = $5.3B cash GP vs $2.6B today; every $1/ton improvement = $31/share EV at 15× EBITDA. IIJA still flowing (accelerating pre-Sept 2026 cliff); data centre construction boom (70%+ of 600M+ sq ft within 30 miles of VMC facility). FY2026E adj EPS $9.30 (+19% YoY); adj EBITDA $2.4–2.6B. WATCHLIST: adj composite 2.85 vs market-implied 2.71 (FAIRLY VALUED); Ratio B 1.59×. At $269 the conservative 2yr return is only +4.4%. Key risk: IIJA reauthorisation cliff September 2026. ACCUMULATE $240–252; BUY below $232."},
    "CTVA": {"ticker": "CTVA", "signal": "◐ WATCHLIST", "signal_short": "WATCHLIST", "signal_color": "#60a5fa",
              "price": 82.21,   "date": "2026-05-28", "epp_gap_pct": 64.0,  "ratio_b_fmt": "1.27x",
              "sector_group": "Basic Resources",
              "company": "Corteva, Inc.", "sector": "Agricultural Sciences · Seeds (Pioneer) · Crop Protection · NYSE: CTVA",
              "summary": "Leading ag-input duopolist: Pioneer seeds + Corteva CP. FY2025 op EPS $3.34 (+30% YoY); Q1 2026 EPS $1.50 (+33%, +28% beat). Planned Seed/CP separation Q4 2026 — SOTP $84/share at base multiples ($104 bull, $63 bear). Stock near 52-week high ($82 vs $86 ATH). DOJ antitrust trial October 2026 is the binary event risk: loyalty program ruling could force CP distribution restructure → generic flood. Brazil soy trait penetration entering double digits — multi-year royalty expansion runway. Enlist E3 at 65% US soybean acres. WATCHLIST: adj. composite 2.37 vs market-implied 2.50 (FAIRLY VALUED); Ratio B 1.27×. At $82 the conservative 2yr return is only +1.6% (breakeven). Entry zone: $68–72 on DOJ dip or commodity weakness. EPP floor $50 (+64% gap)."},
    "DOW":  {"ticker": "DOW",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 34.52,   "date": "2026-05-29", "epp_gap_pct": 147.0, "ratio_b_fmt": "0.95x",
              "sector_group": "Basic Resources",
              "company": "Dow Inc.", "sector": "Commodity Chemicals · Polyethylene · Polyurethanes · Silicones · NYSE: DOW",
              "summary": "Dow at the trough — EPS negative FY2025, dividend cut 50% to $1.40/yr, $13.1B net debt. Yet two structural advantages: NA ethane feedstock moat ($1,200/MT advantage vs naphtha; highest in history due to Middle East supply shock) + Transform to Outperform $2B EBITDA target by 2027. EPP floor $14 (EV/EBITDA framework: $3.3B × 7× less $13.1B debt). Current $34.52 = 148% premium to EPP — market pricing mid-cycle recovery. Decisive test: Q2 2026 EBITDA (~$2B guided vs Q1 $873M). If Q2 delivers: upgrade to BUY. If Q2 misses: re-evaluate at $26–28. EBITDA recovery path: $3.3B trough → $4.5B mid-cycle consensus → $5.3B full Transform → $6.3B Path2Zero. Ratio B 0.95× (56.5% downside / 59.3% upside to BULL). Adj composite 2.56 vs market-implied 1.80 — UNDERVALUED by signals, but conservative 2yr return -13.2% warns stock already prices recovery. ACCUMULATE $30–35; BUY below $28. Size small until Q2 confirms."},
    "LYB":  {"ticker": "LYB",  "signal": "◐ WATCHLIST", "signal_short": "WATCHLIST", "signal_color": "#60a5fa",
              "price": 72.50,   "date": "2026-05-31", "epp_gap_pct": 272.0, "ratio_b_fmt": "1.46x",
              "sector_group": "Basic Resources",
              "company": "LyondellBasell Industries N.V.", "sector": "Commodity Chemicals · Polypropylene · PO/Styrene · Technology Licensing · NYSE: LYB",
              "summary": "LYB at the trough — EBITDA $2.7B (FY2025 actual), FCF deficit ~$380M vs $1.40B annual dividend burden. Dividend yield 6.2% is attractive but requires EBITDA ≥$3.5B to be FCF-covered. EPP floor $19.5/share (trough EV/EBITDA: $2.7B × 5.5× less $8.8B net debt / 310M shares). Current $72.50 prices in BULL ($5.5B EBITDA × 7.0× EV) — that is the risk. Tech licensing moat (Spherizone/Lupotech IP, 200+ global plants, $505M/yr revenue) provides structural floor. PP-propylene spread $145/MT (BASE), China capacity +3MT/yr (BASE), European output +0.5% (BASE) — all signals cyclically depressed. VEP + Houston exit delivering $430M annualised savings (BULL threshold $450M). Only BULL ($105) and XBULL ($155) scenarios justify current entry. Conservative 2yr: $3.5B EBITDA × 6.0× → $41/shr + $9.04 dividends = $50 → -31% total return. Mid-cycle BASE ($4.0B × 6.5×) = $55/shr — still below today's price. Adj. composite 2.06 vs market-implied 2.68 → OVERVALUED by 0.62 pts. Ratio B 1.46× (WATCHLIST). Key upgrade trigger: PP spread ≥$200/MT or China capacity cancellations confirm peak. WATCHLIST $62–85 | ACCUMULATE $58–67 | BUY below $55 | Size small — dividend at risk below $3.5B EBITDA."},
    "NFLX":  {"ticker": "NFLX",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
               "price": 850.00,  "date": "2026-05-31", "epp_gap_pct": 28.8, "ratio_b_fmt": "0.89x",
               "sector_group": "Technology",
               "company": "Netflix, Inc.", "sector": "Streaming · Ad-Supported Tier · Live Events · Gaming · NASDAQ: NFLX",
               "summary": "Netflix FAIRLY VALUED with ACCUMULATE asymmetry — Ratio B 0.89× (57.6% downside / 64.7% upside). Proxy 2.25, SCA +0.16 → adj 2.41 ≈ market 2.36: model broadly agrees with pricing. ARM +10% YoY = BULL (price increases + ad-tier revenue lift). Ad tier flywheel: 70M MAU × $42 ARPU = $2.94B/yr at 75% incremental margin = $4.07/EPS — still tiny but compounding. BULL ($1,400): 160M ad MAU × $80 ARPU = $12.8B rev → $17.72/EPS from ads alone + $22 subscription EPS ≈ $40 total at 35× = $1,400. Every 10M new ad MAU = +$0.58/EPS = +$17/share; every $10/yr ARPU uplift = +$0.97/EPS = +$29/share. Conservative 2yr (EPS $33 × 24× = $792) = −6.8%; BUY trigger below $750. BEAR ($360): Disney bundling wins + EU targeting ban + margin reversal → EPS $18 × 20× = $360 (−58%). EPP $660 (+29% gap); FY2027E EPP ~$770 as earnings grow. No dividend — all return via ~$400M/qtr buyback (~2%/yr yield). Watch: ad MAU ≥90M → BULL upgrade; ARM ≥12% → upgrade. ACCUMULATE $660–850 | BUY below $750."},
    "GOOGL": {"ticker": "GOOGL", "signal": "◉ BUY",       "signal_short": "BUY",       "signal_color": "#4ade80",
               "price": 172.00,  "date": "2026-05-31", "epp_gap_pct": 17.0,  "ratio_b_fmt": "0.64x",
               "sector_group": "Technology",
               "company": "Alphabet Inc.", "sector": "Google Search · YouTube · Google Cloud · AI Infrastructure · NASDAQ: GOOGL",
               "summary": "Alphabet at ◉ BUY — cheapest it has been on forward P/E in 4 years (~16.4× FY2026E). Ratio B 0.64× (53.5% downside / 83.1% upside): Cloud + YouTube asymmetry swamps the bear case. Proxy 2.35, SCA +0.14 → adj 2.49 vs market 2.16 → UNDERVALUED by 0.33 pts. Cloud growing +29% YoY (BULL signal): every 1% of additional cloud market share = +$4B rev. Search DISRUPTION vs CLOUD OFFSET: at 28% Cloud CAGR, Cloud growth offsets ≤7% search query loss in 2yr; at 10% search loss, net EPS drag only −$0.39 over 2yr vs $10.50 EPS base. Bear ($80) requires DOJ structural divestiture + 25% query loss + cloud slowdown simultaneously — probability 12%. EPP floor $147 (+17% gap); conservative 2yr +3.3% (EPS $11 × 16× + $1.60 div = $177.60) → BUY confirmed even in conservative case. Key binary: DOJ remedy ruling Q3 2026 — behavioral = stock +15-20%; structural = −30%. Upgrade trigger: AI Overviews monetisation ratio ≥1.05× (currently 0.90×). BUY $148–172 | TRIM above $260."},
    "META": {"ticker": "META", "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 590.00,  "date": "2026-05-31", "epp_gap_pct": 40.5,  "ratio_b_fmt": "0.98x",
              "sector_group": "Technology",
              "company": "Meta Platforms, Inc.", "sector": "Social Media · Digital Advertising · AI Infrastructure · Reality Labs · NASDAQ: META",
              "summary": "Meta at FAIRLY VALUED with ACCUMULATE asymmetry — Ratio B 0.98× (66.1% downside / 67.8% upside). Proxy 2.25, SCA +0.105 → adj 2.355 ≈ market 2.36: model says priced correctly. Key upside: Advantage+ driving +14% North America ARPU YoY (BULL signal); every 5pp adoption gain = +$27/share at 22×. Reality Labs -$20B/yr is the structural drag — but path to <$4B/qtr loss = BULL upgrade. FTC divestiture ruling (Q3/Q4 2026) is the binary event: win = stable at $590-620; lose = −30%+ near-term. BULL scenario ($990): int'l ARPU +40% + Advantage+ >55% share + $241B revenue × 53% margin → EPS ~$38 at 26×. BEAR ($200): ad recession + FTC breakup + AI capex write-off → EPS $14 × 14×. EPP floor $420 (+40% gap); conservative 2yr (EPS $25 × 21× + $4 div = $529) = −10.3%. AI capex $65-70B/yr delays EPS compounding — META is a growth story, not income (div yield 0.3%). BUY below $490 (conservative 2yr turns positive). ACCUMULATE $453–620. AVOID above $742."},
    "KNEBV": {"ticker": "KNEBV", "signal": "◐ WATCHLIST", "signal_short": "WATCHLIST", "signal_color": "#60a5fa",
               "price": 46.00,  "date": "2026-06-01", "epp_gap_pct": 9.5,  "ratio_b_fmt": "1.17x",
               "sector_group": "Industrials",
               "company": "KONE Corporation", "sector": "Elevators & Escalators · Service & Modernisation · Building Technology · HEL: KNEBV · Prices in EUR",
               "summary": "KONE ◐ WATCHLIST — Ratio B 1.17× (60.9% downside / 52.2% upside). SIGNAL DOWNGRADED from ACCUMULATE: KONE agreed to acquire TK Elevator (TKE) for €29.4B on 2026-04-29 — Finland's largest ever corporate acquisition. Deal terms: €5B cash + 270M new KONE shares (33.8% post-deal) + €9.2B TKE debt refinanced → pro-forma net debt ~€12B (~4.0× EBITDA, vs Otis 2.5×). Combined entity: €20.5B revenue, 65% service (vs 53% standalone), world's #1 elevator maker (overtakes Otis), dramatically improved Americas exposure. Synergies €700M/yr run-rate by Year 3; EPS accretive Year 1 (adjusted). Scenarios updated for combined entity on 811M post-close shares. JPMorgan upgraded to Overweight, PT €70, on deal day. BEAR (€18): antitrust block or integration failure + China collapse. BASE (€48): deal closes Q2 2027, synergies €500M by FY2028. BULL (€70): full €700M synergies, service 65%, >16% EBIT margin. Conservative 2yr: EPS €2.00 × 18× + €3.56 div = €39.56 → −14.0%. WATCHLIST does NOT reflect quality concern — it reflects binary deal execution event. Upgrade trigger: antitrust clearance (behavioral remedy) → ACCUMULATE. BUY trigger: <€38. EGM June 3, 2026 (Herlin >50% votes: approval certain). All prices in EUR."},
    "T":    {"ticker": "T",    "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 24.80,  "date": "2026-06-01", "epp_gap_pct": 30.0,  "ratio_b_fmt": "0.97x",
              "sector_group": "Telecoms/Media",
              "company": "AT&T Inc.", "sector": "Wireless & Fiber · EchoStar Spectrum · Wireline Legacy · NYSE: T",
              "summary": "AT&T ◎ ACCUMULATE — Ratio B 0.97× (51.6% downside / 53.2% upside). Leveraged option on fiber broadband penetration + EchoStar spectrum acquisition ($23B, mid-2026). 37M fiber homes passed, 10.4M subs at 28.1% penetration; Q1 2026 net adds 273K (record). Each +1M fiber subs = +$0.042 EPS on existing plant. $18B FCF 2026E covers $7.7B dividend (4.5% yield, 2.3× coverage) + $10B/yr debt paydown. Deleverages from 3.1× peak (post-EchoStar close) → 2.5× target end-2028. EPP floor $19 (+30.0% gap, EPS $2.12 × 9× trough P/E). BEAR ($12): EPS $1.70 × 7× distress (recession + leverage trap + overbuilder pressure). BULL ($38): EPS $2.90 × 13× fiber re-rate (net adds 300K+/qtr; EchoStar FWA 5M+ homes). XBULL ($54): fiber 45%+ penetration; FWA #4 wireless; leverage 2.0×; EPS $3.40 × 16×. Conservative 2yr: EPS $2.60 × 9× + $2.22 div = $25.62 → +3.3%. ADJ composite 2.47 vs market 2.45 → FAIRLY VALUED. ACCUMULATE on weakness; triggers: EchoStar close confirmation, fiber net adds 300K+/qtr, leverage below 2.8×."},
    "TTWO": {"ticker": "TTWO", "signal": "◉ BUY",   "signal_short": "BUY",   "signal_color": "#4ade80",
              "price": 224.16, "date": "2026-06-01", "epp_gap_pct": 315.9, "ratio_b_fmt": "0.55x",
              "sector_group": "Consumer Discretionary",
              "company": "Take-Two Interactive Software, Inc.", "sector": "Video Games · AAA Publishing · Mobile (Zynga) · NASDAQ: TTWO",
              "summary": "TTWO ◉ BUY — Ratio B 0.55× (33.1% downside / 60.6% upside). GTA VI launch stock. Nov 19, 2026 date CONFIRMED — $8.0-8.2B FY2027 guidance explicitly tied to it. FY2026 net bookings $6.72B (+19%); OCF $624M. GTA VI = ~36% of FY2027 NB (~$2.9B). Stock fell $264→$188 on May→Nov delay; recovered to $224, still 15% below avg analyst PT $279. GTA V Online: $5B+ lifetime, $1M+/day still in 2026 (13yr post-launch) — GTA VI Online template for decade-long live-service revenue. PC release 2027-28 = additional $1B+ not in guidance. Net CASH target FY2027 year-end (from $2.6B net debt today). First GAAP profitable year FY2027E ($0.55-$0.75). EPP floor $54 (+315.9% gap — large gap is expected for an event-driven stock 6 months pre-launch). Bear $150 (3rd delay or launch flop) · Base $260 (solid 20M units) · Bull $360 (blockbuster 30M+) · XBull $500 (generational title). BUY below $240. Watch: pre-order numbers June 2026, Metacritic score day-1, GTA Online day-1 availability."},
    "VZ":    {"ticker": "VZ",    "signal": "◉ BUY",   "signal_short": "BUY",   "signal_color": "#4ade80",
              "price": 47.81,  "date": "2026-06-02", "epp_gap_pct": 32.8, "ratio_b_fmt": "0.71x",
              "sector_group": "Telecoms/Media",
              "company": "Verizon Communications, Inc.", "sector": "Wireless · Fios Fiber · Frontier Fiber · 5G FWA · NYSE: VZ",
              "summary": "VZ ◉ BUY — Ratio B 0.71× (33.1% downside / 46.4% upside). Cheapest US telecom: 9.4× forward P/E, 7.1× EV/EBITDA, 10.1% FCF yield. 5.9% dividend yield (22 consecutive annual increases; 56% FCF payout). $8.9B free after dividends. Q1 2026: EPS +7.6% YoY (best since 2021); EBITDA +6.7%; first positive Q1 phone adds in 13 years (+55K). Frontier acquisition closed Jan 20, 2026 ($20B; 30M fiber passings nationally; $1B+ synergy target by 2028). FWA: 6M+ subs; target 8-9M by 2028; total broadband 16.8M. Capital return: $25B buyback authorized; $21.5B+ FCF guided 2026. Risk: net debt ~$123B post-Frontier (2.6× EBITDA; target 2.0-2.25× by 2027). Cable MVNO headwind (Xfinity/Spectrum on T-Mobile network — no wholesale offset for VZ). C-band 230M+ POPs covered ($45B investment). Conservative 2yr: EPS $5.00 × 10× + $5.66 div = $55.66 → +16.4%. Analyst consensus $50-51; Morningstar FV $53. Bear $32 · Base $55 · Bull $70 · XBull $90."},
    "TMUS":  {"ticker": "TMUS",  "signal": "◉ BUY", "signal_short": "BUY", "signal_color": "#4ade80",
              "price": 187.53, "date": "2026-06-02", "epp_gap_pct": 69.7, "ratio_b_fmt": "0.47x",
              "sector_group": "Telecoms/Media",
              "company": "T-Mobile US, Inc.", "sector": "Wireless · Fixed Wireless Access · 5G · Fiber (Lumos JV) · NASDAQ: TMUS",
              "summary": "TMUS ◉ BUY — Ratio B 0.47× (36.0% downside / 76.0% upside). FCF machine at 8.9% yield ($18B annual FCF) trading 29.6% below ATH ($266.80). Service revenue accelerating: +8% FY2025, +11% Q1 2026 YoY. FWA at 8.5M subs (60% US market share); target 15M by 2030 — pure incremental EBITDA at zero added capex. 2.5GHz: 110MHz depth vs 40-60MHz for Verizon/AT&T — irreplaceable Sprint spectrum moat. Sprint synergies exceeded ($8B actual vs $7.5B target; NPV upgraded $43B → $70B+). $18.2B buyback authorization in 2026 alone (~9% of float). Dividend $4.08/yr (2.2%; growing ~10%/yr). Net debt $83B (2.45× EBITDA; lowest leverage among major US carriers). Cable MVNO risk: Xfinity/Spectrum Mobile took ~45% of 2025 industry phone adds — on T-Mobile's own network. Deutsche Telekom (53% owner) in early-stage merger talks — optionality not priced in. EV/EBITDA cross-check: Base 8× = $198/share; Bull 10× = $310. Analyst consensus $251-261 (+34-39%). Bear $120 · Base $250 · Bull $330 · XBull $450."},
    "CMCSA": {"ticker": "CMCSA", "signal": "◉ BUY", "signal_short": "BUY", "signal_color": "#4ade80",
              "price": 29.59, "date": "2026-06-02", "epp_gap_pct": -13.5, "ratio_b_fmt": "0.39x",
              "sector_group": "Telecoms/Media",
              "company": "Comcast Corporation", "sector": "Cable & Broadband · NBCUniversal · Peacock · Sky Europe · NASDAQ: CMCSA",
              "summary": "CMCSA ◉ BUY — Ratio B 0.39× (32.4% downside / 82.5% upside). RARE SIGNAL: stock trades BELOW EPP floor ($34.20; gap -13.5%). FCF machine at 7.1× adj EPS misread as secular-decline cable. Versant spinoff completed Jan 2, 2026 (CNBC/MSNBC/Bravo/USA/Syfy/E! → VSNT). Broadband: 31.255M subs; Q1 2026 losses 65K (best since Q4 2020, -117K YoY inflection). Xfinity Mobile: 9.3M lines (+1.5M record 2025); 15% penetration = 85% runway. Epic Universe opened May 2025: parks +19% Q2, +24% Q1 2026; first $1B+ EBITDA quarter. Peacock: 46M paid subs; >$2B quarterly revenue; Q2 2026 profitability guided. FY2025 capital return $11.7B ($6.8B buybacks + $4.9B div). Dividend $1.32/yr (4.7% yield). Net debt $85.1B (2.33× EBITDA). SOP intrinsic ~$52/share. Conservative 2yr: EPS $4.00 × 9× + $2.64 div = $38.64 → +30.6%. Bear $20 · Base $38 · Bull $54 · XBull $70."},
    "CHTR": {"ticker": "CHTR", "signal": "◉ BUY",   "signal_short": "BUY",   "signal_color": "#4ade80",
              "price": 142.79, "date": "2026-06-03", "epp_gap_pct": 90.4, "ratio_b_fmt": "0.29x",
              "sector_group": "Telecoms/Media",
              "company": "Charter Communications, Inc.", "sector": "Cable & Broadband · Spectrum Mobile · Cox Merger · NASDAQ: CHTR",
              "summary": "CHTR ◉ BUY — Ratio B 0.29× (47.4% downside / 166.1% upside). HIGH-LEVERAGE DEEP VALUE: stock fell 67% from 52-week high ($437→$143) as market prices in broadband sub losses + Cox merger leverage fear. At $143: EV/EBITDA 5.0× (cable historical 8-10×), P/E 3.9×, FCF yield 25%+. FY2025: revenue $54.8B, EBITDA $22.7B (+0.6%), FCF $5.0B (+16%). Broadband: 29.6M subs, -120K/quarter (FWA + fiber pressure); mobile: 12.1M lines (+17% YoY). CAPEX CLIFF: $11.7B→$11.4B→<$8B (2028) = FCF inflects to $8-9B by 2027-2028. Network Evolution DOCSIS 4.0: WiFi 7 symmetrical multi-gig; 50% complete → 2027 full rollout; 95% of $94.3B debt matures beyond 2026 (avg 12.7yr). Cox merger (May 2025): FCC approved, California pending; adds 6.5M subs + ~$5B EBITDA; pro-forma leverage ~3.4× (vs standalone 4.15×); target 3.5-3.75× within 3yr. Buybacks suspended (was $5.4B in 2025). Analyst consensus PT $295 (2.1× current). HIGH-RISK BUY: size smaller than CMCSA/VZ given leverage. Conservative 2yr: EPS $42.5 × 5.5× + $2.80 div = $236 → +65.7% (+28.2%/yr). Bear $75 · Base $240 · Bull $380 · XBull $550."},
    "WBD":  {"ticker": "WBD",  "signal": "◌ WATCHLIST", "signal_short": "WATCHLIST", "signal_color": "#60a5fa",
              "price": 27.14, "date": "2026-06-03", "epp_gap_pct": 352.3, "ratio_b_fmt": "1.48x",
              "sector_group": "Telecoms/Media",
              "company": "Warner Bros. Discovery, Inc.", "sector": "Streaming (Max) · Studios · Linear TV (CNN, TNT, TBS) · Netflix Deal · NASDAQ: WBD",
              "summary": "WBD ◌ WATCHLIST — Ratio B 1.48× (48.4% downside / 32.7% upside). DEAL ARB + MEDIA RENAISSANCE: stock tripled from $9.11 (52W low) to $27.14 on Netflix's $82.7B acquisition of Warner Bros. streaming+studios entity ($27.75/share equity; Dec 2025). Spread = 2.2% — most upside already priced in. Discovery Global (linear TV spin-off Q3 2026) equity uncertain (debt-laden). UNDERLYING BUSINESS EXCEPTIONAL: Studios $4B+ global box office in 2025 (Minecraft $961M, F1 $600M+, Superman $619M — first studio ever); Max 140M+ subs (Q1 2026), DTC EBITDA doubled to $1.37B (FY2025), $438M Q1 2026 (+29% YoY); debt paid down $20B+ to $33.5B (3.3x EBITDA). Linear TV structural drag: Networks EBITDA -21%, NBA rights lost ($1.1B hit). FLOOR: PSKY competing $30 all-cash offer (rejected as 'inferior'); Amazon and Apple interested; Netflix $5.8B breakup fee. WATCHLIST — BUY below $22 (Netflix deal = 26% upside). HOLD existing shares above $28 (PSKY floor). Bear $14 · Base $29 · Bull $36 · XBull $46."},
    "PSX":  {"ticker": "PSX",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 183.08, "date": "2026-06-08", "epp_gap_pct": 177.4, "ratio_b_fmt": "0.93x",
              "sector_group": "Energy",
              "company": "Phillips 66", "sector": "Refining · Midstream (DCP) · Chemicals (CPChem JV) · Marketing & Specialties · NYSE: PSX",
              "summary": "PSX ◎ ACCUMULATE — Ratio B 0.93× (26.3% downside / 28.4% upside). INTEGRATED ENERGY NEAR HIGHS: trading at $183 (near 52-wk high $191, up from $111 low) as refining margins surged ($10.11/bbl Q1'26 vs $6.81 Q1'25, +48% YoY) on structural capacity tightness (~550K bpd of US refinery closures within 18 months). Midstream scaling toward $4.5B EBITDA target by 2027 (DCP synergies $500mm realized vs $300mm target, +67% beat); CPChem JV and Marketing & Specialties add diversification. FY2025: revenue $145.5B, adj. earnings $2.6B ($6.44/sh, incl. $964mm LA-refinery D&A charge), GAAP EPS $10.90, CROIC 13.2% (2x peer avg). Balance sheet: $27.1B gross debt, Baa2/BBB- ratings. Capital returns: $5.08/yr dividend (+7% raise, ~2.8% yield), $269mm Q1 buybacks, $43B cumulative since 2012 spin-off, policy to return >50% of OCF. KEY CATALYST: Elliott Management ($2.5B stake, 'Streamline66' $40B unlock thesis) won 2 board seats in a split May-2025 proxy vote; March-2026 détente reached but core Midstream/Chemicals separation ask remains UNRESOLVED — a live, binary catalyst. Consensus PT $180.95 (range $138-213) ≈ current price = essentially fairly priced. Conservative 2yr: EPS $13.88 × 13.5x + $10.16 div = $197.54 → +7.9% (+3.9%/yr) on pure compounding (excludes Elliott-driven re-rating upside). QUALITY COMPOUNDER, NOT DEEP VALUE: add on weakness toward $150-160. Bear $135 · Base $190 · Bull $235 · XBull $290."},
    "OKE":  {"ticker": "OKE",  "signal": "◌ WATCHLIST", "signal_short": "WATCHLIST", "signal_color": "#60a5fa",
              "price": 78.00, "date": "2026-06-08", "epp_gap_pct": 36.8, "ratio_b_fmt": "1.59x",
              "sector_group": "Energy",
              "company": "ONEOK Inc.", "sector": "Midstream Energy · NGL Pipelines & Fractionation · Magellan (Refined Products) · NYSE: OKE",
              "summary": "OKE ◌ WATCHLIST — Ratio B 1.59× (55.1% downside / 34.6% upside). INTEGRATED NGL/GAS MIDSTREAM, MODESTLY UNDERVALUED ON FUNDAMENTALS BUT ASYMMETRY FAVORS PATIENCE: trading at $78 (52-wk range $58-94) after three acquisitions in three years (Magellan, EnLink, Medallion) built an irreplaceable coast-to-coast NGL/refined-products/crude network. Signal dashboard 5-of-6 BULL: Permian associated gas +11% YoY, US gas demand +8% YoY (AI data-centre/LNG tailwind), NGL frac hub utilisation 88%, Magellan crude throughput 715 Mbpd, guided dividend growth +4%/yr — only leverage (3.8x net debt/EBITDA) sits at BASE. Proxy composite 2.90/4.00 vs market-implied 2.78 — Adj gap +0.20 (modestly undervalued). UPDATED EPP: today's $7.8B normalized EBITDA × 7.5x trough multiple (raised from 7.0x for the new AI/LNG secular regime) less $26B net debt = $57/share floor — current price sits +37% above it (real cushion; BEAR $35 would require an EBITDA impairment, not just a price drop, only a 2.0σ move). CONSERVATIVE CASE compounds to +31% over 2yr (+15%/yr incl. dividend) on base-minus assumptions alone — no bull scenario required as deleveraging below 3.5x triggers multiple re-rating. Pays $4.12/yr (5.3% yield; attractive entry <$69 at 6% yield). KEY RISK: NGL keep-whole losses coinciding with leverage >4.5x could push dividend coverage below 1.2x → cut → multiple collapse (joint-probability bear, ~5% likelihood). Quality compounder with a real floor, but Ratio B 1.59× — asymmetry not yet compelling enough for BUY/ACCUMULATE; add on weakness toward $65-69 (yield-driven entry). Bear $35 · Base $70 · Bull $105 · XBull $145."},
    "XOM":  {"ticker": "XOM",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 151.17, "date": "2026-06-08", "epp_gap_pct": 259.9, "ratio_b_fmt": "0.84x",
              "sector_group": "Energy",
              "company": "ExxonMobil Corporation", "sector": "Integrated Oil & Gas · Upstream (Permian/Pioneer, Guyana) · Downstream & Chemicals · Low Carbon Solutions · NYSE: XOM",
              "summary": "XOM ◎ ACCUMULATE — Ratio B 0.84× (27.2% downside / 32.3% upside). FORTRESS SUPERMAJOR AT MID-RANGE: trading at $151 (52-wk range $103-176) with 2026 guidance calling for earnings roughly FLAT as the 2025 oil-price spike (briefly >$110/bbl) normalizes — before a multi-year growth ramp (Guyana, Golden Pass LNG, China chemicals) reaccelerates into 2027-28. TWO IRREPLACEABLE GROWTH ENGINES: Guyana at a record >900K boe/d gross (XOM net ~405K boe/d at 45% stake, sub-$35/bbl breakevens, 4 FPSOs operating/ramping) and Pioneer/Permian integration delivering >$3B/yr synergies (+50% above original guidance, 2.3 MMboe/d 2030 target, growing at 2.5x the pre-deal pace). FY2025: revenue $332B, adj. net income $45B ($7.50/sh), FCF $26.1B with dividends at only 31% of FCF — enormous coverage cushion. BALANCE SHEET IS THE MOAT: AA-/Aa2 — strongest of any major, net debt just $17B; in 2020 (debt ballooned to $68.8B on COVID demand collapse) XOM still raised its dividend, so today's downside here is a PRICE correction, not a solvency event. CAPITAL RETURNS: 43-yr dividend growth streak ($4.12/yr, ~2.7% yield, 'Dividend King' ~2030), ~$20B/yr buybacks, $9.2B total Q1 2026 shareholder returns. Consensus PT $165 (range $130-185); Argus raised to $169 (May 2026). Conservative 2yr ('flat 2026' floor case): EPS $7.55 × 18x + $8.24 div = $144.14 → -4.7% (-2.4%/yr) — BASE/BULL diverge from this floor as Guyana/Permian/Golden Pass ramp into 2027-28. Optionality: Venezuela talks (6 fields, ~$1B compensation owed). Fortress balance sheet makes the downside genuinely cushioned — add on weakness toward $130-140. Bear $110 · Base $165 · Bull $200 · XBull $240."},
    "COP":  {"ticker": "COP",  "signal": "◎ ACCUMULATE", "signal_short": "ACCUMULATE", "signal_color": "#f0b429",
              "price": 117.40, "date": "2026-06-08", "epp_gap_pct": 261.2, "ratio_b_fmt": "0.88x",
              "sector_group": "Energy",
              "company": "ConocoPhillips", "sector": "Independent Exploration & Production · Lower 48 (Permian/Eagle Ford/Bakken) · Alaska (Willow) · Qatar/Port Arthur LNG · NYSE: COP",
              "summary": "COP ◎ ACCUMULATE — Ratio B 0.88× (31.9% downside / 36.3% upside). PURE-PLAY E&P TITAN OFF A +46% RALLY: trading at $117 (52-wk range $86-136) at a premium ~19.9x trailing P/E that some houses already flag as a 'Hold' — this is a high-quality compounder that has re-rated and now needs to grow into its multiple, not a deep-value dislocation. MARATHON INTEGRATION RUNNING AHEAD OF PLAN: run-rate synergies DOUBLED to >$1B (vs $500mm original target) plus ~$1B one-time benefits in 2025; resource added 2.5 BBOE (beat the 2.0 BBOE deal target); ~30% fewer rigs/frac crews delivering MORE combined output; additional >$1B incremental target guided for 2026. GROWTH OPTIONALITY NOT YET IN THE PRICE: Willow (Alaska) ~50% complete (targeting ~180 Mbbl/d — largest new conventional US oil project) plus equity LNG stakes ramping in Qatar/Port Arthur. FY2025: revenue $62B, adj. net income $7.5B ($6.20/sh), FCF $9.5B. INDUSTRY-LEADING COST CUSHION: ~$40/bbl cost-of-supply breakeven; IG balance sheet (net debt $17.5B vs $122.7B assets) — current price ~5.2x the 2020 COVID trough ($22.67) on a vastly larger, lower-cost, higher-FCF company. Capital returns: ~45% of CFO targeted, $2.0B returned in Q1 2026 ($1.0B buybacks + $1.0B dividend, ~2.9% yield). Consensus PT $141 (20 buy / 2 sell of 27 analysts; bear-case target $104.93). Conservative 2yr (multiple-normalization floor case): EPS $6.20 x 17.5x + $6.72 div = $115.92 -> -1.3% — BASE/BULL diverge as Marathon/Willow/LNG growth materializes. KEY RISK: bears warn $60/bbl WTI 'would eviscerate the investment case' for a pure-play, undiluted commodity bet with no downstream cushion. Add on weakness toward $95-105. Bear $80 · Base $135 · Bull $160 · XBull $190."},
    "EA":   {"ticker": "EA",   "signal": "✕ AVOID",  "signal_short": "AVOID",  "signal_color": "#f87171",
              "price": 202.01, "date": "2026-06-03", "epp_gap_pct": 72.7, "ratio_b_fmt": "2.89x",
              "sector_group": "Consumer Discretionary",
              "company": "Electronic Arts Inc.", "sector": "Video Games · Live Services · Sports (FC, Madden, CF) · Battlefield · NASDAQ: EA",
              "summary": "EA ✕ AVOID — Ratio B 2.89× (25.7% downside / 8.9% upside). DEAL ARB: $210/share take-private by PIF/Silver Lake/Affinity Partners ($55B EV); shareholders approved 99% (Dec 22, 2025); CFIUS pending (outside date Sep 28, 2026). Stock at $202 = 4.0% upside if deal closes vs -20.8% downside if CFIUS blocks. Expected arb value: +0.25% (essentially zero alpha). Underlying business is EXCELLENT: FY2026 record net bookings $8.03B (+9.1%); FCF $2.32B (+24.7%); Battlefield 6 (7M sales day-3; franchise record); EA Sports FC 26 (12M copies in 3wk; Metacritic 84); Apex Legends (guided -40%, actual +double digits); College Football franchise ($1B+/yr). 71% live services recurring revenue; UT ecosystem $4.4B/yr. Deal implied 6.9x net bookings vs Activision paid 9.3x — buyers got a bargain. AVOID for new buyers at $202. HOLD for existing shareholders. Re-evaluate below $185 (better arb spread) or below $170 (standalone entry). Bear $150 (CFIUS block) · Base $210 (deal close) · Bull $220 · XBull $245."},
    "DNP":  {"ticker": "DNP",  "signal": "✕ AVOID",  "signal_short": "AVOID",  "signal_color": "#f87171",
              "price": 32.0,    "date": "2026-05-28", "epp_gap_pct": 142.4, "ratio_b_fmt": "1.82x",
              "sector_group": "Consumer Staples",
              "company": "Dino Polska S.A.", "sector": "Polish Grocery Retail · Standalone Discount Format · WSE: DNP · Prices in PLN",
              "summary": "Poland's fastest-growing grocery chain: 2,750 stores (+360/yr; 15% store CAGR), PLN 28B revenue, 5.4% EBIT margin. Post 10:1 split (Jul 2025): EPS PLN 1.14; EPP floor PLN 13 (+142% gap). Ratio B 1.82× (AVOID): at PLN 32 the bear scenario (PLN 8.4) gives 73.8% downside vs bull (PLN 45) 40.6% upside — asymmetric risk despite excellent fundamentals. Adj. composite 3.17 vs market-implied 2.72 — business is UNDERVALUED but price is AVOID. Founder Biernacki 52%: aligned, reinvests at 20%+ ROIC, no dividends. Bear (PLN 8.4): Polish recession + Biedronka price war collapses 5.4% margin. Bull (PLN 45): growth acceleration + premium re-rating 30×. 52W range PLN 28–56; current near 2-yr low. Note: prices in PLN (÷4.25 for EUR)."},
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
