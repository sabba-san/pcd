from flask import Blueprint, render_template

# Define the blueprint as 'bp'
bp = Blueprint('module2', __name__)

@bp.route('/chat', methods=['GET'])
def chatbot_ui():
    # This looks for 'chatbot.html' inside app/templates/
    return render_template('chatbot.html')