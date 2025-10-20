from fastapi import FastAPI
from sqlalchemy.orm import Session
from ariadne import make_executable_schema, QueryType, MutationType, gql
from ariadne.asgi import GraphQL
from . import models, events
from .database import engine, get_db

# -----------------------------------------------
# 📘 GraphQL SDL
# -----------------------------------------------
type_defs = gql("""
    type Product {
        id: ID!
        name: String!
        price: Float!
    }

    type Query {
        products: [Product]
    }

    input ProductInput {
        name: String!
        price: Float!
    }

    type Mutation {
        createProduct(product: ProductInput!): Product
    }
""")

# -----------------------------------------------
# 🔍 Query Resolvers
# -----------------------------------------------
query = QueryType()

@query.field("products")
def resolve_products(_, info):
    db = next(get_db())
    try:
        products = db.query(models.Product).all()
        return [{"id": p.id, "name": p.name, "price": p.price} for p in products]
    finally:
        db.close()

# -----------------------------------------------
# ✏️ Mutation Resolvers
# -----------------------------------------------
mutation = MutationType()

@mutation.field("createProduct")
async def resolve_create_product(_, info, product):
    db = next(get_db())
    try:
        new_product = models.Product(name=product["name"], price=product["price"])
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        await events.publish_event("product-events", {
            "event": "ProductCreated",
            "product_id": new_product.id
        })
        return {
            "id": new_product.id,
            "name": new_product.name,
            "price": new_product.price
        }
    finally:
        db.close()

# -----------------------------------------------
# 🧩 Schema GraphQL
# -----------------------------------------------
schema = make_executable_schema(type_defs, [query, mutation])

# -----------------------------------------------
# 🚀 FastAPI App
# -----------------------------------------------
app = FastAPI()
app.add_route("/graphql", GraphQL(schema, debug=True))

# -----------------------------------------------
# 🏗️ Criação automática das tabelas
# -----------------------------------------------
@app.on_event("startup")
def startup_event():
    models.Base.metadata.create_all(bind=engine)
