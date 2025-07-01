from flask import Flask
from app.api.task_routes import task_bp
from app.api.ai_routes import ai_bp
from app.api.user_story_routes import user_story_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(task_bp)
    app.register_blueprint(ai_bp, url_prefix='/ai')
    app.register_blueprint(user_story_bp)
    return app 