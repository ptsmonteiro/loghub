from django import template
from datetime import date as _date, time as _time, datetime as _datetime, timezone as _dt_timezone
from django.utils import timezone

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


@register.filter(name="zulu")
def zulu(value):
    """Format dates/times in a Zulu (UTC) oriented way.

    - datetime -> YYYY-MM-DD HH:MMZ (converted to UTC)
    - time     -> HH:MMZ (include :SS if seconds present)
    - date     -> YYYY-MM-DD
    - str      -> best-effort ADIF-style parsing (YYYYMMDD, HHMMSS, HHMM)
    - other    -> returned unchanged
    """
    # Handle datetimes (aware or naive)
    if isinstance(value, _datetime):
        dt = value
        if timezone.is_aware(dt):
            # Convert aware datetimes to UTC
            dt = dt.astimezone(_dt_timezone.utc)
        else:
            # Treat naive as UTC by convention for this app
            dt = dt.replace(tzinfo=_dt_timezone.utc)
        fmt = "%Y-%m-%d %H:%M"
        if dt.second or dt.microsecond:
            fmt = "%Y-%m-%d %H:%M:%S"
        return dt.strftime(fmt) + "Z"

    # Handle times
    if isinstance(value, _time):
        if value.second or value.microsecond:
            return value.strftime("%H:%M:%S") + "Z"
        return value.strftime("%H:%M") + "Z"

    # Handle dates
    if isinstance(value, _date):
        return value.strftime("%Y-%m-%d")

    # Strings that look like ADIF values (best effort)
    if isinstance(value, str):
        s = value.strip()
        # Date: YYYYMMDD
        if len(s) == 8 and s.isdigit():
            y, m, d = s[:4], s[4:6], s[6:8]
            return f"{y}-{m}-{d}"
        # Time: HHMMSS
        if len(s) == 6 and s.isdigit():
            return f"{s[:2]}:{s[2:4]}:{s[4:6]}Z"
        # Time: HHMM
        if len(s) == 4 and s.isdigit():
            return f"{s[:2]}:{s[2:4]}Z"
        # ISO-ish: pass through, optionally append Z if endswith 'Z' already
        return s

    return value
