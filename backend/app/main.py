from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import api, models, database
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="BioDataFuse API")

# Configure CORS
origins = [
    "http://localhost:3000",  # Vue.js development server
    "http://localhost:8000",  # Production server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api.router, prefix="/api")

# Startup event
@app.on_event("startup")
async def startup_event():
    # Create database tables
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    logger.info("Database tables created")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}