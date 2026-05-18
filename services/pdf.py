from fpdf import FPDF

def create_pdf_report(company_name: str, audit_text: str) -> str:
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"MLABS GEO Audit: {company_name}", ln=True, align="C")
    pdf.ln(10)

    # Body - cleaning text for PDF compatibility
    clean_text = audit_text.encode('latin-1', 'ignore').decode('latin-1')
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, txt=clean_text)

    file_name = f"{company_name}_audit.pdf"
    pdf.output(file_name)
    return file_name