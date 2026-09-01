
import './RiskReportCard.css';

export default function RiskReportCard({ cowId, scan }) {

  const predictionAvailable =
    scan &&
    scan.risk !== null &&
    scan.risk !== undefined;

  return (
    <div className="rcard rc-low">

      <div className="rcard-top">
        <span className="rcard-title">
          Mastitis Risk Report
        </span>

        <span className="rcard-cow">
          {cowId}
        </span>
      </div>

      <div className="rcard-body">

        {/* Risk score */}
        <div className="rcard-score">

          <div className="rcard-score-main">

            <span className="rcard-num rc-num-low">
              {predictionAvailable
                ? `${scan.risk}%`
                : '--'}
            </span>

            <span className="rcard-pill rc-pill-low">
              {predictionAvailable
                ? 'Prediction Available'
                : 'Prediction Pending'}
            </span>

          </div>

          <span className="rcard-window">
            7-day prediction
          </span>

        </div>


        {/* Sensor information */}
        <div className="rcard-section">

          <span className="rcard-section-title">
            Latest Sensor Reading
          </span>

          <div className="rcard-factors">

            <div className="rcard-factor">
              <span className="rcard-fname">
                Conductivity
              </span>

              <span className="rcard-fpct">
                {scan.conductivity} mS/cm
              </span>
            </div>


            <div className="rcard-factor">
              <span className="rcard-fname">
                Temperature
              </span>

              <span className="rcard-fpct">
                {scan.temperature} °C
              </span>
            </div>


            <div className="rcard-factor">
              <span className="rcard-fname">
                Milk pH
              </span>

              <span className="rcard-fpct">
                {scan.milk_pH}
              </span>
            </div>


            <div className="rcard-factor">
              <span className="rcard-fname">
                Somatic Cell Count
              </span>

              <span className="rcard-fpct">
                {scan.somatic_cell_count}
              </span>
            </div>

          </div>

        </div>


        {/* Recommendation */}
        <div className="rcard-rec rc-rec-low">

          <span className="rcard-rec-icon">
            ✓
          </span>

          <span>
            {predictionAvailable
              ? 'Risk prediction generated from the available scan data.'
              : 'Sensor data received successfully. Mastitis risk prediction will appear after the ML model is connected.'}
          </span>

        </div>

      </div>

    </div>
  );
}