import json
from typing import Dict, List, Optional

from api.dao.features_dao import FeaturesDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.features import (
    Feature,
    FeatureCreateRequest,
    FeatureCreateResult,
    FeaturedEntityType,
    FeaturerType,
    FeaturesDeleteRequest,
    FeaturesGetFilter,
    FeaturesGetResult,
)
from api.utils.rest_utils import (
    process_enum_request_param,
    process_enum_set_param,
    process_int_request_param,
)
from exceptions.exceptions import InvalidArgumentException


class FeaturesMidlayerConnections:
    def __init__(self, config, features_dao: Optional[FeaturesDAO] = None):
        self.features_dao = features_dao if features_dao else FeaturesDAO(config)


class FeaturesMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional[FeaturesMidlayerConnections] = None, **kwargs):
        self.features_dao = conns.features_dao if conns and conns.features_dao else FeaturesDAO(config)

        ## Call the next mixins constructor
        super().__init__(config)

    def features_get(self, filter=FeaturesGetFilter) -> FeaturesGetResult:
        if filter.featured_entity_id and not isinstance(filter.featured_entity_id, int):
            raise InvalidArgumentException(
                "featured_entity_id must be a valid integer", filter.featured_entity_id
            )

        if filter.featured_entity_type and filter.featured_entity_type not in set(
            item.value for item in FeaturedEntityType
        ):
            raise InvalidArgumentException(
                "Invalid value provided for filter field featured_entity_type",
                filter.featured_entity_type,
            )

        if filter.featurer_id and not isinstance(filter.featurer_id, int):
            raise InvalidArgumentException(
                "featurer_id must be a valid integer", filter.featurer_id
            )

        if filter.featurer_type and filter.featurer_type not in set(
            item.value for item in FeaturerType
        ):
            raise InvalidArgumentException(
                "Invalid value provided for filter field featurer_type", filter.featurer_type
            )

        features = self.features_dao.features_get(filter)

        return FeaturesGetResult(features=features)
    

    # Todo: Ideally we would just use the features_get above but this doesn't work yet for passing in lists of feature properties e.g a list of featured_entity_ids
    def get_features_for_featured_entitys(
            self, 
            featured_entity_ids: List[int],
            featured_entity_type: FeaturedEntityType,
            featurer_type: FeaturerType
            ) -> List[Feature]:
        
        if not featured_entity_ids or len(featured_entity_ids) == 0:
            raise InvalidArgumentException(
                f"Invalid value provided for featured_entity_ids: {featured_entity_ids}. At least one featured_entity_id must be provided",
                "featured_entity_ids",
            )
        
        process_enum_request_param(parameter_name="featured_entity_type", parameter=featured_entity_type, enum=FeaturedEntityType, optional=False)

        process_enum_request_param(parameter_name="featurer_type", parameter=featurer_type, enum=FeaturerType, optional=False)


        features = self.features_dao.get_features_for_featured_entity(
            featured_entity_ids=featured_entity_ids,
            featured_entity_type=featured_entity_type,
            featurer_type=featurer_type
        )   

        return features


    def get_featured_entity_feature_counts(
        self,
        featured_entity_ids: List[int], 
        featured_entity_type: FeaturedEntityType
    ) -> Dict[int, int]:
        if not featured_entity_ids or len(featured_entity_ids) == 0:
            raise InvalidArgumentException(
                f"Invalid value provided for featured_entity_ids: {featured_entity_ids}. At least one featured_entity_id must be provided",
                "featured_entity_ids",
            )
        
        process_enum_request_param(
            parameter_name="featured_entity_type", 
            parameter=featured_entity_type, 
            enum=FeaturedEntityType, 
            optional=False
        )
        
        feature_id_to_count_dict = self.features_dao.get_featured_entity_feature_counts(
            featured_entity_ids=featured_entity_ids, 
            featured_entity_type=featured_entity_type
        )

        return feature_id_to_count_dict
    
    def get_users_posts_features(self, post_owner_id: int, featurer_type: FeaturerType)-> FeaturesGetResult:
        
        process_int_request_param(parameter_name="post_owner_id", parameter=post_owner_id, optional=False)
        process_enum_request_param(parameter_name="featurer_type", parameter=featurer_type, enum=FeaturerType, optional=False)

        features = self.features_dao.get_users_posts_features(post_owner_id=post_owner_id, featurer_type=featurer_type)

        return FeaturesGetResult(features=features)

    def feature_create(self, request: FeatureCreateRequest) -> FeatureCreateResult:
        if not request.featured_entity_id or not isinstance(request.featured_entity_id, int):
            raise InvalidArgumentException(
                f"Invalid featured_entity_id ({request.featured_entity_id}) provided",
                "request.featured_entity_id",
            )

        if not request.featured_entity_type or request.featured_entity_type not in set(
            item.value for item in FeaturedEntityType
        ):
            raise InvalidArgumentException(
                f"Invalid featured_entity_type ({request.featured_entity_type}) provided",
                "request.featured_entity_type",
            )

        if not request.featurer_id or not isinstance(request.featurer_id, int):
            raise InvalidArgumentException(
                f"Invalid featurer_id ({request.featurer_id}) provided",
                "request.featurer_id",
            )

        if not request.featurer_type or request.featurer_type not in set(
            item.value for item in FeaturerType
        ):
            raise InvalidArgumentException(
                f"Invalid featurer_type ({request.featurer_type}) provided",
                "request.featurer_type",
            )

        if not request.creator_id or not isinstance(request.creator_id, int):
            raise InvalidArgumentException(
                f"Invalid creator_id ({request.creator_id}) provided",
                "request.creator_id",
            )

        try:
            feature = self.features_dao.feature_create(request)
            return FeatureCreateResult(feature=feature)

        except Exception as err:
            raise Exception(
                f"Failed to create Feature because {json.dumps(str(err))}. Request: {json.dumps(vars(request))}"
            )
        
    def features_delete(self, request: FeaturesDeleteRequest) -> None:
        if not request.ids or len(request.ids) == 0:
            raise InvalidArgumentException(
                f"Invalid value provided for ids: {request.ids}. At least one id must be provided",
                "request.ids",
            )
        
        return self.features_dao.features_delete(request)
