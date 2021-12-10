from fastapi.testclient import TestClient

from main import app, get_settings
from internal.config import Settings

client = TestClient(app)


def get_settings_override():
    return Settings(admin_email="wera.watcharapon@gmail.com")


app.dependency_overrides[get_settings] = get_settings_override


def test_app():
    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "AI.CRM",
        "admin_email": "wera.watcharapon@gmail.com",
        "items_per_user": 50,
    }
