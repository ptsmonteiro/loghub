from django import template

register = template.Library()


@register.filter
def attr(obj, name):
    """Attribute or item lookup helper.

    Tries attribute access first, then falls back to item lookup
    (useful for Django forms where dynamic fields are accessed as form['name']).
    """
    try:
        v = getattr(obj, name)
        if v is not None and v != "":
            return v
    except Exception:
        pass
    try:
        return obj[name]
    except Exception:
        return ""


@register.filter(name="value_for")
def value_for(obj, field):
    if field == "operator_display":
        # Prefer station_callsign; fall back to operator
        op = getattr(obj, "station_callsign", None) or getattr(obj, "operator", None)
        return op or ""
    if hasattr(obj, field):
        return getattr(obj, field)
    extras = getattr(obj, "extras", None) or {}
    if isinstance(extras, dict):
        # Field could be provided as uppercase ADIF tag
        return extras.get(str(field).upper(), "")
    return ""


@register.filter(name="dict_get")
def dict_get(d, key):
    try:
        return (d or {}).get(key)
    except Exception:
        return ""
