from pydantic import BaseModel, AnyUrl, validator, Field


class SellerProductsExcel(BaseModel):
    """
    Represents a link to the *.xlsx file with seller id in
    the database.
    """
    seller_id: int
    file_link: AnyUrl

    class Config:
        schema_extra = {
            'example': {
                'seller_id': 1,
                'file_link': 'https://hostname.com/excel_file.example'
            }
        }


class SellerProduct(BaseModel):
    """
    The product that is represented in the Excel file.
    """
    offer_id: int = Field(ge=1)
    name: str
    price: float = Field(ge=1)
    quantity: int = Field(ge=0)
    available: bool

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'offer_id': 1,
                'name': "Book",
                'price': 450.5,
                'available': True
            }
        }

    @validator('price')
    def price_is_greater_than_zero(cls, value: float):
        return float("{:.2f}".format(value))


class UpdatedProductsInfo(BaseModel):
    """
    Provides information about updating products.
    """
    created: int | None = None
    updated: int | None = None
    deleted: int | None = None
    errors: int | None = None

    class Config:
        schema_extra = {
            'example': {
                'created': 5,
                'updated': 1,
                'deleted': 3,
                'errors': 2,
            }
        }
