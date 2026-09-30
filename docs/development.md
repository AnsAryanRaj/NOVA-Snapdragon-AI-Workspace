# Development Guide for NOVA

This guide provides instructions for setting up and running NOVA frontend and backend services independently.

---

## Prerequisites
- Node.js (v18+)
- Python (3.10+)
- npm (v9+)

---

## Backend Setup & Execution

1. Navigate to backend workspace:
   ```bash
   cd backend
   ```

2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run FastAPI backend server:
   ```bash
   # From root directory:
   $env:PYTHONPATH="backend"
   .\backend\venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
   ```

4. Verify backend health endpoint:
   - Open browser or curl: `http://127.0.0.1:8000/api/health`

5. Run unit test suite:
   ```bash
   $env:PYTHONPATH="backend"
   .\backend\venv\Scripts\python -m pytest
   ```

---

## Frontend Setup & Execution

1. Navigate to frontend workspace:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run Vite development server:
   ```bash
   npm run dev
   ```
   Access at: `http://localhost:5173`

4. Build production distribution bundle:
   ```bash
   npm run build
   ```
