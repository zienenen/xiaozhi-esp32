# Phase 1 Backend

Django/DRF and PostgreSQL backend for device configuration, scenic agents, GPS/NFC check-ins, datasets, demo management, and xiaozhi tool calls.

## Setup

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py check
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 0.0.0.0:8000
```

Set every placeholder in `.env` before migration or seeding. `seed_demo` requires `DEMO_DEVICE_TOKEN`, `DEMO_ADMIN_USERNAME`, and `DEMO_ADMIN_PASSWORD`; it is idempotent and creates one device, two agents, one active spot and NFC tag, one dataset with a summary chunk, and a staff demo account.

## Authentication

- Management APIs use Django session or Basic authentication.
- Device APIs require matching `X-Device-Id` and `X-Device-Token` headers. Only a SHA-256 token digest and masked reference are stored.
- `/agents/{agent_id}/context` and `/knowledge/search` require `X-Tool-Token`.
- Manual simulation requires an authenticated staff user or membership in `factory_admin`/`tester`.

## API

All routes use `/api/v1` and return `success`, `data`, `error`, and `request_id`.

| Area | Routes |
| --- | --- |
| Device | `device-config`, `device-heartbeats`, `location-events` |
| Check-in | `checkins`, `checkins/{checkin_id}` |
| Management | `devices`, `agents`, `bindings`, `binding-events`, `spots`, `nfc-tags`, `datasets` |
| Dataset | `datasets/{dataset_id}/chunks`, `knowledge/search` |
| Demo | `demo/overview`, `demo/simulate-checkin` |
| Tool | `agents/{agent_id}/context` |

GPS reports replace the latest location summary on `Device`; there is no continuous track table. A successful check-in snapshots the most recent coordinates and quality. NFC check-ins use a five-minute device/spot cooldown and return `duplicate` without creating another record. Simulated events are stored with `source=simulation` and `result=simulated`.

## Verification

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test apps.demo --settings=config.test_settings
```

`config.test_settings` uses an in-memory database only for isolated automated tests. Development, demo, and public environments use PostgreSQL exclusively.

## Real Hardware Baseline

`seed_demo` creates simulator/demo configuration and the placeholder NFC tag `04AABBCCDD`. It does not create hardware acceptance evidence. Before each real ESP32 run, reset event and runtime state while preserving `device_001`, its token hash, binding, agents, spots, NFC configuration, and datasets:

```powershell
python manage.py reset_hw_test_data
```

The command is transactional and repeatable. It clears all previous check-ins and resets every device heartbeat/GPS runtime field. After it runs, `device_001` remains configured with `online_status=unknown`; only a subsequent real ESP32 heartbeat may count as hardware acceptance evidence.

### LAN Device Smoke

Find the computer's current LAN IP and add it to `DJANGO_ALLOWED_HOSTS` in `.env`. Start Django on all interfaces:

```powershell
ipconfig
python manage.py runserver 0.0.0.0:8000
```

Use the computer LAN address from the ESP32, for example `http://192.168.x.x:8000/api/v1`. Never configure the ESP32 with `127.0.0.1`, because that address points back to the ESP32 itself.

```powershell
curl.exe -H "X-Device-Id: device_001" -H "X-Device-Token: demo-device-token" "http://192.168.x.x:8000/api/v1/device-config?device_id=device_001"

curl.exe -X POST "http://192.168.x.x:8000/api/v1/device-heartbeats" -H "Content-Type: application/json" -H "X-Device-Id: device_001" -H "X-Device-Token: demo-device-token" -d "{\"device_id\":\"device_001\",\"firmware_version\":\"esp32-hw-test\",\"battery_percent\":100}"
```

A curl/Postman request is only an API smoke test. Run `reset_hw_test_data` again after manual testing so the dashboard returns to `unknown`; do not mark ACC-07 complete without real ESP32/serial evidence.

### Replace The NFC Placeholder

After PN532 serial output shows the physical tag UID, replace the placeholder with the real 4, 7, or 10-byte hexadecimal UID:

```powershell
python manage.py reset_hw_test_data
python manage.py set_hw_nfc_tag "04:11:22:33"
```

The command normalizes separators/case, activates the real tag on `spot_gate_001`, and removes the placeholder when possible. If historical records protect the placeholder, it disables it instead, so `device-config` exposes only the real active UID. The command can be run repeatedly with the same UID. Verify the resulting `tag_id` in Django Admin or the NFC management page before sending a real `/checkins` event.

## Local PostgreSQL Acceptance Runtime

For the current Windows acceptance machine, PostgreSQL 17.10 is installed as a project-local binary runtime under ignored `tmp/` paths, without a Windows service or administrator installation.

```powershell
cd D:\mysterybox\xiaozhi-esp32-main
tmp\pgextract\pgsql\bin\pg_ctl.exe -D tmp\pgdata -l tmp\pg.log start
tmp\pgextract\pgsql\bin\pg_isready.exe -h 127.0.0.1 -p 5432 -U postgres

cd backend
.\.venv\Scripts\python.exe manage.py migrate --noinput
.\.venv\Scripts\python.exe manage.py seed_demo
.\.venv\Scripts\python.exe manage.py migrate --check --noinput
```

Local acceptance connection values are kept in ignored `backend/.env`: database `blindbox`, user `blindbox`, host `127.0.0.1`, port `5432`. Do not commit local `.env`, `tmp/pgdata`, or PostgreSQL binaries.

## Handoff Issues

| ID | Issue | Current evidence | Required action | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| BE-HO-01 | Local PostgreSQL acceptance environment was missing. | Resolved on 2026-07-13: PostgreSQL 17.10 project-local runtime started on `127.0.0.1:5432`; `python manage.py migrate --noinput` passed; `python manage.py seed_demo` passed; `python manage.py migrate --check --noinput` passed; `python manage.py check` passed; 15 backend tests passed; simulator 3 tests passed. | No further action for local software acceptance. Keep public/demo PostgreSQL provisioning as a deployment task. | 研发主管 | 已处理 |
