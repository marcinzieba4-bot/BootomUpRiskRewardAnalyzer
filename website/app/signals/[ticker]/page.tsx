// Server component shell – generateStaticParams builds a placeholder page.
// The real ticker is read client-side by SignalDetailClient via useParams().

import SignalDetailClient from './SignalDetailClient';

// We export a single placeholder so the static exporter generates the shell HTML.
// At runtime useParams() reads the actual ticker from the URL.
export async function generateStaticParams() {
  return [{ ticker: '_' }];
}

export default function SignalDetailPage() {
  return <SignalDetailClient />;
}
