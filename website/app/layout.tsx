import type { Metadata } from 'next';
import { Inter, Playfair_Display } from 'next/font/google';
import './globals.css';
import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'ZembiHF — On-Chain Intelligence',
  description:
    'Institutional-grade on-chain research, wallet analytics, and DeFi intelligence powered by ZembiHF.',
  keywords: ['crypto', 'on-chain analysis', 'DeFi', 'blockchain research', 'wallet intelligence'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    // THEME SWITCH — "light" (white) or "dark" (original navy).
    // This single attribute drives the entire palette; see app/globals.css.
    <html lang="en" data-theme="light" className={`${inter.variable} ${playfair.variable}`}>
      <body className="font-sans bg-vr-bg text-vr-text antialiased">
        <Navbar />
        <main className="relative z-10 min-h-screen">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
