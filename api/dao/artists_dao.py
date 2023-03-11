import time
from typing import Dict, List, Optional

from api.db.db import DB
from api.db.utils.db_util import assert_row_key_exists, build_where_query_string
from api.typings.artists import Artist, ArtistCreateRequest, ArtistsGetFilter
from api.utils import date_time_to_unix_time


class ArtistDBAlias:
    ARTIST_ID = "artist_id"
    ARTIST_UUID = "artist_uuid"
    ARTIST_NAME = "artist_name"
    ARTIST_CREATE_TIME = "artist_create_time"
    ARTIST_BIOGRAPHY = "artist_biography"
    ARTIST_UPDATED_TIME = "artist_update_time"
    ARTIST_OWNER_ID = "artist_owner_id"
    ARTIST_IMAGE_URL = "artist_image_url"


class ArtistsDAO(object):
    db: DB

    ARTIST_SELECTS = [
        "id as " + ArtistDBAlias.ARTIST_ID,
        "uuid as " + ArtistDBAlias.ARTIST_UUID,
        "artist_name as " + ArtistDBAlias.ARTIST_NAME,
        "create_time as " + ArtistDBAlias.ARTIST_CREATE_TIME,
        "biography as " + ArtistDBAlias.ARTIST_BIOGRAPHY,
        "update_time as " + ArtistDBAlias.ARTIST_UPDATED_TIME,
        "owner_id as " + ArtistDBAlias.ARTIST_OWNER_ID,
        "image_url as " + ArtistDBAlias.ARTIST_IMAGE_URL,
    ]

    def __init__(self, config, db: Optional[DB] = None):
        self.db = db if db else DB(config)

    def artists_get(self, filter: ArtistsGetFilter) -> List[Artist]:
        selects = f"""
            SELECT {', '.join(self.ARTIST_SELECTS)} 
            FROM artists
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

        artists = []
        for row in rows:
            artist = self._build_artist_from_row(row)
            artists.append(artist)

        return artists

    def artist_create(self, request: ArtistCreateRequest) -> Artist:
        sql = """
            INSERT INTO artists(uuid, artist_name, create_time, biography, update_time, owner_id, image_url) VALUES(%s, %s, FROM_UNIXTIME(%s), %s, FROM_UNIXTIME(%s), %s, %s)
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

        artist_id = db_result.get_last_row_id()

        return Artist(
            id=artist_id,
            uuid=request.uuid,
            name=request.name,
            create_time=now,
            biography=request.biography,
            update_time=None,
            owner_id=request.owner_id,
            image_url=request.image_url,
        )

    def _build_artist_from_row(self, db_row: Dict[str, any]) -> Artist:
        assert_row_key_exists(db_row, ArtistDBAlias.ARTIST_ID)
        artist_id = int(db_row[ArtistDBAlias.ARTIST_ID])

        assert_row_key_exists(db_row, ArtistDBAlias.ARTIST_UUID)
        artist_uuid = db_row[ArtistDBAlias.ARTIST_UUID]

        assert_row_key_exists(db_row, ArtistDBAlias.ARTIST_NAME)
        artist_name = db_row[ArtistDBAlias.ARTIST_NAME]

        assert_row_key_exists(db_row, ArtistDBAlias.ARTIST_CREATE_TIME)
        artist_create_time = float(date_time_to_unix_time(db_row[ArtistDBAlias.ARTIST_CREATE_TIME]))

        assert_row_key_exists(db_row, ArtistDBAlias.ARTIST_BIOGRAPHY)
        artist_biography = (
            db_row[ArtistDBAlias.ARTIST_BIOGRAPHY]
            if db_row[ArtistDBAlias.ARTIST_BIOGRAPHY]
            else None
        )

        assert_row_key_exists(db_row, ArtistDBAlias.ARTIST_UPDATED_TIME)
        artist_update_time = (
            float(date_time_to_unix_time(db_row[ArtistDBAlias.ARTIST_UPDATED_TIME]))
            if db_row[ArtistDBAlias.ARTIST_UPDATED_TIME]
            else None
        )

        assert_row_key_exists(db_row, ArtistDBAlias.ARTIST_OWNER_ID)
        artist_owner_id = (
            int(db_row[ArtistDBAlias.ARTIST_OWNER_ID])
            if db_row[ArtistDBAlias.ARTIST_OWNER_ID]
            else None
        )

        assert_row_key_exists(db_row, ArtistDBAlias.ARTIST_IMAGE_URL)
        artist_image_url = (
            db_row[ArtistDBAlias.ARTIST_IMAGE_URL]
            if db_row[ArtistDBAlias.ARTIST_IMAGE_URL]
            else None
        )

        return Artist(
            id=artist_id,
            uuid=artist_uuid,
            name=artist_name,
            create_time=artist_create_time,
            biography=artist_biography,
            update_time=artist_update_time,
            owner_id=artist_owner_id,
            image_url=artist_image_url,
        )
