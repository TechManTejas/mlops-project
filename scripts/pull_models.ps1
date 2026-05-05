#!/usr/bin/env pwsh

dvc pull

if ($LASTEXITCODE -eq 0) {
    Write-Host "Models pulled successfully via DVC."
} else {
    Write-Error "dvc pull failed."
    exit $LASTEXITCODE
}
