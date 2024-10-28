from django import template

register = template.Library()


@register.filter
def dicebear_url(email: str, size: int = 32) -> str:
    """
    Returns the dicebear URL for a given email.

    Parameters
    ----------
    email : str
        The user's email address.
    size : int, optional
        The size of the avatar (default is 32).

    Returns
    -------
    str
        The URL for the avatar image.
    """
    return f"https://api.dicebear.com/6.x/initials/svg?seed={email[0].upper()}&size={size}"
