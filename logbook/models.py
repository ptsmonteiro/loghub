import re
from decimal import Decimal
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models


class LogEntry(models.Model):
    """Single log entry (a QSO) with ADIF-aligned fields and constraints."""

    # Core identity
    callsign = models.CharField(max_length=20, db_index=True, help_text="CALL: Station worked")
    qso_date = models.DateField(help_text="QSO_DATE: UTC date contact established")
    time_on = models.TimeField(help_text="TIME_ON: UTC time contact established")

    # Frequency / Band
    band = models.CharField(max_length=16, blank=True, help_text="BAND, e.g., 20m (derived from FREQ if absent)")
    freq = models.DecimalField(
        max_digits=11,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="FREQ in MHz (e.g., 14.074)",
    )
    band_rx = models.CharField(max_length=16, blank=True, help_text="BAND_RX (optional)")
    freq_rx = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True, help_text="FREQ_RX in MHz")

    # Mode
    mode = models.CharField(max_length=32, help_text="MODE, e.g., SSB, FT8")
    submode = models.CharField(max_length=32, blank=True, help_text="SUBMODE (optional)")

    # Propagation / Satellite
    prop_mode = models.CharField(max_length=16, blank=True, help_text="PROP_MODE; 'SAT' requires SAT_NAME")
    sat_name = models.CharField(max_length=32, blank=True, help_text="SAT_NAME if PROP_MODE is SAT")

    # Station/operator identity
    station_callsign = models.CharField(max_length=20, blank=True, help_text="STATION_CALLSIGN (optional)")
    operator = models.CharField(max_length=20, blank=True, help_text="OPERATOR (optional; treated as station callsign if STATION_CALLSIGN absent)")

    # RST and other info
    rst_sent = models.CharField(max_length=8, blank=True)
    rst_rcvd = models.CharField(max_length=8, blank=True)
    # Optional QSO end time/date
    qso_date_off = models.DateField(null=True, blank=True, help_text="QSO_DATE_OFF (optional)")
    time_off = models.TimeField(null=True, blank=True, help_text="TIME_OFF (optional)")

    # Exchange / contest related
    srx = models.PositiveIntegerField(null=True, blank=True, help_text="SRX (optional)")
    srx_string = models.CharField(max_length=32, blank=True, help_text="SRX_STRING (optional)")
    stx = models.PositiveIntegerField(null=True, blank=True, help_text="STX (optional)")
    stx_string = models.CharField(max_length=32, blank=True, help_text="STX_STRING (optional)")
    country = models.CharField(max_length=64, blank=True)
    gridsquare = models.CharField(max_length=16, blank=True, help_text="Grid (worked station)")
    name = models.CharField(max_length=64, blank=True, help_text="NAME (operator name of station worked)")
    tx_pwr = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="TX_PWR in watts")
    dxcc = models.PositiveIntegerField(null=True, blank=True, help_text="DXCC entity code (worked)")
    cq_zone = models.PositiveIntegerField(null=True, blank=True, help_text="CQ zone (worked)")
    itu_zone = models.PositiveIntegerField(null=True, blank=True, help_text="ITU zone (worked)")
    iota = models.CharField(max_length=10, blank=True, help_text="IOTA reference (e.g., EU-005)")

    # Station location (MY_*)
    my_dxcc = models.PositiveIntegerField(null=True, blank=True, help_text="MY_DXCC code")
    my_state = models.CharField(max_length=16, blank=True, help_text="MY_STATE (enumerated per ADIF)")
    my_cnty = models.CharField(max_length=32, blank=True, help_text="MY_CNTY (enumerated per ADIF)")
    my_gridsquare = models.CharField(max_length=16, blank=True)
    my_vucc_grids = models.CharField(max_length=64, blank=True)
    my_cq_zone = models.PositiveIntegerField(null=True, blank=True)
    my_itu_zone = models.PositiveIntegerField(null=True, blank=True)
    my_name = models.CharField(max_length=64, blank=True, help_text="MY_NAME (operator name)")

    # QSLing fields
    lotw_qsl_rcvd = models.CharField(max_length=1, blank=True, help_text="LOTW_QSL_RCVD (Y/N/R/I/V)")
    lotw_qsl_rcvd_date = models.DateField(null=True, blank=True)
    lotw_qsl_sent = models.CharField(max_length=1, blank=True, help_text="LOTW_QSL_SENT (Y/N/R/I/V)")
    lotw_qsl_sent_date = models.DateField(null=True, blank=True)

    # Programs (ADIF-compatible)
    sig = models.CharField(max_length=16, blank=True, help_text="SIG (e.g., POTA/SOTA)")
    sig_info = models.CharField(max_length=32, blank=True, help_text="SIG_INFO (e.g., park/summit ref)")
    my_sig = models.CharField(max_length=16, blank=True, help_text="MY_SIG (e.g., POTA/SOTA)")
    my_sig_info = models.CharField(max_length=32, blank=True, help_text="MY_SIG_INFO (e.g., park/summit ref)")
    # SOTA dedicated fields
    sota_ref = models.CharField(max_length=16, blank=True, help_text="SOTA_REF (worked station)")
    my_sota_ref = models.CharField(max_length=16, blank=True, help_text="MY_SOTA_REF")

    notes = models.TextField(blank=True)

    # Link to upload/import batch this entry came from
    upload = models.ForeignKey('LogImport', related_name='entries', null=True, blank=True, on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-qso_date", "-time_on", "callsign"]
        indexes = [
            models.Index(fields=["qso_date", "time_on"], name="qso_datetime_idx"),
            models.Index(fields=["band"], name="qso_band_idx"),
            models.Index(fields=["mode"], name="qso_mode_idx"),
            models.Index(fields=["gridsquare"], name="qso_grid_idx"),
            models.Index(fields=["dxcc"], name="qso_dxcc_idx"),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.callsign} @ {self.qso_date} {self.time_on} ({self.band} {self.mode})"

    # ---- Validation helpers ----
    _CALLSIGN_RE = re.compile(r"^[A-Z0-9/]+$")

    @staticmethod
    def _validate_callsign(value: str, field_name: str) -> str:
        if not value:
            return value
        v = value.strip().upper()
        if len(v) < 3 or len(v) > 20:
            raise ValidationError({field_name: "Callsign length must be 3..20"})
        if not LogEntry._CALLSIGN_RE.match(v):
            raise ValidationError({field_name: "Callsign must contain A-Z, 0-9 or '/' only"})
        if v.startswith("/") or v.endswith("/"):
            raise ValidationError({field_name: "Callsign must not begin or end with '/'"})
        if not any(c.isalpha() for c in v) or not any(c.isdigit() for c in v):
            raise ValidationError({field_name: "Callsign must contain at least one letter and one digit"})
        if v.startswith("0"):
            raise ValidationError({field_name: "Callsign must not begin with 0"})
        if v.startswith("1") and not (v.startswith("1A") or v.startswith("1M") or v.startswith("1S")):
            raise ValidationError({field_name: "Callsign starting with 1 must begin with 1A/1M/1S"})
        return v

    @staticmethod
    def _derive_band_from_freq(freq_mhz: Optional[Decimal]) -> Optional[str]:
        if not freq_mhz:
            return None
        f = float(freq_mhz)
        ranges = [
            ((1.8, 2.0), "160m"),
            ((3.5, 4.0), "80m"),
            ((5.2, 5.5), "60m"),
            ((7.0, 7.3), "40m"),
            ((10.1, 10.15), "30m"),
            ((14.0, 14.35), "20m"),
            ((18.068, 18.168), "17m"),
            ((21.0, 21.45), "15m"),
            ((24.89, 24.99), "12m"),
            ((28.0, 29.7), "10m"),
            ((50.0, 54.0), "6m"),
            ((70.0, 71.0), "4m"),
            ((144.0, 148.0), "2m"),
            ((222.0, 225.0), "1.25m"),
            ((420.0, 450.0), "70cm"),
            ((902.0, 928.0), "33cm"),
            ((1240.0, 1300.0), "23cm"),
        ]
        for (lo, hi), band in ranges:
            if lo <= f <= hi:
                return band
        return None

    def clean(self):
        # Normalize and validate callsigns
        self.callsign = self._validate_callsign(self.callsign, "callsign")
        if self.station_callsign:
            self.station_callsign = self._validate_callsign(self.station_callsign, "station_callsign")
        if self.operator:
            self.operator = self._validate_callsign(self.operator, "operator")

        # BAND/FREQ presence and derivation
        if not self.band and not self.freq:
            raise ValidationError({"band": "One of BAND or FREQ must be present", "freq": "One of BAND or FREQ must be present"})
        if not self.band and self.freq:
            derived = self._derive_band_from_freq(self.freq)
            if derived:
                self.band = derived
            else:
                raise ValidationError({"freq": "Unable to derive BAND from FREQ"})

        # RX fields: derive band_rx if only freq_rx provided
        if not self.band_rx and self.freq_rx:
            drx = self._derive_band_from_freq(self.freq_rx)
            if drx:
                self.band_rx = drx

        # Propagation/Satellite constraints
        if self.prop_mode.upper() == "SAT":
            if not self.sat_name:
                raise ValidationError({"sat_name": "SAT_NAME required when PROP_MODE is SAT"})
        else:
            if self.sat_name:
                raise ValidationError({"sat_name": "SAT_NAME must be omitted unless PROP_MODE is SAT"})

        # If STATION_CALLSIGN absent but OPERATOR present
        if not self.station_callsign and self.operator:
            self.station_callsign = self.operator

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class LogEntryExtras(models.Model):
    entry = models.OneToOneField(LogEntry, related_name="extras", on_delete=models.CASCADE)
    data = models.JSONField(default=dict, blank=True, help_text="Sparse ADIF fields not in core schema")

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Extras for entry {self.entry_id}"


class LogImport(models.Model):
    KIND_FILE = "file"
    KIND_SERVICE = "service"
    KIND_CHOICES = (
        (KIND_FILE, "File Upload"),
        (KIND_SERVICE, "Service Import"),
    )

    FORMAT_ADIF = "adif"
    FORMAT_CABRILLO = "cabrillo"
    FORMAT_OTHER = "other"
    FORMAT_CHOICES = (
        (FORMAT_ADIF, "ADIF"),
        (FORMAT_CABRILLO, "Cabrillo"),
        (FORMAT_OTHER, "Other"),
    )

    kind = models.CharField(max_length=16, choices=KIND_CHOICES)
    format = models.CharField(max_length=16, choices=FORMAT_CHOICES)
    provider = models.CharField(max_length=32, blank=True, help_text="If kind=service, e.g., LOTW, QRZ, ClubLog")
    original_filename = models.CharField(max_length=255, blank=True)
    content_type = models.CharField(max_length=100, blank=True)
    size_bytes = models.BigIntegerField(null=True, blank=True)
    sha256 = models.CharField(max_length=64, blank=True)
    station_callsign = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    meta = models.JSONField(default=dict, blank=True)

    # Import file storage and status
    STATUS_PENDING = "pending"
    STATUS_DONE = "done"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_DONE, "Done"),
        (STATUS_CANCELLED, "Cancelled"),
    )

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PENDING)
    content_gz = models.BinaryField(null=True, blank=True, help_text="Gzipped original ADIF content")
    entry_count = models.PositiveIntegerField(default=0)
    error_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    imported_at = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        label = self.original_filename or self.provider or self.get_format_display()
        return f"{self.get_kind_display()} - {label}"


class StagedEntry(models.Model):
    """Temporary, per-import holding pen for parsed entries before confirmation."""

    imp = models.ForeignKey(LogImport, related_name="staged_entries", on_delete=models.CASCADE)

    # Core identity
    callsign = models.CharField(max_length=20, db_index=True)
    qso_date = models.DateField()
    time_on = models.TimeField()

    # Frequency / Band
    band = models.CharField(max_length=16, blank=True)
    freq = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    band_rx = models.CharField(max_length=16, blank=True)
    freq_rx = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)

    # Mode
    mode = models.CharField(max_length=32)
    submode = models.CharField(max_length=32, blank=True)

    # Propagation / Satellite
    prop_mode = models.CharField(max_length=16, blank=True)
    sat_name = models.CharField(max_length=32, blank=True)

    # Station/operator identity
    station_callsign = models.CharField(max_length=20, blank=True)
    operator = models.CharField(max_length=20, blank=True)

    # RST and other info
    rst_sent = models.CharField(max_length=8, blank=True)
    rst_rcvd = models.CharField(max_length=8, blank=True)
    qso_date_off = models.DateField(null=True, blank=True)
    time_off = models.TimeField(null=True, blank=True)

    # Exchange / contest related
    srx = models.PositiveIntegerField(null=True, blank=True)
    srx_string = models.CharField(max_length=32, blank=True)
    stx = models.PositiveIntegerField(null=True, blank=True)
    stx_string = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=64, blank=True)
    gridsquare = models.CharField(max_length=16, blank=True)
    name = models.CharField(max_length=64, blank=True)
    tx_pwr = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    dxcc = models.PositiveIntegerField(null=True, blank=True)
    cq_zone = models.PositiveIntegerField(null=True, blank=True)
    itu_zone = models.PositiveIntegerField(null=True, blank=True)
    iota = models.CharField(max_length=10, blank=True)

    # Station location (MY_*)
    my_dxcc = models.PositiveIntegerField(null=True, blank=True)
    my_state = models.CharField(max_length=16, blank=True)
    my_cnty = models.CharField(max_length=32, blank=True)
    my_gridsquare = models.CharField(max_length=16, blank=True)
    my_vucc_grids = models.CharField(max_length=64, blank=True)
    my_cq_zone = models.PositiveIntegerField(null=True, blank=True)
    my_itu_zone = models.PositiveIntegerField(null=True, blank=True)
    my_name = models.CharField(max_length=64, blank=True)

    # QSLing fields
    lotw_qsl_rcvd = models.CharField(max_length=1, blank=True)
    lotw_qsl_rcvd_date = models.DateField(null=True, blank=True)
    lotw_qsl_sent = models.CharField(max_length=1, blank=True)
    lotw_qsl_sent_date = models.DateField(null=True, blank=True)

    # Programs
    sig = models.CharField(max_length=16, blank=True)
    sig_info = models.CharField(max_length=32, blank=True)
    my_sig = models.CharField(max_length=16, blank=True)
    my_sig_info = models.CharField(max_length=32, blank=True)
    sota_ref = models.CharField(max_length=16, blank=True)
    my_sota_ref = models.CharField(max_length=16, blank=True)

    notes = models.TextField(blank=True)

    # Extras as JSON to capture any unmodeled ADIF fields
    extras = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-qso_date", "-time_on", "callsign"]
