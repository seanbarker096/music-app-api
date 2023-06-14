from test.unit import TestCase
from unittest.mock import patch

from api.performer_search_service.api import PerformerSearchService
from api.performer_search_service.search_client.spotify_search_imp import (
    SpotifySearchImp,
)
from api.performer_search_service.types import PerformersSearchRequest


class PerformerSearchServiceTestCase(TestCase):
    EXAMPLE_API_RESPONSE = {
        "artists": {
            "href": "https://api.spotify.com/v1/search?query=f&type=performer&offset=950&limit=2",
            "items": [
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/performer/6CnCjQXjKiV9Ro5GGA8ztB"
                    },
                    "followers": {"href": "null", "total": 5298},
                    "genres": [],
                    "href": "https://api.spotify.com/v1/performers/6CnCjQXjKiV9Ro5GGA8ztB",
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
                    "type": "performer",
                    "uri": "spotify:performer:6CnCjQXjKiV9Ro5GGA8ztB",
                },
                {
                    "external_urls": {
                        "spotify": "https://open.spotify.com/performer/69Iibc3uQ7x2vDeZxTwKCw"
                    },
                    "followers": {"href": "null", "total": 31973},
                    "genres": [],
                    "href": "https://api.spotify.com/v1/performers/69Iibc3uQ7x2vDeZxTwKCw",
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
                    "type": "performer",
                    "uri": "spotify:performer:69Iibc3uQ7x2vDeZxTwKCw",
                },
            ],
            "limit": 2,
            "next": "https://api.spotify.com/v1/search?query=f&type=performer&offset=952&limit=2",
            "offset": 950,
            "previous": "https://api.spotify.com/v1/search?query=f&type=performer&offset=948&limit=2",
            "total": 1000,
        }
    }

    @patch.object(SpotifySearchImp, "_spotify_search_artists")
    @patch.object(SpotifySearchImp, "_spotify_get_access_token")
    def test_performer_search(self, mock_get_access_token, mock_search_artists):
        mock_search_imp = SpotifySearchImp(self.config)
        mock_get_access_token.return_value = "test_token"
        mock_search_artists.return_value = self.EXAMPLE_API_RESPONSE

        service = PerformerSearchService(self.config, mock_search_imp)

        request = PerformersSearchRequest(search_terms={"q": "E"})

        response = service.search(request)

        mock_get_access_token.assert_called_once()
        # 50 is the default limit for spotify implementation
        mock_search_artists.assert_called_once_with("test_token", "E", 50)

        performers = response.performers

        self.assertEqual(len(performers), 2, "Should return two performers")
        self.assertEqual(performers[0].name, "Eminem", "Should return correct performer name (1)")
        self.assertEqual(performers[1].name, "Eric Clapton", "Should return correct performer name (2)")
        self.assertEqual(
            performers[0].uuid, "6CnCjQXjKiV9Ro5GGA8ztB", "Should return correct performer id (1)"
        )
        self.assertEqual(
            performers[1].uuid, "69Iibc3uQ7x2vDeZxTwKCw", "Should return correct performer id (2)"
        )
        self.assertEqual(response.limit, 2, "Should return correct limit")
        self.assertEqual(response.offset, 950, "Should return correct offset")
        self.assertEqual(response.total, 1000, "Should return correct total")
        self.assertEqual(
            response.next,
            "https://api.spotify.com/v1/search?query=f&type=performer&offset=952&limit=2",
            "Should return correct next",
        )
        self.assertEqual(
            response.previous,
            "https://api.spotify.com/v1/search?query=f&type=performer&offset=948&limit=2",
            "Should return correct previous",
        )
