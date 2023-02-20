from typing import Dict

from api.typings.artists import Artist


class ArtistSearchRequest:
    def __init__(self, search_terms: Dict[str, any], limit: int, offset: int):
        self.search_terms = search_terms
        self.limit = limit
        self.offset = offset


class ArtistSearchResult:
    def __init__(
        self, artists: list[Artist], total: int, offset: int, limit: int, next: str, previous: str
    ):
        self.artists = artists
        self.total = total
        self.offset = offset
        self.limit = limit
        self.next = next
        self.previous = previous
