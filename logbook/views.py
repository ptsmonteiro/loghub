from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import LogEntryForm
from .models import LogEntry, LogEntryExtras
from .adif import queryset_to_adif


class LogEntryListView(ListView):
    model = LogEntry
    paginate_by = 25


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

