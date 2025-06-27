from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from . import api, models, database
from .routers import auth, identifiers, datasources, rdf, graphdb
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="BioDataFuse API")

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"🔵 {request.method} {request.url.path} - Client: {request.client.host}")
    
    # Log request headers for debugging
    if request.url.path.startswith("/api/graphdb"):
        logger.info(f"📋 Headers: {dict(request.headers)}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Log response details
    status_color = "🟢" if response.status_code < 400 else "🔴" if response.status_code >= 500 else "🟡"
    logger.info(f"{status_color} {request.method} {request.url.path} - {response.status_code} ({process_time:.3f}s)")
    
    return response

# Custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    logger.error(f"❌ 404 NOT FOUND: {request.method} {request.url.path}")
    logger.error(f"📍 Available GraphDB routes:")
    logger.error(f"   POST /api/graphdb/test-connection")
    logger.error(f"   POST /api/graphdb/list-repositories") 
    logger.error(f"   POST /api/graphdb/create-repository")
    logger.error(f"   POST /api/graphdb/delete-repository")
    logger.error(f"   POST /api/graphdb/upload-rdf")
    
    return JSONResponse(
        status_code=404,
        content={
            "detail": f"Endpoint not found: {request.method} {request.url.path}",
            "available_endpoints": [
                "POST /api/graphdb/test-connection",
                "POST /api/graphdb/list-repositories",
                "POST /api/graphdb/create-repository", 
                "POST /api/graphdb/delete-repository",
                "POST /api/graphdb/upload-rdf"
            ]
        }
    )

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

# Include routers with detailed logging
logger.info("🚀 Registering API routers...")
app.include_router(api.api_router)
app.include_router(auth.router)
app.include_router(identifiers.router)
app.include_router(datasources.router)
app.include_router(rdf.router, prefix="/api")
app.include_router(graphdb.router)
logger.info("✅ All routers registered successfully")

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🌟 BioDataFuse API starting up...")
    # Create database tables
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    logger.info("Database tables created")

