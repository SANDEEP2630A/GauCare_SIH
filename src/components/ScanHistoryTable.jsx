import { useState } from 'react';
import { getRiskClass, getRiskLabel } from '../data/mockCowData';
import './ScanHistoryTable.css';

export default function ScanHistoryTable({ scans }) {
  const [sortKey, setSortKey] = useState('date');
  const [sortAsc, setSortAsc] = useState(false);

  function handleSort(col) {
    if (sortKey === col) setSortAsc(!sortAsc);
    else { setSortKey(col); setSortAsc(true); }
  }

  const sorted = [...scans].sort((a, b) => {
    let va = a[sortKey] ?? a.date;
    let vb = b[sortKey] ?? b.date;
    if (sortKey === 'date') { va = a.date; vb = b.date; }
    if (sortKey === 'risk') { va = a.risk; vb = b.risk; }
    if (sortKey === 'level') { va = a.risk; vb = b.risk; }
    if (va < vb) return sortAsc ? -1 : 1;
    if (va > vb) return sortAsc ? 1 : -1;
    return 0;
  });

  return (
    <div className="history-card">
      <div className="history-label">Scan History</div>
      <table className="history-table">
        <thead>
          <tr>
            <th className={sortKey === 'date' ? 'active' : ''} onClick={() => handleSort('date')}>
              Date {sortKey === 'date' ? (sortAsc ? '\u2191' : '\u2193') : ''}
            </th>
            <th className={sortKey === 'risk' ? 'active' : ''} onClick={() => handleSort('risk')}>
              Risk % {sortKey === 'risk' ? (sortAsc ? '\u2191' : '\u2193') : ''}
            </th>
            <th className={sortKey === 'level' ? 'active' : ''} onClick={() => handleSort('level')}>
              Level {sortKey === 'level' ? (sortAsc ? '\u2191' : '\u2193') : ''}
            </th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((s, i) => {
            const cls = getRiskClass(s.risk);
            return (
              <tr key={i}>
                <td>{s.date}</td>
                <td>{s.risk}%</td>
                <td><span className={`hbadge hbadge-${cls}`}>{getRiskLabel(s.risk)}</span></td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
