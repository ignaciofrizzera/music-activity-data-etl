from src.cloud.s3.FileRepository import FileRepository

class CleanFileRepository(FileRepository):

    def __init__(self):
        super().__init__("clean/")