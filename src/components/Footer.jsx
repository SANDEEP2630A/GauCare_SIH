import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-brand">MastiSense Edge</div>
        <div className="footer-credit">SIH26109 &middot; Team Innovation</div>
        <div className="footer-disclaimer">
          MastiSense Edge is a screening aid, not a diagnostic tool. Always consult a qualified veterinarian for clinical decisions.
        </div>
      </div>
    </footer>
  );
}
