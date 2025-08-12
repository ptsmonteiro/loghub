from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormView

from .forms import LogEntryForm
from .models import LogEntry, LogEntryExtras
from .adif import queryset_to_adif
from .forms_import import ADIFUploadForm
from .imports import gzip_bytes, parse_adif_to_staged, finalize_import, compute_sha256
from .models import LogImport, StagedEntry


class LogEntryListView(ListView):
    model = LogEntry
    paginate_by = 25
    ordering = ["-qso_date", "-time_on", "callsign"]


class LogEntryDetailView(DetailView):
    model = LogEntry


class LogEntryCreateView(CreateView):
    model = LogEntry
    form_class = LogEntryForm
    success_url = reverse_lazy("logbook:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        extras = form.cleaned_data.get("extras")
        if extras:
            LogEntryExtras.objects.update_or_create(entry=self.object, defaults={"data": extras})
        return response


class LogEntryUpdateView(UpdateView):
    model = LogEntry
    form_class = LogEntryForm
    success_url = reverse_lazy("logbook:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        extras = form.cleaned_data.get("extras")
        if extras:
            LogEntryExtras.objects.update_or_create(entry=self.object, defaults={"data": extras})
        else:
            LogEntryExtras.objects.filter(entry=self.object).delete()
        return response


class LogEntryDeleteView(DeleteView):
    model = LogEntry
    success_url = reverse_lazy("logbook:list")


def logbook_export_adif(_request):
    data = queryset_to_adif(LogEntry.objects.all().order_by("qso_date", "time_on", "callsign"))
    resp = HttpResponse(data, content_type="text/plain; charset=utf-8")
    resp["Content-Disposition"] = "attachment; filename=loghub_export.adi"
    return resp


class ImportCreateView(FormView):
    form_class = ADIFUploadForm
    template_name = "logbook/import_new.html"

    def form_valid(self, form):
        f = form.cleaned_data["file"]
        data = f.read()
        if not data:
            return HttpResponseBadRequest("Empty file")
        content_type = getattr(f, "content_type", "application/octet-stream")
        original_filename = getattr(f, "name", "upload.adi")
        size_bytes = len(data)
        sha256 = compute_sha256(data)
        gz = gzip_bytes(data)

        with transaction.atomic():
            imp = LogImport.objects.create(
                kind=LogImport.KIND_FILE,
                format=LogImport.FORMAT_ADIF,
                provider="",
                original_filename=original_filename,
                content_type=content_type,
                size_bytes=size_bytes,
                sha256=sha256,
                station_callsign=form.cleaned_data.get("station_callsign") or "",
                notes=form.cleaned_data.get("notes") or "",
                content_gz=gz,
                status=LogImport.STATUS_PENDING,
            )
            text = data.decode("utf-8", errors="replace")
            ok, err = parse_adif_to_staged(imp, text)
            imp.entry_count = ok
            imp.error_count = err
            imp.save(update_fields=["entry_count", "error_count"])

        return HttpResponseRedirect(reverse("logbook:import_review", args=[imp.pk]))


class ImportReviewView(ListView):
    model = StagedEntry
    paginate_by = 50
    template_name = "logbook/import_review.html"
    context_object_name = "entries"

    def get_queryset(self):
        self.import_obj = LogImport.objects.get(pk=self.kwargs["pk"])  # type: ignore[attr-defined]
        return self.import_obj.staged_entries.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        imp = self.import_obj

        # Scan the ENTIRE import to discover which fields are used
        qs_all = imp.staged_entries.all()

        # Determine which core fields (model fields) have any non-empty value
        exclude_fields = {"id", "imp", "created_at", "extras"}
        # Grab concrete non-relational fields from model
        core_field_names = [
            f.name
            for f in StagedEntry._meta.get_fields()
            if getattr(f, "concrete", False)
            and not getattr(f, "many_to_many", False)
            and not getattr(f, "is_relation", False)
            and f.name not in exclude_fields
        ]

        present_core: set[str] = set()
        # Stream through values to avoid loading full model instances
        for row in qs_all.values(*core_field_names).iterator():
            # operator_display is derived; mark if either source exists
            if (row.get("operator") or row.get("station_callsign")):
                present_core.add("operator_display")
            for k, v in row.items():
                if v is None:
                    continue
                if isinstance(v, str) and v.strip() == "":
                    continue
                present_core.add(k)

        # Ensure these always show for usability
        present_core.update({"callsign", "qso_date", "time_on"})

        # Collect all extras keys with any non-empty value across the import
        extras_keys_set: set[str] = set()
        for ex in qs_all.values_list("extras", flat=True).iterator():
            if not isinstance(ex, dict):
                continue
            for k, v in ex.items():
                if v is None or str(v).strip() == "":
                    continue
                extras_keys_set.add(str(k).upper())

        # Column ordering: start with a preferred order for common fields, then remaining core fields, then extras
        preferred_order = [
            "operator_display",
            "callsign",
            "name",
            "qso_date",
            "time_on",
            "band",
            "mode",
        ]
        label_map = {
            "callsign": "Callsign",
            "qso_date": "Date",
            "time_on": "Time",
            "band": "Band",
            "band_rx": "Band RX",
            "freq": "Freq",
            "freq_rx": "Freq RX",
            "mode": "Mode",
            "submode": "Submode",
            "operator_display": "Operator",
        }

        def label_for(field: str) -> str:
            return label_map.get(field, field.replace("_", " ").title())

        columns: list[tuple[str, str]] = []
        for f in preferred_order:
            if f in present_core:
                columns.append((f, label_for(f)))

        # Remaining core fields (preserving model declaration order)
        # If we show the synthesized operator_display, hide raw operator/station_callsign
        skip_core = set()
        if "operator_display" in present_core:
            skip_core.update({"operator", "station_callsign"})
        for f in core_field_names:
            if f in preferred_order or f not in present_core or f in skip_core:
                continue
            columns.append((f, label_for(f)))

        # Extras: prioritize a few common ones, then alphabetical
        extras_priority = [
            "GRIDSQUARE",
            "DXCC",
            "CQZ",
            "ITUZ",
            "SIG",
            "SIG_INFO",
            "MY_SIG",
            "MY_SIG_INFO",
            "SOTA_REF",
            "MY_SOTA_REF",
        ]
        for k in extras_priority:
            if k in extras_keys_set:
                columns.append((k, k.replace("_", " ")))
        for k in sorted(extras_keys_set - set(extras_priority)):
            columns.append((k, k.replace("_", " ")))

        ctx.update({
            "import": imp,
            "columns": columns,
        })
        return ctx


def import_confirm(request, pk: int):
    imp = LogImport.objects.get(pk=pk)
    if imp.status != LogImport.STATUS_PENDING:
        return HttpResponseBadRequest("Import not pending")
    created = finalize_import(imp)
    imp.status = LogImport.STATUS_DONE
    from django.utils import timezone

    imp.imported_at = timezone.now()
    imp.entry_count = created
    imp.save(update_fields=["status", "imported_at", "entry_count"])
    return HttpResponseRedirect(reverse("logbook:list"))


def import_cancel(request, pk: int):
    imp = LogImport.objects.get(pk=pk)
    if imp.status != LogImport.STATUS_PENDING:
        return HttpResponseBadRequest("Import not pending")
    imp.staged_entries.all().delete()
    imp.status = LogImport.STATUS_CANCELLED
    imp.save(update_fields=["status"])
    return HttpResponseRedirect(reverse("logbook:list"))


class ImportListView(ListView):
    model = LogImport
    paginate_by = 25
    template_name = "logbook/import_list.html"
    context_object_name = "imports"

    def get_queryset(self):
        qs = LogImport.objects.all().order_by("-created_at")
        if self.request.GET.get("all"):
            return qs
        return qs.filter(status=LogImport.STATUS_PENDING)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["show_all"] = bool(self.request.GET.get("all"))
        return ctx
