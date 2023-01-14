import pytest


@pytest.mark.e2e
class TestUpdateSellerProductView:

    @pytest.mark.web
    @pytest.mark.parametrize(
        'file_link', [
            'https://hostname.com/excel_file.xlsx',
            'https://google.com',
            'https://docs.sqlalchemy.org/en/14/index.html'
        ]
    )
    def test_update_seller_products_with_wrong_file_link_returns_400_response(self, test_app, url_for, file_link):
        res = test_app.post(
            url_for('update_seller_products'),
            json={'seller_id': 1, 'file_link': file_link}
        )
        assert res.status_code == 400

    @pytest.mark.parametrize(
        'file_link', [
            'https://',
            '1',
            'some not valid link'
        ]
    )
    def test_if_not_link_provided_422_response_is_returned(self, test_app, url_for, file_link):
        res = test_app.post(
            url_for('update_seller_products'),
            json={'seller_id': 1, 'file_link': file_link}
        )
        assert res.status_code == 422
