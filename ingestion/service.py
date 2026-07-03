from fastapi import UploadFile

async def process_upload(file: UploadFile) -> bytes :
    contents = await file.read()
    return contents