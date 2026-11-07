
from django.db.models import Count, Sum

from apps.players.models import BattingPlayerMatchRegular


def get_batting_analytics(selected_season=None, selected_match_type=None):

    queryset = BattingPlayerMatchRegular.objects.filter(
        is_super_over=False
    )

    # Apply filters.
    if selected_season:
        queryset = queryset.filter(season=selected_season)

    if selected_match_type:
        queryset = queryset.filter(match_type=selected_match_type)

    # KPI aggregation.
    totals = queryset.aggregate(
        matches=Count("match_id", distinct=True),
        players=Count("player", distinct=True),
        runs=Sum("runs_scored"),
        balls=Sum("balls_faced"),
        fours=Sum("fours"),
        sixes=Sum("sixes"),
        dismissals=Sum("dismissals"),
    )

    runs = totals["runs"] or 0
    balls = totals["balls"] or 0
    dismissals = totals["dismissals"] or 0

    batting_average = (
        round(runs / dismissals, 2) if dismissals else None
    )

    strike_rate = (
        round(runs * 100 / balls, 2) if balls else None
    )

    # Top 10 run scorers.
    leaderboard = queryset.values("player").annotate(
        matches=Count("match_id", distinct=True),
        runs=Sum("runs_scored"),
        balls=Sum("balls_faced"),
        fours=Sum("fours"),
        sixes=Sum("sixes"),
        dismissals=Sum("dismissals"),
    ).order_by("-runs", "player")[:10]

    top_batsmen = []

    for row in leaderboard:
        player_runs = row["runs"] or 0
        player_balls = row["balls"] or 0
        player_dismissals = row["dismissals"] or 0

        top_batsmen.append({
            **row,
            "runs": player_runs,
            "strike_rate": (
                round(player_runs * 100 / player_balls, 2)
                if player_balls else None
            ),
            "average": (
                round(player_runs / player_dismissals, 2)
                if player_dismissals else None
            ),
        })

    # Season-wise batting performance.
    season_stats = list(
        queryset.values("season").annotate(
            runs=Sum("runs_scored"),
            fours=Sum("fours"),
            sixes=Sum("sixes"),
        ).order_by("season")
    )

    # Filter options.
    seasons = list(
        BattingPlayerMatchRegular.objects.filter(
            is_super_over=False
        )
        .values_list("season", flat=True)
        .distinct()
        .order_by("season")
    )

    match_types = list(
        BattingPlayerMatchRegular.objects.filter(
            is_super_over=False
        )
        .values_list("match_type", flat=True)
        .distinct()
        .order_by("match_type")
    )

    chart_data = {
        "players": [row["player"] for row in top_batsmen],
        "runs": [row["runs"] for row in top_batsmen],
        "seasons": [row["season"] for row in season_stats],
        "season_runs": [row["runs"] or 0 for row in season_stats],
        "season_fours": [row["fours"] or 0 for row in season_stats],
        "season_sixes": [row["sixes"] or 0 for row in season_stats],
    }

    return {
        "totals": totals,
        "batting_average": batting_average,
        "strike_rate": strike_rate,
        "top_batsmen": top_batsmen,
        "season_stats": season_stats,
        "seasons": seasons,
        "match_types": match_types,
        "selected_season": selected_season or "",
        "selected_match_type": selected_match_type or "",
        "chart_data": chart_data,
    }
