from django.urls import path

from .views import index

urlpatterns = [
    path("", index, name="home"),  # Serve the React app
]
