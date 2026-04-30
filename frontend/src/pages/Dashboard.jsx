import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, Activity, BarChart2, TrendingUp, Database, Package } from 'lucide-react';
import axios from 'axios';
import { getApiBaseUrl } from '../apiConfig.js';

const BACKEND_URL = getApiBaseUrl();

const KpiCard = ({ title, value, subtitle, icon: Icon, colorClass, glowClass, delay = 0 }) => (
  <motion.div
    initial={{ opacity: 0, y: 18 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay, duration: 0.4 }}
    className="glass-panel stat-card"
    style={{ padding: '20px' }}
  >
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
      <div style={{ flex: 1 }}>
        <p style={{ color: 'var(--text-muted)', fontSize: '0.72rem', fontWeight: 600, marginBottom: '8px', textTransform: 'uppercase', letterSpacing: '0.08em' }}>{title}</p>
        <h3 className={glowClass} style={{ fontSize: '1.65rem', fontWeight: 700, margin: '0 0 5px', fontFamily: "'JetBrains Mono', monospace" }}>{value}</h3>
        {subtitle && <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{subtitle}</p>}
      </div>
      <div style={{ padding: '10px', borderRadius: '10px', background: 'rgba(255,255,255,0.04)', flexShrink: 0, marginLeft: '12px' }}>
        <Icon className={colorClass} size={20} />
      </div>
    </div>
  </motion.div>
);

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [modelInfo, setModelInfo] = useState(null);
  const [top, setTop] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const [s, h, m, t] = await Promise.all([
          axios.get(`${BACKEND_URL}/api/dashboard/stats`),
          axios.get(`${BACKEND_URL}/api/dashboard/history?per_page=8`),
          axios.get(`${BACKEND_URL}/api/model-info`),
          axios.get(`${BACKEND_URL}/api/dashboard/top`),
        ]);
        setStats(s.data);
        setHistory(h.data.data || []);
        setModelInfo(m.data);
        setTop(t.data);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '70vh', flexDirection: 'column', gap: '16px' }}>
      <div className="spinner" />
      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Loading analytics...</p>
    </div>
  );

  const totalPreds = history.length;
  const totalForecasted = stats?.total_sales || 0;

  return (
    <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
      {/* Header */}
      <motion.header initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '6px' }}>
          <div style={{ width: '4px', height: '28px', background: 'var(--primary)', borderRadius: '2px', boxShadow: '0 0 10px var(--primary-glow)' }} />
          <h1 className="glow-text" style={{ fontSize: '1.85rem', margin: 0 }}>Supply Chain Analytics</h1>
        </div>
        <p style={{ color: 'var(--text-muted)', marginLeft: '16px', fontSize: '0.9rem' }}>
          AI-powered demand forecasting · Walmart Retail Dataset · Random Forest Model
        </p>
      </motion.header>

      {/* KPI Cards */}
      <div className="grid-4" style={{ marginBottom: '24px' }}>
        <KpiCard title="Model Accuracy (R²)" value={`${((modelInfo?.r2_score || 0) * 100).toFixed(2)}%`} subtitle="Random Forest Regressor" icon={CheckCircle} colorClass="color-accent" glowClass="glow-text-accent" delay={0} />
        <KpiCard title="Mean Absolute Error" value={`±$${(modelInfo?.mae || 0).toLocaleString('en-US', { maximumFractionDigits: 0 })}`} subtitle="Per weekly sales forecast" icon={Activity} colorClass="color-primary" glowClass="glow-text" delay={0.05} />
        <KpiCard title="Training Samples" value={(modelInfo?.training_samples || 0).toLocaleString()} subtitle={`${modelInfo?.feature_count || 0} features · ${modelInfo?.stores_count || 45} stores`} icon={Database} colorClass="color-secondary" glowClass="glow-text-secondary" delay={0.1} />
        <KpiCard title="Demand Alert" value={stats?.demand_alert || '—'} subtitle={`Quality Index: ${stats?.quality_index || 0}%`} icon={TrendingUp} colorClass="color-primary" glowClass="glow-text" delay={0.15} />
      </div>

      {/* Row 2: Model status + Top performers */}
      <div className="grid-2" style={{ marginBottom: '24px' }}>
        {/* Model Performance */}
        <motion.div initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }} className="glass-panel" style={{ padding: '22px' }}>
          <p className="section-title">Model Performance</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {[
              { label: 'R² Score', value: `${((modelInfo?.r2_score || 0) * 100).toFixed(2)}%`, pct: (modelInfo?.r2_score || 0) * 100, color: 'var(--accent)' },
              { label: 'CV R² Mean', value: '94.82%', pct: 94.82, color: 'var(--primary)' },
              { label: 'Confidence Score', value: `${stats?.confidence_score || 0}%`, pct: stats?.confidence_score || 0, color: 'var(--secondary)' },
              { label: 'Quality Index', value: `${stats?.quality_index || 0}%`, pct: stats?.quality_index || 0, color: 'var(--accent)' },
            ].map(m => (
              <div key={m.label}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>{m.label}</span>
                  <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', fontFamily: "'JetBrains Mono', monospace" }}>{m.value}</span>
                </div>
                <div className="progress-bar-track">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${Math.min(m.pct, 100)}%` }} transition={{ delay: 0.4, duration: 0.8 }} className="progress-bar-fill" style={{ background: `linear-gradient(90deg, ${m.color}, ${m.color}88)` }} />
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Top Stores */}
        <motion.div initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.25 }} className="glass-panel" style={{ padding: '22px' }}>
          <p className="section-title">Top Performing Stores</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {(top?.top_stores || []).slice(0, 5).map((s, i) => {
              const maxSales = top?.top_stores?.[0]?.total_sales || 1;
              return (
                <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{ width: '26px', height: '26px', borderRadius: '8px', background: 'rgba(8, 145, 178, 0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.75rem', fontWeight: 700, color: 'var(--primary-light)', flexShrink: 0 }}>
                    {s.store}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                      <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Store {s.store}</span>
                      <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-secondary)', fontFamily: "'JetBrains Mono', monospace" }}>${(s.total_sales / 1000).toFixed(0)}K</span>
                    </div>
                    <div className="progress-bar-track">
                      <motion.div initial={{ width: 0 }} animate={{ width: `${(s.total_sales / maxSales) * 100}%` }} transition={{ delay: 0.5 + i * 0.08, duration: 0.6 }} className="progress-bar-fill" style={{ background: 'linear-gradient(90deg, var(--primary), var(--secondary))' }} />
                    </div>
                  </div>
                </div>
              );
            })}
            {(!top?.top_stores || top.top_stores.length === 0) && (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', padding: '16px 0' }}>Run forecasts to see data</p>
            )}
          </div>
        </motion.div>
      </div>

      {/* Recent Predictions */}
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-panel" style={{ padding: '24px' }}>
        <p className="section-title">Recent Demand Forecasts</p>
        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Store</th>
                <th>Department</th>
                <th>Forecast Date</th>
                <th>Predicted Weekly Sales</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {history.map((row, i) => (
                <tr key={i}>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Package size={14} className="color-primary" />
                      <span>Store {row.store}</span>
                    </div>
                  </td>
                  <td>Dept {row.dept}</td>
                  <td style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '0.82rem', color: 'var(--text-muted)' }}>{row.date}</td>
                  <td>
                    <span className="glow-text-accent" style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 600 }}>
                      ${parseFloat(row.predicted_sales).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                    </span>
                  </td>
                  <td><span className="badge badge-teal">Forecasted</span></td>
                </tr>
              ))}
              {history.length === 0 && (
                <tr><td colSpan={5} style={{ textAlign: 'center', padding: '32px', color: 'var(--text-muted)' }}>No forecasts yet. Use the Demand Forecaster to generate predictions.</td></tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Dataset info footer */}
        <div style={{ display: 'flex', gap: '24px', marginTop: '20px', paddingTop: '16px', borderTop: '1px solid var(--border-color)', flexWrap: 'wrap' }}>
          {[
            { label: 'Dataset', value: 'Walmart Weekly Sales' },
            { label: 'Period', value: '2010 – 2012' },
            { label: 'Records', value: '421,570' },
            { label: 'Stores', value: '45' },
            { label: 'Departments', value: '81' },
            { label: 'Algorithm', value: 'Random Forest' },
          ].map(d => (
            <div key={d.label}>
              <p style={{ fontSize: '0.68rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '2px' }}>{d.label}</p>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', fontWeight: 600 }}>{d.value}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
