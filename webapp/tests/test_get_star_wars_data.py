from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import requests

from webapp.src.app import app

client = TestClient(app)

# Tests for /data
def test_get_star_wars_data():
    response = client.get("/data")
    assert response.status_code == 200
    assert "name" in response.json()

def test_get_star_wars_data_with_id():
    response = client.get("/data?id=2")
    assert response.status_code == 200
    assert "name" in response.json()

def test_get_star_wars_data_invalid_id():
    response = client.get("/data?id=9999")
    assert response.status_code == 500

def test_get_star_wars_data_http_error():
    with patch("webapp.src.app.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError()
        response = client.get("/data?id=1")
        assert response.status_code == 500
        assert response.json()["detail"] == "API Error"

def test_get_star_wars_data_connection_error():
    with patch("webapp.src.app.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        response = client.get("/data?id=1")
        assert response.status_code == 503
        assert response.json()["detail"] == "Service Unavailable"

def test_get_star_wars_data_timeout():
    with patch("webapp.src.app.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout()
        response = client.get("/data?id=1")
        assert response.status_code == 503

# Tests for /
def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_hello_custom_message():
    with patch.dict("os.environ", {"HELLO_MESSAGE": "Hola Pricer!"}):
        from importlib import reload
        import webapp.src.app as app_module
        reload(app_module)
        custom_client = TestClient(app_module.app)
        response = custom_client.get("/")
        assert response.status_code == 200

# Tests for /top-people-by-bmi
def test_top_people_by_bmi():
    response = client.get("/top-people-by-bmi")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 20
    if len(data) > 1:
        assert data[0]["bmi"] >= data[1]["bmi"]

def test_top_people_by_bmi_has_name_and_bmi():
    response = client.get("/top-people-by-bmi")
    assert response.status_code == 200
    for person in response.json():
        assert "name" in person
        assert "bmi" in person

def test_top_people_by_bmi_connection_error():
    with patch("webapp.src.app.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError()
        response = client.get("/top-people-by-bmi")
        assert response.status_code == 503
        assert response.json()["detail"] == "Service Unavailable"

def test_top_people_by_bmi_http_error():
    with patch("webapp.src.app.requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError()
        response = client.get("/top-people-by-bmi")
        assert response.status_code == 500