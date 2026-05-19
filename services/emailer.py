import os
import requests

def send_audit_email(recipient_email: str, lead_name: str, pdf_filename: str):
    resend_api_key = os.getenv("RESEND_API_KEY")
    
    # Read the PDF as bytes
    with open(pdf_filename, 'rb') as f:
        pdf_content = list(f.read()) # Resend needs bytes as a list or base64

    payload = {
        "from": "MLABS <onboarding@resend.dev>", # Use this default for testing
        "to": [recipient_email],
        "subject": "Your MLABS GEO Audit is Ready!",
        "html": f"<strong>Hello {lead_name},</strong><br><br>Your GEO audit is attached.",
        "attachments": [
            {
                "filename": pdf_filename,
                "content": pdf_content
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {resend_api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.resend.com/emails", json=payload, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"Success! Email sent via API to {recipient_email}")
    else:
        print(f"Failed to send email. API Error: {response.text}")