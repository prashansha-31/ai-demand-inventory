import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TrendingUp, Cpu, AlertCircle, ChevronRight } from 'lucide-react';
import axios from 'axios';
import { getApiBaseUrl } from '../apiConfig.js';

const BACKEND_URL = getApiBaseUrl();

const Predictor = () => {
  const [form, setForm] = useState({ store: 1, dept: 1, year: new Date().getFullYear(), month: new Date().getMonth() + 1, week: 1 });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = e => setForm({ ...form, [e.target.name]: parseInt(e.target.value) || 0 });

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true); setError(null); setResult(null);
    try {
      await new Promise(r => setTimeout(r, 600));
      const res = await axios.post(`${BACKEND_URL}/api/predict`, form);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Cannot connect to backend. Is the server running?');
    } finally {
      setLoading(false);
    }
  };

  const months = ['January','February','March','April','May','June','July','August','September','October','November','December'];

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto' }}>
      {/* Header */}
      <motion.header initial={{ opacity: 0 }} animate={{ opacity: 1 }} style={{ marginBottom: '32px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '6px' }}>
          <div style={{ width: '4px', height: '28px', background: 'var(--secondary)', borderRadius: '2px', boxShadow: '0 0 10px var(--secondary-glow)' }} />
          <h1 className="glow-text-secondary" style={{ fontSize: '1.85rem', margin: 0 }}>Weekly Demand Forecaster</h1>
        </div>
        <p style={{ color: 'var(--text-muted)', marginLeft: '16px', fontSize: '0.9rem' }}>
          Enter store and department parameters to generate an AI-powered weekly sales forecast
        </p>
      </motion.header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '28px', alignItems: 'start' }}>
        {/* Form */}
        <motion.div initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }} className="glass-panel" style={{ padding: '28px' }}>
          <p className="section-title" style={{ marginBottom: '22px' }}>Forecast Parameters</p>
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>

            <div className="grid-2">
              <div>
                <label className="label-text">Store ID <span style={{ color: 'var(--text-muted)' }}>(1 – 45)</span></label>
                <input type="number" name="store" min="1" max="45" value={form.store} onChange={handleChange} className="input-field" required />
              </div>
              <div>
                <label className="label-text">Department ID <span style={{ color: 'var(--text-muted)' }}>(1 – 99)</span></label>
                <input type="number" name="dept" min="1" max="99" value={form.dept} onChange={handleChange} className="input-field" required />
              </div>
            </div>

            <div>
              <label className="label-text">Forecast Year</label>
              <input type="number" name="year" min="2010" value={form.year} onChange={handleChange} className="input-field" required />
            </div>

            <div className="grid-2">
              <div>
                <label className="label-text">Month</label>
                <select name="month" value={form.month} onChange={handleChange} className="input-field" style={{ cursor: 'pointer' }}>
                  {months.map((m, i) => <option key={i} value={i + 1}>{m}</option>)}
                </select>
              </div>
              <div>
                <label className="label-text">Week of Year <span style={{ color: 'var(--text-muted)' }}>(1 – 52)</span></label>
                <input type="number" name="week" min="1" max="52" value={form.week} onChange={handleChange} className="input-field" required />
              </div>
            </div>

            {/* Info box */}
            <div style={{ background: 'rgba(8, 145, 178, 0.06)', border: '1px solid rgba(8, 145, 178, 0.2)', borderRadius: '10px', padding: '12px 16px' }}>
              <p style={{ fontSize: '0.78rem', color: 'var(--text-muted)', lineHeight: 1.6 }}>
                The model uses <strong style={{ color: 'var(--primary-light)' }}>seasonal historical lag features</strong> from the same store, department, and month to generate accurate predictions. Seasonal patterns are captured from Walmart's 2010–2012 sales data.
              </p>
            </div>

            <button type="submit" className="btn-primary" style={{ justifyContent: 'center', marginTop: '4px' }} disabled={loading}>
              {loading ? <><Cpu size={16} /> Processing forecast...</> : <><ChevronRight size={16} /> Generate Forecast</>}
            </button>
          </form>
        </motion.div>

        {/* Results */}
        <div>
          <AnimatePresence mode="wait">
            {loading && (
              <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                className="glass-panel animate-pulse-glow" style={{ padding: '40px', textAlign: 'center' }}>
                <div className="spinner" style={{ margin: '0 auto 20px' }} />
                <p style={{ color: 'var(--text-secondary)', fontWeight: 500 }}>Running Random Forest inference...</p>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '6px' }}>Fetching seasonal lag features & computing prediction</p>
              </motion.div>
            )}

            {!loading && result && (
              <motion.div key="result" initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0 }}
                style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>

                {/* Main result */}
                <div className="glass-panel animate-pulse-glow" style={{ padding: '32px', textAlign: 'center', position: 'relative', overflow: 'hidden' }}>
                  <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: '3px', background: 'linear-gradient(90deg, var(--primary), var(--secondary), var(--accent))' }} />
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.78rem', textTransform: 'uppercase', letterSpacing: '0.1em', marginBottom: '10px' }}>Predicted Weekly Sales</p>
                  <h2 className="glow-text-accent" style={{ fontSize: '3.5rem', fontWeight: 800, margin: '0 0 8px', fontFamily: "'JetBrains Mono', monospace" }}>
                    ${result.predicted_sales?.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                  </h2>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginBottom: '16px' }}>
                    {result.inputs_used?.season} · Store {result.inputs_used?.store} · Dept {result.inputs_used?.dept} · Week {result.inputs_used?.week}
                  </p>
                  <div style={{ display: 'flex', justifyContent: 'center', gap: '12px', flexWrap: 'wrap' }}>
                    <span className="badge badge-green"><TrendingUp size={11} /> High Confidence</span>
                    <span className="badge badge-teal">R² 96.27%</span>
                    <span className="badge badge-blue">±$1,669 MAE</span>
                  </div>
                </div>

                {/* Historical data used */}
                {result.lag_features && (
                  <div className="glass-panel" style={{ padding: '20px' }}>
                    <p className="section-title" style={{ marginBottom: '14px', fontSize: '0.85rem' }}>Historical Data Used (Seasonal Match)</p>
                    <div className="grid-2" style={{ gap: '10px' }}>
                      {[
                        { label: 'Last-Week Sales (Lag 1)', value: `$${(result.lag_features.sales_lag1 || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` },
                        { label: '4-Week Prior Sales (Lag 4)', value: `$${(result.lag_features.sales_lag4 || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` },
                        { label: 'Seasonal Rolling Average', value: `$${(result.lag_features.rolling_mean || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` },
                        { label: 'Volatility (σ)', value: `$${(result.lag_features.rolling_std || 0).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}` },
                      ].map(({ label, value }) => (
                        <div key={label} style={{ background: 'rgba(8, 145, 178, 0.06)', borderRadius: '8px', padding: '10px 14px', border: '1px solid rgba(8, 145, 178, 0.12)' }}>
                          <p style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: '4px' }}>{label}</p>
                          <p style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--primary-light)', fontFamily: "'JetBrains Mono', monospace" }}>{value}</p>
                        </div>
                      ))}
                    </div>
                    <p style={{ fontSize: '0.73rem', color: 'var(--text-muted)', marginTop: '12px', lineHeight: 1.6 }}>
                      Based on <strong style={{ color: 'var(--text-secondary)' }}>{result.lag_features.data_points_found} data points</strong> from Store {result.inputs_used?.store}, Dept {result.inputs_used?.dept}, same month ({result.inputs_used?.season}) in the training dataset.
                    </p>
                  </div>
                )}
              </motion.div>
            )}

            {!loading && error && (
              <motion.div key="error" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-panel"
                style={{ padding: '28px', textAlign: 'center', borderColor: 'rgba(239, 68, 68, 0.3)' }}>
                <AlertCircle size={36} style={{ color: 'var(--danger)', marginBottom: '12px' }} />
                <p style={{ color: 'var(--danger)', fontWeight: 600, marginBottom: '6px' }}>Forecast Failed</p>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>{error}</p>
              </motion.div>
            )}

            {!loading && !result && !error && (
              <motion.div key="idle" initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                className="glass-panel" style={{ padding: '48px', textAlign: 'center' }}>
                <TrendingUp size={52} style={{ color: 'var(--border-hover)', margin: '0 auto 16px', display: 'block' }} />
                <p style={{ color: 'var(--text-muted)', fontSize: '1rem', fontWeight: 500 }}>Awaiting Parameters</p>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: '6px' }}>Fill in the form and click Generate Forecast</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
};

export default Predictor;
