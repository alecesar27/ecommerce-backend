from fastapi import FastAPI
from ariadne import gql, QueryType, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
from sqlalchemy.orm import Session
from . import models, events, database
from .database import Base, engine

# --- Criar tabelas no banco automaticamente ---
Base.metadata.create_all(bind=engine)

# --- Definir o schema GraphQL ---
type_defs = gql("""
    type Order {
        id: ID!
        user_id: Int!
        product_id: Int!
        quantity: Int!
        total_price: Float!
    }

    type Query {
        orders: [Order!]!
        order(id: ID!): Order
    }

    input CreateOrderInput {
        user_id: Int!
        product_id: Int!
        quantity: Int!
    }

    type Mutation {
        createOrder(input: CreateOrderInput!): Order!
    }
""")

# --- Query Resolvers ---
query = QueryType()

@query.field("orders")
def resolve_orders(_, info):
    db: Session = next(database.get_db())
    try:
        return db.query(models.Order).all()
    finally:
        db.close()

@query.field("order")
def resolve_order(_, info, id):
    db: Session = next(database.get_db())
    try:
        return db.query(models.Order).filter(models.Order.id == id).first()
    finally:
        db.close()

# --- Mutation Resolvers ---
mutation = MutationType()

@mutation.field("createOrder")
async def resolve_create_order(_, info, input):
    db: Session = next(database.get_db())
    try:
        # Simulação simples de preço por produto
        product_price = 100.0  
        total_price = product_price * input["quantity"]

        new_order = models.Order(
            user_id=input["user_id"],
            product_id=input["product_id"],
            quantity=input["quantity"],
            total_price=total_price,
        )
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Publicar evento Kafka
        await events.publish_event("order-events", {
            "event": "OrderCreated",
            "order_id": new_order.id,
            "user_id": new_order.user_id,
            "product_id": new_order.product_id,
            "quantity": new_order.quantity,
            "total_price": new_order.total_price
        })

        return new_order
    finally:
        db.close()

# --- Criar schema executável ---
schema = make_executable_schema(type_defs, [query, mutation])

# --- Criar app FastAPI com rota GraphQL ---
app = FastAPI(title="Order Service")
app.add_route("/graphql", GraphQL(schema, debug=True))
