
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from apps.matches.models import Matches, Innings
from apps.players.models import (
    BattingPlayerMatchRegular,
    BowlingPlayerMatchRegular,
)


def match_explorer(request):
    matches = Matches.objects.all().order_by("-date", "-match_id")

    season = request.GET.get("season", "").strip()
    team = request.GET.get("team", "").strip()
    venue = request.GET.get("venue", "").strip()

    if season:
        matches = matches.filter(season=season)

    if team:
        matches = matches.filter(
            Q(team1__icontains=team)
            | Q(team2__icontains=team)
        )

    if venue:
        matches = matches.filter(venue__icontains=venue)

    seasons = (
        Matches.objects.values_list("season", flat=True)
        .distinct()
        .order_by("-season")
    )

    paginator = Paginator(matches, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "matches/match_explorer.html", {
        "page_obj": page_obj,
        "seasons": seasons,
        "selected_season": season,
        "selected_team": team,
        "selected_venue": venue,
        "total_matches": paginator.count,
    })


def match_detail(request, match_id):
    match = get_object_or_404(Matches, match_id=match_id)

    innings = Innings.objects.filter(
        match_id=match_id
    ).order_by("innings_number")

    batting_scorecard = (
        BattingPlayerMatchRegular.objects
        .filter(match_id=match_id, is_super_over=False)
        .order_by("-runs_scored")
    )

    bowling_scorecard = (
        BowlingPlayerMatchRegular.objects
        .filter(match_id=match_id, is_super_over=False)
        .order_by("-wickets", "economy_rate")
    )

    return render(request, "matches/match_detail.html", {
        "match": match,
        "innings": innings,
        "batting_scorecard": batting_scorecard,
        "bowling_scorecard": bowling_scorecard,
    })
