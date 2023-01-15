from unittest.mock import patch, MagicMock

from products.services.update_products import UpdateSellerProductFromXLSX


class TestUpdateProducts:

    @patch('xlsx.xlsx_parser.ParseXLSXFile.execute')
    def test_get_workbook_product_records_updates_errors_statistic_and_returns_products(
            self, parse_mock: MagicMock
    ):
        errors = 4
        products = [1, 2, 3]
        parse_statistic = MagicMock()
        parse_statistic.errors = errors
        parse_statistic.products = products
        parse_mock.return_value = parse_statistic
        command = UpdateSellerProductFromXLSX('fake', 'fake')
        workbook_products = command._get_workbook_product_records('fake')
        assert command.data_manipulation_statistics['errors'] == errors
        assert workbook_products == products

    @patch('database.services.structs.DeleteProductData.__new__')
    @patch('database.services.structs.ProductRecord.__new__')
    def test_get_product_groups_relies_on_available_attribute(self, product_mock: MagicMock, delete_mock: MagicMock):
        update_product = MagicMock()
        delete_product = MagicMock()
        update_product_dict = {'available': True}
        delete_product_dict = {'available': False}
        update_product.dict.return_value = update_product_dict
        delete_product.dict.return_value = delete_product_dict

        product_mock.return_value = update_product
        delete_mock.return_value = delete_product

        xlsx_info = MagicMock()
        xlsx_info.seller_id = 1

        res = UpdateSellerProductFromXLSX('fake', xlsx_info)._get_product_groups([update_product, delete_product])
        assert res.update_products[0] is update_product
        assert res.delete_products[0] is delete_product
