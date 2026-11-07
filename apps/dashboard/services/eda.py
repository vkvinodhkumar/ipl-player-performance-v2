
from django.db.models import Count, Sum

from apps.matches.models import Matches
from apps.players.models import (
    BattingPlayerMatchRegular,
    BowlingPlayerMatchRegular,
)


def get_eda_data():
    # 1. Season analysis
    season_matches = list(
        Matches.objects.values("season")
        .annotate(matches=Count("match_id"))
        .order_by("season")
    )

    batting_seasons = list(
        BattingPlayerMatchRegular.objects
        .filter(is_super_over=False)
        .values("season")
        .annotate(
            total_runs=Sum("runs_scored"),
            total_fours=Sum("fours"),
            total_sixes=Sum("sixes"),
        )
        .order_by("season")
    )

    bowling_seasons = list(
        BowlingPlayerMatchRegular.objects
        .filter(is_super_over=False)
        .values("season")
        .annotate(
            total_wickets=Sum("wickets"),
            runs_conceded=Sum("runs_conceded"),
        )
        .order_by("season")
    )

    # 2. Venue analysis
    venue_stats = list(
        Matches.objects.exclude(venue__isnull=True)
        .exclude(venue="")
        .values("venue")
        .annotate(
            matches=Count("match_id"),
        )
        .order_by("-matches")[:10]
    )

    # 3. Team wins
    team_wins = list(
        Matches.objects.exclude(winner__isnull=True)
        .exclude(winner="")
        .values("winner")
        .annotate(wins=Count("match_id"))
        .order_by("-wins")[:10]
    )

    # 4. Batting leaderboard
    batting_rows = (
        BattingPlayerMatchRegular.objects
        .filter(is_super_over=False)
        .values("player")
        .annotate(
            matches=Count("match_id", distinct=True),
            runs=Sum("runs_scored"),
            balls=Sum("balls_faced"),
            fours=Sum("fours"),
            sixes=Sum("sixes"),
            dismissals=Sum("dismissals"),
        )
        .order_by("-runs")[:10]
    )

    top_batsmen = []
    for row in batting_rows:
        runs = row["runs"] or 0
        balls = row["balls"] or 0
        dismissals = row["dismissals"] or 0

        top_batsmen.append({
            **row,
            "strike_rate": round(runs * 100 / balls, 2) if balls else 0,
            "average": round(runs / dismissals, 2) if dismissals else None,
        })

    # 5. Bowling leaderboard
    bowling_rows = (
        BowlingPlayerMatchRegular.objects
        .filter(is_super_over=False)
        .values("player")
        .annotate(
            matches=Count("match_id", distinct=True),
            wickets=Sum("wickets"),
            runs_conceded=Sum("runs_conceded"),
            legal_balls=Sum("legal_balls"),
        )
        .order_by("-wickets", "runs_conceded")[:10]
    )

    top_bowlers = []
    for row in bowling_rows:
        runs = row["runs_conceded"] or 0
        balls = row["legal_balls"] or 0

        top_bowlers.append({
            **row,
            "economy": round(runs * 6 / balls, 2) if balls else 0,
        })

    return {
        "season_matches": season_matches,
        "batting_seasons": batting_seasons,
        "bowling_seasons": bowling_seasons,
        "venue_stats": venue_stats,
        "team_wins": team_wins,
        "top_batsmen": top_batsmen,
        "top_bowlers": top_bowlers,
    }
