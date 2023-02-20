from typing import Optional

from api.artist_search_service.search_client.api import SearchClient
from api.artist_search_service.types import ArtistSearchRequest, ArtistSearchResult


class ArtistSearchService:
    def __init__(self, config, search_client: Optional[SearchClient] = None):
        self.search_client = search_client if search_client else SearchClient(config)

    def artist_search(self, artistSearchRequest: ArtistSearchRequest) -> ArtistSearchResult:
        return self.search_client.search(artistSearchRequest)
