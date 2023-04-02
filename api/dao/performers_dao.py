import json
import time
from typing import Dict, List, Optional

from api.db.db import DBConnection
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.performers import (
    AttendeePerformersGetCount,
    AttendeePerformersGetFilter,
    AttendeePerformersGetResult,
    Performer,
    PerformerCreateRequest,
    PerformersGetFilter,
)
from exceptions.exceptions import InvalidArgumentException


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
    db: DBConnection

    """
    Some queries such as in attendee_performers_get requires a GROUP BY on all columns in performances table. We therefore create this so we can iterate over it when adding it to group by clauses. Using PERFORMANCES_SELECTS in a group by would fail as it contains an alias
    """
    PERFORMER_COLUMNS = [
        "p.id",
        "p.uuid",
        "p.performer_name",
        "p.create_time",
        "p.biography",
        "p.update_time",
        "p.owner_id",
        "p.image_url",
    ]

    PERFORMER_SELECTS = [
        f"{PERFORMER_COLUMNS[0]} as {PerformerDBAlias.PERFORMER_ID}",
        f"{PERFORMER_COLUMNS[1]} as {PerformerDBAlias.PERFORMER_UUID}",
        f"{PERFORMER_COLUMNS[2]} as {PerformerDBAlias.PERFORMER_NAME}",
        f"UNIX_TIMESTAMP({PERFORMER_COLUMNS[3]}) as {PerformerDBAlias.PERFORMER_CREATE_TIME}",
        f"{PERFORMER_COLUMNS[4]} as {PerformerDBAlias.PERFORMER_BIOGRAPHY}",
        f"UNIX_TIMESTAMP({PERFORMER_COLUMNS[5]}) as {PerformerDBAlias.PERFORMER_UPDATED_TIME}",
        f"{PERFORMER_COLUMNS[6]} as {PerformerDBAlias.PERFORMER_OWNER_ID}",
        f"{PERFORMER_COLUMNS[7]} as {PerformerDBAlias.PERFORMER_IMAGE_URL}",
    ]

    def __init__(self, config, db: Optional[DBConnection] = None):
        self.db = db if db else DBConnection(config)

    def performers_get(self, filter: PerformersGetFilter) -> List[Performer]:
        selects = f"""
            SELECT {', '.join(self.PERFORMER_SELECTS)} 
            FROM performers as p
        """

        wheres = []
        binds = []

        if filter.uuids:
            wheres.append("p.uuid in %s")
            binds.append(filter.uuids)

        if filter.ids:
            wheres.append("p.id in %s")
            binds.append(filter.ids)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        with self.db as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

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

        with self.db as cursor:
            cursor.execute(sql, binds)
            performer_id = cursor.lastrowid

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

    def attendee_performers_get(
        self, filter: AttendeePerformersGetFilter
    ) -> AttendeePerformersGetResult:

        selects = self.PERFORMER_SELECTS

        group_by = False
        binds = []
        joins = []
        orders = []
        limit = filter.limit if filter.limit else 10

        if not filter.attendee_id:
            raise InvalidArgumentException("attendee_id is required for attendee_performers_get")

        joins.append(
            """
            INNER JOIN performance
                ON performance.performer_id = p.id
            INNER JOIN performance_attendance as pa
                ON pa.performance_id = performance.id
                AND pa.attendee_id = %s
            """
        )
        binds.append(filter.attendee_id)

        if filter.get_counts:
            group_by = True
            selects.append("COUNT(pa.id) as performance_count")

            # Keep things simple and just order by performance count if they ask for counts
            orders.append("performance_count DESC")

        order_by_string = f"ORDER BY {', '.join(orders)}" if len(orders) > 0 else ""

        # We use distinct for cases where we are not grouping on the performer, in which case we have have multiple rows for the same performer for each of their performances
        select_string = (
            f"SELECT DISTINCT {', '.join(selects)}"
            if not group_by
            else f"SELECT {', '.join(selects)}"
        )

        sql = f"""
            {select_string} FROM performers as p
            {"".join(joins)}
            {f"GROUP BY {', '.join(self.PERFORMER_COLUMNS)}" if group_by else ""}
            {order_by_string}
            LIMIT {limit}
        """

        with self.db as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        performers = []
        counts = [] if filter.get_counts else None

        for row in rows:
            performer = self._build_performer_from_row(row)
            performers.append(performer)

            if filter.get_counts:
                count_result = AttendeePerformersGetCount(
                    attendee_id=filter.attendee_id,
                    performer_id=performer.id,
                    count=int(row["performance_count"]),
                )
                counts.append(count_result)

        return AttendeePerformersGetResult(performers=performers, counts=counts)

    def _build_performer_from_row(self, db_row: Dict[str, any]) -> Performer:
        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_ID)
        performer_id = int(db_row[PerformerDBAlias.PERFORMER_ID])

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_UUID)
        performer_uuid = db_row[PerformerDBAlias.PERFORMER_UUID]

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_NAME)
        performer_name = db_row[PerformerDBAlias.PERFORMER_NAME]

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_CREATE_TIME)
        performer_create_time = int(db_row[PerformerDBAlias.PERFORMER_CREATE_TIME])

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_BIOGRAPHY)
        performer_biography = (
            db_row[PerformerDBAlias.PERFORMER_BIOGRAPHY]
            if db_row[PerformerDBAlias.PERFORMER_BIOGRAPHY]
            else None
        )

        assert_row_key_exists(db_row, PerformerDBAlias.PERFORMER_UPDATED_TIME)
        performer_update_time = (
            int(db_row[PerformerDBAlias.PERFORMER_UPDATED_TIME])
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
