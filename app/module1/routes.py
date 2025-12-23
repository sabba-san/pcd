from flask import Blueprint, render_template, request, redirect, url_for, session, g
import sqlite3
import os

bp = Blueprint('module1', __name__)

# --- DATABASE CONFIG ---
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

# --- HELPER: GUESS SEVERITY ---
def estimate_severity(description):
    desc = description.lower()
    if 'leak' in desc or 'structural' in desc or 'roof' in desc:
        return 'High'
    elif 'crack' in desc:
        return 'Medium'
    else:
        return 'Low'

# 1. Login Routes
@bp.route('/login', methods=['GET'])
def login_ui():
    return render_template('login.html')

@bp.route('/auth', methods=['POST'])
def login_auth():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == 'admin@uum.edu.my' and password == 'admin123':
        session['user_role'] = 'admin'
        session['user_name'] = 'System Administrator'
        return redirect(url_for('module1.admin_dashboard'))
    elif email == 'lawyer@firm.com' and password == 'law123':
        session['user_role'] = 'lawyer'
        session['user_name'] = 'Pn. Zulaikha'
        return redirect(url_for('module1.lawyer_dashboard'))
    elif email == 'developer@ecoworld.com' and password == 'dev123':
        session['user_role'] = 'developer'
        session['user_name'] = 'EcoWorld Contractor'
        return redirect(url_for('module1.developer_portal'))
    elif email == 'abbas@student.uum.edu.my' and password == 'password123':
        session['user_role'] = 'user'
        session['user_name'] = 'Abbas (Student)'
        return redirect(url_for('module1.dashboard'))
    else:
        session['user_role'] = 'user'
        session['user_name'] = 'Abbas Abu Dzarr'
        return redirect(url_for('module1.dashboard'))

# --- 2. SMART DASHBOARD ROUTER (THE FIX) ---
@bp.route('/dashboard')
def dashboard():
    role = session.get('user_role')
    
    # If Developer -> Go to Developer Portal
    if role == 'developer':
        return redirect(url_for('module1.developer_portal'))
    
    # If Lawyer -> Go to Lawyer Console
    elif role == 'lawyer':
        return redirect(url_for('module1.lawyer_dashboard'))
    
    # Default: Homeowner Dashboard
    db = get_db()
    cur = db.execute("SELECT * FROM defects ORDER BY id DESC LIMIT 5")
    recent_defects = cur.fetchall()
    return render_template('dashboard.html', user=session.get('user_name'), defects=recent_defects)

# 3. Admin Dashboard
@bp.route('/admin')
def admin_dashboard():
    return render_template('admin_preview.html', user="System Administrator")

# 4. Lawyer Dashboard
@bp.route('/lawyer_dashboard')
def lawyer_dashboard():
    db = get_db()
    cur = db.execute('SELECT * FROM defects')
    real_cases = cur.fetchall()
    return render_template('module1/lawyer_dashboard.html', cases=real_cases, user="Pn. Zulaikha")

# --- 5. HOUSING DEVELOPER DASHBOARD (PORTAL) ---
@bp.route('/developer-portal')
def developer_portal():
    if session.get('user_role') != 'developer':
        return redirect(url_for('module1.login_ui'))
    
    db = get_db()
    
    # Sidebar: Project List
    cur_projects = db.execute("""
        SELECT project_name, 
               COUNT(*) as total_defects,
               SUM(CASE WHEN status != 'completed' THEN 1 ELSE 0 END) as active_count
        FROM defects 
        GROUP BY project_name
    """)
    projects_raw = cur_projects.fetchall()
    
    # Selected Project Logic
    selected_project = request.args.get('project_name')
    if not selected_project and projects_raw:
        selected_project = projects_raw[0]['project_name'] 
    
    # Main Table: Defects List
    if selected_project:
        cur_defects = db.execute("SELECT * FROM defects WHERE status != 'draft' AND project_name = ?", (selected_project,))
    else:
        cur_defects = db.execute("SELECT * FROM defects WHERE status != 'draft'")
        
    defects = cur_defects.fetchall()

    # Stats
    stats = {
        'new': sum(1 for d in defects if d['status'] == 'locked'),
        'in_progress': sum(1 for d in defects if d['status'] == 'in_progress'),
        'completed': sum(1 for d in defects if d['status'] == 'completed'),
        'current_project': selected_project
    }
    
    # Process & Sort by Severity
    processed_defects = []
    for d in defects:
        d_dict = dict(d)
        d_dict['severity'] = estimate_severity(d['description'])
        if "Uploaded: " in d['description']:
            d_dict['filename'] = d['description'].split("Uploaded: ")[1]
        else:
            d_dict['filename'] = 'sisiranRendered.glb'
        processed_defects.append(d_dict)

    severity_order = {'High': 0, 'Medium': 1, 'Low': 2}
    processed_defects.sort(key=lambda x: severity_order.get(x['severity'], 3))

    return render_template('developer_portal.html', 
                           user=session.get('user_name'), 
                           projects=projects_raw,
                           defects=processed_defects, 
                           stats=stats)

# 6. Update Status Route
@bp.route('/update_status/<int:id>/<string:new_status>')
def update_status(id, new_status):
    if session.get('user_role') != 'developer':
        return redirect(url_for('module1.login_ui'))
        
    db = get_db()
    cur = db.execute("SELECT project_name FROM defects WHERE id = ?", (id,))
    row = cur.fetchone()
    project_name = row['project_name'] if row else None
    
    db.execute("UPDATE defects SET status = ? WHERE id = ?", (new_status, id))
    db.commit()
    
    if project_name:
        return redirect(url_for('module1.developer_portal', project_name=project_name))
    return redirect(url_for('module1.developer_portal'))

# Legacy Route redirect
@bp.route('/projects')
def my_projects():
    return redirect(url_for('module1.developer_portal'))