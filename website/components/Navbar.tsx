'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import Logo from './Logo';

const navLinks = [
  { label: 'Research', href: '/research' },
  { label: 'Signals', href: '/signals' },
  { label: 'Reports', href: 'https://d7g7nkeytae81.cloudfront.net/reports/index.html', external: true },
  { label: 'Logic', href: '/logic' },
];

export default function Navbar() {
  const pathname = usePathname();
  const isApp = pathname.startsWith('/app');

  return (
    <header className="fixed top-0 left-0 right-0 z-50 border-b border-vr-border bg-vr-bg/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">

        {/* Brand */}
        <Link href="/" className="flex items-center gap-3 group shrink-0">
          <Logo size={34} animated />
          <span className="font-sans text-[17px] font-bold tracking-tight text-vr-text group-hover:text-vr-gold transition-colors duration-200">
            ZembiHF
          </span>
        </Link>

        {/* Nav links */}
        <nav className="hidden md:flex items-center gap-7">
          {navLinks.map(({ label, href, external }) => {
            if (external) {
              return (
                <a
                  key={href}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="nav-link text-sm font-medium transition-colors duration-200 pb-0.5 text-vr-muted hover:text-vr-text"
                >
                  {label}
                </a>
              );
            }
            const isActive = pathname === href || pathname.startsWith(href + '/');
            return (
              <Link
                key={href}
                href={href}
                className={`nav-link text-sm font-medium transition-colors duration-200 pb-0.5 ${
                  isActive ? 'active text-vr-text' : 'text-vr-muted hover:text-vr-text'
                }`}
              >
                {label}
              </Link>
            );
          })}
        </nav>

        {/* Enter App */}
        <Link
          href="/app"
          className={`hidden md:flex items-center gap-2 px-5 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
            isApp
              ? 'bg-vr-gold text-vr-bg'
              : 'bg-vr-gold text-vr-bg hover:bg-vr-gold-light'
          }`}
        >
          Enter App
          <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
            <path d="M3 7h8M8 4l3 3-3 3" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </Link>

        {/* Mobile */}
        <div className="md:hidden flex items-center gap-3">
          <Link
            href="/app"
            className="px-3 py-1.5 bg-vr-gold text-vr-bg rounded-md text-xs font-bold"
          >
            Enter App
          </Link>
          <button className="text-vr-muted p-1" aria-label="Open menu">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" />
            </svg>
          </button>
        </div>

      </div>
    </header>
  );
}
