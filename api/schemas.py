from pydantic import BaseModel


class PredictionRequest(BaseModel):
    SK_ID_CURR: int
    features: dict[str, float]


class PredictionResponse(BaseModel):
    SK_ID_CURR: int
    probability: float
    prediction: int
    threshold: float
    decision: str
    inference_time_ms: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    n_features: int
    threshold: float
