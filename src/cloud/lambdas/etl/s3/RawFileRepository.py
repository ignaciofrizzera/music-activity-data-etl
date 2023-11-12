from typing import List, Dict, Any
from s3.FileRepository import FileRepository
from s3.FileType import FileType
import json

class RawFileRepository(FileRepository):
    """Raw files repository (hourly reports and unstructured data)"""
    
    def __init__(self):
        super().__init__("raw/")
    
    def __get_daily_reports(self):
        return self._s3.list_objects(
            Bucket=self._bucket, Prefix=self._build_path_from_now())

    def __get_hourly(self) -> List[Dict[str, List[Dict[str, str]]]]:
        # raw/2023/10/31/01:00.json, 02:00.json, ...
        activity = []
        day_content = self.__get_daily_reports()
        for file in day_content['Contents']:
            activity.append(json.loads(self._s3.get_object(
                Bucket=self._bucket, Key=file['Key'])['Body'].read().decode('utf-8')))
        return activity

    def __get(self, type: str):
        key = f"{self._build_path_from_now()}/{type}.json"
        return json.loads(self._s3.get_object(
            Bucket=self._bucket, Key=key)['Body'].read().decode('utf-8'))

    def get(self, type: str):
        if type == FileType.HOURLY:
            return self.__get_hourly() 
        return self.__get(type)
    
    def post(self, type: str, data: str):
        key = f"{self._build_path_from_now()}/{type}.json"
        self._s3.put_object(Bucket=self._bucket, Key=key, Body=data)

    def delete(self, type: str = None):
        if not type:
            day_content = self.__get_daily_reports()
            for file in day_content['Contents']:
                self._s3.delete_object(Bucket=self._bucket, Key=file['Key'])
        else:
            key = f"{self._build_path_from_now()}({type}).json"
            self._s3.delete_object(Bucket=self._bucket, Key=key)