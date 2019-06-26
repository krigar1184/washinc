from multiprocessing import Lock, RLock
from flask import current_app, g
from wash.models import Product


RETAIL_PRICE_CACHE_KEY = 'retail_price'
RESERVATIONS_COUNT_CACHE_KEY = 'reservations_count'


LOCKS = {
    RETAIL_PRICE_CACHE_KEY: Lock(),
    RESERVATIONS_COUNT_CACHE_KEY: Lock(),
}


def get_retail_price():
    lock = LOCKS[RETAIL_PRICE_CACHE_KEY]
    lock.acquire()

    try:
        cache = current_app.cache
        value = 0

        if cache.has(RETAIL_PRICE_CACHE_KEY):
            value = cache.get(RETAIL_PRICE_CACHE_KEY)
    finally:
        lock.release()

    return value


def set_retail_price(value):
    lock = LOCKS[RETAIL_PRICE_CACHE_KEY]
    lock.acquire()

    try:
        if int(value) <= 0:
            raise Exception  # TODO raise more specific exception here

        current_app.cache.set(RETAIL_PRICE_CACHE_KEY, value)
    finally:
        lock.release()


def create_reservation():
    lock = LOCKS[RESERVATIONS_COUNT_CACHE_KEY]
    lock.acquire()

    try:
        cache = current_app.cache

        if cache.has(RESERVATIONS_COUNT_CACHE_KEY):
            cache.set(RESERVATIONS_COUNT_CACHE_KEY, int(cache.get(RESERVATIONS_COUNT_CACHE_KEY)) + 1)
        else:
            cache.set(RESERVATIONS_COUNT_CACHE_KEY, 1)
    finally:
        lock.release()


def cancel_reservation():
    lock = LOCKS[RESERVATIONS_COUNT_CACHE_KEY]
    lock.acquire()

    try:
        cache = current_app.cache
        current_value = int(cache.get(RESERVATIONS_COUNT_CACHE_KEY))

        if current_value in (0, None):
            raise Exception("This could never happen")

        cache.set(RESERVATIONS_COUNT_CACHE_KEY, current_value - 1)
    finally:
        lock.release()


def get_reservations():
    with LOCKS[RESERVATIONS_COUNT_CACHE_KEY]:
        return current_app.cache.get(RESERVATIONS_COUNT_CACHE_KEY)


def create_product(**data):
    product = Product(**data)
    current_app.locks[product.id] = RLock()
    products = current_app.cache.get('products')
    products[product.id] = product

    with current_app.locks[product.id]:
        current_app.cache.set('products', products)
    return product


def update_product(product_id, **data):
    if product_id not in current_app.locks:
        current_app.locks[product_id] = RLock()

    with current_app.locks[product_id]:
        product = Product.get(id=product_id)

        for k, v in data.items():
            if k in product.as_dict():
                product.__dict__[k] = v

        products = current_app.cache.get('products')
        products[product_id] = product
        current_app.cache.set('products', products)

    return product


def delete_product(product_id):
    if product_id not in current_app.locks:
        current_app.locks[product_id] = RLock()

    with current_app.locks[product_id]:
        products = Product.all()
        del products[product_id]
        current_app.cache.set('products', products)
