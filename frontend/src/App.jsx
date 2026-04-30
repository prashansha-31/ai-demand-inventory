import { BrowserRouter as Router, Routes, Route, NavLink, Navigate } from 'react-router-dom';
import { LayoutDashboard, TrendingUp, Brain, BarChart3 } from 'lucide-react';
import Dashboard from './pages/Dashboard';
import Predictor from './pages/Predictor';
import ModelInfo from './pages/ModelInfo';
import './index.css';

const Sidebar = () => (
  <div className="sidebar">
    {/* Brand */}
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '36px', padding: '0 4px' }}>
      <div style={{
        background: 'linear-gradient(135deg, var(--primary), var(--secondary))',
        padding: '9px',
        borderRadius: '12px',
        boxShadow: '0 0 20px var(--primary-glow)',
        display: 'flex', alignItems: 'center', justifyContent: 'center'
      }}>
        <BarChart3 color="white" size={20} />
      </div>
      <div>
        <h2 style={{ fontSize: '1rem', fontWeight: 700, margin: 0, color: 'var(--text-main)' }}>DemandCast AI</h2>
        <p style={{ fontSize: '0.68rem', color: 'var(--text-muted)', margin: 0, marginTop: '1px' }}>Supply Chain Intelligence</p>
      </div>
    </div>

    {/* Nav */}
    <div style={{ marginBottom: '8px' }}>
      <p style={{ fontSize: '0.7rem', fontWeight: 600, color: 'var(--text-muted)', letterSpacing: '0.1em', textTransform: 'uppercase', padding: '0 14px', marginBottom: '8px' }}>Navigation</p>
      <nav style={{ display: 'flex', flexDirection: 'column' }}>
        <NavLink to="/dashboard" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <LayoutDashboard size={17} />
          <span>Analytics Dashboard</span>
        </NavLink>
        <NavLink to="/forecast" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <TrendingUp size={17} />
          <span>Demand Forecaster</span>
        </NavLink>
        <NavLink to="/model" className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
          <Brain size={17} />
          <span>Model Intelligence</span>
        </NavLink>
      </nav>
    </div>

    {/* Footer status */}
    <div style={{ marginTop: 'auto' }}>
      <hr className="divider" />
      <div className="glass-panel" style={{ padding: '14px 16px', background: 'rgba(8, 145, 178, 0.05)' }}>
        <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '6px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.08em' }}>Platform Status</p>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ width: '7px', height: '7px', borderRadius: '50%', background: 'var(--success)', boxShadow: '0 0 8px var(--accent-glow)' }} />
          <span style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>All Systems Online</span>
        </div>
        <div style={{ marginTop: '6px', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
          Random Forest · R² 96.27%
        </div>
      </div>
    </div>
  </div>
);

function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/forecast" element={<Predictor />} />
            <Route path="/model" element={<ModelInfo />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
