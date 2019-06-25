import pytest
from wash import create_app


@pytest.fixture
def app():
    return create_app({'SERVER_NAME': 'localhost'})
