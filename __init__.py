from flask import Flask
from flask_migrate import Migrate
from .db import db
from .models import *
from dotenv import load_dotenv
import os
from flask_cors import CORS

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173", "http://127.0.0.1:5173"])  # Allow both frontend origins
    db_url = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'postgresql://username:password@localhost:5432/drivingschool'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    from .routes.users import users_bp
    from .routes.students import students_bp
    from .routes.sessions import sessions_bp
    from .routes.instructors import instructors_bp
    from .routes.activity_log import activity_log_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(students_bp, url_prefix='/students')
    app.register_blueprint(sessions_bp, url_prefix='/sessions')
    app.register_blueprint(instructors_bp, url_prefix='/instructors')
    app.register_blueprint(activity_log_bp, url_prefix='/activity_log')

    return app 