"""Tests for the FastAPI REST API layer."""
import os, tempfile, shutil, atexit

# Isolated temp DB for API tests
_tmp = os.environ.get("YONOCYTECH_DB_PATH")
if not _tmp:
    _tmp_dir = tempfile.mkdtemp()
    os.environ["YONOCYTECH_DB_PATH"] = os.path.join(_tmp_dir, "test.db")
    atexit.register(lambda: shutil.rmtree(_tmp_dir, ignore_errors=True))

import pytest
from fastapi.testclient import TestClient
from api.server import app

client = TestClient(app)


class TestAuthAPI:
    def test_health(self):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"

    def test_register_login(self):
        email = "apitest@example.com"
        resp = client.post("/auth/register", json={
            "name": "API Tester", "email": email, "password": "test1234"
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "token" in data
        assert data["user"]["email"] == email

        resp = client.post("/auth/login", json={
            "email": email, "password": "test1234"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data

    def test_login_invalid(self):
        resp = client.post("/auth/login", json={
            "email": "nobody@example.com", "password": "wrong"
        })
        assert resp.status_code == 401

    def test_me_unauthorized(self):
        resp = client.get("/auth/me")
        assert resp.status_code == 401

    def test_me_authorized(self):
        resp = client.post("/auth/register", json={
            "name": "Me Test", "email": "metest@example.com", "password": "pass1234"
        })
        token = resp.json()["token"]
        resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["email"] == "metest@example.com"


class TestProvidersAPI:
    def test_list_providers(self):
        resp = client.get("/providers/")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        if data:
            assert "id" in data[0]
            assert "name" in data[0]

    def test_list_active_only(self):
        resp = client.get("/providers/?active_only=true")
        assert resp.status_code == 200


class TestAgentsAPI:
    def test_list_agents(self):
        resp = client.get("/agents/")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)


class TestContactAPI:
    def test_submit_contact(self):
        resp = client.post("/contact/", json={
            "name": "Test", "email": "test@example.com",
            "subject": "Test", "message": "Hello from API test"
        })
        assert resp.status_code == 201
        assert resp.json()["detail"] == "Message sent successfully"


class TestSessionsAPI:
    def test_create_session(self):
        resp = client.post("/sessions/", json={
            "user_id": 1, "title": "API Test Session"
        })
        assert resp.status_code == 201
        data = resp.json()
        assert "id" in data
        assert data["title"] == "API Test Session"
