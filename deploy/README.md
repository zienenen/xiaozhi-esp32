# Deploy Module

Status: simple local demo scaffold

Phase 1 starts with a simple local/server demo. Do not require Docker Compose
for the first implementation pass.

```text
Nginx
React static files
Gunicorn
Django/DRF
PostgreSQL
```

## Responsibilities

| File | Purpose |
| --- | --- |
| `.env.example` | Shared deployment variables for local/server setup |
| `nginx.example.conf` | Optional reverse proxy sketch |
| `gunicorn.example.conf.py` | Optional backend process sketch |

Docker Compose is deferred to the next step unless the full-stack engineer needs
it for local PostgreSQL convenience.
