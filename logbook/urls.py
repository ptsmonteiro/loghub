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
    # Imports
    path("imports/new/", views.ImportCreateView.as_view(), name="import_new"),
    path("imports/", views.ImportListView.as_view(), name="import_list"),
    path("imports/<int:pk>/review/", views.ImportReviewView.as_view(), name="import_review"),
    path("imports/<int:pk>/confirm/", views.import_confirm, name="import_confirm"),
    path("imports/<int:pk>/cancel/", views.import_cancel, name="import_cancel"),
]
