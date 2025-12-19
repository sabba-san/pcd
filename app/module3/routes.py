from flask import Blueprint, render_template, request
import os

# -------------------------------------------------
# 1. Define Blueprint
# -------------------------------------------------
bp = Blueprint(
    'module3',
    __name__,
    url_prefix='/module3'
)

# -------------------------------------------------
# ROUTE 1: Display Insert Defect Form
# -------------------------------------------------
@bp.route('/insert_defect', methods=['GET'])
def insert_defect():
    """
    Render the one-stop defect insertion form
    """
    return render_template('module3/insert_defect.html')

# -------------------------------------------------
# ROUTE 2: Handle Form Submission & Show Report
# -------------------------------------------------
@bp.route('/submit_defect', methods=['POST'])
def submit_defect():
    # 1. Retrieve form data
    project_name = request.form.get('project_name')
    owner_name = request.form.get('owner_name')
    unit_no = request.form.get('unit_no')

    # 2. Configure upload directory
    upload_folder = os.path.join(
        os.getcwd(), 'app', 'static', 'uploads'
    )
    os.makedirs(upload_folder, exist_ok=True)

    # 3. Handle LiDAR file upload
    lidar_file = request.files.get('lidar_file')
    filename = "No File"

    if lidar_file and lidar_file.filename:
        filename = lidar_file.filename
        lidar_file.save(os.path.join(upload_folder, filename))

    # 4. Handle optional PDF / image upload
    pdf_file = request.files.get('pdf_file')
    if pdf_file and pdf_file.filename:
        pdf_file.save(os.path.join(upload_folder, pdf_file.filename))

    # 5. Render processing report
    return render_template(
        'module3/process_defect.html',
        project_name=project_name,
        owner_name=owner_name,
        unit_no=unit_no,
        filename=filename
    )

# --- 3. The 3D Visualizer ---
@bp.route('/visualize')
def visualize():
    # Get parameters from URL
    filename = request.args.get('filename', 'rumah sisiran.glb')
    project_name = request.args.get('project_name', 'Demo Project')
    back_to = request.args.get('back_to', 'homeowner')
    
    # CHANGE THIS LINE: viewer.html -> visualize.html
    return render_template('module3/visualize.html', 
                           filename=filename, 
                           project_name=project_name,
                           back_to=back_to)
    
    
    # --- 4. Evidence Review Report (Lawyer Task 1) ---
@bp.route('/evidence_report')
def evidence_report():
    # Mock Data for the specific case (CASE-001)
    report_data = {
        "case_id": "CASE-001",
        "client": "Abbas Abu Dzarr",
        "project": "ASMARINDA12",
        "submission_date": "2025-12-14",
        "ai_confidence": 98,  # Overall AI score
        "risk_level": "High",
        "defects": [
            {
                "id": "D-101",
                "type": "Structural Wall Crack",
                "location": "Master Bedroom - North Wall",
                "severity": "High",
                "confidence": "99%",
                "img": "leak_01.jpg", # Uses your existing demo image
                "status": "Auto-Detected"
            },
            {
                "id": "D-102",
                "type": "Water Mark / Dampness",
                "location": "Ceiling - Corner",
                "severity": "Medium",
                "confidence": "85%",
                "img": "leak_01.jpg",
                "status": "Auto-Detected"
            }
        ]
    }
    return render_template('module3/evidence_report.html', report=report_data)