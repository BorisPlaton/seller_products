from openpyxl.worksheet.worksheet import Worksheet

from validation.exceptions import ValidationException


def validate_worksheet_has_content(worksheet: Worksheet):
    """
    Validates that worksheet has content inside. It is checked by
    rows quantity.
    """
    worksheet_rows_quantity = worksheet.max_row - worksheet.min_row
    if worksheet_rows_quantity <= 1:
        raise ValidationException(
            "Worksheet rows quantity must be greater than one. Not %s." %
            worksheet_rows_quantity
        )


def validate_worksheet_starts_from_left_top_corner(worksheet: Worksheet):
    """
    Validates that worksheet starts from the A1 cell.
    """
    if worksheet.min_column != 1 or worksheet.min_row != 1:
        raise ValidationException(
            "The worksheet must start from the A1 cell."
        )


def validate_worksheet_columns_size(worksheet: Worksheet, expected_columns_quantity: int):
    """
    Validates that the worksheet has fixed quantity of columns. If
    not, raises an exception.
    """
    max_columns_quantity = worksheet.max_column
    if max_columns_quantity != expected_columns_quantity:
        raise ValidationException(
            f"Worksheet must have exactly {expected_columns_quantity} columns."
            f" But has {max_columns_quantity}"
        )
