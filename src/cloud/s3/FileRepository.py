from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict
import json
import boto3
import os


class FileRepository:
    """Raw files repository (hourly reports and unstructured data)"""
    
    def __init__(self):
        load_dotenv()
        self.__s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_ACCESS_SECRET_KEY'), region_name='sa-east-1')
        self.__bucket = 'spotify-activity-data'
        self.__cloud_root_folder = 'raw/'
    
    def __build_path_from_now(self) -> str:
        # raw/2023/10/31/
        return self.__cloud_root_folder + datetime.now().strftime('%Y-%m-%d').replace('-', '/')
    
    def __get_daily_reports(self):
        return self.__s3.list_objects(
            Bucket=self.__bucket, Prefix=self.__build_path_from_now())

    def get(self) -> List[Dict[str, List[Dict[str, str]]]]:
        # raw/2023/10/31/01:00.json, 02:00.json, ...
        activity = []
        day_content = self.__get_daily_reports()
        for file in day_content['Contents']:
            activity.append(json.loads(self.__s3.get_object(
                Bucket=self.__bucket, Key=file['Key'])['Body'].read().decode('utf-8')))
        return activity

    def post_unstructured(self, data: str):
        # raw/2023/10/31/report.json
        key = f"{self.__build_path_from_now()}/report.json"
        res = self.__s3.put_object(Bucket=self.__bucket, Key=key, Body=data)
        if res['ResponseMetadata']['HTTPStatusCode'] == 200:
            self.__delete_hourly_reports(key)
    
    def __delete_hourly_reports(self, key: str):
        day_content = self.__get_daily_reports()
        for file in day_content['Contents']:
            if file['Key'] != key:
                self.__s3.delete_object(Bucket=self.__bucket, Key=file['Key'])