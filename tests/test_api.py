"""Smoke tests for FastAPI service."""
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


SAMPLE_PAYLOAD = {
    "Age": 35,
    "BusinessTravel": "Travel_Rarely",
    "DailyRate": 800,
    "Department": "Research & Development",
    "DistanceFromHome": 5,
    "Education": 3,
    "EducationField": "Life Sciences",
    "EnvironmentSatisfaction": 3,
    "Gender": "Male",
    "HourlyRate": 65,
    "JobInvolvement": 3,
    "JobLevel": 2,
    "JobRole": "Research Scientist",
    "JobSatisfaction": 3,
    "MaritalStatus": "Married",
    "MonthlyIncome": 5000,
    "MonthlyRate": 14000,
    "NumCompaniesWorked": 2,
    "OverTime": "No",
    "PercentSalaryHike": 15,
    "PerformanceRating": 3,
    "RelationshipSatisfaction": 3,
    "StockOptionLevel": 1,
    "TotalWorkingYears": 10,
    "TrainingTimesLastYear": 2,
    "WorkLifeBalance": 3,
    "YearsAtCompany": 5,
    "YearsInCurrentRole": 3,
    "YearsSinceLastPromotion": 1,
    "YearsWithCurrManager": 3,
}


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["service"] == "HR Attrition Predictor"


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()


def test_predict_schema_invalid():
    """Invalid payload should return 422."""
    bad = {"Age": 200}  # missing fields & invalid range
    r = client.post("/predict", json=bad)
    assert r.status_code == 422


def test_predict_payload_validates():
    """Sample payload should pass schema validation.
    Will return 503 if no model loaded — that's OK for CI."""
    r = client.post("/predict", json=SAMPLE_PAYLOAD)
    assert r.status_code in (200, 503)
