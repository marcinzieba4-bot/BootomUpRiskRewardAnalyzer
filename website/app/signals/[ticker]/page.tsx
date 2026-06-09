import SignalDetailClient from './SignalDetailClient';

const API = 'https://7qc9qknegk.execute-api.eu-north-1.amazonaws.com';

// Hardcoded fallback list ensures pages are pre-generated even if the API
// is unreachable at build time. Keep in sync with lambda_function.py SUMMARY.
const KNOWN_TICKERS = [
  'ISRG','MSFT','MU','WMB','AAPL','TSLA','SO','NVDA','HD','LRCX','AVGO','MCD',
  'CRM','ORCL','CSCO','SAP','NOW','ACN','KTY','IBM','AMD','ADBE','INTU','QCOM',
  'TXN','PANW','PLTR','INTC','CAT','MRVL','DHR','PFE','ABT','TMO','MRK','ABBV',
  'JNJ','UNH','LLY','PKN','SYK','BSX','AMGN','ELV','VRTX','GILD','BMY','MA','V',
  'JPM','AXP','GS','WFC','SPGI','PGR','C','BX','FISV','SCHW','MRSH','CB','KKR',
  'PYPL','LIN','APD','SHW','PPG','FCX','ECL','BLK','MS','BAC','BRK','NEM','VMC',
  'CTVA','DOW','LYB','NFLX','GOOGL','META','KNEBV','DNP','T','TTWO','CMCSA','TMUS','VZ','EA','CHTR','WBD','PSX','OKE','XOM','COP','CVX','SLB','KMI','MPC','BKR','TRGP','VLO','OXY','FANG','HAL','DVN','GE','RTX','HON','UNP','ETN','BA','UBER','DE','LMT','GEV','UPS','TT','PH','WM','TDG','EMR','MMM','COST','WMT','DSV','PG','KO','PEP',
];

export async function generateStaticParams() {
  try {
    const res = await fetch(`${API}/signals`, { cache: 'no-store' });
    const data = await res.json();
    const tickers: string[] = (data.signals ?? []).map((s: { ticker: string }) => s.ticker);
    if (tickers.length > 0) {
      return tickers.map(t => ({ ticker: t.toLowerCase() }));
    }
  } catch {
    // fall through to hardcoded list
  }
  return KNOWN_TICKERS.map(t => ({ ticker: t.toLowerCase() }));
}

export default function SignalDetailPage() {
  return <SignalDetailClient />;
}
