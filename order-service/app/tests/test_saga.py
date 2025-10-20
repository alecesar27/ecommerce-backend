import pytest
from unittest.mock import AsyncMock
from app.saga import place_order_saga

@pytest.mark.asyncio
async def test_place_order_saga(mock_db_session, mock_kafka_producer):
    order_data = {"id": 1}
    await place_order_saga(order_data, mock_db_session)
    # Assert event publishing (mocked)
    mock_kafka_producer.assert_called()