from enum import StrEnum


class FileType(StrEnum):
    """
    Enum containing the different file types of the ETL.
    """
    HOURLY = 'hourly'
    UNSTRUCTURED = 'unstructured_report'
    STRUCTURED = 'structured_report'
