from typing import Optional

from api.artist_search_service.api import (
    ArtistSearchService,
    ArtistsSearchRequest,
    ArtistsSearchResult,
)
from api.dao.artists_dao import ArtistsDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.artists import (
    ArtistCreateRequest,
    ArtistCreateResult,
    ArtistsGetFilter,
    ArtistsGetResult,
)
from exceptions.exceptions import InvalidArgumentException


class ArtistsMidlayerConnections:
    def __init__(
        self,
        config,
        artists_dao: Optional[ArtistsDAO] = None,
        artist_search_service: Optional[ArtistSearchService] = None,
    ):
        self.artists_dao = artists_dao if artists_dao else ArtistsDAO(config)
        self.artist_search_service = (
            artist_search_service if artist_search_service else ArtistSearchService(config)
        )


class ArtistsMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional["MidlayerConnections"] = None, **kwargs):
        connnections = (
            conns.artist_mid_conns
            if conns and conns.artist_mid_conns
            else ArtistsMidlayerConnections(config)
        )
        self.artists_dao = connnections.artists_dao
        self.artist_search_service = connnections.artist_search_service

        ## Call the next mixins constructor
        super().__init__(config, conns)

    def artists_get(self, filter=ArtistsGetFilter) -> ArtistsGetResult:

        if filter.uuids and len(filter.uuids) == 0:
            raise InvalidArgumentException(
                "Invalid value provided for filter field uuids. At least one uuid must be provided",
                filter.uuids,
            )

        if not filter.uuids:
            raise InvalidArgumentException("Must provide at least one filter field", filter)

        artists = self.artists_dao.artists_get(filter)
        return ArtistsGetResult(artists=artists)

    def artist_search(self, searchQuery: str) -> ArtistsSearchResult:
        request = ArtistsSearchRequest(
            search_terms={"q": searchQuery},
        )

        return self.artist_search_service.search(request)

    def artist_create(self, request=ArtistCreateRequest) -> ArtistCreateResult:
        if not isinstance(request.name, str) or len(request.name) == 0:
            raise InvalidArgumentException(
                "Valid artist name must be provided when creating an artist", request.name
            )

        if not isinstance(request.uuid, str) or len(request.uuid) == 0:
            raise InvalidArgumentException(
                "Valid artist uuid must be provided when creating an artist", request.uuid
            )

        if request.owner_id and not isinstance(request.owner_id, int):
            raise InvalidArgumentException("Owner id must be a valid integer", request.owner_id)

        if request.biography and (
            not isinstance(request.biography, str) or len(request.biography) == 0
        ):
            raise InvalidArgumentException("Biography must be a valid string", request.biography)

        artist = self.artists_dao.artist_create(request)

        return ArtistCreateResult(artist=artist)

    def artist_get_or_create(self, uuid: str) -> ArtistsGetResult:
        artist = None
        filter = ArtistsGetFilter(uuids=[uuid])
        fetched_artists = self.artists_get(filter=filter).artists

        if len(fetched_artists) > 1:
            raise Exception(
                f"Failed to get_or_create artist for uuid {uuid}. More than one artist was found for this uuid"
            )

        ## If no artist found in our db, grab it from spotify and create it in our db
        if len(fetched_artists) == 0:
            search_artist = self.artist_search_service.get_artist_by_uuid(uuid)

            if search_artist.uuid != uuid:
                raise Exception(
                    "Search service returned artist with different uuid than requested. uuid requests: {uuid}, uuid returned: {search_artist.uuid}"
                )

            created_artist = self.artist_create(
                ArtistCreateRequest(
                    name=search_artist.name,
                    uuid=search_artist.uuid,
                    image_url=search_artist.image_url,
                )
            ).artist

            artist = created_artist
        else:
            artist = fetched_artists[0]

        return ArtistsGetResult(artists=[artist])
