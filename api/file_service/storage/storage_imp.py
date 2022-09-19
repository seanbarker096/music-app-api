from abc import ABC, abstractmethod

"""Abstract base class for various storage implementation classes built for a given paas e.g. Amazon s3. 
"""
class StorageImp(ABC):
    
    @abstractmethod
    def save(self, upload_request: object):
        ...

    '''Abstract method which takes in some form of file related request object, and generates an upload request object with parameters specific to the given storage implementation'''
    @abstractmethod
    def process_upload_request(self, ) -> object:
        ...
