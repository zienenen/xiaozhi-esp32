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

function Get-LanIp {
    $preferred = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
        Where-Object {
            $_.IPAddress -notlike "127.*" -and
            $_.IPAddress -notlike "169.254.*" -and
            $_.InterfaceAlias -notmatch "Mihomo|Loopback|VMware|VirtualBox|vEthernet|WSL"
        } |
        Sort-Object @{ Expression = { if ($_.InterfaceAlias -match "WLAN|Wi-Fi|无线") { 0 } elseif ($_.InterfaceAlias -match "以太网|Ethernet") { 1 } else { 2 } } }, InterfaceMetric |
        Select-Object -First 1

    if ($preferred) {
        return $preferred.IPAddress
    }
    return "127.0.0.1"
}

function Set-EnvValue($Path, $Key, $Value) {
    $line = "$Key=$Value"
    if (!(Test-Path $Path)) {
        Set-Content -Path $Path -Value $line -Encoding UTF8
        return
    }

    $content = Get-Content -Path $Path
    $matched = $false
    $next = foreach ($item in $content) {
        if ($item -match "^$([regex]::Escape($Key))=") {
            $matched = $true
            $line
        }
        else {
            $item
        }
    }

    if (!$matched) {
        $next += $line
    }
    Set-Content -Path $Path -Value $next -Encoding UTF8
}

function Require-Path($Path, $Message) {
    if (!(Test-Path $Path)) {
        throw "$Message`nMissing: $Path"
    }
}

Require-Path $PgBin "PostgreSQL local runtime is not ready. Ask the RD lead to set up PostgreSQL first."
Require-Path $PgData "PostgreSQL data directory is not ready. Ask the RD lead to initialize PostgreSQL first."
Require-Path (Join-Path $BackendDir ".venv\Scripts\python.exe") "Backend Python venv is missing."
Require-Path (Join-Path $FrontendDir "package.json") "Frontend project is missing."

$LanIp = Get-LanIp
$BackendEnv = Join-Path $BackendDir ".env"
$AllowedHosts = "127.0.0.1,localhost,$LanIp"
$CorsOrigins = "http://127.0.0.1:5173,http://localhost:5173,http://127.0.0.1:4173,http://localhost:4173,http://${LanIp}:5173,http://${LanIp}:4173"

Write-Host "== Detected LAN IP: $LanIp ==" -ForegroundColor Cyan
Set-EnvValue $BackendEnv "DJANGO_ALLOWED_HOSTS" $AllowedHosts
Set-EnvValue $BackendEnv "CORS_ALLOWED_ORIGINS" $CorsOrigins

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

Write-Host "== Starting backend: http://0.0.0.0:8000 ==" -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command",
    "cd '$BackendDir'; .\.venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000"
) -WindowStyle Normal

Write-Host "== Starting frontend: http://0.0.0.0:5173 ==" -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-ExecutionPolicy", "Bypass",
    "-Command",
    "cd '$FrontendDir'; npm run dev -- --host 0.0.0.0"
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
Write-Host "Open on this computer: http://127.0.0.1:5173"
Write-Host "Open from LAN/mobile: http://${LanIp}:5173"
Write-Host "Backend health: http://${LanIp}:8000/api/v1/health"
Write-Host "ESP32 device API base URL: http://${LanIp}:8000/api/v1"
Write-Host "Login: root / root"
Write-Host "Role: RD test user"
Write-Host ""
Write-Host "To send virtual GPS/NFC data later, run:" -ForegroundColor Yellow
Write-Host "cd $SimulatorDir"
Write-Host "python simulate_device.py --base-url http://127.0.0.1:8000/api/v1 --device-id device_001 --device-token demo-device-token --admin-username root --admin-password root flow --gps-count 2 --interval 1"
