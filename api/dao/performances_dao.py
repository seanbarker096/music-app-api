import datetime
import time
from typing import Dict, List, Optional

from api.db.db import DB
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.features import FeaturedEntityType, FeaturerType
from api.typings.performances import (
    Performance,
    PerformanceAttendance,
    PerformanceAttendanceCreateRequest,
    PerformanceCounts,
    PerformanceCreateRequest,
    PerformancesCountsGetFilter,
    PerformancesCountsGetResult,
    PerformancesGetFilter,
)
from api.typings.tags import TaggedEntityType, TaggedInEntityType


class PerformancesDBAlias:
    PERFORMANCE_ID = "performance_id"
    PERFORMANCE_VENUE_ID = "performance_venue_id"
    PERFORMANCE_PERFORMER_ID = "performance_performer_id"
    PERFORMANCE_DATE = "performance_date"  # users can create performances, so we don't want a unique performance if two usres input a different time of day but the same performer. We therefore store the date only
    PERFORMANCE_CREATE_TIME = "performance_create_time"
    PERFORMANCE_UPDATE_TIME = "performance_update_time"


class PerformancesDAO:
    def __init__(self, config, db: Optional[DB] = None):
        self.db = db if db else DB(config)

    PERFORMANCE_SELECTS = [
        "p.id as " + PerformancesDBAlias.PERFORMANCE_ID,
        "p.venue_id as " + PerformancesDBAlias.PERFORMANCE_VENUE_ID,
        "p.performer_id as " + PerformancesDBAlias.PERFORMANCE_PERFORMER_ID,
        "UNIX_TIMESTAMP(p.performance_date) as " + PerformancesDBAlias.PERFORMANCE_DATE,
        "UNIX_TIMESTAMP(p.create_time) as " + PerformancesDBAlias.PERFORMANCE_CREATE_TIME,
        "UNIX_TIMESTAMP(p.update_time) as " + PerformancesDBAlias.PERFORMANCE_UPDATE_TIME,
    ]

    def performance_create(self, request: PerformanceCreateRequest) -> Performance:

        sql = """
            INSERT INTO performance (venue_id, performer_id, performance_date, create_time, update_time)
            VALUES  (%s, %s, DATE(FROM_UNIXTIME(%s)), FROM_UNIXTIME(%s), FROM_UNIXTIME(%s))
            """

        now = time.time()

        binds = (
            request.venue_id,
            request.performer_id,
            request.performance_date,
            now,
            None,
        )

        db_result = self.db.run_query(sql, binds)

        performance_id = db_result.get_last_row_id()

        return Performance(
            id=performance_id,
            venue_id=request.venue_id,
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
            """

        db_result = self.db.run_query(sql, binds)

        rows = db_result.get_rows()

        performances = []
        for row in rows:
            performance = self._build_performance_from_row(row)
            performances.append(performance)

        return performances

    def performances_counts_get(
        self, filter: PerformancesCountsGetFilter
    ) -> PerformancesCountsGetResult:
        wheres = []
        joins = []
        binds = []

        selects = self.PERFORMANCE_SELECTS

        if filter.include_attendee_count:
            joins.append(
                """
                LEFT JOIN performance_attendance as pa
                    ON pa.performance_id = p.id
                """
            )
            selects.append("COUNT(DISTINCT pa.id) as attendance_count")

        if filter.include_tag_count:
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

        if filter.include_features_count:
            joins.append(
                """
                LEFT JOIN feature as f
                    ON f.featurer_id = p.id
                    AND f.featurer_type = %s
                    AND f.featured_entity_type = %s
                """
            )

            binds.append(FeaturerType.PERFORMANCE.value)
            # For now we just support feature counts for performance posts
            binds.append(FeaturedEntityType.POST.value)

            selects.append("COUNT(DISTINCT f.id) as features_count")

        wheres.append("p.id in %s")
        binds.append(filter.performance_ids)

        where_string = build_where_query_string(wheres, "AND")

        sql = f"""
            SELECT DISTINCT {', '.join(selects)} 
            FROM performance as p
            {"".join(joins)}
            {where_string}
            GROUP BY p.id
            """

        db_result = self.db.run_query(sql, binds)

        rows = db_result.get_rows()

        performances = []
        counts = []

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

            performances.append(performance)
            counts.append(performance_counts)

        return PerformancesCountsGetResult(performances=performances, counts=counts)

    def _build_performance_from_row(self, db_row: Dict[str, any]) -> Performance:
        assert_row_key_exists(db_row, PerformancesDBAlias.PERFORMANCE_ID)
        performance_id = int(db_row[PerformancesDBAlias.PERFORMANCE_ID])

        assert_row_key_exists(db_row, PerformancesDBAlias.PERFORMANCE_VENUE_ID)
        venue_id = (
            int(db_row[PerformancesDBAlias.PERFORMANCE_VENUE_ID])
            if db_row[PerformancesDBAlias.PERFORMANCE_VENUE_ID]
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
            venue_id=venue_id,
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
    def __init__(self, config, db: Optional[DB] = None):
        self.db = db if db else DB(config)

    PERFORMANCE_ATTENDANCE_SELECTS = [
        "id as " + PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_ID,
        "performance_id as " + PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_PERFORMANCE_ID,
        "attendee_id as " + PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_ATTENDEE_ID,
        "UNIX_TIMESTAMP(create_time) as "
        + PerformanceAttendancesDBAlias.PERFORMANCE_ATTENDANCE_CREATE_TIME,
    ]

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

        db_result = self.db.run_query(sql, binds)

        performance_attendance_id = db_result.get_last_row_id()

        return PerformanceAttendance(
            id=performance_attendance_id,
            performance_id=request.performance_id,
            attendee_id=request.attendee_id,
            create_time=now,
        )
