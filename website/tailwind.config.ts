import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Light theme. Gold stays the brand accent but is darkened so it
        // clears WCAG AA as text and as an icon stroke on white.
        vr: {
          bg:       '#ffffff',
          surface:  '#f6f6f9',
          card:     '#ffffff',
          border:   '#e5e5ee',
          gold:     '#9a6f12',   // 5.0:1 on white — safe for text and icons
          'gold-light': '#b8862a',
          'gold-dim':   '#c9a961',
          text:     '#12122a',
          muted:    '#565b78',
          faint:    '#8b90ab',
          green:    '#15803d',
          blue:     '#1d4ed8',
          red:      '#dc2626',
          amber:    '#b45309',
        },
      },
      fontFamily: {
        sans:  ['var(--font-inter)', 'system-ui', 'sans-serif'],
        serif: ['var(--font-playfair)', 'Georgia', 'serif'],
        mono:  ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      backgroundImage: {
        'hero-radial':
          'radial-gradient(ellipse at 20% 50%, rgba(154,111,18,0.07) 0%, transparent 55%), radial-gradient(ellipse at 80% 15%, rgba(29,78,216,0.05) 0%, transparent 50%)',
        'card-shine':
          'linear-gradient(135deg, rgba(154,111,18,0.045) 0%, transparent 55%)',
      },
      boxShadow: {
        'vr-card':  '0 1px 2px rgba(18,18,42,0.04), 0 1px 3px rgba(18,18,42,0.06)',
        'vr-raised': '0 8px 28px rgba(18,18,42,0.10), 0 2px 6px rgba(18,18,42,0.05)',
      },
      keyframes: {
        'fade-up': {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'pulse-glow': {
          '0%, 100%': { filter: 'drop-shadow(0 1px 2px rgba(18,18,42,0.12))' },
          '50%':       { filter: 'drop-shadow(0 2px 8px rgba(154,111,18,0.38))' },
        },
        shimmer: {
          '0%':   { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      animation: {
        'fade-up':    'fade-up 0.6s ease-out forwards',
        'pulse-glow': 'pulse-glow 3s ease-in-out infinite',
        shimmer:      'shimmer 2.5s linear infinite',
      },
    },
  },
  plugins: [],
};

export default config;
