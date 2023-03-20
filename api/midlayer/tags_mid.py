import json
from typing import Optional

from api.dao.tags_dao import TagsDAO
from api.events.tags.event_objects.tag_event import TagEventType
from api.events.tags.tag_event_subject import TagEventSubject
from api.midlayer import BaseMidlayerMixin
from api.typings.tags import (
    TagCreateRequest,
    TagCreateResult,
    TaggedEntityType,
    TaggedInEntityType,
    TagsGetFilter,
    TagsGetResult,
)
from exceptions.exceptions import InvalidArgumentException


class TagsMidlayerConnections:
    def __init__(self, config, tags_dao: Optional[TagsDAO] = None):
        self.tags_dao = tags_dao or TagsDAO(config)


class TagsMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional["MidlayerConnections"] = None, **kwargs):
        connections = (
            conns.tag_mid_conns
            if conns and conns.tag_mid_conns
            else TagsMidlayerConnections(config)
        )
        self.tags_dao = connections.tags_dao

        self.tag_event_subject = TagEventSubject(config=config)

        ## Call the next mixins constructor
        super().__init__(config, conns)

    # def tags_get(self, filter=TagsGetFilter) -> TagsGetResult:

    #     tags = self.tags_dao.tags_get(filter)

    #     return TagsGetResult(tags=tags)

    def tag_create(self, request: TagCreateRequest) -> TagCreateResult:
        if not isinstance(
            request.tagged_in_entity_type, str
        ) or request.tagged_in_entity_type not in set(item.value for item in TaggedInEntityType):
            raise InvalidArgumentException(
                f"Invalid argument tagged_in_entity_type. Request: {json.dumps(vars(request))}",
                "request.tagged_in_entity_type",
            )

        if not isinstance(request.tagged_in_entity_id, int) or not request.tagged_in_entity_id:
            raise InvalidArgumentException(
                f"Invalid argument tagged_in_entity_id. Request: {json.dumps(vars(request))}",
                "request.tagged_in_entity_id",
            )

        if not isinstance(request.tagged_entity_type, str) or request.tagged_entity_type not in set(
            item.value for item in TaggedEntityType
        ):
            raise InvalidArgumentException(
                f"Invalid argument tagged_entity_type. Request: {json.dumps(vars(request))}",
                "request.tagged_entity_type",
            )

        if not isinstance(request.tagged_entity_id, int) or not request.tagged_entity_id:
            raise InvalidArgumentException(
                f"Invalid argument tagged_entity_id. Request: {json.dumps(vars(request))}",
                "request.tagged_entity_id",
            )

        if not isinstance(request.creator_id, int) or not request.creator_id:
            raise InvalidArgumentException(
                f"Invalid argument creator_id. Request: {json.dumps(vars(request))}",
                "request.creator_id",
            )

        try:
            tag = self.tags_dao.tag_create(request)

            # Notify observers
            self.tag_event_subject.publish_event(state=tag, event_type=TagEventType.CREATED.value)

            return TagCreateResult(tag=tag)

        except Exception as err:
            raise Exception(
                f"Failed to create tag because {json.dumps(str(err))}. Request: {json.dumps(vars(request))}"
            )

    def tags_get(self, request: TagsGetFilter) -> TagsGetResult:

        if not request.tagged_entity_type or request.tagged_entity_type not in set(
            item.value for item in TaggedEntityType
        ):
            raise InvalidArgumentException(
                f"Invalid argument tagged_entity_type. Request: {json.dumps(vars(request))}",
                "request.tagged_entity_type",
            )

        if not request.tagged_entity_id or not isinstance(request.tagged_entity_id, int):
            raise InvalidArgumentException(
                f"Invalid argument tagged_entity_id. Request: {json.dumps(vars(request))}",
                "request.tagged_entity_id",
            )

        try:
            tags = self.tags_dao.tags_get(request)
            return TagsGetResult(tags=tags)

        except Exception as err:
            raise Exception(
                f"Failed to get tags because {json.dumps(str(err))}. Request: {json.dumps(vars(request))}"
            )
