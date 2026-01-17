import json

from s3.RawFileRepository import RawFileRepository
from s3.FileType import FileType


def transform():
   # Due to Spotify deprecating many endpoints, this function is not pretty straightforward.
   file_repository = RawFileRepository()
   data = file_repository.get(FileType.UNSTRUCTURED)
   file_repository.post(FileType.STRUCTURED, json.dumps(data))


def lambda_handler(event, context):
   transform()
