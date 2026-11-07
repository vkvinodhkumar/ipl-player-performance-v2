from django.urls import path

from apps.inference import views

app_name = "inference"

urlpatterns = [
    path("batting/", views.batting_prediction, name="batting_prediction"),
    path("bowling/", views.bowling_prediction, name="bowling_prediction"),
]
