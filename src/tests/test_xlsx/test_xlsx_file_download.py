from unittest.mock import patch, MagicMock

import pytest
from openpyxl.workbook import Workbook

from xlsx.download_xlsx_file import DownloadXLSXFile
from xlsx.exceptions import XLSXDownloadFailure


class TestDownloadXLSXFile:

    @patch('requests.get')
    @pytest.mark.parametrize(
        'status_code', [300, 500, 400, 199]
    )
    def test_if_status_code_not_in_range_200_299_raises_exception(self, get_method: MagicMock, status_code):
        mocked_response = MagicMock()
        mocked_response.status_code = status_code
        get_method.return_value = mocked_response
        with pytest.raises(XLSXDownloadFailure):
            DownloadXLSXFile('fake_link')._download_file()

    @patch('requests.get')
    @pytest.mark.parametrize(
        'status_code', [200, 299]
    )
    def test_if_response_is_200_its_content_returned(self, get_method: MagicMock, status_code):
        response_content = 'fake content'
        mocked_response = MagicMock()
        mocked_response.status_code = status_code
        mocked_response.content = response_content
        get_method.return_value = mocked_response
        assert DownloadXLSXFile('fake_link')._download_file() == response_content

    @pytest.mark.web
    @pytest.mark.xfail
    def test_file_is_actually_downloaded_and_returned_as_bytes(self, xlsx_link):
        response = DownloadXLSXFile(xlsx_link).execute()
        assert isinstance(response, Workbook)

    @pytest.mark.parametrize(
        'fake_link', [
            'fake link', 'https://some-wrong-link-123456770-.com/'
        ]
    )
    def test_download_from_unknown_link_raises_download_failure_exception(self, fake_link):
        with pytest.raises(XLSXDownloadFailure):
            DownloadXLSXFile(fake_link)._download_file()
