import json

import pytest

from config import settings
from exceptions import ExtractionValidationError
from extraction.providers import ClaudeProvider, OpenAIProvider
from extraction.schemas import ExtractedInvoice


def test_parse_extraction_response_raises_validation_error_on_invalid_json():
    # Arrange
    incomplete_json = (
        '{"invoice_date": "2026-01-15", "currency": "USD", "total_amount": 500, '
        '"line_items": []}'
    )
    provider = ClaudeProvider(api_key=settings.anthropic_api_key)

    # Act & Assert
    with pytest.raises(ExtractionValidationError):
        provider.parse_extraction_response(incomplete_json)


@pytest.mark.asyncio
async def test_claude_invoice_returns_correctly():
    # Arrange
    provider = ClaudeProvider(api_key=settings.anthropic_api_key)

    # Act
    with open("tests/fixtures/extraction/invoice_01.pdf", "rb") as f:
        file_bytes = f.read()

    extracted_json = await provider.extract_invoice(file_bytes=file_bytes)

    with open("tests/fixtures/extraction/invoice_01_expected.json") as j:
        expected_data = json.load(j)

    expected_invoice = ExtractedInvoice(**expected_data)

    # Assert
    assert extracted_json == expected_invoice


@pytest.mark.asyncio
async def test_openai_invoice_returns_correctly():
    # Arrange
    provider = OpenAIProvider(api_key=settings.openai_api_key)

    # Act
    with open("tests/fixtures/extraction/invoice_01.pdf", "rb") as f:
        file_bytes = f.read()

    extracted_json = await provider.extract_invoice(file_bytes=file_bytes)

    with open("tests/fixtures/extraction/invoice_01_expected.json") as j:
        expected_data = json.load(j)

    expected_invoice = ExtractedInvoice(**expected_data)

    # Assert
    assert extracted_json == expected_invoice
