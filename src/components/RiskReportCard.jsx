import { useEffect, useRef, useState } from 'react';
import { getRiskClass, getRiskLabel, getRecommendation, factorMeta } from '../data/mockCowData';
import './RiskReportCard.css';

function animateNum(from, to, dur, cb) {
  const start = performance.now();
  let raf;
  function tick(now) {
    const t = Math.min((now - start) / dur, 1);
    const e = 1 - Math.pow(1 - t, 3);
    cb(Math.round(from + (to - from) * e));
    if (t < 1) raf = requestAnimationFrame(tick);
  }
  raf = requestAnimationFrame(tick);
  return () => cancelAnimationFrame(raf);
}

function pctFor(level) {
  return level === 'High' ? 88 : level === 'Medium' ? 55 : 22;
}

export default function RiskReportCard({ cowId, scan, animate }) {
  const [displayRisk, setDisplayRisk] = useState(animate ? 0 : scan.risk);
  const prevRisk = useRef(scan.risk);
  const cardRef = useRef(null);

  useEffect(() => {
    if (animate) {
      const cancel = animateNum(prevRisk.current, scan.risk, 480, setDisplayRisk);
      prevRisk.current = scan.risk;
      return cancel;
    }
    setDisplayRisk(scan.risk);
  }, [scan.risk, animate]);

  useEffect(() => {
    if (animate && cardRef.current) {
      cardRef.current.style.animation = 'none';
      cardRef.current.offsetHeight;
      cardRef.current.style.animation = 'reportSlide 0.35s ease both';
    }
  }, [cowId, animate]);

  const cls = getRiskClass(scan.risk);

  return (
    <div className={`rcard rc-${cls}`} ref={cardRef}>
      <div className="rcard-top">
        <span className="rcard-title">Mastitis Risk Report</span>
        <span className="rcard-cow">{cowId}</span>
      </div>

      <div className="rcard-body">
        {/* Risk score */}
        <div className="rcard-score">
          <div className="rcard-score-main">
            <span className={`rcard-num rc-num-${cls}`}>
              {displayRisk}<span className="rcard-pct">%</span>
            </span>
            <span className={`rcard-pill rc-pill-${cls}`}>{getRiskLabel(scan.risk)}</span>
          </div>
          <span className="rcard-window">7-day prediction</span>
        </div>

        {/* Factors */}
        <div className="rcard-section">
          <span className="rcard-section-title">Contributing Factors</span>
          <div className="rcard-factors">
            {factorMeta.map(m => {
              const level = scan.factors[m.key];
              const pct = pctFor(level);
              const up = m.isUp;
              return (
                <div className="rcard-factor" key={m.key}>
                  <span className={`rcard-ficon rc-ficon-${up ? 'up' : 'dn'}`}>
                    {up ? '\u2191' : '\u2193'}
                  </span>
                  <span className="rcard-fname">{m.label}</span>
                  <div className="rcard-fbar-wrap">
                    <div className="rcard-fbar-bg">
                      <div
                        className={`rcard-fbar rc-fbar-${up ? 'up' : 'dn'}`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    <span className={`rcard-fpct rc-fpct-${up ? 'up' : 'dn'}`}>
                      {up ? '+' : '-'}{pct}%
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Recommendation */}
        <div className={`rcard-rec rc-rec-${cls}`}>
          <span className="rcard-rec-icon">
            {cls === 'low' ? '\u2713' : cls === 'moderate' ? '\u26A0' : '\u25CF'}
          </span>
          <span>{getRecommendation(scan.risk)}</span>
        </div>
      </div>
    </div>
  );
}
