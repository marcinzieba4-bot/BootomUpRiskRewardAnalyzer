'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';

const API = 'https://7qc9qknegk.execute-api.eu-north-1.amazonaws.com';

const SCOLOR: Record<string, string> = {
  ACCUMULATE: 'text-amber-700 border-amber-500/40 bg-amber-500/10',
  WATCHLIST:  'text-blue-700  border-blue-500/40  bg-blue-500/10',
  AVOID:      'text-red-700   border-red-500/40   bg-red-500/10',
  BUY:        'text-green-700 border-green-500/40 bg-green-500/10',
};

export default function SignalDetailClient() {
  const params = useParams();
  const ticker = (params?.ticker as string ?? '').toUpperCase();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ticker) return;
    fetch(`${API}/signals/${ticker}`)
      .then(r => r.ok ? r.json() : null)
      .then(json => { setData(json); setLoading(false); })
      .catch(() => setLoading(false));
  }, [ticker]);

  const colorCls = data ? (SCOLOR[data.signal_short] ?? SCOLOR['AVOID']) : '';
  const report: string = data?.part2 && data?.part3
    ? data.part2 + '\n\n' + data.part3
    : data?.report ?? '';

  if (loading) {
    return (
      <div className="pt-28 pb-24 max-w-5xl mx-auto px-6">
        <div className="flex items-center gap-2 text-vr-faint text-xs mb-8">
          <Link href="/signals" className="hover:text-vr-gold transition-colors">Signals</Link>
          <span>›</span>
          <span className="text-vr-muted">{ticker}</span>
        </div>
        <div className="text-vr-muted text-center py-24 animate-pulse">Loading signal…</div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="pt-28 pb-24 max-w-5xl mx-auto px-6 text-center">
        <p className="text-vr-muted py-24">Signal not found.</p>
        <Link href="/signals" className="text-vr-gold hover:underline text-sm">← Back to all signals</Link>
      </div>
    );
  }

  return (
    <div className="pt-28 pb-24 max-w-5xl mx-auto px-6">

      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-vr-faint text-xs mb-8">
        <Link href="/signals" className="hover:text-vr-gold transition-colors">Signals</Link>
        <span>›</span>
        <span className="text-vr-muted">{data.ticker}</span>
      </div>

      {/* Hero */}
      <div className="mb-10">
        <div className="flex items-start justify-between flex-wrap gap-4 mb-4">
          <div>
            <h1 className="font-mono text-5xl font-bold text-vr-text">{data.ticker}</h1>
            <p className="text-vr-muted mt-1">{data.company}</p>
            <p className="text-vr-faint text-xs mt-0.5">{data.sector}</p>
          </div>
          <div className="text-right">
            <div className={`inline-block border rounded-xl px-4 py-2 text-2xl font-bold font-mono ${colorCls}`}>
              {data.signal}
            </div>
            <div className="text-vr-muted text-sm mt-2 font-mono">${data.price} · {data.date}</div>
          </div>
        </div>
        <p className="text-vr-muted leading-relaxed max-w-2xl">{data.summary}</p>
      </div>

      {/* Key metrics */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-10">
        {[
          { label: 'Current Price',    value: data.sector?.includes('Prices in EUR') ? `€${data.price}` : data.sector?.includes('Prices in PLN') ? `PLN ${data.price}` : `$${data.price}` },
          { label: 'EPP Gap',          value: `${data.epp_gap_pct > 0 ? '+' : ''}${data.epp_gap_pct}%` },
          { label: 'Ratio B (Method)', value: data.ratio_b_fmt },
        ].map(({ label, value }) => (
          <div key={label} className="rounded-xl border border-vr-border bg-vr-card p-4 text-center">
            <div className="text-vr-text font-bold text-xl font-mono">{value}</div>
            <div className="text-vr-faint text-xs mt-1">{label}</div>
          </div>
        ))}
      </div>

      <div className="gold-divider mb-10" />

      {/* Full analyst report */}
      {report && report !== data.summary ? (
        <section className="mb-12">
          <h2 className="font-serif text-xl font-bold text-vr-text mb-6">Analyst Report</h2>
          <div className="rounded-xl border border-vr-border bg-vr-surface overflow-hidden">
            <pre className="p-6 text-xs leading-relaxed text-vr-muted font-mono overflow-x-auto whitespace-pre-wrap break-words">
              {report}
            </pre>
          </div>
        </section>
      ) : null}

      {/* Disclaimer */}
      <div className="mb-10 p-4 rounded-xl border border-vr-border bg-vr-card/50">
        <p className="text-vr-faint text-xs text-center">
          <span className="text-vr-gold font-semibold">EPP</span> = pessimistic P/E × current EPS (floor, not target).{' '}
          <span className="text-vr-gold font-semibold">Ratio B</span> = downside to EPP ÷ upside at conservative exit multiple.
          All prices USD. Not financial advice.
        </p>
      </div>

      <Link href="/signals" className="inline-flex items-center gap-2 text-vr-muted hover:text-vr-gold transition-colors text-sm">
        ← Back to all signals
      </Link>
    </div>
  );
}
