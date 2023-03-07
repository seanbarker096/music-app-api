from api.typings.features import FeatureContextType, FeatureOwnerType


class FeatureFixtureDTO:
    def __init__(
        self,
        context_type: FeatureContextType,
        context_id: int,
        owner_type: FeatureOwnerType,
        owner_id: int,
    ):
        self.context_type = context_type
        self.context_id = context_id
        self.owner_type = owner_type
        self.owner_id = owner_id

    def get_context_type(self) -> str:
        return self.context_type

    def get_context_id(self) -> int:
        return self.context_id

    def get_owner_type(self) -> str:
        return self.owner_type

    def get_owner_id(self) -> int:
        return self.owner_id
