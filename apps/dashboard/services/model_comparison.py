import csv
import json
from pathlib import Path

from django.conf import settings


ARTIFACT_DIR = Path(settings.BASE_DIR) / "artifacts" / "model_comparison"


def _read_json(path):
    with path.open("r", encoding="utf-8-sig") as file:
        return json.load(file)


def _read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def get_model_comparison():
    selection = _read_json(
        ARTIFACT_DIR / "final_target_model_selection.json"
    )
    comparison = _read_csv(
        ARTIFACT_DIR / "corrected_ml_dl_baseline_comparison.csv"
    )

    selected_models = selection["models"]
    results = []

    for target, selection_info in selected_models.items():
        target_rows = [
            row for row in comparison if row["target"] == target
        ]

        selected_model = selection_info["model"]

        selected_row = next(
            (row for row in target_rows if row["model"] == selected_model),
            None,
        )

        baseline_row = next(
            (
                row for row in target_rows
                if row["model"] == "Training_Mean_Baseline"
            ),
            None,
        )

        if not selected_row or not baseline_row:
            continue

        selected_mae = float(selected_row["MAE"])
        baseline_mae = float(baseline_row["MAE"])

        improvement = (
            ((baseline_mae - selected_mae) / baseline_mae) * 100
            if baseline_mae else 0
        )

        results.append({
            "category": selected_row["category"].title(),
            "target": target.replace("target_next_match_", "").replace("_", " ").title(),
            "target_key": target,
            "selected_model": selected_model,
            "model_type": selected_row["model_type"],
            "test_rows": int(selected_row["test_rows"]),
            "mae": selected_mae,
            "rmse": float(selected_row["RMSE"]),
            "baseline_mae": baseline_mae,
            "baseline_rmse": float(baseline_row["RMSE"]),
            "mae_improvement": improvement,
            "reason": selection_info.get("reason", ""),
            "model_results": [
                {
                    "model": row["model"],
                    "model_type": row["model_type"],
                    "mae": float(row["MAE"]),
                    "rmse": float(row["RMSE"]),
                }
                for row in target_rows
            ],
        })

    batting = [row for row in results if row["category"] == "Batting"]
    bowling = [row for row in results if row["category"] == "Bowling"]

    return {
        "results": results,
        "batting": batting,
        "bowling": bowling,
        "total_targets": len(results),
        "dl_count": sum(r["model_type"] == "Deep Learning" for r in results),
        "ml_count": sum(r["model_type"] == "Machine Learning" for r in results),
        "test_period": selection["selection_policy"]["test_period"],
        "selection_policy": selection["selection_policy"],
        "baseline_discrepancy": (
            "Saved bowling DummyRegressor metrics differ from the "
            "independently recalculated training-mean baseline. "
            "The precise historical cause has not been established."
        ),
    }