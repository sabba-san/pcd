from flask import Blueprint, render_template, request, redirect, url_for, session

# Use your original Blueprint definition (no prefix, as in your original code)
bp = Blueprint('module1', __name__)

# --- 1. Login Page Display ---
@bp.route('/login', methods=['GET'])
def login_ui():
    return render_template('login.html')

# --- 2. Login Logic (The Traffic Controller) ---
@bp.route('/auth', methods=['POST'])
def login_auth():
    # Get what the user typed
    email = request.form.get('email')
    password = request.form.get('password')

    # ADMIN CHECK
    if email == 'admin@uum.edu.my' and password == 'admin123':
        session['user_role'] = 'admin'
        session['user_name'] = 'System Administrator'
        return redirect(url_for('module1.admin_dashboard'))
    
    # 2. HOUSING DEVELOPER LOGIN
    elif email == 'developer@ecoworld.com' and password == 'dev123':
        session['user_role'] = 'developer'
        session['user_name'] = 'EcoWorld Contractor'
        return redirect(url_for('module1.developer_portal'))
    
    # 3. LAWYER CHECK (*** NEW ADDITION ***)
    elif email == 'lawyer@firm.com' and password == 'law123':
        session['user_role'] = 'lawyer'
        session['user_name'] = 'Pn. Zulaikha'
        return redirect(url_for('module1.lawyer_dashboard'))
    
    # NORMAL USER CHECK
    else:
        session['user_role'] = 'user'
        session['user_name'] = 'Abbas Abu Dzarr'
        return redirect(url_for('module1.dashboard'))

# --- 3. User Dashboard ---
@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=session.get('user_name'))

# --- 4. Admin Dashboard ---
@bp.route('/admin')
def admin_dashboard():
    # 1. Security Check
    if session.get('user_role') != 'admin':
        return redirect(url_for('module1.login_ui'))
        
    # 2. Render the page WITH the Admin Name
    return render_template('admin_preview.html', user="System Administrator")

# --- 5. Housing Developer Portal ---
@bp.route('/developer-portal')
def developer_portal():
    # Security: Only allow Developers
    if session.get('user_role') != 'developer':
        return redirect(url_for('module1.login_ui'))
    
    return render_template('developer_portal.html', user=session.get('user_name'))

# --- 6. My Projects Route (*** NEW ADDITION ***) ---
@bp.route('/projects')
def my_projects():
    # Dummy data to match your design
    user_projects = [
        {
            "id": "40",
            "name": "ASMARINDA12",
            "date": "2025-12-14",
            "unit": "A-85",
            "address": "Sisiran Sintok 1b, 06050 Changlun, Kedah",
            "defects": 5,
            "status": "Processing",
            "filename": "rumah sisiran.glb"  # Ensure this file is in app/static/uploads/
        },
        {
            "id": "39",
            "name": "Master Bedroom Leak",
            "date": "2025-12-13",
            "unit": "A-85",
            "address": "Sisiran Sintok 1b, 06050 Changlun, Kedah",
            "defects": 3,
            "status": "In Progress",
            "filename": "rumah sisiran.glb"
        },
        {
            "id": "38",
            "name": "SISIRAN 2",
            "date": "2025-12-10",
            "unit": "B-12",
            "address": "Taman Teja, 06010 Changlun, Kedah",
            "defects": 8,
            "status": "Completed",
            "filename": "rumah sisiran.glb"
        }
    ]
    
    return render_template('module1/projects.html', projects=user_projects)

# --- 7. LAWYER DASHBOARD ROUTE (*** NEW ADDITION ***) ---
@bp.route('/lawyer_dashboard')
def lawyer_dashboard():
    # Mock data for the lawyer's active cases
    urgent_cases = [
        {
            "id": "CASE-001", 
            "client": "Abbas Abu Dzarr", 
            "project": "ASMARINDA12",
            "issue": "Structural Wall Crack", 
            "severity": "High", 
            "status": "Pending Review",
            "filename": "rumah sisiran.glb" # Uses your existing demo file
        },
        {
            "id": "CASE-004", 
            "client": "Siti Aishah", 
            "project": "Unit A-85",
            "issue": "Roof Leakage", 
            "severity": "Medium", 
            "status": "Evidence Verified",
            "filename": "rumah sisiran.glb"
        }
    ]
    
    return render_template('module1/lawyer_dashboard.html', cases=urgent_cases)