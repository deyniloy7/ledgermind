from fastapi import UploadFile
from typing import Final
from exceptions import InvalidFileTypeError, FileTooLargeError, EmptyFileError

ALLOWED_TYPES: Final = ["application/pdf", "image/png", "image/jpeg"]
MAX_FILE_SIZE_MB: Final = 10
MAX_FILE_SIZE_BYTES: Final = MAX_FILE_SIZE_MB * 1024 * 1024


async def process_upload(file: UploadFile) -> bytes:
    contents = await file.read()
    if len(contents) == 0:
        raise EmptyFileError(filename=file.filename)
    if file.content_type not in ALLOWED_TYPES:
        raise InvalidFileTypeError(filename=file.filename, allowed_types=ALLOWED_TYPES)
    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise FileTooLargeError(
            filename=file.filename,
            file_size_mb=(len(contents) / (1024 * 1024)),
            limit_mb=MAX_FILE_SIZE_MB,
        )
    return contents
