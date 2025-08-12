import datetime as dt
import gzip
import hashlib
import io
import re
from typing import Iterable

from django.db import transaction

from .models import LogEntry, LogEntryExtras, LogImport, StagedEntry
from .adif_fields import CORE_MAP
from .adif_catalog import normalize_extra_value


ADIF_TAG_RE = re.compile(r"<([A-Za-z0-9_]+):([0-9]+)(?::[A-Za-z])?>", re.IGNORECASE)


def gzip_bytes(data: bytes) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(data)
    return buf.getvalue()


def parse_adif_records(data: str) -> Iterable[dict]:
    # Split on <EOR> boundaries; ignore header prior to <EOH>
    parts = data.split("<EOH>")
    body = parts[1] if len(parts) > 1 else parts[0]
    for rec in body.split("<EOR>"):
        rec = rec.strip()
        if not rec:
            continue
        pos = 0
        fields: dict[str, str] = {}
        while True:
            m = ADIF_TAG_RE.search(rec, pos)
            if not m:
                break
            tag = m.group(1).upper()
            length = int(m.group(2))
            val_start = m.end()
            value = rec[val_start : val_start + length]
            fields[tag] = value
            pos = val_start + length
        yield fields


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


# CORE_MAP now provided by adif_fields


def parse_adif_to_staged(imp: LogImport, text: str) -> tuple[int, int]:
    """Parse ADIF text, create StagedEntry rows. Return (ok_count, error_count)."""
    ok = 0
    err = 0
    to_create: list[StagedEntry] = []
    for fields in parse_adif_records(text):
        data: dict = {}
        extras: dict = {}
        for tag, val in fields.items():
            if tag in CORE_MAP:
                mapping = CORE_MAP[tag]
                if isinstance(mapping, tuple):
                    key, caster = mapping
                    try:
                        data[key] = caster(val)
                    except Exception:
                        # Bad cast, keep as extra so user can inspect
                        extras[tag] = val
                else:
                    data[mapping] = val
            else:
                # Normalize per ADIF catalog when possible
                extras[tag] = normalize_extra_value(tag, val)
        # Required minimal fields
        if not data.get("callsign") or not data.get("qso_date") or not data.get("time_on"):
            err += 1
            continue
        se = StagedEntry(imp=imp, **data)
        if extras:
            se.extras = extras
        to_create.append(se)
    # Bulk create in batches
    for i in range(0, len(to_create), 500):
        StagedEntry.objects.bulk_create(to_create[i : i + 500])
    ok += len(to_create)
    return ok, err


@transaction.atomic
def finalize_import(imp: LogImport) -> int:
    """Move staged entries to the main logbook, linking back to the import."""
    count = 0
    for se in imp.staged_entries.all().iterator():
        entry = LogEntry(
            callsign=se.callsign,
            qso_date=se.qso_date,
            time_on=se.time_on,
            band=se.band,
            freq=se.freq,
            band_rx=se.band_rx,
            freq_rx=se.freq_rx,
            mode=se.mode,
            submode=se.submode,
            prop_mode=se.prop_mode,
            sat_name=se.sat_name,
            station_callsign=se.station_callsign,
            operator=se.operator,
            rst_sent=se.rst_sent,
            rst_rcvd=se.rst_rcvd,
            qso_date_off=se.qso_date_off,
            time_off=se.time_off,
            srx=se.srx,
            srx_string=se.srx_string,
            stx=se.stx,
            stx_string=se.stx_string,
            country=se.country,
            gridsquare=se.gridsquare,
            name=se.name,
            tx_pwr=se.tx_pwr,
            dxcc=se.dxcc,
            cq_zone=se.cq_zone,
            itu_zone=se.itu_zone,
            iota=se.iota,
            my_dxcc=se.my_dxcc,
            my_state=se.my_state,
            my_cnty=se.my_cnty,
            my_gridsquare=se.my_gridsquare,
            my_vucc_grids=se.my_vucc_grids,
            my_cq_zone=se.my_cq_zone,
            my_itu_zone=se.my_itu_zone,
            my_name=se.my_name,
            lotw_qsl_rcvd=se.lotw_qsl_rcvd,
            lotw_qsl_rcvd_date=se.lotw_qsl_rcvd_date,
            lotw_qsl_sent=se.lotw_qsl_sent,
            lotw_qsl_sent_date=se.lotw_qsl_sent_date,
            sig=se.sig,
            sig_info=se.sig_info,
            my_sig=se.my_sig,
            my_sig_info=se.my_sig_info,
            sota_ref=se.sota_ref,
            my_sota_ref=se.my_sota_ref,
            notes=se.notes,
            upload=imp,
        )
        entry.save()
        if se.extras:
            LogEntryExtras.objects.create(entry=entry, data=se.extras)
        count += 1
    # Clear staged entries after finalization
    imp.staged_entries.all().delete()
    return count


def compute_sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()
