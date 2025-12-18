from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # REQUIRED for session to work (keeps users logged in)
    app.config['SECRET_KEY'] = 'dev_secret_key_123' 

    # 1. Register Login / Dashboard
    from app.module1.routes import bp as module1_bp
    app.register_blueprint(module1_bp)

    # 2. Register Old Chatbot (Optional - keep if you still have files in module2)
    from app.module2.routes import bp as module2_bp
    app.register_blueprint(module2_bp)

    # 3. Register Defect Form & 3D Viewer
    from app.module3.routes import bp as module3_bp
    app.register_blueprint(module3_bp)

    # 4. Register Legal Chatbot & Knowledge Base
    from app.module4.routes import bp as module4_bp
    app.register_blueprint(module4_bp)

    # Root Redirect: Send localhost:5001/ -> Login Page
    from flask import redirect, url_for
    @app.route('/')
    def index():
        # Redirects to the login logic in Module 1
        return redirect(url_for('module1.login_ui'))

    return app