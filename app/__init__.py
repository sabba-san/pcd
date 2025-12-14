from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # REQUIRED for session to work
    app.config['SECRET_KEY'] = 'dev_secret_key_123' 

    # 1. Register Login / Dashboard
    from app.module1.routes import bp as module1_bp
    app.register_blueprint(module1_bp)

    # 2. Register Old Chatbot (If you are replacing this, you can remove it later)
    from app.module2.routes import bp as module2_bp
    app.register_blueprint(module2_bp)

    # 3. Register Defect Form (Lidar)
    from app.module3.routes import bp as module3_bp
    app.register_blueprint(module3_bp)

    # --- 4. NEW: Register Legal Chatbot ---
    from app.module4.routes import bp as module4_bp
    app.register_blueprint(module4_bp)

    return app