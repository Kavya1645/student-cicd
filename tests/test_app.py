import os
import tempfile

os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")

import app as student_app  # noqa: E402


def client():
    return student_app.app.test_client()


def test_health():
    assert client().get("/health").get_json() == {"status": "ok"}


def test_create_update_delete():
    c = client()
    c.post("/add", data={"name": "Asha", "email": "asha@x.com", "course": "CSE"})
    assert b"Asha" in c.get("/").data

    c.post("/edit/1", data={"name": "Asha Patel", "email": "asha@x.com", "course": "IT"})
    page = c.get("/").data
    assert b"Asha Patel" in page and b"IT" in page

    c.post("/delete/1")
    assert b"Asha Patel" not in c.get("/").data
