import { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';
import './TrajectoryChart.css';

export default function TrajectoryChart({ scans }) {
  const canvasRef = useRef(null);
  const chartRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    // Destroy previous chart before creating a new one
    if (chartRef.current) {
      chartRef.current.destroy();
      chartRef.current = null;
    }

    if (!scans || scans.length === 0) return;

    // Previous scans + new scans
    const labels = scans.map((s, index) =>
      s.date ? s.date.slice(5) : `Scan ${index + 1}`
    );

    // Use ONLY real prediction values
    // No prediction = null, NOT 0
    const values = scans.map((s) =>
      Number.isFinite(Number(s.risk))
        ? Number(s.risk)
        : null
    );

    chartRef.current = new Chart(canvasRef.current, {
      type: 'line',

      data: {
        labels,

        datasets: [
          {
            label: 'Risk %',
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

            // Don't connect across missing predictions
            spanGaps: false,
          },
        ],
      },

      options: {
        responsive: true,
        maintainAspectRatio: false,

        animation: {
          duration: 550,
          easing: 'easeOutQuart',
        },

        plugins: {
          legend: {
            display: false,
          },
        },

        scales: {
          x: {
            grid: {
              color: '#f0f0f0',
            },

            ticks: {
              font: {
                size: 11,
              },

              color: '#9ca3af',
            },
          },

          y: {
            min: 0,
            max: 100,

            grid: {
              color: '#f0f0f0',
            },

            ticks: {
              font: {
                size: 11,
              },

              color: '#9ca3af',

              callback: (value) => `${value}%`,
            },
          },
        },
      },
    });

    return () => {
      if (chartRef.current) {
        chartRef.current.destroy();
        chartRef.current = null;
      }
    };
  }, [scans]);

  return (
    <div className="trajectory-card">
      <div className="trajectory-label">
        Risk Trajectory
      </div>

      <div className="trajectory-wrap">
        <canvas ref={canvasRef} />
      </div>
    </div>
  );
}