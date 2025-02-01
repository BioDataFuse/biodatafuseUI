from fastapi import APIRouter
from .routers import auth, identifiers, datasources

api_router = APIRouter()

# Include all routers
api_router.include_router(auth.router, prefix="/api")
api_router.include_router(identifiers.router, prefix="/api")
api_router.include_router(datasources.router, prefix="/api")

# Health check endpoint
@api_router.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}