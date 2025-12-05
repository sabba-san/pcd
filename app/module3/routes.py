from flask import Blueprint, render_template, request, make_response
from fpdf import FPDF
import os

# --- 1. Define the Blueprint (This was missing!) ---
bp = Blueprint('module3', __name__, url_prefix='/module3')

# --- 2. Route to Show the Form ---
@bp.route('/report', methods=['GET'])
def show_form():
    return render_template('module3/form.html')

# --- 3. Route to Generate PDF ---
@bp.route('/generate', methods=['POST'])
def generate_report():
    # --- A. Get Text Input ---
    owner_name = request.form.get('owner_name')
    unit_no = request.form.get('unit_no')
    location = request.form.get('location')
    description = request.form.get('description')
    
    # --- B. Handle Image Upload ---
    image = request.files.get('evidence')
    image_path = None
    
    if image and image.filename != '':
        upload_folder = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, image.filename)
        image.save(image_path)

    # --- C. Generate PDF with FPDF ---
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt="DLP Defect Report", ln=True, align='C')
    pdf.ln(10)
    
    # Owner & Property Info
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Owner Name: {owner_name}", ln=True)
    pdf.cell(0, 10, txt=f"Unit Number: {unit_no}", ln=True)
    pdf.ln(5)
    
    # Defect Details
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt="Defect Details:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Location: {location}", ln=True)
    pdf.ln(2)
    pdf.multi_cell(0, 10, txt=f"Description: {description}")
    pdf.ln(5)

    # Embed Image (if uploaded)
    if image_path:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, txt="Evidence Photo:", ln=True)
        pdf.ln(2)
        try:
            pdf.image(image_path, x=10, w=100)
        except Exception as e:
            pdf.cell(0, 10, txt="Error loading image.", ln=True)

    # --- D. Return PDF as Download ---
    pdf_bytes = pdf.output(dest='S')
    response = make_response(bytes(pdf_bytes))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Report_Defect.pdf'
    
    return response