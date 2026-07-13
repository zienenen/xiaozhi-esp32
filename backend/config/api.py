import secrets
import uuid

from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import exception_handler


def request_id():
    return f"req_{uuid.uuid4().hex}"


def envelope(data=None, *, error=None, status=200):
    return Response({"success": error is None, "data": data if error is None else None, "error": error, "request_id": request_id()}, status=status)


def api_error(code, message, *, status=400, details=None):
    return envelope(error={"code": code, "message": message, "details": details or {}}, status=status)


def drf_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None
    code = getattr(exc, "default_code", "request_error")
    detail = response.data
    message = str(detail.get("detail", "请求处理失败")) if isinstance(detail, dict) else "请求处理失败"
    response.data = {"success": False, "data": None, "error": {"code": code, "message": message, "details": detail}, "request_id": request_id()}
    return response


class ToolTokenPermission(BasePermission):
    message = "Invalid tool credentials."

    def has_permission(self, request, view):
        expected = getattr(settings, "XIAOZHI_TOOL_TOKEN", "")
        supplied = request.headers.get("X-Tool-Token", "")
        return bool(expected and supplied and secrets.compare_digest(supplied, expected))
