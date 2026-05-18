# Python
from pydantic import BaseModel, EmailStr, HttpUrl, constr

class LeadInput(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr
    company_name: constr(strip_whitespace=True, min_length=1)
    company_url: HttpUrl

