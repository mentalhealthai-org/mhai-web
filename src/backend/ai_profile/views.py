"""User Profile views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ai_profile.models import AIProfile

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@method_decorator(login_required, name="dispatch")
class AIProfileView(TemplateView):
    template_name = "generic.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Render the user profile page with the user's profile ID in context.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.

        Returns
        -------
        HttpResponse
            The HTTP response with the rendered template.
        """
        context = super().get_context_data()

        profile = get_object_or_404(AIProfile, user=request.user)

        context["context"] = {
            "ai_profile_id": profile.id,
            "user_id": request.user.id,
        }
        return render(request, "generic.html", context)
