import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Brain, Award, Layers, GitBranch } from 'lucide-react';
import axios from 'axios';
import { getApiBaseUrl } from '../apiConfig.js';

const BACKEND_URL = getApiBaseUrl();

const ModelInfo = () => {
  const [info, setInfo] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${BACKEND_URL}/api/model-info`)
      .then(r => setInfo(r.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '70vh', flexDirection: 'column', gap: '16px' }}>
      <div className="spinner" />
      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Loading model data...</p>
    </div>
  );

  const maxR2 = Math.max(...(info?.model_comparison || []).map(m => m.test_r2));

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <motion.header initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '6px' }}>
          <div style={{ width: '4px', height: '28px', background: 'var(--accent)', borderRadius: '2px', boxShadow: '0 0 10px var(--accent-glow)' }} />
          <h1 className="glow-text-accent" style={{ fontSize: '1.85rem', margin: 0 }}>Model Intelligence</h1>
        </div>
        <p style={{ color: 'var(--text-muted)', marginLeft: '16px', fontSize: '0.9rem' }}>
          AI-Based Demand Forecasting &amp; Inventory Optimization Platform — Model Evaluation Report
        </p>
      </motion.header>

      {/* Dataset + Winner Cards */}
      <div className="grid-3" style={{ marginBottom: '24px' }}>
        {[
          { icon: Brain, title: 'Selected Model', val: 'Random Forest', sub: 'Best overall performance', color: 'var(--accent)', glow: 'var(--accent-glow)' },
          { icon: Layers, title: 'Training Dataset', val: '421,570', sub: 'Walmart weekly sales records', color: 'var(--primary)', glow: 'var(--primary-glow)' },
          { icon: Award, title: 'Test Accuracy (R²)', val: `${((info?.r2_score || 0) * 100).toFixed(2)}%`, sub: `MAE ±$${(info?.mae || 0).toLocaleString('en-US', { maximumFractionDigits: 0 })}  ·  RMSE $${(info?.rmse || 0).toLocaleString('en-US', { maximumFractionDigits: 0 })}`, color: 'var(--secondary)', glow: 'var(--secondary-glow)' },
        ].map((c, i) => (
          <motion.div key={i} initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.06 }}
            className="glass-panel" style={{ padding: '22px', display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ padding: '12px', borderRadius: '12px', background: `${c.color}18`, flexShrink: 0 }}>
              <c.icon style={{ color: c.color, filter: `drop-shadow(0 0 6px ${c.glow})` }} size={22} />
            </div>
            <div>
              <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em', marginBottom: '4px' }}>{c.title}</p>
              <p style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-main)', marginBottom: '3px', fontFamily: "'JetBrains Mono', monospace" }}>{c.val}</p>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{c.sub}</p>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Model Comparison Table */}
      <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
        className="glass-panel" style={{ padding: '24px', marginBottom: '24px' }}>
        <p className="section-title" style={{ marginBottom: '16px' }}>Model Comparison — All Algorithms Evaluated</p>
        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Algorithm</th>
                <th>Test R²</th>
                <th>Test MAE ($)</th>
                <th>Test RMSE ($)</th>
                <th>CV R² Mean</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {(info?.model_comparison || []).map((m, i) => (
                <tr key={i}>
                  <td style={{ color: 'var(--text-muted)', fontFamily: "'JetBrains Mono', monospace", fontSize: '0.8rem' }}>{i + 1}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      {m.best && <Award size={13} className="color-accent" />}
                      <span style={{ fontWeight: m.best ? 600 : 400, color: m.best ? 'var(--accent-light)' : 'var(--text-main)' }}>{m.name}</span>
                    </div>
                  </td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <span style={{ fontFamily: "'JetBrains Mono', monospace", fontWeight: 600, color: m.best ? 'var(--accent-light)' : 'var(--text-main)', minWidth: '52px' }}>
                        {(m.test_r2 * 100).toFixed(2)}%
                      </span>
                      <div className="progress-bar-track" style={{ width: '70px' }}>
                        <div className="progress-bar-fill" style={{ width: `${(m.test_r2 / maxR2) * 100}%`, background: m.best ? 'linear-gradient(90deg, var(--accent), var(--primary))' : 'linear-gradient(90deg, var(--primary), var(--secondary))' }} />
                      </div>
                    </div>
                  </td>
                  <td style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '0.83rem', color: 'var(--text-muted)' }}>{m.test_mae.toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '0.83rem', color: 'var(--text-muted)' }}>{m.test_rmse.toLocaleString('en-US', { minimumFractionDigits: 2 })}</td>
                  <td style={{ fontFamily: "'JetBrains Mono', monospace", fontSize: '0.83rem', color: 'var(--text-muted)' }}>{m.cv_r2 > 0 ? `${(m.cv_r2 * 100).toFixed(2)}%` : '—'}</td>
                  <td>{m.best ? <span className="badge badge-green"><Award size={10} /> Selected</span> : <span className="badge badge-blue">Evaluated</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>

      {/* Feature Importance + Best Params */}
      <div className="grid-2" style={{ marginBottom: '24px' }}>
        {/* Feature Importance */}
        <motion.div initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }} className="glass-panel" style={{ padding: '22px' }}>
          <p className="section-title" style={{ marginBottom: '18px' }}>Feature Importance (Random Forest)</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {(info?.feature_importance || []).map((f, i) => (
              <div key={i}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', fontFamily: "'JetBrains Mono', monospace" }}>{f.feature}</span>
                  <span style={{ fontSize: '0.78rem', fontWeight: 600, color: f.importance > 0.5 ? 'var(--accent-light)' : 'var(--text-muted)', fontFamily: "'JetBrains Mono', monospace" }}>
                    {(f.importance * 100).toFixed(2)}%
                  </span>
                </div>
                <div className="progress-bar-track">
                  <motion.div initial={{ width: 0 }} animate={{ width: `${f.importance * 100}%` }} transition={{ delay: 0.5 + i * 0.05, duration: 0.6 }}
                    className="progress-bar-fill"
                    style={{ background: f.importance > 0.5 ? 'linear-gradient(90deg, var(--accent), var(--primary))' : f.importance > 0.05 ? 'linear-gradient(90deg, var(--primary), var(--secondary))' : 'rgba(100,116,139,0.5)' }}
                  />
                </div>
              </div>
            ))}
          </div>
          <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '14px', lineHeight: 1.6 }}>
            <strong style={{ color: 'var(--accent-light)' }}>sales_lag1</strong> (prior week sales) dominates at 90.75%, confirming strong autocorrelation in retail demand patterns.
          </p>
        </motion.div>

        {/* Best params + training info */}
        <motion.div initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.35 }} className="glass-panel" style={{ padding: '22px' }}>
          <p className="section-title" style={{ marginBottom: '18px' }}>Hyperparameters &amp; Training Details</p>

          {/* Best params */}
          <div style={{ marginBottom: '20px' }}>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '10px' }}>Tuned Hyperparameters (GridSearchCV)</p>
            <div className="grid-2" style={{ gap: '8px' }}>
              {Object.entries(info?.best_params || {}).map(([k, v]) => (
                <div key={k} style={{ background: 'rgba(8, 145, 178, 0.06)', border: '1px solid rgba(8, 145, 178, 0.15)', borderRadius: '8px', padding: '10px 14px' }}>
                  <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginBottom: '3px' }}>{k}</p>
                  <p style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--primary-light)', fontFamily: "'JetBrains Mono', monospace" }}>{v}</p>
                </div>
              ))}
            </div>
          </div>

          <hr className="divider" />

          {/* Training stats */}
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '10px' }}>Dataset &amp; Training Statistics</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {[
              { label: 'Dataset', val: info?.dataset },
              { label: 'Date Range', val: info?.date_range },
              { label: 'Total Records', val: (info?.total_records || 0).toLocaleString() },
              { label: 'Training Samples', val: (info?.training_samples || 0).toLocaleString() },
              { label: 'Test Samples', val: (info?.test_samples || 0).toLocaleString() },
              { label: 'Features', val: `${info?.feature_count || 0} engineered features` },
              { label: 'Stores', val: info?.stores_count },
              { label: 'Departments', val: info?.departments_count },
            ].map(({ label, val }) => (
              <div key={label} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid rgba(255,255,255,0.04)' }}>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{label}</span>
                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', fontFamily: "'JetBrains Mono', monospace" }}>{val}</span>
              </div>
            ))}
          </div>

          {/* Feature list */}
          <hr className="divider" />
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '10px' }}>Feature Set</p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
            {(info?.features || []).map(f => (
              <span key={f} style={{ background: 'rgba(59, 130, 246, 0.08)', border: '1px solid rgba(59, 130, 246, 0.2)', color: 'var(--secondary-light)', padding: '3px 10px', borderRadius: '6px', fontSize: '0.75rem', fontFamily: "'JetBrains Mono', monospace" }}>
                {f}
              </span>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Pipeline summary */}
      <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
        className="glass-panel" style={{ padding: '22px' }}>
        <p className="section-title" style={{ marginBottom: '16px' }}>
          <GitBranch size={14} style={{ marginRight: '6px' }} />
          ML Pipeline Summary
        </p>
        <div style={{ display: 'flex', gap: '0', overflowX: 'auto' }}>
          {[
            { step: '1', label: 'Data Ingestion', detail: 'Walmart SQLite DB\n421,570 records' },
            { step: '2', label: 'Feature Engineering', detail: 'Lag features, rolling stats,\ndate decomposition' },
            { step: '3', label: 'Model Training', detail: '11 algorithms evaluated\nGridSearchCV tuning' },
            { step: '4', label: 'Model Selection', detail: 'Random Forest selected\nR² = 96.27%' },
            { step: '5', label: 'API Deployment', detail: 'FastAPI backend\nSeasonal prediction' },
          ].map((s, i, arr) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', flex: 1, minWidth: '140px' }}>
              <div style={{ textAlign: 'center', flex: 1, padding: '0 4px' }}>
                <div style={{ width: '36px', height: '36px', borderRadius: '50%', background: 'linear-gradient(135deg, var(--primary), var(--secondary))', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 8px', fontSize: '0.8rem', fontWeight: 700, color: 'white', boxShadow: '0 0 12px var(--primary-glow)' }}>{s.step}</div>
                <p style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '4px' }}>{s.label}</p>
                <p style={{ fontSize: '0.71rem', color: 'var(--text-muted)', whiteSpace: 'pre-line', lineHeight: 1.5 }}>{s.detail}</p>
              </div>
              {i < arr.length - 1 && (
                <div style={{ width: '24px', flexShrink: 0, height: '2px', background: 'linear-gradient(90deg, var(--primary), var(--secondary))', opacity: 0.4 }} />
              )}
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default ModelInfo;
