from io import BytesIO

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from sqlalchemy.orm import Session

from database.db import SessionLocal
from products.schemas import UpdatedProductsInfo, SellerExcelFile, ExcelProductRecord
from products.services.download_xlsx_file import DownloadXLSXFile


class UpdateSellerProductFromXLSX:
    """
    The command to update seller's products from the given
    *.xlsx file. Returns operation statistics: created, updated,
    deleted and errors.
    """

    def __init__(self, seller_xlsx: SellerExcelFile, session: Session = None):
        """
        Receives data about the seller and URL to the Excel file.
        """
        self.seller_xlsx = seller_xlsx
        self.session = session or SessionLocal()
        self.operation_statistics = UpdatedProductsInfo()
        self.xlsx_products: list[ExcelProductRecord | None] = []

    def execute(self) -> UpdatedProductsInfo:
        """
        Executes commands (create, update or delete) and returns its
        statistics.
        """
        workbook = self.get_excel_file()
        with self.session.begin() as session:
            self.process_product_records(session, workbook)
        return self.operation_statistics

    def get_excel_file(self) -> Workbook:
        """
        Loads an Excel file and returns it as a Workbook.
        """
        excel_file_in_bytes = DownloadXLSXFile(self.seller_xlsx.file_link).execute()
        return load_workbook(BytesIO(excel_file_in_bytes))

    def process_product_records(self, session: Session, workbook: Workbook):
        """
        Executes corresponding operations for the products.
        """
