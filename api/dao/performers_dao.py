import time
from typing import Dict, List, Optional

from api.db.db import DB
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.performers import (
    Performer,
    PerformerCreateRequest,
    PerformersGetFilter,
)
from api.utils import date_time_to_unix_time


class PerformerDBAlias:
    PERFORMER_ID = "performer_id"
    PERFORMER_UUID = "performer_uuid"
    PERFORMER_NAME = "performer_name"
    PERFORMER_CREATE_TIME = "performer_create_time"
    PERFORMER_BIOGRAPHY = "performer_biography"
    PERFORMER_UPDATED_TIME = "performer_update_time"
    PERFORMER_OWNER_ID = "performer_owner_id"
    PERFORMER_IMAGE_URL = "performer_image_url"


class PerformersDAO(object):
    db: DB

    PERFORMER_SELECTS = [
        "id as " + PerformerDBAlias.PERFORMER_ID,
        "uuid as " + PerformerDBAlias.PERFORMER_UUID,
        "performer_name as " + PerformerDBAlias.PERFORMER_NAME,
        "create_time as " + PerformerDBAlias.PERFORMER_CREATE_TIME,
        "biography as " + PerformerDBAlias.PERFORMER_BIOGRAPHY,
        "update_time as " + PerformerDBAlias.PERFORMER_UPDATED_TIME,
        "owner_id as " + PerformerDBAlias.PERFORMER_OWNER_ID,
        "image_url as " + PerformerDBAlias.PERFORMER_IMAGE_URL,
    ]

    def __init__(self, config, db: Optional[DB] = None):
        self.db = db if db else DB(config)

    def performers_get(self, filter: PerformersGetFilter) -> List[Performer]:
        selects = f"""
            SELECT {', '.join(self.PERFORMER_SELECTS)} 
            FROM performers
        """

        wheres = []
        binds = []

        if filter.uuids:
            wheres.append("uuid in %s")
            binds.append(filter.uuids)

        if filter.ids:
            wheres.append("id in %s")
            binds.append(filter.ids)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        db_result = self.db.run_query(sql, binds)

        rows = db_result.get_rows()

        performers = []
        for row in rows:
            performer = self._build_performer_from_row(row)
            performers.append(performer)

        return performers

    def performer_create(self, request: PerformerCreateRequest) -> Performer:
        sql = """
            INSERT INTO performers(uuid, performer_name, create_time, biography, update_time, owner_id, image_url) VALUES(%s, %s, FROM_UNIXTIME(%s), %s, FROM_UNIXTIME(%s), %s, %s)
        """

        now = time.time()

        binds = (
            request.uuid,
            request.name,
            now,
            request.biography,
            None,
            request.owner_id,
            request.image_url,
        )

        db_result = self.db.run_query(sql, binds)

        performer_id = db_result.get_last_row_id()

        return Performer(
            id=performer_id,
            uuid=request.uuid,
            name=request.name,
            create_time=now,
            biography=request.biography,
            update_time=None,
            owner_id=request.owner_id,
            image_url=request.image_url,
        )

    def _build_performer_from_row(self, db_row: Dict[str, any]) -> Performer:
        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_ID)
        performer_id = int(db_row[PerformerDBAlias.PERFORMER_ID])

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_UUID)
        performer_uuid = db_row[PerformerDBAlias.PERFORMER_UUID]

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_NAME)
        performer_name = db_row[PerformerDBAlias.PERFORMER_NAME]

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_CREATE_TIME)
        performer_create_time = float(date_time_to_unix_time(db_row[PerformerDBAlias.PERFORMER_CREATE_TIME]))

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_BIOGRAPHY)
        performer_biography = (
            db_row[PerformerDBAlias.PERFORMER_BIOGRAPHY]
            if db_row[PerformerDBAlias.PERFORMER_BIOGRAPHY]
            else None
        )

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_UPDATED_TIME)
        performer_update_time = (
            float(date_time_to_unix_time(db_row[PerformerDBAlias.PERFORMER_UPDATED_TIME]))
            if db_row[PerformerDBAlias.PERFORMER_UPDATED_TIME]
            else None
        )

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_OWNER_ID)
        performer_owner_id = (
            int(db_row[PerformerDBAlias.PERFORMER_OWNER_ID])
            if db_row[PerformerDBAlias.PERFORMER_OWNER_ID]
            else None
        )

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_IMAGE_URL)
        performer_image_url = (
            db_row[PerformerDBAlias.PERFORMER_IMAGE_URL]
            if db_row[PerformerDBAlias.PERFORMER_IMAGE_URL]
            else None
        )

        return Performer(
            id=performer_id,
            uuid=performer_uuid,
            name=performer_name,
            create_time=performer_create_time,
            biography=performer_biography,
            update_time=performer_update_time,
            owner_id=performer_owner_id,
            image_url=performer_image_url,
        )
