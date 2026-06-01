# 🚀 Quickstart - Eksekusi 1 Hari

## STEP 1: Setup (5 menit)

```bash
# Unzip & masuk folder
cd hr-attrition

# Buat virtual env
python -m venv venv
source venv/bin/activate     # Linux/Mac
# venv\Scripts\activate      # Windows

# Install deps
pip install -r requirements.txt
```

## STEP 2: Download Dataset (2 menit)

Download dari Kaggle:
https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset

Letakkan file `WA_Fn-UseC_-HR-Employee-Attrition.csv` di:
```
data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv
```

## STEP 3: EDA (30 menit)

```bash
jupyter notebook notebooks/01_eda.ipynb
```
Jalanin semua cell. Screenshot plot-plot penting buat slide.

## STEP 4: Training Model (15-30 menit)

```bash
python -m src.train --trials 10 --epochs 30
```

Output:
- `models/attrition_model.keras`
- `models/preprocessor.joblib`
- `models/metrics.json`
- `reports/confusion_matrix.png`
- `reports/roc_curve.png`
- `reports/training_curves.png`

## STEP 5: Jalanin API (1 menit)

Terminal 1:
```bash
uvicorn api.main:app --reload --port 8000
```

Test:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/health

## STEP 6: Jalanin Streamlit UI (1 menit)

Terminal 2:
```bash
streamlit run streamlit_app/app.py
```

Buka: http://localhost:8501

## STEP 7: Push ke GitHub (5 menit)

```bash
git init
git add .
git commit -m "feat: HR attrition predictor with DNN + FastAPI + Streamlit"
git branch -M main
git remote add origin git@github.com:USERNAME/hr-attrition.git
git push -u origin main
```

GitHub Actions akan otomatis jalan (lint + test + docker build).

## STEP 8: Slide Presentasi (sudah ada!)

✅ **`presentation/HR_Attrition_Predictor.pptx`** — 14 slide siap pakai.

Kamu tinggal:
1. Buka di PowerPoint / Google Slides
2. Ganti angka di slide 10 (Model Evaluation) dengan **hasil training kamu sendiri** dari `models/metrics.json`
3. Ganti placeholder education jika perlu disesuaikan
4. Tambahkan screenshot Streamlit kamu di slide 12 jika mau lebih kuat

Plus: **`LITERATURE_REVIEW.md`** — 6 paper referensi yang udah disusun rapi (Frye, Yedida, Chawla SMOTE, Fallucchi, Sculley, SHRM). Sebut ini saat presentasi untuk poin metodologi penelitian.

### Outline 14 Slide

1. **Title** - HR Attrition Predictor
2. **Self Intro** - Niko, fresh grad AI/ML
3. **Overview Projects** - sebutkan project lain (RAG chatbot, AI interview)
4. **Problem Statement** - cost turnover, reactive HR
5. **Data Understanding** - IBM dataset, 1470 rows, 35 features, 16% attrition
6. **Data Preprocessing** - drop constants, encoding, scaling, SMOTE
7. **EDA** - 3-4 plots paling insightful (OverTime, MonthlyIncome, Age, correlation heatmap)
8. **Model Architecture** - DNN diagram (input → 128 → 64 → 32 → 1)
9. **Hyperparameter Tuning** - Keras Tuner Random Search, best HP table
10. **Evaluation** - confusion matrix, ROC curve, F1/AUC/Accuracy
11. **Deployment** - architecture diagram (Streamlit → FastAPI → Model → SQLite)
12. **Demo Screenshots** - Streamlit predict + dashboard pages
13. **CI/CD** - screenshot GitHub Actions green checkmark
14. **Conclusion & Recommendation** - business value, future work

## 🆘 Troubleshooting

**`ModuleNotFoundError: No module named 'src'`**
→ Jalanin dari root folder pakai `python -m src.train` (bukan `python src/train.py`)

**TensorFlow install gagal di Mac M1/M2**
→ Ganti `tensorflow==2.16.1` jadi `tensorflow-macos==2.16.1` di requirements.txt

**API 503 "Model not loaded"**
→ Belum training. Jalanin `python -m src.train` dulu.

**Streamlit "Cannot connect to API"**
→ API belum jalan. Buka terminal baru, run uvicorn.

## ⏱️ Estimasi Total Waktu

| Task | Waktu |
|------|-------|
| Setup + download data | 10 min |
| EDA + screenshot | 30 min |
| Training (tuning 10 trials) | 30 min |
| Testing API + UI | 15 min |
| Push GitHub + CI | 15 min |
| Slide presentasi | 90 min |
| **Total** | **~3 jam** |

Sisanya buat polish + latihan presentasi. 🔥
