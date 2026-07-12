# checkins

Owns GPS nearby events and NFC-confirmed check-in records.

Phase 1 scope:
- Save check-in event and location quality summary
- Do not save continuous GPS tracks
- Throttle/aggregate location events around 10 seconds
- Keep `source=device` and `source=simulation` clearly separated
- Return `speak_text` and `next_action` for device-side narration
