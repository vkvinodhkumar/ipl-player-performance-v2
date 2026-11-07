
from django.urls import path
from . import views

app_name = "players"

urlpatterns = [
    path("", views.player_search, name="player_search"),

    # Static route must come before the dynamic player route.
    path("compare/", views.player_comparison, name="player_comparison"),

    path("<str:player_name>/", views.player_profile, name="player_profile"),
]
