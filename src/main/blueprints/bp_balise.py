from flask import Blueprint
from main.controllers import balise_cont

bp_balise = Blueprint('balises', __name__,url_prefix="/balise")

bp_balise.route('/',                                            methods=['GET'])        (balise_cont.index)
bp_balise.route('/<int:post_id>/<string>/create',               methods=['GET'])        (balise_cont.create)
bp_balise.route('/<int:post_id>/<string>/updateMany',           methods=['GET'])        (balise_cont.updateMany)
bp_balise.route('/<int:balise_id>',                             methods=['GET'])        (balise_cont.show)
bp_balise.route('/<int:balise_id>/edit',                        methods=['POST'])       (balise_cont.update)
bp_balise.route('/<int:post_id>/update',                        methods=['GET'])        (balise_cont.destroyMany)
bp_balise.route('/<int:balise_id>',                             methods=['POST'])       (balise_cont.destroy)