from fastapi import FastAPI
from config import settings

app = FastAPI(
    title=settings.app_name,
    description="AI powered invoice and financial ledger system",
    version=settings.app_version
)

@app.get("/health")
async def health_check():
    return {
        "status": "ok", 
        "app": settings.app_name,
        "version": settings.app_version
        }