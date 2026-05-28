// generateStaticParams must be in a server component (no 'use client')
// The actual UI is in SignalDetailClient which is a client component.

import SignalDetailClient from './SignalDetailClient';

export async function generateStaticParams() {
  return []; // client-side only — shell page
}

export default function SignalDetailPage() {
  return <SignalDetailClient />;
}
