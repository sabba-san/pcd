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

# -------------------------------------------------
# ROUTE 3: 3D Visualizer Page
# -------------------------------------------------
@bp.route('/visualize', methods=['GET'])
def visualize():
    """
    Render the 3D visualizer page
    """
    filename = request.args.get('filename', 'default.glb')
    project_name = request.args.get('project_name', 'Demo Project')

    return render_template(
        'module3/visualize.html',
        filename=filename,
        project_name=project_name
    )
