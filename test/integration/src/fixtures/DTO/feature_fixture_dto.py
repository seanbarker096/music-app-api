from api.typings.features import FeaturedEntityType, FeaturerType


class FeatureFixtureDTO:
    def __init__(
        self,
        featured_entity_type: FeaturedEntityType,
        featured_entity_id: int,
        featurer_type: FeaturerType,
        featurer_id: int,
        creator_id: int,
    ):
        self.featured_entity_type = featured_entity_type
        self.featured_entity_id = featured_entity_id
        self.featurer_type = featurer_type
        self.featurer_id = featurer_id
        self.creator_id = creator_id

    def get_featured_entity_type(self) -> str:
        return self.featured_entity_type

    def get_featured_entity_id(self) -> int:
        return self.featured_entity_id

    def get_featurer_type(self) -> str:
        return self.featurer_type

    def get_featurer_id(self) -> int:
        return self.featurer_id

    def get_creator_id(self) -> int:
        return self.creator_id
