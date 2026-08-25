from abc import ABC, abstractmethod
from anthropic import AsyncAnthropic
from extraction.schemas import ExtractedInvoice


class LLMProvider(ABC):
    @abstractmethod
    async def extract_invoice(self, file_bytes: bytes) -> ExtractedInvoice:
        pass


class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)
