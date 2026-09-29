"""Entry point of the Python AI/NLP Service.

Run with:  python -m app.main   (docs/decisions/0004-ai-service.md §4)
"""

import os

import uvicorn
from fastapi import FastAPI

SERVICE_NAME = "ai-service"

# Configuration comes from environment variables (CLAUDE.md §12, §13).
# Defaults are for local development only.
ENVIRONMENT = os.getenv("NODE_ENV", "development")
PORT = int(os.getenv("AI_SERVICE_PORT", "8000"))
IS_DEVELOPMENT = ENVIRONMENT == "development"

# Interactive API docs are disabled outside development (ADR 0004 §5).
app = FastAPI(
    title="Career Prediction AI Service",
    docs_url="/docs" if IS_DEVELOPMENT else None,
    redoc_url="/redoc" if IS_DEVELOPMENT else None,
    openapi_url="/openapi.json" if IS_DEVELOPMENT else None,
)


@app.get("/health")
def health() -> dict:
    """Liveness check used by the Express backend (ENVIRONMENT_SETUP §39).

    Uses the Standard Response Format (API.md §6).
    Must not expose sensitive information (ENVIRONMENT_SETUP §40).
    """
    return {
        "success": True,
        "data": {"status": "ok", "service": SERVICE_NAME},
    }


if __name__ == "__main__":
    # 0.0.0.0 = listen on all network interfaces, so other containers
    # (the backend) can reach this service inside Docker.
    uvicorn.run(app, host="0.0.0.0", port=PORT)
