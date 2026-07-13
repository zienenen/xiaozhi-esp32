"""Blind-box device integration simulator (standard-library only)."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


class SimulatorError(RuntimeError):
    """An HTTP, transport, or API-contract failure."""


@dataclass
class Settings:
    base_url: str
    device_id: str
    device_token: str
    admin_username: str
    admin_password: str
    spot_id: str
    tag_id: str
    latitude: float
    longitude: float
    timeout: float

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Device-Id": self.device_id,
            "X-Device-Token": self.device_token,
            "User-Agent": "mysterybox-device-simulator/1.0",
        }

    @property
    def admin_headers(self) -> dict[str, str]:
        if not self.admin_username or not self.admin_password:
            raise SimulatorError("NFC simulation requires --admin-username and --admin-password")
        credentials = base64.b64encode(f"{self.admin_username}:{self.admin_password}".encode("utf-8")).decode("ascii")
        return {"Content-Type": "application/json", "Authorization": f"Basic {credentials}", "User-Agent": "mysterybox-device-simulator/1.0"}


def event_time() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def request_json(settings: Settings, method: str, path: str, payload: dict[str, Any] | None = None, *, headers: dict[str, str] | None = None) -> dict[str, Any]:
    url = f"{settings.base_url.rstrip('/')}/{path.lstrip('/')}"
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers or settings.headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=settings.timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(raw)
        except json.JSONDecodeError:
            detail = raw
        raise SimulatorError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SimulatorError(f"backend unavailable: {exc.reason}") from exc
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SimulatorError("backend returned non-JSON content") from exc
    if not isinstance(result, dict):
        raise SimulatorError("backend response must be a JSON object")
    if result.get("success") is False:
        error = result.get("error") or {}
        code = error.get("code", "api_error") if isinstance(error, dict) else "api_error"
        message = error.get("message", "request rejected") if isinstance(error, dict) else str(error)
        raise SimulatorError(f"{code}: {message}")
    return result


def pull_config(settings: Settings) -> dict[str, Any]:
    query = urllib.parse.urlencode({"device_id": settings.device_id})
    return request_json(settings, "GET", f"device-config?{query}")


def heartbeat(settings: Settings) -> dict[str, Any]:
    return request_json(settings, "POST", "device-heartbeats", {
        "device_id": settings.device_id, "firmware_version": "simulator-1.0.0",
        "battery_percent": 82, "gps_status": "fixed", "event_time": event_time(),
    })


def location(settings: Settings, *, event_type: str = "near_spot") -> dict[str, Any]:
    return request_json(settings, "POST", "location-events", {
        "device_id": settings.device_id, "spot_id": settings.spot_id,
        "event_type": event_type, "latitude": settings.latitude, "longitude": settings.longitude,
        "distance_meters": 36 if event_type == "near_spot" else 120,
        "location_quality": {"fix": True, "satellites": 8, "hdop": 1.2},
        "event_time": event_time(),
    })


def checkin(settings: Settings, tag_id: str | None = None) -> dict[str, Any]:
    return request_json(settings, "POST", "demo/simulate-checkin", {
        "device_id": settings.device_id, "spot_id": settings.spot_id,
        "tag_id": tag_id or settings.tag_id, "simulate_gps_nearby": True,
        "reason": "device simulator integration test",
    }, headers=settings.admin_headers)


def emit(name: str, action) -> dict[str, Any]:
    print(f"\n== {name} ==")
    result = action()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


def run(args: argparse.Namespace, settings: Settings) -> None:
    if args.command in ("config", "flow"):
        emit("pull config", lambda: pull_config(settings))
    if args.command in ("heartbeat", "flow"):
        emit("heartbeat", lambda: heartbeat(settings))
    if args.command == "gps":
        count = args.count
        for index in range(count):
            emit(f"GPS report {index + 1}/{count}", lambda: location(settings, event_type=args.event_type))
            if index + 1 < count:
                time.sleep(args.interval)
    if args.command == "flow":
        for index in range(args.gps_count):
            emit(f"GPS report {index + 1}/{args.gps_count}", lambda: location(settings, event_type="location_update"))
            if index + 1 < args.gps_count:
                time.sleep(args.interval)
        emit("GPS nearby", lambda: location(settings, event_type="near_spot"))
        emit("NFC success", lambda: checkin(settings))
    if args.command == "checkin":
        default_tags = {"unknown": "UNKNOWN_TAG", "disabled": "DISABLED_TAG"}
        tag = args.case_tag_id or default_tags.get(args.case, settings.tag_id)
        emit(f"NFC {args.case}", lambda: checkin(settings, tag))
        if args.case == "duplicate":
            emit("NFC duplicate (second request)", lambda: checkin(settings, tag))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Mystery-box device integration simulator")
    p.add_argument("--base-url", default=os.getenv("SIM_BASE_URL", "http://127.0.0.1:8000/api/v1"))
    p.add_argument("--device-id", default=os.getenv("SIM_DEVICE_ID", "device_001"))
    p.add_argument("--device-token", default=os.getenv("SIM_DEVICE_TOKEN", "demo-device-token"))
    p.add_argument("--admin-username", default=os.getenv("SIM_ADMIN_USERNAME", ""))
    p.add_argument("--admin-password", default=os.getenv("SIM_ADMIN_PASSWORD", ""))
    p.add_argument("--spot-id", default=os.getenv("SIM_SPOT_ID", "spot_gate_001"))
    p.add_argument("--tag-id", default=os.getenv("SIM_TAG_ID", "04AABBCCDD"))
    p.add_argument("--latitude", type=float, default=float(os.getenv("SIM_LATITUDE", "31.2304")))
    p.add_argument("--longitude", type=float, default=float(os.getenv("SIM_LONGITUDE", "121.4737")))
    p.add_argument("--timeout", type=float, default=float(os.getenv("SIM_TIMEOUT", "10")))
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("config", help="pull device configuration")
    sub.add_parser("heartbeat", help="send one heartbeat")
    gps = sub.add_parser("gps", help="send periodic GPS/location events")
    gps.add_argument("--count", type=int, default=1)
    gps.add_argument("--interval", type=float, default=10.0)
    gps.add_argument("--event-type", choices=("location_update", "near_spot"), default="near_spot")
    nfc = sub.add_parser("checkin", help="send an NFC check-in (repeat to verify duplicate)")
    nfc.add_argument("--case", choices=("success", "unknown", "disabled", "duplicate"), default="success")
    nfc.add_argument("--tag-id", dest="case_tag_id", help="tag for the selected case; backend fixture determines its status")
    flow = sub.add_parser("flow", help="run config -> heartbeat -> GPS -> nearby -> NFC")
    flow.add_argument("--gps-count", type=int, default=1)
    flow.add_argument("--interval", type=float, default=10.0)
    return p


def main() -> int:
    args = parser().parse_args()
    if getattr(args, "count", 1) < 1 or getattr(args, "gps_count", 1) < 1:
        print("ERROR: count must be at least 1", file=sys.stderr)
        return 2
    settings = Settings(args.base_url, args.device_id, args.device_token, args.admin_username, args.admin_password, args.spot_id, args.tag_id,
                        args.latitude, args.longitude, args.timeout)
    try:
        run(args, settings)
    except (SimulatorError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
