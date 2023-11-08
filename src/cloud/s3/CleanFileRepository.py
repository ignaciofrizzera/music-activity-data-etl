from src.cloud.s3.FileRepository import FileRepository
from botocore.exceptions import ClientError
from io import StringIO
import pandas as pd

class CleanFileRepository(FileRepository):

    def __init__(self):
        super().__init__("clean/")
    
    def __build_path_from_date(self, date: str) -> str:
        # clean/2023/11/2023-11-04.json
        year_month_path = '/'.join(date.split('-')[:2])
        return f"{self._cloud_root_folder}{year_month_path}/{date}.json"

    def get(self, type: str) -> pd.DataFrame:
        try:
            key = self.__build_path_from_date(type)
            data = self._s3.get_object(Bucket=self._bucket, Key=key)['Body'].read().decode('utf-8')
            return pd.read_csv(StringIO(data))
        except ClientError:
            return pd.DataFrame()

    def post(self, type: str, data: str):
        key = self.__build_path_from_date(type)
        self._s3.put_object(Bucket=self._bucket, Key=key, Body=data)

    def delete(self, type: str = None):
        # Why would I want to delete my structured data?
        pass