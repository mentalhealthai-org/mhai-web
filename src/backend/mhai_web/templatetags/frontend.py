import json

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def frontend_static(asset: str):
    manifest_path = (
        settings.BASE_DIR.parent / "frontend" / "build" / "asset-manifest.json"
    )
    with manifest_path.open("r") as manifest_file:
        manifest = json.load(manifest_file)
    return manifest["files"].get(asset, asset)
