from __future__ import annotations

import logging
import uuid
from enum import StrEnum
from typing import TYPE_CHECKING

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from starlette.responses import Response

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

log = structlog.get_logger()

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class InvestigationStatus(StrEnum):
    queued = "queued"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class Severity(StrEnum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    warning = "warning"


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------


class IncidentRequest(BaseModel):
    title: str
    service: str
    severity: Severity = Severity.warning
    description: str = ""


class InvestigationResponse(BaseModel):
    incident: str
    status: InvestigationStatus
    next_steps: list[str]


class ErrorResponse(BaseModel):
    detail: str
    request_id: str | None = None


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AI SRE Copilot",
    version="0.1.0",
    description="Incident investigation API for cloud-native systems.",
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_logging_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request_id = str(uuid.uuid4())[:8]
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id, method=request.method, path=request.url.path
    )

    log.info("request_started", client=request.client.host if request.client else None)

    response = await call_next(request)

    log.info("request_completed", status_code=response.status_code)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    log.error("unhandled_exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": None},
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "ai-sre-copilot"}


@app.post(
    "/api/v1/incidents/investigate",
    response_model=InvestigationResponse,
    responses={422: {"model": ErrorResponse}},
)
async def investigate(request: IncidentRequest) -> InvestigationResponse:
    log.info("investigation_requested", service=request.service, severity=request.severity.value)

    # MVP placeholder. Future versions will call observability adapters,
    # Kubernetes, GitHub and an LLM investigator.
    return InvestigationResponse(
        incident=request.title,
        status=InvestigationStatus.queued,
        next_steps=[
            "Collect Kubernetes workload state",
            "Query Prometheus metrics",
            "Inspect logs and traces",
            "Correlate recent deployments",
        ],
    )
