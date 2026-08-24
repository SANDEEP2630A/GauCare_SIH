import './CowSelector.css';

export default function CowSelector({ cows, selected, onChange, onScan, scanning }) {
  return (
    <div className="cow-selector">
      <div className="cow-selector-field">
        <label htmlFor="cowSelect">Cow ID</label>
        <select id="cowSelect" value={selected} onChange={e => onChange(e.target.value)}>
          {cows.map(c => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>
      <button className={`scan-btn${scanning ? ' scanning' : ''}`} onClick={onScan} disabled={scanning}>
        {scanning ? 'SCANNING\u2026' : 'SCAN'}
      </button>
    </div>
  );
}
