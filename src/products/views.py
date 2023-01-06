from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.services.selectors import get_all_products
from products.dependencies import get_db_session, get_products_criteria
from products.schemas import SellerExcelFile, UpdatedProductsInfo, SellerProduct


products_tag = "Products"
router = APIRouter(
    prefix='/products',
    tags=[products_tag],
)


@router.post('/', response_model=UpdatedProductsInfo)
def update_seller_products(seller_xlsx: SellerExcelFile):
    """
    Updates products in the database. This method can **create**, **delete**
    or **update** already existing products. Parses file from the
    provided link, and returns response with **deleted**, **updated** and
    **created** rows in the db. Also, response has **errors quantity** during
    parsing rows from the Excel file.
    """


@router.get('/', response_model=list[SellerProduct])
def get_products(
        criteria: dict = Depends(get_products_criteria), session: Session = Depends(get_db_session)
):
    """
    Returns products from the database by the provided query parameters. Only
    those products whose `available` column equals **True** are returned.
    """
    return get_all_products(session, **criteria)
