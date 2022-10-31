from typing import Optional


class Post(object):
    id: int = ...
    owner_id: int = ...
    content: str = ...
    create_time: int = ...
    update_time: Optional[int] = ...
    attachment_id: Optional[int] = ...

    def __init__(
        self,
        id: int,
        owner_id: int,
        content: str,
        create_time: int,
        update_time: Optional[int],
        attachment_id: Optional[int],
    ):
        self.id = id
        self.owner_id = owner_id
        self.content = content
        self.create_time = create_time
        self.update_time = update_time
        self.attachment_id = attachment_id


class PostCreateRequest(object):
    owner_id: int = ...
    content: str = ...
    attachment_id: Optional[int] = ...

    def __init__(self, owner_id: int, content: str, attachment_id: Optional[int]):
        self.owner_id = owner_id
        self.content = content
        self.attachment_id = attachment_id


class PostCreateResult(object):
    post: Post = ...

    def __init__(self, post: Post):
        self.post = post
