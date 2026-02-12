# SafeSight Analytics - Admin User Setup Script
# This script creates the initial admin user for the system

Write-Host "SafeSight Analytics - Admin User Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker status..." -ForegroundColor Yellow
$dockerRunning = docker info 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host "Docker is running ✓" -ForegroundColor Green
Write-Host ""

# Check if backend container is running
Write-Host "Checking backend container..." -ForegroundColor Yellow
$backendRunning = docker compose -f deploy/docker-compose.yml ps backend 2>&1 | Select-String "running"
if (-not $backendRunning) {
    Write-Host "ERROR: Backend container is not running." -ForegroundColor Red
    Write-Host "Please start the system first with: docker compose -f deploy/docker-compose.yml up" -ForegroundColor Yellow
    exit 1
}

Write-Host "Backend container is running ✓" -ForegroundColor Green
Write-Host ""

# Create admin user
Write-Host "Creating admin user..." -ForegroundColor Yellow
Write-Host ""

docker compose -f deploy/docker-compose.yml exec -T backend python create_admin.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Admin user setup complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Credentials:" -ForegroundColor Yellow
    Write-Host "  Username: admin" -ForegroundColor White
    Write-Host "  Password: admin123" -ForegroundColor White
    Write-Host ""
    Write-Host "You can now login at:" -ForegroundColor Yellow
    Write-Host "  API: http://localhost:8000/docs" -ForegroundColor White
    Write-Host "  Dashboard: http://localhost:5173" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERROR: Failed to create admin user." -ForegroundColor Red
    Write-Host "Check the error message above for details." -ForegroundColor Yellow
    exit 1
}

