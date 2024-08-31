
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.program.router import extract_data as data_extraction_router
from src.program.router import send_email as email_sending_router
from datetime import date

# Initialize FastAPI application
app = FastAPI()

# ====================
# Middleware Configuration
# ====================

# Add CORS middleware to allow requests from all origins (modify as needed for security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify as needed to specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Modify as needed to specify allowed methods
    allow_headers=["*"],  # Modify as needed to specify allowed headers
)

# ====================
# Router Configuration
# ====================

# Create a new APIRouter instance
router = APIRouter()

# Include the routers for data extraction and email sending with specific prefixes
router.include_router(data_extraction_router.router, prefix="/data_extraction")
router.include_router(email_sending_router.router, prefix="/email_sending")

# ====================
# Root Endpoint
# ====================

@router.get("/")
def read_root():
    """
    Root endpoint for the main API.

    Returns:
        dict: A simple message indicating that the main API is working.
    """
    return {"Hello": "Main email API"}

# Include the router in the FastAPI application
app.include_router(router)
