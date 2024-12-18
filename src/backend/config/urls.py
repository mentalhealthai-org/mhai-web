# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from mhai_web.urls import urlpatterns as mhai_urls
from mhai_chat.urls import urlpatterns as mhai_chat_urls


from ai_profile.urls import (
    api_urlpatterns as ai_profile_api_urls,
    views_urlpatterns as ai_profile_views_urls,
)
from user_profile.urls import (
    api_urlpatterns as user_profile_api_urls,
    views_urlpatterns as user_profile_views_urls,
)

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("mhai_web.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Application paths
    *mhai_urls,
    *mhai_chat_urls,
    *user_profile_views_urls,
    *ai_profile_views_urls,
    # Static files serving
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# Serve static and media files in development
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

# API URLs
urlpatterns += [
    # Base API path
    path("api/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    # Application API endpoints
    path("api/ai-profile/", include(ai_profile_api_urls)),
    path("api/profile/", include(user_profile_api_urls)),
    # mhai_chat URLs under `api/chat/`
    path("api/mhai-chat/", include("mhai_chat.api.urls")),
]

if settings.DEBUG:
    # Debug error pages
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls))
        ] + urlpatterns
