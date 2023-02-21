from abc import ABC, abstractmethod
from typing import List

from api.artist_search_service.types import ArtistSearchRequest


class SearchImp(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def search(self, request: ArtistSearchRequest) -> List[Artist]:
        ...

    @abstractmethod
    def process_request(self, request: ArtistSearchRequest) -> List[Artist]:
        ...

    @abstractmethod
    def build_searcg_result(self, raw_result: List[Artist]) -> List[Artist]:
        ...
