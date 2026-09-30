# Development Setup Script for NOVA
Write-Host "Setting up NOVA Workspace Assistant Environment..." -ForegroundColor Cyan

# Check Python & Node
Write-Host "Checking runtime environments..." -ForegroundColor Yellow
python --version
node -v
npm -v

# Initialize Python Virtual Environment for Backend if needed
if (-not (Test-Path "backend\venv")) {
    Write-Host "Creating Python virtual environment in backend\venv..." -ForegroundColor Yellow
    python -m venv backend\venv
}

Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
.\backend\venv\Scripts\pip install -r backend\requirements.txt

# Install Frontend Dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install
Set-Location ..

Write-Host "Setup Complete! NOVA is ready for development." -ForegroundColor Green
