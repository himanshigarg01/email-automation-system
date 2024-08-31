import os
import sys
from aiosmtplib import SMTP, SMTPException
from email.message import EmailMessage
from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.program.api.extract_data import get_receivers

async def send_email():
    """
    Asynchronously send personalized emails with attachments to multiple recipients.
    
    This function loads the email template, personalizes it, attaches necessary files, 
    and sends the email using the SMTP protocol. In case of any error, detailed 
    exception handling is implemented to capture the exact line of failure.
    """
    try:
        # Load environment variables specific to email credentials
        load_dotenv("src/program/data/cred.env")

        # Get email addresses and names from the CSV file
        receiver_emails, receiver_names = get_receivers("storage/recievers_details/receivers.csv")

        # Iterate through the list of receivers and send personalized emails
        for mail_id, name in zip(receiver_emails, receiver_names):
            # Handle empty or placeholder names by using 'Team' instead
            name = "Team" if not name or name == "-" else name

            # Load and personalize the HTML email content
            html_content = load_html_template("src/program/data/email_template.html", name)
            
            # Log the HTML content for debugging
            print(f"Sending email to {mail_id}")

            # Prepare the email message
            email = EmailMessage()
            email['From'] = os.getenv("EMAIL_USERNAME")
            email['To'] = mail_id
            email['Subject'] = "Inquiry Regarding Data Analytics/Business Analytics Opportunities"
            email.set_content(html_content, subtype='html')

            # Attach files from the specified directory
            attachments_directory = "storage/attachments/"
            for filename in os.listdir(attachments_directory):
                file_path = os.path.join(attachments_directory, filename)
                with open(file_path, "rb") as attachment_file:
                    file_data = attachment_file.read()
                    email.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=filename)

            # Send the email using the SMTP server asynchronously
            async with SMTP(hostname=os.getenv("EMAIL_HOST"), port=int(os.getenv("EMAIL_PORT"))) as smtp:
                await smtp.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
                await smtp.send_message(email)

            # Log the success of each sent email
            print(f"Message: Email sent successfully to {mail_id}")

        # Return a JSON response if all emails were sent successfully
        return JSONResponse(status_code=200, content={"message": "All emails sent successfully"})

    except SMTPException as e:
        # Handle SMTP-specific exceptions and log the line number of the error
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)} (Line: {line_number})")

    except Exception as e:
        # Handle general exceptions and log the line number of the error
        exc_type, exc_obj, tb = sys.exc_info()
        line_number = tb.tb_lineno
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)} (Line: {line_number})")

def load_html_template(file_path: str, receiver_name: str) -> str:
    """
    Load and personalize the HTML email template with the receiver's name.

    Args:
    file_path (str): The path to the HTML template file.
    receiver_name (str): The name of the email recipient.

    Returns:
    str: The personalized HTML content.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        template = file.read()
    return template.replace("{{ receiver_name }}", receiver_name)