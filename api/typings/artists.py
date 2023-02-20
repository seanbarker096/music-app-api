from typing import List, Optional


class Artist:
    id: int = ...
    uuid: str = ...
    name: str = ...
    create_time: float = ...
    biography: Optional[str] = ...
    updated_time: Optional[float] = ...
    owner_id: Optional[int] = ...

    def __init__(
        self,
        id: int,
        uuid: str,
        name: str,
        create_time: float,
        biography: Optional[str] = None,
        updated_time: Optional[float] = None,
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


class ArtistsGetResult:
    artists: List[Artist] = ...

    def __init__(self, artists: List[Artist]) -> None:
        self.artists = artists


class ArtistCreateRequest:
    name: str = ...
    uuid: str = ...
    biography: Optional[str] = ...
    owner_id: Optional[int] = ...

    def __init__(
        self, name: str, uuid: str, biography: Optional[str] = None, owner_id: Optional[str] = None
    ) -> None:
        self.name = name
        self.uuid = uuid
        self.biography = biography
        self.owner_id = owner_id


class ArtistCreateResult:
    artist: Artist = ...

    def __init__(self, artist: Artist) -> None:
        self.artist = artist
