from time import sleep
import multiprocessing as mp
import threading as thr
import random
import pytest
from flask import url_for, current_app


@pytest.mark.parametrize('price', [random.randint(100, 999)])
def test_retail_price_success(client, product, price):
    price = str(price)

    response = client.get(url_for('api.retail_price_view', product_id=product.id))
    assert response.status_code == 200
    assert response.json['retail_price'] == 0

    response = client.put(url_for('api.retail_price_view'), json={'retail_price': str(price)})
    assert response.status_code == 204

    response = client.get(url_for('api.retail_price_view'))
    assert response.status_code == 200

    new_price = response.json['retail_price']
    assert new_price == price
    assert int(new_price) > 0


@pytest.mark.parametrize('price', [0, -99])
def test_update_retail_price_fail(client, price):
    old_price = current_app.cache.get('retail_price')
    price = str(price)

    with pytest.raises(Exception):
        response = client.put(url_for('api.retail_price_view'), json={'retail_price': str(price)})

    assert current_app.cache.get('retail_price') == old_price


def test_update_reservations(client):
    response = client.put(url_for('api.create_reservation_view'))
    assert response.status_code == 204
    assert client.get(url_for('api.get_reservations_view')).json['reservations_count'], 1

    response = client.delete(url_for('api.cancel_reservation_view'))
    assert response.status_code == 204
    assert client.get(url_for('api.get_reservations_view')).json['reservations_count'], 0


def test_multiple_clients(app, client):
    def proc(idx):
        s = random.randint(1, 5)
        print(f'Thread {idx} sleeps for {s} seconds')
        sleep(s)

        with app.app_context():
            response = client.put(url_for('api.retail_price_view'), json={'retail_price': idx})

        assert response.status_code == 204
        print(f'Process {idx} finished')

    for i in range(1, 100):
        p = thr.Thread(target=proc, args=(i,))
        p.start()
