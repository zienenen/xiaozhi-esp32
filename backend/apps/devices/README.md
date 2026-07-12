# devices

Owns device identity and device-facing configuration.

Phase 1 scope:
- `device_id`
- `sn`
- masked `device_token_ref`
- online status
- last heartbeat
- latest GPS/location quality summary
- current bound agent reference

Do not expose plaintext device tokens in list or detail responses.
