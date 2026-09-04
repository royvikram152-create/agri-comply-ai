# AGRICOMPLY AI — Deployment Guide

This guide outlines steps for deploying **AGRICOMPLY AI** both locally and on **Vercel** with zero cost.

---

## 1. Local Development Setup

### Backend (FastAPI + Python 3.13)
```bash
# 1. Create and activate virtual environment
py -m venv backend/venv
backend/venv/Scripts/activate  # On Windows

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Set PYTHONPATH and run server
$env:PYTHONPATH="backend"
python -m uvicorn app.main:app --reload --port 8000
```
Backend API will be running at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### Frontend (React + Vite + Tailwind)
```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```
Frontend app will be running at `http://localhost:3000`.

---

## 2. Vercel Serverless Deployment

AGRICOMPLY AI is configured for 100% zero-cost deployment on Vercel using Python Serverless functions + Vite static build.

### Steps:
1. Push this repository to GitHub.
2. Log into [Vercel](https://vercel.com) and click **Add New Project**.
3. Import your GitHub repository.
4. Vercel automatically reads `vercel.json` and builds both:
   - Python backend API via `@vercel/python` (`api/index.py`).
   - React Vite frontend static bundle (`frontend/dist`).
5. Deploy! No API keys required.
