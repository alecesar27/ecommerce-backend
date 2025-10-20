import pytest
from strawberry import Schema
from app.schemas import Query, Mutation
from app.models import User
from app.database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.auth import get_password_hash

# --- Criar banco de dados de teste em memória ---
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# --- Fixture de sessão do banco ---
@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Schema Strawberry ---
schema = Schema(query=Query, mutation=Mutation)

# --- Testes ---
@pytest.mark.asyncio
async def test_register_mutation(db_session):
    # Criar usuário de teste com hashed_password truncado
    hashed = get_password_hash("pass")[:72]
    user = User(username="testuser", hashed_password=hashed)
    db_session.add(user)
    db_session.commit()

    query = """
    mutation {
      register(username: "testuser", password: "pass") {
        id
        username
      }
    }
    """
    result = await schema.execute(query, context_value={"db": db_session})
    assert result.errors is None
    assert result.data["register"]["username"] == "testuser"

@pytest.mark.asyncio
async def test_login_mutation(db_session):
    # Criar usuário de teste com hashed_password
    hashed = get_password_hash("pass")[:72]
    user = User(username="testuser", hashed_password=hashed)
    db_session.add(user)
    db_session.commit()

    query = """
    mutation {
      login(username: "testuser", password: "pass")
    }
    """
    result = await schema.execute(query, context_value={"db": db_session})
    assert result.errors is None
    # Ajuste conforme sua função real de login
    assert result.data["login"] == "jwt-token"

@pytest.mark.asyncio
async def test_user_query(db_session):
    # Criar usuário de teste com hashed_password
    hashed = get_password_hash("pass")[:72]
    user = User(username="testuser", hashed_password=hashed)
    db_session.add(user)
    db_session.commit()

    query = """
    query {
      user(id: 1) {
        username
      }
    }
    """
    result = await schema.execute(query, context_value={"db": db_session})
    assert result.errors is None
    assert result.data["user"]["username"] == "testuser"
