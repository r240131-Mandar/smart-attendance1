import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from app import create_app  # noqa: E402


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()


def login(client, username, password):
    return client.post("/login", data={"username": username, "password": password},
                       follow_redirects=True)


def test_health(client):
    assert client.get("/health").json == {"status": "ok"}


def test_login_page_loads(client):
    assert client.get("/login").status_code == 200


def test_invalid_login(client):
    resp = login(client, "teacher1", "wrong")
    assert b"Invalid username or password" in resp.data


def test_teacher_login_goes_to_mark_page(client):
    resp = login(client, "teacher1", "teach123")
    assert b"Mark Attendance" in resp.data


def test_mark_and_student_view(client):
    login(client, "teacher1", "teach123")
    # Only student id 2 (Amit) is present
    client.post("/mark", data={"subject": "ASDD", "date": "2026-10-01", "present": ["2"]})
    client.get("/logout")
    resp = login(client, "amit", "pass123")
    assert b"ASDD" in resp.data
    assert b"100.0%" in resp.data


def test_low_attendance_report(client):
    login(client, "teacher1", "teach123")
    client.post("/mark", data={"subject": "ASDD", "date": "2026-10-01", "present": ["2"]})
    resp = client.get("/report")
    assert b"Neha Joshi" in resp.data      # absent -> 0% -> flagged
    assert b"Amit Patil" not in resp.data  # present -> 100% -> not flagged


def test_student_cannot_open_report(client):
    login(client, "amit", "pass123")
    resp = client.get("/report", follow_redirects=True)
    assert b"Low-Attendance Report" not in resp.data
