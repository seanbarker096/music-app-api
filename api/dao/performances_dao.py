import time
from typing import Dict, List, Optional

from api.db.db import DBConnectionManager, FlaskDBConnectionManager
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.features import FeaturedEntityType, FeaturerType
from api.typings.performances import (
    Performance,
    PerformanceAttendance,
    PerformanceAttendanceCreateRequest,
    PerformanceAttendanceDeleteRequest,
    PerformanceAttendancesGetFilter,
    PerformanceCounts,
    PerformanceCreateRequest,
    PerformancesGetFilter,
)
from api.typings.tags import TaggedEntityType, TaggedInEntityType


class PerformancesDBAlias:
    PERFORMANCE_ID = "performance_id"
    PERFORMANCE_EVENT_ID = "performance_event_id"
    PERFORMANCE_PERFORMER_ID = "performance_performer_id"
    PERFORMANCE_DATE = "performance_date"  # users can create performances, so we don't want a unique performance if two usres input a different time of day but the same performer. We therefore store the date only
    PERFORMANCE_CREATE_TIME = "performance_create_time"
    PERFORMANCE_UPDATE_TIME = "performance_update_time"


class PerformancesDAO:
    def __init__(self, config, db: Optional[DBConnectionManager] = None):
        self.db = db if db else FlaskDBConnectionManager
        self.config = config

    PERFORMANCE_SELECTS = [
        "p.id as " + PerformancesDBAlias.PERFORMANCE_ID,
        "p.event_id as " + PerformancesDBAlias.PERFORMANCE_EVENT_ID,
        "p.performer_id as " + PerformancesDBAlias.PERFORMANCE_PERFORMER_ID,
        "UNIX_TIMESTAMP(p.performance_date) as " + PerformancesDBAlias.PERFORMANCE_DATE,
        "UNIX_TIMESTAMP(p.create_time) as " + PerformancesDBAlias.PERFORMANCE_CREATE_TIME,
        "UNIX_TIMESTAMP(p.update_time) as " + PerformancesDBAlias.PERFORMANCE_UPDATE_TIME,
    ]

    def performance_create(self, request: PerformanceCreateRequest) -> Performance:

        sql = """
            INSERT INTO performance (event_id, performer_id, performance_date, create_time, update_time)
            VALUES  (%s, %s, DATE(FROM_UNIXTIME(%s)), FROM_UNIXTIME(%s), FROM_UNIXTIME(%s))
            """

        now = time.time()

        binds = (
            request.event_id,
            request.performer_id,
            request.performance_date,
            now,
            None,
        )

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            performance_id = cursor.lastrowid

        return Performance(
            id=performance_id,
            event_id=request.event_id,
            performer_id=request.performer_id,
            performance_date=request.performance_date,
            create_time=now,
            update_time=None,
        )

    def performances_get(self, filter: PerformancesGetFilter) -> List[Performance]:
        selects = f"""
            SELECT {", ".join(self.PERFORMANCE_SELECTS)}
            FROM performance as p
            """

        wheres = []
        joins = []
        binds = []

        if filter.attendee_ids:
            joins.append(
                """
                LEFT JOIN performance_attendance as pa
                    ON pa.performance_id = p.id
                    AND pa.attendee_id in %s
                """
            )
            binds.append(filter.attendee_ids)
            # providing this filter implies we are only returning performances that user has attended. LEFT JOIN instead of INNER in case this behaviour changes though
            wheres.append("pa.id IS NOT NULL")

        if filter.ids:
            wheres.append("p.id in %s")
            binds.append(filter.ids)

        if filter.performer_ids:
            wheres.append("p.performer_id in %s")
            binds.append(filter.performer_ids)

        if filter.performance_date:
            wheres.append("p.performance_date = DATE(FROM_UNIXTIME(%s))")
            binds.append(filter.performance_date)

        if len(wheres) == 0:
            raise Exception("Unbounded performances_get query. Please provide at least one filter")

        where_string = build_where_query_string(wheres, "AND")

        sql = f"""
            {selects}
            {"".join(joins)}
            {where_string}
            ORDER BY p.performance_date DESC
            """

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        performances = []
        for row in rows:
            performance = self._build_performance_from_row(row)
            performances.append(performance)

        return performances

    def performances_counts_get(
        self,
        performance_ids: List[int],
        include_attendee_count=False,
        include_tag_count=False,
        include_features_count=False,
    ) -> Dict[int, PerformanceCounts]:
        """
        returns: Dict of performance_id to PerformanceCounts
        """
        wheres = []
        joins = []
        binds = []

        selects = [*self.PERFORMANCE_SELECTS]

        if not include_attendee_count and not include_tag_count and not include_features_count:
            raise Exception("Must provide at least one count to include")

        if len(performance_ids) == 0:
            return {}

        if include_attendee_count:
            joins.append(
                """
                LEFT JOIN performance_attendance as pa
                    ON pa.performance_id = p.id
                """
            )
            selects.append("COUNT(DISTINCT pa.id) as attendance_count")

        if include_tag_count:
            joins.append(
                """
                LEFT JOIN tag as t
                    ON t.tagged_entity_id = p.id
                    AND t.tagged_entity_type = %s
                    AND t.tagged_in_entity_type = %s
                """
            )
            binds.append(TaggedEntityType.PERFORMANCE.value)
            # For now we just support tag counts for performance posts
            binds.append(TaggedInEntityType.POST.value)

            selects.append("COUNT(DISTINCT t.id) as tag_count")

        if include_features_count:
            joins.append(
                """
                LEFT JOIN performers
                    ON performers.id = p.performer_id
                LEFT JOIN feature as f
                    ON f.featurer_id = performers.id
                    AND f.featurer_type = %s
                    AND f.featured_entity_type = %s
                """
            )

            binds.append(FeaturerType.PERFORMER.value)
            # For now we just support feature counts for performance posts
            binds.append(FeaturedEntityType.POST.value)

            selects.append("COUNT(DISTINCT f.id) as features_count")

        wheres.append("p.id in %s")
        binds.append(performance_ids)

        where_string = build_where_query_string(wheres, "AND")

        sql = f"""
            SELECT DISTINCT {', '.join(selects)} 
            FROM performance as p
            {"".join(joins)}
            {where_string}
            GROUP BY p.id
            """

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        result = {}

        for row in rows:
            performance = self._build_performance_from_row(row)

            attendance_count = row.get("attendance_count", None)
            tag_count = row.get("tag_count", None)
            features_count = row.get("features_count", None)

            performance_counts = PerformanceCounts(
                performance_id=performance.id,
                attendee_count=attendance_count,
                tag_count=tag_count,
                features_count=features_count,
            )

            result[performance.id] = performance_counts

        return result

    def _build_performance_from_row(self, db_row: Dict[str, any]) -> Performance:
        assert_row_key_exists(db_row, PerformancesDBAlias.PERFORMANCE_ID)
        performance_id = int(db_row[PerformancesDBAlias.PERFORMANCE_ID])

        assert_row_key_exists(db_row, PerformancesDBAlias.PERFORMANCE_EVENT_ID)
        event_id = (
            int(db_row[PerformancesDBAlias.PERFORMANCE_EVENT_ID])
            if db_row[PerformancesDBAlias.PERFORMANCE_EVENT_ID]
            else None
        )

        assert_row_key_exists(db_row, PerformancesDBAlias.PERFORMANCE_PERFORMER_ID)
        performer_id = int(db_row[PerformancesDBAlias.PERFORMANCE_PERFORMER_ID])

        assert_row_key_exists(db_row, PerformancesDBAlias.PERFORMANCE_DATE)
        performance_date = int(db_row[PerformancesDBAlias.PERFORMANCE_DATE])

        assert_row_key_exists(db_row, PerformancesDBAlias.PERFORMANCE_CREATE_TIME)
        create_time = int(db_row[PerformancesDBAlias.PERFORMANCE_CREATE_TIME])

        assert_row_key_exists(db_row, PerformancesDBAlias.PERFORMANCE_UPDATE_TIME)
        update_time = (
            int(db_row[PerformancesDBAlias.PERFORMANCE_UPDATE_TIME])
            if db_row[PerformancesDBAlias.PERFORMANCE_UPDATE_TIME]
            else None
        )

        return Performance(
            id=performance_id,
            event_id=event_id,
            performer_id=performer_id,
            performance_date=performance_date,
            create_time=create_time,
            update_time=update_time,
        )


class PerformanceAttendancesDBAlias:
    PERFORMANCE_ATTENDANCE_ID = "performance_attendance_id"
    PERFORMANCE_ATTENDANCE_PERFORMANCE_ID = "performance_attendance_performance_id"
    PERFORMANCE_ATTENDANCE_ATTENDEE_ID = "performance_attendance_attendee_id"
    PERFORMANCE_ATTENDANCE_CREATE_TIME = "performance_attendance_create_time"


class PerformanceAttendancesDAO:
    PERFORMANCE_ATTENDANCE_SELECTS = [
        "pa.id as " + PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_ID,
        "pa.performance_id as "
        + PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_PERFORMANCE_ID,
        "pa.attendee_id as " + PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_ATTENDEE_ID,
        "UNIX_TIMESTAMP(pa.create_time) as "
        + PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_CREATE_TIME,
    ]

    def __init__(self, config, db: Optional[DBConnectionManager] = None):
        self.db = db if db else FlaskDBConnectionManager
        self.config = config

    def performance_attendance_create(
        self, request: PerformanceAttendanceCreateRequest
    ) -> PerformanceAttendance:
        sql = """
                INSERT INTO performance_attendance (performance_id, attendee_id, create_time)
                VALUES  (%s, %s, FROM_UNIXTIME(%s))
                """

        now = time.time()

        binds = (
            request.performance_id,
            request.attendee_id,
            now,
        )

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            performance_attendance_id = cursor.lastrowid

        return PerformanceAttendance(
            id=performance_attendance_id,
            performance_id=request.performance_id,
            attendee_id=request.attendee_id,
            create_time=now,
        )
    
    def performance_attendance_delete(
        self, request: PerformanceAttendanceDeleteRequest
    ) -> None:
        sql = """
                DELETE FROM performance_attendance
                WHERE id = %s
                """

        binds = (
            request.id,
        )

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)

    def performance_attendances_get(
        self, filter: PerformanceAttendancesGetFilter
    ) -> List[Performance]:

        selects = f"""
        SELECT {' ,'.join(self.PERFORMANCE_ATTENDANCE_SELECTS)}
        FROM performance_attendance as pa
        """

        binds = []
        wheres = []


        if filter.ids:
            wheres.append("pa.id in %s")
            binds.append(filter.ids)
            
        if filter.performance_ids:
            wheres.append("pa.performance_id in %s")
            binds.append(filter.performance_ids)

        if filter.attendee_ids:
            wheres.append("pa.attendee_id in %s")
            binds.append(filter.attendee_ids)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        performance_attendances = []
        for row in rows:
            performance_attendance = self._build_performance_attendance_from_db_row(row)
            performance_attendances.append(performance_attendance)

        return performance_attendances

    def _build_performance_attendance_from_db_row(
        self, row: Dict[str, any]
    ) -> PerformanceAttendance:
        assert_row_key_exists(row, PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_ID)
        performance_attendance_id = int(
            row[PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_ID]
        )

        assert_row_key_exists(
            row, PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_PERFORMANCE_ID
        )
        performance_id = int(
            row[PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_PERFORMANCE_ID]
        )

        assert_row_key_exists(row, PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_ATTENDEE_ID)
        attendee_id = int(row[PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_ATTENDEE_ID])

        assert_row_key_exists(row, PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_CREATE_TIME)
        create_time = int(row[PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_CREATE_TIME])

        return PerformanceAttendance(
            id=performance_attendance_id,
            performance_id=performance_id,
            attendee_id=attendee_id,
            create_time=create_time,
        )
