from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import boto3


class FileRepository(ABC):
    
    def __init__(self, root_folder: str):
        self._s3 = boto3.client('s3') # in lambdas we don't need to specify credentials.
        self._bucket = 'spotify-activity-data'
        self._cloud_root_folder = root_folder
        self._timedelta = -3
    
    def transform_to_timezone(self, date: str) -> str:
        argentina_time = datetime.fromisoformat(date) + timedelta(hours=self._timedelta)
        return argentina_time.strftime('%Y-%m-%d')
    
    def _build_path_from_now(self) -> str:
        # raw/2023/10/31/
        return self._cloud_root_folder + \
            self.transform_to_timezone(str(datetime.now())).replace('-', '/')
    
    @abstractmethod
    def get(self, type: str):
        pass

    @abstractmethod
    def post(self, type: str, data: str):
        pass

    @abstractmethod
    def delete(self, type: str = None):
        pass