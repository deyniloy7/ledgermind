from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: Decimal
    line_total: Decimal


class ExtractedInvoice(BaseModel):
    vendor_name: str
    invoice_date: date
    currency: str
    total_amount: Decimal
    line_items: list[LineItem] = []
