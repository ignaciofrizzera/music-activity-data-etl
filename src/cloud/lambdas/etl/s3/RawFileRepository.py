from typing import List, Dict, Optional
import json

from s3.FileRepository import FileRepository
from s3.FileType import FileType


class RawFileRepository(FileRepository):
    """
    The raw file repository handles the creation, retrieval, and deletion of unstructured data. This
    class interacts with **raw** data of our s3 bucket.
    """

    def __init__(self):
        super().__init__("raw/")
    
    def __get_daily_reports(self):
        """
        Get all reports from the current day from the Raw Repository.

        Returns:
            list: List containing all the reports from the current day.
        """
        return self._s3.list_objects(
            Bucket=self._bucket, Prefix=self._build_path_from_now())

    def __get_hourly(self) -> List[Dict[str, List[Dict[str, str]]]]:
        """
        Get all hourly reports from the current day.
        """
        # raw/2023/10/31/01:00.json, 02:00.json, ...
        activity = []
        day_content = self.__get_daily_reports()
        for file in day_content['Contents']:
            activity.append(json.loads(self._s3.get_object(
                Bucket=self._bucket, Key=file['Key'])['Body'].read().decode('utf-8')))
        return activity

    def __get(self, type: str):
        """
        Private get method to retrieve a file from the Raw Repository. This method
        initializes the file key based on type and the current day and retrieves it from s3.

        Args:
            type (str): The file type to retrieve. Based on the `FileType` enum.
        """
        key = f"{self._build_path_from_now()}/{type}.json"
        return json.loads(self._s3.get_object(
            Bucket=self._bucket, Key=key)['Body'].read().decode('utf-8'))

    def get(self, type: str):
        """
        Get a file from the Raw Repository.

        Args:
            type (str): The file type to retrieve. Based on the `FileType` enum.
        """
        if type == FileType.HOURLY:
            return self.__get_hourly()
        return self.__get(type)

    def post(self, type: str, data: str):
        """
        Post a file in the Raw Repository.

        Args:
            type (str): The file type to post. Based on the `FileType` enum.
            data (str): String representation of the content of the file.
        """
        key = f"{self._build_path_from_now()}/{type}.json"
        self._s3.put_object(Bucket=self._bucket, Key=key, Body=data)

    def delete(self, type: Optional[str] = None):
        """
        Delete a file in the Raw Repository by type.

        Args:
            type (Optional[str]): File type to delete. Based on the `FileType` enum.
                If not provided, all files from the current day are deleted.
        """
        if not type:
            day_content = self.__get_daily_reports()
            for file in day_content['Contents']:
                self._s3.delete_object(Bucket=self._bucket, Key=file['Key'])
        else:
            key = f"{self._build_path_from_now()}({type}).json"
            self._s3.delete_object(Bucket=self._bucket, Key=key)
