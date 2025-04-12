from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')
    CORS(app, supports_credentials=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes.auth_routes import auth_bp
    from app.routes.twitter_routes import twitter_bp
    from app.routes.tiktok_routes import tiktok_bp
    from app.routes.youtube_routes import youtube_bp
    from app.routes.prompt_routes import prompt_bp
    from app.routes.user_routes import user_bp
    from app.routes.content_routes import content_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(twitter_bp)
    app.register_blueprint(tiktok_bp)
    app.register_blueprint(youtube_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(content_bp)
    return app
