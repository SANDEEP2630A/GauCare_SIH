import './FeatureHighlights.css';

const features = [
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 12h-4l-3 9L9 3l-3 9H2"/>
      </svg>
    ),
    color: 'teal',
    title: 'Multimodal Sensing',
    desc: 'Combines conductivity, spectral, and temperature signals for a richer picture than any single sensor.',
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
      </svg>
    ),
    color: 'blue',
    title: 'Risk Trajectory',
    desc: 'Tracks the trend over time — not just a single reading, but the direction risk is heading.',
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
    ),
    color: 'violet',
    title: 'Explainable AI',
    desc: 'Shows exactly which signals are driving the score — no black box, full transparency.',
  },
  {
    icon: (
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
      </svg>
    ),
    color: 'rose',
    title: 'Fully Offline',
    desc: 'Runs locally on a Raspberry Pi — no internet connection needed, works in remote sheds.',
  },
];

export default function FeatureHighlights() {
  return (
    <section className="features">
      <div className="features-inner">
        <div className="features-header">
          <span className="features-eyebrow">Why MastiSense</span>
          <h2 className="features-heading">Built for the field,<br />designed for trust.</h2>
          <p className="features-sub">Everything a veterinarian or farmer needs to make confident decisions — right at the shed.</p>
        </div>
        <div className="features-grid">
          {features.map((f, i) => (
            <div className={`feature-card feature-card-${f.color}`} key={i} style={{ animationDelay: `${i * 0.1}s` }}>
              <div className="feature-card-top">
                <div className={`feature-icon feature-icon-${f.color}`}>{f.icon}</div>
              </div>
              <h3 className="feature-title">{f.title}</h3>
              <p className="feature-desc">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
