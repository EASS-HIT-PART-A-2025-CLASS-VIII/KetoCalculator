from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_calc_ok():
    payload = {
        "unit_system": "metric",
        "sex": "male",
        "age_years": 25,
        "height_cm": 180,
        "weight_kg": 80,
        "activity_level": "moderate",
        "goal": "maintain",
    }
    r = client.post("/calc", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "bmi" in data
    assert "macros" in data
    assert "forecast" in data
