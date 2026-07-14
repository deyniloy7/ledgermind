from datetime import datetime
from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    size_bytes: int
    content_type: str
    message: str
    uploaded_at: datetime
