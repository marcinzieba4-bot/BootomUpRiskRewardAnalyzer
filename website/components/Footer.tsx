import Link from 'next/link';
import Logo from './Logo';

const footerLinks = [
  {
    heading: 'Platform',
    links: [
      { label: 'Research', href: '/research' },
      { label: 'Logic', href: '/logic' },
      { label: 'Wallet Analytics', href: '/wallet' },
      { label: 'Services', href: '/services' },
    ],
  },
  {
    heading: 'Company',
    links: [
      { label: 'About', href: '#' },
      { label: 'Methodology', href: '/logic' },
      { label: 'Careers', href: '#' },
      { label: 'Contact', href: '#' },
    ],
  },
  {
    heading: 'Legal',
    links: [
      { label: 'Terms of Service', href: '#' },
      { label: 'Privacy Policy', href: '#' },
      { label: 'Risk Disclosure', href: '#' },
    ],
  },
];

export default function Footer() {
  return (
    <footer className="relative z-10 border-t border-vr-border bg-vr-surface mt-20">
      <div className="max-w-7xl mx-auto px-6 pt-14 pb-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10 mb-12">

          {/* Brand column */}
          <div className="md:col-span-1">
            <Link href="/" className="flex items-center gap-3 mb-4">
              <Logo size={32} />
              <span className="font-serif text-lg font-bold text-vr-text">ZembiHF</span>
            </Link>
            <p className="text-vr-faint text-sm leading-relaxed mb-5">
              Institutional-grade on-chain intelligence for the modern digital asset investor.
            </p>
            {/* Social placeholders */}
            <div className="flex gap-3">
              {['X', 'in', 'gh'].map((s) => (
                <a
                  key={s}
                  href="#"
                  className="w-8 h-8 rounded-md border border-vr-border flex items-center justify-center text-vr-faint text-xs font-bold hover:border-vr-gold hover:text-vr-gold transition-colors"
                >
                  {s}
                </a>
              ))}
            </div>
          </div>

          {/* Link columns */}
          {footerLinks.map(({ heading, links }) => (
            <div key={heading}>
              <h4 className="text-vr-muted text-xs font-semibold tracking-widest uppercase mb-4">
                {heading}
              </h4>
              <ul className="space-y-2.5">
                {links.map(({ label, href }) => (
                  <li key={label}>
                    <Link
                      href={href}
                      className="text-vr-faint text-sm hover:text-vr-gold transition-colors duration-150"
                    >
                      {label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="gold-divider mb-6" />

        <div className="flex flex-col md:flex-row items-center justify-between gap-3 text-vr-faint text-xs">
          <span>© {new Date().getFullYear()} ZembiHF. All rights reserved.</span>
          <span className="text-center">
            Not financial advice. Crypto assets involve substantial risk. Past performance is not indicative of future results.
          </span>
          <span className="text-vr-gold/60 font-mono tracking-widest">
            AWS · Next.js · Web3
          </span>
        </div>
      </div>
    </footer>
  );
}
