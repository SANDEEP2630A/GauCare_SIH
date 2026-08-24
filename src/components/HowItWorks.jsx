import './HowItWorks.css';

const steps = [
  {
    num: '01',
    color: 'teal',
    title: 'Collect sample',
    desc: 'Draw a small milk sample into the sealed chamber.',
  },
  {
    num: '02',
    color: 'blue',
    title: 'Scan',
    desc: 'Press SCAN — sensors capture conductivity, spectrum, and temperature.',
  },
  {
    num: '03',
    color: 'violet',
    title: 'AI analysis',
    desc: 'On-device model evaluates risk against historical patterns.',
  },
  {
    num: '04',
    color: 'rose',
    title: 'Risk report',
    desc: 'Get a color-coded risk score with contributing factors in seconds.',
  },
];

export default function HowItWorks() {
  return (
    <section className="how" id="how-it-works">
      <div className="how-inner">
        <div className="how-header">
          <span className="how-eyebrow">Simple process</span>
          <h2 className="how-heading">How it works</h2>
          <p className="how-sub">From sample to actionable risk report in under 60 seconds.</p>
        </div>
        <div className="how-steps">
          {steps.map((s, i) => (
            <div className={`how-step how-step-${s.color}`} key={i} style={{ animationDelay: `${i * 0.12}s` }}>
              <div className={`how-num how-num-${s.color}`}>{s.num}</div>
              {i < steps.length - 1 && <div className={`how-connector how-connector-${s.color}`} />}
              <h3 className="how-step-title">{s.title}</h3>
              <p className="how-step-desc">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
