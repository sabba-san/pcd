from flask import Blueprint, render_template, request, redirect, url_for, session, g
import sqlite3
import os

# Define Blueprint
bp = Blueprint('module1', __name__)

# --- DATABASE CONNECTION CONFIG ---
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
# ----------------------------------

# 1. Login Page
@bp.route('/login', methods=['GET'])
def login_ui():
    return render_template('login.html')

# 2. Login Logic (Updated with New User)
@bp.route('/auth', methods=['POST'])
def login_auth():
    email = request.form.get('email')
    password = request.form.get('password')

    # ADMIN CHECK
    if email == 'admin@uum.edu.my' and password == 'admin123':
        session['user_role'] = 'admin'
        session['user_name'] = 'System Administrator'
        return redirect(url_for('module1.admin_dashboard'))
    
    # LAWYER CHECK
    elif email == 'lawyer@firm.com' and password == 'law123':
        session['user_role'] = 'lawyer'
        session['user_name'] = 'Pn. Zulaikha'
        return redirect(url_for('module1.lawyer_dashboard'))
    
    # HOUSING DEVELOPER CHECK
    elif email == 'developer@ecoworld.com' and password == 'dev123':
        session['user_role'] = 'developer'
        session['user_name'] = 'EcoWorld Contractor'
        return redirect(url_for('module1.developer_portal'))

    # --- NEW USER ADDED HERE ---
    elif email == 'abbas@student.uum.edu.my' and password == 'password123':
        session['user_role'] = 'user'
        session['user_name'] = 'Abbas (Student)'
        return redirect(url_for('module1.dashboard'))

    # DEFAULT FALLBACK (Any other login goes to Homeowner Dashboard)
    else:
        session['user_role'] = 'user'
        session['user_name'] = 'Abbas Abu Dzarr'
        return redirect(url_for('module1.dashboard'))

# 3. Homeowner Dashboard
@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=session.get('user_name'))

# 4. Admin Dashboard
@bp.route('/admin')
def admin_dashboard():
    return render_template('admin_preview.html', user="System Administrator")

# 5. Lawyer Dashboard (Connected to DB)
@bp.route('/lawyer_dashboard')
def lawyer_dashboard():
    db = get_db()
    # Get Real Defects from Database
    cur = db.execute('SELECT * FROM defects')
    real_cases = cur.fetchall()
    
    return render_template('module1/lawyer_dashboard.html', cases=real_cases, user="Pn. Zulaikha")

# 6. Developer Portal
@bp.route('/developer-portal')
def developer_portal():
    if session.get('user_role') != 'developer':
        return redirect(url_for('module1.login_ui'))
    return render_template('developer_portal.html', user=session.get('user_name'))

# 7. My Projects Route
@bp.route('/projects')
def my_projects():
    # Mock data for projects
    user_projects = [
        {
            "id": "40", "name": "ASMARINDA12", "date": "2025-12-14",
            "unit": "A-85", "address": "Sisiran Sintok 1b", "defects": 5,
            "status": "Processing", "filename": "rumah sisiran.glb" 
        },
        {
            "id": "38", "name": "SISIRAN 2", "date": "2025-12-10",
            "unit": "B-12", "address": "Taman Teja", "defects": 8,
            "status": "Completed", "filename": "rumah sisiran.glb"
        }
    ]
    return render_template('module1/projects.html', projects=user_projects)