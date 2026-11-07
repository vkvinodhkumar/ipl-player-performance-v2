import numpy as np
import pandas as pd

from .model_loader import load_ml_model
from .dl_inference import _to_dataframe, InferenceInputError
from .output import format_prediction


ML_TARGETS = {
    "batting": "target_next_match_runs_scored",
    "bowling": "target_next_match_wickets",
}


def predict_ml(category, features):
    """Generate predictions using the selected production ML pipeline."""

    if category not in ML_TARGETS:
        raise InferenceInputError(
            "Category must be 'batting' or 'bowling'."
        )

    frame = _to_dataframe(features)
    model = load_ml_model(category)

    required_features = list(model.feature_names_in_)
    missing = [
        column for column in required_features
        if column not in frame.columns
    ]

    if missing:
        raise InferenceInputError(
            f"{category} ML model is missing required features: {missing}"
        )

    model_input = frame.loc[:, required_features]

    try:
        raw_predictions = np.asarray(
            model.predict(model_input)
        ).reshape(-1)

    except Exception as exc:
        raise RuntimeError(
            f"{category} ML inference failed: {exc}"
        ) from exc

    if len(raw_predictions) != len(frame):
        raise RuntimeError(
            "ML prediction count does not match input rows."
        )

    target = ML_TARGETS[category]

    predictions = [
        format_prediction(target, value)
        for value in raw_predictions
    ]

    return {
        "category": category,
        "model_type": "ML",
        "rows": len(frame),
        "predictions": {
            target: predictions
        },
    }
