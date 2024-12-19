from django.contrib import admin

from .models import DashApp, StatelessApp


@admin.register(StatelessApp)
class StatelessAppAdmin(admin.ModelAdmin):
    list_display = ("app_name", "slug")


@admin.register(DashApp)
class DashAppAdmin(admin.ModelAdmin):
    list_display = (
        "instance_name",
        "slug",
        "stateless_app",
        "creation",
        "update",
    )
    actions = ["populate_app_state"]

    @admin.action(description="Populate app state with layout defaults")
    def populate_app_state(self, request, queryset):
        for app_instance in queryset:
            app_instance.populate_values()
