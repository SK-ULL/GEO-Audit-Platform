from fastapi.middleware.cors import CORSMiddleware
from services.google_sheets import log_lead_to_sheets
from services.google_drive import upload_to_drive
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# Import your Pydantic model (which now handles the Email/URL validation)
from models import LeadInput

# Import your service pipeline
from services.scraper import scrape_company_website
from services.ai import generate_geo_audit
from services.pdf import create_pdf_report
from services.emailer import send_audit_email

# Initialize the API with some branding for the /docs page
app = FastAPI(
    title="MLABS GEO Engine",
    description="Automated Generative Engine Optimization Audit API with resilient fallbacks.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows any site to access your API
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
@app.get("/healthz")
async def health_check():
    return {"status": "ok"}

# --- CUSTOM VALIDATION HANDLER ---
# This catches bad emails/URLs and returns a clean, readable error to the user
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    custom_errors = []
    for err in errors:
        custom_errors.append({
            "field": err["loc"][-1],
            "message": err["msg"].capitalize()
        })
    
    print(f"Validation Error: {custom_errors}")
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid input data provided.",
            "details": custom_errors
        }
    )

# --- MAIN API ROUTE ---
@app.post("/api/submit-lead")
async def process_lead(lead: LeadInput):
    try:
        # The data validation (Email/URL formats) has already happened automatically 
        # by the time the code reaches this point, thanks to FastAPI & Pydantic!
        print(f"\n🚀 New Lead Received: {lead.name} from {lead.company_name}")
        
        # 1. SCRAPE (Includes your new timeout/fallback logic)
        print(f"--- 1. Scraping: {lead.company_url} ---")
        scraped_content = scrape_company_website(str(lead.company_url))
        
        # 2. ANALYZE (Includes your new AI try/except blocks)
        print(f"--- 2. Analyzing with AI... ---")
        audit_report_md = generate_geo_audit(lead.company_name, scraped_content)
        
        # 3. GENERATE PDF
        print(f"--- 3. Generating PDF Document... ---")
        pdf_filename = create_pdf_report(lead.company_name, audit_report_md)
        
        # 4. SEND EMAIL
        print(f"--- 4. Sending Email to {lead.email}... ---")
        send_audit_email(str(lead.email), lead.name, pdf_filename)
        
        # 5. BONUS: CLOUD LOGGING & ARCHIVING
        print(f"--- 5. Archiving to Google Cloud... ---")
        log_lead_to_sheets(lead.name, str(lead.email), lead.company_name, "Success")
        upload_to_drive(pdf_filename)
        
        print(f" Pipeline complete for {lead.company_name}!\n")
        return {
            "status": "success",
            "message": f"Audit complete and emailed to {lead.email}!",
            "lead_name": lead.name
        }

    except Exception as e:
        # This catches any massive, unexpected system crashes
        print(f"CRITICAL PIPELINE ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail="An internal processing error occurred.")

# --- SERVER STARTUP ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)