from http import HTTPStatus


class ValidationError(Exception):
    def __init__(self, errors=None, message="Bad Request"):
        self.status_code = HTTPStatus.BAD_REQUEST.value  # 400
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(Exception):
    def __init__(self, errors=None, message="Unauthorized error"):
        self.status_code = HTTPStatus.UNAUTHORIZED.value  # 401
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class PermissionError(Exception):
    def __init__(self, errors=None, message="Permission error"):
        self.status_code = HTTPStatus.FORBIDDEN.value  # 403
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    def __init__(self, errors=None, message="NotFound error"):
        self.status_code = HTTPStatus.NOT_FOUND.value  # 404
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    def __init__(self, errors=None, message="Conflict error"):
        self.status_code = HTTPStatus.CONFLICT.value  # 409
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class ServerError(Exception):
    def __init__(self, errors=None, message="Server error"):
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value  # 500
        self.errors = errors
        self.message = message
        super().__init__(self.message)
