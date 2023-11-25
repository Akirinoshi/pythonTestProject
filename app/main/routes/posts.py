# Import required libraries and modules
from http import HTTPStatus

from flask import jsonify
from dependency_injector.wiring import Provide, inject
from flask_pydantic import validate
from flask import Blueprint

from app.common.utils.get_not_null_attrs import get_not_nullable_attrs
from app.common.utils.prepare_filters import prepare_filters
from app.main.models.post_likes import PostLikes
from app.main.models.posts import Post
from app.main.models.users import User
from app.main.repositories.post_repository import PostRepository
from app.main.schemas.posts import PostPutModel, PostCreateModel, PostQuery, PostAssessModel

post_bp = Blueprint("post", __name__, url_prefix="/api/post/")


@post_bp.route('/', methods=['GET'])
@validate()
@inject
def get_all_posts(query: PostQuery, user: User = Provide["user"]):
    value_filters = prepare_filters(
        model=Post, params=get_not_nullable_attrs(query.value_filters)
    )

    pageable_posts = PostRepository.get_all(
        per_page=query.pager.per_page,
        page=query.pager.page,
        sort=query.pager.sort,
        value_filters=value_filters,
    )

    if pageable_posts.total_pages < query.pager.page:
        return {
            "error": f"Page '{query.pager.page}' does not exist"
        }, HTTPStatus.NOT_FOUND

    return pageable_posts.to_dict()


@post_bp.route('/', methods=['POST'])
@validate()
@inject
def create_post(body: PostCreateModel, user: User = Provide["user"]):
    content = body.content

    post_id = Post(content=content, user_id=user.id).create()

    return jsonify(message='Success', post_id=post_id), 200


# Endpoint for updating a post
@post_bp.route('/<int:post_id>', methods=['PATCH'])
@inject
@validate()
def update_post(body: PostPutModel, post_id, user: User = Provide["user"]):
    post = Post.query.get(post_id)

    if not post:
        return jsonify(message='Post not found'), 404

    if post.user_id != user.id:
        return jsonify(message='Unauthorized to update this post'), 403

    post.content = body.content
    post.update()

    return jsonify(message='Post updated successfully'), 200


# Endpoint for deleting a post
@post_bp.route('/<int:post_id>', methods=['DELETE'])
@inject
def delete_post(post_id, user: User = Provide["user"]):
    post = Post.query.get(post_id)

    if not post:
        return jsonify(message='Post not found'), 404

    if post.user_id != user.id:
        return jsonify(message='Unauthorized to delete this post'), 403

    post.delete()

    return jsonify(message='Post deleted successfully'), 200


@post_bp.route('/assess/', methods=['POST'])
@validate()
@inject
def assess_post(body: PostAssessModel, user: User = Provide["user"]):
    post_id, like = body.post_id, body.like

    post = Post.query.get(post_id)

    if not post:
        return jsonify(message='Post not found'), 404

    posted_like = PostLikes.query.filter_by(user_id=user.id, post_id=post_id).first()

    if posted_like:
        if posted_like.like == like:
            return jsonify(message='Already assessed'), 200
        else:
            posted_like.like = like
            posted_like.update()
            return jsonify(message='Success'), 200
    else:
        PostLikes(user_id=user.id, post_id=post_id, like=like).create()
        return jsonify(message='Success'), 201
