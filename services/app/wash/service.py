import os
from multiprocessing import Lock, RLock
from flask import current_app
from wash.models import Product, Reservation


def create_reservation(product_id, customer_id):
    locks = current_app.locks['products']

    if product_id not in locks:
        locks[product_id] = RLock()

    with locks[product_id]:
        cache = current_app.cache
        reservation = Reservation(product_id=product_id, customer_id=customer_id)
        reservations = Reservation.all()
        reservations[reservation.id] = reservation
        current_app.cache.set('reservations', reservations)

    return reservation


def cancel_reservation(product_id, customer_id):
    reservation = Reservation.get_many(product_id=product_id, customer_id=customer_id)[0]
    reservations = Reservation.all()
    del reservations[reservation.id]
    current_app.cache.set('reservations', reservations)


def get_reservations(product_id, customer_id):
    return Reservation.get_many(customer_id=customer_id)


def create_product(**data):
    product = Product(**data)
    current_app.locks['products'][product.id] = RLock()
    products = current_app.cache.get('products')
    products[product.id] = product

    with current_app.locks['products'][product.id]:
        current_app.cache.set('products', products)
    return product


def update_product(product_id, **data):
    if product_id not in current_app.locks['products']:
        current_app.locks['products'][product_id] = RLock()

    with current_app.locks['products'][product_id]:
        product = Product.get(id=product_id)

        for k, v in data.items():
            if k in product.as_dict():
                product.__dict__[k] = v

        products = current_app.cache.get('products')
        products[product_id] = product
        current_app.cache.set('products', products)

    return product


def delete_product(product_id):
    if product_id not in current_app.locks['products']:
        current_app.locks['products'][product_id] = RLock()

    with current_app.locks['products'][product_id]:
        products = Product.all()
        del products[product_id]
        current_app.cache.set('products', products)
