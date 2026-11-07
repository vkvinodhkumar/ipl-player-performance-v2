from django.db.models import Count, Sum

from apps.batting.models import BattingNextMatchFeatures
from apps.bowling.models import BowlingNextMatchFeatures
from apps.players.identity import source_player_names


def safe_divide(numerator, denominator, multiplier=1):
    if not denominator:
        return None
    return round(numerator / denominator * multiplier, 2)


def get_player_profile(player_name):
    if not isinstance(player_name, str) or not player_name.strip():
        raise ValueError("A valid player name is required.")

    player_name = player_name.strip()
    source_names = source_player_names(player_name)

    batting_qs = BattingNextMatchFeatures.objects.filter(
        player__in=source_names
    )
    bowling_qs = BowlingNextMatchFeatures.objects.filter(
        player__in=source_names
    )

    batting = batting_qs.aggregate(
        matches=Count("match_id", distinct=True),
        runs=Sum("runs_scored", default=0),
        balls=Sum("balls_faced", default=0),
        fours=Sum("fours", default=0),
        sixes=Sum("sixes", default=0),
        dismissals=Sum("dismissals", default=0),
        innings=Sum("innings_batted", default=0),
        not_outs=Sum("not_out_innings", default=0),
    )

    bowling = bowling_qs.aggregate(
        matches=Count("match_id", distinct=True),
        runs_conceded=Sum("runs_conceded", default=0),
        legal_balls=Sum("legal_balls", default=0),
        wickets=Sum("wickets", default=0),
    )

    batting["batting_average"] = safe_divide(
        batting["runs"], batting["innings"] - batting["not_outs"]
    )
    batting["strike_rate"] = safe_divide(
        batting["runs"], batting["balls"], 100
    )

    bowling["economy_rate"] = safe_divide(
        bowling["runs_conceded"], bowling["legal_balls"] / 6
    )
    bowling["bowling_average"] = safe_divide(
        bowling["runs_conceded"], bowling["wickets"]
    )
    bowling["bowling_strike_rate"] = safe_divide(
        bowling["legal_balls"], bowling["wickets"]
    )

    batting_by_season = list(
        batting_qs.values("season").annotate(
            matches=Count("match_id", distinct=True),
            runs=Sum("runs_scored", default=0),
            balls=Sum("balls_faced", default=0),
            fours=Sum("fours", default=0),
            sixes=Sum("sixes", default=0),
            dismissals=Sum("dismissals", default=0),
            innings=Sum("innings_batted", default=0),
            not_outs=Sum("not_out_innings", default=0),
        ).order_by("season")
    )

    for row in batting_by_season:
        row["batting_average"] = safe_divide(
            row["runs"], row["innings"] - row["not_outs"]
        )
        row["strike_rate"] = safe_divide(
            row["runs"], row["balls"], 100
        )

    bowling_by_season = list(
        bowling_qs.values("season").annotate(
            matches=Count("match_id", distinct=True),
            runs_conceded=Sum("runs_conceded", default=0),
            legal_balls=Sum("legal_balls", default=0),
            wickets=Sum("wickets", default=0),
        ).order_by("season")
    )

    for row in bowling_by_season:
        row["economy_rate"] = safe_divide(
            row["runs_conceded"], row["legal_balls"] / 6
        )
        row["bowling_average"] = safe_divide(
            row["runs_conceded"], row["wickets"]
        )
        row["bowling_strike_rate"] = safe_divide(
            row["legal_balls"], row["wickets"]
        )

    latest_batting = batting_qs.order_by("-date", "-match_id").first()
    latest_bowling = bowling_qs.order_by("-date", "-match_id").first()

    latest = max(
        (r for r in (latest_batting, latest_bowling) if r),
        key=lambda r: (r.date, r.match_id),
        default=None,
    )

    return {
        "player": player_name,
        "source_names": source_names,
        "batting": batting,
        "bowling": bowling,
        "batting_by_season": batting_by_season,
        "bowling_by_season": bowling_by_season,
        "latest_match": {
            "match_id": latest.match_id,
            "date": latest.date,
            "season": latest.season,
        } if latest else None,
        "has_batting": batting["matches"] > 0,
        "has_bowling": bowling["matches"] > 0,
    }
