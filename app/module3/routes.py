from flask import Blueprint, render_template, request, g, redirect, url_for
import sqlite3
import os

bp = Blueprint('module3', __name__, url_prefix='/module3')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATABASE = os.path.join(BASE_DIR, 'app.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
        db.execute('''
            CREATE TABLE IF NOT EXISTS defects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT,
                unit_no TEXT,
                description TEXT,
                status TEXT DEFAULT 'draft',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
    return db

@bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 1. Insert Defect
@bp.route('/insert_defect', methods=['GET'])
def insert_defect():
    return render_template('module3/insert_defect.html')

# 2. Submit Defect
@bp.route('/submit_defect', methods=['POST'])
def submit_defect():
    project_name = request.form.get('project_name')
    unit_no = request.form.get('unit_no')
    
    upload_folder = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    
    lidar_file = request.files.get('lidar_file')
    filename = "No File"
    if lidar_file and lidar_file.filename:
        filename = lidar_file.filename
        lidar_file.save(os.path.join(upload_folder, filename))

    db = get_db()
    db.execute(
        'INSERT INTO defects (project_name, unit_no, description, status) VALUES (?, ?, ?, ?)',
        (project_name, unit_no, f"Uploaded: {filename}", 'draft')
    )
    db.commit()

    return render_template('module3/process_defect.html', project_name=project_name, unit_no=unit_no, filename=filename)

# 3. Evidence Report
@bp.route('/evidence_report')
def evidence_report():
    db = get_db()
    cur = db.execute('SELECT * FROM defects')
    defects = cur.fetchall()
    
    draft_count = db.execute("SELECT COUNT(*) FROM defects WHERE status = 'draft'").fetchone()[0]
    case_status = "PENDING REVIEW" if draft_count > 0 else "FINALIZED"

    case_info = {
        "case_id": "CASE-001",
        "client": "Abbas Abu Dzarr",
        "project": "ASMARINDA12",
        "status": case_status,
        "risk_level": "High"
    }

    return render_template('module3/evidence_report.html', defects=defects, report=case_info)

# 4. Lock Single Evidence
@bp.route('/lock_evidence/<int:id>', methods=['POST'])
def lock_evidence(id):
    db = get_db()
    db.execute("UPDATE defects SET status = 'locked' WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for('module3.evidence_report'))

# 5. Validate All (Bulk Lock)
@bp.route('/validate_all', methods=['POST'])
def validate_all():
    db = get_db()
    db.execute("UPDATE defects SET status = 'locked' WHERE status = 'draft'")
    db.commit()
    return redirect(url_for('module3.evidence_report'))

# 6. Visualizer (UPDATED BACK BUTTON LOGIC)
@bp.route('/visualize')
def visualize():
    filename = request.args.get('filename', 'sisiranRendered.glb') 
    project_name = request.args.get('project_name', 'Demo Project')
    
    # Check where the user came from
    back_to_param = request.args.get('back_to', 'homeowner')
    
    if back_to_param == 'developer':
        # FIX: Send developer back to the specific project page they were on
        back_url = url_for('module1.developer_portal', project_name=project_name)
    elif back_to_param == 'lawyer':
        back_url = url_for('module1.lawyer_dashboard')
    else:
        back_url = url_for('module1.dashboard')

    return render_template('module3/visualize.html', 
                           filename=filename, 
                           project_name=project_name,
                           back_url=back_url) # Pass full URL to template