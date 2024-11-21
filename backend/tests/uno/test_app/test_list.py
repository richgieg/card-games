from fastapi.testclient import TestClient


def test_list(client: TestClient) -> None:
    client.post("/create")
    client.post("/create")
    client.post("/create")
    response = client.get("/list")
    assert len(response.json()["games"]) == 3
