import json
from typing import Optional

from api.dao.features_dao import FeaturesDAO
from api.midlayer import BaseMidlayerMixin
from api.typings.features import (
    FeatureContextType,
    FeatureCreateRequest,
    FeatureCreateResult,
    FeatureOwnerType,
    FeaturesGetFilter,
    FeaturesGetResult,
)
from exceptions.exceptions import InvalidArgumentException


class FeaturesMidlayerConnections:
    def __init__(self, config, features_dao: Optional[FeaturesDAO] = None):
        self.features_dao = features_dao if features_dao else FeaturesDAO(config)


class FeaturesMidlayerMixin(BaseMidlayerMixin):
    def __init__(self, config, conns: Optional["MidlayerConnections"] = None, **kwargs):
        connections = (
            conns.feature_mid_conns
            if conns and conns.feature_mid_conns
            else FeaturesMidlayerConnections(config)
        )
        self.features_dao = connections.features_dao

        ## Call the next mixins constructor
        super().__init__(config, conns)

    def features_get(self, filter=FeaturesGetFilter) -> FeaturesGetResult:

        if filter.context_id and not isinstance(filter.context_id, int):
            raise InvalidArgumentException("context_id must be a valid integer", filter.context_id)

        if filter.context_type and filter.context_type not in FeatureContextType:
            raise InvalidArgumentException(
                "Invalid value provided for filter field context_type", filter.context_type
            )

        if filter.owner_id and not isinstance(filter.owner_id, int):
            raise InvalidArgumentException("owner_id must be a valid integer", filter.owner_id)

        if filter.owner_type and filter.owner_type not in FeatureOwnerType:
            raise InvalidArgumentException(
                "Invalid value provided for filter field owner_type", filter.owner_type
            )

        features = self.features_dao.features_get(filter)

        return FeaturesGetResult(features=features)

    def feature_create(self, request: FeatureCreateRequest) -> FeatureCreateResult:
        if not request.context_id or not isinstance(request.context_id, int):
            raise InvalidArgumentException(
                f"Invalid context_id ({request.context_id}) provided",
                "request.context_id",
            )

        if not request.context_type or request.context_type not in set(
            item.value for item in FeatureContextType
        ):
            raise InvalidArgumentException(
                f"Invalid context_type ({request.context_type}) provided",
                "request.context_type",
            )

        if not request.owner_id or not isinstance(request.owner_id, int):
            raise InvalidArgumentException(
                f"Invalid owner_id ({request.owner_id}) provided",
                "request.owner_id",
            )

        if not request.owner_type or request.owner_type not in set(
            item.value for item in FeatureOwnerType
        ):
            raise InvalidArgumentException(
                f"Invalid owner_type ({request.owner_type}) provided",
                "request.owner_type",
            )

        try:
            feature = self.features_dao.feature_create(request)
            return FeatureCreateResult(feature=feature)

        except Exception as err:
            raise Exception(
                f"Failed to create Feature because {json.dumps(str(err))}. Request: {json.dumps(vars(request))}"
            )
