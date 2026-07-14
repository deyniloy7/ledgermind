from fastapi import APIRouter, UploadFile, File
from ingestion.schemas import UploadResponse
from ingestion.service import process_upload
from datetime import datetime, timezone

router = APIRouter(prefix="/invoices", tags=["ingestion"])


@router.post("/upload", response_model=UploadResponse)
async def upload_invoice(file: UploadFile = File(...)) -> UploadResponse:
    contents = await process_upload(file)
    return UploadResponse(
        filename=file.filename,
        size_bytes=len(contents),
        content_type=file.content_type,
        message="Invoice uploaded successfully",
        uploaded_at=datetime.now(timezone.utc),
    )
