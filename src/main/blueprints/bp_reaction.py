from flask import Blueprint
from main.controllers import react_cont

bp_reaction = Blueprint('reactions', __name__)

bp_reaction.route('/posts/<int:post_id>/reaction/<int:react_id>',       methods=['GET'])           (react_cont.toggle)
bp_reaction.route('/admin/reaction/create',                             methods=['POST'])          (react_cont.create)
bp_reaction.route('/admin/reaction/<int:reaction_id>/edit',             methods=['POST'])          (react_cont.update)
bp_reaction.route('/admin/reaction/<int:reaction_id>',                  methods=['POST'])          (react_cont.destroy)