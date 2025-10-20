import pytest
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def mock_kafka_producer():
    return AsyncMock()

@pytest.fixture
def mock_redis():
    return MagicMock()