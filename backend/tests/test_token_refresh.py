import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, create_password_reset_token
from app.models.user import User as UserModel


@pytest.mark.asyncio
async def test_login_returns_refresh_token(async_client: AsyncClient, db_session: AsyncSession):
    """Test that login returns both access and refresh tokens"""
    # Create user
    user = UserModel(
        username="refreshtest",
        email="refresh@example.com",
        hashed_password=get_password_hash("testpass"),
        role="viewer",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "refreshtest", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_token_success(async_client: AsyncClient, db_session: AsyncSession):
    """Test successful token refresh"""
    # Create user
    user = UserModel(
        username="tokrefresh",
        email="tokrefresh@example.com",
        hashed_password=get_password_hash("password"),
        role="admin",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login to get refresh token
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "tokrefresh", "password": "password"}
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Use refresh token
    response = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_token_invalid(async_client: AsyncClient):
    """Test refresh with invalid token"""
    response = await async_client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalid.token.here"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_password_reset_request(async_client: AsyncClient, db_session: AsyncSession):
    """Test password reset request"""
    # Create user
    user = UserModel(
        username="resetuser",
        email="reset@example.com",
        hashed_password=get_password_hash("oldpassword"),
        role="viewer",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Request password reset
    response = await async_client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "reset@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "reset_token" in data  # In production this would be sent via email


@pytest.mark.asyncio
async def test_password_reset_confirm(async_client: AsyncClient, db_session: AsyncSession):
    """Test password reset confirmation"""
    # Create user
    user = UserModel(
        username="confirmreset",
        email="confirmreset@example.com",
        hashed_password=get_password_hash("oldpassword"),
        role="viewer",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Generate reset token
    reset_token = create_password_reset_token(user.email)
    
    # Reset password
    response = await async_client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "token": reset_token,
            "new_password": "newpassword123"
        }
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset successful"
    
    # Verify can login with new password
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "confirmreset", "password": "newpassword123"}
    )
    assert login_response.status_code == 200


@pytest.mark.asyncio
async def test_password_reset_invalid_token(async_client: AsyncClient):
    """Test password reset with invalid token"""
    response = await async_client.post(
        "/api/v1/auth/password-reset/confirm",
        json={
            "token": "invalid.token",
            "new_password": "newpassword"
        }
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_password_reset_nonexistent_email(async_client: AsyncClient):
    """Test password reset request for non-existent email"""
    response = await async_client.post(
        "/api/v1/auth/password-reset/request",
        json={"email": "nonexistent@example.com"}
    )
    # Should still return 200 to not reveal if email exists
    assert response.status_code == 200
