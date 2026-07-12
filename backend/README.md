# Backend Module

Status: scaffold

This module is the self-owned business backend for phase 1. It does not replace
`xiaozhi.me` voice services. It stores business configuration and exposes APIs
that the device, frontend, simulator, and xiaozhi-side tool/MCP entry can call.

## Stack

- Django
- Django REST Framework
- PostgreSQL
- Simple demo account for phase 1
- `device_id + device_token` static token for phase 1 device access

## Django Apps

| App | Responsibility |
| --- | --- |
| `devices` | Device identity, token reference, online state, heartbeat, latest location summary |
| `agents` | Agent profile, personality prompt, voice reference, context generation |
| `spots` | Scenic spot, GPS radius, check-in message, dataset reference |
| `nfc_tags` | NFC tag registry, spot binding, tag status |
| `checkins` | Device check-in event, idempotency, duplicate handling, simulation marker |
| `datasets` | Real scenic dataset status, summary chunks, knowledge search endpoint |
| `demo` | Demo overview and manual simulation endpoints |

## Confirmed Phase 1 APIs

| Area | Endpoint |
| --- | --- |
| Device config | `GET /api/v1/device-config` |
| Heartbeat | `POST /api/v1/device-heartbeats` |
| Location event | `POST /api/v1/location-events` |
| Check-in | `POST /api/v1/checkins` |
| Agent context | `GET /api/v1/agents/{agent_id}/context` |
| Knowledge search | `POST /api/v1/knowledge/search` |
| Demo overview | `GET /api/v1/demo/overview` |
| Simulate check-in | `POST /api/v1/demo/simulate-checkin` |

## Development

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## Notes For Full-Stack Engineers

- Keep real-time audio out of Django.
- Keep continuous GPS tracks out of the database. Store only check-in event data
  and throttled location quality/latest summaries.
- Do not store device token plaintext in list/detail responses.
- The xiaozhi-side tool/MCP entry should call this backend for context and
  knowledge instead of storing scenic knowledge in the xiaozhi console.
