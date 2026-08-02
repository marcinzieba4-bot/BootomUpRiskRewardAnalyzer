const steps = [
  {
    number: '01',
    title: 'On-Chain Data Aggregation',
    subtitle: 'Multi-chain ingestion at block depth',
    body: 'ZembiHF\'s pipeline continuously ingests raw block data across 18 EVM and non-EVM chains. Transaction traces, internal calls, token transfers, and smart contract events are decoded and normalized into a unified schema. No summarized third-party feeds — only first-party, full-fidelity data.',
    bullets: [
      'Full transaction trace decoding (EVM debug_traceTransaction)',
      'Event log parsing across 50,000+ contract ABIs',
      'Cross-chain asset bridge tracking',
      'Real-time mempool monitoring for pending transactions',
    ],
  },
  {
    number: '02',
    title: 'Behavioral Pattern Recognition',
    subtitle: 'Wallet-level clustering & entity resolution',
    body: 'Raw addresses are clustered into behavioral entities using heuristic co-spend analysis, gas payment patterns, and temporal transaction graphs. This resolves pseudonymous addresses into high-confidence entity clusters — the foundation of all downstream analytics.',
    bullets: [
      'UTXO and account-model co-spend clustering',
      'Smart contract deployer lineage tracing',
      'Exchange deposit address attribution',
      'Whale wallet cohort identification',
    ],
  },
  {
    number: '03',
    title: 'Risk Scoring Engine',
    subtitle: 'Multi-factor quantitative risk assessment',
    body: 'Each wallet and position is scored across six independent risk dimensions: concentration risk, counterparty exposure, protocol smart-contract risk, liquidity depth vs. position size, historical drawdown profile, and cross-chain leverage ratios. Scores update in near real-time.',
    bullets: [
      'Gini coefficient for portfolio concentration',
      'Protocol audit score integration (Code4rena, Sherlock)',
      'Oracle manipulation exposure assessment',
      'Liquidation proximity heatmaps for lending positions',
    ],
  },
  {
    number: '04',
    title: 'Action Recommendations',
    subtitle: 'Bespoke intelligence, not generic alerts',
    body: 'Risk scores and behavioral signals feed a recommendation layer that generates wallet-specific, position-aware action proposals. Recommendations are ranked by urgency, impact magnitude, and execution feasibility — always with full reasoning transparency.',
    bullets: [
      'Rebalancing proposals with slippage estimates',
      'Hedge suggestions mapped to on-chain derivative venues',
      'Exit sequencing for illiquid positions',
      'Yield optimization routes accounting for gas costs',
    ],
  },
];

const principles = [
  {
    icon: '⬡',
    title: 'First-Party Data Only',
    desc: 'We never rely on third-party aggregated feeds. Every insight is derived from raw block data we index ourselves.',
  },
  {
    icon: '◈',
    title: 'Transparent Reasoning',
    desc: 'Every recommendation exposes its full evidence chain. No black boxes — you see exactly what drove the conclusion.',
  },
  {
    icon: '◇',
    title: 'Non-Custodial Always',
    desc: 'Connecting your wallet never grants us custody or signing rights. Analysis is read-only, end-to-end.',
  },
  {
    icon: '◉',
    title: 'Adversarial Testing',
    desc: 'Our models are stress-tested against historical market dislocations: March 2020, May 2021, and the Terra/FTX collapses.',
  },
];

export default function LogicPage() {
  return (
    <div className="pt-28 pb-24">

      {/* Page header */}
      <div className="max-w-7xl mx-auto px-6 mb-20">
        <div className="flex items-center gap-2 mb-4">
          <span className="w-6 h-px bg-vr-gold" />
          <span className="text-vr-gold text-xs font-semibold tracking-widest uppercase">
            Methodology
          </span>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-end">
          <div>
            <h1 className="font-serif text-4xl md:text-5xl font-bold text-vr-text mb-4">
              The ZembiHF Logic Layer
            </h1>
            <p className="text-vr-muted text-lg leading-relaxed">
              A four-phase analytical pipeline that transforms raw blockchain data into
              structured, actionable intelligence — with full auditability at every step.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-4">
            {[
              { label: 'Data Sources', value: '18 Chains' },
              { label: 'ABI Library', value: '50K+' },
              { label: 'Risk Factors', value: '6 Dimensions' },
              { label: 'Latency', value: '< 2s' },
            ].map(({ label, value }) => (
              <div key={label} className="rounded-xl border border-vr-border bg-vr-card p-5">
                <div className="font-serif text-2xl font-bold text-vr-gold mb-1">{value}</div>
                <div className="text-vr-faint text-xs uppercase tracking-wide">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="gold-divider" />

      {/* Steps */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <div className="space-y-6">
          {steps.map(({ number, title, subtitle, body, bullets }) => (
            <div
              key={number}
              className="card-hover grid grid-cols-1 lg:grid-cols-12 gap-0 rounded-2xl border border-vr-border bg-vr-card overflow-hidden"
            >
              {/* Step number column */}
              <div className="lg:col-span-2 bg-vr-gold/5 border-b lg:border-b-0 lg:border-r border-vr-border flex flex-col items-center justify-center p-8">
                <span className="font-mono text-5xl font-bold text-vr-gold/30 leading-none">
                  {number}
                </span>
              </div>

              {/* Content */}
              <div className="lg:col-span-10 p-8 md:p-10">
                <div className="mb-1">
                  <span className="text-vr-faint text-xs uppercase tracking-widest font-semibold">
                    {subtitle}
                  </span>
                </div>
                <h2 className="font-serif text-2xl md:text-3xl font-bold text-vr-text mb-4">
                  {title}
                </h2>
                <p className="text-vr-muted leading-relaxed mb-7 max-w-3xl">{body}</p>
                <ul className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
                  {bullets.map((b) => (
                    <li key={b} className="flex items-start gap-2.5 text-sm text-vr-muted">
                      <span className="mt-1 w-1.5 h-1.5 rounded-full bg-vr-gold shrink-0" />
                      {b}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="gold-divider" />

      {/* Principles */}
      <div className="max-w-7xl mx-auto px-6 py-20">
        <h2 className="font-serif text-3xl font-bold text-vr-text mb-10 text-center">
          Core Principles
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {principles.map(({ icon, title, desc }) => (
            <div
              key={title}
              className="card-hover rounded-xl border border-vr-border bg-vr-card p-6 text-center"
            >
              <div className="text-3xl text-vr-gold mb-4">{icon}</div>
              <h3 className="font-serif text-lg font-bold text-vr-text mb-2">{title}</h3>
              <p className="text-vr-faint text-sm leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </div>

      {/* CTA */}
      <div className="max-w-7xl mx-auto px-6">
        <div className="rounded-2xl border border-vr-gold/20 bg-vr-gold/5 p-10 text-center">
          <h3 className="font-serif text-2xl font-bold text-vr-text mb-3">
            Ready to See It in Action?
          </h3>
          <p className="text-vr-muted mb-6 max-w-md mx-auto text-sm">
            The Wallet Intelligence Engine applies this entire pipeline to your portfolio.
            Join the waitlist to be first in line.
          </p>
          <button className="px-6 py-3 bg-vr-gold text-vr-bg font-semibold rounded-lg hover:bg-vr-gold-light transition-colors text-sm">
            Join the Waitlist
          </button>
        </div>
      </div>
    </div>
  );
}
