from flask import Flask

# 1. Initialize the app globally (No create_app function)
app = Flask(__name__)

# 2. Register Module 1 (Login)
from app.module1.routes import bp as module1_bp
app.register_blueprint(module1_bp)

# 3. Register Module 2 (Chatbot)
from app.module2.routes import bp as module2_bp
app.register_blueprint(module2_bp)

# 4. Register Module 3 (Defect Form)
from app.module3.routes import bp as module3_bp
app.register_blueprint(module3_bp)