import uuid
import pytest
from wash import create_app
from wash.service import create_product
from wash.models import Customer


@pytest.fixture
def app():
    return create_app({'SERVER_NAME': 'localhost'})


@pytest.fixture
def product():
    return create_product(name='name', description='description')


@pytest.fixture
def customer():
    return Customer()
