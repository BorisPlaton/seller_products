from sqlalchemy.orm import Session

from database.db import SessionLocal
from products.schemas import UpdatedProductsInfo, ExcelProductRecord


class UpdateSellerProductFromXLSX:
    """
    The command to update seller's products from the given
    *.xlsx file. Returns operation statistics: created, updated,
    deleted and errors.
    """

    def __init__(self, seller_id: int, products: list[ExcelProductRecord], session: Session = None):
        """
        Receives data about the seller and URL to the Excel file.
        """
        self.products = products
        self.seller_id = seller_id
        self.session = session or SessionLocal()

    def execute(self) -> UpdatedProductsInfo:
        """
        Executes commands (create, update or delete) and returns its
        statistics.
        """
        self._process_product_records()
        return self.operation_statistics

    def _process_product_records(self):
        """
        Executes corresponding operations for the products.
        """
