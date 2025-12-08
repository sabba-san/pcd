from flask import Blueprint, render_template, request, redirect, url_for, session

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
# app/module1/routes.py

@bp.route('/admin')
def admin_dashboard():
    # 1. Security Check
    if session.get('user_role') != 'admin':
        return redirect(url_for('module1.login_ui'))
        
    # 2. Render the page WITH the Admin Name
    # (This 'user' variable tells base.html what to show in the top right)
    return render_template('admin_preview.html', user="System Administrator")