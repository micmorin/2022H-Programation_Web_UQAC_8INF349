from flask import Blueprint
from main.controllers import API_cont

bp_api_post = Blueprint('api_post', __name__, url_prefix="/api/post")

bp_api_post.route('/',                             methods=['GET'])       (API_cont.all_posts)
bp_api_post.route('/<int:id>',                     methods=['GET'])       (API_cont.one_post)
bp_api_post.route('/',                             methods=['PUT'])       (API_cont.create_post)
bp_api_post.route('/',                             methods=['POST'])      (API_cont.update_post)
bp_api_post.route('/<int:id>',                     methods=['DELETE'])    (API_cont.destroy_post)