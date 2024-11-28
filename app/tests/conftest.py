from app.db.main import get_async_session
from app.handlers.auth.dependencies import AccessTokenBearer, RoleChecker,RefreshTokenBearer
from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import Mock
import pytest
from httpx import AsyncClient

mock_session = Mock()
mock_repo = Mock()
mock_user_service = Mock()
mock_book_service =Mock()

def get_mock_session():
    yield mock_session

access_token_bearer = AccessTokenBearer()
refresh_token_bearer = RefreshTokenBearer()
role_checker = RoleChecker(['admin'])

app.dependency_overrides[get_async_session] = get_mock_session
app.dependency_overrides[role_checker] = Mock()
app.dependency_overrides[refresh_token_bearer]= Mock()
app.dependency_overrides[access_token_bearer]= Mock()

@pytest.fixture
def fake_session():
    return mock_session


@pytest.fixture
def fake_user_service():
    return mock_user_service

@pytest.fixture
def fake_repo():
    return mock_repo


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
async def async_test_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
