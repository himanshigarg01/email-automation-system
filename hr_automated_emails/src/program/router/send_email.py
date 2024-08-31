from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from src.program.api.send_email import send_email

# Initialize FastAPI application
app = FastAPI()

# Initialize APIRouter
router = APIRouter()

# ====================
# Endpoint Definitions
# ====================

@router.get("/send-email-testing", tags=["Email Testing"])
async def send_email_testing_endpoint():
    """
    Example GET endpoint to test the email sending functionality.

    Returns:
        dict: A simple message indicating that the email sending API is working.
    """
    return {"message": "Email sending API is working."}

@router.post("/send-email", tags=["Email Sending"])
async def send_email_endpoint():
    """
    Endpoint to trigger the email sending process.

    Returns:
        JSONResponse: A message indicating the success or failure of the email sending operation.
    """
    try:
        # Call the asynchronous send_email function
        await send_email()
        return JSONResponse(status_code=200, content={"message": "All emails sent successfully"})
    
    except HTTPException as e:
        # Handle HTTPException and return appropriate error response
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    
    except Exception as e:
        # Handle unexpected errors and log the error details
        import sys
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)} (Line: {line_number})")

# Include the router in the FastAPI application
app.include_router(router)