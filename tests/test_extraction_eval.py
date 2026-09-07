import pytest

from exceptions import ExtractionValidationError
from extraction.providers import ClaudeProvider


def test_parse_extraction_response_raises_validation_error_on_invalid_json():
    # Arrange
    incomplete_json = (
        '{"invoice_date": "2026-01-15", "currency": "USD", "total_amount": 500, '
        '"line_items": []}'
    )
    provider = ClaudeProvider(api_key="api_key")

    # Act & Assert
    with pytest.raises(ExtractionValidationError):
        provider.parse_extraction_response(incomplete_json)
