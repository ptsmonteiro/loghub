from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import QSOForm
from .models import QSO


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

