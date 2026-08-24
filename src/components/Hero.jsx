import { Link } from 'react-router-dom';
import { getRiskClass, getRiskLabel } from '../data/mockCowData';
import './Hero.css';

export default function Hero() {
  const previewRisk = 24;
  const cls = getRiskClass(previewRisk);

  return (
    <section className="hero">
      <div className="hero-bg-orb hero-bg-orb-1" />
      <div className="hero-bg-orb hero-bg-orb-2" />
      <div className="hero-bg-orb hero-bg-orb-3" />
      <div className="hero-inner">
        <div className="hero-content">
          <div className="hero-badge">
            <span className="hero-badge-dot" />
            Built for Indian dairy farms
          </div>
          <h1 className="hero-headline">
            Detect the risk<br />
            <span className="hero-headline-accent">before the symptoms.</span>
          </h1>
          <p className="hero-sub">
            Portable, offline-first mastitis risk forecasting. Multimodal sensing
            meets explainable AI &mdash; no internet required, results in seconds.
          </p>
          <div className="hero-actions">
            <Link to="/dashboard" className="hero-btn hero-btn-primary">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              View Live Dashboard
            </Link>
            <a href="#how-it-works" className="hero-btn hero-btn-ghost">How it works</a>
          </div>
          <div className="hero-stats">
            <div className="hero-stat">
              <span className="hero-stat-num">3</span>
              <span className="hero-stat-label">Sensors combined</span>
            </div>
            <div className="hero-stat-divider" />
            <div className="hero-stat">
              <span className="hero-stat-num">7-day</span>
              <span className="hero-stat-label">Prediction window</span>
            </div>
            <div className="hero-stat-divider" />
            <div className="hero-stat">
              <span className="hero-stat-num">0 ms</span>
              <span className="hero-stat-label">Internet needed</span>
            </div>
          </div>
        </div>
        <div className="hero-visual">
          <div className={`hero-card hero-card-${cls}`}>
            <div className="hero-card-shine" />
            <div className="hero-card-header">
              <span className="hero-card-title">Live Risk Assessment</span>
              <span className="hero-card-status">
                <span className="hero-card-status-dot" />
                Online
              </span>
            </div>
            <div className="hero-card-body">
              <div className="hero-card-cow">Cow COW-027</div>
              <div className="hero-card-risk">
                <span className={`hero-card-num hero-card-num-${cls}`}>{previewRisk}</span>
                <span className="hero-card-pct">%</span>
              </div>
              <span className={`hero-card-pill hero-card-pill-${cls}`}>{getRiskLabel(previewRisk)}</span>
            </div>
            <div className="hero-card-factors">
              <div className="hero-card-factor">
                <span className="hero-card-factor-label">Conductivity</span>
                <div className="hero-card-factor-bar"><div className="hero-card-factor-fill hero-card-factor-fill-low" style={{ width: '25%' }} /></div>
              </div>
              <div className="hero-card-factor">
                <span className="hero-card-factor-label">Spectral</span>
                <div className="hero-card-factor-bar"><div className="hero-card-factor-fill hero-card-factor-fill-low" style={{ width: '18%' }} /></div>
              </div>
              <div className="hero-card-factor">
                <span className="hero-card-factor-label">Temperature</span>
                <div className="hero-card-factor-bar"><div className="hero-card-factor-fill hero-card-factor-fill-low" style={{ width: '12%' }} /></div>
              </div>
            </div>
            <div className="hero-card-footer">7-day prediction window</div>
          </div>
        </div>
      </div>
    </section>
  );
}
