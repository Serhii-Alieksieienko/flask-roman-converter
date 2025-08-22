import pytest
from main import app as flask_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_home_page_get(client):
    """Test that a GET request to the home page is successful."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome!" in response.data

def test_home_page_post_not_allowed(client):
    """Test that a POST request to the home page is not allowed."""
    response = client.post("/")
    assert response.status_code == 405