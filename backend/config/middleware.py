import logging


logger = logging.getLogger("backend.api")


class ApiAuditMiddleware:
    """Log operational metadata without reading credential headers or request bodies."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith("/api/"):
            device_id = request.headers.get("X-Device-Id", "-")
            logger.info("api_call path=%s method=%s device_id=%s status=%s", request.path, request.method, device_id, response.status_code)
        return response
