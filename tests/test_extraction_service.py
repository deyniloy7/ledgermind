import pytest
from extraction.providers import ClaudeProvider, OpenAIProvider
from extraction.service import get_provider
from exceptions import InvalidProviderError


def test_invalid_provider_name_raises_invalid_provider_error():
    # Arrange
    provider_name = "gemini"
    api_key = "api_key"

    # Act & Assert
    with pytest.raises(InvalidProviderError):
        get_provider(provider_name, api_key=api_key)


def test_provider_name_claude_gives_us_Claude_Provider():
    # Arrange
    provider_name = "claude"
    api_key = "api_key"

    # Act
    result = get_provider(provider_name, api_key=api_key)

    # Assert
    assert isinstance(result, ClaudeProvider)


def test_provider_name_open_ai_gives_us_OpenAi_Provider():
    # Arrange
    provider_name = "open_ai"
    api_key = "api_key"

    # Act
    result = get_provider(provider_name, api_key=api_key)

    # Assert
    assert isinstance(result, OpenAIProvider)
