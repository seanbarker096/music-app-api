import json
from typing import Optional

from api.performer_search_service.search_client.search_imp import SearchImp
from api.performer_search_service.search_client.spotify_search_imp import (
    SpotifySearchImp,
)
from api.performer_search_service.types import (
    PerformerSearchPerformer,
    PerformersSearchRequest,
    PerformersSearchResult,
)
from exceptions.exceptions import AppSearchServiceException


class PerformerSearchService:
    def __init__(self, config, search_imp: Optional[SearchImp] = None):
        self.config = config

        if not search_imp:
            implementation_type = self.config["config_file"]["performer-search-service"].get(
                "search-client", "spotify"
            )

            match implementation_type:
                case "spotify":
                    self.search_imp = SpotifySearchImp(config)

        else:
            self.search_imp = search_imp

    def search(self, request: PerformersSearchRequest) -> PerformersSearchResult:
        try:
            processed_request = self.search_imp.process_request(request)

            raw_result = self.search_imp.search(processed_request)

            return self.search_imp.build_search_result(raw_result)

        except Exception as err:
            raise AppSearchServiceException(
                f"Failed to fetch performers from spotfy api because {json.dumps(str(err))}"
            )

    def get_performer_by_uuid(self, uuid: str) -> PerformerSearchPerformer:
        try:
            if not isinstance(uuid, str) or not uuid:
                raise AppSearchServiceException(f"Invalid uuid provided: {uuid}")

            if self.search_imp.client != "spotify":
                raise AppSearchServiceException(
                    "get_performer_by_uuid is only supported for spotify search inmplementation"
                )

            return self.search_imp.get_performer_by_uuid(uuid)

        except Exception as err:
            raise AppSearchServiceException(
                f"Failed to get performer by uuid from spotfy api because {json.dumps(str(err))}"
            )
