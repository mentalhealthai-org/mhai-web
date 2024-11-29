from django.urls import path

from dashboards.health_charts import patient

from . import views

app_name = "dashboards"

urlpatterns = [
    path("", views.dashboard, name="dashboards"),
]
