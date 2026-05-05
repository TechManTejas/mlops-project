#!/usr/bin/env pwsh

if (-not (Test-Path ".\\venv\\Scripts\\Activate.ps1")) {
    Write-Error "Virtual environment not found at .\\venv"
    exit 1
}

. .\\venv\\Scripts\\Activate.ps1

python -m bentoml serve src.mlops_project.service:ParkingDetectorService --reload --port 3000
