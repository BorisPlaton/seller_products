from exceptions.base_exc import AppException


class XLSXException(AppException):
    """
    Represents a base exception related to the Excel file.
    """


class AllRecordsAreInvalid(XLSXException):
    """
    Shows that all rows in the Excel file are invalid.
    """


class InvalidXLSXHeaders(XLSXException):
    """
    Shows that table's headers are invalid and don't match
    the expected ones.
    """


class XLSXDownloadFailure(XLSXException):
    """
    Download an Excel file from remote source failed.
    """
