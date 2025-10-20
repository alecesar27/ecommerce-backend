import strawberry
from strawberry import federation

@strawberry.federation.type(keys=["id"])
class User:
    id: int
    username: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User | None:
        # Resolver logic: query DB
        return User(id=id, username="example")

@strawberry.type
class Mutation:
    @strawberry.mutation
    def register(self, username: str, password: str) -> User:
        # Call auth logic, publish event
        return User(id=1, username=username)

    @strawberry.mutation
    def login(self, username: str, password: str) -> str:
        # Return JWT token
        return "jwt-token"