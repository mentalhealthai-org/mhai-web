"""Models for the dashboard."""

from __future__ import annotations

import json

from django.db import models
from django.utils.text import slugify


class StatelessApp(models.Model):
    """
    A stateless Dash app.

    Represents a Dash application without any specific state.
    """

    app_name = models.CharField(
        max_length=100, unique=True, blank=False, null=False
    )
    slug = models.SlugField(max_length=110, unique=True, blank=True)

    def __str__(self):
        return self.app_name

    def save(self, *args, **kwargs):
        """Override save method to automatically populate the slug field."""
        if not self.slug:
            self.slug = slugify(self.app_name)
        super().save(*args, **kwargs)

    def as_dash_app(self):
        """
        Return a DjangoDash instance of the Dash application.
        """
        from django_plotly_dash import DjangoDash

        return DjangoDash(name=self.app_name)


class DashApp(models.Model):
    """
    Represents a Dash application and its internal state.
    """

    stateless_app = models.ForeignKey(
        StatelessApp, on_delete=models.PROTECT, related_name="dash_instances"
    )
    instance_name = models.CharField(
        max_length=100, unique=True, blank=True, null=False
    )
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    base_state = models.TextField(default="{}", null=False)
    creation = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    save_on_change = models.BooleanField(default=False, null=False)

    def __str__(self):
        return self.instance_name

    def save(self, *args, **kwargs):
        """Override save method to populate the slug field."""
        if not self.slug:
            self.slug = slugify(self.instance_name)
        super().save(*args, **kwargs)

    def current_state(self):
        """
        Return the current internal state of the model instance.
        """
        import json

        return json.loads(self.base_state)

    def update_current_state(self, wid, key, value):
        """
        Update the current internal state, ignoring non-tracked objects.
        """
        state = self.current_state()
        if wid not in state:
            state[wid] = {}
        state[wid][key] = value
        self.base_state = json.dumps(state)
        if self.save_on_change:
            self.save()

    def populate_values(self):
        """
        Add values from the underlying dash layout configuration to base_state.
        """
        # Example logic: Update base_state with default layout values.
        # You need to integrate this with your actual Dash app layout.
        layout_defaults = {"layout_key": "default_value"}  # Placeholder
        self.base_state = json.dumps(layout_defaults)
        self.save()
