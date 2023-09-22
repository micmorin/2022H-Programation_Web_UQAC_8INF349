from flask_login.login_manager import LoginManager

from main.models.md_user import User

lm = LoginManager()

def init_app(app):
    lm.init_app(app)
    lm.login_view = 'default.login'

    @lm.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
    