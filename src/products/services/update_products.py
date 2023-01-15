from typing import NamedTuple

from fastapi import HTTPException
from openpyxl.workbook import Workbook
from sqlalchemy.orm import Session

from database.models import Product
from database.services.deletes import delete_products_by_records
from database.services.inserts import insert_product_on_conflict_update
from database.services.selectors import get_filtered_products
from database.services.structs import ProductRecord, DeleteProductData
from products.schemas import UpdatedProductsInfo, ExcelProductRecord, SellerExcelFile
from xlsx.download_xlsx_file import DownloadXLSXFile
from xlsx.exceptions import XLSXException
from xlsx.xlsx_parser import ParseXLSXFile


class DeleteUpdateProducts(NamedTuple):
    """
    Has two group of products: first is for the delete operation, the
    second is for create/update operation.
    """
    delete_products: list[DeleteProductData]
    update_products: list[ProductRecord]


class UpdateSellerProductFromXLSX:
    """
    The command to update seller's products from the given
    *.xlsx file. Returns operation statistics: created, updated,
    deleted and errors.
    """

    def __init__(self, session: Session, xlsx_info: SellerExcelFile):
        """
        Receives data about the seller and URL to the Excel file.
        """
        self.session = session
        self.xlsx_info = xlsx_info
        self.data_manipulation_statistics = {
            'updated': 0,
            'created': 0,
            'deleted': 0,
            'errors': 0,
        }

    def execute(self) -> UpdatedProductsInfo:
        """
        Executes commands (create, update or delete) and returns its
        statistics.
        """
        try:
            xlsx_workbook = DownloadXLSXFile(self.xlsx_info.file_link).execute()
            parsed_products = self._get_workbook_product_records(xlsx_workbook)
            self._process_product_records(self._get_product_groups(parsed_products))
            return UpdatedProductsInfo(**self.data_manipulation_statistics)
        except XLSXException as e:
            raise HTTPException(400, str(e))

    def _get_workbook_product_records(self, workbook: Workbook) -> list[ExcelProductRecord]:
        """
        Parses products from the Excel file. If file is correct, returns
        validated product records. Also, updates statistic about errors
        during records validation.
        """
        parsed_records_data = ParseXLSXFile(workbook, ExcelProductRecord).execute()
        self.data_manipulation_statistics['errors'] = parsed_records_data.errors
        return parsed_records_data.products

    def _get_product_groups(self, product_records: list[ExcelProductRecord]) -> DeleteUpdateProducts:
        """
        Filter products for delete and update/create operations.
        """
        products_for_update = []
        products_for_delete = []
        seller_id = self.xlsx_info.seller_id
        for product in product_records:
            product_values = product.dict()
            if product_values.pop('available'):
                products_for_update.append(ProductRecord(**product_values, seller_id=seller_id))
            else:
                products_for_delete.append(DeleteProductData(offer_id=product.offer_id, seller_id=seller_id))
        return DeleteUpdateProducts(delete_products=products_for_delete, update_products=products_for_update)

    def _process_product_records(self, performed_products: DeleteUpdateProducts):
        """
        Executes corresponding operations for the products. Also, updates statistics
        about performed operations.
        """
        deleted_rows_quantity = delete_products_by_records(
            self.session, performed_products.delete_products
        )
        created_rows = insert_product_on_conflict_update(
            self.session, performed_products.update_products
        )
        updated_rows_quantity = get_filtered_products(
            self.session,
            ((~Product.offer_id.in_([row['offer_id'] for row in created_rows])) &
             (Product.seller_id == self.xlsx_info.seller_id))
        ).count()
        self.data_manipulation_statistics.update(
            deleted=deleted_rows_quantity, updated=updated_rows_quantity,
            created=len(created_rows)
        )
