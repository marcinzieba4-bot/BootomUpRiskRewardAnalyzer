import Link from 'next/link';

const categories = ['All', 'Analysis', 'Research', 'Commentary', 'Market Update'];

const articles = [
  {
    category: 'Analysis',
    categoryColor: 'bg-blue-500/10 text-blue-700 border-blue-500/20',
    title: 'The Liquidity Mirage: Understanding Deep Order Books in Thin Markets',
    excerpt:
      'As on-chain liquidity metrics increasingly diverge from reported figures, institutional participants face a fragmented landscape where slippage costs quietly erode alpha generation across DeFi protocols.',
    date: 'Apr 12, 2025',
    readTime: '8 min read',
    author: 'ZembiHF Research',
  },
  {
    category: 'Research',
    categoryColor: 'bg-vr-gold/10 text-vr-gold border-vr-gold/20',
    title: 'EigenLayer and the Restaking Paradigm: Security as a Service',
    excerpt:
      'The emergence of restaking introduces novel vectors of systemic risk while simultaneously unlocking a trillion-dollar addressable market in cryptoeconomic security guarantees across the modular stack.',
    date: 'Apr 8, 2025',
    readTime: '11 min read',
    author: 'ZembiHF Research',
  },
  {
    category: 'Commentary',
    categoryColor: 'bg-emerald-500/10 text-emerald-700 border-emerald-500/20',
    title: 'Bitcoin Dominance Cycles: A 4-Year Framework Revisited',
    excerpt:
      'Historical dominance cycles suggest we are entering the late expansion phase, characterized by capital rotation from large-cap to mid-cap Layer-1 assets as narrative velocity accelerates.',
    date: 'Apr 3, 2025',
    readTime: '6 min read',
    author: 'ZembiHF Editorial',
  },
  {
    category: 'Research',
    categoryColor: 'bg-vr-gold/10 text-vr-gold border-vr-gold/20',
    title: 'zkRollup Economics: Why Proof Generation Costs Determine L2 Survival',
    excerpt:
      'With proving costs comprising up to 40% of operational overhead for zero-knowledge rollups, the economics of decentralized sequencing remain precarious — and the race to proof compression is existential.',
    date: 'Mar 28, 2025',
    readTime: '13 min read',
    author: 'ZembiHF Research',
  },
  {
    category: 'Analysis',
    categoryColor: 'bg-blue-500/10 text-blue-700 border-blue-500/20',
    title: 'The Stablecoin Flywheel: How Circle and Tether Build Treasury Yield Machines',
    excerpt:
      'USDC and USDT reserve compositions reveal a sophisticated arbitrage of short-duration treasury yields, generating over $6B in annualized revenue while bearing minimal credit risk exposure.',
    date: 'Mar 21, 2025',
    readTime: '9 min read',
    author: 'ZembiHF Research',
  },
  {
    category: 'Market Update',
    categoryColor: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
    title: 'MEV in 2025: From Dark Forest to Structured Market',
    excerpt:
      'The evolution of maximal extractable value from chaotic frontrunning to institutionalized block building represents one of the most significant structural shifts in public blockchain economics this cycle.',
    date: 'Mar 14, 2025',
    readTime: '7 min read',
    author: 'ZembiHF Editorial',
  },
];

export default function ResearchPage() {
  return (
    <div className="pt-28 pb-24 max-w-7xl mx-auto px-6">

      {/* Page header */}
      <div className="mb-14">
        <div className="flex items-center gap-2 mb-4">
          <span className="w-6 h-px bg-vr-gold" />
          <span className="text-vr-gold text-xs font-semibold tracking-widest uppercase">
            Knowledge Base
          </span>
        </div>
        <h1 className="font-serif text-4xl md:text-5xl font-bold text-vr-text mb-4">
          Research & Commentary
        </h1>
        <p className="text-vr-muted text-lg max-w-2xl">
          Original analysis, long-form research, and editorial commentary on the blockchain economy.
          No hype — just rigorous signal.
        </p>
      </div>

      {/* Category filter */}
      <div className="flex flex-wrap gap-2 mb-12">
        {categories.map((cat, i) => (
          <button
            key={cat}
            className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-colors ${
              i === 0
                ? 'bg-vr-gold text-vr-bg border-vr-gold'
                : 'border-vr-border text-vr-muted hover:border-vr-gold hover:text-vr-gold'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      <div className="gold-divider mb-12" />

      {/* Featured (first article large) */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 mb-8">
        <article className="card-hover lg:col-span-3 rounded-xl border border-vr-border bg-vr-card p-8 flex flex-col">
          <span className={`badge border mb-4 self-start ${articles[0].categoryColor}`}>
            {articles[0].category}
          </span>
          <h2 className="font-serif text-2xl md:text-3xl font-bold text-vr-text mb-4 leading-snug">
            {articles[0].title}
          </h2>
          <p className="text-vr-muted leading-relaxed flex-1 mb-6">{articles[0].excerpt}</p>
          <div className="flex items-center justify-between text-vr-faint text-xs pt-5 border-t border-vr-border">
            <div className="flex items-center gap-3">
              <span>{articles[0].author}</span>
              <span className="text-vr-border">·</span>
              <span>{articles[0].date}</span>
            </div>
            <span>{articles[0].readTime}</span>
          </div>
        </article>

        <article className="card-hover lg:col-span-2 rounded-xl border border-vr-border bg-vr-card p-8 flex flex-col">
          <span className={`badge border mb-4 self-start ${articles[1].categoryColor}`}>
            {articles[1].category}
          </span>
          <h2 className="font-serif text-xl font-bold text-vr-text mb-3 leading-snug">
            {articles[1].title}
          </h2>
          <p className="text-vr-muted text-sm leading-relaxed flex-1 mb-6">
            {articles[1].excerpt}
          </p>
          <div className="flex items-center justify-between text-vr-faint text-xs pt-4 border-t border-vr-border">
            <span>{articles[1].date}</span>
            <span>{articles[1].readTime}</span>
          </div>
        </article>
      </div>

      {/* Remaining grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {articles.slice(2).map(({ category, categoryColor, title, excerpt, date, readTime, author }) => (
          <article
            key={title}
            className="card-hover rounded-xl border border-vr-border bg-vr-card p-6 flex flex-col"
          >
            <span className={`badge border mb-4 self-start ${categoryColor}`}>{category}</span>
            <h3 className="font-serif text-lg font-bold text-vr-text mb-3 leading-snug">
              {title}
            </h3>
            <p className="text-vr-muted text-sm leading-relaxed flex-1 mb-5">{excerpt}</p>
            <div className="flex items-center justify-between text-vr-faint text-xs pt-4 border-t border-vr-border">
              <div className="flex items-center gap-2">
                <span className="truncate">{author}</span>
                <span className="text-vr-border">·</span>
                <span className="shrink-0">{date}</span>
              </div>
              <span className="shrink-0">{readTime}</span>
            </div>
          </article>
        ))}
      </div>

      {/* Load more placeholder */}
      <div className="mt-12 text-center">
        <button className="px-8 py-3 border border-vr-border text-vr-muted rounded-lg hover:border-vr-gold hover:text-vr-gold transition-colors text-sm font-medium">
          Load More Articles
        </button>
      </div>
    </div>
  );
}
