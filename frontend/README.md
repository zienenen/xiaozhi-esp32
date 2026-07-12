# Frontend Module

Status: scaffold

This module is the responsive Web frontend for PC, tablet, and mobile. It is
not three independent apps. It provides the management and demo UI described by
the confirmed product interaction spec.

## Stack

- React
- Vite
- TypeScript
- Ant Design
- React Router

## Page Modules

| Route | Page | Product Priority |
| --- | --- | --- |
| `/login` | Demo login | P0 |
| `/` | Demo overview | P0 |
| `/devices` | Device list | P0 |
| `/devices/:id` | Device detail | P0 |
| `/agents` | Agent list and edit entry | P0 |
| `/bindings` | Device-agent binding | P0 |
| `/spots` | Scenic spot list/edit entry | P0 |
| `/nfc-tags` | NFC tag list/detail entry | P0 |
| `/checkins` | Check-in records | P0 |
| `/datasets` | Scenic dataset status | P0 |
| `/simulate-checkin` | Manual simulated check-in | P0 |

## Development

```powershell
cd frontend
npm install
npm run dev
```

The backend API base URL is configured by `VITE_API_BASE_URL`.
