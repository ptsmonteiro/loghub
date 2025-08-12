from django import template

register = template.Library()


@register.filter
def attr(obj, name):
    return getattr(obj, name, "")


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
