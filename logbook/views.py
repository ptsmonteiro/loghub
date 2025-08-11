from __future__ import annotations

from datetime import datetime
from decimal import Decimal, InvalidOperation

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Upload, QSO


def parse_adif(content: str):
    records = []
    for raw in content.split("<eor>"):
        raw = raw.strip()
        if not raw:
            continue
        data: dict[str, str] = {}
        while "<" in raw:
            start = raw.find("<")
            end = raw.find(">", start)
            if end == -1:
                break
            tag_def = raw[start + 1 : end]
            parts = tag_def.split(":", 2)
            tag = parts[0].upper()
            length = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
            raw = raw[end + 1 :]
            if length is not None:
                value = raw[:length]
                raw = raw[length:]
            else:
                idx = raw.find("<")
                value = raw[:idx] if idx != -1 else raw
                raw = raw[idx:] if idx != -1 else ""
            data[tag] = value.strip()
        if data:
            records.append(data)
    return records


@csrf_exempt
def upload_adif(request):
    if request.method != "POST":
        return HttpResponse(status=405)
    adif_file = request.FILES.get("adif")
    if not adif_file:
        return JsonResponse({"error": "adif file required"}, status=400)
    text = adif_file.read().decode("utf-8", errors="ignore")
    records = parse_adif(text)
    if not records:
        return JsonResponse({"error": "no qsos found"}, status=400)
    station_callsign = request.POST.get("station_callsign")
    if any("STATION_CALLSIGN" not in r for r in records) and not station_callsign:
        return JsonResponse({"error": "station_callsign required"}, status=400)

    required = ["CALL", "QSO_DATE", "TIME_ON", "MODE"]
    for r in records:
        if (
            any(f not in r or not r[f] for f in required)
            or ("BAND" not in r and "FREQ" not in r)
        ):
            return JsonResponse({"error": "missing required qso fields"}, status=400)
    upload = Upload.objects.create()
    created = 0
    for r in records:
        sc = r.get("STATION_CALLSIGN", station_callsign)
        date_str = r.get("QSO_DATE")
        time_str = r.get("TIME_ON")
        qso_date = None
        time_on = None
        freq = None
        if date_str:
            try:
                qso_date = datetime.strptime(date_str, "%Y%m%d").date()
            except ValueError:
                pass
        if time_str:
            try:
                fmt = "%H%M%S" if len(time_str) == 6 else "%H%M"
                time_on = datetime.strptime(time_str, fmt).time()
            except ValueError:
                pass
        freq_str = r.get("FREQ")
        if freq_str:
            try:
                freq = Decimal(freq_str)
            except (InvalidOperation, ValueError):
                pass
        QSO.objects.create(
            upload=upload,
            call=r.get("CALL", ""),
            station_callsign=sc or "",
            qso_date=qso_date,
            time_on=time_on,
            freq=freq,
            band=r.get("BAND", ""),
            mode=r.get("MODE", ""),
        )
        created += 1
    return JsonResponse({"upload_id": upload.id, "created_qsos": created})
