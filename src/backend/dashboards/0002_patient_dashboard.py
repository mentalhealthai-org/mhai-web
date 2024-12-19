# from django.db import migrations


# def add_dash_apps(apps, schema_editor):
#     StatelessApp = apps.get_model("django_plotly_dash", "StatelessApp")
#     DashApp = apps.get_model("django_plotly_dash", "DashApp")

#     # Add StatelessApp for your Dash application
#     stateless_app, _ = StatelessApp.objects.get_or_create(
#         app_name="DashboardPatientView", slug="dashboard-patient-view"
#     )

#     # Add DashApp with instance state
#     dash_app, _ = DashApp.get_or_create(
#         stateless_app=stateless_app,
#     )
#     dash_app.instance_name = "Dashboard Patient View Instance"
#     dash_app.slug = "dashboard-patient-view-instance"
#     dash_app.base_state = "{}"
#     dash_app.save_on_change = True
#     dash_app.save()


# def remove_dash_apps(apps, schema_editor):
#     DashApp = apps.get_model("django_plotly_dash", "DashApp")
#     StatelessApp = apps.get_model("django_plotly_dash", "StatelessApp")

#     DashApp.objects.filter(slug="dashboard-patient-view-instance").delete()
#     StatelessApp.objects.filter(slug="dashboard-patient-view").delete()


# class Migration(migrations.Migration):
#     dependencies = [
#         ("dashboards", "0001_initial"),
#     ]

#     operations = [
#         migrations.RunPython(add_dash_apps, remove_dash_apps),
#     ]
