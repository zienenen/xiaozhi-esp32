# Device Simulator

Status: scaffold

Use this module before the ESP32/GPS/NFC hardware arrives. It simulates the
device-facing API calls defined in `docs/blindbox_project/web_api_contract.md`.

## Simulated Flow

1. Pull device config.
2. Send heartbeat.
3. Send GPS nearby event.
4. Send NFC-confirmed check-in.
5. Read returned `speak_text` and `next_action`.

## Usage

```powershell
cd tools\device_simulator
python simulate_device.py --base-url http://127.0.0.1:8000/api/v1 --device-id device_001 --device-token demo-device-token
```
