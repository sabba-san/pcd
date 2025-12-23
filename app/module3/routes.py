from flask import Blueprint, render_template, request, g, redirect, url_for, session
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
    return db

@bp.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 1. Insert Defect Page
@bp.route('/insert_defect', methods=['GET'])
def insert_defect():
    # Pre-fill project name from session if available
    user_project = session.get('user_project', '')
    return render_template('module3/insert_defect.html', user_project=user_project)

# 2. Submit Defect (NOW LINKS TO USER_ID)
@bp.route('/submit_defect', methods=['POST'])
def submit_defect():
    # Security: Ensure user is logged in
    if 'user_id' not in session:
        return redirect(url_for('module1.login_ui'))
        
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
    # Insert with USER_ID
    db.execute(
        'INSERT INTO defects (user_id, project_name, unit_no, description, status, filename) VALUES (?, ?, ?, ?, ?, ?)',
        (session['user_id'], project_name, unit_no, f"Uploaded: {filename}", 'draft', filename)
    )
    db.commit()

    return render_template('module3/process_defect.html', 
                           project_name=project_name, 
                           unit_no=unit_no, 
                           filename=filename)

# 3. Evidence Report (Filtered by User)
@bp.route('/evidence_report')
def evidence_report():
    if 'user_id' not in session: return redirect(url_for('module1.login_ui'))
    
    db = get_db()
    
    # Lawyer sees ALL, Homeowner sees THEIR OWN
    if session.get('user_role') == 'lawyer':
        cur = db.execute('SELECT * FROM defects')
    else:
        cur = db.execute('SELECT * FROM defects WHERE user_id = ?', (session['user_id'],))
        
    defects = cur.fetchall()
    
    # Check status for banner
    if session.get('user_role') == 'lawyer':
        draft_count = db.execute("SELECT COUNT(*) FROM defects WHERE status = 'draft'").fetchone()[0]
    else:
        draft_count = sum(1 for d in defects if d['status'] == 'draft')
        
    case_status = "PENDING REVIEW" if draft_count > 0 else "FINALIZED"

    case_info = {
        "case_id": f"CASE-{session['user_id']:03d}",
        "client": session.get('user_name'),
        "project": session.get('user_project'),
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

# 5. Validate All
@bp.route('/validate_all', methods=['POST'])
def validate_all():
    db = get_db()
    # Lawyers lock ALL drafts, Users lock THEIR drafts
    if session.get('user_role') == 'lawyer':
         db.execute("UPDATE defects SET status = 'locked' WHERE status = 'draft'")
    else:
         db.execute("UPDATE defects SET status = 'locked' WHERE status = 'draft' AND user_id = ?", (session['user_id'],))
         
    db.commit()
    return redirect(url_for('module3.evidence_report'))

# 6. Visualizer
@bp.route('/visualize')
def visualize():
    filename = request.args.get('filename', 'sisiranRendered.glb') 
    project_name = request.args.get('project_name', 'Demo Project')
    back_to_param = request.args.get('back_to', 'homeowner')
    
    if back_to_param == 'developer':
        back_url = url_for('module1.developer_portal', project_name=project_name)
    elif back_to_param == 'lawyer':
        back_url = url_for('module1.lawyer_dashboard')
    else:
        back_url = url_for('module1.dashboard')

    return render_template('module3/visualize.html', filename=filename, project_name=project_name, back_url=back_url)