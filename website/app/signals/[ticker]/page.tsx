import SignalDetailClient from './SignalDetailClient';

const API = 'https://7qc9qknegk.execute-api.eu-north-1.amazonaws.com';

export async function generateStaticParams() {
  try {
    const res = await fetch(`${API}/signals`, { cache: 'no-store' });
    const data = await res.json();
    return (data.signals ?? []).map((s: { ticker: string }) => ({
      ticker: s.ticker.toLowerCase(),
    }));
  } catch {
    return [{ ticker: '_' }];
  }
}

export default function SignalDetailPage() {
  return <SignalDetailClient />;
}
