import React from 'react';

interface LogoProps {
  size?: number;
  animated?: boolean;
}

/**
 * ZembiHF mark — a circular badge on a cream face with a gold ring, carrying a
 * geometric "Z" monogram and a rising signal line through it.
 *
 * Built for the light theme: ink-on-cream rather than gold-on-black, so it holds
 * contrast on white and stays legible down to ~24px (the wordmark lives beside
 * the mark in the navbar, so nothing here needs to be read as text).
 */
export default function Logo({ size = 40, animated = false }: LogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={animated ? 'animate-pulse-glow' : ''}
      role="img"
      aria-label="ZembiHF"
    >
      <defs>
        <linearGradient id="zFace" x1="20%" y1="0%" x2="80%" y2="100%">
          <stop offset="0%" stopColor="#ffffff" />
          <stop offset="100%" stopColor="#f4efe2" />
        </linearGradient>
        <linearGradient id="zRing" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#c9a961" />
          <stop offset="55%" stopColor="#9a6f12" />
          <stop offset="100%" stopColor="#6f4f0c" />
        </linearGradient>
        <linearGradient id="zSignal" x1="0%" y1="100%" x2="100%" y2="0%">
          <stop offset="0%" stopColor="#b8862a" />
          <stop offset="100%" stopColor="#9a6f12" />
        </linearGradient>
      </defs>

      {/* Badge */}
      <circle cx="50" cy="50" r="45" fill="url(#zFace)" stroke="url(#zRing)" strokeWidth="5" />
      <circle cx="50" cy="50" r="39.5" fill="none" stroke="#9a6f12" strokeWidth="1" opacity="0.22" />

      {/* Rising signal line, set behind the monogram */}
      <path
        d="M26 68 L40 55 L50 62 L74 33"
        stroke="url(#zSignal)"
        strokeWidth="4.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        opacity="0.42"
      />

      {/* Z monogram */}
      <path
        d="M33 34 H67 L33 66 H67"
        stroke="#12122a"
        strokeWidth="8.5"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />

      {/* Signal endpoint */}
      <circle cx="74" cy="33" r="5.5" fill="#9a6f12" stroke="url(#zFace)" strokeWidth="2" />
    </svg>
  );
}
