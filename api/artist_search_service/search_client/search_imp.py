from typing import List

from api.artist_search_service.types import ArtistSearchRequest


class SearchImp:
    def __init__(self, config):
        self.config = config

    def search(self, query: str) -> List[Artist]:
        raise NotImplementedError

    def process_request(self, request: ArtistSearchRequest) -> List[Artist]:
        ...
