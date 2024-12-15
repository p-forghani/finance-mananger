from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate(db)
login = LoginManager()


def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'users.login'
    global sendgrid

    # Register blueprints
    from app.routes.expenses import expense_bp as expenses_blueprint
    from app.routes.users import users_bp as users_blueprint
    app.register_blueprint(expenses_blueprint)
    app.register_blueprint(users_blueprint)

    # Import models (ensures they are registered with SQLAlchemy)
    with app.app_context():
        from app import models  # noqa

    return app
