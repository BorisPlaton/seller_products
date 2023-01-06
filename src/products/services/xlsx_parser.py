from dataclasses import dataclass
from typing import Iterable

from openpyxl.cell import Cell
from openpyxl.workbook import Workbook

from products.schemas import ExcelProductRecord
from products.services.validation_mixin import ValidationMixin


@dataclass
class ParsedRecords:
    """
    Represents information about the parsed Excel file.
    It has list of products and errors quantity during
    parsing.
    """
    products: list[ExcelProductRecord]
    errors: int


class ParseXLSXFile(ValidationMixin):
    """
    Parses an Excel file and returns record rows. Parses only the
    first worksheet and starts from the A1 cell.
    """

    def __init__(self, workbook: Workbook):
        """
        Stores workbook with product records.
        """
        self.workbook = workbook
        self.columns_map = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
        }
        self.validators = [
            self._validate_table_has_content,
            self._validate_columns_quantity,
        ]

    def execute(self) -> ParsedRecords:
        """
        Parses an Excel file and returns validated product records
        and errors quantity during parsing.
        """
        self.validate()

    def _validate_columns_quantity(self):
        pass

    def _validate_table_has_content(self):
        pass


class ParseXLSXRow(ValidationMixin):
    """
    Parses a single row in the worksheet and returns it. If
    an error occurs, raises an exception.
    """

    def __init__(self, record_row: Iterable[Cell]):
        self.record_row = record_row
        self.validators = [
            self._validate_cells_quantity
        ]

    def execute(self):
        self.validate()

    def _validate_cells_quantity(self):
        pass
