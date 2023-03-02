import base64
import json
from typing import Any, Dict, List, Optional

import requests

from api.artist_search_service.search_client.search_imp import SearchImp
from api.artist_search_service.types import ArtistsSearchRequest, ArtistsSearchResult
from api.typings.artists import ArtistSearchArtist
from exceptions.exceptions import AppSearchServiceException


class SpotifySearchRequest:
    q: str = ...
    limit: Optional[int] = ...

    def __init__(self, q: str, limit: Optional[int] = None):
        self.q = q
        self.limit = limit if limit else 50


class SpotifySearchImp(SearchImp):
    def __init__(self, config):
        self.config = config
        self.secret = config["config_file"]["artist-search-service"].get("spotity-client-secret")
        self.client_id = config["config_file"]["artist-search-service"].get("spotify-client-id")
        self.client = "spotify"

    def process_request(self, request: ArtistsSearchRequest) -> SpotifySearchRequest:
        ## Currently only support the q search term
        searchTerm = request.search_terms.get("q", None)

        if not searchTerm:
            raise Exception("Invalid search terms provided")

        return SpotifySearchRequest(q=searchTerm, limit=request.limit)

    def search(self, request: SpotifySearchRequest) -> str:
        ## TODO: Avoid calling this every time. Instead cache the token somwhere and request it
        access_token = self._spotify_get_access_token()

        return self._spotify_search_artists(access_token, request.q, request.limit)

    def build_search_result(self, api_result: Dict[str, Any]) -> ArtistsSearchResult:

        dict = api_result.get("artists", None)

        limit = dict.get("limit", None)
        next = dict.get("next", None)
        previous = dict.get("previous", None)
        offset = dict.get("offset", None)
        total = dict.get("total", None)
        artists = dict.get("items", [])

        app_artists = [self._build_app_artist(artist) for artist in artists]

        return ArtistsSearchResult(
            artists=app_artists,
            total=total,
            offset=offset,
            limit=limit,
            next=next,
            previous=previous,
        )

    def _spotify_get_access_token(self) -> str:
        auth_str = f"{self.client_id}:{self.secret}"
        b64_auth_str = base64.b64encode(auth_str.encode()).decode("ascii")

        print(b64_auth_str)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {b64_auth_str}",
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data=data,
            headers=headers,
        )

        try:
            print(response.json())
            response.raise_for_status()
            access_token = response.json()["access_token"]
            return access_token
        except requests.exceptions.HTTPError as err:
            raise Exception(
                f"Failed to get access token from spotify api. Error: {json.dumps(str(err))}"
            )

    def _spotify_search_artists(self, access_token, search_term, limit) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://api.spotify.com/v1/search?q={search_term}&type=artist&limit={limit}"
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            raise Exception(
                f"Error in request to spotify api when searching for artists. Error: {json.dumps(str(err))}"
            )

    def _build_app_artist(self, artist: dict) -> ArtistSearchArtist:

        self._assert_field_exists("name", artist)
        name = artist["name"]

        self._assert_field_exists("id", artist)
        uuid = artist["id"]

        self._assert_field_exists("images", artist)
        image_url = artist["images"][-1]["url"] if len(artist["images"]) > 0 else None

        return ArtistSearchArtist(name=name, uuid=uuid, image_url=image_url)

    def _assert_field_exists(self, field: str, artist: Dict[str, Any]):

        if artist.get(field, None) is None:
            raise Exception(
                f"Field {field} not found in in spotify api response. Response: {json.dumps(artist)}"
            )

    def get_artist_by_uuid(
        self,
        uuid: str,
    ) -> ArtistSearchArtist:
        access_token = self._spotify_get_access_token()
        artist_dict = self._get_artist_by_uuid(access_token, uuid)

        self._assert_field_exists("name", artist_dict)
        name = artist_dict["name"]

        self._assert_field_exists("id", artist_dict)
        uuid = artist_dict["id"]

        self._assert_field_exists("images", artist_dict)
        image_url = artist_dict["images"][-1]["url"] if len(artist_dict["images"]) > 0 else None

        return ArtistSearchArtist(name=name, uuid=uuid, image_url=image_url)

    def _get_artist_by_uuid(
        self,
        access_token: str,
        uuid: str,
    ) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"https://api.spotify.com/v1/artists/{uuid}"
        response = requests.get(url, headers=headers)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            raise Exception(
                f"Error in request to spotify api when getting artist by uuid: {uuid}. Error: {json.dumps(str(err))}"
            )