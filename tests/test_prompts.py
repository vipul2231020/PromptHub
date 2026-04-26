import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.db.session import get_db

# ──────────────────────────────────────────
# Test Database Setup (SQLite in-memory)
# ──────────────────────────────────────────

TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def auth_headers(client):
    """Create admin user and get auth token."""
    # Register admin
    client.post("/auth/register", json={
        "email": "admin@test.com",
        "password": "testpass123"
    })

    # Manually make admin (direct DB update)
    db = TestSessionLocal()
    from app.models.user import User
    user = db.query(User).filter(User.email == "admin@test.com").first()
    if user:
        user.is_admin = True
        db.commit()
    db.close()

    # Login
    response = client.post("/auth/login", json={
        "email": "admin@test.com",
        "password": "testpass123"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ──────────────────────────────────────────
# AUTH TESTS
# ──────────────────────────────────────────

class TestAuth:
    def test_register_success(self, client):
        response = client.post("/auth/register", json={
            "email": "newuser@test.com",
            "password": "password123"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "newuser@test.com"
        assert "id" in data

    def test_register_duplicate_email(self, client):
        client.post("/auth/register", json={
            "email": "duplicate@test.com",
            "password": "password123"
        })
        response = client.post("/auth/register", json={
            "email": "duplicate@test.com",
            "password": "password123"
        })
        assert response.status_code == 400

    def test_login_success(self, client):
        client.post("/auth/register", json={
            "email": "logintest@test.com",
            "password": "password123"
        })
        response = client.post("/auth/login", json={
            "email": "logintest@test.com",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client):
        response = client.post("/auth/login", json={
            "email": "logintest@test.com",
            "password": "wrongpassword"
        })
        assert response.status_code == 401


# ──────────────────────────────────────────
# PROMPT TESTS
# ──────────────────────────────────────────

class TestPrompts:
    def test_get_prompts_empty(self, client):
        response = client.get("/prompts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_prompt_as_admin(self, client, auth_headers):
        response = client.post("/prompts/", json={
            "title": "Test Prompt",
            "content": "This is a test prompt for unit testing purposes.",
            "category": "coding",
            "tags": ["test", "coding"]
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Prompt"
        assert data["category"] == "coding"
        return data["id"]

    def test_create_prompt_unauthorized(self, client):
        response = client.post("/prompts/", json={
            "title": "Test Prompt",
            "content": "Content here",
            "category": "coding",
        })
        assert response.status_code == 403

    def test_get_prompt_by_id(self, client, auth_headers):
        # Create a prompt first
        create_resp = client.post("/prompts/", json={
            "title": "Get By ID Test",
            "content": "Testing get by ID functionality",
            "category": "writing",
        }, headers=auth_headers)
        prompt_id = create_resp.json()["id"]

        response = client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        assert response.json()["id"] == prompt_id

    def test_get_prompt_not_found(self, client):
        response = client.get("/prompts/99999")
        assert response.status_code == 404

    def test_filter_by_category(self, client, auth_headers):
        response = client.get("/prompts/?category=coding")
        assert response.status_code == 200
        prompts = response.json()
        for prompt in prompts:
            assert prompt["category"] == "coding"


# ──────────────────────────────────────────
# ANALYTICS TESTS
# ──────────────────────────────────────────

class TestAnalytics:
    def test_get_trending(self, client):
        response = client.get("/analytics/trending")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_stats(self, client):
        response = client.get("/analytics/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_prompts" in data
        assert "total_usage" in data
        assert "average_rating" in data


# ──────────────────────────────────────────
# HEALTH CHECK TESTS
# ──────────────────────────────────────────

class TestHealth:
    def test_root_health_check(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_detailed_health(self, client):
        response = client.get("/health")
        assert response.status_code == 200
