from flask import Blueprint
from main.controllers import comm_cont

bp_comments = Blueprint('comments', __name__)

bp_comments.route('/posts/<int:post_id>/comment',         methods=['POST'])       (comm_cont.create)
bp_comments.route('/posts/<int:post_id>/comment/edit',    methods=['POST'])       (comm_cont.update)
bp_comments.route('/posts/<int:post_id>/comment/delete',  methods=['POST'])       (comm_cont.destroy)