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
