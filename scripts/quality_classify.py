#!/usr/bin/env python3
"""
Quality × price classification for the VeeRock coverage universe.

Replaces the one-dimensional BUY / ACCUMULATE / WATCHLIST / HOLD / AVOID tier
(which is a pure valuation read and therefore tends to rate structurally
challenged businesses as "BUY" simply because they are cheap) with a
two-axis taxonomy:

  axis 1 — business durability (hand-curated per ticker, BUSINESS_PROFILES)
      DURABLE     franchise / compounder; low risk the business becomes useless
      CYCLICAL    good business whose earnings ARE the cycle (commodities,
                  semis, autos, cap goods, banks, refiners ...)
      STRUCTURAL  secular decline or a live disruption / existential threat
      TURNAROUND  franchise not permanently impaired but currently broken
      SPECIAL     deal arbitrage, binary legal/legislative outcome, bond

  axis 2 — price / asymmetry (deterministic from the model's own numbers:
      Ratio B, EPP gap, adjusted-vs-market composite gap, conservative 2yr)
      CHEAP  downside limited, asymmetry favourable
      FAIR   neutrally valued
      RICH   priced for perfection

  and the resulting classes (signal_short / signal on the site):

      COMPOUNDER AT LOW PRICE          DURABLE    × CHEAP        green
      QUALITY, NEUTRALLY VALUED        DURABLE    × FAIR         amber
      QUALITY, PRICED FOR PERFECTION   DURABLE    × RICH         red
      CYCLICAL, RISK PRICED IN         CYCLICAL   × CHEAP        amber
      CYCLICAL, NEUTRALLY VALUED       CYCLICAL   × FAIR         blue
      TOO MUCH CYCLE RISK              CYCLICAL   × RICH         red
      CHEAP, BUT STRUCTURAL RISK       STRUCTURAL × CHEAP        blue
      STRUCTURAL RISK, NOT CHEAP       STRUCTURAL × FAIR/RICH    red
      TURNAROUND BET                   TURNAROUND × CHEAP/FAIR   blue
      SPECIAL SITUATION                SPECIAL    × any          blue

Usage
  python3 scripts/quality_classify.py --local DIR        classify JSONs in DIR, print table
  python3 scripts/quality_classify.py --apply-s3         enrich every veerock-signals/*.json
                                                         on S3, redeploy the Lambda summary,
                                                         invalidate CloudFront
  python3 scripts/quality_classify.py --apply-s3 --dry   same, no writes

The module is also imported by scripts/consolidate_lambda.py so that every
nightly-refreshed ticker is re-classified before it reaches the Lambda.
"""
import argparse
import glob
import json
import math
import os
import re
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Axis 1 — business durability.  kind, obsolescence risk 1 (very low) .. 5
# (existential), one-line reason.  Hand-curated; keep in sync when tickers
# are added to coverage.  Unknown tickers fall back to DURABLE/3 with a note.
# ─────────────────────────────────────────────────────────────────────────────
D, C, S, T, X = "DURABLE", "CYCLICAL", "STRUCTURAL", "TURNAROUND", "SPECIAL"

BUSINESS_PROFILES = {
    # ── Finance ──────────────────────────────────────────────────────────────
    "ALV":  (D, 2, "Diversified insurer/asset manager; nat-cat and PIMCO flow risk, not obsolescence"),
    "AXP":  (D, 2, "Closed-loop premium card network with fee flywheel; credit cycle is the swing"),
    "BAC":  (C, 2, "Money-center bank; earnings are the rate/credit cycle, franchise durable"),
    "BBVA": (C, 2, "Spain/Mexico/Turkey bank at peak ROTE; rate-cut and Mexico concentration risk"),
    "BLK":  (D, 2, "Largest asset manager, iShares + Aladdin; fee compression is slow, not existential"),
    "BNP":  (C, 2, "Eurozone universal bank; re-rating done, NII compression is the cycle risk"),
    "BRK":  (D, 1, "Conglomerate with fortress balance sheet; PacifiCorp wildfire tail is the one real risk"),
    "BX":   (D, 2, "Largest alternative manager; fee-related earnings durable, realizations cyclical"),
    "C":    (C, 2, "Restructuring money-center bank; ROTCE improving, still a credit/trading cycle name"),
    "CB":   (D, 2, "Global P&C underwriter; cat season swings, franchise durable"),
    "CS":   (D, 2, "AXA: diversified insurer; plan execution excellent, price is the constraint"),
    "DB1":  (D, 1, "Exchange/clearing/data monopoly-like franchise"),
    "DBK":  (C, 3, "Deutsche Bank at a cyclical profit peak after a long restructuring"),
    "FISV": (T, 3, "Fiserv: Clover/merchant deceleration and guidance reset; core banking base sticky"),
    "GS":   (C, 2, "Investment bank; trading/IB revenue is the cycle, priced at a peak"),
    "INGA": (C, 2, "Dutch/EU retail bank at a 52-week high; deposit-margin compression is the risk"),
    "ISP":  (C, 2, "Italian bank with the best fee annuity in Italy; BTP beta and MPS deal risk"),
    "JPM":  (C, 1, "Best-in-class universal bank; still a rate/credit cycle at a record multiple"),
    "KKR":  (D, 2, "Alternative manager with insurance balance sheet; fee earnings durable"),
    "MA":   (D, 1, "Payments network duopoly; regulatory interchange risk, no obsolescence risk"),
    "MRSH": (D, 1, "Marsh McLennan: fee-based broking/consulting moat, 19 years of margin expansion"),
    "MS":   (C, 2, "Wealth-management-led bank; still cyclical, priced for a peak"),
    "MUV2": (D, 2, "Reinsurer; P&C pricing cycle softening, franchise durable"),
    "NDA":  (C, 2, "Nordic bank at the top of its range; rate-cut cycle risk"),
    "PGR":  (C, 1, "Progressive: elite underwriter, but combined ratio is at a cyclical peak"),
    "PKO":  (C, 2, "Polish state-linked bank near all-time high; rate and regulatory cycle"),
    "PYPL": (T, 3, "PayPal: branded checkout share loss vs Apple/Shop Pay; Venmo monetisation unproven"),
    "PZU":  (D, 2, "Polish insurer; state ownership and Pekao reorganisation overhang"),
    "SAN":  (C, 2, "Santander: record profitability, LatAm growth; still a bank cycle"),
    "SCHW": (D, 2, "Schwab: scale brokerage/bank; cash-sorting relief is the tailwind, rates the risk"),
    "SPGI": (D, 1, "Ratings duopoly + indices flywheel; Dividend King"),
    "UCG":  (C, 2, "UniCredit at highs; Commerzbank integration and NII compression risk"),
    "V":    (D, 1, "Payments network duopoly; DOJ debit suit is the overhang"),
    "WFC":  (C, 2, "Asset-cap-freed bank; earnings cyclical, franchise durable"),
    "XTB":  (C, 3, "Retail CFD broker: revenue is client trading volume and volatility"),
    "UST":  (X, 1, "10-year Treasury benchmark, not an equity"),
    # ── Utilities ────────────────────────────────────────────────────────────
    "AEP":  (D, 1, "Regulated transmission/distribution utility; rate-base growth, rate sensitivity"),
    "AWK":  (D, 1, "Regulated water utility, bond proxy"),
    "CEG":  (C, 2, "Nuclear fleet: durable assets, but earnings ride power prices and AI-demand PPAs"),
    "D":    (X, 1, "Dominion: being acquired by NextEra (all-stock), trades on deal spread"),
    "DTE":  (D, 1, "Regulated Michigan utility; data-center docket is the catalyst"),
    "DUK":  (D, 1, "Regulated Southeast utility; data-center pipeline, rate sensitivity"),
    "EIX":  (X, 3, "Edison: regulated wires franchise, but California wildfire liability is an uncapped, legislature-decided tail"),
    "ENEL": (D, 1, "Italian/LatAm integrated utility; regulated networks plus renewables"),
    "ETR":  (D, 1, "Regulated Gulf-coast utility; capex plan priced at ~24x"),
    "EXC":  (D, 1, "Pure-play regulated wires utility; PJM capacity tailwind"),
    "IBE":  (D, 1, "Iberdrola: regulated networks + renewables compounder"),
    "NEE":  (D, 1, "Largest US renewables developer + FPL; Dominion merger execution risk"),
    "PCG":  (X, 3, "PG&E: post-bankruptcy wires franchise, but California wildfire liability remains uncapped after SB 492 died"),
    "PEG":  (D, 1, "PSEG: regulated NJ utility plus nuclear; 6-8% EPS growth guide"),
    "SO":   (D, 1, "Southern: regulated utility, Vogtle in rate base, data-center pipeline"),
    "SRE":  (D, 1, "Sempra: regulated California/Texas utilities plus LNG infrastructure"),
    "VST":  (C, 2, "Vistra: merchant power + nuclear; earnings ride power prices and AI-load PPAs"),
    "WEC":  (D, 1, "Regulated Wisconsin utility; Microsoft data-center load"),
    "XEL":  (D, 1, "Regulated Midwest/Colorado utility; wildfire litigation is the tail"),
    # ── Telecoms / Media ─────────────────────────────────────────────────────
    "CHTR": (S, 4, "Cable broadband losing share to fixed-wireless/fiber, video in secular decline, high leverage"),
    "CMCSA":(S, 3, "Cable broadband losing subscribers to fixed-wireless/fiber; parks/NBCU diversify but core is in slow decline"),
    "DTEGY":(D, 2, "Deutsche Telekom: T-Mobile US growth engine, German incumbent"),
    "T":    (D, 2, "AT&T: wireless + fiber; legacy copper/wireline decline is managed"),
    "TMUS": (D, 2, "T-Mobile: share-gaining US wireless #1; capital-intensive oligopoly"),
    "VZ":   (D, 2, "Verizon: wireless oligopoly, 5.7% yield; Starlink-direct is the long-term threat"),
    "WBD":  (X, 3, "Warner Bros Discovery: Paramount Skydance cash deal, trades on close probability"),
    # ── Technology ───────────────────────────────────────────────────────────
    "AAPL": (D, 1, "Apple ecosystem; memory-cost margin question is cyclical, not structural"),
    "ACN":  (D, 3, "Accenture: GenAI can deflate IT-services pricing; also the delivery partner for it"),
    "ADBE": (D, 3, "Adobe: creative-suite moat vs generative-AI substitution; CEO seat vacant"),
    "ADYEN":(D, 2, "Adyen: single-platform payments, 20%+ growth, net cash"),
    "AMD":  (C, 2, "AMD: AI/data-center GPU ramp; semis cycle and valuation risk"),
    "ASML": (C, 1, "ASML: EUV monopoly; earnings ride the semi-capex cycle and China policy"),
    "AVGO": (D, 2, "Broadcom: custom AI silicon + VMware software; semi cycle exposure"),
    "CRM":  (D, 3, "Salesforce: CRM leader; agentic AI could compress per-seat pricing"),
    "CSCO": (D, 2, "Cisco: networking incumbent with AI-infrastructure order book"),
    "GOOGL":(D, 2, "Alphabet: search cash machine + cloud; AI-search cannibalisation is the debate"),
    "IBM":  (D, 3, "IBM: consulting + software + mainframe; slow-growth, AI both threat and driver"),
    "IFX":  (C, 2, "Infineon: power/auto semis; auto cycle and Chinese competition"),
    "INTC": (T, 4, "Intel: foundry turnaround with government stake; execution unproven, 5x run"),
    "INTU": (D, 3, "Intuit: TurboTax/QuickBooks; growth reset to 9-10%, AI-tax risk"),
    "LRCX": (C, 1, "Lam Research: etch/deposition leader; WFE cycle"),
    "META": (D, 2, "Meta: ad engine healthy; capex/FCF trajectory is the swing"),
    "MRVL": (C, 2, "Marvell: custom AI silicon; hyperscaler capex cycle, priced for a ramp"),
    "MSFT": (D, 1, "Microsoft: Azure + M365 + OpenAI; capex intensity is the only real debate"),
    "MU":   (C, 2, "Micron: HBM/DRAM; memory cycle at a record, CXMT competition"),
    "NFLX": (D, 2, "Netflix: scaled streaming leader with ads flywheel"),
    "NOW":  (D, 3, "ServiceNow: workflow platform; agentic AI vs per-seat licensing unresolved"),
    "NVDA": (C, 2, "Nvidia: AI compute leader; demand is a capex cycle, China conceded"),
    "ORCL": (D, 3, "Oracle: OCI/AI backlog financed with debt + equity; BBB- credit, execution risk"),
    "PANW": (D, 2, "Palo Alto: security platform consolidator; growth decelerating to 20s"),
    "PLTR": (D, 3, "Palantir: exceptional growth, extreme multiple; enterprise AI durability unproven"),
    "PRX":  (D, 2, "Prosus: Tencent stake + profitable e-commerce ecosystems at a NAV discount"),
    "QCOM": (C, 3, "Qualcomm: handset decline (Apple exit) vs auto/data-center diversification"),
    "SAP":  (D, 2, "SAP: ERP incumbent with cloud backlog; AI-agent rollout pace is the debate"),
    "TXN":  (C, 1, "Texas Instruments: analog leader; industrial/auto semi cycle, capex-heavy"),
    "UBER": (D, 3, "Uber: mobility platform; autonomous vehicles are both partner and threat"),
    "WKL":  (D, 3, "Wolters Kluwer: information services; AI-disruption fear vs proven renewals"),
    # ── Industrials ──────────────────────────────────────────────────────────
    "AI":   (D, 1, "Air Liquide: industrial-gas oligopoly, take-or-pay contracts"),
    "AIR":  (D, 1, "Airbus: aircraft duopoly with 9,000+ backlog; delivery pace is the swing"),
    "APD":  (D, 1, "Air Products: industrial-gas oligopoly; hydrogen megaprojects are optionality"),
    "ATCOA":(C, 2, "Atlas Copco: compressors/vacuum; semi-capex and industrial cycle"),
    "BA":   (T, 2, "Boeing: duopoly franchise in a multi-year production/quality recovery"),
    "CAT":  (C, 1, "Caterpillar: heavy equipment; record backlog at a cycle-peak multiple"),
    "DE":   (C, 1, "Deere: ag equipment; row-crop replacement cycle at a trough, stock at an all-time high"),
    "DG":   (D, 1, "Vinci: concessions (airports/toll roads) + contracting; inflation-linked"),
    "DHL":  (C, 2, "DHL: express/logistics; global-trade and tariff cycle"),
    "DSV":  (C, 2, "DSV: asset-light freight forwarder; Schenker integration, freight cycle"),
    "EMR":  (C, 2, "Emerson: automation; industrial capex cycle, test & measurement"),
    "ENR":  (C, 2, "Siemens Energy: grid/gas-turbine super-cycle; wind losses, order-driven"),
    "ETN":  (C, 1, "Eaton: electrical equipment; AI data-center capex cycle, priced for it"),
    "FERG": (C, 1, "Ferguson: #1 plumbing/HVAC distributor; housing and R&R cycle"),
    "GE":   (D, 1, "GE Aerospace: engine aftermarket annuity; priced at ~42x"),
    "GEV":  (C, 2, "GE Vernova: gas turbines/grid; order boom, priced for it"),
    "HON":  (D, 2, "Honeywell: diversified industrial post-spin; steady, fully priced"),
    "KNEBV":(D, 2, "Kone: elevators with service annuity; China new-build weakness"),
    "LIN":  (D, 1, "Linde: industrial-gas oligopoly, pricing power"),
    "LMT":  (D, 2, "Lockheed: defense prime; F-35 program overhang, budget-driven"),
    "MMM":  (D, 3, "3M: diversified industrial; PFAS litigation is a long-tail liability"),
    "PH":   (C, 1, "Parker Hannifin: motion/control; industrial cycle, 70 years of dividend increases"),
    "RHM":  (C, 2, "Rheinmetall: European rearmament; order-driven, ceasefire de-rating risk, 45% vol"),
    "RTX":  (D, 1, "RTX: defense + Pratt aftermarket; $289B backlog"),
    "SAF":  (D, 1, "Safran: LEAP engine aftermarket annuity; duopoly"),
    "SIE":  (D, 1, "Siemens: automation/electrification/mobility; record industrial profit"),
    "SU":   (D, 1, "Schneider Electric: electrification/energy management leader"),
    "TDG":  (D, 1, "TransDigm: proprietary aerospace parts, pricing power, levered compounder"),
    "TT":   (D, 1, "Trane: HVAC leader with data-center cooling; priced for flawless execution"),
    "UNP":  (D, 1, "Union Pacific: railroad duopoly; NS merger pending"),
    "UPS":  (D, 3, "UPS: parcel network; Amazon volume glide-down and margin reset"),
    "WM":   (D, 1, "Waste Management: landfill/collection moat with pricing power"),
    # ── Consumer Discretionary ───────────────────────────────────────────────
    "ABNB": (D, 2, "Airbnb: two-sided travel marketplace; growth slowing, priced richly"),
    "ADS":  (D, 2, "adidas: global sportswear #2; brand momentum, CFO succession"),
    "ALE":  (D, 3, "Allegro: Polish e-commerce leader; Temu/Shein price competition"),
    "AMZN": (D, 1, "Amazon: retail + AWS + ads; FTC ad-auction suit is an overhang"),
    "AZO":  (D, 2, "AutoZone: auto-parts retail, counter-cyclical; EV mix is a slow long-term headwind"),
    "BKNG": (D, 2, "Booking: OTA leader; AI agents could disintermediate over time"),
    "BMW":  (C, 3, "BMW: premium autos; EV transition and Chinese competition, 2.3% auto margin"),
    "CDR":  (C, 3, "CD Projekt: hit-driven game developer priced on two unreleased titles"),
    "CMG":  (D, 2, "Chipotle: unit-growth restaurant franchise; salmonella outbreak is transient"),
    "EA":   (X, 1, "Electronic Arts: take-private completed, delisted"),
    "EL":   (D, 2, "EssilorLuxottica: lens/frames near-monopoly; Ray-Ban Meta optionality, Apple eyewear risk"),
    "F":    (C, 3, "Ford: legacy auto with EV losses; tariff and credit cycle"),
    "GM":   (C, 3, "GM: legacy auto at a cycle-peak margin; tariffs, recalls, EV losses"),
    "HD":   (D, 1, "Home Depot: home-improvement leader; frozen housing market is cyclical"),
    "HLT":  (D, 2, "Hilton: asset-light franchisor; lodging demand cycle"),
    "ITX":  (D, 2, "Inditex: best-in-class fast-fashion execution, net cash"),
    "LOW":  (D, 1, "Lowe's: home-improvement #2; DIY demand trough, guidance cut"),
    "LPP":  (D, 2, "LPP: CEE apparel retailer (Sinsay) with store rollout runway"),
    "MAR":  (D, 2, "Marriott: asset-light franchisor; Middle East RevPAR headwind"),
    "MBG":  (C, 3, "Mercedes: premium autos; China share loss, tariffs"),
    "MC":   (D, 2, "LVMH: luxury leader; China/aspirational demand cycle"),
    "MCD":  (D, 1, "McDonald's: franchised restaurant royalty stream at a 52-week low"),
    "NKE":  (T, 3, "Nike: brand still huge, but earnings collapsed; new management, China malaise"),
    "ORLY": (D, 2, "O'Reilly: auto-parts retail compounder"),
    "RACE": (D, 1, "Ferrari: scarcity luxury brand, order book years long"),
    "RCL":  (C, 2, "Royal Caribbean: cruise demand cycle with $22B net debt"),
    "RMS":  (D, 1, "Hermès: the most durable luxury brand; growth slowing from Middle East"),
    "SBUX": (T, 2, "Starbucks: brand intact, US traffic turnaround under way, priced for success"),
    "TJX":  (D, 1, "TJX: off-price retail leader, counter-cyclical"),
    "TSLA": (C, 3, "Tesla: auto earnings collapsed, priced on robotaxi/Optimus optionality"),
    "TTWO": (D, 2, "Take-Two: GTA VI launch Nov 2026; hit-driven but franchise-backed"),
    "VOW3": (T, 3, "Volkswagen: deepest restructuring in its history; China share loss, tariffs"),
    "ZAB":  (X, 1, "Zabka: Couche-Tard cash tender open, capped upside"),
    # ── Healthcare ───────────────────────────────────────────────────────────
    "ABBV": (D, 2, "AbbVie: Skyrizi/Rinvoq replaced Humira; patent cycle managed"),
    "ABT":  (D, 1, "Abbott: diversified devices/diagnostics/nutrition"),
    "AMGN": (D, 2, "Amgen: biotech with biosimilar and obesity pipeline"),
    "ARGX": (D, 3, "argenx: Vyvgart single-franchise concentration, FcRn competition"),
    "BAYN": (T, 3, "Bayer: glyphosate litigation + pharma patent cliff (Xarelto, Eylea)"),
    "BMY":  (S, 3, "Bristol: Eliquis/Opdivo loss-of-exclusivity 2028 vs unproven growth portfolio"),
    "BSX":  (D, 1, "Boston Scientific: cardiology device leader (WATCHMAN, Farapulse)"),
    "DHR":  (D, 1, "Danaher: life-science tools compounder"),
    "ELV":  (D, 2, "Elevance: managed care; Medicaid/MA cost trend and policy risk"),
    "GILD": (D, 2, "Gilead: HIV franchise annuity, oncology optionality"),
    "HCA":  (D, 2, "HCA: largest hospital operator; policy/reimbursement risk"),
    "ISRG": (D, 1, "Intuitive Surgical: robotic-surgery leader, razor/blade"),
    "JNJ":  (D, 1, "J&J: pharma + medtech; talc settlement overhang"),
    "LLY":  (D, 1, "Eli Lilly: GLP-1 leader; priced for it"),
    "MRK":  (D, 3, "Merck: Keytruda 2028 patent cliff vs vaccine/pipeline wins"),
    "PFE":  (S, 3, "Pfizer: Eliquis/Ibrance LOE cliff, post-COVID reset; 6% yield"),
    "SNY":  (D, 2, "Sanofi: Dupixent-led immunology, cheapest large pharma"),
    "SYK":  (D, 1, "Stryker: orthopaedics/medtech compounder"),
    "TMO":  (D, 1, "Thermo Fisher: life-science tools leader"),
    "UNH":  (D, 2, "UnitedHealth: managed-care scale; DOJ criminal/civil probe and MA exits"),
    "VRTX": (D, 2, "Vertex: CF monopoly, pain franchise; Crinetics deal"),
    # ── Consumer Staples ─────────────────────────────────────────────────────
    "ABI":  (D, 2, "AB InBev: global brewer, deleveraging; volumes back to growth"),
    "AD":   (D, 2, "Ahold Delhaize: grocery, low margin, 4% yield"),
    "BN":   (D, 2, "Danone: specialised nutrition engine, defensive"),
    "CL":   (D, 1, "Colgate: oral-care leader; EM FX, Hill's competition"),
    "COST": (D, 1, "Costco: membership model, best retail franchise, priced as such"),
    "DNP":  (D, 2, "Dino Polska: grocery discounter rollout; Biedronka/Lidl price war"),
    "KHC":  (S, 3, "Kraft Heinz: legacy packaged-food brands in volume decline"),
    "KO":   (D, 1, "Coca-Cola: global beverage brand system"),
    "MDLZ": (D, 2, "Mondelez: snacking leader; cocoa costs easing, GLP-1 headwind"),
    "MNST": (D, 2, "Monster: energy drinks with Coca-Cola distribution; ~41x earnings"),
    "MO":   (S, 3, "Altria: US cigarette volumes in secular decline, NJOY blocked; 6.4% yield"),
    "OR":   (D, 1, "L'Oréal: beauty leader, record margins"),
    "PEP":  (D, 2, "PepsiCo: snacks + beverages; Elliott-driven cost program, 4.2% yield"),
    "PG":   (D, 1, "P&G: consumer staples compounder, 70 dividend increases"),
    "PM":   (D, 2, "Philip Morris: smoke-free (IQOS/ZYN) transition offsets cigarette decline"),
    "TGT":  (D, 3, "Target: discretionary-heavy retailer losing share to Walmart/Amazon"),
    "WMT":  (D, 1, "Walmart: scale retail + ads/marketplace; consolidating near 52-week low"),
    # ── Energy ───────────────────────────────────────────────────────────────
    "BKR":  (C, 2, "Baker Hughes: oilfield services + LNG equipment; leverage post-Chart"),
    "COP":  (C, 2, "ConocoPhillips: E&P; earnings are the oil price"),
    "CVX":  (C, 2, "Chevron: integrated major; oil price, Hess synergies"),
    "DVN":  (C, 2, "Devon: shale E&P; oil price"),
    "ENI":  (C, 2, "Eni: integrated major; Brent-driven, buyback"),
    "FANG": (C, 2, "Diamondback: lowest-cost Permian E&P; oil price"),
    "HAL":  (C, 2, "Halliburton: oilfield services; rig-count cycle"),
    "KMI":  (D, 2, "Kinder Morgan: fee-based gas pipelines"),
    "MPC":  (C, 2, "Marathon Petroleum: refining crack spreads at a geopolitical peak"),
    "OKE":  (D, 2, "ONEOK: midstream NGL/gas; acquisition-driven, leverage"),
    "OXY":  (C, 3, "Occidental: levered E&P; oil price and debt"),
    "PKN":  (C, 2, "Orlen: CEE refining/petchem/retail at record margins"),
    "PSX":  (C, 2, "Phillips 66: refining + midstream; crack-spread peak"),
    "SLB":  (C, 2, "Schlumberger: oilfield services leader; upstream capex cycle"),
    "TRGP": (D, 2, "Targa: Permian midstream/NGL; volume-driven, priced for it"),
    "TTE":  (C, 2, "TotalEnergies: integrated major + LNG; Brent-driven"),
    "VLO":  (C, 2, "Valero: refining crack spreads at a peak"),
    "WMB":  (D, 1, "Williams: Transco gas pipeline annuity; AI-power demand"),
    "XOM":  (C, 1, "ExxonMobil: integrated major, Guyana/Permian; oil price"),
    # ── Materials / Basic Resources ──────────────────────────────────────────
    "BAS":  (C, 2, "BASF: chemicals; China overcapacity, EU energy costs"),
    "ECL":  (D, 1, "Ecolab: water/hygiene services compounder"),
    "FCX":  (C, 2, "Freeport: copper/gold miner; copper price"),
    "PPG":  (C, 2, "PPG: coatings; industrial/auto demand cycle"),
    "SGO":  (C, 2, "Saint-Gobain: building materials; construction cycle"),
    "SHW":  (D, 1, "Sherwin-Williams: paint stores moat, pricing power"),
    "VMC":  (D, 1, "Vulcan: aggregates quasi-monopoly; infrastructure funding"),
    "CTVA": (C, 2, "Corteva: seeds/crop protection; ag cycle, Vylor spin"),
    "DOW":  (C, 2, "Dow: commodity chemicals at trough earnings; ethane advantage normalising"),
    "KGH":  (C, 2, "KGHM: copper/silver miner; metals at records, Polish state owner"),
    "KTY":  (C, 2, "Kety: aluminium extrusions/packaging; European industrial cycle"),
    "LYB":  (C, 3, "LyondellBasell: polyolefins at a trough with leverage and a dividend cut"),
    "NEM":  (C, 2, "Newmont: gold miner; gold price, rising AISC"),
}

KIND_LABEL = {
    D: "durable franchise", C: "cyclical", S: "structurally challenged",
    T: "turnaround", X: "special situation",
}

# ─────────────────────────────────────────────────────────────────────────────
# Classes.  key == signal_short on the site, label == badge text.
# Colours reuse the four badge palettes the site CSS ships (green/amber/blue/red).
# ─────────────────────────────────────────────────────────────────────────────
CLASSES = {
    "COMPOUNDER AT LOW PRICE":        dict(icon="◉", color="#4ade80", tone="green",
        desc="Durable business, downside limited, asymmetry favourable"),
    "QUALITY, NEUTRALLY VALUED":      dict(icon="◎", color="#f0b429", tone="amber",
        desc="Durable business at a fair price; add on weakness"),
    "QUALITY, PRICED FOR PERFECTION": dict(icon="✕", color="#f87171", tone="red",
        desc="Great business, no margin of safety; trim into strength"),
    "CYCLICAL, RISK PRICED IN":       dict(icon="◎", color="#f0b429", tone="amber",
        desc="Earnings are the cycle, but the price already discounts it; size small"),
    "CYCLICAL, NEUTRALLY VALUED":     dict(icon="◐", color="#60a5fa", tone="blue",
        desc="Cyclical at a fair price; timing, not value"),
    "TOO MUCH CYCLE RISK":            dict(icon="✕", color="#f87171", tone="red",
        desc="Cyclical priced on peak earnings or a peak multiple"),
    "CHEAP, BUT STRUCTURAL RISK":     dict(icon="◐", color="#60a5fa", tone="blue",
        desc="Statistically cheap, but the business faces a live structural threat"),
    "STRUCTURAL RISK, NOT CHEAP":     dict(icon="✕", color="#f87171", tone="red",
        desc="Structural threat and no valuation support"),
    "TURNAROUND BET":                 dict(icon="◐", color="#60a5fa", tone="blue",
        desc="Franchise intact, earnings broken; pay for the recovery, not the floor"),
    "SPECIAL SITUATION":              dict(icon="◐", color="#60a5fa", tone="blue",
        desc="Deal spread, binary legal/legislative outcome, or a bond"),
}

LEGACY_TIERS = {"BUY", "ACCUMULATE", "WATCHLIST", "HOLD", "HOLD/TRIM", "TRIM", "AVOID", "ACQUIRED"}

# ─────────────────────────────────────────────────────────────────────────────
# Number extraction from the model JSON
# ─────────────────────────────────────────────────────────────────────────────
def _num(x, default=None):
    if x is None:
        return default
    if isinstance(x, (int, float)):
        return float(x)
    m = re.search(r"[-+]?\d+(?:\.\d+)?", str(x).replace(",", ""))
    return float(m.group()) if m else default


def parse_ratio_b(entry):
    s = str(entry.get("ratio_b_fmt", "")).strip()
    if not s or s.upper().startswith("N/A") or s.lower().startswith("n/m"):
        return math.inf
    v = _num(s)
    return v if v is not None else math.inf


def parse_adj_gap(entry):
    """Adjusted composite minus market-implied composite (positive = undervalued)."""
    rep = entry.get("report") or ""
    m = re.search(r"Adj(?:usted)?\s+gap:\s*([-+]?\d+\.\d+)", rep)
    if m:
        return float(m.group(1))
    s = entry.get("summary") or ""
    m = re.search(r"Adj(?:usted)?\.?\s*(?:composite|comp)\s*\(?([\d.]+)(?:/4(?:\.0+)?)?\)?\s*(?:vs\.?|versus)\s*(?:the\s+)?market(?:[- ]implied|[- ]composite)?(?:\s+composite)?\s*\(?([\d.]+)", s, re.I)
    if m:
        return round(float(m.group(1)) - float(m.group(2)), 2)
    m = re.search(r"gap\s*(?:of|at|to|=|is|:)?\s*\(?([-+]\d\.\d{2,3})\b", s)
    if m:
        return float(m.group(1))
    m = re.search(r"([-+]\d\.\d{2,3})\s*(?:pts?|points)?\s*\)?\s*\[?(?:UNDERVALUED|OVERVALUED|FAIRLY VALUED|MODESTLY)", s)
    if m:
        return float(m.group(1))
    m = re.search(r"(?:UNDERVALUED|OVERVALUED|FAIRLY VALUED)\s*\(?(?:gap\s*)?([-+]\d\.\d{2,3})", s)
    if m:
        return float(m.group(1))
    m = re.search(r"composite\s+gap[^.;|]{0,40}?([-+]\d\.\d{2,3})\b", s)
    if m:
        return float(m.group(1))
    m = re.search(r"\bgap[^.;|]{0,40}?\bto\s+([-+]\d\.\d{2,3})\b", s)
    if m:
        return float(m.group(1))
    return None


def parse_verdict(entry):
    txt = (entry.get("report") or "") + " " + (entry.get("summary") or "")
    for v in ("MODESTLY UNDERVALUED", "MODESTLY OVERVALUED", "FAIRLY VALUED", "UNDERVALUED", "OVERVALUED"):
        if re.search(r"\b" + v + r"\b", txt):
            return v
    return None


def parse_cons_return(entry):
    """Conservative 2-yr total return in %, if the summary states one."""
    s = entry.get("summary") or ""
    m = re.search(r"Conservative(?:\s+growth)?(?:\s+2[- ]?yr|\s+2-year|\s+case)[^.]*", s, re.I)
    if not m:
        return None
    seg = s[m.start(): m.start() + 260]
    for pm in re.finditer(r"([-+]\d+(?:\.\d+)?)%", seg):
        tail = seg[pm.end(): pm.end() + 4]
        head = seg[max(0, pm.start() - 12): pm.start()]
        if "/yr" in tail or "CAGR" in seg[pm.end(): pm.end() + 12] or "CAGR" in head:
            continue
        return float(pm.group(1))
    return None


def parse_down_up(entry):
    s = entry.get("summary") or ""
    m = re.search(r"\(([\d.]+)% downside(?: to [^/]*?)? / \+?([\d.]+)% upside", s)
    if m:
        return float(m.group(1)), float(m.group(2))
    return None, None


# ─────────────────────────────────────────────────────────────────────────────
# Axis 2 — price state
# ─────────────────────────────────────────────────────────────────────────────
def price_state(rb, epp, adj, cons, verdict):
    """CHEAP / FAIR / RICH from the model's own numbers."""
    adj_v = adj if adj is not None else {
        "UNDERVALUED": 0.6, "MODESTLY UNDERVALUED": 0.3, "FAIRLY VALUED": 0.0,
        "MODESTLY OVERVALUED": -0.3, "OVERVALUED": -0.7}.get(verdict, 0.0)
    epp_v = epp if epp is not None else 60.0

    rich = (
        rb >= 2.0                                    # downside ≥ 2x upside
        or (rb >= 1.75 and adj_v < 0.2)              # poor asymmetry, no composite support
        or adj_v <= -0.5                             # model reads OVERVALUED outright
        or (epp_v > 100 and rb >= 1.0)               # far above floor with no asymmetry edge
        or (epp_v > 200 and (adj_v < 0.2 or rb >= 0.9))
        or (cons is not None and cons <= -15 and adj_v < 0.5)
    )
    if rich:
        return "RICH"

    cheap = (
        epp_v <= 100
        and adj_v > -0.45
        and (cons is None or cons > -5)
        and (
            epp_v <= 0
            or (rb <= 0.85 and (epp_v <= 40 or adj_v >= 0.3))
            or (adj_v >= 0.5 and rb <= 1.25)
            or (rb <= 0.5 and adj_v >= 0.0)
        )
    )
    return "CHEAP" if cheap else "FAIR"


def classify(entry):
    """Return the quality dict for one ticker entry (does not mutate)."""
    t = entry.get("ticker", "").upper()
    kind, risk, why = BUSINESS_PROFILES.get(t, (D, 3, "no curated profile yet — treated as durable/neutral"))
    rb = parse_ratio_b(entry)
    epp = _num(entry.get("epp_gap_pct"))
    adj = parse_adj_gap(entry)
    cons = parse_cons_return(entry)
    verdict = parse_verdict(entry)
    legacy = entry.get("legacy_signal_short") or entry.get("signal_short") or ""
    if legacy not in LEGACY_TIERS:
        legacy = entry.get("legacy_signal_short") or ""

    if legacy == "ACQUIRED" or kind == X:
        ps = price_state(rb, epp, adj, cons, verdict)
        key = "SPECIAL SITUATION"
    else:
        ps = price_state(rb, epp, adj, cons, verdict)
        if kind == D:
            key = {"CHEAP": "COMPOUNDER AT LOW PRICE", "FAIR": "QUALITY, NEUTRALLY VALUED",
                   "RICH": "QUALITY, PRICED FOR PERFECTION"}[ps]
        elif kind == C:
            key = {"CHEAP": "CYCLICAL, RISK PRICED IN", "FAIR": "CYCLICAL, NEUTRALLY VALUED",
                   "RICH": "TOO MUCH CYCLE RISK"}[ps]
        elif kind == S:
            key = "CHEAP, BUT STRUCTURAL RISK" if ps == "CHEAP" else "STRUCTURAL RISK, NOT CHEAP"
        else:  # TURNAROUND
            key = "TURNAROUND BET" if ps != "RICH" else "STRUCTURAL RISK, NOT CHEAP"

    c = CLASSES[key]
    bits = [f"{KIND_LABEL[kind]} (obsolescence risk {risk}/5)", f"price {ps.lower()}"]
    if rb != math.inf:
        bits.append(f"Ratio B {rb:.2f}x")
    if epp is not None:
        bits.append(f"{epp:+.0f}% to EPP floor")
    if adj is not None:
        bits.append(f"model-vs-market gap {adj:+.2f}")
    if cons is not None:
        bits.append(f"conservative 2yr {cons:+.0f}%")
    note = f"{why}. " + "; ".join(bits) + "."
    return {
        "quality_class": key,
        "quality_label": f"{c['icon']} {key}",
        "quality_color": c["color"],
        "quality_tone": c["tone"],
        "business_kind": kind,
        "obsolescence_risk": risk,
        "price_state": ps,
        "quality_note": note,
        "_rb": rb, "_epp": epp, "_adj": adj, "_cons": cons, "_verdict": verdict,
    }


_LEAD_RE = re.compile(
    r"^\s*(?:[A-Z0-9.]{1,7}(?:\s+10Y)?\s*)?[◉◎◐▷✕]?\s*(?:BUY|ACCUMULATE|WATCHLIST|HOLD/TRIM|HOLD|TRIM|AVOID)"
    r"(?:\s*\([^)]*\))?\s*(?:—|--|-|–|:)\s*")


def enrich(entry):
    """Mutate entry: add quality_* fields, move the legacy tier aside, and make
    signal / signal_short / signal_color carry the new class.  Idempotent."""
    if entry.get("signal_short") in LEGACY_TIERS or "legacy_signal_short" not in entry:
        if entry.get("signal_short") in LEGACY_TIERS:
            entry["legacy_signal_short"] = entry["signal_short"]
            entry["legacy_signal"] = entry.get("signal", "")
    q = classify(entry)
    for k, v in q.items():
        if not k.startswith("_"):
            entry[k] = v
    entry["signal_short"] = q["quality_class"]
    entry["signal"] = q["quality_label"]
    entry["signal_color"] = q["quality_color"]
    # Lead the summary with the new class so the narrative and the badge agree.
    summ = entry.get("summary") or ""
    summ = re.sub(r"^\s*[◉◎◐▷✕] (?:COMPOUNDER|QUALITY|CYCLICAL|TOO MUCH|CHEAP, BUT|STRUCTURAL RISK|TURNAROUND|SPECIAL)[^|]*\|\s*", "", summ)
    summ = _LEAD_RE.sub("", summ, count=1)
    entry["summary"] = f"{q['quality_label']} — {q['quality_note']} | {summ}".strip()
    # Header line of the full printed report: "Signal: ◐ WATCHLIST   Ratio B: ..."
    rep = entry.get("report")
    if isinstance(rep, str) and rep:
        rep = re.sub(r"Signal:\s*[◉◎◐▷✕]?\s*(?:COMPOUNDER|QUALITY|CYCLICAL|TOO MUCH|CHEAP, BUT|STRUCTURAL RISK|TURNAROUND|SPECIAL)[^\n]*?\[model tier: ([A-Z/]+)\]",
                     r"Signal: \1", rep, count=1)
        rep = re.sub(r"Signal:\s*[◉◎◐▷✕]?\s*(BUY|ACCUMULATE|WATCHLIST|HOLD/TRIM|HOLD|TRIM|AVOID)\b",
                     lambda m: f"Signal: {q['quality_label']}  [model tier: {m.group(1)}]", rep, count=1)
        entry["report"] = rep
    return entry


# ─────────────────────────────────────────────────────────────────────────────
# CLI helpers
# ─────────────────────────────────────────────────────────────────────────────
def load_dir(path):
    out = []
    for f in sorted(glob.glob(os.path.join(path, "*.json"))):
        with open(f, encoding="utf-8") as fh:
            out.append(json.load(fh))
    return out


def print_table(entries):
    rows = []
    for e in entries:
        q = classify(e)
        rows.append((q["quality_class"], e["ticker"], e.get("legacy_signal_short") or e.get("signal_short"),
                     e.get("sector_group", ""), q["_rb"], q["_epp"], q["_adj"], q["_cons"], q["business_kind"], q["obsolescence_risk"]))
    rows.sort(key=lambda r: (list(CLASSES).index(r[0]), r[1]))
    cur = None
    for r in rows:
        if r[0] != cur:
            cur = r[0]
            n = sum(1 for x in rows if x[0] == cur)
            print(f"\n=== {cur}  ({n})")
        rb = "inf" if r[4] == math.inf else f"{r[4]:.2f}"
        adj = "" if r[6] is None else f"{r[6]:+.2f}"
        cons = "" if r[7] is None else f"{r[7]:+.0f}%"
        print(f"  {r[1]:<6}{str(r[2]):<11}{r[3][:18]:<19}{r[8][:4]}/{r[9]}  rb={rb:<5} epp={r[5]!s:<7} adj={adj:<6} cons={cons}")


def _aws():
    import boto3
    key, sec = os.environ.get("AWS_Key"), os.environ.get("AWS_Pass")
    if not key or not sec:
        sys.exit("AWS_Key / AWS_Pass not set")
    kw = dict(aws_access_key_id=key, aws_secret_access_key=sec)
    return (boto3.client("s3", **kw), boto3.client("lambda", region_name="eu-north-1", **kw),
            boto3.client("cloudfront", **kw))


def apply_s3(dry=False):
    import io, time, urllib.request, zipfile, tempfile, shutil
    BUCKET, PREFIX, FN, DIST = "s3bucketmz", "veerock-signals/", "veerock-signal-api", "E15IJW4438D21G"
    s3, lam, cf = _aws()
    keys = [o["Key"] for o in s3.list_objects_v2(Bucket=BUCKET, Prefix=PREFIX, MaxKeys=1000).get("Contents", [])
            if o["Key"].endswith(".json")]
    changed = []
    for k in keys:
        body = json.loads(s3.get_object(Bucket=BUCKET, Key=k)["Body"].read())
        before = (body.get("signal_short"), body.get("quality_note"))
        enrich(body)
        if (body.get("signal_short"), body.get("quality_note")) != before:
            changed.append("/" + k)
            if not dry:
                s3.put_object(Bucket=BUCKET, Key=k, Body=json.dumps(body, ensure_ascii=False),
                              ContentType="application/json")
    print(f"S3 signals: {len(changed)} of {len(keys)} updated{' (dry)' if dry else ''}")

    # Lambda summary.json (served by GET /signals and reused by the 07:00 regen)
    cfg = lam.get_function(FunctionName=FN)
    work = tempfile.mkdtemp(prefix="quality_")
    try:
        zp = os.path.join(work, "live.zip")
        urllib.request.urlretrieve(cfg["Code"]["Location"], zp)
        ex = os.path.join(work, "x")
        with zipfile.ZipFile(zp) as z:
            z.extractall(ex)
        sp = os.path.join(ex, "summary.json")
        summary = json.load(open(sp, encoding="utf-8"))
        n = 0
        for t, e in summary.items():
            e.setdefault("ticker", t)
            before = (e.get("signal_short"), e.get("quality_note"))
            enrich(e)
            n += (e.get("signal_short"), e.get("quality_note")) != before
        print(f"Lambda summary.json: {n} of {len(summary)} entries updated")
        if not dry and n:
            json.dump(summary, open(sp, "w", encoding="utf-8"), ensure_ascii=False)
            # keep a copy of this module inside the package for future use
            shutil.copy(__file__, os.path.join(ex, "quality_classify.py"))
            dz = os.path.join(work, "deploy.zip")
            with zipfile.ZipFile(dz, "w", zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(ex):
                    dirs[:] = [d for d in dirs if d != "__pycache__"]
                    for fn in files:
                        if fn.endswith(".pyc"):
                            continue
                        full = os.path.join(root, fn)
                        zf.write(full, os.path.relpath(full, ex))
            lam.update_function_code(FunctionName=FN, ZipFile=open(dz, "rb").read())
            for _ in range(30):
                st = lam.get_function_configuration(FunctionName=FN)["LastUpdateStatus"]
                if st == "Successful":
                    print("Lambda redeployed OK")
                    break
                if st == "Failed":
                    sys.exit("Lambda update failed")
                time.sleep(2)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    if changed and not dry:
        cf.create_invalidation(DistributionId=DIST, InvalidationBatch={
            "Paths": {"Quantity": 1, "Items": ["/veerock-signals/*"]},
            "CallerReference": f"quality-{int(time.time())}"})
        print("CloudFront invalidation created for /veerock-signals/*")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", help="directory of veerock-signals JSONs to classify and tabulate")
    ap.add_argument("--write-local", help="write enriched copies of --local JSONs into this directory")
    ap.add_argument("--apply-s3", action="store_true")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    if a.local:
        entries = load_dir(a.local)
        print_table(entries)
        if a.write_local:
            os.makedirs(a.write_local, exist_ok=True)
            for e in entries:
                enrich(e)
                with open(os.path.join(a.write_local, f"{e['ticker']}.json"), "w", encoding="utf-8") as fh:
                    json.dump(e, fh, ensure_ascii=False, indent=1)
            print(f"wrote {len(entries)} enriched JSONs to {a.write_local}")
    if a.apply_s3:
        apply_s3(dry=a.dry)
    if not (a.local or a.apply_s3):
        ap.print_help()


if __name__ == "__main__":
    main()
