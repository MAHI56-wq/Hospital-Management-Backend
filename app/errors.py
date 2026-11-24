from flask import jsonify
class AppError(Exception):
    def __init__(self, status, title, detail, code, errors=None):
        super().__init__(detail)
        self.status, self.title, self.detail, self.code = status, title, detail, code
        self.errors = errors or {}
class ValidationFailed(AppError):
    def __init__(self, errors):
        super().__init__(422, "Validation failed", "One or more fields are invalid", "validation_failed", errors)
class NotFound(AppError):
    def __init__(self, detail="Resource not found"):
        super().__init__(404, "Resource not found", detail, "not_found")
class Conflict(AppError):
    def __init__(self, detail):
        super().__init__(409, "Request conflicts with current state", detail, "conflict")
def problem_response(error, request_id=None):
    body = {"type": f"/problems/{error.code}", "title": error.title, "status": error.status,
            "detail": error.detail, "code": error.code, "requestId": request_id}
    if error.errors: body["errors"] = error.errors
    response = jsonify(body); response.status_code = error.status
    response.content_type = "application/problem+json"
    return response
