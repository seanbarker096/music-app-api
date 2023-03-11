from typing import List, Optional


class Artist:
    id: int = ...
    uuid: str = ...
    name: str = ...
    create_time: float = ...
    biography: Optional[str] = ...
    update_time: Optional[float] = ...
    owner_id: Optional[int] = ...
    image_url: Optional[str] = ...

    def __init__(
        self,
        id: int,
        uuid: str,
        name: str,
        create_time: float,
        biography: Optional[str] = None,
        update_time: Optional[float] = None,
        owner_id: Optional[int] = None,
        image_url: Optional[str] = None,
    ) -> None:
        self.id = id
        self.uuid = uuid
        self.name = name
        self.create_time = create_time
        self.biography = biography
        self.update_time = update_time
        self.owner_id = owner_id
        self.image_url = image_url


class ArtistSearchArtist:
    uuid: str = ...
    name: str = ...
    image_url: Optional[str] = ...

    def __init__(self, uuid: str, name: str, image_url: Optional[str] = None) -> None:
        self.uuid = uuid
        self.name = name
        self.image_url = image_url


class ArtistsGetFilter:
    ids: Optional[List[int]] = ...
    uuids: Optional[List[int]] = ...

    def __init__(self, ids: Optional[List[int]] = None, uuids: Optional[List[int]] = None) -> None:
        self.uuids = uuids
        self.ids = ids


class ArtistsGetResult:
    artists: List[Artist] = ...

    def __init__(self, artists: List[Artist]) -> None:
        self.artists = artists


class ArtistCreateRequest:
    name: str = ...
    uuid: str = ...
    biography: Optional[str] = ...
    owner_id: Optional[int] = ...
    image_url: Optional[str] = ...

    def __init__(
        self,
        name: str,
        uuid: str,
        biography: Optional[str] = None,
        owner_id: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> None:
        self.name = name
        self.uuid = uuid
        self.biography = biography
        self.owner_id = owner_id
        self.image_url = image_url


class ArtistCreateResult:
    artist: Artist = ...

    def __init__(self, artist: Artist) -> None:
        self.artist = artist
