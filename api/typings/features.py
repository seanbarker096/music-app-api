from enum import Enum
from typing import List, Optional


class FeatureOwnerType(Enum):
    USER = "user"
    ARTIST = "artist"


class FeatureContextType(Enum):
    POST = "post"


class Feature:
    id: int = ...
    context_type: FeatureContextType = ...
    context_id: int = ...
    owner_type: FeatureOwnerType = ...
    owner_id: int = ...

    def __init__(
        self,
        id: int,
        context_type: str,
        context_id: int,
        owner_type: str,
        owner_id: int,
    ):
        self.id = id
        self.context_type = context_type
        self.context_id = context_id
        self.owner_type = owner_type
        self.owner_id = owner_id


class FeaturesGetFilter:
    context_type: Optional[FeatureContextType] = ...
    context_id: Optional[int] = ...
    owner_type: Optional[FeatureOwnerType] = ...
    owner_id: Optional[int] = ...

    def __init__(
        self,
        context_type: Optional[str] = None,
        context_id: Optional[int] = None,
        owner_type: Optional[str] = None,
        owner_id: Optional[int] = None,
    ):
        self.context_type = context_type
        self.context_id = context_id
        self.owner_type = owner_type
        self.owner_id = owner_id


class FeaturesGetResult:
    features: List[Feature] = ...

    def __init__(self, features: List[Feature]) -> None:
        self.features = features


class FeatureCreateRequest:
    context_type: FeatureContextType = ...
    context_id: int = ...
    owner_type: FeatureOwnerType = ...
    owner_id: int = ...

    def __init__(
        self,
        context_type: str,
        context_id: int,
        owner_type: str,
        owner_id: int,
    ):
        self.context_type = context_type
        self.context_id = context_id
        self.owner_type = owner_type
        self.owner_id = owner_id


class FeatureCreateResult:
    feature: Feature = ...

    def __init__(self, feature: Feature) -> None:
        self.feature = feature
