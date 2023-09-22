# APPLICATION FACTORY

from flask import Flask
from main.app_init import apparence, database, migration, login
from main.blueprints.bp_default import bp_default
from main.blueprints.bp_users import bp_users
from main.blueprints.bp_posts import bp_posts
from main.blueprints.bp_comment import bp_comments
from main.blueprints.bp_reaction import bp_reaction
from main.blueprints.bp_admin import bp_admin
from main.blueprints.bp_balise import bp_balise
from main.blueprints.bp_API import bp_api_post

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    apparence.init_app(app)
    database.init_app(app)
    migration.init_app(app)
    login.init_app(app)

    app.register_blueprint(bp_default)
    app.register_blueprint(bp_posts)
    app.register_blueprint(bp_users)
    app.register_blueprint(bp_comments)
    app.register_blueprint(bp_reaction)
    app.register_blueprint(bp_admin)
    app.register_blueprint(bp_balise)
    app.register_blueprint(bp_api_post)

    return app