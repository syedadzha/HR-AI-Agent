$env:PYTHONPATH = "backend"
# Try running pytest
if (Get-Command "pytest" -ErrorAction SilentlyContinue) {
    pytest backend/tests -v
} else {
    Write-Host "pytest not found. Attempting to run via python -m pytest..."
    python -m pytest backend/tests -v
}
