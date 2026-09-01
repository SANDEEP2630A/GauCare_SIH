import { Link } from 'react-router-dom';
import { CowFace } from './CowIcon';
import './Navbar.css';

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-logo">
          <span className="navbar-logo-mark"><CowFace size={16} /></span>
          <span className="navbar-logo-text">GauCare</span>
        </Link>
        <Link to="/dashboard" className="navbar-cta">Launch Dashboard</Link>
      </div>
    </nav>
  );
}
