import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_create_camera(async_client):
    response = await async_client.post("/api/v1/cameras/", json={
        "name": "API Test Camera",
        "rtsp_url": "rtsp://test",
        "location": "Test Location",
        "is_active": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API Test Camera"
    assert "id" in data

@pytest.mark.asyncio
async def test_read_cameras(async_client):
    response = await async_client.get("/api/v1/cameras/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_person(async_client):
    response = await async_client.post("/api/v1/persons/", json={
        "name": "API Test Person",
        "type": "vip",
        "notes": "Test notes"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "API Test Person"
    assert data["type"] == "vip" 
