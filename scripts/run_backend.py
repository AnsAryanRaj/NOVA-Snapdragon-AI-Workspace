"""Development script to run the FastAPI backend server."""

import os
import sys
import uvicorn

if __name__ == "__main__":
    # Add backend directory to sys.path
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(project_root, "backend")
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

    print("Starting NOVA FastAPI Backend on http://127.0.0.1:8000 ...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
