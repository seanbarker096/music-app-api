from typing import Dict, List, Optional

from api.db.db import DBConnectionManager, FlaskDBConnectionManager
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.events import Event, EventCreateRequest, EventsGetFilter


class EventsDBAlias:
    EVENT_ID = "event_id"
    EVENT_NAME = "event_name"
    EVENT_VENUE_NAME = "event_venue_name"
    EVENT_START_DATE = "event_start_date"
    EVENT_END_DATE = "event_end_date"
    EVENT_EVENT_TYPE = "event_event_type"


class EventsDAO:
    db: DBConnectionManager

    EVENT_SELECTS = [
        "e.id as " + EventsDBAlias.EVENT_ID,
        "e.name as " + EventsDBAlias.EVENT_NAME,
        "e.venue_name as " + EventsDBAlias.EVENT_VENUE_NAME,
        "UNIX_TIMESTAMP(e.start_date) as " + EventsDBAlias.EVENT_START_DATE,
        "UNIX_TIMESTAMP(e.end_date) as " + EventsDBAlias.EVENT_END_DATE,
        "e.event_type as " + EventsDBAlias.EVENT_TYPE,
    ]

    def __init__(self, config, db: Optional[DBConnectionManager] = None):
        self.db = db if db else FlaskDBConnectionManager
        self.config = config

    def event_create(self, request: EventCreateRequest) -> Event:
        sql = f"""
            INSERT INTO event(name, venue_name, start_date, end_date, event_type)
            VALUES(%s, %s, DATE(FROM_UNIXTIME(%s)), DATE(FROM_UNIXTIME(%s)), %s)
        """

        binds = (
            request.name,
            request.venue_name,
            request.start_date,
            request.end_date,
            request.event_type,
        )

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            event_id = cursor.lastrowid

        return Event(
            id=event_id,
            name=request.name,
            venue_name=request.venue_name,
            start_date=request.start_date,
            end_date=request.end_date,
            event_type=request.event_type,
        )
    
    def events_get(self, filter: EventsGetFilter) -> List[Event]:
        selects = f"""
            SELECT {', '.join(self.EVENT_SELECTS)} from event as e
        """

        wheres = []
        binds = []

        if filter.event_type:
            wheres.append("e.event_type = %s")
            binds.append(filter.event_type)

        if filter.start_date:
            wheres.append("e.start_date = DATE(FROM_UNIXTIME(%s))")
            binds.append(filter.start_date)

        if filter.end_date:
            wheres.append("e.end_date = DATE(FROM_UNIXTIME(%s))")
            binds.append(filter.end_date)

        if filter.name:
            wheres.append("e.name = %s")
            binds.append(filter.name)

        where_string = build_where_query_string(wheres, "AND")

        sql = selects + where_string

        with self.db(self.config) as cursor:
            cursor.execute(sql, binds)
            rows = cursor.fetchall()

        events = []
        for row in rows:
            event = self._build_event_from_db_row(row)
            events.append(event)

        return events
    
    def _build_event_from_db_row(self, db_row: Dict[str, any]) -> Event:
        assert_row_key_exists(db_row, EventsDBAlias.EVENT_ID)
        event_id = int(db_row[EventsDBAlias.EVENT_ID])

        assert_row_key_exists(db_row, EventsDBAlias.EVENT_NAME)
        event_name = db_row[EventsDBAlias.EVENT_NAME]

        assert_row_key_exists(db_row, EventsDBAlias.EVENT_VENUE_NAME)
        event_venue_name = db_row[EventsDBAlias.EVENT_VENUE_NAME]

        assert_row_key_exists(db_row, EventsDBAlias.EVENT_START_DATE)
        event_start_date = db_row[EventsDBAlias.EVENT_START_DATE]

        assert_row_key_exists(db_row, EventsDBAlias.EVENT_END_DATE)
        event_end_date = db_row[EventsDBAlias.EVENT_END_DATE]

        assert_row_key_exists(db_row, EventsDBAlias.EVENT_EVENT_TYPE)
        event_event_type = db_row[EventsDBAlias.EVENT_EVENT_TYPE]

        return Event(
            id=event_id,
            name=event_name,
            venue_name=event_venue_name,
            start_date=event_start_date,
            end_date=event_end_date,
            event_type=event_event_type,
        )