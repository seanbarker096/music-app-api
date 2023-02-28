from typing import Dict, List, Optional

from api.db.db import DB
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.features import Feature, FeatureCreateRequest, FeaturesGetFilter


class FeaturesDBAlias:
    FEATURE_ID = "feature_id"
    FEATURE_CONTEXT_TYPE = "feature_context_type"
    FEATURE_CONTEXT_ID = "feature_context_id"
    FEATURE_OWNER_TYPE = "feature_owner_type"
    FEATURE_OWNER_ID = "feature_owner_id"


class FeaturesDAO:
    db: DB

    FEATURE_SELECTS = [
        "id as " + FeaturesDBAlias.FEATURE_ID,
        "context_type as " + FeaturesDBAlias.FEATURE_CONTEXT_TYPE,
        "context_id as " + FeaturesDBAlias.FEATURE_CONTEXT_ID,
        "owner_type as " + FeaturesDBAlias.FEATURE_OWNER_TYPE,
        "owner_id as " + FeaturesDBAlias.FEATURE_OWNER_ID,
    ]

    def __init__(self, config, db: Optional[DB] = None):
        self.db = db if db else DB(config)

    def feature_create(self, request: FeatureCreateRequest) -> Feature:
        sql = """
            INSERT INTO feature(context_type, context_id, owner_type, owner_id)
            VALUES(%s, %s, %s, %s)
        """

        binds = (
            request.context_type,
            request.context_id,
            request.owner_type,
            request.owner_id,
        )

        db_result = self.db.run_query(sql, binds)

        feature_id = db_result.get_last_row_id()

        return Feature(
            id=feature_id,
            context_type=request.context_type,
            context_id=request.context_id,
            owner_type=request.owner_type,
            owner_id=request.owner_id,
        )

    def features_get(self, filter: FeaturesGetFilter) -> List[Feature]:
        selects = f"""
            SELECT {', '.join(self.FEATURE_SELECTS)} from feature
        """

        wheres = []
        binds = []

        if filter.context_id:
            wheres.append("context_id = %s")
            binds.append(int(filter.context_id))

        if filter.context_type:
            wheres.append("context_type = %s")
            binds.append(filter.context_type)

        if filter.owner_id:
            wheres.append("owner_id = %s")
            binds.append(int(filter.owner_id))

        if filter.owner_type:
            wheres.append("owner_type = %s")
            binds.append(filter.owner_type)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        db_result = self.db.run_query(sql, binds)

        rows = db_result.get_rows()

        features = []
        for row in rows:
            feature = self._build_feature_from_db_row(row)
            features.append(feature)

        return features

    def _build_feature_from_db_row(self, db_row: Dict[str, any]) -> Feature:

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_ID)
        feature_id = int(db_row[FeaturesDBAlias.FEATURE_ID])

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_CONTEXT_TYPE)
        feature_context_type = db_row[FeaturesDBAlias.FEATURE_CONTEXT_TYPE]

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_CONTEXT_ID)
        feature_context_id = int(db_row[FeaturesDBAlias.FEATURE_CONTEXT_ID])

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_OWNER_TYPE)
        feature_owner_type = db_row[FeaturesDBAlias.FEATURE_OWNER_TYPE]

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_OWNER_ID)
        feature_owner_id = int(db_row[FeaturesDBAlias.FEATURE_OWNER_ID])

        return Feature(
            id=feature_id,
            context_type=feature_context_type,
            context_id=feature_context_id,
            owner_type=feature_owner_type,
            owner_id=feature_owner_id,
        )
