from fastapi import FastAPI
from ariadne import gql, QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from .database import engine, Base

# --- Definir schema Ariadne ---
type_defs = gql("""
    type Notification {
        id: ID!
        user_id: Int!
        message: String!
    }

    type Query {
        notifications: [Notification!]!
    }
""")

# --- Query resolvers ---
query = QueryType()

@query.field("notifications")
def resolve_notifications(_, info):
    # Aqui você pode consultar o banco de dados ou retornar uma lista fixa para testes
    return [
        {"id": 1, "user_id": 1, "message": "Order #123 paid"},
        {"id": 2, "user_id": 2, "message": "Order #124 shipped"}
    ]

# --- Criar schema executável ---
schema = make_executable_schema(type_defs, query)

# --- Criar app FastAPI ---
app = FastAPI(title="Notification Service")
app.add_route("/graphql", GraphQL(schema, debug=True))

# --- Inicializar banco de dados ---
Base.metadata.create_all(bind=engine)

# --- Código comentado do Kafka para consumir eventos ---
# from aiokafka import AIOKafkaConsumer
# import asyncio
# import json
#
# async def consume_notifications():
#     consumer = AIOKafkaConsumer(
#         'order-events', 
#         'user-events', 
#         bootstrap_servers='kafka:9092'
#     )
#     await consumer.start()
#     try:
#         async for msg in consumer:
#             event = json.loads(msg.value.decode())
#             if event["event"] == "OrderPaid":
#                 print(f"Send email for order {event['order_id']}")
#             # Handle other events
#     finally:
#         await consumer.stop()
#
# asyncio.run(consume_notifications())
