from fastapi import FastAPI

app = FastAPI(
    title="LedgerMind",
    description="AI powered invoice and financial ledger system",
    version="0.1.0"
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "app": "LedgerMind"}