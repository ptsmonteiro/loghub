from django.contrib import admin

from .models import QSO, QSOExtras, LogImport


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
        "notes",
    )


class QSOExtrasInline(admin.StackedInline):
    model = QSOExtras
    extra = 0
    can_delete = True
    fields = ("data",)


QSOAdmin.inlines = [QSOExtrasInline]


@admin.register(LogImport)
class LogImportAdmin(admin.ModelAdmin):
    list_display = ("id", "kind", "format", "provider", "original_filename", "station_callsign", "created_at", "qso_count")
    list_filter = ("kind", "format", "provider")
    search_fields = ("original_filename", "provider", "station_callsign", "sha256")
    readonly_fields = ("created_at", "imported_at")

    def qso_count(self, obj):  # pragma: no cover - trivial
        return obj.qsos.count()
