from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions import LedgerMindException

def ledger_mind_exception_handler(_request: Request, exc: LedgerMindException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )