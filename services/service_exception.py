from fastapi import HTTPException, status

class ServiceException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str = "GENERIC_ERROR"):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

class NotFoundException(ServiceException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail, error_code="NOT_FOUND")

class InvalidInputException(ServiceException):
    def __init__(self, detail: str = "Invalid input provided"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail, error_code="INVALID_INPUT")
