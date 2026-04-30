/**
 * API base URL:
 * - Optional VITE_API_URL override (split deploy / custom backend).
 * - Production default: same origin (empty string → `/api/...`) when UI is served by FastAPI.
 * - Dev default: local uvicorn on port 8000.
 */
export const getApiBaseUrl = () => {
  const env = import.meta.env.VITE_API_URL;
  if (env && String(env).trim()) return String(env).replace(/\/$/, '');
  if (import.meta.env.PROD) return '';
  return 'http://localhost:8000';
};
