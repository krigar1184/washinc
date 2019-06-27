import uuid
from flask import g, current_app
from abc import ABCMeta


class Model(metaclass=ABCMeta):
    table_name = None

    def __init__(self):
        self.id = str(uuid.uuid4())

    def __str__(self):
        return f'Product#{self.id} ({self.name})'

    def as_dict(self):
        return self.__dict__

    @classmethod
    def get(cls, **kwargs):
        return cls.all()[kwargs['id']]

    @classmethod
    def get_many(cls, **kwargs):
        result = []

        for _, r in cls.all().items():
            is_match = True

            for k, v in r.as_dict().items():
                if k not in kwargs:
                    continue

                if v != kwargs.get(k):
                    is_match = False

            if is_match:
                result.append(r)

        return result

    @classmethod
    def all(cls):
        return current_app.cache.get(cls.table_name)


class Product(Model):
    table_name = 'products'

    def __init__(self, name, description=None, retail_price=0):
        super().__init__()

        self.name = name
        self.description = description
        self.retail_price = retail_price


class Reservation(Model):
    table_name = 'reservations'

    def __init__(self, customer_id, product_id):
        super().__init__()

        self.customer_id = customer_id
        self.product_id = product_id
