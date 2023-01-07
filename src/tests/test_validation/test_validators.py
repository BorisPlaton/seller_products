from unittest.mock import MagicMock

import pytest

from validation.validators import validate_worksheet_has_content, validate_worksheet_columns_quantity


class TestValidators:

    @pytest.mark.parametrize(
        'max_row', [-2, 0, 1]
    )
    def test_if_worksheet_has_invalid_rows_quantity_exception_raised(self, max_row):
        worksheet_mock = MagicMock()
        worksheet_mock.max_row = max_row
        with pytest.raises(ValueError):
            validate_worksheet_has_content(worksheet_mock)

    def test_if_worksheet_has_valid_rows_exception_not_risen(self):
        worksheet_mock = MagicMock()
        worksheet_mock.max_row = 5
        res = validate_worksheet_has_content(worksheet_mock)
        assert res is None

    def test_validate_worksheet_columns_quantity_raises_exception_if_columns_quantities_dont_equal(self):
        column_quantity = 2
        worksheet_mock = MagicMock()
        worksheet_mock.max_column = column_quantity + 1
        worksheet_mock.min_column = column_quantity - 1
        with pytest.raises(ValueError):
            validate_worksheet_columns_quantity(worksheet_mock, column_quantity)

    def test_validate_worksheet_columns_quantity_doesnt_rise_exception_if_columns_quantities_equal(self):
        column_quantity = 2
        worksheet_mock = MagicMock()
        worksheet_mock.max_column = column_quantity
        worksheet_mock.min_column = column_quantity
        res = validate_worksheet_columns_quantity(worksheet_mock, column_quantity)
        assert res is None
