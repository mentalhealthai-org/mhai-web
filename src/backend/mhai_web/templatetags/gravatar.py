import hashlib

from django import template

register = template.Library()


@register.filter
def gravatar_url(
    email: str, size: int = 32, default: str = "identicon"
) -> str:
    """
    Generate Gravatar URL.

    Returns the Gravatar URL for a given email with a specified
    default image if no Gravatar is found.

    Parameters
    ----------
    email : str
        The user's email address.
    size : int, optional
        The size of the Gravatar image (default is 32).
    default : str, optional
        The default image type if no Gravatar is found.
        Options include 'identicon', 'monsterid',
        'wavatar', 'retro', and 'robohash' (default is 'identicon').

    Returns
    -------
    str
        The URL for the Gravatar image with the specified default.
    """
    email_hash = hashlib.md5(  # noqa: S324
        email.strip().lower().encode("utf-8"),
    ).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}"
