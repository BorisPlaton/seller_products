import requests
from openpyxl.workbook import Workbook
from requests.exceptions import RequestException

from validation.utils import get_validator_name
from xlsx.exceptions import XLSXDownloadFailure
from xlsx.validators import validate_content_is_workbook
from xlsx.xlsx_validation import XLSXValidationMixin


class DownloadXLSXFile(XLSXValidationMixin):
    """
    Downloads a *.xlsx file and returns it content as
    bytes.
    """

    def __init__(self, file_link: str):
        """
        Stores link to the Excel file.
        """
        super().__init__()
        self.file_link = file_link
        self.validators = [
            validate_content_is_workbook
        ]

    def execute(self) -> Workbook:
        """
        Downloads the file and returns its content as bytes. If some
        failure occurred during a downloading process, then raises
        an exception.
        """
        self.validate(content=self._download_file())
        return self.validators_returns[get_validator_name(validate_content_is_workbook)]

    def _download_file(self):
        """
        Downloads an Excel file and returns its content. If status code
        indicates failure, then raises an exception.
        """
        try:
            response = requests.get(self.file_link)
            if response.status_code not in range(200, 300):
                raise XLSXDownloadFailure("Failed to download a file from '%s'. Response: %s %s" % (
                    self.file_link, response.status_code, response.reason
                ))
            return response.content
        except RequestException as e:
            raise XLSXDownloadFailure(str(e))
