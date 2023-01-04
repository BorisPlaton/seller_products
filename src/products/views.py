from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.services.selectors import get_filtered_products
from products.dependencies import get_db_session
from products.schemas import SellerProductsExcel, UpdatedProductsInfo, SellerProduct


products_tag = "Products"
router = APIRouter(
    prefix='/products',
    tags=[products_tag],
)


@router.post('/', response_model=UpdatedProductsInfo)
def update_seller_products(
        seller_products: SellerProductsExcel, session: Session = Depends(get_db_session)
):
    """
    Updates products in the database. This method can **create**, **delete**
    or **update** already existing products. Parses file from the
    provided link, and returns response with **deleted**, **updated** and
    **created** rows in the db. Also, response has **errors quantity** during
    parsing rows from the Excel file.
    """


@router.get('/', response_model=list[SellerProduct])
def get_products(
        seller_id: int | None = None, offer_id: int | None = None,
        name_substring: str | None = None, session: Session = Depends(get_db_session)
):
    """
    Returns products from the database by the provided query parameters.
    """
    return get_filtered_products(session, seller_id=seller_id, offer_id=offer_id)

