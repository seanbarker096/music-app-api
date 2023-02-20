from api.artist_search_service.search_client.search_imp import SearchImp


class SpotifySearchImp(SearchImp):
    def __init__(self, config):
        self.config = config

    def search(self, query: str) -> List[Artist]:
        return self.spotify_client.search(query)
