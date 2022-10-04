from abc import ABC, abstractmethod


# Methods receive generic request objects and extract the fields it requires. Then it returns a response object common to all storage implementations so the Storage class does not have to be aware of all potential reponse types that could be returned depending on a given StorageImp.
class StorageImp(ABC):
    """Abstract base class for various storage implementation classes built for a given paas e.g. Amazon s3."""

    @abstractmethod
    def save(self, upload_request: object) -> str:
        """Saves file to the storage service PaaS and returns the download url"""
        ...

    @abstractmethod
    def process_upload_request(
        self,
    ) -> object:
        """Abstract method which takes in some form of file related request object, and generates an upload request object with parameters specific to the given storage implementation"""
        ...

    @abstractmethod
    def get_item(self, request: object) -> object:
        """Get an item from the storage service PaaS. Should return the raw bytes"""
        ...

    @abstractmethod
    def get_download_url(self, request: object) -> str:
        ...
