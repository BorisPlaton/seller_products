from openpyxl.worksheet.worksheet import Worksheet


def validate_worksheet_has_content(worksheet: Worksheet):
    """
    Validates that worksheet has content inside. It is checked by
    rows quantity.
    """
    worksheet_rows_quantity = worksheet.max_row
    if worksheet_rows_quantity <= 1:
        raise ValueError(
            "Worksheet rows quantity must be greater than one. Not %s." %
            worksheet_rows_quantity
        )


def validate_worksheet_columns_quantity(worksheet: Worksheet, expected_columns_quantity: int):
    """
    Validates that the worksheet has fixed quantity of columns. If
    not, raises an exception.
    """
    max_columns_quantity = worksheet.max_column
    min_columns_quantity = worksheet.min_column
    if not (
            expected_columns_quantity ==
            max_columns_quantity ==
            min_columns_quantity
    ):
        raise ValueError(
            f"Worksheet must have exactly {expected_columns_quantity} columns. "
            f"But has {max_columns_quantity} max. columns and {min_columns_quantity} min columns."
        )
