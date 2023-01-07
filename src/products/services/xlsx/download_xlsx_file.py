import requests
from fastapi import HTTPException
from loguru import logger


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

    def execute(self) -> bytes:
        """
        Downloads the file and returns its content as bytes. If some
        failure occurred during a downloading process, then raises
        a 400 exception.
        """
        try:
            return self._download_file(self.file_link)
        except Exception:
            raise HTTPException(
                detail="Failed to download an Excel file from %s" % self.file_link,
                status_code=400
            )

    @staticmethod
    @logger.catch(Exception, level='ERROR', exclude=ValueError)
    def _download_file(file_link: str):
        """
        Downloads an Excel file and returns its content. If status code
        indicates failure, then raises an Exception.
        """
        response = requests.get(file_link)
        if response.status_code not in range(200, 300):
            logger.warning(
                "Failed to download from %s. Response: %s %s" % (file_link, response.status_code, response.reason)
            )
            raise ValueError("Status code is %s, but expected to be in range 200-299." % response.status_code)
        return response.content
