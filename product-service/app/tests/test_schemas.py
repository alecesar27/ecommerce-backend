import pytest
from strawberry import Schema
from app.schemas import Query, Mutation

schema = Schema(query=Query, mutation=Mutation)

@pytest.mark.asyncio
async def test_create_product_mutation():
    query = """
    mutation {
      createProduct(name: "Laptop", price: 999.99) {
        id
        name
        price
      }
    }
    """
    result = await schema.execute(query)
    assert result.errors is None
    assert result.data["createProduct"]["name"] == "Laptop"

@pytest.mark.asyncio
async def test_products_query():
    query = """
    query {
      products {
        name
        price
      }
    }
    """
    result = await schema.execute(query)
    assert result.errors is None
    assert len(result.data["products"]) == 1