from io import BytesIO

import requests
from loguru import logger
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

from products.services.xlsx.exceptions import DownloadFailure


class DownloadXLSXFile:
    """
    Downloads a *.xlsx file and returns it content as
    bytes.
    """

    def __init__(self, file_link: str):
        """
        Stores link to the Excel file.
        """
        self.file_link = file_link

    def execute(self) -> Workbook:
        """
        Downloads the file and returns its content as bytes. If some
        failure occurred during a downloading process, then raises
        an exception.
        """
        try:
            return load_workbook(BytesIO(self._download_file()))
        except DownloadFailure as e:
            raise e
        except Exception:
            raise DownloadFailure("Failed to download file from '%s'." % self.file_link)

    def _download_file(self):
        """
        Downloads an Excel file and returns its content. If status code
        indicates failure, then raises an exception.
        """
        try:
            response = requests.get(self.file_link)
            if response.status_code not in range(200, 300):
                raise DownloadFailure("Failed to download a file from '%s'. Response: %s %s" % (
                    self.file_link, response.status_code, response.reason
                ))
            return response.content
        except Exception as e:
            logger.warning(str(e))
            raise e
