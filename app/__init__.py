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
    CORS(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
