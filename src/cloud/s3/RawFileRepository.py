from typing import List, Dict, Any
from src.cloud.s3.FileRepository import FileRepository
import json

class RawFileRepository(FileRepository):
    """Raw files repository (hourly reports and unstructured data)"""
    
    def __init__(self):
        super().__init__("raw/")
    
    def __get_daily_reports(self):
        return self._s3.list_objects(
            Bucket=self._bucket, Prefix=self._build_path_from_now())

    def get_hourly(self) -> List[Dict[str, List[Dict[str, str]]]]:
        # raw/2023/10/31/01:00.json, 02:00.json, ...
        activity = []
        day_content = self.__get_daily_reports()
        for file in day_content['Contents']:
            activity.append(json.loads(self._s3.get_object(
                Bucket=self._bucket, Key=file['Key'])['Body'].read().decode('utf-8')))
        return activity

    def get_daily(self) -> List[Dict[str, Any]]:
        key = f"{self._build_path_from_now()}/report.json"
        return json.loads(self._s3.get_object(
            Bucket=self._bucket, Key=key)['Body'].read().decode('utf-8'))

    def post_unstructured(self, data: str):
        # raw/2023/10/31/report.json
        key = f"{self._build_path_from_now()}/report.json"
        self._s3.put_object(Bucket=self._bucket, Key=key, Body=data)
        
    def get_daily_structured(self) -> List[Dict[str, Any]]:
        key = f"{self._build_path_from_now()}/structured_report.json"
        return json.loads(self._s3.get_object(
            Bucket=self._bucket, Key=key)['Body'].read().decode('utf-8'))
    
    def post_structured(self, data: str):
        # raw/2023/10/31/structured_report.json
        key = f"{self._build_path_from_now()}/structured_report.json"
        self._s3.put_object(Bucket=self._bucket, Key=key, Body=data)

    # def __delete_hourly_reports(self, key: str):
    #     day_content = self.__get_daily_reports()
    #     for file in day_content['Contents']:
    #         if file['Key'] != key:
    #             self.__s3.delete_object(Bucket=self.__bucket, Key=file['Key'])