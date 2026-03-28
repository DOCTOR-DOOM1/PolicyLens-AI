from fpdf import FPDF

def generate_policy_pdf(user_data, scheme_name):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="PolicyLens AI - Application Draft", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="(This is a helper document for CSC/Government Offices)", ln=True, align='C')
    pdf.ln(10)

    # Scheme Info
    pdf.set_font("Arial", 'B', 12)
    safe_scheme = scheme_name.replace("₹", "Rs. ")
    pdf.cell(200, 10, txt=f"TARGET SCHEME: {safe_scheme}", ln=True)
    pdf.ln(5)

    # User Data
    pdf.set_font("Arial", size=12)
    for key, value in user_data.items():
        safe_value = str(value).replace("₹", "Rs. ")
        pdf.cell(200, 10, txt=f"{key.capitalize()}: {safe_value}", ln=True)

    pdf.ln(10)
    pdf.multi_cell(0, 10, txt="Note to Official: The above citizen has been identified as eligible for this scheme via PolicyLens RAG Analysis. Please facilitate the official filing process.")

    return pdf.output() # This returns the PDF bytes