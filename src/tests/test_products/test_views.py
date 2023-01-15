import pytest
from mixer.backend.sqlalchemy import mixer

from database.models import Seller


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

    @pytest.mark.web
    def test_if_empty_database_delete_and_update_operations_returns_zero(
            self, db_session, test_app, xlsx_link, url_for
    ):
        seller: Seller = mixer.blend(Seller)
        db_session.add(seller)
        db_session.commit()
        res = test_app.post(
            url_for('update_seller_products'),
            json={'seller_id': seller.seller_id, 'file_link': xlsx_link}
        )
        assert res.status_code == 200
        content = res.json()
        assert not content['deleted']
        assert content['created'] == 1
        assert content['errors'] == 1
        assert not content['updated']
