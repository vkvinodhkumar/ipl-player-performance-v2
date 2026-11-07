import numpy as np
import pandas as pd

from .model_loader import load_model_registry, load_dl_bundle
from .output import format_prediction


class InferenceInputError(ValueError):
    """Raised when inference input does not match model requirements."""


def _to_dataframe(features):
    if isinstance(features, pd.DataFrame):
        frame = features.copy()
    elif isinstance(features, dict):
        frame = pd.DataFrame([features])
    else:
        raise InferenceInputError(
            "Input must be a pandas DataFrame or dictionary."
        )

    if frame.empty:
        raise InferenceInputError("Inference input cannot be empty.")

    if frame.columns.duplicated().any():
        raise InferenceInputError("Duplicate input columns are not allowed.")

    return frame


def predict_dl(category, features):
    """
    Generate predictions for every registered DL target in a category.

    category: 'batting' or 'bowling'
    features: one dictionary or a pandas DataFrame
    """

    if category not in {"batting", "bowling"}:
        raise InferenceInputError(
            "Category must be 'batting' or 'bowling'."
        )

    frame = _to_dataframe(features)
    registry = load_model_registry()

    targets = [
        (target, item)
        for target, item in registry["models"].items()
        if item.get("category") == category
    ]

    if not targets:
        raise InferenceInputError(
            f"No registered DL models found for {category}."
        )

    results = {}

    for target, item in targets:
        bundle = load_dl_bundle(target)
        preprocessor = bundle["preprocessor"]

        required_features = list(preprocessor.feature_names_in_)
        missing = [
            column for column in required_features
            if column not in frame.columns
        ]

        if missing:
            raise InferenceInputError(
                f"{target} is missing required features: {missing}"
            )

        model_input = frame.loc[:, required_features]

        try:
            transformed = preprocessor.transform(model_input)
            transformed = np.asarray(transformed, dtype=np.float32)

            if transformed.shape[1] != bundle["feature_count"]:
                raise InferenceInputError(
                    f"{target}: expected {bundle['feature_count']} "
                    f"transformed features, got {transformed.shape[1]}."
                )

            model = bundle["model"]

            if transformed.shape[1] != model.input_shape[-1]:
                raise InferenceInputError(
                    f"{target}: transformed feature count does not "
                    "match the Keras model input."
                )

            scaled_predictions = np.asarray(
                model(transformed, training=False)
            ).reshape(-1, 1)

            raw_predictions = bundle["scaler"].inverse_transform(
                scaled_predictions
            ).reshape(-1)

        except InferenceInputError:
            raise
        except Exception as exc:
            raise RuntimeError(
                f"DL inference failed for {target}: {exc}"
            ) from exc

        if len(raw_predictions) != len(frame):
            raise RuntimeError(
                f"{target}: prediction count does not match input rows."
            )

        results[target] = [
            format_prediction(target, value)
            for value in raw_predictions
        ]

    return {
        "category": category,
        "model_type": "DL",
        "rows": len(frame),
        "predictions": results,
    }
