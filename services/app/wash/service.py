from multiprocessing import RLock
from flask import current_app


RETAIL_PRICE_CACHE_KEY = 'retail_price'
RESERVATIONS_COUNT_CACHE_KEY = 'reservations_count'


LOCK = RLock()


def get_retail_price():
    LOCK.acquire()

    try:
        cache = current_app.cache
        value = 0

        if cache.has(RETAIL_PRICE_CACHE_KEY):
            value = cache.get(RETAIL_PRICE_CACHE_KEY)
    finally:
        LOCK.release()

    return value


def set_retail_price(value):
    LOCK.acquire()

    try:
        if int(value) <= 0:
            raise Exception  # TODO raise more specific exception here

        current_app.cache.set(RETAIL_PRICE_CACHE_KEY, value)
    finally:
        LOCK.release()


def create_reservation():
    LOCK.acquire()

    try:
        cache = current_app.cache

        if cache.has(RESERVATIONS_COUNT_CACHE_KEY):
            
            cache.set(RESERVATIONS_COUNT_CACHE_KEY, int(cache.get(RESERVATIONS_COUNT_CACHE_KEY)) + 1)
        else:
            cache.set(RESERVATIONS_COUNT_CACHE_KEY, 1)
    finally:
        LOCK.release()


def cancel_reservation():
    LOCK.acquire()

    try:
        cache = current_app.cache
        current_value = int(cache.get(RESERVATIONS_COUNT_CACHE_KEY))

        if current_value in (0, None):
            raise Exception("This could never happen")

        cache.set(RESERVATIONS_COUNT_CACHE_KEY, current_value - 1)
    finally:
        LOCK.release()


def get_reservations():
    return current_app.cache.get(RESERVATIONS_COUNT_CACHE_KEY)
