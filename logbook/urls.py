from django.urls import path

from . import views


app_name = "logbook"

urlpatterns = [
    path("", views.LogEntryListView.as_view(), name="list"),
    path("new/", views.LogEntryCreateView.as_view(), name="create"),
    path("<int:pk>/", views.LogEntryDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.LogEntryUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.LogEntryDeleteView.as_view(), name="delete"),
    path("export.adif", views.logbook_export_adif, name="export_adif"),
]

