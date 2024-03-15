import pytest

from .fixtures import *


@pytest.fixture(scope="session")
def rf():
    from rest_framework.test import APIRequestFactory

    return APIRequestFactory()
