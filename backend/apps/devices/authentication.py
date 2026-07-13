from config.api import api_error
from .models import Device


def authenticate_device(request, body_device_id=None):
    device_id = request.headers.get("X-Device-Id") or request.query_params.get("device_id") or body_device_id
    token = request.headers.get("X-Device-Token", "")
    try:
        device = Device.objects.get(pk=device_id)
    except Device.DoesNotExist:
        return None, api_error("device_not_found", "设备不存在", status=404)
    if request.headers.get("X-Device-Id") != device_id or not token or not device.check_token(token):
        return None, api_error("invalid_device_token", "设备鉴权失败", status=401)
    return device, None
