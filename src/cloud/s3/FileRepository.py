from dotenv import load_dotenv
from datetime import datetime
import boto3
import os


class FileRepository:
    
    def __init__(self, root_folder: str):
        load_dotenv()
        self._s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_ACCESS_SECRET_KEY'), region_name='sa-east-1')
        self._bucket = 'spotify-activity-data'
        self._cloud_root_folder = root_folder
    
    def _build_path_from_now(self) -> str:
        # raw/2023/10/31/
        return self._cloud_root_folder + datetime.now().strftime('%Y-%m-%d').replace('-', '/')