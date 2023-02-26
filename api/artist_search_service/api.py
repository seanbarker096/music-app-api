import json
from typing import Optional

from api.artist_search_service.search_client.search_imp import SearchImp
from api.artist_search_service.search_client.spotify_search_imp import SpotifySearchImp
from api.artist_search_service.types import (
    ArtistSearchArtist,
    ArtistsSearchRequest,
    ArtistsSearchResult,
)
from exceptions.exceptions import AppSearchServiceException


class ArtistSearchService:
    def __init__(self, config, search_imp: Optional[SearchImp] = None):
        self.config = config

        if not search_imp:
            implementation_type = self.config["config_file"]["artist-search-service"].get(
                "search-client", "spotify"
            )

            match implementation_type:
                case "spotify":
                    self.search_imp = SpotifySearchImp(config)

        else:
            self.search_imp = search_imp

    def search(self, request: ArtistsSearchRequest) -> ArtistsSearchResult:
        try:
            processed_request = self.search_imp.process_request(request)

            raw_result = self.search_imp.search(processed_request)

            return self.search_imp.build_search_result(raw_result)

        except Exception as err:
            raise AppSearchServiceException(
                f"Failed to fetch artists from spotfy api because {json.dumps(str(err))}"
            )

    def get_artist_by_uuid(self, uuid: str) -> ArtistSearchArtist:
        try:
            if not isinstance(uuid, str) or not uuid:
                raise AppSearchServiceException(f"Invalid uuid provided: {uuid}")

            if self.search_imp.client != "spotify":
                raise AppSearchServiceException(
                    "get_artist_by_uuid is only supported for spotify search inmplementation"
                )

            return self.search_imp.get_artist_by_uuid(uuid)

        except Exception as err:
            raise AppSearchServiceException(
                f"Failed to get artist by uuid from spotfy api because {json.dumps(str(err))}"
            )
