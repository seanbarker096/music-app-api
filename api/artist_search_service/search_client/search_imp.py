from abc import ABC, abstractmethod
from typing import Any, Dict, List

from api.artist_search_service.types import ArtistSearchRequest
from api.typings.artists import Artist


class SearchImp(ABC):
    """Abstract class for artist search implementations."""

    @abstractmethod
    def search(self, request: ArtistSearchRequest) -> Dict[str, Any]:
        """Returns json encoded result"""
        ...

    @abstractmethod
    def process_request(self, request: ArtistSearchRequest) -> List[Artist]:
        ...

    @abstractmethod
    def build_search_result(self, raw_result: List[Artist]) -> List[Artist]:
        ...
