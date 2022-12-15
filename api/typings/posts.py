from enum import Enum
from typing import Optional


class Post(object):
    id: int = ...
    owner_id: int = ...
    content: str = ...
    create_time: int = ...
    update_time: Optional[int] = ...

    def __init__(
        self,
        id: int,
        owner_id: int,
        content: str,
        create_time: int,
        update_time: Optional[int],
    ):
        self.id = id
        self.owner_id = owner_id
        self.content = content
        self.create_time = create_time
        self.update_time = update_time


class PostCreateRequest(object):
    owner_id: int = ...
    content: str = ...

    def __init__(
        self,
        owner_id: int,
        content: str,
    ):
        self.owner_id = owner_id
        self.content = content


class PostCreateResult(object):
    post: Post = ...

    def __init__(self, post: Post):
        self.post = post


class PostAttachment(object):
    id: int = ...
    post_id: int = ...
    file_id: int = ...
    create_time: int = ...

    def __init__(self, id: int, post_id: int, file_id: int, create_time: int):
        self.id = id
        self.post_id = post_id
        self.file_id = file_id
        self.create_time = create_time


class PostAttachmentsCreateRequest(object):
    post_id: int = ...
    file_ids: tuple[int] = ...

    def __init__(self, post_id: int, file_ids: tuple[int]):
        self.post_id = post_id
        self.file_ids = file_ids


class PostAttachmentsCreateResult(object):
    post_attachments: tuple[PostAttachment]

    def __init__(self, post_attachments: tuple[PostAttachment]) -> None:
        self.post_attachments = post_attachments
