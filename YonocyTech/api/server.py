"""FastAPI application entry point with CORS, routes, and middleware."""
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import auth, sessions, providers, agents, contact, admin
from api.schemas import HealthResponse

# Auto-migrate database on startup
from database.schema import migrate
migrate()

app = FastAPI(
    title="YonocyTech AI API",
    version="2.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow React frontend (Vercel) and Streamlit
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:8501").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"},
    )


@app.get("/health", response_model=HealthResponse, tags=["System"])
def health():
    return HealthResponse()


app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(providers.router)
app.include_router(agents.router)
app.include_router(contact.router)
app.include_router(admin.router)
