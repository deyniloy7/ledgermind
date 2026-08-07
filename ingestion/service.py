from fastapi import UploadFile
from typing import Final
from exceptions import InvalidFileTypeError, FileTooLargeError, EmptyFileError
from observability.logging import get_logger
from observability.middleware import request_id_var

logger = get_logger(__name__)

ALLOWED_TYPES: Final = ["application/pdf", "image/png", "image/jpeg"]
MAX_FILE_SIZE_MB: Final = 10
MAX_FILE_SIZE_BYTES: Final = MAX_FILE_SIZE_MB * 1024 * 1024


async def process_upload(file: UploadFile) -> bytes:
    request_id = request_id_var.get()
    logger.info(
        "file_received",
        request_id=request_id,
        filename=file.filename,
        content_type=file.content_type,
    )
    contents = await file.read()
    if len(contents) == 0:
        logger.warning(
            "empty_file_rejected", request_id=request_id, filename=file.filename
        )
        raise EmptyFileError(filename=file.filename)

    if file.content_type not in ALLOWED_TYPES:
        logger.warning(
            "invalid_file_rejected",
            request_id=request_id,
            filename=file.filename,
            content_type=file.content_type,
        )
        raise InvalidFileTypeError(filename=file.filename, allowed_types=ALLOWED_TYPES)

    if len(contents) > MAX_FILE_SIZE_BYTES:
        logger.warning(
            "file_too_large",
            request_id=request_id,
            filename=file.filename,
            size_bytes=len(contents),
        )
        raise FileTooLargeError(
            filename=file.filename,
            file_size_mb=(len(contents) / (1024 * 1024)),
            limit_mb=MAX_FILE_SIZE_MB,
        )

    logger.info(
        "file_processed",
        request_id=request_id,
        filename=file.filename,
        content_type=file.content_type,
        size_bytes=len(contents),
    )
    return contents
