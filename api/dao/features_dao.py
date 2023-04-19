from typing import Dict, List, Optional

from api.db.db import DBConnectionManager, FlaskDBConnectionManager
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.features import (
    Feature,
    FeatureCreateRequest,
    FeaturedEntityType,
    FeaturerType,
    FeaturesGetFilter,
)


class FeaturesDBAlias:
    FEATURE_ID = "feature_id"
    FEATURE_FEATURED_ENTITY_TYPE = "feature_featured_entity_type"
    FEATURE_FEATURED_ENTITY_ID = "feature_featured_entity_id"
    FEATURE_FEATURER_TYPE = "feature_featurer_type"
    FEATURE_FEATURER_ID = "feature_featurer_id"
    FEATURE_CREATOR_ID = "feature_creator_id"


class FeaturesDAO:
    db: DBConnectionManager

    FEATURE_COLUMNS = [
        "f.id",
        "f.featured_entity_type",
        "f.featured_entity_id",
        "f.featurer_type",
        "f.featurer_id",
        "f.creator_id",
    ]

    FEATURE_SELECTS = [
        f"{FEATURE_COLUMNS[0]} as {FeaturesDBAlias.FEATURE_ID}",
        f"{FEATURE_COLUMNS[1]} as {FeaturesDBAlias.FEATURE_FEATURED_ENTITY_TYPE}",
        f"{FEATURE_COLUMNS[2]} as {FeaturesDBAlias.FEATURE_FEATURED_ENTITY_ID}",
        f"{FEATURE_COLUMNS[3]} as {FeaturesDBAlias.FEATURE_FEATURER_TYPE}",
        f"{FEATURE_COLUMNS[4]} as {FeaturesDBAlias.FEATURE_FEATURER_ID}",
        f"{FEATURE_COLUMNS[5]} as {FeaturesDBAlias.FEATURE_CREATOR_ID}",
    ]

    def __init__(self, config, db: Optional[DBConnectionManager] = None):
        self.db = db if db else FlaskDBConnectionManager
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

        with self.db(self.config) as cursor:
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
            SELECT {', '.join(self.FEATURE_SELECTS)} from feature as f
        """

        wheres = []
        binds = []

        if filter.featured_entity_id:
            wheres.append("f.featured_entity_id = %s")
            binds.append(int(filter.featured_entity_id))

        if filter.featured_entity_type:
            wheres.append("f.featured_entity_type = %s")
            binds.append(filter.featured_entity_type)

        if filter.featurer_id:
            wheres.append("f.featurer_id = %s")
            binds.append(int(filter.featurer_id))

        if filter.featurer_type:
            wheres.append("f.featurer_type = %s")
            binds.append(filter.featurer_type)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        features = []
        for row in rows:
            feature = self._build_feature_from_db_row(row)
            features.append(feature)

        return features
    

    def get_features_for_featured_entity(
            self,
            featured_entity_ids: List[int],
            featured_entity_type: FeaturedEntityType,
            featurer_type: FeaturerType
            )-> List[Feature]:
        
        selects = f"""
            SELECT {', '.join(self.FEATURE_SELECTS)} from feature as f
            """
        
        wheres = []
        binds = []

        wheres.append("f.featured_entity_id IN %s")
        binds.append(featured_entity_ids)

        wheres.append("f.featured_entity_type = %s")
        binds.append(featured_entity_type)

        wheres.append("f.featurer_type = %s")
        binds.append(featurer_type)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        features = []
        for row in rows:
            feature = self._build_feature_from_db_row(row)
            features.append(feature)

        return features

    def get_featured_entity_feature_counts(self, featured_entity_ids: List[int], featured_entity_type: FeaturedEntityType) -> Dict[int, int]:
        selects = f"""
            SELECT f.featured_entity_id as {FeaturesDBAlias.FEATURE_FEATURED_ENTITY_ID}, count(*) as feature_count from feature as f
            """

        wheres = []
        binds = []

        wheres.append("f.featured_entity_id IN %s")
        binds.append(featured_entity_ids)

        wheres.append("f.featured_entity_type = %s")
        binds.append(featured_entity_type)

        where_string = build_where_query_string(wheres, "AND")

        sql = f"""
            {selects}
            {where_string}
            GROUP BY f.featured_entity_id
            """

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        featured_entity_feature_counts = {}
        for row in rows:
            assert_row_key_exists(row, FeaturesDBAlias.FEATURE_FEATURED_ENTITY_ID)
            featured_entity_id = int(row[FeaturesDBAlias.FEATURE_FEATURED_ENTITY_ID])
            count = row['feature_count']
            featured_entity_feature_counts[featured_entity_id] = count
            
        return featured_entity_feature_counts
    

    def get_users_posts_features(self, post_owner_id: int, featurer_type: FeaturerType) -> List[Feature]:
        selects = f"""
            SELECT {', '.join(self.FEATURE_SELECTS)} from feature as f
            INNER JOIN post p
                ON p.id = f.featured_entity_id
            GROUP BY {', '.join(self.FEATURE_COLUMNS)}
        """

        wheres = []
        binds = []

        wheres.append("f.featured_entity_type = %s")
        binds.append(FeaturedEntityType.POST.value)

        wheres.append("f.featurer_type = %s")
        binds.append(featurer_type)

        wheres.append("p.owner_id = %s")
        binds.append(post_owner_id)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        with self.db(self.config) as cursor:
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
