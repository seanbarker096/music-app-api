import json
import logging
from typing import Optional

from api.dao.tags_dao import TagsDAO
from api.events.tags.event_objects.tag_event import TagEventType
from api.events.tags.tag_event_subject import TagEventSubject
from api.midlayer import BaseMidlayerMixin
from api.midlayer.performances_mid import PerformancesMidlayerMixin
from api.typings.performances import PerformancesGetFilter
from api.typings.tags import (
    TagCreateRequest,
    TagCreateResult,
    TagDeleteRequest,
    TaggedEntityType,
    TaggedInEntityType,
    TagsGetFilter,
    TagsGetResult,
)
from api.utils.rest_utils import (
    process_bool_request_param,
    process_enum_request_param,
    process_int_request_param,
)
from exceptions.exceptions import InvalidArgumentException
from exceptions.response.exceptions import TagNotFoundException


class TagsMidlayerConnections:
    def __init__(self, config, tags_dao: Optional[TagsDAO] = None):
        self.tags_dao = tags_dao or TagsDAO(config)


class TagsMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional[TagsMidlayerConnections] = None, tag_event_subject: TagEventSubject = None, performances_mid: PerformancesMidlayerMixin = None,  **kwargs):
        self.tags_dao = conns.tags_dao if conns and conns.tags_dao else TagsDAO(config)
        self.tag_event_subject = tag_event_subject if tag_event_subject else TagEventSubject(
            config=config
        )
        self.performances_mid = performances_mid if performances_mid else PerformancesMidlayerMixin(config)

        ## Call the next mixins constructor
        super().__init__(config)

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
            if request.tagged_in_entity_type == TaggedInEntityType.POST.value and request.tagged_entity_type == TaggedEntityType.PERFORMANCE.value:
                # We only allow a performer to create a single unique tag between one of their performances and a post.We therefore delete any existing tags between the post and the performer's performances. To avoid deleting a tag and recreating the exact one, first check to see if the tag in the create request exists already. If it does, do not delete and recreate it. We just return the existing tag.
                tags_get_filter = TagsGetFilter(
                    tagged_in_entity_type=request.tagged_in_entity_type,
                    tagged_in_entity_id=request.tagged_in_entity_id,
                    tagged_entity_type=request.tagged_entity_type,
                    tagged_entity_id=request.tagged_entity_id,
                )

                tags = self.tags_dao.tags_get(filter=tags_get_filter)

                if len(tags) == 1:
                    return TagCreateResult(tag=tags[0])

                if len(tags) > 1:
                    logging.warning(f"""More than one tag found between post with id {request.tagged_in_entity_id} and performance with id {request.tagged_entity_id}. These will be deleted.""")
                
                self._remove_existing_performer_performances_linked_to_post(request)
            
            created_tag = self.tags_dao.tag_create(request)

            # Notify observers
            self.tag_event_subject.publish_event(state=created_tag, event_type=TagEventType.CREATED.value)

            return TagCreateResult(tag=created_tag)

        except Exception as err:
            raise Exception(
                f"Failed to create tag because {json.dumps(str(err))}. Request: {json.dumps(vars(request))}"
            )
        
    def _remove_existing_performer_performances_linked_to_post(self, request: TagCreateRequest) -> None:
        """
        For a given performer, delete all tags between a specific post and any of their performances.
        """    
        # get the performance to get the performer
        performances_get_filter = PerformancesGetFilter(
            ids=[request.tagged_entity_id]
        )
        performances = self.performances_mid.performances_get(performances_get_filter).performances

        if len(performances) == 0:
            raise Exception(f"Failed to create tag between post with id {request.tagged_in_entity_id} and performance with id {request.tagged_entity_id} because the performance does not exist")
        
        performer_id = performances[0].performer_id

        return self.tags_dao.delete_performance_post_tags_by_performer_id(
            post_id=request.tagged_in_entity_id,
            performer_id=performer_id
        )

    def tags_get(self, request: TagsGetFilter) -> TagsGetResult:
        
        if request.ids and len(request.ids) == 0:
            raise InvalidArgumentException(
                f"Invalid argument ids. Must provide at least one id if providing this filter field. Request: {json.dumps(vars(request))}",
                "request.ids",
            )

        process_enum_request_param(parameter_name="tagged_entity_type", parameter=request.tagged_entity_type, enum=TaggedEntityType)
        process_int_request_param("tagged_entity_id", request.tagged_entity_id)
        process_enum_request_param(parameter_name="tagged_in_entity_type", parameter=request.tagged_in_entity_type, enum=TaggedInEntityType)
        process_int_request_param("tagged_in_entity_id", request.tagged_in_entity_id)
        process_bool_request_param(parameter_name="only_single_tagged_entity_type", parameter=request.only_single_tagged_entity_type)

        if not request.tagged_entity_id and not request.tagged_in_entity_id and not request.tagged_in_entity_type and not request.tagged_entity_type:
            raise InvalidArgumentException(
                f"Must provide at least one filter field. Request: {json.dumps(vars(request))}",
                "TagsGetFilter",
            )

        try:
            tags = self.tags_dao.tags_get(request)
            return TagsGetResult(tags=tags)

        except Exception as err:
            raise Exception(
                f"Failed to get tags because {json.dumps(str(err))}. Request: {json.dumps(vars(request))}"
            )

    def tags_delete(self, request: TagDeleteRequest) -> None:
        
        if not request.id:
            raise InvalidArgumentException(
                f"Must provide at least one tag id to delete. Request: {json.dumps(vars(request))}",
                "request.ids",
            )
        
        tag_id = request.id
        
        try:
            # CHeck if tag exists
            tags_get_filter = TagsGetFilter(
                ids=[request.id]
            )
            tags = self.tags_dao.tags_get(filter=tags_get_filter)

            if len(tags) == 0:
                raise TagNotFoundException(f"Failed to delete tags because no tags with id {tag_id} exists")
            
            tag = tags[0]
            
            self.tags_dao.tags_delete(request)   

        except Exception as err:
            raise Exception(
                f"Failed to delete tags because {json.dumps(str(err))}. Request: {json.dumps(vars(request))}"
            )

        # Notify observers
        self.tag_event_subject.publish_event(state=tag, event_type=TagEventType.DELETED.value)

        return
       