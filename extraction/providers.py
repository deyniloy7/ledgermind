from abc import ABC, abstractmethod
from extraction.schemas import ExtractedInvoice


class LLMProvider(ABC):
    @abstractmethod
    async def extract_invoice(self, file_bytes: bytes) -> ExtractedInvoice:
        pass
