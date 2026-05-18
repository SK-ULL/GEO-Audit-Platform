from pydantic import BaseModel, EmailStr, Field

class LeadInput(BaseModel):
    # Field is the modern, more stable way to handle min_length and stripping
    name: str = Field(..., min_length=1)
    email: EmailStr
    company_name: str = Field(..., min_length=1)
    company_url: str

