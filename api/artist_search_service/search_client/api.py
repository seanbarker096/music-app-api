from typing import Optional

from api.artist_search_service.search_client import SearchImp, SpotifySearchImp


class SearchClient(object):
    def __init__(self, config, search_imp: Optional[SearchImp] = None):
        self.config = config

        if not search_imp:
            implementation_type = self.config["config_file"]["artist-search-service"].get(
                "search-client", "spotify"
            )

            match implementation_type:
                case "spotify":
                    self.search_imp = SpotifySearchImp(config)

        else:
            self.search_imp = search_imp

    def search(self, query: str) -> List[Artist]:
        return self.search_imp.search(query)

    def _search(self, query: str) -> List[Artist]:
        ...
