from django.urls import path

from . import views


app_name = "qsos"

urlpatterns = [
    path("", views.QSOListView.as_view(), name="list"),
    path("new/", views.QSOCreateView.as_view(), name="create"),
    path("<int:pk>/", views.QSODetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.QSOUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.QSODeleteView.as_view(), name="delete"),
]

