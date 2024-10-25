from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="generic.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="generic.html"),
        name="about",
    ),
]
