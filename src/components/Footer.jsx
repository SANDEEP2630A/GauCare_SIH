import { CowFace } from './CowIcon';
import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-brand"><CowFace size={14} /> GauCare</div>
        <div className="footer-credit">SIH26109 &middot; Team Innovation</div>
        <div className="footer-disclaimer">
          GauCare is a screening aid, not a diagnostic tool. Always consult a qualified veterinarian for clinical decisions.
        </div>
      </div>
    </footer>
  );
}
