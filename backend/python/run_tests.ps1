Write-Host "Starting Regression Suite..."

# 1. Check if Docker is running
docker ps > $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: MongoDB is not running"
    exit 1
}
../../venv/Scripts/python.exe -m pytest django_app/tests/ --maxfail=1 --disable-warnings

# 3. Check result
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: All tests passed"
} else {
    Write-Host "Failure: Regression detected or Pytest not found"
    exit 1
}