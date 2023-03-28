from typing import Dict, List, Optional


class Performer:
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


class PerformerSearchPerformer:
    uuid: str = ...
    name: str = ...
    image_url: Optional[str] = ...

    def __init__(self, uuid: str, name: str, image_url: Optional[str] = None) -> None:
        self.uuid = uuid
        self.name = name
        self.image_url = image_url

 
class PerformersGetFilter:
    ids: Optional[List[int]] = ...
    uuids: Optional[List[int]] = ...

    def __init__(self, ids: Optional[List[int]] = None, uuids: Optional[List[int]] = None) -> None:
        self.uuids = uuids
        self.ids = ids


class PerformersGetResult:
    performers: List[Performer] = ...

    def __init__(self, performers: List[Performer]) -> None:
        self.performers = performers


class PerformerCreateRequest:
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


class PerformerCreateResult:
    performer: Performer = ...

    def __init__(self, performer: Performer) -> None:
        self.performer = performer

class AttendeePerformersGetFilter:
    attendee_id: int = ...
    get_counts: bool = ...
    limit: int = ...

    def __init__(self, attendee_id: int, get_counts: bool = False, limit: int = 10) -> None:
        self.attendee_id = attendee_id
        self.get_counts = get_counts
        self.limit = limit


class AttendeePerformersGetCount:
    performer_id: int = ...
    count: int = ...
    attendee_id: int = ...

    def __init__(self, performer_id: int, count: int, attendee_id: int) -> None:
        self.performer_id = performer_id
        self.count = count
        self.attendee_id = attendee_id

class AttendeePerformersGetResult:
    performers: List[Performer] = ...
    counts: Optional[List[AttendeePerformersGetCount]] = ...

    def __init__(self, performers: List[Performer], counts: List[AttendeePerformersGetCount] = None) -> None:
        self.performers = performers
        self.counts = counts