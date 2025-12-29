import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User as UserModel


@pytest.fixture
async def auth_token(async_client: AsyncClient, db_session: AsyncSession) -> str:
    """Create a test user and return authentication token"""
    # Create test user
    user = UserModel(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass123"),
        role="admin",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login to get token
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "testpass123"}
    )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_camera(async_client: AsyncClient, auth_token: str):
    response = await async_client.post(
        "/api/v1/cameras/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "name": "API Test Camera",
            "rtsp_url": "rtsp://test",
            "location": "Test Location",
            "is_active": True
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API Test Camera"
    assert "id" in data


@pytest.mark.asyncio
async def test_read_cameras(async_client: AsyncClient, auth_token: str):
    response = await async_client.get(
        "/api/v1/cameras/",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_person(async_client: AsyncClient, auth_token: str):
    response = await async_client.post(
        "/api/v1/persons/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "name": "API Test Person",
            "type": "vip",
            "notes": "Test notes"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API Test Person"
    assert data["type"] == "vip" 
