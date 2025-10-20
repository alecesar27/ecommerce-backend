import pytest
from strawberry import Schema
from app.schemas import Subscription

schema = Schema(subscription=Subscription)

@pytest.mark.asyncio
async def test_notifications_subscription():
    query = """
    subscription {
      notifications {
        message
      }
    }
    """
    # Note: Full subscription testing requires WebSocket; this is a basic check
    result = await schema.subscribe(query)
    messages = []
    async for msg in result:
        messages.append(msg.data)
        if len(messages) >= 1:  # Stop after one for test
            break
    assert len(messages) > 0
    assert "notification" in messages[0]["notifications"]["message"].lower()