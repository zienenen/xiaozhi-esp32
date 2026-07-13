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

## Handoff Issues

| ID | Issue | Current evidence | Required action | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| BE-HO-01 | The local PostgreSQL acceptance environment is unavailable. No PostgreSQL service/runtime, Docker, or Podman was found, and `127.0.0.1:5432` is unreachable. | `python manage.py check` passes; 13 backend tests pass; migrations have no model drift; real PostgreSQL `python manage.py migrate` cannot connect. | Provide reachable PostgreSQL connection values in `.env`, run `python manage.py migrate`, run `python manage.py seed_demo`, and record the results. | 研发主管 | 待处理 |
