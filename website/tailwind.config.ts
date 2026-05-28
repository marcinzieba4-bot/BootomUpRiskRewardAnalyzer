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
        vr: {
          bg:       '#05050a',
          surface:  '#0c0c17',
          card:     '#101020',
          border:   '#1d1d32',
          gold:     '#d4a853',
          'gold-light': '#f0c96a',
          'gold-dim':   '#8b6914',
          text:     '#f1f5f9',
          muted:    '#94a3b8',
          faint:    '#475569',
          green:    '#10b981',
          blue:     '#3b82f6',
          red:      '#ef4444',
        },
      },
      fontFamily: {
        sans:  ['var(--font-inter)', 'system-ui', 'sans-serif'],
        serif: ['var(--font-playfair)', 'Georgia', 'serif'],
      },
      backgroundImage: {
        'hero-radial':
          'radial-gradient(ellipse at 20% 50%, rgba(212,168,83,0.07) 0%, transparent 55%), radial-gradient(ellipse at 80% 15%, rgba(59,130,246,0.05) 0%, transparent 50%)',
        'card-shine':
          'linear-gradient(135deg, rgba(212,168,83,0.04) 0%, transparent 50%)',
      },
      keyframes: {
        'fade-up': {
          '0%':   { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'pulse-glow': {
          '0%, 100%': { filter: 'drop-shadow(0 0 6px rgba(212,168,83,0.4))' },
          '50%':       { filter: 'drop-shadow(0 0 14px rgba(212,168,83,0.8))' },
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
