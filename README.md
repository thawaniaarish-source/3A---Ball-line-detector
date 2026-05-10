# Multi-Sport Ball Line Detector

A modular app that decides whether a ball has touched the line (or stayed clear) from tracked camera data.

## Features
- Multi-sport decision profiles: table tennis, badminton, basketball, tennis.
- Geometry engine that can ingest any tracking source (OpenCV, DeepSORT, custom model).
- OpenCV camera helpers for quick prototyping.
- REST API for integration with scoreboards and replay systems.
- CLI mode for edge devices.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
pytest
ball-line-detector --sport table_tennis --x 50 --y 50 --r-mm 8 --line 40,40,40,100
```

## Run API
```bash
pip install -e .[api]
uvicorn app_api:app --reload
```
POST `/judge` payload:
```json
{
  "sport": "badminton",
  "x": 320,
  "y": 240,
  "r_mm": 14,
  "lines": [{"x1": 300, "y1": 50, "x2": 300, "y2": 420}]
}
```

## System architecture ideas for a production-grade version
1. **Ingest layer**: multi-camera RTSP streams with timestamp sync.
2. **Calibration layer**: court homography & automatic line map extraction.
3. **Tracking layer**: detector (YOLO/RT-DETR) + temporal tracker (ByteTrack/OCSORT).
4. **Decision layer**: this repository's geometry + sport-specific rules.
5. **Review layer**: confidence thresholds, replay clip, manual override UI.
6. **Audit layer**: persist frame evidence, hashes, and decision logs.


## Deploy to Vercel

This repository now includes a static UI (`public/index.html`) and a Vercel Python Serverless Function (`api/judge.py`).

- `/` serves the UI.
- `POST /api/judge` evaluates the line decision.
- `GET /api/judge` returns health JSON.

If your prior deployment showed nothing, it was because there was no static page or Vercel routing config.


### Vercel visibility fix

This repo now uses a root `index.html` and explicit `vercel.json` routes so `/` always renders a page and `/api/judge` resolves to the Python function.


### Why the Vercel build failed (setuptools error)

Vercel detected `pyproject.toml` and attempted a Python package build. With a flat repo layout containing top-level folders like `api/`, `public/`, and `ball_line_detector/`, setuptools package auto-discovery can fail with: `Multiple top-level packages discovered in a flat-layout`.

This is now fixed by explicitly telling setuptools to only package `ball_line_detector*` and exclude non-package folders.


## Exact steps to deploy on Vercel (FastAPI entrypoint fix)
1. Push this code to your GitHub repo (it now includes `api/main.py` with a top-level `app = FastAPI(...)`).
2. In Vercel, open your project settings and make sure the **Root Directory** points to this repo folder.
3. In Vercel, go to **Deployments** and click **Redeploy** on the latest commit (or push a new commit).
4. After deploy completes, open `https://<your-project>.vercel.app/` and confirm the UI loads.
5. Verify health endpoint in browser: `https://<your-project>.vercel.app/api/judge` (should return JSON status).
6. Test judge endpoint with POST (for example from Postman/curl):
   ```bash
   curl -X POST https://<your-project>.vercel.app/api/judge \
     -H "content-type: application/json" \
     -d '{"sport":"table_tennis","x":50,"y":50,"r_mm":8,"lines":[{"x1":40,"y1":40,"x2":40,"y2":100}]}'
   ```

If you still see the old error, clear Vercel build cache and redeploy:
- Project -> Settings -> Functions -> (or Deployments page) -> **Redeploy with existing Build Cache disabled**.
