# Deploy on Render (single service)

One **Web Service** runs FastAPI: REST API under `/api/...`, Swagger at `/docs`, and the React app at `/` (with client-side routes like `/dashboard`).

## Blueprint

1. Push this repo to GitHub (or GitLab/Bitbucket).
2. [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
3. Select the repo; confirm `render.yaml` creates **one** service: `ai-demand-inventory`.
4. Deploy.

Build uses **`Dockerfile`**: Node builds `frontend/`, Python installs deps, `init_db.py` seeds SQLite, image runs `uvicorn` on `$PORT`.

## Environment

- **No `VITE_API_URL` required** for single deploy: the production build calls `/api/...` on the same host.

## Local “single service” check

```bash
cd frontend
npm ci
npm run build
cd ..
python init_db.py
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open `http://127.0.0.1:8000/` for the UI and `http://127.0.0.1:8000/docs` for the API.

## Large model file

If `models/demand_model_advanced.pkl` is too large for Git, use [Git LFS](https://git-lfs.com/) or another artifact strategy before the Docker build can succeed on Render.
