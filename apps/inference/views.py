
from django.shortcuts import render

from apps.batting.models import BattingNextMatchFeatures
from apps.bowling.models import BowlingNextMatchFeatures
from apps.players.identity import canonical_player_name
from apps.inference.services.player_inference import predict_player


def prediction_page(request, category):
    if category not in ("batting", "bowling"):
        raise ValueError("Unsupported prediction category.")

    model = (
        BattingNextMatchFeatures
        if category == "batting"
        else BowlingNextMatchFeatures
    )

    raw_names = model.objects.values_list(
        "player", flat=True
    ).distinct()

    players = sorted(
        {canonical_player_name(name) for name in raw_names},
        key=str.casefold,
    )

    selected_player = request.GET.get("player", "").strip()
    result = None
    error = None

    if selected_player:
        selected_player = canonical_player_name(selected_player)

        if selected_player not in players:
            error = "Player not found. Select a player from the suggestions."
        else:
            try:
                result = predict_player(category, selected_player)
            except (ValueError, TypeError) as exc:
                error = str(exc)

    return render(
        request,
        "inference/prediction.html",
        {
            "category": category,
            "players": players,
            "selected_player": selected_player,
            "result": result,
            "error": error,
        },
    )


def batting_prediction(request):
    return prediction_page(request, "batting")


def bowling_prediction(request):
    return prediction_page(request, "bowling")
