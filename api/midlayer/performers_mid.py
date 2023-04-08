import json
from typing import Optional

from api.dao.performers_dao import PerformersDAO
from api.midlayer import BaseMidlayerMixin
from api.performer_search_service.api import (
    PerformerSearchService,
    PerformersSearchRequest,
    PerformersSearchResult,
)
from api.typings.performers import (
    AttendeePerformersGetFilter,
    AttendeePerformersGetResult,
    PerformerCreateRequest,
    PerformerCreateResult,
    PerformersGetFilter,
    PerformersGetResult,
)
from api.utils.rest_utils import process_bool_request_param, process_int_request_param
from exceptions.exceptions import InvalidArgumentException


class PerformersMidlayerConnections:
    def __init__(
        self,
        config,
        performers_dao: Optional[PerformersDAO] = None,
        performer_search_service: Optional[PerformerSearchService] = None,
    ):
        self.performers_dao = performers_dao if performers_dao else PerformersDAO(config)
        self.performer_search_service = (
            performer_search_service if performer_search_service else PerformerSearchService(config)
        )


class PerformersMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional[PerformersMidlayerConnections] = None, **kwargs):
        self.performers_dao = conns.performers_dao if conns and conns.performers_dao else PerformersDAO(config)
        self.performer_search_service = conns.performer_search_service if conns and conns.performer_search_service else PerformerSearchService(config)

        ## Call the next mixins constructor
        super().__init__(config)

    def performers_get(self, filter=PerformersGetFilter) -> PerformersGetResult:

        if filter.uuids and len(filter.uuids) == 0:
            raise InvalidArgumentException(
                "Invalid value provided for filter field uuids. At least one uuid must be provided",
                filter.uuids,
            )

        if not filter.uuids and not filter.ids:
            raise InvalidArgumentException(
                f"Must provide at least one filter field. Filter: {json.dumps(vars(filter))}",
                "filter",
            )

        performers = self.performers_dao.performers_get(filter)
        return PerformersGetResult(performers=performers)

    def performer_search(self, searchQuery: str) -> PerformersSearchResult:
        request = PerformersSearchRequest(
            search_terms={"q": searchQuery},
        )

        return self.performer_search_service.search(request)

    def performer_create(self, request=PerformerCreateRequest) -> PerformerCreateResult:
        if not isinstance(request.name, str) or len(request.name) == 0:
            raise InvalidArgumentException(
                "Valid performer name must be provided when creating an performer", request.name
            )

        if not isinstance(request.uuid, str) or len(request.uuid) == 0:
            raise InvalidArgumentException(
                "Valid performer uuid must be provided when creating an performer", request.uuid
            )

        if request.owner_id and not isinstance(request.owner_id, int):
            raise InvalidArgumentException("Owner id must be a valid integer", request.owner_id)

        if request.biography and (
            not isinstance(request.biography, str) or len(request.biography) == 0
        ):
            raise InvalidArgumentException("Biography must be a valid string", request.biography)

        try:
            performer = self.performers_dao.performer_create(request)
        except Exception as err:
            raise Exception(
                f"Failed to create performer because {json.dumps(str(err))}. Request: {json.dumps(vars(request))}"
            )

        return PerformerCreateResult(performer=performer)

    def performer_get_or_create(self, uuid: str) -> PerformersGetResult:
        performer = None
        filter = PerformersGetFilter(uuids=[uuid])
        fetched_performers = self.performers_get(filter=filter).performers

        if len(fetched_performers) > 1:
            raise Exception(
                f"Failed to get_or_create performer for uuid {uuid}. More than one performer was found for this uuid"
            )

        ## If no performer found in our db, grab it from spotify and create it in our db
        if len(fetched_performers) == 0:
            search_performer = self.performer_search_service.get_performer_by_uuid(uuid)

            if search_performer.uuid != uuid:
                raise Exception(
                    f"Search service returned performer with different uuid than requested. uuid requests: {uuid}, uuid returned: {search_performer.uuid}"
                )

            created_performer = self.performer_create(
                PerformerCreateRequest(
                    name=search_performer.name,
                    uuid=search_performer.uuid,
                    image_url=search_performer.image_url,
                )
            ).performer

            performer = created_performer
        else:
            performer = fetched_performers[0]

        return PerformersGetResult(performers=[performer])

    def attendee_performers_get(self, filter: AttendeePerformersGetFilter):
        process_int_request_param("attendee_id", filter.attendee_id, optional=False)
        process_bool_request_param("get_counts", filter.get_counts, optional=True)

        try:
            return self.performers_dao.attendee_performers_get(filter=filter)

        except Exception as e:
            raise Exception(
                f"Failed to get performances because {str(e)}. Filter: {json.dumps(vars(filter))}"
            )
