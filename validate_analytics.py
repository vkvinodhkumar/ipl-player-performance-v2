from apps.players.models import (
    BattingPlayerMatchRegular,
    BowlingPlayerMatchRegular,
)
from apps.dashboard.services.batting_analytics import get_batting_analytics
from apps.dashboard.services.bowling_analytics import get_bowling_analytics

tests = [
    ("BATTING", BattingPlayerMatchRegular, get_batting_analytics),
    ("BOWLING", BowlingPlayerMatchRegular, get_bowling_analytics),
]

for name, model, service in tests:
    print(f"\n========== {name} ==========")

    base = service()

    seasons = list(
        model.objects.filter(is_super_over=False)
        .values_list("season", flat=True)
        .distinct()
        .order_by("season")
    )

    match_types = list(
        model.objects.filter(is_super_over=False)
        .values_list("match_type", flat=True)
        .distinct()
        .order_by("match_type")
    )

    print("Base matches:", base["totals"]["matches"])
    print("Available seasons:", seasons)
    print("Available match types:", match_types)

    for season in seasons:
        result = service(selected_season=season)
        print(
            f"Season {season}: "
            f"{result['totals']['matches']} matches"
        )

    for match_type in match_types:
        result = service(selected_match_type=match_type)
        print(
            f"Match type {match_type}: "
            f"{result['totals']['matches']} matches"
        )

print("\nANALYTICS FILTER VALIDATION COMPLETED")
