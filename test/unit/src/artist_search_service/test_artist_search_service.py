import json
from test.unit import TestCase
from unittest.mock import Mock, patch

from api.artist_search_service.api import ArtistSearchService
from api.artist_search_service.search_client.spotify_search_imp import SpotifySearchImp
from api.artist_search_service.types import ArtistsSearchRequest


class ArtistSearchServiceTestCase(TestCase):
    EXAMPLE_API_RESPONSE = {
        "artists": {
            "href": "https://api.spotify.com/v1/search?query=f&type=artist&offset=950&limit=2",
            "items": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/6CnCjQXjKiV9Ro5GGA8ztB"
                    },
                    "followers": {"href": "null", "total": 5298},
                    "genres": [],
                    "href": "https://api.spotify.com/v1/artists/6CnCjQXjKiV9Ro5GGA8ztB",
                    "id": "6CnCjQXjKiV9Ro5GGA8ztB",
                    "images": [
                        {
                            "height": 640,
                            "url": "https://i.scdn.co/image/ab6761610000e5ebe65d511a67b93123f63324dd",
                            "width": 640,
                        },
                        {
                            "height": 320,
                            "url": "https://i.scdn.co/image/ab67616100005174e65d511a67b93123f63324dd",
                            "width": 320,
                        },
                        {
                            "height": 160,
                            "url": "https://i.scdn.co/image/ab6761610000f178e65d511a67b93123f63324dd",
                            "width": 160,
                        },
                    ],
                    "name": "Eminem",
                    "popularity": 54,
                    "type": "artist",
                    "uri": "spotify:artist:6CnCjQXjKiV9Ro5GGA8ztB",
                },
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/artist/69Iibc3uQ7x2vDeZxTwKCw"
                    },
                    "followers": {"href": "null", "total": 31973},
                    "genres": [],
                    "href": "https://api.spotify.com/v1/artists/69Iibc3uQ7x2vDeZxTwKCw",
                    "id": "69Iibc3uQ7x2vDeZxTwKCw",
                    "images": [
                        {
                            "height": 640,
                            "url": "https://i.scdn.co/image/ab6761610000e5eb7afc98ed72a989977d32f13a",
                            "width": 640,
                        },
                        {
                            "height": 320,
                            "url": "https://i.scdn.co/image/ab676161000051747afc98ed72a989977d32f13a",
                            "width": 320,
                        },
                        {
                            "height": 160,
                            "url": "https://i.scdn.co/image/ab6761610000f1787afc98ed72a989977d32f13a",
                            "width": 160,
                        },
                    ],
                    "name": "Eric Clapton",
                    "popularity": 50,
                    "type": "artist",
                    "uri": "spotify:artist:69Iibc3uQ7x2vDeZxTwKCw",
                },
            ],
            "limit": 2,
            "next": "https://api.spotify.com/v1/search?query=f&type=artist&offset=952&limit=2",
            "offset": 950,
            "previous": "https://api.spotify.com/v1/search?query=f&type=artist&offset=948&limit=2",
            "total": 1000,
        }
    }

    @patch.object(SpotifySearchImp, "_spotify_search_artists")
    @patch.object(SpotifySearchImp, "_spotify_get_access_token")
    def test_artist_search(self, mock_get_access_token, mock_search_artists):
        mock_search_imp = SpotifySearchImp(self.config)
        mock_get_access_token.return_value = "test_token"
        mock_search_artists.return_value = self.EXAMPLE_API_RESPONSE

        service = ArtistSearchService(self.config, mock_search_imp)

        request = ArtistsSearchRequest(search_terms={"q": "E"})

        response = service.search(request)

        mock_get_access_token.assert_called_once()
        # 50 is the default limit for spotify implementation
        mock_search_artists.assert_called_once_with("test_token", "E", 50)

        artists = response.artists

        self.assertEqual(len(artists), 2, "Should return two artists")
        self.assertEqual(artists[0].name, "Eminem", "Should return correct artist name (1)")
        self.assertEqual(artists[1].name, "Eric Clapton", "Should return correct artist name (2)")
        self.assertEqual(
            artists[0].uuid, "6CnCjQXjKiV9Ro5GGA8ztB", "Should return correct artist id (1)"
        )
        self.assertEqual(
            artists[1].uuid, "69Iibc3uQ7x2vDeZxTwKCw", "Should return correct artist id (2)"
        )
        self.assertEqual(response.limit, 2, "Should return correct limit")
        self.assertEqual(response.offset, 950, "Should return correct offset")
        self.assertEqual(response.total, 1000, "Should return correct total")
        self.assertEqual(
            response.next,
            "https://api.spotify.com/v1/search?query=f&type=artist&offset=952&limit=2",
            "Should return correct next",
        )
        self.assertEqual(
            response.previous,
            "https://api.spotify.com/v1/search?query=f&type=artist&offset=948&limit=2",
            "Should return correct previous",
        )
