
from django.db.models import Count, Sum

from apps.players.models import BowlingPlayerMatchRegular


def get_bowling_analytics(selected_season=None, selected_match_type=None):

    queryset = BowlingPlayerMatchRegular.objects.filter(
        is_super_over=False
    )

    if selected_season:
        queryset = queryset.filter(season=selected_season)

    if selected_match_type:
        queryset = queryset.filter(match_type=selected_match_type)

    # KPI calculations
    totals = queryset.aggregate(
        matches=Count("match_id", distinct=True),
        players=Count("player", distinct=True),
        wickets=Sum("wickets"),
        runs_conceded=Sum("runs_conceded"),
        legal_balls=Sum("legal_balls"),
    )

    wickets = totals["wickets"] or 0
    runs = totals["runs_conceded"] or 0
    balls = totals["legal_balls"] or 0

    economy = round(runs * 6 / balls, 2) if balls else None
    bowling_average = round(runs / wickets, 2) if wickets else None
    bowling_strike_rate = round(balls / wickets, 2) if wickets else None

    # Top 10 wicket takers
    leaderboard = queryset.values("player").annotate(
        matches=Count("match_id", distinct=True),
        wickets=Sum("wickets"),
        runs_conceded=Sum("runs_conceded"),
        legal_balls=Sum("legal_balls"),
    ).order_by("-wickets", "runs_conceded", "player")[:10]

    top_bowlers = []

    for row in leaderboard:
        player_wickets = row["wickets"] or 0
        player_runs = row["runs_conceded"] or 0
        player_balls = row["legal_balls"] or 0

        top_bowlers.append({
            **row,
            "wickets": player_wickets,
            "economy": (
                round(player_runs * 6 / player_balls, 2)
                if player_balls else None
            ),
            "average": (
                round(player_runs / player_wickets, 2)
                if player_wickets else None
            ),
            "strike_rate": (
                round(player_balls / player_wickets, 2)
                if player_wickets else None
            ),
        })

    # Season-wise bowling performance
    season_stats = list(
        queryset.values("season").annotate(
            wickets=Sum("wickets"),
            runs_conceded=Sum("runs_conceded"),
            legal_balls=Sum("legal_balls"),
        ).order_by("season")
    )

    seasons = list(
        BowlingPlayerMatchRegular.objects.filter(
            is_super_over=False
        ).values_list("season", flat=True).distinct().order_by("season")
    )

    match_types = list(
        BowlingPlayerMatchRegular.objects.filter(
            is_super_over=False
        ).values_list("match_type", flat=True).distinct().order_by("match_type")
    )

    chart_data = {
        "players": [row["player"] for row in top_bowlers],
        "wickets": [row["wickets"] for row in top_bowlers],
        "seasons": [row["season"] for row in season_stats],
        "season_wickets": [row["wickets"] or 0 for row in season_stats],
        "season_economy": [
            round((row["runs_conceded"] or 0) * 6 / row["legal_balls"], 2)
            if row["legal_balls"] else None
            for row in season_stats
        ],
    }

    return {
        "totals": totals,
        "economy": economy,
        "bowling_average": bowling_average,
        "bowling_strike_rate": bowling_strike_rate,
        "top_bowlers": top_bowlers,
        "season_stats": season_stats,
        "seasons": seasons,
        "match_types": match_types,
        "selected_season": selected_season or "",
        "selected_match_type": selected_match_type or "",
        "chart_data": chart_data,
    }
