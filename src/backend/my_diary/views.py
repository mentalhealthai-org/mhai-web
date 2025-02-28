"""Mhai Chat views."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse


@method_decorator(login_required, name="dispatch")
class MhaiDiaryView(TemplateView):
    template_name = "generic.html"

    def get(self, request: HttpRequest) -> HttpResponse:
        """
        Render the mhai chat page.

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

        context["context"] = {
            "user_id": request.user.id,
        }
        return render(request, "generic.html", context)
