from typing import Dict, Optional

from api.typings.performers import PerformerSearchPerformer


class PerformersSearchRequest:
    search_terms: Dict[str, any] = ...
    limit: Optional[int] = ...
    offset: Optional[int] = ...

    def __init__(
        self,
        search_terms: Dict[str, any],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        self.search_terms = search_terms
        self.limit = limit
        self.offset = offset


class PerformersSearchResult:
    performers: list[PerformerSearchPerformer] = ...
    total: int = ...
    offset: int = ...
    limit: int = ...
    next: Optional[str] = ...
    previous: Optional[str] = ...

    def __init__(
        self,
        performers: list[PerformerSearchPerformer],
        total: int,
        offset: int,
        limit: int,
        next: Optional[str] = None,
        previous: Optional[str] = None,
    ):
        self.performers = performers
        self.total = total
        self.offset = offset
        self.limit = limit
        self.next = next
        self.previous = previous
