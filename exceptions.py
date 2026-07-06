from datetime import datetime, timezone

class LedgerMindException(Exception):
    def __init__(self, message: str, error_code: str, status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.timestamp = datetime.now(timezone.utc).isoformat()
        super().__init__(message)
    
    def to_dict(self) -> dict:
        return {
            "error": self.error_code,
            "message": self.message,
            "timestamp": self.timestamp
        }
    
class InvalidFileTypeError(LedgerMindException):
    def __init__(self, filename: str, allowed_types: list[str]):
        super().__init__(
            message=f"File '{filename}' is not allowed. Accepted types: {','.join(allowed_types)}",
            error_code="INVALID_FILE_TYPE",
            status_code=415
        )

class FileTooLargeError(LedgerMindException):
    def __init__(self, filename: str, file_size_mb: float, limit_mb: int):
        super().__init__(
            message=f"File '{filename}' size {file_size_mb:.1f}MB exceeds limit of {limit_mb}MB",
            error_code="FILE_TOO_LARGE",
            status_code=413
        )

class EmptyFileError(LedgerMindException):
    def __init__(self, filename: str):
        super().__init__(
            message=f"File '{filename}' is empty",
            error_code="EMPTY_FILE",
            status_code=400
        )