from typing import Optional
import json

from s3.FileRepository import FileRepository
import pandas as pd
from botocore.exceptions import ClientError


class CleanFileRepository(FileRepository):
    """
    The clean file repository handles the creation, retrieval, and deletion of structured data. This
    class interacts with **clean** data of our s3 bucket.

    The data managed by this repository is used by final consumers of the information.
    """

    def __init__(self):
        super().__init__("clean/")

    def __build_path_from_date(self, date: str) -> str:
        """
        Generate a path from the repository root folder and the current data.

        Args:
            date (str): String representation of a date.
        """
        # clean/2023/11/2023-11-04.json
        year_month_path = '/'.join(date.split('-')[:2])
        return f"{self._cloud_root_folder}{year_month_path}/{date}.json"

    def get(self, type: str) -> pd.DataFrame:
        """
        Retrieve a file from the Clean Repository and return it as a pandas DataFrame.

        Args:
            type (str): The file type to retrieve. Based on the `FileType` enum.

        Returns:
            pd.DataFrame: Content of the file represented as a pandas DataFrame.
        """
        try:
            key = self.__build_path_from_date(type)
            data = self._s3.get_object(Bucket=self._bucket, Key=key)['Body'].read().decode('utf-8')
            return pd.DataFrame(json.loads(data))
        except ClientError:
            return pd.DataFrame()

    def post(self, type: str, data: str):
        """
        Post a file in the Clean Repository.

        Args:
            type (str): The file type to post. Based on the `FileType` enum.
            data (str): String representation of the content of the file.
        """
        key = self.__build_path_from_date(type)
        self._s3.put_object(Bucket=self._bucket, Key=key, Body=data)

    def delete(self, type: Optional[str] = None):
        """
        Delete a file from the repository. For now this operation is not supported.

        Args:
            type (Optional[str]): The file type to delete. Based on the `FileType` enum.

        Raises:
            NotImplementedError: On every single call. This method is not yet supported in the `CleanFileRepository`.
        """
        # Why would I want to delete my structured data?
        raise NotImplementedError("The `delete` method is not implemented in the CleanFileRepository.")
