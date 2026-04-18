from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    from app.routes.agent import agent_bp
    app.register_blueprint(agent_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return {"status": "ok", "message": "ResearchAI Flask backend running"}
    
    return app