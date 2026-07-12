# Project Structure

This repository keeps the original xiaozhi ESP32 firmware and adds phase 1
business software modules in the same repository.

```text
xiaozhi-esp32-main/
  main/                  Original xiaozhi ESP32 firmware
  backend/               Django/DRF business backend
  frontend/              React responsive management/demo frontend
  tools/device_simulator Hardware-free API simulator
  deploy/                Phase 1 deployment references
  docs/blindbox_project/ Confirmed product and architecture documents
```

## Integration Rule

- Do not put Django/React code under `main/`.
- Do not put firmware code under `backend/` or `frontend/`.
- The firmware is a device client of the backend.
- `xiaozhi.me` is a phase 1 voice/tool entry dependency, not the business data source.
- The xiaozhi-side MCP/tool entry should call our backend for agent context and
  scenic knowledge.

## Current Scaffold Status

| Module | Status | Next Owner |
| --- | --- | --- |
| `backend/` | Framework scaffold ready | Full-stack engineer |
| `frontend/` | Framework scaffold ready | Full-stack engineer |
| `tools/device_simulator/` | Simulator scaffold ready | Full-stack engineer |
| `deploy/` | Simple local/server deployment notes ready; Docker Compose deferred | Full-stack/DevOps |
| `main/` | Original firmware retained | Firmware/full-stack engineer |

## Local Dependency Status

| Module | Local state |
| --- | --- |
| `backend/` | `.venv` created and `requirements.txt` installed |
| `frontend/` | `node_modules` created and `package.json` installed |

Validation already run:

```powershell
cd backend
.\.venv\Scripts\python manage.py check

cd ..\frontend
npm run build
```

Results:

- Django system check passed.
- React/Vite production build passed.
- `npm install` reported 1 moderate and 1 high audit issue. Do not run
  `npm audit fix --force` blindly; let the full-stack engineer assess package
  upgrades during implementation.
