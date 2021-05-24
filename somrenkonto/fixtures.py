import pytest

from .factories import *


@pytest.fixture
def technical_visit_event():
    return TechnicalVisitEventFactory.create()
