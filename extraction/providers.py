import base64
from abc import ABC, abstractmethod
import json

from anthropic import AsyncAnthropic

from exceptions import InvalidProviderResponseError
from extraction.schemas import ExtractedInvoice


class LLMProvider(ABC):
    @abstractmethod
    async def extract_invoice(self, file_bytes: bytes) -> ExtractedInvoice:
        pass


class ClaudeProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = AsyncAnthropic(api_key=api_key)

    async def extract_invoice(self, file_bytes: bytes) -> ExtractedInvoice:
        """Extract structured invoice data from a file using Claude's API.

        Claude is instructed to return raw JSON, but occasionally wraps its
        response in markdown code fences despite this instruction. This method
        defensively strips such fences before parsing to avoid brittle failures
        on otherwise-valid responses.

        Args:
            file_bytes: The raw invoice file content (PDF), as returned by ingestion's
                process_upload.

        Returns:
            ExtractedInvoice: An ExtractedInvoice with vendor, date, currency, total,
                and line items parsed from the document.

        Raises:
            InvalidProviderResponseError: If Claude's response cannot be parsed as
                valid JSON.
        """
        encoded_file = base64.standard_b64encode(file_bytes).decode("utf-8")
        response = await self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": encoded_file,
                            },
                        },
                        {"type": "text", "text": self._build_prompt()},
                    ],
                }
            ],
        )
        raw_json = response.content[0].text
        cleaned_json = raw_json.strip()

        if cleaned_json.startswith("```"):
            cleaned_json = cleaned_json.split("\n", 1)[1]

        if cleaned_json.endswith("```"):
            cleaned_json = cleaned_json.rsplit("\n", 1)[0]

        try:
            parsed_data = json.loads(cleaned_json)
        except json.JSONDecodeError:
            raise InvalidProviderResponseError(raw_response=raw_json)
        extracted_invoice = ExtractedInvoice(**parsed_data)
        return extracted_invoice

    def _build_prompt(self) -> str:
        """Build the extraction instruction prompt sent to Claude.

        Explicitly specifies field names, types, and output format so the
        model returns JSON matching ExtractedInvoice's schema, rather than
        a plausible-but-mismatched structure.

        Returns:
            The full prompt text as a single string.
        """
        return """Extract the following invoice fields as JSON:
                    - vendor_name (string)
                    - invoice_date (string, ISO 8601 format YYYY-MM-DD)
                    - currency (string, 3-letter code like USD, INR)
                    - total_amount (number, no currency symbols)
                    - line_items (array of objects, each with:
                        description, quantity, unit_price, line_total)

                    Return ONLY valid JSON matching this exact structure. No
                    explanation, no markdown formatting, no code fences.
                """
