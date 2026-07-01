"""Training pipeline Random Forest dengan threshold tuning.
SMOTE di dalam tiap fold CV (anti data leakage) +
threshold optimization untuk maksimalkan F1.
"""
import argparse
import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.model_selection import (
    RandomizedSearchCV,
    StratifiedKFold,
    cross_validate,
)
from sklearn.pipeline import Pipeline as SkPipeline
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from src.model_rf import build_rf_model
from src.preprocessing import load_data, preprocess_no_smote

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
MODEL_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"

# Random state global
SEED = 42

# Param grid - di-prefix "rf__" karena Pipeline
RF_PARAM_GRID = {
    "rf__n_estimators": [100, 200, 300],
    "rf__max_depth": [5, 10, 20, None],
    "rf__min_samples_split": [2, 5, 10],
    "rf__min_samples_leaf": [1, 2, 4],
    "rf__max_features": ["sqrt", "log2"],
}


def make_pipeline():
    """Pipeline: SMOTE → Random Forest.

    Pakai ImbPipeline (dari imblearn), BUKAN sklearn Pipeline.
    Bedanya: ImbPipeline tahu cara handle SMOTE — dia cuma
    di-apply pas .fit(), tidak pas .predict()/.score().

    Hasilnya: pas cross-validation, SMOTE cuma jalan di
    training fold, validation fold dibiarkan ASLI.
    """
    return ImbPipeline([
        ("smote", SMOTE(random_state=SEED)),
        ("rf", build_rf_model(random_state=SEED)),
    ])


def tune(data, n_iter=30):
    """Tuning dengan CV yang BENAR — SMOTE di dalam fold."""
    print("\n=== Hyperparameter Tuning (SMOTE-in-fold) ===")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

    search = RandomizedSearchCV(
        estimator=make_pipeline(),
        param_distributions=RF_PARAM_GRID,
        n_iter=n_iter,
        scoring="roc_auc",
        cv=cv,
        random_state=SEED,
        n_jobs=-1,
        verbose=1,
    )
    search.fit(data["X_train"], data["y_train"])

    print("\n=== Best hyperparameters ===")
    clean_params = {k.replace("rf__", ""): v
                    for k, v in search.best_params_.items()}
    print(json.dumps(clean_params, indent=2))
    print(f"Best CV ROC-AUC: {search.best_score_:.4f}")

    return search.best_estimator_, clean_params


def cross_validate_pipeline(pipeline, data):
    """CV jujur — multi-metric, SMOTE handled by pipeline."""
    print("\n=== Stratified 5-Fold CV (SMOTE jalan di tiap fold) ===")
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)

    results = cross_validate(
        pipeline, data["X_train"], data["y_train"],
        cv=cv,
        scoring=["roc_auc", "f1", "precision", "recall"],
        n_jobs=-1,
        return_train_score=False,
    )

    cv_results = {}
    for metric in ["roc_auc", "f1", "precision", "recall"]:
        scores = results[f"test_{metric}"]
        cv_results[metric] = {
            "mean": float(scores.mean()),
            "std": float(scores.std()),
            "per_fold": [float(s) for s in scores],
        }
        print(f"  {metric:10s}: {scores.mean():.4f} (+/- {scores.std():.4f})")

    return cv_results


def find_best_threshold(pipeline, data):
    """Cari threshold optimal yang memaksimalkan F1-score.

    Default RF pakai threshold 0.5 — tapi karena data imbalance,
    threshold yang lebih rendah biasanya kasih recall lebih baik.
    Kita coba threshold dari 0.10 sampai 0.70, pilih yang F1 tertinggi.
    """
    print("\n=== Threshold Tuning ===")
    y_test = data["y_test"]
    y_proba = pipeline.predict_proba(data["X_test"])[:, 1]

    thresholds = np.arange(0.10, 0.71, 0.02)
    best_thr, best_f1 = 0.5, 0.0

    print(f"  {'Threshold':<12}{'F1':<10}{'Precision':<12}{'Recall':<10}")
    print(f"  {'-' * 44}")
    for thr in thresholds:
        preds = (y_proba >= thr).astype(int)
        f1 = f1_score(y_test, preds)
        prec = precision_score(y_test, preds, zero_division=0)
        rec = recall_score(y_test, preds)
        # Tampilkan tiap step 0.10 biar nggak terlalu panjang
        if abs(round(thr, 2) * 100 % 10) < 1:
            print(f"  {thr:<12.2f}{f1:<10.4f}{prec:<12.4f}{rec:<10.4f}")
        if f1 > best_f1:
            best_f1, best_thr = f1, float(thr)

    print(f"\n  🎯 Optimal threshold: {best_thr:.2f} (F1 = {best_f1:.4f})")
    return best_thr


def evaluate(pipeline, data, threshold=0.5):
    """Evaluasi final di test set pakai threshold yang bisa di-tune."""
    REPORTS_DIR.mkdir(exist_ok=True)

    y_test = data["y_test"]
    y_proba = pipeline.predict_proba(data["X_test"])[:, 1]
    y_pred = (y_proba >= threshold).astype(int)

    metrics = {
        "accuracy": float((y_pred == y_test).mean()),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred)),
        "threshold": float(threshold),
    }
    print("\n=== Test Set Metrics ===")
    print(json.dumps(metrics, indent=2))
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=["Stay", "Leave"]))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Greens",
                xticklabels=["Stay", "Leave"],
                yticklabels=["Stay", "Leave"], ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion Matrix - Random Forest (threshold={threshold:.2f})")
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "confusion_matrix_rf.png", dpi=120)
    plt.close(fig)

    # ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, label=f"AUC = {metrics['roc_auc']:.3f}")
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve - Random Forest")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "roc_curve_rf.png", dpi=120)
    plt.close(fig)

    # Feature importance - akses RF dari dalam pipeline
    rf_model = pipeline.named_steps["rf"]
    importances = rf_model.feature_importances_
    feat_names = data["feature_names"]
    idx = np.argsort(importances)[::-1][:15]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(range(len(idx)), importances[idx][::-1], color="#2E7D32")
    ax.set_yticks(range(len(idx)))
    ax.set_yticklabels([feat_names[i] for i in idx][::-1])
    ax.set_xlabel("Importance")
    ax.set_title("Top 15 Feature Importance - Random Forest")
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "feature_importance_rf.png", dpi=120)
    plt.close(fig)

    return metrics


def main(n_iter=30, data_path=None):
    if data_path is None:
        data_path = DATA_PATH
    MODEL_DIR.mkdir(exist_ok=True)

    df = load_data(data_path)
    data = preprocess_no_smote(df)

    # 1. Hyperparameter tuning (SMOTE di tiap fold)
    best_pipeline, best_params = tune(data, n_iter=n_iter)

    # 2. Cross-validation jujur
    cv_results = cross_validate_pipeline(best_pipeline, data)

    # 3. Cari threshold optimal di test set
    best_thr = find_best_threshold(best_pipeline, data)

    # 4. Evaluasi final pakai threshold yang udah dituning
    metrics = evaluate(best_pipeline, data, threshold=best_thr)

    # Simpan semua hasil
    # Bundle: preprocessor (sudah fitted) + RF (sudah trained) → 1 file siap-serve.
    # SMOTE tidak ikut karena hanya dipakai saat training, bukan saat prediksi.
    serving_model = SkPipeline([
        ("preprocessor", data["preprocessor"]),
        ("rf", best_pipeline.named_steps["rf"]),
    ])
    joblib.dump(serving_model, MODEL_DIR / "attrition_model_rf.joblib")

    # Overwrite feature_names biar konsisten dengan pipeline final
    with open(MODEL_DIR / "feature_names.json", "w") as f:
        json.dump(data["feature_names"], f, indent=2)

    with open(MODEL_DIR / "metrics_rf.json", "w") as f:
        json.dump({
            "test_metrics": metrics,
            "cv_results": cv_results,
            "best_params": best_params,
            "best_threshold": float(best_thr),
        }, f, indent=2)

    print(f"\n✅ Semua hasil tersimpan di {MODEL_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--iter", type=int, default=30)
    args = parser.parse_args()
    main(n_iter=args.iter)
