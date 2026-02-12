# SafeSight Analytics - System Test Script
# This script tests if all services are running correctly

Write-Host "SafeSight Analytics - System Test" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Test 1: Docker is running
Write-Host "[1/6] Checking Docker..." -ForegroundColor Yellow
$dockerRunning = docker info 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "      ✓ Docker is running" -ForegroundColor Green
} else {
    Write-Host "      ✗ Docker is not running" -ForegroundColor Red
    $allGood = $false
}

# Test 2: Backend container
Write-Host "[2/6] Checking backend container..." -ForegroundColor Yellow
$backendStatus = docker compose -f deploy/docker-compose.yml ps backend 2>&1 | Select-String "running"
if ($backendStatus) {
    Write-Host "      ✓ Backend container is running" -ForegroundColor Green
} else {
    Write-Host "      ✗ Backend container is not running" -ForegroundColor Red
    $allGood = $false
}

# Test 3: Frontend container
Write-Host "[3/6] Checking frontend container..." -ForegroundColor Yellow
$frontendStatus = docker compose -f deploy/docker-compose.yml ps frontend 2>&1 | Select-String "running"
if ($frontendStatus) {
    Write-Host "      ✓ Frontend container is running" -ForegroundColor Green
} else {
    Write-Host "      ✗ Frontend container is not running" -ForegroundColor Red
    $allGood = $false
}

# Test 4: Database container
Write-Host "[4/6] Checking database container..." -ForegroundColor Yellow
$dbStatus = docker compose -f deploy/docker-compose.yml ps database 2>&1 | Select-String "running"
if ($dbStatus) {
    Write-Host "      ✓ Database container is running" -ForegroundColor Green
} else {
    Write-Host "      ✗ Database container is not running" -ForegroundColor Red
    $allGood = $false
}

# Test 5: Backend API
Write-Host "[5/6] Testing backend API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -Method GET -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "      ✓ Backend API is responding" -ForegroundColor Green
    } else {
        Write-Host "      ✗ Backend API returned status $($response.StatusCode)" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "      ✗ Backend API is not responding" -ForegroundColor Red
    Write-Host "        Error: $($_.Exception.Message)" -ForegroundColor Gray
    $allGood = $false
}

# Test 6: Frontend
Write-Host "[6/6] Testing frontend..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 5 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "      ✓ Frontend is responding" -ForegroundColor Green
    } else {
        Write-Host "      ✗ Frontend returned status $($response.StatusCode)" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "      ✗ Frontend is not responding" -ForegroundColor Red
    Write-Host "        Error: $($_.Exception.Message)" -ForegroundColor Gray
    $allGood = $false
}

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "All tests passed! ✓" -ForegroundColor Green
    Write-Host ""
    Write-Host "System is ready for demo:" -ForegroundColor Cyan
    Write-Host "  Frontend:    http://localhost:5173" -ForegroundColor White
    Write-Host "  Backend API: http://localhost:8000" -ForegroundColor White
    Write-Host "  API Docs:    http://localhost:8000/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "Don't forget to create admin user:" -ForegroundColor Yellow
    Write-Host "  .\setup-admin.ps1" -ForegroundColor White
} else {
    Write-Host "Some tests failed. Please check the errors above." -ForegroundColor Red
    Write-Host ""
    Write-Host "To start the system:" -ForegroundColor Yellow
    Write-Host "  .\start-system.ps1" -ForegroundColor White
}

