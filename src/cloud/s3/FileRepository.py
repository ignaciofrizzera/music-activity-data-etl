from dotenv import load_dotenv
from datetime import datetime
from typing import List, Dict
import json
import boto3
import os


# Raw file repository.
class FileRepository:
    
    def __init__(self):
        load_dotenv()
        self.__s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_ACCESS_SECRET_KEY'), region_name='sa-east-1')
        self.__bucket = 'spotify-activity-data'
        self.__cloud_root_folder = 'raw/'
    
    def __build_path_from_now(self) -> str:
        # raw/2023/10/31/
        return self.__cloud_root_folder + datetime.now().strftime('%Y-%m-%d').replace('-', '/')

    def get(self) -> List[Dict[str, List[Dict[str, str]]]]:
        # raw/2023/10/31/01:00.json, 02:00.json, ...
        activity = []
        prefix = self.__build_path_from_now()
        day_content = self.__s3.list_objects(Bucket=self.__bucket, Prefix=prefix)
        for file in day_content['Contents']:
            activity.append(json.loads(self.__s3.get_object(
                Bucket=self.__bucket, Key=file['Key'])['Body'].read().decode('utf-8')))
        return activity

    # TODO: initially this FileRepository (maybe do one for raw, other for clean)
    # shouldn't have a post, since the data is gathered from the step-function, there should
    # be no reason whatsoever for this service to publish files/data.
    # def post():
    #     pass

    def delete():
        pass