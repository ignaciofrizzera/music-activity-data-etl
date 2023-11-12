# from dotenv import load_dotenv
from datetime import datetime
from abc import ABC, abstractmethod
import boto3
# import os


class FileRepository(ABC):
    
    def __init__(self, root_folder: str):
        # load_dotenv()
        self._s3 = boto3.client('s3') # in lambdas we don't need to specify credentials.
        self._bucket = 'spotify-activity-data'
        self._cloud_root_folder = root_folder
    
    def _build_path_from_now(self) -> str:
        # raw/2023/10/31/
        return self._cloud_root_folder + datetime.now().strftime('%Y-%m-%d').replace('-', '/')
    
    @abstractmethod
    def get(self, type: str):
        pass

    @abstractmethod
    def post(self, type: str, data: str):
        pass

    @abstractmethod
    def delete(self, type: str = None):
        pass