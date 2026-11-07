import math
from decimal import Decimal, ROUND_HALF_UP

from .model_loader import load_output_policy


def format_prediction(target, raw_prediction):
    """Preserve raw prediction and apply the configured output constraints."""

    try:
        raw = float(raw_prediction)
    except (TypeError, ValueError) as exc:
        raise ValueError("Prediction must be numeric.") from exc

    if not math.isfinite(raw):
        raise ValueError("Prediction must be finite.")

    policy = load_output_policy()

    count_targets = set(policy["count_targets"])
    rate_targets = set(policy["rate_targets"])

    value = max(Decimal(str(raw)), Decimal("0"))

    if target in count_targets:
        constrained = int(
            value.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
        )
    elif target in rate_targets:
        constrained = float(
            value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )
    else:
        raise ValueError(f"Unknown prediction target: {target}")

    return {
        "target": target,
        "raw_prediction": raw,
        "constrained_prediction": constrained,
    }
