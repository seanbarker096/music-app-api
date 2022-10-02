from abc import ABC, abstractmethod

from api.file_service.typings.typings import FileCreateRequest


class StorageImp(ABC):
    """Abstract base class for various storage implementation classes built for a given paas e.g. Amazon s3."""

    @abstractmethod
    def save(self, upload_request: FileCreateRequest) -> str:
        """Saves file to the storage service PaaS and returns the download url"""
        ...

    @abstractmethod
    def process_upload_request(
        self,
    ) -> object:
        """Abstract method which takes in some form of file related request object, and generates an upload request object with parameters specific to the given storage implementation"""
        ...

    @abstractmethod
    def get_item(self) -> any:
        """Get an item from the storage service PaaS"""
        ...
