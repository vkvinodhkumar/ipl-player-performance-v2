from apps.matches.models import Matches, Deliveries
from apps.players.models import (
    BattingPlayerMatchRegular,
    BowlingPlayerMatchRegular,
)
from apps.players.identity import canonical_player_name


def get_dashboard_kpis():

    batting_players = set(
        canonical_player_name(name)
        for name in BattingPlayerMatchRegular.objects
        .values_list("player", flat=True)
        .distinct()
    )

    bowling_players = set(
        canonical_player_name(name)
        for name in BowlingPlayerMatchRegular.objects
        .values_list("player", flat=True)
        .distinct()
    )

    return {
        "total_matches": Matches.objects.count(),
        "total_players": len(batting_players | bowling_players),
        "total_deliveries": Deliveries.objects.count(),
        "batting_records": BattingPlayerMatchRegular.objects.count(),
        "bowling_records": BowlingPlayerMatchRegular.objects.count(),
    }
