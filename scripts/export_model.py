"""
Export du modèle depuis MLflow vers des fichiers standalone dans artifacts/.

Ce script extrait le modèle enregistré dans MLflow et le sauvegarde
sous forme de fichiers indépendants pour le déploiement en production,
sans dépendance à MLflow au runtime.

Usage:
    cd notebooks/  # MLflow DB est dans ce dossier
    python ../scripts/export_model.py
"""

import json
import shutil
import sys
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn

# Chemins
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

# MLflow config — la DB est dans notebooks/
MLFLOW_DB = PROJECT_ROOT / "notebooks" / "mlflow.db"
MODEL_NAME = "Credit_Scoring_Model_LGBM"


def main():
    print("=" * 60)
    print("EXPORT DU MODÈLE DEPUIS MLFLOW")
    print("=" * 60)

    # 1. Configurer MLflow
    mlflow.set_tracking_uri(f"sqlite:///{MLFLOW_DB}")
    print(f"Tracking URI: sqlite:///{MLFLOW_DB}")

    # 2. Charger le modèle depuis le registry
    model_uri = f"models:/{MODEL_NAME}/latest"
    print(f"Chargement du modèle: {model_uri}")

    try:
        model = mlflow.sklearn.load_model(model_uri)
    except Exception as e:
        print(f"Erreur lors du chargement: {e}")
        sys.exit(1)

    print(f"Modèle chargé: {type(model).__name__}")

    # 3. Créer le dossier artifacts
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    # 4. Exporter le modèle avec joblib
    model_path = ARTIFACTS_DIR / "model.pkl"
    joblib.dump(model, model_path)
    print(f"Modèle exporté: {model_path} ({model_path.stat().st_size / 1024:.0f} KB)")

    # 5. Extraire et sauvegarder les noms de features
    feature_names = list(model.feature_name_)
    features_path = ARTIFACTS_DIR / "feature_names.json"
    with open(features_path, "w") as f:
        json.dump(feature_names, f, indent=2)
    print(f"Features exportées: {features_path} ({len(feature_names)} features)")

    # 6. Copier le scaler
    scaler_src = DATA_DIR / "scaler.pkl"
    scaler_dst = ARTIFACTS_DIR / "scaler.pkl"
    if scaler_src.exists():
        shutil.copy2(scaler_src, scaler_dst)
        print(f"Scaler copié: {scaler_dst}")
    else:
        print(f"Scaler non trouvé: {scaler_src}")

    # 7. Copier le metadata
    metadata_src = MODELS_DIR / "model_metadata.json"
    metadata_dst = ARTIFACTS_DIR / "model_metadata.json"
    if metadata_src.exists():
        shutil.copy2(metadata_src, metadata_dst)
        print(f"Metadata copié: {metadata_dst}")
    else:
        print(f"Metadata non trouvé: {metadata_src}")

    # 8. Vérification
    print("\n" + "=" * 60)
    print("VÉRIFICATION")
    print("=" * 60)

    model_check = joblib.load(model_path)
    with open(features_path) as f:
        features_check = json.load(f)

    print(f"Modèle rechargé: {type(model_check).__name__}")
    print(f"Features rechargées: {len(features_check)}")
    print(f"Artifacts dans {ARTIFACTS_DIR}:")
    for f in sorted(ARTIFACTS_DIR.iterdir()):
        print(f"  {f.name} ({f.stat().st_size / 1024:.0f} KB)")

    print("\nExport terminé.")


if __name__ == "__main__":
    main()
