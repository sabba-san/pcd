from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # REQUIRED for session to work
    app.config['SECRET_KEY'] = 'dev_secret_key_123' 

    # 1. Register Login
    from app.module1.routes import bp as module1_bp
    app.register_blueprint(module1_bp)

    # 2. Register Chatbot
    from app.module2.routes import bp as module2_bp
    app.register_blueprint(module2_bp)

    # 3. Register Defect Form
    from app.module3.routes import bp as module3_bp
    app.register_blueprint(module3_bp)

    return app