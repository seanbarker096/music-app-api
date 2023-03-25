from typing import Optional


class PerformerFixtureDTO:
    def __init__(
        self, 
        uuid: str,
        name: str,
        create_time: int,
        biography: Optional[str] = None,
        update_time: Optional[int] = None,
        owner_id: Optional[int] = None,
        image_url: Optional[str] = None
    ):
        self.uuid = uuid
        self.name = name
        self.create_time = create_time
        self.biography = biography if biography else 'A great performer from London'
        self.update_time = update_time
        self.owner_id = owner_id
        self.image_url = image_url if image_url else 'https://www.fakeurl.com/some_artist'
    
    def get_uuid(self) -> str:
        return self.uuid
    
    def get_name(self) -> str:
        return self.name
    
    def get_create_time(self) -> int:
        return self.create_time
    
    def get_biography(self) -> Optional[str]:
        return self.biography
    
    def get_update_time(self) -> Optional[int]:
        return self.update_time
    
    def get_owner_id(self) -> Optional[int]:
        return self.owner_id
    
    def get_image_url(self) -> Optional[str]:
        return self.image_url
