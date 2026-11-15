# SO retrospective findings (hindsight)

Patterns seen in `outcome.json` for the SO weekly dates: 105 from 2008-01-04 to 2009-12-31, all The Southern Company (NYSE: SO). They are
**labels and hypotheses**: never feed them back into the method or the fact sheet. The batch was scored only after its point-in-time build
was committed (db1a562) and its decisions, controls, leak scan, sensitivities and firewall result were written to the README and committed
(fe0a6be); the outcomes were computed on 2026-11-15. After the scoring the ten release titles were renamed to the repository's form
("Southern Company Q3 2007 results (8-K, ...)") so that `SERIES.md` names the latest print; text only, and every class, tier and metric
was checked identical. Every date has its 6-month, 1-, 2- and 3-year horizons (the last ends 2012-12-31). Total returns include the
quarterly dividends ($0.4025 from the ex-date of 2008-01-31, $0.42 from 2008-05-01, $0.4375 from 2009-04-30, $0.455 from 2010-04-29,
$0.4725 from 2011-04-28, $0.49 from 2012-05-03): $3.12-3.68 a share over two years, 8.6-13.2% of the entry price. No split or
distribution falls in any horizon, so every price is as traded. Medians of an even count take the upper middle value
(`statistics.median_high`). The 15%/yr hurdle is +32.2% over two years and +52.1% over three. "Call held" is `call_check_2y`: CHEAP should
clear the hurdle or beat the benchmark (SPY), FAIR should land within ±15pp of the benchmark, and RICH should miss the hurdle and lag the
benchmark. The 2008 table runs to 2008-12-26; 2009-01-02 closes the ISO week of 2008-12-29 and sits in the 2009 table.

## 2008 (52 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 15 | +7.7% | +1.9% to +27.7% | 0 | 12 | -7.1% | 12 |
| class CHEAP, legacy tier ACCUMULATE | 5 | +3.0% | -0.1% to +9.4% | 0 | 5 | -10.5% | 5 |
| class FAIR, legacy tier ACCUMULATE | 5 | +5.1% | +3.0% to +7.9% | 0 | 5 | -11.7% | 0 |
| class RICH, legacy tier BUY | 11 | +15.6% | -3.3% to +20.8% | 0 | 3 | -2.8% | 8 |
| class RICH, legacy tier ACCUMULATE | 9 | +2.9% | -2.6% to +12.9% | 0 | 8 | -12.6% | 1 |
| class RICH, legacy tier WATCHLIST | 4 | +2.9% | +0.3% to +6.1% | 0 | 4 | -13.4% | 0 |
| class RICH, legacy tier AVOID | 3 | -5.3% | -7.8% to -2.7% | 0 | 3 | -19.0% | 0 |
| FY07E = FY06's $2.10 (2008-01-04 to 2008-01-25) | 4 | -2.7% | -7.8% to +0.3% | 0 | 4 | -17.2% | 0 |
| FY08E = FY07's $2.29 (Q4 2007 release) (2008-01-31 to 2008-02-22) | 4 | -2.6% | -3.3% to +0.7% | 0 | 4 | -12.8% | 0 |
| FY08E = FY07's $2.28 (FY2007 10-K) (2008-02-29 to 2008-12-26) | 44 | +6.5% | -0.1% to +27.7% | 0 | 32 | -8.9% | 26 |
| latest print Q3 2007 (2008-01-04 to 2008-01-25) | 4 | -2.7% | -7.8% to +0.3% | 0 | 4 | -17.2% | 0 |
| latest print Q4 2007 (2008-01-31 to 2008-04-25) | 13 | +1.3% | -3.3% to +4.2% | 0 | 13 | -12.9% | 3 |
| latest print Q1 2008 (2008-05-01 to 2008-07-25) | 13 | +4.0% | -0.1% to +12.0% | 0 | 13 | -7.7% | 10 |
| latest print Q2 2008 (2008-07-31 to 2008-10-17) | 12 | +7.9% | +3.9% to +27.7% | 0 | 10 | -10.1% | 4 |
| latest print Q3 2008 (2008-10-24 to 2008-12-26) | 10 | +16.9% | +12.9% to +20.8% | 0 | 0 | -2.4% | 9 |

- **CHEAP held on 17 of its 20 dates, by beating a falling SPY, never by the hurdle.** The CHEAP dates of 2008 ($32.26-37.15, 14.1-16.3x
  FY07's $2.28) returned -0.1% to +27.7% over two years, dividends included, while SPY returned -18.7% to +36.8%; 17 beat it, none cleared
  the 32.2% hurdle, and the return to the m12-24 average price was -11.9% to +5.0%. The three misses are the CHEAP dates of October 2008
  after the crash (2008-10-10, 2008-10-17, 2008-10-31: +20.6% to +27.7%, 6-9pp behind SPY's rebound from its March 2009 low).
- **The RICH calls of January and February 2008 missed on all eight, though the stock fell.** On FY06's $2.10 (17.2-18.9x, AVOID on three)
  and then on the Q4 2007 print (15.5-15.9x), the eight dates returned -7.8% to +0.7% over two years and their m12-24 average price was
  12-21% under the entry, but SPY fell 10-18%, so each beat it by 7-16pp and the call (miss the hurdle and lag the benchmark) missed. Over
  three years they returned +8.2% to +21.5%, 12-19pp ahead of SPY. Every one sat through a 32-34% drawdown to the 2009-03-12 low ($26.81).
- **The other RICH dates of 2008 held on 9 of 19, FAIR on none of 5.** The RICH calls held where SPY's 2009-2010 rebound outran SO (the
  dates of late October to December 2008) and missed where SO beat a falling SPY (March-April and August-September 2008, +0.9% to +6.5%);
  the five FAIR dates returned +3.0% to +7.9% and beat SPY by 15-21pp, outside the ±15pp band. After two years the 2008 dates landed at the
  BEAR (28) or BASE (24) scenario price.
- **The anchor lagged and the multiple was set by Mirant.** Both the four January dates on FY06's $2.10 (FY07 came in at $2.28) and the
  14x floor ($29.40-32.06, from yearly lows that include 1998-1999 at 16.6-17.1x with Mirant in the price) proved too high for the 2009
  low ($26.81, 11.9x FY08's $2.25). Hypothesis, not a rule: a window that spans a large spin-off and keeps the pre-spin prices sets the
  floor and the median too high; test it on other tickers with spin-offs inside the window (BMY's started after Zimmer), never fit it to SO.

## 2009 (53 dates)

| Group | Dates | Median 2-yr total return | Range | Cleared 15%/yr hurdle | Beat SPY | Median m12-24 avg price | Call held |
|---|---|---|---|---|---|---|---|
| class CHEAP, legacy tier BUY | 13 | +35.9% | +20.8% to +54.2% | 11 | 0 | +18.7% | 11 |
| class RICH, legacy tier BUY | 39 | +43.1% | +17.1% to +59.1% | 36 | 28 | +22.1% | 3 |
| class RICH, legacy tier ACCUMULATE | 1 | +11.5% | +11.5% | 0 | 0 | -6.2% | 1 |
| FY08E = FY07's $2.28 (FY2007 10-K) (2009-01-02 to 2009-01-23) | 4 | +20.0% | +11.5% to +20.6% | 0 | 0 | +0.9% | 4 |
| FY09E = FY08's $2.26 (Q4 2008 release) (2009-01-29 to 2009-02-20) | 4 | +32.5% | +20.8% to +37.4% | 2 | 0 | +13.9% | 2 |
| FY09E = FY08's $2.25 (FY2008 10-K) (2009-02-27 to 2009-12-31) | 45 | +43.0% | +32.7% to +59.1% | 45 | 28 | +22.1% | 9 |
| latest print Q3 2008 (2009-01-02 to 2009-01-23) | 4 | +20.0% | +11.5% to +20.6% | 0 | 0 | +0.9% | 4 |
| latest print Q4 2008 (2009-01-29 to 2009-04-24) | 13 | +35.9% | +20.8% to +54.2% | 11 | 0 | +18.7% | 11 |
| latest print Q1 2009 (2009-04-30 to 2009-07-24) | 13 | +43.1% | +34.9% to +59.1% | 13 | 6 | +23.7% | 0 |
| latest print Q2 2009 (2009-07-30 to 2009-10-23) | 13 | +42.6% | +35.6% to +45.6% | 13 | 12 | +21.9% | 0 |
| latest print Q3 2009 (2009-10-29 to 2009-12-31) | 10 | +48.2% | +41.0% to +50.8% | 10 | 10 | +24.2% | 0 |

- **The January 2009 RICH calls held** (2009-01-02 to 2009-01-23, the Q3 2008 print, $34.65-37.47): +11.5% to +20.6% over two years,
  29-39pp behind SPY's rebound, under the hurdle.
- **CHEAP from the Q4 2008 print to 2009-04-24 held on 11 of 13, all by the hurdle.** At $27.14-33.86 (12.1-15.0x, the 0th-32nd percentile,
  around a 13-14x floor) the 13 dates returned +20.8% to +54.2% over two years; 11 cleared the hurdle, none kept up with SPY's +55.9% to
  +98.7% from its lows. The two misses are the first two (2009-01-29 and 2009-02-06: +20.8% and +21.8%). Over three years they returned
  +47.7% to +87.5%.
- **RICH from the Q1 2009 print missed on all 36 dates, while the tier said BUY.** At $27.70-34.22 (12.3-15.2x FY08's $2.25, the
  0th-45th percentile of the window; Ratio B -0.25 to 0.47, the price under the BEAR case on 9) the 36 dates returned +34.9% to +59.1% over
  two years, dividends included: every one over the hurdle and 28 ahead of SPY. Over three years they returned +43.8% to +84.4%, all 36
  ahead of SPY by 8-35pp, 31 over the three-year hurdle; the largest drawdown inside two years was 9%. The class came from the adjusted gap:
  the proxy composite (1.30-1.95) read the recession in the quarter (retail kWh -5.1% to -6.6%, the electric utilities' net income down,
  revenue down with fuel recovery), BASE turned negative with revenue as reported (-1.8% to -15.0%/yr), and the market composite rose to
  2.2-3.7. After two years the 2009 dates landed at the BULL (32), BASE (14), XBULL (4) or BEAR (3) scenario price.

## Across the two years

- **Calls held on 41 of 105:** CHEAP 28 of 33, FAIR 0 of 5, RICH 13 of 67. The RICH class carries the misses: in 2008 the stock lost less
  than a falling market, in 2009 it rose from the low with it.
- **The ranks run through the price, not the signals.** Across the 105 dates Ratio B ranks the two-year return at Spearman -0.88 and the
  return to the m12-24 average price at -0.95, the entry price at -0.83 and -0.91, the EPP gap at -0.64 and -0.77 (the right signs); the
  adjusted gap at -0.29 and -0.21 and the proxy composite at -0.73 and -0.76 (the wrong sign: the strongest signal readings came before the
  worst returns, the weakest at the low). Within 2008 Ratio B ranks at -0.65 and -0.89, within 2009 at -0.46 and -0.74.
- **The measured calls, scored (hindsight; the README's sensitivities were computed before any outcome).** Keeping Yahoo's Mirant factor
  would have held 28 calls instead of 41, the company's EPS excluding synthetic fuels and items 35, BASE on retail non-fuel revenue 41;
  every signal at its XBULL value, a bracket rather than an encoding, 84. The misses do not come from the encoded judgement calls but from
  the signals' reading of the recession.
- **Profile drift:** the models' DURABLE, risk 2, against today's profile of DURABLE, risk 1 (`outcome.json`; label only).

Hypotheses for the live model (test them on other tickers and periods; never fold them into this archive):
- For a regulated utility the quarter's operating signals (retail sales, segment earnings, revenue and a margin that fuel recovery moves)
  are coincident with a recession and contrarian at its trough: the weakest proxy came at the price low.
- When the tier and the class disagree (BUY and RICH on 39 dates of 2009), Ratio B and the multiple's percentile were right here.
- In a falling market the CHEAP call "holds" by beating SPY with a flat return: none of SO's 2008 CHEAP dates cleared the hurdle; the
  benchmark leg flatters a defensive stock in a bear market and penalizes it in a rebound.
