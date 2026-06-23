'use client';

import { Suspense, useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';

const API = 'https://7qc9qknegk.execute-api.eu-north-1.amazonaws.com';

const SIGNAL_META: Record<string, { icon: string; bg: string; border: string; text: string }> = {
  ACCUMULATE: { icon: '◎', bg: 'bg-amber-500/10', border: 'border-amber-500/30', text: 'text-amber-400' },
  WATCHLIST:  { icon: '◐', bg: 'bg-blue-500/10',  border: 'border-blue-500/30',  text: 'text-blue-400'  },
  AVOID:      { icon: '✕', bg: 'bg-red-500/10',   border: 'border-red-500/30',   text: 'text-red-400'   },
  BUY:        { icon: '◉', bg: 'bg-green-500/10', border: 'border-green-500/30', text: 'text-green-400' },
  HOLD:       { icon: '◇', bg: 'bg-gray-500/10',  border: 'border-gray-500/30',  text: 'text-gray-400'  },
};

const SIGNAL_ORDER = ['BUY', 'ACCUMULATE', 'WATCHLIST', 'AVOID', 'HOLD'] as const;

const CURRENCY_SYMBOL: Record<string, string> = { EUR: '€', PLN: 'PLN ', USD: '$' };
function currencySymbol(s: any): string {
  if (s?.currency) return CURRENCY_SYMBOL[s.currency] ?? `${s.currency} `;
  if (s?.sector?.includes('Prices in EUR')) return '€';
  if (s?.sector?.includes('Prices in PLN')) return 'PLN ';
  return '$';
}

const SECTOR_ORDER = [
  'Technology',
  'Healthcare',
  'Industrials',
  'Consumer Discretionary',
  'Consumer Staples',
  'Energy',
  'Utilities',
  'Basic Resources',
  'Materials',
  'Finance',
  'Telecoms/Media',
];

const SECTOR_ICONS: Record<string, string> = {
  'Technology':             '⬡',
  'Healthcare':             '✦',
  'Industrials':            '◈',
  'Consumer Discretionary': '◇',
  'Consumer Staples':       '◆',
  'Energy':                 '◎',
  'Utilities':              '○',
  'Basic Resources':        '◉',
  'Materials':              '▲',
  'Finance':                '◐',
  'Telecoms/Media':         '◑',
};

export default function SignalsPage() {
  return (
    <Suspense fallback={<div className="pt-28 pb-24 max-w-7xl mx-auto px-6 text-vr-muted text-center">Loading…</div>}>
      <SignalsPageInner />
    </Suspense>
  );
}

function SignalsPageInner() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [signals, setSignals] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const selectedSector = searchParams.get('sector');

  const selectSector = (sector: string | null) => {
    if (sector === null) {
      router.push('/signals');
    } else {
      router.push(`/signals?sector=${encodeURIComponent(sector)}`);
    }
  };

  useEffect(() => {
    fetch(`${API}/signals`)
      .then(r => r.json())
      .then(json => {
        setSignals(json.signals ?? []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  // Group by sector_group
  const sectorMap: Record<string, any[]> = {};
  for (const s of signals) {
    const sg = s.sector_group ?? 'Other';
    if (!sectorMap[sg]) sectorMap[sg] = [];
    sectorMap[sg].push(s);
  }
  const orderedSectors = [
    ...SECTOR_ORDER.filter(s => sectorMap[s]),
    ...Object.keys(sectorMap).filter(s => !SECTOR_ORDER.includes(s)),
  ];

  const sectorStocks = selectedSector ? (sectorMap[selectedSector] ?? []) : [];

  return (
    <div className="pt-28 pb-24 max-w-7xl mx-auto px-6">

      {/* Header */}
      <div className="mb-14">
        <div className="flex items-center gap-2 mb-4">
          <span className="w-6 h-px bg-vr-gold" />
          <span className="text-vr-gold text-xs font-semibold tracking-widest uppercase">
            BottomUp Risk/Reward
          </span>
        </div>
        <h1 className="font-serif text-4xl md:text-5xl font-bold text-vr-text mb-4">
          Equity Signal Models
        </h1>
        <p className="text-vr-muted text-lg max-w-2xl">
          Fundamental stock analysis using the EPP floor framework. Each signal is driven by
          earnings quality, cross-read composites, and attractiveness ratios — not price targets.
        </p>
      </div>

      {/* Framework callout */}
      <div className="rounded-xl border border-vr-border bg-vr-card p-6 mb-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
          {[
            { label: '◉ BUY',        note: 'Ratio B < 0.75x',   desc: 'Floor gap dominated by upside' },
            { label: '◎ ACCUMULATE', note: 'Ratio B 0.75–1.1x', desc: 'Balanced; edge to upside' },
            { label: '◐ WATCHLIST',  note: 'Ratio B 1.1–1.75x', desc: 'Floor gap exceeds EPS upside' },
            { label: '✕ AVOID',      note: 'Ratio B > 1.75x',   desc: 'Growth fully priced in' },
          ].map(({ label, note, desc }) => (
            <div key={label} className="p-3 rounded-lg bg-vr-bg/50">
              <div className="font-mono text-vr-gold font-bold text-sm mb-1">{label}</div>
              <div className="text-vr-text text-xs font-medium mb-0.5">{note}</div>
              <div className="text-vr-faint text-xs">{desc}</div>
            </div>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="text-vr-muted text-center py-16">Loading signals…</div>
      ) : selectedSector === null ? (
        /* ── SECTOR GRID ── */
        <>
          <div className="flex items-center gap-3 mb-6">
            <span className="text-vr-text font-serif text-2xl font-bold">Sectors</span>
            <span className="text-vr-faint text-sm">— click to explore stocks</span>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5 mb-14">
            {orderedSectors.map(sector => {
              const stocks = sectorMap[sector];
              const counts: Record<string, number> = {};
              for (const s of stocks) {
                counts[s.signal_short] = (counts[s.signal_short] ?? 0) + 1;
              }
              const icon = SECTOR_ICONS[sector] ?? '◌';
              return (
                <button
                  key={sector}
                  onClick={() => selectSector(sector)}
                  className="card-hover rounded-xl border border-vr-border bg-vr-card p-6 flex flex-col text-left group transition-all"
                >
                  <div className="flex items-center gap-3 mb-4">
                    <span className="text-vr-gold text-2xl leading-none">{icon}</span>
                    <div>
                      <div className="font-serif text-vr-text font-bold text-lg group-hover:text-vr-gold transition-colors">
                        {sector}
                      </div>
                      <div className="text-vr-faint text-xs mt-0.5">
                        {stocks.length} {stocks.length === 1 ? 'stock' : 'stocks'}
                      </div>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2 mt-auto">
                    {SIGNAL_ORDER.map(sig => {
                      const n = counts[sig];
                      if (!n) return null;
                      const m = SIGNAL_META[sig];
                      return (
                        <span
                          key={sig}
                          className={`text-[11px] font-semibold px-2 py-0.5 rounded-full border ${m.bg} ${m.border} ${m.text}`}
                        >
                          {m.icon} {n} {sig}
                        </span>
                      );
                    })}
                  </div>
                </button>
              );
            })}
          </div>
        </>
      ) : (
        /* ── SECTOR DETAIL ── */
        <>
          <div className="flex items-center gap-4 mb-8">
            <button
              onClick={() => selectSector(null)}
              className="flex items-center gap-1.5 text-vr-gold hover:text-vr-text transition-colors text-sm font-medium"
            >
              ← All Sectors
            </button>
            <span className="text-vr-border">|</span>
            <span className="font-serif text-vr-text text-2xl font-bold">{selectedSector}</span>
            <span className="text-vr-faint text-sm">
              {sectorStocks.length} {sectorStocks.length === 1 ? 'stock' : 'stocks'}
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sectorStocks.map((s: any) => {
              const meta = SIGNAL_META[s.signal_short] ?? SIGNAL_META['AVOID'];
              return (
                <Link
                  key={s.ticker}
                  href={`/signals/${s.ticker.toLowerCase()}`}
                  className="card-hover rounded-xl border border-vr-border bg-vr-card p-6 flex flex-col group"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <span className="font-mono text-2xl font-bold text-vr-text group-hover:text-vr-gold transition-colors">
                        {s.ticker}
                      </span>
                      <p className="text-vr-muted text-xs mt-0.5">{s.company}</p>
                    </div>
                    <span className={`badge border px-2.5 py-1 rounded-full text-xs font-semibold ${meta.bg} ${meta.border} ${meta.text}`}>
                      {meta.icon} {s.signal_short}
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-2 mb-4">
                    <div className="bg-vr-bg/60 rounded-lg p-2 text-center">
                      <div className="text-vr-text font-semibold text-sm">{currencySymbol(s)}{s.price}</div>
                      <div className="text-vr-faint text-[10px] mt-0.5">Price</div>
                    </div>
                    <div className="bg-vr-bg/60 rounded-lg p-2 text-center">
                      <div className="text-vr-text font-semibold text-sm">+{s.epp_gap_pct}%</div>
                      <div className="text-vr-faint text-[10px] mt-0.5">EPP Gap</div>
                    </div>
                    <div className="bg-vr-bg/60 rounded-lg p-2 text-center">
                      <div className="text-vr-text font-semibold text-sm font-mono">{s.ratio_b_fmt}</div>
                      <div className="text-vr-faint text-[10px] mt-0.5">Ratio B</div>
                    </div>
                  </div>

                  <p className="text-vr-muted text-sm leading-relaxed flex-1 mb-4">{s.summary}</p>

                  <div className="flex items-center justify-between text-vr-faint text-xs pt-3 border-t border-vr-border">
                    <span>{s.date}</span>
                    <span className="text-vr-gold group-hover:underline">Full analysis →</span>
                  </div>
                </Link>
              );
            })}
          </div>
        </>
      )}

      <div className="mt-14 p-6 rounded-xl border border-vr-border bg-vr-card/50">
        <p className="text-vr-muted text-sm text-center">
          <span className="text-vr-gold font-semibold">EPP</span> (Earnings Power Price) = current EPS × min-viable trough P/E.{' '}
          <span className="text-vr-gold font-semibold">Ratio B</span> = downside to EPP ÷ upside at conservative exit multiple.{' '}
          Primary signal is Method B. Prices shown in each company's primary listing currency. Not financial advice.
        </p>
      </div>
    </div>
  );
}
