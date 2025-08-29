from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from pathlib import Path
from dotenv import load_dotenv

# Import our modules
from database import connect_to_mongo, close_mongo_connection
from routes import router as api_routes

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Lifespan event handler for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Sun Star International API...")
    try:
        await connect_to_mongo()
        logger.info("Database connected successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("Shutting down Sun Star International API...")
    await close_mongo_connection()
    logger.info("Database disconnected successfully")

# Create FastAPI app
app = FastAPI(
    title="Sun Star International API",
    description="API for Sun Star International FZ-LLC trading company website",
    version="1.0.0",
    lifespan=lifespan
)

# Create API router with /api prefix
api_router = APIRouter(prefix="/api")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # In production, specify exact origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@api_router.get("/")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Sun Star International API is running",
        "version": "1.0.0"
    }

# Include all API routes
api_router.include_router(api_routes)

# Add the API router to the main app
app.include_router(api_router)

# Root endpoint (legacy compatibility)
@app.get("/")
async def root():
    return {"message": "Sun Star International FZ-LLC API - Use /api/ endpoints"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)