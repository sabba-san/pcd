from flask import Blueprint, render_template

# Define the blueprint as 'bp' so the dynamic loader finds it
bp = Blueprint('module1', __name__)

@bp.route('/login', methods=['GET'])
def login_ui():
    # This looks for 'login.html' inside app/templates/
    return render_template('login.html')

@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')