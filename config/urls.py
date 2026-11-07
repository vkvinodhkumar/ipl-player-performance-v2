
from django.contrib import admin
from django.urls import include, path

from apps.dashboard.views import (
    dashboard_home,
    model_comparison,
    eda_insights,
    batting_analytics,
    bowling_analytics,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard_home, name="dashboard_home"),
    path("players/", include("apps.players.urls")),
    path("predictions/", include("apps.inference.urls")),
    path("model-comparison/", model_comparison, name="model_comparison"),
    path("eda/", eda_insights, name="eda_insights"),
    path("matches/", include("apps.matches.urls")),
    path("batting-analytics/", batting_analytics, name="batting_analytics"),
    path("bowling-analytics/", bowling_analytics, name="bowling_analytics"),
]
