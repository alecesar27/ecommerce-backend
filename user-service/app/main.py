from fastapi import FastAPI
from ariadne import gql, QueryType, MutationType, make_executable_schema
from ariadne.asgi import GraphQL
import uuid

app = FastAPI(title="User Service")

# Simulação de banco em memória
users = {}

type_defs = gql("""
    type User {
        id: ID!
        username: String!
    }

    type Query {
        users: [User!]!
    }

    type Mutation {
        register(username: String!, password: String!): User!
    }
""")

query = QueryType()
mutation = MutationType()

@query.field("users")
def resolve_users(*_):
    return list(users.values())

@mutation.field("register")
def resolve_register(*_, username, password):
    user_id = str(uuid.uuid4())
    user = {"id": user_id, "username": username}
    users[user_id] = user
    return user

schema = make_executable_schema(type_defs, [query, mutation])
app.mount("/graphql", GraphQL(schema, debug=True))

@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}
