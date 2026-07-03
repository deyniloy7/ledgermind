from fastapi import APIRouter,  UploadFile, File
from ingestion.service import process_upload

router = APIRouter(prefix="/invoices", tags=["ingestion"])

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...)):
    contents = await process_upload(file)
    return {
        "filename": file.filename,
        "size": len(contents),
        "content_type": file.content_type
    }