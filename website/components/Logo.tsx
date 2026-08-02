import React from 'react';

interface LogoProps {
  size?: number;
  animated?: boolean;
}

export default function Logo({ size = 40, animated = false }: LogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={animated ? 'animate-pulse-glow' : ''}
      aria-label="ZembiHF logo"
    >
      <defs>
        <radialGradient id="badgeFace" cx="35%" cy="28%" r="75%">
          <stop offset="0%" stopColor="#161628" />
          <stop offset="100%" stopColor="#080810" />
        </radialGradient>
        <linearGradient id="ringGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#f0c96a" />
          <stop offset="100%" stopColor="#8b6914" />
        </linearGradient>
      </defs>

      {/* Circle badge */}
      <circle cx="50" cy="50" r="45.5" fill="url(#badgeFace)" stroke="url(#ringGrad)" strokeWidth="5" />
      <circle cx="50" cy="50" r="45.5" fill="none" stroke="#f0c96a" strokeWidth="1" opacity="0.25" />

      {/* Wordmark embedded in the circle */}
      <text
        x="50"
        y="51"
        textAnchor="middle"
        dominantBaseline="central"
        fontFamily="Inter, system-ui, sans-serif"
        fontWeight="800"
        fontSize="19"
        letterSpacing="-0.5"
        textLength="76"
        lengthAdjust="spacingAndGlyphs"
        fill="#f0c96a"
      >
        ZembiHF
      </text>
    </svg>
  );
}
