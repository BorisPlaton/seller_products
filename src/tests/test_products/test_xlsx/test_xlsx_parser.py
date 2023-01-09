from unittest.mock import MagicMock, Mock

import pytest
from openpyxl.workbook import Workbook
from pydantic import BaseModel, ValidationError

from products.schemas import ExcelProductRecord
from products.services.xlsx.download_xlsx_file import DownloadXLSXFile
from products.services.xlsx.xlsx_parser import SetWorksheetHeader, ParseXLSXRowRecords, ParseXLSXFile
from validation.exceptions import ValidationException


class TestSetWorksheetHeader:

    def test_command_raises_exception_if_cell_has_unknown_header(self):
        headers = ['header1', 'header2']
        first_cell = MagicMock()
        first_cell.value = 'unknown header'
        columns_map = {}
        with pytest.raises(ValueError):
            SetWorksheetHeader([first_cell], columns_map, headers=headers).execute()

    def test_command_set_values_in_the_given_map_dict(self):
        headers = ['header1', 'header2']
        first_cell = MagicMock()
        second_cell = MagicMock()
        first_cell.value = headers[0]
        second_cell.value = headers[1]
        columns_map = {}
        SetWorksheetHeader([first_cell, second_cell], columns_map, headers=headers).execute()
        assert columns_map[0] == headers[0]
        assert columns_map[1] == headers[1]


class TestParseXLSXRowRecords:

    @pytest.fixture(scope='class')
    def record_class(self):
        class Record(BaseModel):
            record_id: int
            name: str
            available: bool

        return Record

    @pytest.fixture
    def columns_map(self, record_class):
        return {
            column_num: column_type for column_num, column_type
            in enumerate(record_class.__annotations__)
        }

    @pytest.fixture(scope='class')
    def records_row(self, record_class):
        cells = []
        for record_type in record_class.__annotations__.values():
            cell = Mock()
            if record_type is int:
                cell.value = 10
            elif record_type is str:
                cell.value = 'long string'
            elif record_type is bool:
                cell.value = True
            cells.append(cell)
        return cells

    def test_exception_is_risen_if_cells_has_invalid_type(self):
        class Record(BaseModel):
            header: int

        cell = MagicMock()
        cell.value = 'some string'
        columns_map = {0: 'header'}
        records_row = [cell]
        with pytest.raises(ValidationError):
            ParseXLSXRowRecords(records_row, columns_map, record_class=Record).execute()

    def test_if_credentials_are_valid_returns_given_record_class(self, record_class, records_row, columns_map):
        record_instance = ParseXLSXRowRecords(records_row, columns_map, record_class=record_class).execute()
        assert isinstance(record_instance, record_class)
        for column_num, column_name in columns_map.items():
            assert getattr(record_instance, column_name) == records_row[column_num].value


class TestParseXLSXFile:

    def test_xlsx_file_is_parsed_properly_from_constructed(self, workbook, worksheet_record_class):
        parsed_records_stat = ParseXLSXFile(workbook, worksheet_record_class).execute()
        assert not parsed_records_stat.errors
        for record in parsed_records_stat.products:
            assert isinstance(record, worksheet_record_class)

    @pytest.mark.xfail
    @pytest.mark.web
    def test_xlsx_file_is_parsed_from_downloaded_file(self, xlsx_link):
        workbook = DownloadXLSXFile(xlsx_link).execute()
        parsed_records_stat = ParseXLSXFile(workbook, ExcelProductRecord).execute()
        assert parsed_records_stat.errors == 1
        assert len(parsed_records_stat.products) == 2
        for record in parsed_records_stat.products:
            assert isinstance(record, ExcelProductRecord)

    def test_exception_risen_if_workbook_has_empty_worksheet(self, worksheet_record_class):
        with pytest.raises(ValidationException):
            ParseXLSXFile(Workbook(), worksheet_record_class).execute()
