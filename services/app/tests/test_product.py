import pytest
from flask import url_for
from wash.models import Product


@pytest.mark.parametrize('data', [
    {
        'name': 'product 1',
        'description': 'some description',
        'retail_price': 123,
    },
])
def test_add_product(client, data):
    response = client.put(url_for('api.create_product_view'), json=data)
    assert response.status_code == 201

    product_url = response.json['product_url']
    response = client.get(product_url)
    assert response.status_code == 200


@pytest.mark.parametrize('data', [
    {
        'name': 'another name',
        'description': 'another description',
        'retail_price': 333,
    },
])
def test_update_product(client, product, data):
    response = client.put(url_for('api.product_view', product_id=product.id), json=data)
    assert response.status_code == 200

    product_url = response.json['product_url']
    response = client.get(product_url)
    assert response.status_code == 200
    product_data = response.json
    assert product_data['name'] == data['name']
    assert product_data['description'] == data['description']
    assert product_data['retail_price'] == data['retail_price']


def test_delete_product(client, product):
    assert product.id in Product.all()

    response = client.delete(url_for('api.product_view', product_id=product.id))
    assert response.status_code == 204

    assert product.id not in Product.all()
