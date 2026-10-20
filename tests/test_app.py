import pytest
from app import app, tasks


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as client:
        yield client


def setup_function():
    tasks.clear()
    tasks.extend([
        {"id": 1, "title": "Sample task", "done": False},
        {"id": 2, "title": "Finished task", "done": True},
    ])


def test_home_page_shows_tasks(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sample task" in response.data


def test_add_task(client):
    response = client.post("/add", data={"title": "Read CI/CD guide"})
    assert response.status_code == 302
    assert any(task["title"] == "Read CI/CD guide" for task in tasks)


def test_toggle_task(client):
    client.post("/toggle/1")
    assert tasks[0]["done"] is True


def test_delete_task(client):
    client.post("/delete/1")
    assert not any(task["id"] == 1 for task in tasks)


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}
