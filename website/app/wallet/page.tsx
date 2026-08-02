const walletFeatures = [
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
        <circle cx="11" cy="11" r="9" stroke="#d4a853" strokeWidth="1.5" />
        <path d="M7 11l3 3 5-5" stroke="#d4a853" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    label: 'Read-only connection — non-custodial, no signing rights ever granted',
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
        <rect x="3" y="3" width="16" height="16" rx="3" stroke="#d4a853" strokeWidth="1.5" />
        <path d="M7 11h8M11 7v8" stroke="#d4a853" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
    label: 'Full portfolio snapshot across all connected chains',
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
        <path d="M11 3v4M11 15v4M3 11h4M15 11h4" stroke="#d4a853" strokeWidth="1.5" strokeLinecap="round" />
        <circle cx="11" cy="11" r="4" stroke="#d4a853" strokeWidth="1.5" />
      </svg>
    ),
    label: '6-dimensional risk score with drill-down explanations',
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
        <path d="M3 17l5-5 4 4 7-9" stroke="#d4a853" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    label: 'Bespoke action recommendations ranked by urgency and impact',
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 22 22" fill="none">
        <path d="M11 2L13.5 8.5H20L14.5 12.5L16.5 19L11 15.5L5.5 19L7.5 12.5L2 8.5H8.5L11 2Z" stroke="#d4a853" strokeWidth="1.5" strokeLinejoin="round" />
      </svg>
    ),
    label: 'Watchlist monitoring — alerts on material wallet state changes',
  },
];

const supportedWallets = [
  'MetaMask', 'Ledger', 'Coinbase Wallet', 'WalletConnect', 'Rabby', 'Safe (Gnosis)',
];

export default function WalletPage() {
  return (
    <div className="pt-28 pb-24 max-w-7xl mx-auto px-6">

      <div className="max-w-3xl mx-auto text-center mb-16">
        {/* Status badge */}
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-vr-gold/30 bg-vr-gold/5 text-vr-gold text-xs font-semibold tracking-wider uppercase mb-8">
          <span className="w-1.5 h-1.5 rounded-full bg-vr-gold animate-pulse" />
          In Development — Launching Soon
        </div>

        <h1 className="font-serif text-4xl md:text-5xl font-bold text-vr-text mb-5">
          Wallet Intelligence Engine
        </h1>
        <p className="text-vr-muted text-lg leading-relaxed">
          Connect your wallet and let ZembiHF\'s four-phase analytical pipeline scan your
          positions, quantify your risk exposure, and surface bespoke on-chain recommendations —
          built for your exact portfolio, not generic advice.
        </p>
      </div>

      {/* Mock wallet connect UI */}
      <div className="max-w-lg mx-auto mb-20">
        <div className="rounded-2xl border border-vr-border bg-vr-card p-8">
          <h2 className="font-serif text-xl font-bold text-vr-text mb-6 text-center">
            Connect Your Wallet
          </h2>

          <div className="space-y-3 mb-6">
            {supportedWallets.map((w) => (
              <button
                key={w}
                disabled
                className="w-full flex items-center gap-4 px-5 py-3.5 rounded-xl border border-vr-border bg-vr-surface text-vr-faint text-sm font-medium cursor-not-allowed opacity-60 hover:border-vr-gold/30 transition-colors"
              >
                <span className="w-8 h-8 rounded-lg bg-vr-border flex items-center justify-center text-xs font-bold text-vr-faint">
                  {w.slice(0, 2).toUpperCase()}
                </span>
                {w}
                <span className="ml-auto text-xs text-vr-faint/60">Coming soon</span>
              </button>
            ))}
          </div>

          <p className="text-vr-faint text-xs text-center leading-relaxed">
            Non-custodial · Read-only · No private keys required
          </p>
        </div>
      </div>

      {/* Features */}
      <div className="max-w-3xl mx-auto">
        <h3 className="font-serif text-2xl font-bold text-vr-text mb-6 text-center">
          What You\'ll Get
        </h3>
        <div className="space-y-3">
          {walletFeatures.map(({ icon, label }) => (
            <div
              key={label}
              className="flex items-center gap-4 rounded-xl border border-vr-border bg-vr-card px-6 py-4"
            >
              <div className="shrink-0">{icon}</div>
              <p className="text-vr-muted text-sm">{label}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Waitlist CTA */}
      <div className="max-w-xl mx-auto mt-16 rounded-2xl border border-vr-gold/20 bg-vr-gold/5 p-8 text-center">
        <h3 className="font-serif text-xl font-bold text-vr-text mb-2">
          Be First When We Launch
        </h3>
        <p className="text-vr-muted text-sm mb-6">
          Early access users receive free premium tier access for the first 90 days.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <input
            type="email"
            placeholder="your@email.com"
            className="px-4 py-2.5 rounded-lg bg-vr-surface border border-vr-border text-vr-text text-sm placeholder:text-vr-faint focus:outline-none focus:border-vr-gold flex-1 min-w-0"
          />
          <button className="px-5 py-2.5 bg-vr-gold text-vr-bg font-semibold rounded-lg hover:bg-vr-gold-light transition-colors text-sm shrink-0">
            Join Waitlist
          </button>
        </div>
      </div>
    </div>
  );
}
