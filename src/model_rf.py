"""Random Forest model untuk binary attrition classification.
Pembanding dari model DNN (lihat model.py).
"""
from sklearn.ensemble import RandomForestClassifier


def build_rf_model(
    n_estimators=200,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features="sqrt",
    random_state=42,
):
    """Bangun Random Forest classifier.

    Args:
        n_estimators: jumlah pohon dalam forest
        max_depth: kedalaman maksimal tiap pohon (None = tanpa batas)
        min_samples_split: minimal sampel untuk memecah node
        min_samples_leaf: minimal sampel di tiap daun
        max_features: jumlah fitur dipertimbangkan tiap split
        random_state: seed untuk reproducibility
    """
    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        min_samples_leaf=min_samples_leaf,
        max_features=max_features,
        random_state=random_state,
        n_jobs=-1,                  # pakai semua CPU core
        class_weight="balanced",    # bantu tangani sisa imbalance
    )
    return model


# Search space untuk hyperparameter tuning
RF_PARAM_GRID = {
    "n_estimators": [100, 200, 300],
    "max_depth": [5, 10, 20, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2"],
}