from flask import Blueprint
from main.controllers import default_cont

bp_default = Blueprint('default',__name__, url_prefix="/")

bp_default.route("/")(default_cont.index)
bp_default.route("/login", methods=['GET', 'POST'])(default_cont.login)
bp_default.route("/logout")(default_cont.logout)