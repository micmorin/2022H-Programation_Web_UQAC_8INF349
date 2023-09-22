from flask import Blueprint
from main.controllers import post_cont

bp_posts = Blueprint('posts', __name__,url_prefix="/posts")

bp_posts.route('/',                     methods=['GET'])        (post_cont.index)
bp_posts.route('/create',               methods=['GET'])        (post_cont.create)
bp_posts.route('/<int:status>/store',   methods=['POST'])       (post_cont.store)
bp_posts.route('/<int:post_id>',        methods=['GET'])        (post_cont.show)
bp_posts.route('/<int:post_id>/edit',   methods=['GET','POST']) (post_cont.update)
bp_posts.route('/<int:post_id>',        methods=['POST'])       (post_cont.destroy)