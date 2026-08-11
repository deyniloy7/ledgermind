import pytest
from unittest.mock import AsyncMock, MagicMock
from ingestion.service import process_upload
from exceptions import EmptyFileError, FileTooLargeError, InvalidFileTypeError


@pytest.mark.asyncio
async def test_upload_empty_file_raises_empty_file_error():
    # Arrange
    mock_file = MagicMock()
    mock_file.filename = "empty.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.read = AsyncMock(return_value=b"")

    # Act & Assert
    with pytest.raises(EmptyFileError):
        await process_upload(mock_file)


@pytest.mark.asyncio
async def test_upload_invalid_file_raises_invalid_file_type_error():
    # Arrange
    mock_file = MagicMock()
    mock_file.filename = "invalid.jar"
    mock_file.content_type = "application/jar"
    mock_file.read = AsyncMock(return_value=b"some content")

    # Act & Assert
    with pytest.raises(InvalidFileTypeError):
        await process_upload(mock_file)


@pytest.mark.asyncio
async def test_upload_large_file_raises_file_too_large_error():
    # Arrange
    mock_file = MagicMock()
    mock_file.filename = "empty.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.read = AsyncMock(return_value=b"x" * (11 * 1024 * 1024))

    # Act & Assert
    with pytest.raises(FileTooLargeError):
        await process_upload(mock_file)


@pytest.mark.asyncio
async def test_upload_returns_correct_bytes_when_given_a_valid_pdf():
    # Arrange
    mock_file = MagicMock()
    mock_file.filename = "valid.pdf"
    mock_file.content_type = "application/pdf"
    mock_file.read = AsyncMock(return_value=b"valid pdf content")

    # Act
    result = await process_upload(mock_file)

    # Assert
    assert result == b"valid pdf content"
