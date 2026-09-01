export function CowFace({ size = 20, className = '' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d="M3 8c0 0 1-3 4-3s3 2 5 2 3-2 5-2 4 3 4 3" />
      <path d="M3 8v6c0 4 3 7 9 7s9-3 9-7V8" />
      <circle cx="9" cy="11" r="1" fill="currentColor" stroke="none" />
      <circle cx="15" cy="11" r="1" fill="currentColor" stroke="none" />
      <ellipse cx="12" cy="14" rx="2" ry="1.5" />
    </svg>
  );
}

export function CowSilhouette({ size = 120, className = '' }) {
  return (
    <svg width={size} height={size * 0.7} viewBox="0 0 160 112" fill="none" className={className}>
      <path d="M20 30c0 0 4-16 18-16s14 10 26 10 16-10 26-10 18 16 18 16" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" opacity="0.15" />
      <path d="M15 35c-2 0-6 2-6 8v20c0 16 12 32 48 32s48-16 48-32V43c0-6-4-8-6-8" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" opacity="0.12" />
      <circle cx="55" cy="55" r="3" fill="currentColor" opacity="0.1" />
      <circle cx="85" cy="55" r="3" fill="currentColor" opacity="0.1" />
      <ellipse cx="70" cy="70" rx="8" ry="5" stroke="currentColor" strokeWidth="2" opacity="0.08" />
    </svg>
  );
}

export function CowSpot({ size = 40, className = '' }) {
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" fill="none" className={className}>
      <ellipse cx="20" cy="20" rx="16" ry="14" fill="currentColor" opacity="0.04" />
      <ellipse cx="18" cy="18" rx="10" ry="8" fill="currentColor" opacity="0.03" />
    </svg>
  );
}
