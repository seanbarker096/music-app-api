from abc import ABC, abstractmethod
from typing import Any, Dict, List

from api.performer_search_service.types import PerformersSearchRequest
from api.typings.performers import Performer


class SearchImp(ABC):
    """Abstract class for performer search implementations."""

    @abstractmethod
    def search(self, request: PerformersSearchRequest) -> Dict[str, Any]:
        """Returns json encoded result"""
        ...

    @abstractmethod
    def process_request(self, request: PerformersSearchRequest) -> List[Performer]:
        ...

    @abstractmethod
    def build_search_result(self, raw_result: List[Performer]) -> List[Performer]:
        ...
