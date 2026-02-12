# SafeSight Analytics - System Startup Script
# This script starts all services using Docker Compose

Write-Host "SafeSight Analytics - Starting System" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
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

# Navigate to deploy directory
if (-not (Test-Path "deploy/docker-compose.yml")) {
    Write-Host "ERROR: docker-compose.yml not found. Are you in the SafeSight directory?" -ForegroundColor Red
    exit 1
}

Write-Host "Starting all services..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  IMPORTANT: This will keep running and show logs - THIS IS NORMAL!" -ForegroundColor Cyan
Write-Host "   The terminal staying active means your services are running." -ForegroundColor Cyan
Write-Host "   Open a NEW terminal window for other commands." -ForegroundColor Cyan
Write-Host ""
Write-Host "Services will be available at:" -ForegroundColor Cyan
Write-Host "  Frontend:    http://localhost:5173" -ForegroundColor White
Write-Host "  Backend API: http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:    http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "To run in background instead, use: docker compose up --build -d" -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
Write-Host ""

# Start services
cd deploy
docker compose up --build

