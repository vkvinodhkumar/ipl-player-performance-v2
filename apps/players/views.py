
from django.http import Http404
from django.shortcuts import render

from apps.batting.models import BattingNextMatchFeatures
from apps.bowling.models import BowlingNextMatchFeatures

from .identity import canonical_player_name
from .services.profile import get_player_profile


def player_search(request):
    query = request.GET.get("q", "").strip()
    players = []
    total_players = 0

    if query:
        batting_names = BattingNextMatchFeatures.objects.filter(
            player__icontains=query
        ).values_list("player", flat=True).distinct()

        bowling_names = BowlingNextMatchFeatures.objects.filter(
            player__icontains=query
        ).values_list("player", flat=True).distinct()

        canonical_names = {
            canonical_player_name(name)
            for name in list(batting_names) + list(bowling_names)
        }

        players = sorted(canonical_names, key=str.casefold)
        total_players = len(players)
        players = players[:50]

    return render(
        request,
        "players/player_search.html",
        {
            "query": query,
            "players": players,
            "total_players": total_players,
            "displayed_players": len(players),
        },
    )


def player_profile(request, player_name):
    player_name = canonical_player_name(player_name)

    try:
        profile = get_player_profile(player_name)
    except (ValueError, TypeError):
        raise Http404("Player not found.")

    if not profile["has_batting"] and not profile["has_bowling"]:
        raise Http404("Player not found.")

    batting = profile["batting"]
    bowling = profile["bowling"]

    batting_cards = [
        ("Matches", batting["matches"]),
        ("Runs", batting["runs"]),
        ("Balls Faced", batting["balls"]),
        ("Fours", batting["fours"]),
        ("Sixes", batting["sixes"]),
        ("Average", batting["batting_average"]),
        ("Strike Rate", batting["strike_rate"]),
    ]

    bowling_cards = [
        ("Matches", bowling["matches"]),
        ("Runs Conceded", bowling["runs_conceded"]),
        ("Legal Balls", bowling["legal_balls"]),
        ("Wickets", bowling["wickets"]),
        ("Economy", bowling["economy_rate"]),
        ("Average", bowling["bowling_average"]),
        ("Strike Rate", bowling["bowling_strike_rate"]),
    ]

    batting_chart_data = {
        "seasons": [row["season"] for row in profile["batting_by_season"]],
        "runs": [row["runs"] for row in profile["batting_by_season"]],
        "average": [
            row["batting_average"]
            for row in profile["batting_by_season"]
        ],
        "strike_rate": [
            row["strike_rate"]
            for row in profile["batting_by_season"]
        ],
    }

    bowling_chart_data = {
        "seasons": [row["season"] for row in profile["bowling_by_season"]],
        "wickets": [row["wickets"] for row in profile["bowling_by_season"]],
        "average": [
            row["bowling_average"]
            for row in profile["bowling_by_season"]
        ],
        "economy": [
            row["economy_rate"]
            for row in profile["bowling_by_season"]
        ],
    }

    return render(
        request,
        "players/player_profile.html",
        {
            "profile": profile,
            "batting_cards": batting_cards,
            "bowling_cards": bowling_cards,
            "batting_chart_json": batting_chart_data,
            "bowling_chart_json": bowling_chart_data,
        },
    )


def build_comparison_rows(
    metrics,
    stats1,
    stats2,
    player1_name,
    player2_name,
):
    """Build individual metric comparisons and determine the leader."""

    rows = []

    lower_is_better = {
        "economy_rate",
        "bowling_average",
        "bowling_strike_rate",
    }

    for label, key in metrics:
        value1 = stats1.get(key)
        value2 = stats2.get(key)

        if value1 is None and value2 is None:
            leader = "N/A"

        elif value1 is None:
            leader = player2_name

        elif value2 is None:
            leader = player1_name

        elif value1 == value2:
            leader = "Tie"

        elif key in lower_is_better:
            leader = (
                player1_name if value1 < value2 else player2_name
            )

        else:
            leader = (
                player1_name if value1 > value2 else player2_name
            )

        rows.append({
            "label": label,
            "player1_value": value1,
            "player2_value": value2,
            "leader": leader,
        })

    return rows


def player_comparison(request):

    # Get all available players.
    batting_names = BattingNextMatchFeatures.objects.values_list(
        "player", flat=True
    ).distinct()

    bowling_names = BowlingNextMatchFeatures.objects.values_list(
        "player", flat=True
    ).distinct()

    players = sorted(
        {
            canonical_player_name(name)
            for name in list(batting_names) + list(bowling_names)
        },
        key=str.casefold,
    )

    # Read selected players.
    player1_name = canonical_player_name(
        request.GET.get("player1", "").strip()
    )

    player2_name = canonical_player_name(
        request.GET.get("player2", "").strip()
    )

    player1 = None
    player2 = None
    error = None

    # Validate selection.
    if player1_name or player2_name:

        if not player1_name or not player2_name:
            error = "Please select both players."

        elif player1_name == player2_name:
            error = "Please select two different players."

        elif (
            player1_name not in players
            or player2_name not in players
        ):
            error = "One or both selected players are invalid."

        else:
            player1 = get_player_profile(player1_name)
            player2 = get_player_profile(player2_name)

    # Batting metrics.
    batting_metrics = [
        ("Matches", "matches"),
        ("Runs", "runs"),
        ("Balls Faced", "balls"),
        ("Batting Average", "batting_average"),
        ("Strike Rate", "strike_rate"),
        ("Fours", "fours"),
        ("Sixes", "sixes"),
    ]

    # Bowling metrics.
    bowling_metrics = [
        ("Matches", "matches"),
        ("Wickets", "wickets"),
        ("Runs Conceded", "runs_conceded"),
        ("Legal Balls", "legal_balls"),
        ("Economy Rate", "economy_rate"),
        ("Bowling Average", "bowling_average"),
        ("Bowling Strike Rate", "bowling_strike_rate"),
    ]


    batting_rows = []
    bowling_rows = []
    comparison_chart_data = {}
    comparison_summary = {}

    if player1 and player2:

        batting_rows = build_comparison_rows(
            batting_metrics,
            player1["batting"],
            player2["batting"],
            player1_name,
            player2_name,
        )

        bowling_rows = build_comparison_rows(
            bowling_metrics,
            player1["bowling"],
            player2["bowling"],
            player1_name,
            player2_name,
        )

        # Count metric leads.
        player1_wins = sum(
            row["leader"] == player1_name
            for row in batting_rows + bowling_rows
        )

        player2_wins = sum(
            row["leader"] == player2_name
            for row in batting_rows + bowling_rows
        )

        comparison_summary = {
            "player1_wins": player1_wins,
            "player2_wins": player2_wins,
            "ties": sum(
                row["leader"] == "Tie"
                for row in batting_rows + bowling_rows
            ),
        }

        # Chart data: primary batting and bowling metrics.
        comparison_chart_data = {
            "players": [player1_name, player2_name],
            "batting_runs": [
                player1["batting"]["runs"],
                player2["batting"]["runs"],
            ],
            "bowling_wickets": [
                player1["bowling"]["wickets"],
                player2["bowling"]["wickets"],
            ],
        }

    return render(
        request,
        "players/player_comparison.html",
        {
            "players": players,
            "player1_name": player1_name,
            "player2_name": player2_name,
            "player1": player1,
            "player2": player2,
            "error": error,
            "batting_rows": batting_rows,
            "bowling_rows": bowling_rows,
            "comparison_summary": comparison_summary,
            "comparison_chart_data": comparison_chart_data,
        },
    )
