from typing import Final

from exceptions import InvalidProviderError
from extraction.providers import ClaudeProvider, LLMProvider, OpenAIProvider
from observability.logging import get_logger
from observability.middleware import request_id_var

logger = get_logger(__name__)

ALLOWED_PROVIDER_NAMES: Final = ["claude", "open_ai"]


def get_provider(provider_name: str, api_key: str) -> LLMProvider:
    """Select and construct the LLMProvider matching the given provider name.

    Acts as a factory: validates provider_name against the set of supported
    providers and returns a fully constructed, ready-to-use instance. The
    API key is injected here rather than read from config internally, so
    each provider stays independently testable with a fake key and has no
    hidden dependency on how or where configuration is loaded.

    Args:
        provider_name: Which provider to use. Must be "claude" or "open_ai";
            typically sourced from settings.llm_provider.
        api_key: The API key for the selected provider, passed through to
            its constructor.

    Returns:
        A constructed ClaudeProvider or OpenAIProvider instance, ready to
        call extract_invoice on.

    Raises:
        InvalidProviderError: If provider_name is not a recognized provider.
    """
    request_id = request_id_var.get()
    logger.info(
        "provider_requested",
        provider_name=provider_name,
        request_id=request_id,
    )

    if provider_name not in ALLOWED_PROVIDER_NAMES:
        logger.warning(
            "invalid_provider_name",
            provider_name=provider_name,
            request_id=request_id,
        )
        raise InvalidProviderError(provider_name)

    return (
        ClaudeProvider(api_key)
        if provider_name == "claude"
        else OpenAIProvider(api_key)
    )
