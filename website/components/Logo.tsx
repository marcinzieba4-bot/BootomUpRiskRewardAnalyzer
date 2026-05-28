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
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={animated ? 'animate-pulse-glow' : ''}
      aria-label="VeeRock logo"
    >
      <defs>
        <radialGradient id="rockFace" cx="35%" cy="28%" r="65%">
          <stop offset="0%" stopColor="#f0c96a" />
          <stop offset="45%" stopColor="#d4a853" />
          <stop offset="100%" stopColor="#7a5b10" />
        </radialGradient>
        <radialGradient id="rockShadow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#d4a853" stopOpacity="0" />
          <stop offset="100%" stopColor="#3b2500" stopOpacity="0.6" />
        </radialGradient>
      </defs>

      {/* Rock body — irregular boulder polygon */}
      <path
        d="M21 2 L34 7 L38 16 L37 28 L30 36 L18 38 L7 33 L3 22 L5 10 L14 4 Z"
        fill="url(#rockFace)"
      />
      {/* Depth / shadow overlay */}
      <path
        d="M21 2 L34 7 L38 16 L37 28 L30 36 L18 38 L7 33 L3 22 L5 10 L14 4 Z"
        fill="url(#rockShadow)"
      />
      {/* Rock texture cracks */}
      <path d="M14 8 L18 16" stroke="#7a5b10" strokeWidth="0.8" strokeLinecap="round" opacity="0.6" />
      <path d="M27 10 L31 20" stroke="#7a5b10" strokeWidth="0.8" strokeLinecap="round" opacity="0.5" />
      <path d="M9 24 L14 30" stroke="#7a5b10" strokeWidth="0.7" strokeLinecap="round" opacity="0.4" />

      {/* V carved into the rock */}
      <path
        d="M12 13 L19.5 29 L27 13"
        stroke="#1a0e00"
        strokeWidth="4"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
      {/* V highlight (gives carved depth) */}
      <path
        d="M12 13 L19.5 29 L27 13"
        stroke="#f0c96a"
        strokeWidth="1.2"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
        opacity="0.35"
      />
    </svg>
  );
}
