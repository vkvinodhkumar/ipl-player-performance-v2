
from django.urls import path
from apps.matches import views

app_name = "matches"

urlpatterns = [
    path("", views.match_explorer, name="match_explorer"),
    path("<str:match_id>/", views.match_detail, name="match_detail"),
]
