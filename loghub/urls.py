from django.http import HttpResponseRedirect
from django.urls import include, path


def root_redirect(_request):
    return HttpResponseRedirect("/qsos/")


urlpatterns = [
    path("", root_redirect, name="root"),
    path("qsos/", include("qsos.urls")),
]
