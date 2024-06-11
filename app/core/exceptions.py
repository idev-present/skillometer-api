from starlette import status


class ValidationError(Exception):
    def __init__(self, errors=None, message="Bad Request"):
        self.status_code = status.HTTP_400_BAD_REQUEST  # 400
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(Exception):
    def __init__(self, errors=None, message="Unauthorized error"):
        self.status_code = status.HTTP_401_UNAUTHORIZED  # 401
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class PermissionError(Exception):
    def __init__(self, errors=None, message="Permission error"):
        self.status_code = status.HTTP_403_FORBIDDEN  # 403
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    def __init__(self, errors=None, message="NotFound error"):
        self.status_code = status.HTTP_404_NOT_FOUND  # 404
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class ConflictError(Exception):
    def __init__(self, errors=None, message="Conflict error"):
        self.status_code = status.HTTP_409_CONFLICT  # 409
        self.errors = errors
        self.message = message
        super().__init__(self.message)


class ServerError(Exception):
    def __init__(self, errors=None, message="Server error"):
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR  # 500
        self.errors = errors
        self.message = message
        super().__init__(self.message)
