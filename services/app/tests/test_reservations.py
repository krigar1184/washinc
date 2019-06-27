import random
import threading as thr
from time import sleep
import pytest
from flask import url_for
from wash.models import Reservation


def test_update_reservations(app, client, product):
    response = client.put(url_for('api.reservation_view', product_id=product.id))
    assert response.status_code == 201

    response = client.get(url_for('api.reservation_view', product_id=product.id))
    assert len(response.json) == 1

    response = client.put(url_for('api.reservation_view', product_id=product.id))
    assert response.status_code == 201

    response = client.get(url_for('api.reservation_view', product_id=product.id))
    assert len(response.json) == 2

    response = client.delete(url_for('api.reservation_view', product_id=product.id))
    assert response.status_code == 204

    response = client.get(url_for('api.reservation_view', product_id=product.id))
    assert len(response.json) == 1

    with app.test_client() as c:  # using different client to simulate different user sessions
        response = c.put(url_for('api.reservation_view', product_id=product.id))
        assert response.status_code == 201

        response = c.get(url_for('api.reservation_view', product_id=product.id))
        assert len(response.json) == 1


def test_multiple_clients(app, product, client):
    def proc(idx, c):
        sleep_time = random.randint(1, 5)
        print(f'Thread {idx} sleeps for {sleep_time} seconds')
        sleep(sleep_time)

        with app.app_context():
            response = c.put(url_for('api.reservation_view', product_id=product.id))

        assert response.status_code == 201
        print(f'Process {idx} finished')

    for i in range(1, 100):
        p = thr.Thread(target=proc, args=(i, client))
        p.start()
