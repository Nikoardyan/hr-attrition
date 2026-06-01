# HR Attrition Predictor

Deep Learning system to predict employee attrition risk for proactive HR intervention.

## 🎯 Business Problem

Employee turnover costs companies 50-200% of an employee's annual salary in recruitment, training, and lost productivity. HR teams currently react *after* a resignation letter is submitted. This system provides **early warning** so HR can intervene proactively (salary review, role change, retention conversation).

## 📊 Dataset

[IBM HR Analytics Employee Attrition & Performance](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
- 1,470 rows × 35 columns
- Binary target: `Attrition` (Yes/No)
- Class imbalance: ~16% positive class

## 🏗️ Architecture

```
Streamlit UI ──▶ FastAPI ──▶ DNN Model (Keras)
                   │
                   ▼
               SQLite (prediction logs)
```

## 🚀 Quick Start

```bash
# 1. Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Download dataset
# Put WA_Fn-UseC_-HR-Employee-Attrition.csv in data/raw/

# 3. Train model
python src/train.py

# 4. Run API
uvicorn api.main:app --reload --port 8000

# 5. Run Streamlit UI (new terminal)
streamlit run streamlit_app/app.py
```

## 📁 Structure

```
.
├── api/                    # FastAPI service
├── data/                   # Raw and processed data
├── models/                 # Saved model weights & preprocessors
├── notebooks/              # EDA notebook
├── src/                    # Training pipeline
├── streamlit_app/          # Web UI
├── tests/                  # Pytest tests
└── .github/workflows/      # CI/CD
```

## 🧪 Model Performance

| Metric    | Score |
|-----------|-------|
| Accuracy  | TBD   |
| F1-Score  | TBD   |
| ROC-AUC   | TBD   |
| Precision | TBD   |
| Recall    | TBD   |

## 🛠️ Tech Stack

- **ML**: TensorFlow/Keras, scikit-learn, imbalanced-learn (SMOTE), Keras Tuner
- **API**: FastAPI, Uvicorn, SQLAlchemy, SQLite
- **UI**: Streamlit, Plotly
- **DevOps**: Docker, GitHub Actions, pytest, flake8
# hr-attrition
