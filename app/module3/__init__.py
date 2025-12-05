# from flask import Flask

# def create_app():
#     app = Flask(__name__)

#     # --- 1. Register Module 1 (Login) ---
#     from app.module1.routes import bp as module1_bp
#     app.register_blueprint(module1_bp)

#     # --- 2. Register Module 2 (Chatbot) ---
#     from app.module2.routes import bp as module2_bp
#     app.register_blueprint(module2_bp)

#     # --- 3. Register Module 3 (Defect Form) --- <--- THIS WAS LIKELY MISSING
#     from app.module3.routes import bp as module3_bp
#     app.register_blueprint(module3_bp)

#     # --- 4. Register Module 4 (If you have it) ---
#     # from app.module4.routes import bp as module4_bp
#     # app.register_blueprint(module4_bp)

#     return app