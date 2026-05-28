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
          bg:       '#080810',
          surface:  '#0d0d1a',
          card:     '#10101e',
          border:   '#1c1c2e',
          gold:     '#d4a853',
          'gold-light': '#f0c96a',
          'gold-dim':   '#8b6914',
          text:     '#e8e8f4',
          muted:    '#6b7096',
          faint:    '#3d4068',
          green:    '#22c55e',
          blue:     '#60a5fa',
          red:      '#ef4444',
          amber:    '#f59e0b',
        },
      },
      fontFamily: {
        sans:  ['var(--font-inter)', 'system-ui', 'sans-serif'],
        serif: ['var(--font-playfair)', 'Georgia', 'serif'],
        mono:  ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace'],
      },
      backgroundImage: {
        'hero-radial':
          'radial-gradient(ellipse at 20% 50%, rgba(212,168,83,0.06) 0%, transparent 55%), radial-gradient(ellipse at 80% 15%, rgba(96,165,250,0.04) 0%, transparent 50%)',
        'card-shine':
          'linear-gradient(135deg, rgba(212,168,83,0.03) 0%, transparent 50%)',
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
