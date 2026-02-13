import json

from api.predict import CreditScoringModel


def test_model_loads_successfully():
    model = CreditScoringModel()
    assert model.model is not None
    assert len(model.feature_names) == 419


def test_prediction_deterministic():
    model = CreditScoringModel()
    with open("tests/fixtures/sample_client.json") as f:
        data = json.load(f)
    result1 = model.predict(data["features"])
    result2 = model.predict(data["features"])
    assert result1["probability"] == result2["probability"]


def test_threshold_boundary():
    model = CreditScoringModel()
    result = model.predict({})
    assert result["prediction"] == (1 if result["probability"] >= model.threshold else 0)


def test_feature_alignment_extra_features():
    model = CreditScoringModel()
    features = {"FAKE_FEATURE_1": 999.0, "FAKE_FEATURE_2": -999.0}
    result = model.predict(features)
    assert 0.0 <= result["probability"] <= 1.0
