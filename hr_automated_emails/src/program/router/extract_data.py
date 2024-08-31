from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import warnings
from enum import Enum
from src.program.api.extract_data import *  # Assuming this import is needed; otherwise, it can be removed
import sys

# Suppress warnings
warnings.filterwarnings("ignore")

# Initialize FastAPI app and router
app = FastAPI()
router = APIRouter()

# ====================
# Endpoint Definitions
# ====================

@router.get("/data_extraction", tags=["Data Extraction"])
async def data_extraction_endpoint():
    """
    Example GET endpoint to verify the API's functionality.

    Returns:
        dict: A simple message indicating the endpoint is working.
    """
    return {"message": "Data extraction API is working."}

@router.post("/receiver_info_file", tags=["File Upload"])
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a CSV file containing receiver information.

    Args:
        file (UploadFile): The file to be uploaded.

    Returns:
        dict: Information about the uploaded file, including its location.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            return JSONResponse(status_code=400, content={"message": "File must be a CSV."})

        # Define the save directory for the uploaded file
        save_directory = "storage/recievers_details"
        os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist

        # Define file path and save the file
        file_path = os.path.join(save_directory, "receivers.csv").replace("\\", "/")
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)

        # Read the CSV file to validate columns
        df = pd.read_csv(file_path)
        required_columns = {'s_no', 'email_id', 'name'}
        if not required_columns.issubset(df.columns):
            return JSONResponse(status_code=400, content={"message": "CSV must contain columns: s_no, email_id, name."})

        # Adjust file path for response
        file_path = file_path.replace("storage", "ns")

        return {"filename": "receivers.csv", "location": file_path}
    except Exception as e:
        # Log the line number of the error
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno
        return JSONResponse(status_code=500, content={"message": f"Failed to upload file: {str(e)} (Line: {line_number})"})

# ====================
# Enum Definitions
# ====================

class AttachmentType(str, Enum):
    """
    Enum for different types of attachments.
    """
    resume = "resume"
    portfolio = "portfolio"
    cover_letter = "cover_letter"
    others = "others"


@router.post("/save_attachments", tags=["File Upload"])
async def save_attachments(type: AttachmentType, file: UploadFile = File(...)):
    """
    Endpoint to save an attachment to a specified directory based on its type.

    Args:
        type (AttachmentType): The type of attachment (e.g., resume, portfolio).
        file (UploadFile): The file to be uploaded.

    Returns:
        dict: Information about the uploaded file, including its location.
    """
    try:
        # Define the save directory for attachments
        save_directory = "storage/attachments"
        os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist

        # Extract file extension and construct full file name
        file_extension = os.path.splitext(file.filename)[1]
        full_file_name = f"{type.value}{file_extension}"

        # Construct the full file path
        file_path = os.path.join(save_directory, full_file_name).replace("\\", "/")

        # Save the file
        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)

        # Adjust file path for response
        file_path = file_path.replace("storage", "ns")

        return {"filename": full_file_name, "location": file_path}
    except Exception as e:
        # Log the line number of the error
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno
        return {"error": f"Failed to save attachment: {str(e)} (Line: {line_number})"}

# Include the router in the FastAPI app
app.include_router(router)