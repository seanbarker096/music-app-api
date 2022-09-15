from abc import ABC, abstractmethod

"""Abstract base class for various storage implementation classes built for a given paas e.g. Amazon s3. 
"""
class StorageImp(ABC):
    
    @abstractmethod
    def save(self):
        pass
