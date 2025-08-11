from django.contrib import admin

from .models import QSO


@admin.register(QSO)
class QSOAdmin(admin.ModelAdmin):
    list_display = ("callsign", "qso_date", "time_on", "band", "mode", "prop_mode", "sat_name", "my_sota_ref")
    list_filter = ("band", "mode", "prop_mode", "qso_date", "my_sota_ref")
    search_fields = (
        "callsign",
        "station_callsign",
        "operator",
        "country",
        "gridsquare",
        "my_gridsquare",
        "sota_ref",
        "my_sota_ref",
        "comment",
    )
