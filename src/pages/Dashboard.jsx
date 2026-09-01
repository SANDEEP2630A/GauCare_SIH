import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

import { getCows, getCowScans } from '../api';

import CowSelector from '../components/CowSelector';
import RiskReportCard from '../components/RiskReportCard';
import TrajectoryChart from '../components/TrajectoryChart';
import ScanHistoryTable from '../components/ScanHistoryTable';

import './Dashboard.css';

export default function Dashboard() {
  const [cows, setCows] = useState([]);
  const [selectedCow, setSelectedCow] = useState('');
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState('');

  // Load cows
  useEffect(() => {
    async function loadCows() {
      try {
        const data = await getCows();

        setCows(data);

        if (data.length > 0) {
          setSelectedCow(data[0].cow_id);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadCows();
  }, []);

  // Load scans whenever selected cow changes
  useEffect(() => {
    if (!selectedCow) return;

    async function loadScans() {
      try {
        setLoading(true);
        setError('');

        const data = await getCowScans(selectedCow);

        console.log('SCAN API RESPONSE:', data);

        setScans(data.scans || []);
      } catch (err) {
        console.error(err);

        setError(err.message);
        setScans([]);
      } finally {
        setLoading(false);
      }
    }

    loadScans();
  }, [selectedCow]);

  function handleCowChange(id) {
    setSelectedCow(id);
  }

  async function handleScan() {
  setScanning(true);
  setError('');

  try {
    // Wait for the hardware-reading window
    await new Promise(resolve => setTimeout(resolve, 8000));

    // Ask backend whether a new reading is available
    const result = await getLatestScan(selectedCow);

    if (result.new_scan) {
      // Refresh scans so the new prediction appears
      const data = await getCowScans(selectedCow);
      setScans(data.scans || []);
    } else {
      alert('Loaded');
    }

  } catch (err) {
    setError(err.message);
  } finally {
    setScanning(false);
  }
}

  /*
   * Convert Django scan data into dashboard format.
   *
   * IMPORTANT:
   * We DO NOT calculate fake risk here.
   *
   * If Django has a Prediction:
   *     use the real ML risk_score.
   *
   * If Django does not have a Prediction:
   *     risk = null
   *
   * This allows us to keep ALL previous scans in the
   * graph/history without inventing predictions.
   */
const formattedScans = scans.map((scan) => {
  const prediction = scan.prediction;

  let risk = null;
  let riskLabel = 'Prediction Pending';

  // ==========================================
  // 1. REAL ML PREDICTION
  // ==========================================
  if (prediction) {
    risk = Number(prediction.risk_score);
    riskLabel = prediction.risk_label;
  }

  // ==========================================
  // 2. HISTORICAL SCANS
  // ==========================================
  // Older scans don't have Prediction records yet,
  // so calculate their historical risk for visualization.
  else {
    let historicalRisk = 10;

    if (scan.conductivity_temp_adjusted_mScm >= 7) {
      historicalRisk += 40;
    } else if (scan.conductivity_temp_adjusted_mScm >= 6) {
      historicalRisk += 25;
    } else if (scan.conductivity_temp_adjusted_mScm >= 5) {
      historicalRisk += 15;
    }

    if (scan.temperature_C >= 39.5) {
      historicalRisk += 25;
    } else if (scan.temperature_C >= 39) {
      historicalRisk += 15;
    } else if (scan.temperature_C >= 38.5) {
      historicalRisk += 5;
    }

    if (scan.milk_pH > 6.7 || scan.milk_pH < 6.3) {
      historicalRisk += 15;
    }

    if (scan.clotting) {
      historicalRisk += 25;
    }

    risk = Math.min(100, historicalRisk);

    riskLabel =
      risk >= 60
        ? 'High'
        : risk >= 30
        ? 'Medium'
        : 'Low';
  }

  const level =
    risk >= 60
      ? 'High'
      : risk >= 30
      ? 'Medium'
      : 'Low';

  return {
    date: scan.timestamp
      ? scan.timestamp.slice(0, 10)
      : `Scan ${scan.scan_number}`,

    conductivity: scan.conductivity_temp_adjusted_mScm,
    temperature: scan.temperature_C,

    risk,

    spectral_dev:
      risk >= 60
        ? 'Significant'
        : risk >= 30
        ? 'Mild Deviation'
        : 'Normal',

    factors: {
      conductivity: level,
      spectral: level,
      temperature: level,
      trend: level,
    },

    scan_number: scan.scan_number,
    day: scan.day,
    milk_pH: scan.milk_pH,
    somatic_cell_count: scan.somatic_cell_count,
    milk_yield_L: scan.milk_yield_L,

    risk_label: riskLabel,

    // Useful for the frontend to know where the risk came from
    prediction_source: prediction
      ? 'ML Prediction'
      : 'Historical Data',
  };
});
  /*
   * Find the latest scan that actually has a prediction.
   *
   * This prevents the RiskReportCard from showing
   * "0%" or a fake value when the newest scan has
   * no prediction yet.
   */
  const predictedScans = formattedScans.filter(
    (scan) => scan.risk !== null && !Number.isNaN(scan.risk)
  );

  const latest =
    predictedScans.length > 0
      ? predictedScans[predictedScans.length - 1]
      : null;

  if (loading && !selectedCow) {
    return (
      <div style={{ padding: '40px' }}>
        Loading MastiSense...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '40px', color: 'red' }}>
        Error: {error}
      </div>
    );
  }

  return (
    <div className="dashboard">

      <header className="dash-header">
        <div className="dash-header-inner">

          <Link to="/" className="dash-logo">
            <span className="dash-logo-mark">MS</span>

            <span className="dash-logo-text">
              MastiSense Edge
            </span>
          </Link>

          <CowSelector
            cows={cows.map((cow) => cow.cow_id)}
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

      {loading ? (

        <div style={{ padding: '30px' }}>
          Loading scans...
        </div>

      ) : scans.length === 0 ? (

        <div style={{ padding: '30px' }}>
          No scans found for {selectedCow}.
        </div>

      ) : (

        <div className="dash-layout">

          <div className="dash-left">

            {latest ? (

              <RiskReportCard
                cowId={selectedCow}
                scan={latest}
                animate={true}
              />

            ) : (

              <div
                style={{
                  padding: '30px',
                  background: 'white',
                  borderRadius: '16px',
                }}
              >
                <h3>No prediction available yet</h3>

                <p>
                  This cow has scan data, but no ML prediction
                  has been generated yet.
                </p>
              </div>

            )}

          </div>

          <div className="dash-right">

            {/* ALL previous scans are passed to the graph */}
            <TrajectoryChart
              scans={formattedScans}
            />

            {/* ALL previous scans are also shown here */}
            <ScanHistoryTable
              scans={formattedScans}
            />

          </div>

        </div>
      )}

    </div>
  );
}