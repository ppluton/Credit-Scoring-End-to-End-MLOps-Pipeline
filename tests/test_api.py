def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True
    assert data["n_features"] == 419
    assert data["threshold"] > 0


def test_predict_returns_valid_response(client, sample_payload):
    response = client.post("/predict", json=sample_payload)
    assert response.status_code == 200
    data = response.json()
    assert "probability" in data
    assert "prediction" in data
    assert "decision" in data
    assert "inference_time_ms" in data


def test_predict_probability_in_range(client, sample_payload):
    response = client.post("/predict", json=sample_payload)
    data = response.json()
    assert 0.0 <= data["probability"] <= 1.0


def test_predict_decision_consistency(client, sample_payload):
    response = client.post("/predict", json=sample_payload)
    data = response.json()
    if data["probability"] >= data["threshold"]:
        assert data["prediction"] == 1
        assert data["decision"] == "REFUSED"
    else:
        assert data["prediction"] == 0
        assert data["decision"] == "APPROVED"


def test_predict_with_empty_features(client):
    payload = {"SK_ID_CURR": 0, "features": {}}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert 0.0 <= data["probability"] <= 1.0


def test_predict_with_partial_features(client):
    payload = {
        "SK_ID_CURR": 99999,
        "features": {"AMT_CREDIT": 0.5, "AMT_ANNUITY": -0.3},
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200


def test_model_info_endpoint(client):
    response = client.get("/model-info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_type"] == "LGBMClassifier"
    assert data["n_features"] == 419
    assert "metadata" in data
