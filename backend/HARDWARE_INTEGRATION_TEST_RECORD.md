# Real Hardware Integration Test Record

| Field | Value |
| --- | --- |
| Date | 2026-07-18 |
| Scope | BE-12 reset baseline, BE-13 LAN API and real ESP32 heartbeat, BE-14 real NFC replacement workflow |
| LAN endpoint | `http://192.168.101.119:8000/api/v1` (WLAN address for this test session) |
| Device | ESP32-S3 `192.168.101.10`, `device_001`, firmware `blindbox-2.2.6` |
| Database | Project-local PostgreSQL 17.10 on `127.0.0.1:5432` |

| Check | Trigger/evidence | Result | Acceptance classification |
| --- | --- | --- | --- |
| `reset_hw_test_data` repeatability | Executed twice against PostgreSQL; `device_001`, binding, active spot/tag retained; check-ins remained 0; runtime state remained `unknown` | Pass | Backend readiness only |
| LAN `device-config` | Authenticated manual request returned device, `agent_alo`, `spot_gate_001`, and active placeholder tag | HTTP 200 | API smoke only; device-side call pending |
| LAN `device-heartbeats` smoke | Manual request marked with firmware `manual-lan-smoke-not-esp32`; state reset afterward | Pass | API smoke only; not ESP32 evidence |
| Real ESP32 heartbeat | Serial showed `Got IP: 192.168.101.10`, `Heartbeat enabled: device=device_001 interval=30s`, then two `Heartbeat accepted: HTTP 200` lines; Django logged matching POST 200 responses at 18:54:54 and 18:55:25 | Pass | `hardware_verified`, limited to real device heartbeat |
| PostgreSQL heartbeat state | At 18:55:57 CST: `online_status=online`, `last_seen_at=2026-07-18T10:55:25.030958+00:00`, `firmware_version=blindbox-2.2.6`, `last_gps_status=not_connected` | Pass | Real ESP32 heartbeat persisted |
| Real PN532 UID | No physical PN532 UID supplied in this run | Not executed | QG-5 NFC remains incomplete |
| NFC replacement workflow | `set_hw_nfc_tag` automated tests cover normalization, idempotence, placeholder removal/disable, and invalid UID rejection | Pass | Workflow ready; hardware evidence pending |

## Blocker resolution

The 18:47 report that the backend was still `unknown` and waiting for an ESP32 heartbeat is stale. Django received real device POSTs every 30 seconds after 18:47, the firmware independently logged HTTP 200 acceptance, and PostgreSQL held `device_001=online`. No heartbeat simulator or manual heartbeat process was running during the fresh capture.

This resolves only the BE-13 real-heartbeat subtask. Device-side `/device-config`, real GPS/NFC events, frontend visual confirmation, MAX98357A/speaker, and battery acceptance remain pending; ACC-07 and QG-5 therefore remain partially complete.

## Network note

`192.168.168.155` was a deprecated address on a disconnected WLAN adapter. For this session, both devices joined `BusinessCentre-Guest`: ESP32 `192.168.101.10`, computer `192.168.101.119`. The local ignored `.env` contains the active WLAN address in `DJANGO_ALLOWED_HOSTS`. LAN IPs must be rechecked before every hardware session. Device credentials remain only in ignored local configuration and are not printed in logs.

## 2026-07-19 home-network re-verification

| Check | Evidence | Result |
| --- | --- | --- |
| Wi-Fi reprovisioning | ESP32 found and joined `CMCC-22NX`; received `192.168.1.10` | Pass |
| Host/API address | Computer WLAN `192.168.1.6`; ignored local `sdkconfig` and `.env` updated for this address | Pass |
| Firmware reliability fix | Heartbeat moved to a dedicated FreeRTOS task; ESP-IDF `esp_http_client` uses a 10-second timeout and retries on the next 30-second cycle | Pass |
| Flash | `xiaozhi.bin` size `0x28a0b0`; app partition 36% free; esptool reported `Hash of data verified` | Pass |
| Real heartbeat | Serial showed two cycles of `Sending heartbeat` followed by `Heartbeat accepted: HTTP 200` | Pass, `hardware_verified` |
| Persistence | With COM4 closed, PostgreSQL `last_seen_at` advanced from `2026-07-19T05:17:35.145252+00:00` to `2026-07-19T05:18:06.892342+00:00` in about 31 seconds; `device_001=online`, `firmware_version=blindbox-2.2.6`, `last_gps_status=not_connected` | Pass |

The database schema was not changed. The transient backend startup failure was caused by the project-local PostgreSQL process not running; after starting PostgreSQL, Django passed its system check and accepted the real device heartbeats.
