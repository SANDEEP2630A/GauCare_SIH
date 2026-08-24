import { Link } from 'react-router-dom';
import './Navbar.css';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-logo">
          <span className="navbar-logo-mark">MS</span>
          <span className="navbar-logo-text">MastiSense Edge</span>
        </Link>
        <Link to="/dashboard" className="navbar-cta">Launch Dashboard</Link>
      </div>
    </nav>
  );
}
