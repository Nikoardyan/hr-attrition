"""
Preprocessing module untuk HR Attrition Predictor.
Implementasi pipeline preprocessing yang reusable & reproducible.

Catatan:
  - preprocess()         → versi lama (DNN): SMOTE sebelum return
  - preprocess_no_smote()→ versi baru (RF): SMOTE dilakukan di
                            dalam Pipeline saat CV (anti leakage)
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from typing import Tuple, Dict, List
import joblib


def load_data(path: str) -> pd.DataFrame:
    """Load CSV dataset."""
    df = pd.read_csv(path)
    print(f"✓ Loaded data: {df.shape}")
    return df


def clean_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Data cleaning:
    1. Cek missing values & duplikat
    2. Hapus kolom konstan (variance = 0)
    """
    n_missing = df.isnull().sum().sum()
    n_duplicates = df.duplicated().sum()

    if n_missing > 0:
        print(f"⚠️  Warning: {n_missing} missing values ditemukan")
    if n_duplicates > 0:
        print(f"⚠️  Warning: {n_duplicates} duplikat ditemukan")
        df = df.drop_duplicates().reset_index(drop=True)

    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    # Buang kolom ID — bukan fitur prediktif & tidak ada di schema API
    id_cols = [c for c in ["EmployeeNumber"] if c in df.columns]
    drop_cols = constant_cols + id_cols
    df_clean = df.drop(columns=drop_cols).copy()

    print(f"✓ Cleaning: {len(drop_cols)} kolom dihapus → {drop_cols}")
    print(f"  Shape: {df.shape} → {df_clean.shape}")

    return df_clean, drop_cols


def encode_target(df: pd.DataFrame, target_col: str = 'Attrition') -> Tuple[pd.DataFrame, np.ndarray]:
    """Encode target dari Yes/No → 1/0."""
    y = df[target_col].map({'Yes': 1, 'No': 0}).values
    X = df.drop(columns=[target_col])
    print(f"✓ Target encoded: {np.bincount(y)} (class 0, class 1)")
    return X, y


def build_preprocessor(X: pd.DataFrame) -> Tuple[ColumnTransformer, List[str], List[str]]:
    """Bikin preprocessor: StandardScaler (numerik) + OneHotEncoder (kategorikal)."""
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), categorical_cols)
        ],
        remainder='drop'
    )

    print("✓ Preprocessor built:")
    print(f"    {len(numerical_cols)} numerical → StandardScaler")
    print(f"    {len(categorical_cols)} categorical → OneHotEncoder")

    return preprocessor, numerical_cols, categorical_cols


# ============================================================
# VERSI LAMA — dipakai untuk DNN (train.py)
# ============================================================
def preprocess(
    df: pd.DataFrame,
    target_col: str = 'Attrition',
    test_size: float = 0.2,
    random_state: int = 42,
    apply_smote: bool = True
) -> Dict:
    """End-to-end preprocessing pipeline (versi DNN — SMOTE sebelum return)."""
    print("\n" + "=" * 60)
    print("PREPROCESSING PIPELINE (DNN)")
    print("=" * 60)

    print("\n[1/5] Data Cleaning")
    df_clean, dropped_cols = clean_data(df)

    print("\n[2/5] Encode Target")
    X, y = encode_target(df_clean, target_col)

    print(f"\n[3/5] Stratified Train-Test Split ({int((1 - test_size) * 100)}:{int(test_size * 100)})")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    print(f"  Train: {X_train.shape[0]} | Class dist: {np.bincount(y_train)}")
    print(f"  Test : {X_test.shape[0]} | Class dist: {np.bincount(y_test)}")

    print("\n[4/5] Feature Transformation")
    preprocessor, num_cols, cat_cols = build_preprocessor(X_train)
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(cat_cols).tolist()
    feature_names = num_cols + cat_feature_names
    print(f"  Features setelah one-hot: {len(feature_names)}")

    if apply_smote:
        print("\n[5/5] SMOTE on Training Set Only")
        smote = SMOTE(random_state=random_state)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train_processed, y_train)
        print(f"  Train sebelum SMOTE: {X_train_processed.shape[0]} | {np.bincount(y_train)}")
        print(f"  Train sesudah SMOTE: {X_train_balanced.shape[0]} | {np.bincount(y_train_balanced)}")
    else:
        print("\n[5/5] SMOTE Skipped (apply_smote=False)")
        X_train_balanced = X_train_processed
        y_train_balanced = y_train

    print("\n" + "=" * 60)
    print("✓ PREPROCESSING SELESAI (DNN)")
    print("=" * 60)

    return {
        'X_train': X_train_balanced,
        'X_test': X_test_processed,
        'y_train': y_train_balanced,
        'y_test': y_test,
        'preprocessor': preprocessor,
        'feature_names': feature_names,
        'dropped_cols': dropped_cols,
        'num_cols': num_cols,
        'cat_cols': cat_cols,
    }


# ============================================================
# VERSI BARU — dipakai untuk Random Forest (train_rf.py)
# ============================================================
def preprocess_no_smote(
    df: pd.DataFrame,
    target_col: str = 'Attrition',
    test_size: float = 0.2,
    random_state: int = 42,
) -> Dict:
    """
    Versi preprocess TANPA SMOTE.

    Dipakai untuk Random Forest dengan cross-validation,
    di mana SMOTE harus diterapkan di dalam tiap fold CV
    (pakai imblearn Pipeline) — supaya tidak terjadi data
    leakage ke fold validasi.

    Steps:
        1. Clean data
        2. Encode target Yes/No → 1/0
        3. Stratified train-test split
        4. Fit preprocessor on train, transform train & test
        (SMOTE TIDAK dilakukan di sini)
    """
    print("\n" + "=" * 60)
    print("PREPROCESSING PIPELINE (Random Forest — NO SMOTE)")
    print("=" * 60)

    print("\n[1/4] Data Cleaning")
    df_clean, dropped_cols = clean_data(df)

    print("\n[2/4] Encode Target")
    X, y = encode_target(df_clean, target_col)

    print(f"\n[3/4] Stratified Train-Test Split ({int((1 - test_size) * 100)}:{int(test_size * 100)})")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )
    print(f"  Train: {X_train.shape[0]} | Class dist: {np.bincount(y_train)}")
    print(f"  Test : {X_test.shape[0]} | Class dist: {np.bincount(y_test)}")

    print("\n[4/4] Feature Transformation")
    preprocessor, num_cols, cat_cols = build_preprocessor(X_train)
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(cat_cols).tolist()
    feature_names = num_cols + cat_feature_names
    print(f"  Features setelah one-hot: {len(feature_names)}")

    print("\n" + "=" * 60)
    print("✓ PREPROCESSING SELESAI — siap untuk Pipeline + SMOTE-in-fold")
    print("=" * 60)

    return {
        'X_train': X_train_processed,
        'X_test': X_test_processed,
        'y_train': y_train,        # ← masih asli, BELUM di-SMOTE
        'y_test': y_test,
        'preprocessor': preprocessor,
        'feature_names': feature_names,
        'dropped_cols': dropped_cols,
        'num_cols': num_cols,
        'cat_cols': cat_cols,
    }


def save_artifacts(artifacts: Dict, output_dir: str = 'models/'):
    """Simpan preprocessor & feature names."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    joblib.dump(artifacts['preprocessor'], f"{output_dir}/preprocessor.joblib")

    import json
    with open(f"{output_dir}/feature_names.json", 'w') as f:
        json.dump(artifacts['feature_names'], f, indent=2)

    print(f"✓ Artifacts saved to {output_dir}")


def save_preprocessor(preprocessor, path):
    """Alias untuk simpan preprocessor saja (dipakai train.py DNN)."""
    import os
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(preprocessor, path)


# ============================================================
# USAGE EXAMPLE
# ============================================================
if __name__ == '__main__':
    df = load_data('data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv')
    artifacts = preprocess(df, target_col='Attrition', test_size=0.2, apply_smote=True)
    save_artifacts(artifacts, output_dir='models/')

    print("\nShape final:")
    print(f"  X_train: {artifacts['X_train'].shape}")
    print(f"  X_test : {artifacts['X_test'].shape}")
    print(f"  Features: {len(artifacts['feature_names'])}")
