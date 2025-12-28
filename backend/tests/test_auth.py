import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User as UserModel


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    """Test user registration"""
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
            "role": "viewer"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # Should not expose password


@pytest.mark.asyncio
async def test_register_duplicate_username(async_client: AsyncClient, db_session: AsyncSession):
    """Test registration with duplicate username"""
    # Create existing user
    user = UserModel(
        username="existing",
        email="existing@example.com",
        hashed_password=get_password_hash("password"),
        role="viewer"
    )
    db_session.add(user)
    await db_session.commit()
    
    # Try to register with same username
    response = await async_client.post(
        "/api/v1/auth/register",
        json={
            "username": "existing",
            "email": "different@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, db_session: AsyncSession):
    """Test successful login"""
    # Create user
    user = UserModel(
        username="logintest",
        email="login@example.com",
        hashed_password=get_password_hash("testpass123"),
        role="admin",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "logintest", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(async_client: AsyncClient, db_session: AsyncSession):
    """Test login with wrong password"""
    user = UserModel(
        username="wrongpass",
        email="wrong@example.com",
        hashed_password=get_password_hash("correctpass"),
        role="viewer"
    )
    db_session.add(user)
    await db_session.commit()
    
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "wrongpass", "password": "wrongpassword"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user(async_client: AsyncClient, db_session: AsyncSession):
    """Test getting current user info"""
    # Create user and login
    user = UserModel(
        username="metest",
        email="me@example.com",
        full_name="Me Test",
        hashed_password=get_password_hash("mypass"),
        role="operator",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login to get token
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "metest", "password": "mypass"}
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = await async_client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "metest"
    assert data["email"] == "me@example.com"
    assert data["role"] == "operator"


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(async_client: AsyncClient):
    """Test accessing protected endpoint without authentication"""
    response = await async_client.get("/api/v1/cameras/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_with_token(async_client: AsyncClient, db_session: AsyncSession):
    """Test accessing protected endpoint with valid token"""
    # Create user
    user = UserModel(
        username="tokenuser",
        email="token@example.com",
        hashed_password=get_password_hash("password"),
        role="viewer",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "tokenuser", "password": "password"}
    )
    token = login_response.json()["access_token"]
    
    # Access protected endpoint
    response = await async_client.get(
        "/api/v1/cameras/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_role_based_access_viewer_cannot_create(async_client: AsyncClient, db_session: AsyncSession):
    """Test that viewer role cannot create cameras"""
    # Create viewer user
    user = UserModel(
        username="viewer",
        email="viewer@example.com",
        hashed_password=get_password_hash("pass"),
        role="viewer",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "viewer", "password": "pass"}
    )
    token = login_response.json()["access_token"]
    
    # Try to create camera
    response = await async_client.post(
        "/api/v1/cameras/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Test Camera",
            "rtsp_url": "rtsp://test",
            "location": "Test Location"
        }
    )
    assert response.status_code == 403  # Forbidden


@pytest.mark.asyncio
async def test_role_based_access_admin_can_delete(async_client: AsyncClient, db_session: AsyncSession):
    """Test that admin role can delete cameras"""
    # Create admin user
    user = UserModel(
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("adminpass"),
        role="admin",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "adminpass"}
    )
    token = login_response.json()["access_token"]
    
    # Create camera first
    from app.models.camera import Camera
    camera = Camera(name="Delete Me", rtsp_url="rtsp://test", location="Test")
    db_session.add(camera)
    await db_session.commit()
    await db_session.refresh(camera)
    
    # Delete camera
    response = await async_client.delete(
        f"/api/v1/cameras/{camera.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
