
from django.shortcuts import render
from django.db.models import Count

from apps.dashboard.services.kpi import get_dashboard_kpis
from apps.matches.models import Matches


def dashboard_home(request):
    kpis = get_dashboard_kpis()

    season_stats = list(
        Matches.objects.values("season")
        .annotate(matches=Count("match_id"))
        .order_by("season")
    )

    return render(
        request,
        "dashboard/home.html",
        {
            "kpis": kpis,
            "season_stats": season_stats,
        },
    )


from apps.dashboard.services.model_comparison import get_model_comparison


def model_comparison(request):
    context = get_model_comparison()
    return render(request, "dashboard/model_comparison.html", context)


from apps.dashboard.services.eda import get_eda_data


def eda_insights(request):
    context = get_eda_data()
    return render(request, "dashboard/eda.html", context)


from django.shortcuts import render
from django.db.models import Count

from apps.dashboard.services.kpi import get_dashboard_kpis
from apps.dashboard.services.model_comparison import get_model_comparison
from apps.dashboard.services.eda import get_eda_data
from apps.dashboard.services.batting_analytics import get_batting_analytics

from apps.matches.models import Matches


def dashboard_home(request):
    kpis = get_dashboard_kpis()

    season_stats = list(
        Matches.objects.values("season")
        .annotate(matches=Count("match_id"))
        .order_by("season")
    )

    return render(
        request,
        "dashboard/home.html",
        {
            "kpis": kpis,
            "season_stats": season_stats,
        },
    )


def model_comparison(request):
    context = get_model_comparison()
    return render(request, "dashboard/model_comparison.html", context)


def eda_insights(request):
    context = get_eda_data()
    return render(request, "dashboard/eda.html", context)


def batting_analytics(request):
    selected_season = request.GET.get("season", "").strip()
    selected_match_type = request.GET.get("match_type", "").strip()

    context = get_batting_analytics(
        selected_season=selected_season or None,
        selected_match_type=selected_match_type or None,
    )

    return render(
        request,
        "dashboard/batting_analytics.html",
        context,
    )



from django.shortcuts import render
from django.db.models import Count

from apps.dashboard.services.kpi import get_dashboard_kpis
from apps.dashboard.services.model_comparison import get_model_comparison
from apps.dashboard.services.eda import get_eda_data
from apps.dashboard.services.batting_analytics import get_batting_analytics
from apps.dashboard.services.bowling_analytics import get_bowling_analytics

from apps.matches.models import Matches


def dashboard_home(request):
    kpis = get_dashboard_kpis()

    season_stats = list(
        Matches.objects.values("season")
        .annotate(matches=Count("match_id"))
        .order_by("season")
    )

    return render(
        request,
        "dashboard/home.html",
        {
            "kpis": kpis,
            "season_stats": season_stats,
        },
    )


def model_comparison(request):
    context = get_model_comparison()
    return render(request, "dashboard/model_comparison.html", context)


def eda_insights(request):
    context = get_eda_data()
    return render(request, "dashboard/eda.html", context)


def batting_analytics(request):
    selected_season = request.GET.get("season", "").strip()
    selected_match_type = request.GET.get("match_type", "").strip()

    context = get_batting_analytics(
        selected_season=selected_season or None,
        selected_match_type=selected_match_type or None,
    )

    return render(
        request,
        "dashboard/batting_analytics.html",
        context,
    )


def bowling_analytics(request):
    selected_season = request.GET.get("season", "").strip()
    selected_match_type = request.GET.get("match_type", "").strip()

    context = get_bowling_analytics(
        selected_season=selected_season or None,
        selected_match_type=selected_match_type or None,
    )

    return render(
        request,
        "dashboard/bowling_analytics.html",
        context,
    )
