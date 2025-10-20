import strawberry
from strawberry import federation

@strawberry.federation.type(keys=["id"])
class Order:
    id: int
    user_id: int
    product_id: int
    status: str

@strawberry.type
class Query:
    @strawberry.field
    def orders(self, user_id: int) -> list[Order]:
        # CQRS read
        return [Order(id=1, user_id=user_id, product_id=1, status="pending")]

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_order(self, user_id: int, product_id: int, quantity: int) -> Order:
        # Trigger Saga
        order = Order(id=1, user_id=user_id, product_id=product_id, status="pending")
        await saga.place_order_saga({"id": order.id}, db)
        return order