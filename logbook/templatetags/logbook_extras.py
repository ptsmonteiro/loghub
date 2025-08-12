from django import template

register = template.Library()


@register.filter
def attr(obj, name):
    return getattr(obj, name, "")


@register.filter(name="value_for")
def value_for(obj, field):
    if field == "operator_display":
        op = getattr(obj, "operator", None) or getattr(obj, "station_callsign", None)
        return op or ""
    if hasattr(obj, field):
        return getattr(obj, field)
    extras = getattr(obj, "extras", None) or {}
    if isinstance(extras, dict):
        # Field could be provided as uppercase ADIF tag
        return extras.get(str(field).upper(), "")
    return ""
