import { useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { cowData } from '../data/mockCowData';
import CowSelector from '../components/CowSelector';
import RiskReportCard from '../components/RiskReportCard';
import TrajectoryChart from '../components/TrajectoryChart';
import ScanHistoryTable from '../components/ScanHistoryTable';
import './Dashboard.css';

const cowIds = Object.keys(cowData);

export default function Dashboard() {
  const [selectedCow, setSelectedCow] = useState(cowIds[0]);
  const [scans, setScans] = useState(cowData);
  const [scanning, setScanning] = useState(false);
  const [animKey, setAnimKey] = useState(0);

  const currentScans = scans[selectedCow];
  const latest = currentScans[currentScans.length - 1];

  const handleCowChange = useCallback((id) => {
    setSelectedCow(id);
    setAnimKey(k => k + 1);
  }, []);

  const handleScan = useCallback(() => {
    setScanning(true);
    setTimeout(() => {
      setScans(prev => {
        const arr = [...prev[selectedCow]];
        const last = arr[arr.length - 1];
        const nr = Math.min(100, Math.max(0, last.risk + Math.round((Math.random() - 0.4) * 12)));
        const nc = Math.max(3.5, last.conductivity + (Math.random() - 0.4) * 0.6);
        const nt = Math.max(38, Math.min(40.5, last.temperature + (Math.random() - 0.45) * 0.3));
        const fl = { conductivity: 'Low', spectral: 'Low', temperature: 'Low', trend: 'Low' };
        if (nr > 25) fl.conductivity = 'Medium';
        if (nr > 50) { fl.conductivity = 'High'; fl.spectral = 'Medium'; fl.trend = 'Medium'; }
        if (nr > 70) { fl.spectral = 'High'; fl.trend = 'High'; fl.temperature = 'Medium'; }
        if (nr > 85) fl.temperature = 'High';
        arr.push({
          date: new Date().toISOString().slice(0, 10),
          conductivity: +nc.toFixed(1),
          temperature: +nt.toFixed(1),
          spectral_dev: nr > 60 ? 'Significant' : nr > 30 ? 'Mild Deviation' : 'Normal',
          risk: nr,
          factors: fl,
        });
        return { ...prev, [selectedCow]: arr };
      });
      setScanning(false);
      setAnimKey(k => k + 1);
    }, 650);
  }, [selectedCow]);

  return (
    <div className="dashboard">
      <header className="dash-header">
        <div className="dash-header-inner">
          <Link to="/" className="dash-logo">
            <span className="dash-logo-mark">MS</span>
            <span className="dash-logo-text">MastiSense Edge</span>
          </Link>
          <CowSelector
            cows={cowIds}
            selected={selectedCow}
            onChange={handleCowChange}
            onScan={handleScan}
            scanning={scanning}
          />
          <div className="dash-offline">
            <span className="dash-offline-dot" />
            Offline Active
          </div>
        </div>
      </header>

      <div className="dash-layout">
        <div className="dash-left">
          <RiskReportCard
            key={animKey}
            cowId={selectedCow}
            scan={latest}
            animate={true}
          />
        </div>
        <div className="dash-right">
          <TrajectoryChart scans={currentScans} />
          <ScanHistoryTable scans={currentScans} />
        </div>
      </div>
    </div>
  );
}
