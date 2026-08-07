from fastapi import FastAPI
from config import settings
from ingestion.router import router as ingestion_router
from exceptions_handler import ledger_mind_exception_handler
from exceptions import LedgerMindException
from observability.logging import configure_logging
from observability.middleware import RequestIDMiddleware

app = FastAPI(
    title=settings.app_name,
    description="AI powered invoice and financial ledger system",
    version=settings.app_version,
)

configure_logging()

app.add_middleware(RequestIDMiddleware)

app.add_exception_handler(LedgerMindException, ledger_mind_exception_handler)

app.include_router(ingestion_router, prefix=f"/api/{settings.api_version}")


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
    }
