from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.database import Base, engine
from backend.models.user import User
from backend.models.device import Device
from backend.models.session import Session
from backend.models.alert import Alert

from backend.api.devices import router as device_router
from backend.api.users import router as user_router
from backend.api.sessions import router as session_router
from backend.api.alerts import router as alert_router
from backend.api.telemetry import router as telemetry_router
from backend.api.monitoring import router as monitoring_router



# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="AI-Powered Insider Threat Detection",
    version="1.0"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routers
app.include_router(device_router)
app.include_router(user_router)
app.include_router(session_router)
app.include_router(alert_router)
app.include_router(telemetry_router)
app.include_router(monitoring_router)
# Home API
@app.get("/")
def home():
    return {
        "message": "Insider Threat Detection API is running"
    }


# Health Check API
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }