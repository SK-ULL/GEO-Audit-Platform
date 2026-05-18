import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_audit_email(recipient_email: str, lead_name: str, pdf_filename: str):
    """
    Sends the generated PDF audit to the lead via email.
    """
    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")

    if not sender_email or not sender_password:
        print("WARNING: Email credentials missing in .env file.")
        return

    # 1. Draft the Email
    msg = EmailMessage()
    msg['Subject'] = 'Your MLABS GEO Audit is Ready!'
    msg['From'] = sender_email
    msg['To'] = recipient_email

    body = f"""Hello {lead_name},

Thank you for requesting a GEO Audit from MLABS. 
Our AI has finished analyzing your digital footprint. Please find your customized report attached to this email.

Best regards,
The MLABS Automation Engine
"""
    msg.set_content(body)

    # 2. Attach the PDF
    try:
        with open(pdf_filename, 'rb') as f:
            pdf_data = f.read()
        
        msg.add_attachment(
            pdf_data, 
            maintype='application', 
            subtype='pdf', 
            filename=pdf_filename
        )
    except FileNotFoundError:
        print(f"Error: Could not find the file {pdf_filename} to attach.")
        return

    # 3. Send the Email securely via Gmail's SMTP server
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Success! Email sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")