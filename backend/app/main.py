"""
OcchioEsperto.it — Main FastAPI application.
Serves API endpoints, static files, and the frontend.
"""
import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .config import (
    CORS_ORIGINS, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW_SECONDS,
    UPLOAD_DIR, STATIC_DIR, DISCLAIMER, IS_PRODUCTION,
)
from .database import init_db
from .routers import auth, vespa, payments, admin

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application on startup."""
    # Create directories
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(STATIC_DIR, exist_ok=True)

    # Initialize application database
    init_db()
    print("✅ Application database initialized")

    yield

    print("🛑 Application shutting down")


app = FastAPI(
    title="OcchioEsperto.it API",
    description="API per l'identificazione e analisi di Vespa Piaggio",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Rate limit handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Middleware ---

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["X-Process-Time"] = str(process_time)

    # HSTS (HTTP Strict Transport Security) — only in production
    if IS_PRODUCTION:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

    return response


@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    """Global exception handler."""
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Errore interno del server",
                "disclaimer": DISCLAIMER,
                "error_type": type(e).__name__,
            },
        )


# --- Routers ---

app.include_router(auth.router)
app.include_router(vespa.router)
app.include_router(payments.router)
app.include_router(admin.router)


# --- Static files ---

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Serve frontend static files (if build exists)
if os.path.exists(STATIC_DIR) and os.listdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# --- API Info ---

@app.get("/api")
def api_root():
    """API root with available endpoints."""
    return {
        "name": "OcchioEsperto.it API",
        "version": "1.0.0",
        "endpoints": {
            "auth": {
                "register": "POST /api/register",
                "login": "POST /api/login",
                "profile": "GET /api/me",
            },
            "vespa": {
                "models": "GET /api/vespa/models",
                "model_detail": "GET /api/vespa/models/{id}",
                "identify": "POST /api/vespa/identify",
                "analyze": "POST /api/vespa/analyze",
                "save": "POST /api/vespa/save",
                "garage": "GET /api/vespa/garage",
                "lead": "POST /api/vespa/lead",
            },
            "payments": {
                "plans": "GET /api/payments/plans",
                "checkout": "POST /api/payments/create-checkout",
                "webhook": "POST /api/payments/webhook",
                "verify": "POST /api/payments/verify",
            },
            "admin": {
                "leads": "GET /api/admin/leads",
                "stats": "GET /api/admin/stats",
            },
        },
        "docs": "/api/docs",
        "disclaimer": DISCLAIMER,
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "disclaimer": DISCLAIMER,
    }


# --- Frontend catch-all ---

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    """
    Serve the frontend SPA for non-API routes.
    Falls back to index.html for client-side routing.
    """
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)

    return JSONResponse(
        status_code=200,
        content={
            "message": "OcchioEsperto.it - Benvenuto! Il frontend è in fase di sviluppo.",
            "api_docs": "/api/docs",
            "disclaimer": DISCLAIMER,
        }
    )