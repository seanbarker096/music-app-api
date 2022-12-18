import time
from typing import Optional


class PostAttachmentFixtureDTO:
    def __init__(self, post_id: int, file_id: int, create_time: Optional[int]) -> None:
        self._post_id = post_id
        self._file_id = file_id
        self._create_time = create_time if create_time else time.time()

    def get_post_id(self) -> int:
        return self._post_id

    def get_file_id(self) -> int:
        return self._file_id

    def get_create_time(self) -> int:
        return self._create_time
