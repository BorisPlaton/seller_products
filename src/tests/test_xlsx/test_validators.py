from unittest.mock import MagicMock

import pytest

from validation.exceptions import ValidationException
from xlsx.validators import (
    validate_worksheet_has_content, validate_worksheet_columns_size,
    validate_worksheet_starts_from_left_top_corner
)


class TestValidators:

    @pytest.mark.parametrize(
        'min_row, max_row', [
            (1, 2),
            (1, 1),
        ]
    )
    def test_if_worksheet_has_invalid_rows_quantity_exception_raised(self, min_row, max_row):
        worksheet_mock = MagicMock()
        worksheet_mock.min_row = min_row
        worksheet_mock.max_row = max_row
        with pytest.raises(ValidationException):
            validate_worksheet_has_content(worksheet_mock)

    def test_if_worksheet_has_valid_rows_exception_not_risen(self):
        worksheet_mock = MagicMock()
        worksheet_mock.max_row = 5
        worksheet_mock.min_row = 1
        res = validate_worksheet_has_content(worksheet_mock)
        assert res is None

    def test_validate_worksheet_columns_quantity_raises_exception_if_columns_quantities_dont_equal(self):
        column_quantity = 2
        worksheet_mock = MagicMock()
        worksheet_mock.max_column = column_quantity + 1
        with pytest.raises(ValidationException):
            validate_worksheet_columns_size(worksheet_mock, column_quantity)

    def test_validate_worksheet_columns_quantity_doesnt_rise_exception_if_columns_quantities_equal(self):
        column_quantity = 2
        worksheet_mock = MagicMock()
        worksheet_mock.max_column = column_quantity
        res = validate_worksheet_columns_size(worksheet_mock, column_quantity)
        assert res is None

    @pytest.mark.parametrize(
        'min_row, min_column',
        [
            (1, 2),
            (2, 1),
            (10, 4),
        ]
    )
    def test_validate_worksheet_starts_from_left_top_corner_rises_exception_if_not_first_cell_is_min_row_and_col(
            self, min_row, min_column
    ):
        worksheet_mock = MagicMock()
        worksheet_mock.min_column = min_column
        worksheet_mock.min_row = min_row
        with pytest.raises(ValidationException):
            validate_worksheet_starts_from_left_top_corner(worksheet_mock)

    def test_validate_worksheet_on_first_cell_doesnt_rise_exception_if_min_and_max_is_one(self):
        worksheet_mock = MagicMock()
        worksheet_mock.min_column = 1
        worksheet_mock.min_row = 1
        res = validate_worksheet_starts_from_left_top_corner(worksheet_mock)
        assert res is None
