param(
    [switch]$SkipSeed,
    [switch]$RunSimulator
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$PgBin = Join-Path $RepoRoot "tmp\pgextract\pgsql\bin"
$PgData = Join-Path $RepoRoot "tmp\pgdata"
$BackendDir = Join-Path $RepoRoot "backend"
$FrontendDir = Join-Path $RepoRoot "frontend"
$SimulatorDir = Join-Path $RepoRoot "tools\device_simulator"

function Require-Path($Path, $Message) {
    if (!(Test-Path $Path)) {
        throw "$Message`nMissing: $Path"
    }
}

Require-Path $PgBin "PostgreSQL local runtime is not ready. Ask the RD lead to set up PostgreSQL first."
Require-Path $PgData "PostgreSQL data directory is not ready. Ask the RD lead to initialize PostgreSQL first."
Require-Path (Join-Path $BackendDir ".venv\Scripts\python.exe") "Backend Python venv is missing."
Require-Path (Join-Path $FrontendDir "package.json") "Frontend project is missing."

Write-Host "== Starting PostgreSQL ==" -ForegroundColor Cyan
$pgReady = & (Join-Path $PgBin "pg_isready.exe") -h 127.0.0.1 -p 5432 -U postgres 2>$null
if ($LASTEXITCODE -ne 0) {
    & (Join-Path $PgBin "pg_ctl.exe") -D $PgData -l (Join-Path $RepoRoot "tmp\pg.log") start
    Start-Sleep -Seconds 2
}
& (Join-Path $PgBin "pg_isready.exe") -h 127.0.0.1 -p 5432 -U postgres

Write-Host "== Preparing backend database ==" -ForegroundColor Cyan
Push-Location $BackendDir
try {
    .\.venv\Scripts\python.exe manage.py migrate --noinput
    if (!$SkipSeed) {
        .\.venv\Scripts\python.exe manage.py seed_demo
    }
}
finally {
    Pop-Location
}

Write-Host "== Starting backend: http://127.0.0.1:8000 ==" -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command",
    "cd '$BackendDir'; .\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000"
) -WindowStyle Normal

Write-Host "== Starting frontend: http://127.0.0.1:5173 ==" -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command",
    "cd '$FrontendDir'; npm run dev"
) -WindowStyle Normal

Start-Sleep -Seconds 3

if ($RunSimulator) {
    Write-Host "== Running virtual GPS/NFC simulator once ==" -ForegroundColor Cyan
    Push-Location $SimulatorDir
    try {
        python simulate_device.py `
            --base-url http://127.0.0.1:8000/api/v1 `
            --device-id device_001 `
            --device-token demo-device-token `
            --admin-username root `
            --admin-password root `
            flow --gps-count 2 --interval 1
    }
    finally {
        Pop-Location
    }
}

Write-Host ""
Write-Host "Local demo is starting." -ForegroundColor Green
Write-Host "Open: http://127.0.0.1:5173"
Write-Host "Login: root / root"
Write-Host "Role: 研发测试人员"
Write-Host ""
Write-Host "To send virtual GPS/NFC data later, run:" -ForegroundColor Yellow
Write-Host "cd $SimulatorDir"
Write-Host "python simulate_device.py --base-url http://127.0.0.1:8000/api/v1 --device-id device_001 --device-token demo-device-token --admin-username root --admin-password root flow --gps-count 2 --interval 1"
