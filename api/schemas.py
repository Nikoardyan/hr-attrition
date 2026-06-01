"""Pydantic schemas for API requests/responses."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class EmployeeFeatures(BaseModel):
    """All input features required to make a prediction.

    Field constraints reflect the original IBM dataset value ranges.
    """

    Age: int = Field(..., ge=18, le=65)
    BusinessTravel: Literal["Travel_Rarely", "Travel_Frequently", "Non-Travel"]
    DailyRate: int = Field(..., ge=100, le=2000)
    Department: Literal["Sales", "Research & Development", "Human Resources"]
    DistanceFromHome: int = Field(..., ge=1, le=30)
    Education: int = Field(..., ge=1, le=5)
    EducationField: Literal[
        "Life Sciences",
        "Medical",
        "Marketing",
        "Technical Degree",
        "Human Resources",
        "Other",
    ]
    EnvironmentSatisfaction: int = Field(..., ge=1, le=4)
    Gender: Literal["Male", "Female"]
    HourlyRate: int = Field(..., ge=30, le=100)
    JobInvolvement: int = Field(..., ge=1, le=4)
    JobLevel: int = Field(..., ge=1, le=5)
    JobRole: Literal[
        "Sales Executive",
        "Research Scientist",
        "Laboratory Technician",
        "Manufacturing Director",
        "Healthcare Representative",
        "Manager",
        "Sales Representative",
        "Research Director",
        "Human Resources",
    ]
    JobSatisfaction: int = Field(..., ge=1, le=4)
    MaritalStatus: Literal["Single", "Married", "Divorced"]
    MonthlyIncome: int = Field(..., ge=1000, le=20000)
    MonthlyRate: int = Field(..., ge=2000, le=27000)
    NumCompaniesWorked: int = Field(..., ge=0, le=10)
    OverTime: Literal["Yes", "No"]
    PercentSalaryHike: int = Field(..., ge=10, le=25)
    PerformanceRating: int = Field(..., ge=1, le=4)
    RelationshipSatisfaction: int = Field(..., ge=1, le=4)
    StockOptionLevel: int = Field(..., ge=0, le=3)
    TotalWorkingYears: int = Field(..., ge=0, le=40)
    TrainingTimesLastYear: int = Field(..., ge=0, le=6)
    WorkLifeBalance: int = Field(..., ge=1, le=4)
    YearsAtCompany: int = Field(..., ge=0, le=40)
    YearsInCurrentRole: int = Field(..., ge=0, le=20)
    YearsSinceLastPromotion: int = Field(..., ge=0, le=15)
    YearsWithCurrManager: int = Field(..., ge=0, le=20)


class PredictionResponse(BaseModel):
    probability: float = Field(..., description="Probability of leaving (0-1)")
    prediction: Literal["Will Leave", "Will Stay"]
    risk_level: Literal["Low", "Medium", "High"]
    recommendation: str


class PredictionLog(BaseModel):
    id: int
    timestamp: datetime
    probability: float
    prediction: str
    risk_level: str

    model_config = {"from_attributes": True}
