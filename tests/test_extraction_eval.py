import json
import os
from unittest.mock import patch

import anthropic
import httpx2
import pytest

from config import settings
from exceptions import ExtractionValidationError, ProviderUnavailableError
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
async def test_extract_invoice_raises_provider_unavailable_on_api_error():
    # Arrange
    provider = ClaudeProvider(api_key=settings.anthropic_api_key)
    fake_request = httpx2.Request(
        method="POST", url="https://api.anthropic.com/v1/messages"
    )
    fake_error = anthropic.APIError(
        message="Rate limit exceeded", request=fake_request, body=None
    )

    # Act & Assert
    with patch.object(provider.client.messages, "create", side_effect=fake_error):
        with pytest.raises(ProviderUnavailableError):
            await provider.extract_invoice(file_bytes=b"fake pdf content")


@pytest.mark.skipif(
    os.getenv("RUN_REAL_API_EVAL_TESTS") != "true",
    reason=(
        "Real-API eval tests disabled by default — individual account, "
        "cost-conscious standing decision"
    ),
)
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


@pytest.mark.skipif(
    os.getenv("RUN_REAL_API_EVAL_TESTS") != "true",
    reason=(
        "Real-API eval tests disabled by default — individual account, "
        "cost-conscious standing decision"
    ),
)
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
