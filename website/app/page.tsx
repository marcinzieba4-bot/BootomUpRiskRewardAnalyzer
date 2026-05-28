import Link from 'next/link';

const stats = [
  { label: 'Wallets Analyzed',  value: '142K+' },
  { label: 'Chains Supported',  value: '18'    },
  { label: 'Research Reports',  value: '380+'  },
  { label: 'Assets Under Watch', value: '$4.2B' },
];

const features = [
  {
    title: 'On-Chain Research',
    desc: 'Peer-reviewed analysis of DeFi protocols, token mechanics, and macro-crypto cycles. Published openly for the community.',
    link: '/research',
    linkLabel: 'Browse Research',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M4 4h10l4 4v12H4V4Z" stroke="#d4a853" strokeWidth="1.5" strokeLinejoin="round" />
        <path d="M14 4v4h4M7 9h6M7 12h6M7 15h4" stroke="#d4a853" strokeWidth="1.4" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    title: 'Wallet Intelligence',
    desc: 'Connect your wallet. Get a 6-dimension risk score, behavioral analysis, and bespoke action recommendations in seconds.',
    link: '/app',
    linkLabel: 'Enter App',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <rect x="2" y="6" width="20" height="13" rx="2" stroke="#d4a853" strokeWidth="1.5" />
        <path d="M2 10h20" stroke="#d4a853" strokeWidth="1.4" />
        <circle cx="17" cy="15.5" r="1.5" fill="#d4a853" />
      </svg>
    ),
  },
  {
    title: 'Risk Scoring Engine',
    desc: 'Multi-factor quantitative risk assessment across concentration, counterparty exposure, protocol security, and liquidation proximity.',
    link: '/logic',
    linkLabel: 'Read the Methodology',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M12 3L21 8v8L12 21 3 16V8L12 3Z" stroke="#d4a853" strokeWidth="1.5" />
        <circle cx="12" cy="12" r="3" stroke="#d4a853" strokeWidth="1.4" />
      </svg>
    ),
  },
  {
    title: 'Action Recommendations',
    desc: 'Every risk signal resolves into a ranked, wallet-specific recommendation — with full reasoning, slippage estimates, and execution routes.',
    link: '/app',
    linkLabel: 'Enter App',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M4 16L9 9l4 4 4-5 3 3" stroke="#d4a853" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="19" cy="5" r="2" stroke="#d4a853" strokeWidth="1.4" />
      </svg>
    ),
  },
  {
    title: 'Multi-Chain Coverage',
    desc: 'Ethereum, Arbitrum, Optimism, Base, Polygon, Solana, Avalanche, BNB Chain and 10 more — one unified intelligence layer.',
    link: '/logic',
    linkLabel: 'See Methodology',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="9" stroke="#d4a853" strokeWidth="1.5" />
        <path d="M3 12h18M12 3c-3 3-4 5.4-4 9s1 6 4 9M12 3c3 3 4 5.4 4 9s-1 6-4 9" stroke="#d4a853" strokeWidth="1.4" />
      </svg>
    ),
  },
  {
    title: 'Crossmint Payments',
    desc: 'Access premium tiers with crypto or card. ETH, USDC, SOL, or any major credit card — powered by Crossmint.',
    link: '/app',
    linkLabel: 'View Plans',
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M12 2L22 7v10L12 22 2 17V7L12 2Z" stroke="#d4a853" strokeWidth="1.5" />
        <path d="M8 12l3 3 5-5" stroke="#d4a853" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
];

const latestArticles = [
  {
    category: 'Analysis',
    title: 'The Liquidity Mirage: Understanding Deep Order Books in Thin Markets',
    date: 'Apr 12, 2025',
    readTime: '8 min',
  },
  {
    category: 'Research',
    title: 'EigenLayer and the Restaking Paradigm: Security as a Service',
    date: 'Apr 8, 2025',
    readTime: '11 min',
  },
  {
    category: 'Commentary',
    title: 'Bitcoin Dominance Cycles: A 4-Year Framework Revisited',
    date: 'Apr 3, 2025',
    readTime: '6 min',
  },
];

export default function HomePage() {
  return (
    <>
      {/* ── HERO ── */}
      <section className="relative min-h-screen flex items-center pt-16 overflow-hidden">

        {/* Background glow orbs */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] rounded-full bg-vr-gold/5 blur-[120px]" />
          <div className="absolute bottom-1/4 right-1/4 w-[400px] h-[400px] rounded-full bg-blue-600/4 blur-[100px]" />
        </div>

        <div className="relative max-w-7xl mx-auto px-6 w-full py-28">
          <div className="max-w-4xl">

            {/* Tag */}
            <div className="inline-flex items-center gap-2.5 border border-vr-border bg-vr-surface/60 rounded-full px-4 py-1.5 mb-10">
              <span className="w-1.5 h-1.5 rounded-full bg-vr-green animate-pulse" />
              <span className="text-vr-muted text-xs font-medium tracking-wide">
                On-Chain Intelligence · Powered by VeeRock
              </span>
            </div>

            {/* Headline */}
            <h1 className="text-5xl md:text-6xl lg:text-[74px] font-bold leading-[1.05] tracking-tight text-vr-text mb-7">
              The intelligence layer<br />
              for{' '}
              <span className="text-vr-gold">on-chain capital.</span>
            </h1>

            {/* Sub */}
            <p className="text-vr-muted text-lg md:text-xl leading-relaxed mb-10 max-w-2xl">
              Deep research, wallet behavioral analytics, and bespoke risk recommendations
              for DeFi participants who demand signal over noise.
            </p>

            {/* CTAs */}
            <div className="flex flex-wrap gap-4 items-center">
              <Link
                href="/app"
                className="inline-flex items-center gap-2.5 px-7 py-3.5 bg-vr-gold text-vr-bg font-bold rounded-xl hover:bg-vr-gold-light transition-colors duration-200"
              >
                Enter App
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                  <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </Link>
              <Link
                href="/research"
                className="inline-flex items-center gap-2 px-7 py-3.5 border border-vr-border text-vr-muted font-semibold rounded-xl hover:border-vr-gold/50 hover:text-vr-text transition-colors duration-200"
              >
                Read Research
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS ── */}
      <section className="border-y border-vr-border bg-vr-surface/50">
        <div className="max-w-7xl mx-auto px-6 py-10">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-vr-border">
            {stats.map(({ label, value }) => (
              <div key={label} className="bg-vr-surface px-8 py-7 text-center">
                <div className="text-3xl md:text-4xl font-bold text-vr-text mb-1 tracking-tight">
                  {value}
                </div>
                <div className="text-vr-faint text-xs uppercase tracking-widest font-medium">
                  {label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FEATURES ── */}
      <section className="max-w-7xl mx-auto px-6 py-28">
        <div className="mb-14">
          <p className="text-vr-gold text-xs font-semibold tracking-widest uppercase mb-3">
            Platform
          </p>
          <h2 className="text-3xl md:text-4xl font-bold text-vr-text max-w-xl leading-tight">
            Built for operators who trade on knowledge.
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-px bg-vr-border">
          {features.map(({ title, desc, link, linkLabel, icon }) => (
            <div
              key={title}
              className="group bg-vr-surface hover:bg-vr-card transition-colors duration-200 p-8 flex flex-col"
            >
              <div className="mb-5 opacity-80 group-hover:opacity-100 transition-opacity">
                {icon}
              </div>
              <h3 className="text-vr-text font-bold text-lg mb-2.5">{title}</h3>
              <p className="text-vr-faint text-sm leading-relaxed flex-1 mb-5">{desc}</p>
              <Link
                href={link}
                className="text-vr-gold text-sm font-semibold hover:text-vr-gold-light transition-colors flex items-center gap-1.5"
              >
                {linkLabel}
                <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                  <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </Link>
            </div>
          ))}
        </div>
      </section>

      {/* ── LATEST RESEARCH ── */}
      <section className="border-t border-vr-border bg-vr-surface/30">
        <div className="max-w-7xl mx-auto px-6 py-20">
          <div className="flex items-end justify-between mb-10">
            <div>
              <p className="text-vr-gold text-xs font-semibold tracking-widest uppercase mb-2">
                Research
              </p>
              <h2 className="text-3xl font-bold text-vr-text">Latest from the desk</h2>
            </div>
            <Link
              href="/research"
              className="hidden md:flex items-center gap-1.5 text-sm text-vr-muted hover:text-vr-gold transition-colors font-medium"
            >
              All research
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                <path d="M2 6h8M7 3l3 3-3 3" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </Link>
          </div>

          <div className="divide-y divide-vr-border">
            {latestArticles.map(({ category, title, date, readTime }) => (
              <Link
                key={title}
                href="/research"
                className="flex items-center justify-between gap-6 py-5 group hover:bg-vr-surface/40 -mx-4 px-4 rounded-lg transition-colors"
              >
                <div className="flex items-start gap-5">
                  <span className="shrink-0 mt-0.5 badge border bg-vr-gold/8 text-vr-gold border-vr-gold/15">
                    {category}
                  </span>
                  <span className="text-vr-muted text-sm font-medium group-hover:text-vr-text transition-colors leading-snug">
                    {title}
                  </span>
                </div>
                <div className="hidden md:flex items-center gap-5 text-vr-faint text-xs shrink-0">
                  <span>{date}</span>
                  <span>{readTime}</span>
                  <svg className="opacity-0 group-hover:opacity-100 transition-opacity" width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M3 7h8M8 4l3 3-3 3" stroke="#d4a853" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ── ENTER APP CTA ── */}
      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="relative rounded-2xl border border-vr-gold/20 overflow-hidden">
          {/* Background glow */}
          <div className="absolute inset-0 bg-gradient-to-br from-vr-gold/6 via-transparent to-transparent pointer-events-none" />
          <div className="absolute -top-20 -right-20 w-64 h-64 rounded-full bg-vr-gold/8 blur-[60px] pointer-events-none" />

          <div className="relative px-10 py-14 md:py-16 flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
            <div className="max-w-xl">
              <h2 className="text-3xl md:text-4xl font-bold text-vr-text mb-3">
                Ready to analyze your wallet?
              </h2>
              <p className="text-vr-muted leading-relaxed">
                Connect your wallet to the VeeRock engine. Get a full risk breakdown,
                position analysis, and ranked action recommendations — non-custodial, read-only.
              </p>
            </div>
            <Link
              href="/app"
              className="shrink-0 inline-flex items-center gap-3 px-8 py-4 bg-vr-gold text-vr-bg font-bold rounded-xl hover:bg-vr-gold-light transition-colors text-base"
            >
              Enter App
              <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                <path d="M4 9h10M10 5l4 4-4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
