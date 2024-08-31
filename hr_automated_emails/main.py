import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from src.program.main import router as mailrouter
# from src.program.crontab.cron import start_scheduler

from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html

# Initialize FastAPI app with custom documentation settings
app = FastAPI(docs_url=None)  # Disable default docs URL

# ====================
# Middleware Configuration
# ====================

# Configure CORS to allow requests from specified origins
origins = ['*', "http://localhost:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================
# Router and Static Files Configuration
# ====================

# Include the mail router with a specific prefix
app.include_router(mailrouter, prefix="/mail_program")

# Mount static files directory for serving static files
app.mount("/ns", StaticFiles(directory="storage"), name="storage")

# ====================
# Root Endpoint
# ====================

@app.get("/")
def read_root():
    """
    Root endpoint for the FastAPI application.

    Returns:
        dict: A message indicating the root endpoint is working.
    """
    return {"Hello": "《《《《 ..MAIL MAIN.. 》》》》"}

# ====================
# Custom Documentation Endpoints
# ====================

@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation():
    """
    Custom Swagger UI documentation endpoint.

    Returns:
        HTML: Swagger UI documentation HTML page.
    """
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom API Docs")

@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation():
    """
    Custom ReDoc documentation endpoint.

    Returns:
        HTML: ReDoc documentation HTML page.
    """
    return get_redoc_html(openapi_url="/openapi.json", title="Custom API Docs")

# ====================
# Scheduler Initialization (Commented Out)
# ====================

# Uncomment to start the scheduler
# start_scheduler()

# ====================
# Run the Application
# ====================

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)