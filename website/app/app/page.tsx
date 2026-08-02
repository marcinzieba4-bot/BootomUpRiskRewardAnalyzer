import Link from 'next/link';

const supportedWallets = [
  { name: 'MetaMask',       abbr: 'MM' },
  { name: 'Ledger',         abbr: 'LG' },
  { name: 'Coinbase Wallet',abbr: 'CB' },
  { name: 'WalletConnect',  abbr: 'WC' },
  { name: 'Rabby',          abbr: 'RB' },
  { name: 'Safe (Gnosis)',  abbr: 'SF' },
];

const tiers = [
  {
    name: 'Explorer',
    price: 'Free',
    desc: 'Public research access',
    features: ['All published research', 'Market commentary', 'Newsletter'],
    cta: 'Current Plan',
    active: true,
    payment: null,
  },
  {
    name: 'Analyst',
    price: '$149/mo',
    desc: 'Full analytics + wallet engine',
    features: ['Wallet Intelligence Engine', '6-dimension risk scoring', 'Action recommendations', 'Webhook alerts'],
    cta: 'Pay with Crossmint',
    active: false,
    payment: 'crossmint',
  },
  {
    name: 'Institutional',
    price: 'Custom',
    desc: 'Enterprise API + dedicated support',
    features: ['Multi-wallet aggregation', 'Custom risk parameters', 'REST + WebSocket API', 'SLA + dedicated analyst'],
    cta: 'Contact Sales',
    active: false,
    payment: null,
  },
];

export default function AppPage() {
  return (
    <div className="min-h-screen pt-16 bg-vr-bg">

      {/* App topbar */}
      <div className="border-b border-vr-border bg-vr-surface/60 sticky top-16 z-40">
        <div className="max-w-7xl mx-auto px-6 h-11 flex items-center gap-6">
          {['Wallet', 'Portfolio', 'Alerts', 'Services'].map((tab, i) => (
            <button
              key={tab}
              className={`text-xs font-semibold pb-0.5 border-b-2 transition-colors ${
                i === 0
                  ? 'border-vr-gold text-vr-gold'
                  : 'border-transparent text-vr-faint hover:text-vr-muted'
              }`}
            >
              {tab}
            </button>
          ))}
          <div className="ml-auto flex items-center gap-2 text-vr-faint text-xs">
            <span className="w-1.5 h-1.5 rounded-full bg-vr-green" />
            Live
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* ── LEFT: Wallet Connect ── */}
          <div className="lg:col-span-5 space-y-5">

            {/* Connect panel */}
            <div className="rounded-2xl border border-vr-border bg-vr-card p-7">
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-bold text-vr-text">Connect Wallet</h2>
                <span className="badge bg-vr-gold/10 text-vr-gold border border-vr-gold/20">
                  Coming Soon
                </span>
              </div>

              <div className="space-y-2.5 mb-6">
                {supportedWallets.map(({ name, abbr }) => (
                  <button
                    key={name}
                    disabled
                    className="w-full flex items-center gap-4 px-4 py-3 rounded-xl border border-vr-border bg-vr-surface text-vr-faint text-sm cursor-not-allowed hover:border-vr-gold/20 transition-colors"
                  >
                    <span className="w-8 h-8 rounded-lg bg-vr-border flex items-center justify-center text-[10px] font-bold shrink-0">
                      {abbr}
                    </span>
                    <span className="font-medium">{name}</span>
                    <span className="ml-auto">
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                        <path d="M5 4l3 3-3 3" stroke="#8b90ab" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                      </svg>
                    </span>
                  </button>
                ))}
              </div>

              <p className="text-center text-vr-faint text-xs">
                Non-custodial · Read-only · No private keys
              </p>
            </div>

            {/* Risk preview (mock) */}
            <div className="rounded-2xl border border-vr-border bg-vr-card p-6">
              <h3 className="text-sm font-bold text-vr-muted mb-4 uppercase tracking-wider">
                Risk Snapshot Preview
              </h3>
              <div className="space-y-3">
                {[
                  { label: 'Concentration Risk', val: 72, color: 'bg-amber-500' },
                  { label: 'Counterparty Exposure', val: 34, color: 'bg-vr-green' },
                  { label: 'Protocol Risk', val: 55, color: 'bg-amber-500' },
                  { label: 'Liquidation Proximity', val: 18, color: 'bg-vr-green' },
                  { label: 'Cross-chain Leverage', val: 81, color: 'bg-red-500' },
                  { label: 'Oracle Exposure', val: 40, color: 'bg-vr-green' },
                ].map(({ label, val, color }) => (
                  <div key={label}>
                    <div className="flex justify-between text-xs text-vr-faint mb-1">
                      <span>{label}</span>
                      <span className="font-mono">{val}/100</span>
                    </div>
                    <div className="h-1.5 rounded-full bg-vr-border overflow-hidden">
                      <div
                        className={`h-full rounded-full ${color} opacity-60`}
                        style={{ width: `${val}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <p className="text-vr-faint/50 text-xs text-center mt-4 italic">
                — Connect wallet to see your actual scores —
              </p>
            </div>
          </div>

          {/* ── RIGHT: Services / Tiers ── */}
          <div className="lg:col-span-7 space-y-5">

            {/* Crossmint banner */}
            <div className="flex items-center gap-4 p-4 rounded-xl border border-vr-gold/20 bg-vr-gold/4">
              <div className="w-9 h-9 rounded-lg border border-vr-gold/25 bg-vr-gold/10 flex items-center justify-center shrink-0">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                  <path d="M9 1.5L17 5.5v7L9 16.5 1 12.5v-7L9 1.5Z" stroke="#9a6f12" strokeWidth="1.4" />
                  <path d="M6 9l2.5 2.5L12 6" stroke="#9a6f12" strokeWidth="1.4" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <div>
                <p className="text-vr-text text-sm font-semibold leading-tight">Powered by Crossmint</p>
                <p className="text-vr-faint text-xs">
                  Pay with ETH, USDC, SOL — or any credit / debit card. No crypto wallet required for card payments.
                </p>
              </div>
            </div>

            {/* Tier cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {tiers.map(({ name, price, desc, features, cta, active, payment }) => (
                <div
                  key={name}
                  className={`rounded-xl border p-5 flex flex-col ${
                    active
                      ? 'border-vr-gold/30 bg-vr-gold/5'
                      : 'border-vr-border bg-vr-card'
                  }`}
                >
                  <div className="mb-4">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm font-bold text-vr-text">{name}</span>
                      {active && (
                        <span className="badge bg-vr-green/10 text-vr-green border border-vr-green/20 text-[9px]">
                          Active
                        </span>
                      )}
                    </div>
                    <div className="font-bold text-vr-gold text-xl mb-0.5">{price}</div>
                    <p className="text-vr-faint text-xs">{desc}</p>
                  </div>
                  <ul className="space-y-1.5 flex-1 mb-5">
                    {features.map((f) => (
                      <li key={f} className="flex items-center gap-2 text-xs text-vr-faint">
                        <span className="w-1 h-1 rounded-full bg-vr-gold/60 shrink-0" />
                        {f}
                      </li>
                    ))}
                  </ul>
                  <button
                    disabled={!active && name !== 'Institutional'}
                    className={`w-full py-2.5 rounded-lg text-xs font-bold transition-colors ${
                      active
                        ? 'border border-vr-gold/30 text-vr-gold cursor-default'
                        : payment === 'crossmint'
                        ? 'bg-vr-border text-vr-faint cursor-not-allowed opacity-60'
                        : 'border border-vr-border text-vr-faint hover:border-vr-gold/30 hover:text-vr-muted cursor-not-allowed opacity-60'
                    }`}
                  >
                    {active ? cta : `${cta} — Soon`}
                  </button>
                </div>
              ))}
            </div>

            {/* Recommendations preview (mock) */}
            <div className="rounded-2xl border border-vr-border bg-vr-card p-6">
              <h3 className="text-sm font-bold text-vr-muted mb-4 uppercase tracking-wider">
                Sample Recommendations
              </h3>
              <div className="space-y-3">
                {[
                  { urgency: 'HIGH', color: 'text-red-700 bg-red-500/10 border-red-500/20', text: 'Reduce cross-chain leverage on Arbitrum positions — liquidation within 12% of current price.' },
                  { urgency: 'MED',  color: 'text-amber-700 bg-amber-500/10 border-amber-500/20', text: 'Rotate 18% USDC idle balance into short-duration yield on Base (est. +4.2% APY).' },
                  { urgency: 'LOW',  color: 'text-vr-green bg-vr-green/10 border-vr-green/20', text: 'ETH staking ratio below peer cohort median — consider increasing liquid staking allocation.' },
                ].map(({ urgency, color, text }) => (
                  <div key={urgency + text.slice(0, 10)} className="flex items-start gap-3 p-3.5 rounded-lg bg-vr-surface border border-vr-border/50">
                    <span className={`badge border shrink-0 mt-0.5 ${color}`}>{urgency}</span>
                    <p className="text-vr-faint text-xs leading-relaxed">{text}</p>
                  </div>
                ))}
              </div>
              <p className="text-vr-faint/50 text-xs text-center mt-4 italic">
                — Connect wallet to receive personalized recommendations —
              </p>
            </div>

          </div>
        </div>

        {/* Back to site */}
        <div className="mt-12 pt-8 border-t border-vr-border text-center">
          <Link href="/" className="text-vr-faint text-sm hover:text-vr-gold transition-colors">
            ← Back to ZembiHF.com
          </Link>
        </div>
      </div>
    </div>
  );
}
