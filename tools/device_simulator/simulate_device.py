import argparse
import datetime as dt
import json
import urllib.request


def request_json(method: str, url: str, payload: dict | None, headers: dict) -> dict:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/api/v1")
    parser.add_argument("--device-id", default="device_001")
    parser.add_argument("--device-token", default="demo-device-token")
    args = parser.parse_args()

    headers = {
        "Content-Type": "application/json",
        "X-Device-Id": args.device_id,
        "X-Device-Token": args.device_token,
    }
    now = dt.datetime.now(dt.timezone.utc).isoformat()

    steps = [
        ("GET", f"{args.base_url}/device-config?device_id={args.device_id}", None),
        (
            "POST",
            f"{args.base_url}/device-heartbeats",
            {
                "device_id": args.device_id,
                "firmware_version": "simulator-0.1.0",
                "battery_percent": 82,
                "gps_status": "fixed",
                "event_time": now,
            },
        ),
        (
            "POST",
            f"{args.base_url}/location-events",
            {
                "device_id": args.device_id,
                "spot_id": "spot_gate_001",
                "event_type": "near_spot",
                "latitude": 31.2304,
                "longitude": 121.4737,
                "distance_meters": 36,
                "location_quality": {"fix": True, "satellites": 8, "hdop": 1.2},
                "event_time": now,
            },
        ),
        (
            "POST",
            f"{args.base_url}/checkins",
            {
                "device_id": args.device_id,
                "spot_id": "spot_gate_001",
                "tag_id": "04AABBCCDD",
                "method": "gps_nearby_nfc_confirmed",
                "source": "device",
                "event_time": now,
                "location_quality": {"fix": True, "satellites": 8, "hdop": 1.2},
            },
        ),
    ]

    for method, url, payload in steps:
        print(f"\n{method} {url}")
        try:
            print(json.dumps(request_json(method, url, payload, headers), ensure_ascii=False, indent=2))
        except Exception as exc:
            print(f"REQUEST_FAILED: {exc}")


if __name__ == "__main__":
    main()
