from pathlib import Path
from functools import lru_cache
import json

import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[3]

REGISTRY_PATH = PROJECT_ROOT / "artifacts" / "dl_models" / "model_registry.json"

OUTPUT_POLICY_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "model_comparison"
    / "output_constraint_policy.json"
)

ML_MODEL_PATHS = {
    "batting": PROJECT_ROOT / "models" / "batting" / "original_gb_model.joblib",
    "bowling": PROJECT_ROOT / "models" / "bowling" / "wickets_model.joblib",
}


class ModelArtifactError(RuntimeError):
    """Raised when a required model artifact cannot be loaded."""


def _validate_path(path):
    path = path.resolve()

    if not path.is_relative_to(PROJECT_ROOT.resolve()):
        raise ModelArtifactError(f"Artifact path outside project: {path}")

    if not path.is_file():
        raise ModelArtifactError(f"Artifact not found: {path}")

    return path


@lru_cache(maxsize=1)
def load_model_registry():
    path = _validate_path(REGISTRY_PATH)

    with path.open("r", encoding="utf-8") as file:
        registry = json.load(file)

    if not isinstance(registry.get("models"), dict):
        raise ModelArtifactError("Invalid model registry structure.")

    return registry


@lru_cache(maxsize=1)
def load_output_policy():
    path = _validate_path(OUTPUT_POLICY_PATH)

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache(maxsize=10)
def load_dl_bundle(target):
    registry = load_model_registry()
    item = registry["models"].get(target)

    if item is None:
        raise ModelArtifactError(f"Unknown DL target: {target}")

    paths = {
        key: _validate_path(PROJECT_ROOT / item[key])
        for key in ("model_path", "preprocessor_path", "scaler_path")
    }

    try:
        import tensorflow as tf

        model = tf.keras.models.load_model(
            paths["model_path"],
            compile=False,
        )

        preprocessor = joblib.load(paths["preprocessor_path"])
        scaler = joblib.load(paths["scaler_path"])

    except Exception as exc:
        raise ModelArtifactError(
            f"Failed to load DL artifacts for {target}: {exc}"
        ) from exc

    return {
        "target": target,
        "category": item["category"],
        "model": model,
        "preprocessor": preprocessor,
        "scaler": scaler,
        "feature_count": item["feature_count"],
    }


@lru_cache(maxsize=2)
def load_ml_model(category):
    if category not in ML_MODEL_PATHS:
        raise ModelArtifactError(f"Unknown ML category: {category}")

    path = _validate_path(ML_MODEL_PATHS[category])

    try:
        return joblib.load(path)
    except Exception as exc:
        raise ModelArtifactError(
            f"Failed to load {category} ML model: {exc}"
        ) from exc


def clear_model_cache():
    """Clear cached models and configuration, useful for testing."""
    load_dl_bundle.cache_clear()
    load_ml_model.cache_clear()
    load_model_registry.cache_clear()
    load_output_policy.cache_clear()
