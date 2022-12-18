import time
from typing import Optional


class PostFixtureDTO(object):
    def __init__(
        self,
        owner_id: int,
        content: Optional[str] = "A test",
        create_time: Optional[int] = None,
        update_time: Optional[int] = None,
        is_deleted: Optional[bool] = False,
    ) -> None:
        self.content = content
        self.owner_id = owner_id
        self.create_time = create_time if create_time else time.time()
        self.update_time = update_time
        self.is_deleted = is_deleted

    def get_content(self) -> str:
        return self.content

    def get_owner_id(self) -> int:
        return self.owner_id

    def get_create_time(self) -> int:
        return self.create_time

    def get_update_time(self) -> Optional[int]:
        return self.update_time

    def is_deleted(self) -> Optional[bool]:
        return self.is_deleted
