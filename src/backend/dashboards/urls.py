from django.urls import path

from dashboards.dash_apps.finished_apps import simpleexample

from . import views

app_name = "dashboards"

urlpatterns = [
    path("", views.dashboard, name="dashboards"),
]
