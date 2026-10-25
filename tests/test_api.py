from fastapi.testclient import (
    TestClient,
)

from app.api import app


client = TestClient(
    app
)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok"
    }


def test_scene_endpoint():

    response = client.get(
        "/scene"
    )

    assert response.status_code == 200

    data = response.json()

    assert data[
        "object_count"
    ] == 5

    assert len(
        data["objects"]
    ) == 5


def test_scene_points_endpoint():

    response = client.get(
        "/scene/points"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(
        data["objects"]
    ) == 5

    for obj in data["objects"]:

        assert len(
            obj["points"]
        ) > 0