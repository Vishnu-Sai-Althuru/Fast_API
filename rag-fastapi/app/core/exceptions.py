from fastapi import status


class AppError(Exception):
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


class InputValidationError(AppError):
    def __init__(self, detail: str = "Invalid input provided."):
        super().__init__(detail, status.HTTP_400_BAD_REQUEST)


class ServiceUnavailableError(AppError):
    def __init__(self, detail: str = "Service is unavailable right now."):
        super().__init__(detail, status.HTTP_503_SERVICE_UNAVAILABLE)


class QueryProcessingError(AppError):
    def __init__(self, detail: str = "Unable to process the request right now."):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR)
