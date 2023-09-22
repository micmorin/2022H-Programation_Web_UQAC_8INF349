from flask_migrate import Migrate
from main.app_init.database import db

migrate = Migrate()

def init_app(app):
    migrate.init_app(app, db)