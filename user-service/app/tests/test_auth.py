from app.auth import get_password_hash, verify_password, create_access_token

def test_password_hashing():
    hashed = get_password_hash("password")
    assert verify_password("password", hashed)
    assert not verify_password("wrong", hashed)

def test_create_access_token():
    token = create_access_token({"sub": "user"})
    assert isinstance(token, str)
    assert len(token) > 0