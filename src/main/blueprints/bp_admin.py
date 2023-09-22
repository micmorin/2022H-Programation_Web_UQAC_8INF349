from flask import Blueprint
from main.controllers import admin_cont

bp_admin = Blueprint('admin', __name__,url_prefix="/admin")

bp_admin.route('/',                             methods=['GET'])       (admin_cont.index)
bp_admin.route('/profil/create',                methods=['POST'])      (admin_cont.createProfil)
bp_admin.route('/profil/<int:profil_id>/edit',  methods=['POST'])      (admin_cont.updateProfil)
bp_admin.route('/profil/<int:profil_id>',       methods=['POST'])      (admin_cont.destroyProfil)