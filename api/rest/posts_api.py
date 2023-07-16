import json
from typing import List

import flask

from api.typings.features import FeaturedEntityType, FeaturerType
from api.typings.performers import PerformersGetFilter
from api.typings.posts import (
    FeaturedPostsGetFilter,
    Post,
    PostAttachmentFileMap,
    PostAttachmentsCreateRequest,
    PostAttachmentsGetFilter,
    PostCreateRequest,
    PostOwnerType,
    PostsGetFilter,
    ProfilePostsGetFilter,
    ProfileType,
)
from api.utils import rest_utils
from exceptions.response.exceptions import BadRequestException

blueprint = flask.Blueprint("posts", __name__)

auth = rest_utils.auth


@blueprint.route("/posts/", methods=["POST"])
@auth
def post_create():
    data = flask.request.json

    creator_id = int(flask.g.auth_user.user_id)

    post_create_request = PostCreateRequest(
        owner_id=data.get("owner_id", None),
        owner_type=data.get("owner_type", None),
        content=data.get("content", None),
        creator_id=creator_id,
        note=data.get("note", None),
    )

    post_result = flask.current_app.conns.midlayer.post_create(post_create_request)
    post = post_result.post

    attachment_files = data.get("attachment_files")

    attachment_dicts = []

    if attachment_files and len(attachment_files) > 0:
        maps = []

        for attachment_file in attachment_files:
            if not attachment_file.get('attachment_file_id'):
                raise BadRequestException(f"""Invalid request. Must provide a valid attachment_file_id for all attachment_files. Request: {json.dumps(attachment_files)}""", source='attachment_files')
            
            maps.append(
                PostAttachmentFileMap(
                    attachment_file_id=attachment_file.get('attachment_file_id'), 
                    thumbnail_file_id=attachment_file.get('thumbnail_file_id')
                )
            )


        attachment_create_request = PostAttachmentsCreateRequest(
                post_id=post.id, post_attachment_file_maps=maps
            )
        

        attachment_result = flask.current_app.conns.midlayer.post_attachments_create(
            attachment_create_request
        )

        for attachment in attachment_result.post_attachments:
            attachment_dicts.append(vars(attachment))

    response = {}
    response["post"] = vars(post_result.post)
    response["attachments"] = attachment_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/posts/<int:post_id>", methods=["GET"])
@auth
def post_get_by_id(post_id: int):

    if not post_id:
        raise Exception("Invalid request. Must provide a valid post_id")

    posts_get_filter = PostsGetFilter(ids=[post_id], is_deleted=False)

    posts_get_result = flask.current_app.conns.midlayer.posts_get(posts_get_filter)
    post = posts_get_result.posts[0]

    attachment_dicts = []
    if post:
        post_attachments_get_filter = PostAttachmentsGetFilter(post_ids=[post.id])

        post_attachments_get_result = flask.current_app.conns.midlayer.post_attachments_get(
            post_attachments_get_filter
        )

        attachments = post_attachments_get_result.post_attachments

        for attachment in attachments:
            attachment_dicts.append(rest_utils.class_to_dict(attachment))

    response = {}
    response["post"] = rest_utils.class_to_dict(post)
    response["attachments"] = attachment_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/posts/", methods=["GET"])
@auth
def posts_get():

    owner_ids = rest_utils.process_api_set_request_param("owner_ids[]", type=int)
    owner_types = rest_utils.process_enum_set_api_request_param("owner_types[]", PostOwnerType)

    ids = rest_utils.process_api_set_request_param("ids[]", type=int)

    limit = rest_utils.process_int_api_request_param("limit", optional=True)

    posts_get_filter = PostsGetFilter(
        owner_ids=owner_ids, owner_types=owner_types, ids=ids, is_deleted=False, limit=limit
    )

    posts_get_result = flask.current_app.conns.midlayer.posts_get(posts_get_filter)
    posts = posts_get_result.posts

    attachment_dicts = []
    if len(posts) > 0:
        posts, attachment_dicts = build_posts(posts)

    response = {}

    response["posts"] = [rest_utils.class_to_dict(post) for post in posts]

    response["attachments"] = attachment_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/featured/", methods=["GET"])
@auth
def featured_posts_get():
    owner_id = rest_utils.process_int_api_request_param("owner_id", optional=False)
    owner_type = rest_utils.process_enum_api_request_param(
        "owner_type", PostOwnerType, optional=False
    )
    
    is_featured_by_users = rest_utils.process_bool_api_request_param(
        "is_featured_by_users", optional=True
    )
    is_featured_by_performers = rest_utils.process_bool_api_request_param(
        "is_featured_by_performers", optional=True
    )

    if not is_featured_by_users and not is_featured_by_performers:
        raise Exception(
            "Invalid request. Must provide at least one of is_featured_by_users or is_featured_by_performers in request"
        )
    
    limit = rest_utils.process_int_api_request_param("limit", optional=True)

    featured_posts_get_filter = FeaturedPostsGetFilter(
        owner_id=owner_id, 
        owner_type=owner_type,
        is_featured_by_users=is_featured_by_users,
        is_featured_by_performers=is_featured_by_performers,
        limit=limit
    )

    featured_posts_get_result = flask.current_app.conns.midlayer.featured_posts_get(
        featured_posts_get_filter
    )

    posts = featured_posts_get_result.posts

    attachment_dicts = []
    if len(posts) > 0:
        posts, attachment_dicts = build_posts(posts)

    response = {}

    response["posts"] = [rest_utils.class_to_dict(post) for post in posts]

    response["attachments"] = attachment_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/attachments/", methods=["GET"])
@auth
def post_attachments_get():
    post_ids = rest_utils.process_api_set_request_param("post_ids[]", type=int)

    post_attachments_get_filter = PostAttachmentsGetFilter(post_ids=post_ids)

    post_attachments_get_result = flask.current_app.conns.midlayer.post_attachments_get(
        post_attachments_get_filter
    )

    attachments = post_attachments_get_result.post_attachments

    attachment_dicts = [rest_utils.class_to_dict(attachment) for attachment in attachments]

    response = {}
    response["attachments"] = attachment_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


@blueprint.route("/profiles/<string:profile_id>/posts", methods=["GET"])
@auth
def get_profiles_posts(profile_id: str):
    """Get all posts for a user. This includes posts they created, posts they are tagged in and posts they have featured in their profile (depending on the filters applied)."""

    # Because profile_id is in the middle of the url, it is a string. We need to convert it to an int
    profile_id = int(profile_id)

    include_tagged = rest_utils.process_bool_api_request_param("include_tagged")
    include_owned = rest_utils.process_bool_api_request_param("include_owned")
    include_featured = rest_utils.process_bool_api_request_param("include_featured")
    profile_type = rest_utils.process_enum_api_request_param("profile_type", ProfileType)

    offset = rest_utils.process_int_api_request_param("offset", optional=True)
    limit = rest_utils.process_int_api_request_param("limit", optional=True)

    profile_posts_get_filter = ProfilePostsGetFilter(
        profile_id=profile_id,
        profile_type=profile_type,
        include_tagged=include_tagged,
        include_owned=include_owned,
        include_featured=include_featured,
        offset=offset,
        limit=limit,
    )

    posts = flask.current_app.conns.midlayer.profile_posts_get(profile_posts_get_filter).posts

    attachment_dicts = []
    if len(posts) > 0:
        posts, attachment_dicts = build_posts(posts)

    response = {}
    response["posts"] = [rest_utils.class_to_dict(post) for post in posts]
    response["attachments"] = attachment_dicts

    return flask.current_app.response_class(
        response=json.dumps(response), status=200, mimetype="application/json"
    )


def build_posts(posts: List[Post]):
    # Get all attachments for the posts
    post_ids = [post.id for post in posts]
    attachment_dicts = []
    post_attachments_get_filter = PostAttachmentsGetFilter(post_ids=post_ids)

    post_attachments_get_result = flask.current_app.conns.midlayer.post_attachments_get(
        post_attachments_get_filter
    )

    attachments = post_attachments_get_result.post_attachments

    attachment_dicts = [rest_utils.class_to_dict(attachment) for attachment in attachments]

    # Get total feature count for each post
    post_id_to_feature_count_dict = (
        flask.current_app.conns.midlayer.get_featured_entity_feature_counts(
            featured_entity_ids=post_ids,
            featured_entity_type=FeaturedEntityType.POST.value,
        )
    )

    # Get all featuring artists for the posts
    post_features = flask.current_app.conns.midlayer.get_features_for_featured_entitys(
        featured_entity_ids=post_ids,
        featured_entity_type=FeaturedEntityType.POST.value,
        featurer_type=FeaturerType.PERFORMER.value,
    )

    post_features_dict = {}
    artist_ids = []

    # We should only have one feature per post
    for post_feature in post_features:
        post_id = post_feature.featured_entity_id
        post_features_dict[post_id] = post_feature
        artist_ids.append(post_feature.featurer_id)

    # Get all artists for the posts
    artists = []
    if len(artist_ids) > 0:
        performers_get_filter = PerformersGetFilter(ids=artist_ids)
        artists = flask.current_app.conns.midlayer.performers_get(performers_get_filter).performers

    artists_by_id = {}
    for artist in artists:
        artists_by_id[artist.id] = artist

    for post in posts:
        post.featuring_performer = None

        artist_post_feature = post_features_dict.get(post.id, None)
        # Convert the artist to a dict
        if artist_post_feature:
            featuring_performer = artists_by_id.get(artist_post_feature.featurer_id, None)

            post.featuring_performer = (
                rest_utils.class_to_dict(featuring_performer) if featuring_performer else None
            )

        post.feature_count = post_id_to_feature_count_dict.get(post.id, 0)

    return posts, attachment_dicts
