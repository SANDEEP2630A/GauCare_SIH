import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import './TrajectoryChart.css';

export default function TrajectoryChart({ scans }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (chartRef.current) chartRef.current.destroy();

    const labels = scans.map(s => s.date.slice(5));
    const values = scans.map(s => s.risk);

    chartRef.current = new Chart(canvasRef.current, {
      type: 'line',
      data: {
        labels,
        datasets: [{
          data: values,
          borderColor: '#0969da',
          backgroundColor: 'rgba(9, 105, 218, 0.06)',
          fill: true,
          tension: 0.3,
          pointRadius: 4,
          pointBackgroundColor: '#0969da',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          borderWidth: 2,
        }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: { duration: 550, easing: 'easeOutQuart' },
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { color: '#f0f0f0' }, ticks: { font: { size: 11 }, color: '#9ca3af' } },
          y: { min: 0, max: 100, grid: { color: '#f0f0f0' }, ticks: { font: { size: 11 }, color: '#9ca3af', callback: v => v + '%' } },
        },
      },
    });

    return () => { if (chartRef.current) chartRef.current.destroy(); };
  }, [scans]);

  return (
    <div className="trajectory-card">
      <div className="trajectory-label">Risk Trajectory</div>
      <div className="trajectory-wrap">
        <canvas ref={canvasRef} />
      </div>
    </div>
  );
}
