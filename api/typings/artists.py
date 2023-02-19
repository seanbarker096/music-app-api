from typing import List, Optional


class Artist:
    id: int = ...
    uuid: str = ...
    name: str = ...
    create_time: str = ...
    biography: Optional[str] = ...
    updated_time: Optional[str] = ...
    owner_id: Optional[int] = ...

    def __init__(
        self,
        id: int,
        uuid: str,
        name: str,
        create_time: str,
        biography: Optional[str] = None,
        updated_time: Optional[str] = None,
        owner_id: Optional[int] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.name = name
        self.create_time = create_time
        self.biography = biography
        self.updated_time = updated_time
        self.owner_id = owner_id


class ArtistsGetFilter:
    uuids: Optional[List[int]] = ...

    def __init__(self, uuids: Optional[List[int]] = None) -> None:
        self.uuids = uuids
