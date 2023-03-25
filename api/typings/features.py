from enum import Enum
from typing import List, Optional


class FeaturerType(Enum):
    USER = "user"
    PERFORMER = "performer"


class FeaturedEntityType(Enum):
    POST = "post"


class Feature:
    id: int = ...
    featured_entity_type: FeaturedEntityType = ...  # The object that has been featured. E.g. a post
    featured_entity_id: int = ...
    featurer_type: FeaturerType  # The object which has featured the featured entity. E.g. a performer, or a user
    featurer_id: int
    creator_id: int  # The auth user who created the feature object

    def __init__(
        self,
        id: int,
        featured_entity_type: FeaturedEntityType,
        featured_entity_id: int,
        featurer_type: FeaturerType,
        featurer_id: int,
        creator_id: int,
    ):
        self.id = id
        self.featured_entity_type = featured_entity_type
        self.featured_entity_id = featured_entity_id
        self.featurer_type = featurer_type
        self.featurer_id = featurer_id
        self.creator_id = creator_id


class FeaturesGetFilter:
    featured_entity_type: Optional[FeaturedEntityType] = ...
    featured_entity_id: Optional[int] = ...
    featurer_type: Optional[FeaturerType] = ...
    featurer_id: Optional[int] = ...

    def __init__(
        self,
        featured_entity_type: Optional[str] = None,
        featured_entity_id: Optional[int] = None,
        featurer_type: Optional[str] = None,
        featurer_id: Optional[int] = None,
    ):
        self.featured_entity_type = featured_entity_type
        self.featured_entity_id = featured_entity_id
        self.featurer_type = featurer_type
        self.featurer_id = featurer_id


class FeaturesGetResult:
    features: List[Feature] = ...

    def __init__(self, features: List[Feature]) -> None:
        self.features = features


class FeatureCreateRequest:
    featured_entity_type: FeaturedEntityType = ...
    featured_entity_id: int = ...
    featurer_type: FeaturerType = ...
    featurer_id: int = ...
    creator_id: int = ...

    def __init__(
        self,
        featured_entity_type: str,
        featured_entity_id: int,
        featurer_type: str,
        featurer_id: int,
        creator_id: int,
    ):
        self.featured_entity_type = featured_entity_type
        self.featured_entity_id = featured_entity_id
        self.featurer_type = featurer_type
        self.featurer_id = featurer_id
        self.creator_id = creator_id


class FeatureCreateResult:
    feature: Feature = ...

    def __init__(self, feature: Feature) -> None:
        self.feature = feature
