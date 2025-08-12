from django.http import HttpResponseRedirect
from django.urls import include, path


def root_redirect(_request):
    return HttpResponseRedirect("/logbook/")


urlpatterns = [
    path("", root_redirect, name="root"),
    path("logbook/", include("logbook.urls")),
]
