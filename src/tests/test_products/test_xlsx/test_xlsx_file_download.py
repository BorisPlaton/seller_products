from io import BytesIO
from unittest.mock import patch, MagicMock

import pytest
from fastapi import HTTPException
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

from products.services.xlsx.download_xlsx_file import DownloadXLSXFile


class TestDownloadXLSXFile:

    @patch('requests.get')
    @pytest.mark.parametrize(
        'status_code', [300, 500, 400, 199]
    )
    def test_if_status_code_not_in_range_200_299_raises_value_error(self, get_method: MagicMock, status_code):
        mocked_response = MagicMock()
        mocked_response.status_code = status_code
        get_method.return_value = mocked_response
        with pytest.raises(ValueError):
            DownloadXLSXFile._download_file('fake_link')

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
        assert DownloadXLSXFile._download_file('fake_link') == response_content

    @patch('products.services.xlsx.download_xlsx_file.DownloadXLSXFile._download_file')
    def test_if_execute_method_failed_raises_http_exception(self, method_mock: MagicMock):
        method_mock.side_effect = Exception()
        with pytest.raises(HTTPException) as e:
            DownloadXLSXFile('fake link').execute()
        assert e.value.status_code == 400

    @pytest.mark.web
    @pytest.mark.xfail(reason="Link with Excel file no longer exist.")
    def test_file_is_actually_downloaded_and_returned_as_bytes(self):
        response = DownloadXLSXFile(
            'https://docs.google.com/spreadsheets/d/11hqrBYKDtxTe7-NbPGDYMSVks-SO6f9b/export?format=xlsx&gid=1225459015'
        ).execute()
        assert isinstance(response, bytes)
        wb = load_workbook(BytesIO(response))
        assert isinstance(wb, Workbook)
