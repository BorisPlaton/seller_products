from dataclasses import dataclass
from functools import cached_property
from typing import TypeVar

from openpyxl.cell import Cell
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pydantic import BaseModel, ValidationError

from xlsx.exceptions import AllRecordsAreInvalid, InvalidXLSXHeaders
from xlsx.validators import (
    validate_worksheet_starts_from_left_top_corner,
    validate_worksheet_columns_size, validate_worksheet_has_content,
    validate_rows_dont_have_duplicates
)
from xlsx.xlsx_validation import XLSXValidationMixin


RecordClass = TypeVar('RecordClass', bound=BaseModel)


@dataclass
class ParsedRecords:
    """
    Represents information about the parsed Excel file.
    It has list of products and errors quantity during
    parsing.
    """
    products: list[RecordClass]
    errors: int


class ParseXLSXFile(XLSXValidationMixin):
    """
    Parses an Excel file and returns record rows. Parses only the
    first worksheet and starts from the A1 cell.
    """

    def __init__(self, workbook: Workbook, record_class: type[RecordClass]):
        """
        Stores workbook with product records. The `record_class` argument is used for
        validating the row in the workbook.
        """
        super().__init__()
        self.workbook = workbook
        self.record_class = record_class
        self.columns_map = {i: None for i, _ in enumerate(self.worksheet_headers)}
        self.validators = [
            validate_worksheet_has_content,
            validate_worksheet_columns_size,
            validate_worksheet_starts_from_left_top_corner,
        ]

    def execute(self) -> ParsedRecords:
        """
        Parses an Excel file and returns validated product records
        and errors quantity during parsing.
        """
        self.validate()
        self._define_columns_map()
        return self._parse_file_records()

    @property
    def worksheet(self) -> Worksheet:
        """
        Returns the first worksheet in the workbook. It is used
        to search the content.
        """
        return self.workbook.worksheets[0]

    @cached_property
    def worksheet_headers(self):
        """
        Returns headers that are expected to be in the worksheet first row.
        """
        return [name for name in self.record_class.__annotations__]

    def get_validators_kwargs(self):
        return {
            'worksheet': self.worksheet,
            'expected_columns_quantity': len(self.columns_map)
        }

    def _define_columns_map(self):
        """
        Sets values in the columns map dictionary.
        """
        first_row = next(self.worksheet.iter_rows())
        SetWorksheetHeader(first_row, self.columns_map, headers=self.worksheet_headers).execute()

    def _parse_file_records(self) -> ParsedRecords:
        """
        Parses a *.xlsx file and returns parsed records with errors
        quantity.
        """
        product_records = []
        errors_quantity = 0
        for row_index, row in enumerate(self.worksheet.iter_rows(2), start=2):
            try:
                parsed_record = ParseXLSXRowRecords(
                    row, self.columns_map, record_class=self.record_class,
                    row_index=row_index
                ).execute()
                product_records.append(parsed_record)
            except ValidationError:
                errors_quantity += 1
        if not product_records:
            raise AllRecordsAreInvalid("All rows in the excel file are invalid.")
        return ParsedRecords(products=product_records, errors=errors_quantity)


class BaseParseXLSXRow(XLSXValidationMixin):
    """
    Defines a base signature for the another row parses.
    """

    def __init__(self, records_row: tuple[Cell], columns_map: dict):
        """
        Saves records to be parsed.
        """
        super().__init__()
        self.records_row = records_row
        self.columns_map = columns_map


class SetWorksheetHeader(BaseParseXLSXRow):
    """
    Parses the first row and returns map of columns number to
    column name.
    """

    def __init__(self, *args, headers: list[str]):
        super().__init__(*args)
        self.headers = headers

    def execute(self):
        """
        Executes the command and returns a map.
        """
        return self._create_columns_map()

    def _create_columns_map(self):
        """
        Iterates over the first row and constructs a map.
        """
        for column_num, column in enumerate(self.records_row):
            header_name = column.value
            if header_name not in self.headers:
                raise InvalidXLSXHeaders("First row has an unknown header %s." % header_name)
            self.columns_map[column_num] = header_name


class ParseXLSXRowRecords(BaseParseXLSXRow):
    """
    Parses a single row in the worksheet and returns it. If
    an error occurs, raises an exception.
    """

    def __init__(self, *args, record_class: type[RecordClass], row_index: int):
        super().__init__(*args)
        self.record_class = record_class
        self.row_index = row_index
        self.validators = [
            validate_rows_dont_have_duplicates()
        ]

    def execute(self) -> RecordClass:
        """
        Firstly, validates the row, and then returns parsed record. If
        some validation doesn't pass, raises an exception.
        """
        record_instance = self._get_record_instance()
        self.validate(record_row=record_instance)
        return record_instance

    def _get_record_instance(self) -> RecordClass:
        """
        Returns validated record class with values from the corresponding
        columns.
        """
        columns_value = {
            self.columns_map[cell_num]: cell.value for cell_num, cell
            in enumerate(self.records_row)
        }
        return self.record_class(**columns_value)

    def get_validators_kwargs(self) -> dict:
        return {'row_index': self.row_index}
