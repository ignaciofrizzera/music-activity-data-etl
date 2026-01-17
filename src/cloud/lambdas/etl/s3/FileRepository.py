from typing import Optional
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

import boto3


class FileRepository(ABC):
    """
    Interface to define basic operations to interact with storage in s3.
    """

    def __init__(self, root_folder: str):
        """
        Initialize a repository pointing to an specific folder in s3.

        Args:
            root_folder (str): Folder associated to the repository.

        Attributes:
            _s3: Interface to interact with the s3 service.
            _bucket (str): Name of the s3 bucket.
            _cloud_root_folder (str): Name of the folder associated with the repository. Provided in initialization.
            _timedelta (int): Delta time for timezones.
        """
        self._s3 = boto3.client('s3') # in lambdas we don't need to specify credentials.
        self._bucket = 'spotify-activity-data'
        self._cloud_root_folder = root_folder
        self._timedelta = -3

    def transform_to_timezone(self, date: str) -> str:
        """
        Transform a date into argentinian standard time (UTC-3).

        Args:
            date (str): String representation of the date to convert.

        Returns:
            str: String representation of the date in argentinian standard time.
        """
        argentina_time = datetime.fromisoformat(date) + timedelta(hours=self._timedelta)
        return argentina_time.strftime('%Y-%m-%d')

    def _build_path_from_now(self) -> str:
        """
        Generate a path from the root folder associated and the current day.

        Returns:
            str: Path generated.
        """
        # e.g: raw/2023/10/31/
        return self._cloud_root_folder + \
            self.transform_to_timezone(str(datetime.now())).replace('-', '/')

    @abstractmethod
    def get(self, type: str):
        """
        Retrieve a file from the repository.

        Args:
            type (str): The file type to retrieve. Based on the `FileType` enum.
        """
        pass

    @abstractmethod
    def post(self, type: str, data: str):
        """
        Post a file in the repository.

        Args:
            type (str): The file type to retrieve. Based on the `FileType` enum.
            data (str): Content of the file.
        """
        pass

    @abstractmethod
    def delete(self, type: Optional[str] = None):
        """
        Delete a file from the repository.

        Args:
            type (Optional[str]): The file type to delete. Based on the `FileType` enum.
        """
        pass
