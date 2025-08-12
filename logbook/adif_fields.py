"""
Central ADIF field mapping for core columns and minimal typing.

This keeps TAG -> model field mapping in one place so we can:
- Parse ADIF into core fields vs JSON extras
- Avoid storing extras that duplicate core columns
- Drive labels/help later if needed
"""

from decimal import Decimal
import datetime as dt
from typing import Callable, Tuple, Union


def _to_date(s: str | None) -> dt.date | None:
    if not s:
        return None
    try:
        return dt.datetime.strptime(s, "%Y%m%d").date()
    except Exception:
        return None


def _to_time(s: str | None) -> dt.time | None:
    if not s:
        return None
    try:
        # Accept 4 or 6 digits
        if len(s) == 4:
            return dt.datetime.strptime(s, "%H%M").time()
        return dt.datetime.strptime(s, "%H%M%S").time()
    except Exception:
        return None


# TAG -> model field name or (field, caster)
CORE_MAP: dict[str, Union[str, Tuple[str, Callable[[str], object]]]] = {
    "CALL": "callsign",
    "QSO_DATE": ("qso_date", _to_date),
    "TIME_ON": ("time_on", _to_time),
    "QSO_DATE_OFF": ("qso_date_off", _to_date),
    "TIME_OFF": ("time_off", _to_time),
    "BAND": "band",
    "FREQ": ("freq", Decimal),
    "BAND_RX": "band_rx",
    "FREQ_RX": ("freq_rx", Decimal),
    "MODE": "mode",
    "SUBMODE": "submode",
    "PROP_MODE": "prop_mode",
    "SAT_NAME": "sat_name",
    "STATION_CALLSIGN": "station_callsign",
    "OPERATOR": "operator",
    "RST_RCVD": "rst_rcvd",
    "RST_SENT": "rst_sent",
    "SRX": ("srx", int),
    "SRX_STRING": "srx_string",
    "STX": ("stx", int),
    "STX_STRING": "stx_string",
    "GRIDSQUARE": "gridsquare",
    "SIG": "sig",
    "SIG_INFO": "sig_info",
    "MY_SIG": "my_sig",
    "MY_SIG_INFO": "my_sig_info",
    "SOTA_REF": "sota_ref",
    "MY_SOTA_REF": "my_sota_ref",
    "NAME": "name",
    "TX_PWR": ("tx_pwr", Decimal),
    "COUNTRY": "country",
    "DXCC": ("dxcc", int),
    "IOTA": "iota",
    "CQZ": ("cq_zone", int),
    "ITUZ": ("itu_zone", int),
    "MY_DXCC": ("my_dxcc", int),
    "MY_STATE": "my_state",
    "MY_CNTY": "my_cnty",
    "MY_GRIDSQUARE": "my_gridsquare",
    "MY_VUCC_GRIDS": "my_vucc_grids",
    "MY_CQ_ZONE": ("my_cq_zone", int),
    "MY_ITU_ZONE": ("my_itu_zone", int),
    "MY_NAME": "my_name",
    "LOTW_QSL_RCVD": "lotw_qsl_rcvd",
    "LOTW_QSLRDATE": ("lotw_qsl_rcvd_date", _to_date),
    "LOTW_QSL_SENT": "lotw_qsl_sent",
    "LOTW_QSLSDATE": ("lotw_qsl_sent_date", _to_date),
    "NOTES": "notes",
}

# Convenience sets for quick checks
CORE_TAGS: set[str] = set(CORE_MAP.keys())
CORE_FIELD_NAMES: set[str] = set(v[0] if isinstance(v, tuple) else v for v in CORE_MAP.values())

