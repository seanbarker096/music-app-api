from typing import Dict, List, Optional

from api.db.db import DBConnectionManager
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.features import Feature, FeatureCreateRequest, FeaturesGetFilter


class FeaturesDBAlias:
    FEATURE_ID = "feature_id"
    FEATURE_FEATURED_ENTITY_TYPE = "feature_featured_entity_type"
    FEATURE_FEATURED_ENTITY_ID = "feature_featured_entity_id"
    FEATURE_FEATURER_TYPE = "feature_featurer_type"
    FEATURE_FEATURER_ID = "feature_featurer_id"
    FEATURE_CREATOR_ID = "feature_creator_id"


class FeaturesDAO:
    db: DBConnectionManager

    FEATURE_SELECTS = [
        "id as " + FeaturesDBAlias.FEATURE_ID,
        "featured_entity_type as " + FeaturesDBAlias.FEATURE_FEATURED_ENTITY_TYPE,
        "featured_entity_id as " + FeaturesDBAlias.FEATURE_FEATURED_ENTITY_ID,
        "featurer_type as " + FeaturesDBAlias.FEATURE_FEATURER_TYPE,
        "featurer_id as " + FeaturesDBAlias.FEATURE_FEATURER_ID,
        "creator_id as " + FeaturesDBAlias.FEATURE_CREATOR_ID,
    ]

    def __init__(self, config, db: Optional[DBConnectionManager] = None):
        self.db = db if db else DBConnectionManager(config)
        self.config = config

    def feature_create(self, request: FeatureCreateRequest) -> Feature:
        sql = """
            INSERT INTO feature(featured_entity_type, featured_entity_id, featurer_type, featurer_id, creator_id)
            VALUES(%s, %s, %s, %s, %s)
        """

        binds = (
            request.featured_entity_type,
            request.featured_entity_id,
            request.featurer_type,
            request.featurer_id,
            request.creator_id,
        )

        with self.db as cursor:
            cursor.execute(sql, binds)
            feature_id = cursor.lastrowid

        return Feature(
            id=feature_id,
            featured_entity_type=request.featured_entity_type,
            featured_entity_id=request.featured_entity_id,
            featurer_type=request.featurer_type,
            featurer_id=request.featurer_id,
            creator_id=request.creator_id,
        )

    def features_get(self, filter: FeaturesGetFilter) -> List[Feature]:
        selects = f"""
            SELECT {', '.join(self.FEATURE_SELECTS)} from feature
        """

        wheres = []
        binds = []

        if filter.featured_entity_id:
            wheres.append("featured_entity_id = %s")
            binds.append(int(filter.featured_entity_id))

        if filter.featured_entity_type:
            wheres.append("featured_entity_type = %s")
            binds.append(filter.featured_entity_type)

        if filter.featurer_id:
            wheres.append("featurer_id = %s")
            binds.append(int(filter.featurer_id))

        if filter.featurer_type:
            wheres.append("featurer_type = %s")
            binds.append(filter.featurer_type)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        with self.db as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        features = []
        for row in rows:
            feature = self._build_feature_from_db_row(row)
            features.append(feature)

        return features

    def _build_feature_from_db_row(self, db_row: Dict[str, any]) -> Feature:

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_ID)
        feature_id = int(db_row[FeaturesDBAlias.FEATURE_ID])

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_FEATURED_ENTITY_TYPE)
        feature_featured_entity_type = db_row[FeaturesDBAlias.FEATURE_FEATURED_ENTITY_TYPE]

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_FEATURED_ENTITY_ID)
        feature_featured_entity_id = int(db_row[FeaturesDBAlias.FEATURE_FEATURED_ENTITY_ID])

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_FEATURER_TYPE)
        feature_featurer_type = db_row[FeaturesDBAlias.FEATURE_FEATURER_TYPE]

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_FEATURER_ID)
        feature_featurer_id = int(db_row[FeaturesDBAlias.FEATURE_FEATURER_ID])

        assert_row_key_exists(db_row, FeaturesDBAlias.FEATURE_CREATOR_ID)
        feature_creator_id = int(db_row[FeaturesDBAlias.FEATURE_CREATOR_ID])

        return Feature(
            id=feature_id,
            featured_entity_type=feature_featured_entity_type,
            featured_entity_id=feature_featured_entity_id,
            featurer_type=feature_featurer_type,
            featurer_id=feature_featurer_id,
            creator_id=feature_creator_id,
        )
