import re
from decimal import Decimal
from typing import Optional

from django.core.exceptions import ValidationError
from django.db import models


class QSO(models.Model):
    """QSO model following LoTW-relevant ADIF fields and constraints."""

    # Core QSO identity
    callsign = models.CharField(max_length=20, db_index=True, help_text="CALL: Station worked")
    qso_date = models.DateField(help_text="QSO_DATE: UTC date contact established")
    time_on = models.TimeField(help_text="TIME_ON: UTC time contact established")

    # Frequency / Band (one of BAND or FREQ must be present)
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
    country = models.CharField(max_length=64, blank=True)
    gridsquare = models.CharField(max_length=16, blank=True, help_text="Grid (worked station)")

    # Station location (MY_*)
    my_dxcc = models.PositiveIntegerField(null=True, blank=True, help_text="MY_DXCC code")
    my_state = models.CharField(max_length=16, blank=True, help_text="MY_STATE (enumerated per ADIF)")
    my_cnty = models.CharField(max_length=32, blank=True, help_text="MY_CNTY (enumerated per ADIF)")
    my_gridsquare = models.CharField(max_length=16, blank=True)
    my_vucc_grids = models.CharField(max_length=64, blank=True)
    my_cq_zone = models.PositiveIntegerField(null=True, blank=True)
    my_itu_zone = models.PositiveIntegerField(null=True, blank=True)

    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-qso_date", "-time_on", "callsign"]

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
        if not QSO._CALLSIGN_RE.match(v):
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
            # If not SAT, clear SAT_NAME if present but allow keeping it blank
            if self.sat_name:
                raise ValidationError({"sat_name": "SAT_NAME must be omitted unless PROP_MODE is SAT"})

        # If STATION_CALLSIGN absent but OPERATOR present, per ADIF treat OPERATOR as station callsign
        if not self.station_callsign and self.operator:
            self.station_callsign = self.operator

    def save(self, *args, **kwargs):
        # Ensure validation and derivations run on save from any path
        self.full_clean()
        return super().save(*args, **kwargs)
