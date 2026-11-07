from apps.batting.models import BattingNextMatchFeatures
from apps.bowling.models import BowlingNextMatchFeatures
from apps.players.models import BattingPlayerMatchRegular

from .model_loader import load_dl_bundle, load_ml_model
from .dl_inference import predict_dl
from .ml_inference import predict_ml


class PlayerNotFoundError(LookupError):
    pass


def predict_player(category, player):
    if category not in {"batting", "bowling"}:
        raise ValueError("Category must be batting or bowling.")

    if not isinstance(player, str) or not player.strip():
        raise ValueError("A valid player name is required.")

    player = player.strip()

    if category == "batting":
        record = (
            BattingNextMatchFeatures.objects
            .filter(player=player)
            .order_by("-date", "-match_id")
            .first()
        )

        if record is None:
            raise PlayerNotFoundError(
                f"No batting feature record found for {player}."
            )

        regular = BattingPlayerMatchRegular.objects.filter(
            match_id=record.match_id,
            player=player,
        ).first()

        if regular is None:
            raise PlayerNotFoundError(
                f"Batting statistics not found for {player} "
                f"in match {record.match_id}."
            )

        dl_features = list(
            load_dl_bundle(
                "target_next_match_runs_scored"
            )["preprocessor"].feature_names_in_
        )

        ml_features = list(
            load_ml_model("batting").feature_names_in_
        )

        features = {
            name: getattr(record, name)
            for name in dl_features
        }

        features["batting_average"] = regular.batting_average

        missing = [
            name for name in ml_features
            if name not in features
        ]

        if missing:
            raise ValueError(
                f"Missing batting ML features: {missing}"
            )

    else:
        record = (
            BowlingNextMatchFeatures.objects
            .filter(player=player)
            .order_by("-date", "-match_id")
            .first()
        )

        if record is None:
            raise PlayerNotFoundError(
                f"No bowling feature record found for {player}."
            )

        features = {
            name: getattr(record, name)
            for name in set(
                list(
                    load_dl_bundle(
                        "target_next_match_wickets"
                    )["preprocessor"].feature_names_in_
                )
                + list(
                    load_ml_model("bowling").feature_names_in_
                )
            )
        }

    dl_result = predict_dl(category, features)
    ml_result = predict_ml(category, features)

    return {
        "player": player,
        "category": category,
        "source_match_id": record.match_id,
        "source_date": record.date,
        "ml_predictions": ml_result["predictions"],
        "dl_predictions": dl_result["predictions"],
    }
