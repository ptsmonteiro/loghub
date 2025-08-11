from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import QSOForm
from .models import QSO
from .adif import queryset_to_adif


class QSOListView(ListView):
    model = QSO
    paginate_by = 25


class QSODetailView(DetailView):
    model = QSO


class QSOCreateView(CreateView):
    model = QSO
    form_class = QSOForm
    success_url = reverse_lazy("qsos:list")


class QSOUpdateView(UpdateView):
    model = QSO
    form_class = QSOForm
    success_url = reverse_lazy("qsos:list")


class QSODeleteView(DeleteView):
    model = QSO
    success_url = reverse_lazy("qsos:list")


def qsos_export_adif(_request):
    data = queryset_to_adif(QSO.objects.all().order_by("qso_date", "time_on", "callsign"))
    resp = HttpResponse(data, content_type="text/plain; charset=utf-8")
    resp["Content-Disposition"] = "attachment; filename=loghub_export.adi"
    return resp
