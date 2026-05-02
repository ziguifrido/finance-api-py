from fastapi import status

from services.service_exception import (
    InvalidInputException,
    NotFoundException,
    ServiceException,
)


class TestServiceException:
    def test_service_exception_default_values(self):
        exc = ServiceException(status_code=500, detail="Server error")
        assert exc.status_code == 500
        assert exc.detail == "Server error"
        assert exc.error_code == "GENERIC_ERROR"

    def test_service_exception_custom_error_code(self):
        exc = ServiceException(
            status_code=400, detail="Bad request", error_code="CUSTOM_ERROR"
        )
        assert exc.status_code == 400
        assert exc.detail == "Bad request"
        assert exc.error_code == "CUSTOM_ERROR"

    def test_service_exception_is_http_exception(self):
        exc = ServiceException(status_code=500, detail="Error")
        assert hasattr(exc, "status_code")
        assert hasattr(exc, "detail")


class TestNotFoundException:
    def test_not_found_exception_default_values(self):
        exc = NotFoundException()
        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert exc.detail == "Resource not found"
        assert exc.error_code == "NOT_FOUND"

    def test_not_found_exception_custom_detail(self):
        exc = NotFoundException(detail="Ticker XYZ not found")
        assert exc.status_code == status.HTTP_404_NOT_FOUND
        assert exc.detail == "Ticker XYZ not found"
        assert exc.error_code == "NOT_FOUND"


class TestInvalidInputException:
    def test_invalid_input_exception_default_values(self):
        exc = InvalidInputException()
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Invalid input provided"
        assert exc.error_code == "INVALID_INPUT"

    def test_invalid_input_exception_custom_detail(self):
        exc = InvalidInputException(detail="Invalid symbol format")
        assert exc.status_code == status.HTTP_400_BAD_REQUEST
        assert exc.detail == "Invalid symbol format"
        assert exc.error_code == "INVALID_INPUT"
