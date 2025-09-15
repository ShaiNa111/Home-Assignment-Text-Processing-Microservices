from fastapi.testclient import TestClient
from serving_service.main import app

client = TestClient(app)


def test_summarize_endpoint(monkeypatch):
    # Dummy gRPC response object
    class DummyResponse:
        tokens = ["Hello"]
        sentences = ["Hello world."]
        sentiment = "Neutral"

    # Fake gRPC call
    def fake_process_text(req):
        return DummyResponse()

    from serving_service import main
    monkeypatch.setattr(main.stub, "ProcessText", fake_process_text)

    response = client.post("/summarize", json={"text": "Hello world."})
    data = response.json()

    assert response.status_code == 200
    assert data["tokens"] == ["Hello"]
    assert data["sentiment"] == "Neutral"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
