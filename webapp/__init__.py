from venv import create
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.db import db
from webapp.user.views import blueprint as user_blueprint
from webapp.user.models import User


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(user_blueprint)

    return app


app = create_app()
