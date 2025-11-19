from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1 import auth, uploads, ai, health

app = FastAPI(title="SmartBarangay Forms API", version="0.1.0")

# CORS (dev-friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(uploads.router, prefix="/api/v1/uploads", tags=["uploads"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])


@app.get("/")
def root():
    return {"service": "SmartBarangay Forms API", "version": "0.1.0"}
