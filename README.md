<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</div>

<br>

<h1 align="center">Sentinel · HR Attrition Intelligence 🧠</h1>

<p align="center">
  <strong>Proactive employee retention powered by Machine Learning and SHAP explainability, packaged in an ultra-premium dark UI.</strong>
</p>

---

## 📖 Overview

Employee turnover is expensive, costing companies anywhere from 50% to 200% of an employee's annual salary in recruiting, training, and lost productivity. Too often, HR teams are forced to be reactive, only taking action *after* a resignation letter has been submitted.

**Sentinel** is an AI-driven platform that predicts employee flight risk (attrition) before it happens. By leveraging a robust Random Forest model and SHAP (SHapley Additive exPlanations), Sentinel not only predicts *who* is likely to leave, but explains exactly *why*—empowering HR professionals and managers to take targeted, proactive measures.

## ✨ Features

- **Real-Time Attrition Prediction**: Instantly score the flight risk of any employee based on 44 demographic and professional features.
- **SHAP Explainability**: Go beyond a simple "High Risk" score. Sentinel explains the positive and negative driving factors behind every single prediction.
- **Interactive 3D/2D Visualizations**: Explore data dynamically with immersive 3D risk maps and detailed SHAP contribution charts using Plotly.
- **Global Analytics Dashboard**: Monitor company-wide attrition trends, department-specific risks, and maintain a high-risk employee watchlist.
- **Ultra-Premium UI**: A sleek, dark-themed glassmorphism interface designed for professional enterprise environments.

## 🛠 Tech Stack

| Category | Technology |
| --- | --- |
| **Programming Language** | Python 3.10+ |
| **Machine Learning / AI** | scikit-learn, SHAP, SMOTE |
| **Frontend** | Streamlit, Plotly |
| **Backend API** | FastAPI, Uvicorn |
| **Database** | SQLite, SQLAlchemy |
| **Deployment** | Docker, GitHub Actions |
| **Data Manipulation** | Pandas, NumPy |

## 🏗 Project Architecture

Sentinel uses a decoupled architecture, separating the ultra-premium frontend from the robust AI backend.

```ascii
      User
       │
       ▼
 ┌────────────┐
 │  Frontend  │ (Streamlit, UI, Plotly Charts)
 └──────┬─────┘
        │ REST API calls
        ▼
 ┌────────────┐
 │ Backend API│ (FastAPI, Request Validation)
 └──────┬─────┘
        │
        ▼
 ┌────────────┐
 │  AI Model  │ (Scikit-Learn RF + SHAP Explainer)
 └──────┬─────┘
        │
        ▼
 ┌────────────┐
 │  Database  │ (SQLite - Prediction History)
 └────────────┘
```

## 📁 Folder Structure

```text
hr-attrition/
├── api/                    # FastAPI backend service
│   ├── main.py             # API endpoints and routing
│   ├── database.py         # SQLAlchemy config
│   └── models.py           # DB Schemas & Pydantic models
├── streamlit_app/          # Streamlit frontend application
│   ├── app.py              # Ultra-premium UI and dashboard
│   └── requirements.txt    # Frontend dependencies
├── model/                  # ML models and scalers
│   ├── rf_model.pkl        # Trained Random Forest model
│   └── explainer.pkl       # Fitted SHAP explainer
├── notebooks/              # Jupyter notebooks for EDA and training
├── Dockerfile              # Docker configuration
└── README.md
```

## 🚀 Installation

Follow these steps to run Sentinel locally from scratch.

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/hr-attrition.git
cd hr-attrition
```

**2. Create a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install requirements**
```bash
# Install backend requirements (adjust path if requirements are split)
pip install -r requirements.txt

# Install frontend requirements
pip install -r streamlit_app/requirements.txt
```

**4. Environment Variables (Optional)**
Create a `.env` file in the root directory if you need to override defaults:
```env
API_URL=http://localhost:8000
```

**5. Run the Backend (FastAPI)**
Open a terminal, activate your virtual environment, and run:
```bash
uvicorn api.main:app --reload --port 8000
```

**6. Run the Frontend (Streamlit)**
Open a *new* terminal, activate your virtual environment, and run:
```bash
streamlit run streamlit_app/app.py --server.port 8501
```

## 💻 Usage

1. Navigate to `http://localhost:8501` in your web browser.
2. Ensure the **System Status** in the sidebar shows the Inference API as "Operational".
3. **Prediksi Risiko**: Enter employee data into the form and click "Analisis Risiko". The system will output the probability of attrition and an interactive SHAP chart explaining the key drivers.
4. **Analitik**: View the historical dashboard, global feature importances, and track your high-risk employee watchlist.

## 📸 Screenshots

*(Replace the placeholder links below with actual screenshots of your application)*

| Dashboard Overview | Risk Prediction Engine |
| :---: | :---: |
| <img src="https://via.placeholder.com/600x350.png?text=Dashboard+Analytics" width="100%"> | <img src="https://via.placeholder.com/600x350.png?text=SHAP+Explainability" width="100%"> |

## 🔌 API Documentation

The FastAPI backend automatically provides Swagger documentation at `http://localhost:8000/docs`. Key endpoints include:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Check API health and model loaded status. |
| `POST` | `/explain` | Run inference on employee data and return probability + SHAP contributions. |
| `GET` | `/predictions` | Fetch historical prediction logs. |
| `DELETE` | `/predictions` | Clear all prediction history. |
| `GET` | `/feature-importance`| Fetch the global feature importance of the Random Forest model. |

## 🤖 Machine Learning / AI Details

- **Dataset**: IBM HR Analytics Employee Attrition & Performance dataset (1,470 records, 44 features).
- **Data Preprocessing**: Categorical encoding and feature scaling. Handled extreme class imbalance using **SMOTE** (Synthetic Minority Over-sampling Technique).
- **Model Architecture**: Scikit-Learn **Random Forest Classifier**.
- **Evaluation Metrics**: Tuned heavily for **Recall** to ensure high-risk employees are not missed.
- **Model Performance**: 
  - **ROC-AUC**: 0.78
  - **Recall**: 0.70
  - **F1-Score**: 0.49
  - *Note: Threshold is explicitly tuned to ~0.28 to maximize the capture of at-risk employees at the slight cost of precision.*

## 🔮 Future Improvements

- Add batch prediction capabilities via CSV upload.
- Integrate active learning to retrain the model as new attrition data flows in.
- Implement Role-Based Access Control (RBAC) to restrict sensitive HR data.
- Add automated email alerts for employees entering the "Critical" risk tier.

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## ✍️ Author

**Your Name**  
AI Engineer / Data Scientist  
- 🐙 [GitHub](https://github.com/yourusername)  
- 💼 [LinkedIn](https://linkedin.com/in/yourusername)  
- ✉️ [Email](mailto:your.email@example.com)  

---
<p align="center">
  <i>Built with ❤️ by an AI Engineer for the future of HR.</i>
</p>
