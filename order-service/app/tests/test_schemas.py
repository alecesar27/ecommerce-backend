import pytest
from strawberry import Schema
from app.schemas import Query, Mutation

schema = Schema(query=Query, mutation=Mutation)

@pytest.mark.asyncio
async def test_create_order_mutation():
    query = """
    mutation {
      createOrder(userId: 1, productId: 1) {
        id
        status
      }
    }
    """
    result = await schema.execute(query)
    assert result.errors is None
    assert result.data["createOrder"]["status"] == "pending"

@pytest.mark.asyncio
async def test_orders_query():
    query = """
    query {
      orders(userId: 1) {
        status
      }
    }
    """
    result = await schema.execute(query)
    assert result.errors is None
    assert len(result.data["orders"]) == 1