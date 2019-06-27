import uuid
import pytest
from wash import create_app
from wash.service import create_product


@pytest.fixture
def app():
    return create_app({'SERVER_NAME': 'localhost'})


@pytest.fixture
def product():
    return create_product(name='name', description='description', retail_price=100)
