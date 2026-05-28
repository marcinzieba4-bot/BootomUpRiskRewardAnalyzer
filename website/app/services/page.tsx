const tiers = [
  {
    name: 'Explorer',
    price: 'Free',
    period: '',
    desc: 'Public research and basic platform access.',
    features: [
      'Access to all published research',
      'Commentary & editorial feed',
      'Basic market overview',
      'Newsletter subscription',
    ],
    cta: 'Get Started',
    highlight: false,
    available: true,
  },
  {
    name: 'Analyst',
    price: '$149',
    period: '/ month',
    desc: 'Full research library and wallet analytics.',
    features: [
      'Everything in Explorer',
      'Full research archive & PDF export',
      'Wallet Intelligence Engine (Beta)',
      '6-dimension risk scoring',
      'Personalized action recommendations',
      'Email & webhook alerts',
    ],
    cta: 'Pay with Crossmint',
    highlight: true,
    available: false,
  },
  {
    name: 'Institutional',
    price: 'Custom',
    period: '',
    desc: 'Enterprise-grade analytics and dedicated support.',
    features: [
      'Everything in Analyst',
      'Multi-wallet portfolio aggregation',
      'Custom risk model parameters',
      'API access (REST + WebSocket)',
      'Dedicated analyst support',
      'SLA-backed uptime guarantees',
      'On-premise data delivery option',
    ],
    cta: 'Contact Sales',
    highlight: false,
    available: false,
  },
];

export default function ServicesPage() {
  return (
    <div className="pt-28 pb-24 max-w-7xl mx-auto px-6">

      {/* Header */}
      <div className="text-center mb-16">
        <div className="flex items-center justify-center gap-2 mb-4">
          <span className="w-6 h-px bg-vr-gold" />
          <span className="text-vr-gold text-xs font-semibold tracking-widest uppercase">
            Pricing & Access
          </span>
          <span className="w-6 h-px bg-vr-gold" />
        </div>
        <h1 className="font-serif text-4xl md:text-5xl font-bold text-vr-text mb-4">
          Services & Plans
        </h1>
        <p className="text-vr-muted text-lg max-w-xl mx-auto">
          Flexible access tiers for individual investors, researchers, and institutional teams.
          Paid plans powered by{' '}
          <span className="text-vr-gold font-semibold">Crossmint</span> — pay in crypto or card.
        </p>
      </div>

      {/* Crossmint banner */}
      <div className="flex items-center justify-center gap-4 mb-14 p-4 rounded-xl border border-vr-gold/20 bg-vr-gold/5 max-w-2xl mx-auto">
        <div className="w-10 h-10 rounded-lg bg-vr-gold/10 border border-vr-gold/20 flex items-center justify-center shrink-0">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 2L18 6v8L10 18 2 14V6L10 2Z" stroke="#d4a853" strokeWidth="1.5" />
            <path d="M6 10l3 3 5-5" stroke="#d4a853" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
        <div>
          <p className="text-vr-text text-sm font-semibold">Powered by Crossmint</p>
          <p className="text-vr-faint text-xs">
            Pay with ETH, USDC, SOL, or any major credit/debit card. No wallet required for
            card payments.
          </p>
        </div>
        <span className="badge bg-vr-gold/10 text-vr-gold border border-vr-gold/20 shrink-0">
          Coming Soon
        </span>
      </div>

      {/* Pricing grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-20">
        {tiers.map(({ name, price, period, desc, features, cta, highlight, available }) => (
          <div
            key={name}
            className={`card-hover relative rounded-2xl border p-8 flex flex-col ${
              highlight
                ? 'border-vr-gold bg-gradient-to-b from-vr-gold/8 to-vr-card'
                : 'border-vr-border bg-vr-card'
            }`}
          >
            {highlight && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                <span className="px-4 py-1 bg-vr-gold text-vr-bg text-xs font-bold rounded-full tracking-wide uppercase">
                  Most Popular
                </span>
              </div>
            )}

            <div className="mb-6">
              <h2 className="font-serif text-xl font-bold text-vr-text mb-1">{name}</h2>
              <p className="text-vr-faint text-sm mb-4">{desc}</p>
              <div className="flex items-end gap-1">
                <span className="font-serif text-4xl font-bold text-vr-text">{price}</span>
                {period && (
                  <span className="text-vr-muted text-sm mb-1.5">{period}</span>
                )}
              </div>
            </div>

            <ul className="space-y-3 flex-1 mb-8">
              {features.map((f) => (
                <li key={f} className="flex items-start gap-2.5 text-sm text-vr-muted">
                  <svg
                    className="shrink-0 mt-0.5"
                    width="14"
                    height="14"
                    viewBox="0 0 14 14"
                    fill="none"
                  >
                    <circle cx="7" cy="7" r="6" stroke="#d4a853" strokeWidth="1.2" />
                    <path
                      d="M4.5 7l2 2 3-3"
                      stroke="#d4a853"
                      strokeWidth="1.2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  {f}
                </li>
              ))}
            </ul>

            <button
              disabled={!available}
              className={`w-full py-3 rounded-xl font-semibold text-sm transition-colors ${
                available
                  ? highlight
                    ? 'bg-vr-gold text-vr-bg hover:bg-vr-gold-light'
                    : 'border border-vr-gold text-vr-gold hover:bg-vr-gold/10'
                  : 'border border-vr-border text-vr-faint cursor-not-allowed opacity-50'
              }`}
            >
              {available ? cta : `${cta} — Coming Soon`}
            </button>
          </div>
        ))}
      </div>

      <div className="gold-divider mb-16" />

      {/* FAQ placeholder */}
      <div className="max-w-3xl mx-auto">
        <h2 className="font-serif text-2xl font-bold text-vr-text mb-8 text-center">
          Frequently Asked Questions
        </h2>
        <div className="space-y-4">
          {[
            {
              q: 'Can I pay with cryptocurrency?',
              a: 'Yes. Through our Crossmint integration you can pay using ETH, USDC, SOL, or a range of other tokens across multiple chains. Standard card payments are also accepted.',
            },
            {
              q: 'Is my wallet data stored?',
              a: 'Wallet analysis is performed on-demand and results are session-scoped by default. Persistent watchlist monitoring requires an Analyst account and operates under our Privacy Policy.',
            },
            {
              q: 'What chains are supported?',
              a: 'Currently 18 chains including Ethereum, Arbitrum, Optimism, Base, Polygon, Solana, Avalanche, BNB Chain, and several others. Coverage expands continuously.',
            },
            {
              q: 'Do you offer refunds?',
              a: 'Subscriptions are billed monthly with no long-term commitment. You may cancel at any time; access continues until the end of the billing period.',
            },
          ].map(({ q, a }) => (
            <div key={q} className="rounded-xl border border-vr-border bg-vr-card p-6">
              <h3 className="font-semibold text-vr-text mb-2 text-sm">{q}</h3>
              <p className="text-vr-faint text-sm leading-relaxed">{a}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
