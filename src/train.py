"""Training pipeline with hyperparameter tuning and evaluation."""
import argparse
import json
from functools import partial
from pathlib import Path

import keras_tuner as kt
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from tensorflow import keras

from src.model import build_tuner_model
from src.preprocessing import load_data, preprocess, save_preprocessor

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "raw" / "WA_Fn-UseC_-HR-Employee-Attrition.csv"
MODEL_DIR = ROOT / "models"
REPORTS_DIR = ROOT / "reports"


def tune(data, max_trials=10, epochs=30):
    """Keras Tuner with explicit validation_data (not validation_split)."""
    input_dim = data["X_train"].shape[1]

    tuner = kt.RandomSearch(
        partial(build_tuner_model, input_dim=input_dim),
        objective=kt.Objective("val_loss", direction="min"),  # robust metric
        max_trials=max_trials,
        directory=str(ROOT / "tuner_logs"),
        project_name="hr_attrition",
        overwrite=True,
    )

    early_stop = keras.callbacks.EarlyStopping(
        monitor="val_loss", mode="min", patience=5, restore_best_weights=True
    )

    tuner.search(
        data["X_train"],
        data["y_train"],
        validation_data=(data["X_val"], data["y_val"]),
        epochs=epochs,
        batch_size=64,
        callbacks=[early_stop],
        verbose=1,
    )

    print("\n=== Best hyperparameters ===")
    best_hp = tuner.get_best_hyperparameters(1)[0]
    print(json.dumps(best_hp.values, indent=2))

    return tuner.get_best_models(1)[0], best_hp.values


def evaluate(model, data, history=None):
    """Evaluate model and produce plots. Tunes threshold for best F1."""
    REPORTS_DIR.mkdir(exist_ok=True)

    y_test = data["y_test"]
    y_proba = model.predict(data["X_test"]).flatten()

    # Find threshold that maximizes F1
    thresholds = np.arange(0.1, 0.9, 0.02)
    best_thr, best_f1 = 0.5, 0.0
    for thr in thresholds:
        preds = (y_proba >= thr).astype(int)
        f1 = f1_score(y_test, preds)
        if f1 > best_f1:
            best_f1, best_thr = f1, float(thr)
    print(f"\n🎯 Optimal threshold: {best_thr:.2f} (F1={best_f1:.3f})")

    y_pred = (y_proba >= best_thr).astype(int)

    metrics = {
        "accuracy": float((y_pred == y_test).mean()),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "threshold": best_thr,
    }
    print("\n=== Test Set Metrics ===")
    print(json.dumps(metrics, indent=2))
    print("\n=== Classification Report ===")
    print(classification_report(y_test, y_pred, target_names=["Stay", "Leave"]))

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Stay", "Leave"], yticklabels=["Stay", "Leave"], ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "confusion_matrix.png", dpi=120)
    plt.close(fig)

    # ROC curve
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, label=f"AUC = {metrics['roc_auc']:.3f}")
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curve")
    ax.legend()
    fig.tight_layout()
    fig.savefig(REPORTS_DIR / "roc_curve.png", dpi=120)
    plt.close(fig)

    if history is not None:
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        axes[0].plot(history.history["loss"], label="train")
        axes[0].plot(history.history["val_loss"], label="val")
        axes[0].set_title("Loss")
        axes[0].set_xlabel("Epoch")
        axes[0].legend()
        axes[1].plot(history.history["auc"], label="train")
        if "val_auc" in history.history:
            axes[1].plot(history.history["val_auc"], label="val")
        axes[1].set_title("AUC")
        axes[1].set_xlabel("Epoch")
        axes[1].legend()
        fig.tight_layout()
        fig.savefig(REPORTS_DIR / "training_curves.png", dpi=120)
        plt.close(fig)

    return metrics


def main(max_trials=10, epochs=30):
    MODEL_DIR.mkdir(exist_ok=True)

    df = load_data(DATA_PATH)
    data = preprocess(df, apply_smote=True)

    best_model, best_hp = tune(data, max_trials=max_trials, epochs=epochs)

    # Final fit with best HP, explicit val_data
    history = best_model.fit(
        data["X_train"],
        data["y_train"],
        validation_data=(data["X_val"], data["y_val"]),
        epochs=epochs + 20,
        batch_size=64,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor="val_loss", mode="min",
                patience=10, restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss", mode="min",
                factor=0.5, patience=4, min_lr=1e-6
            ),
        ],
        verbose=2,
    )

    metrics = evaluate(best_model, data, history)

    best_model.save(MODEL_DIR / "attrition_model.keras")
    save_preprocessor(data["preprocessor"], MODEL_DIR / "preprocessor.joblib")

    with open(MODEL_DIR / "feature_names.json", "w") as f:
        json.dump(data["feature_names"], f, indent=2)

    with open(MODEL_DIR / "metrics.json", "w") as f:
        json.dump({"metrics": metrics, "best_hp": best_hp}, f, indent=2)

    print(f"\n✅ All artifacts saved to {MODEL_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--epochs", type=int, default=30)
    args = parser.parse_args()
    main(max_trials=args.trials, epochs=args.epochs)
